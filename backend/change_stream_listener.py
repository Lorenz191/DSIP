import django
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import os
from dotenv import load_dotenv
import asyncio
import json
from channels.layers import get_channel_layer

load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()


async def watch_votes():
    client = MongoClient(
        f"mongodb+srv://{os.getenv('MONGO_UN')}:{os.getenv('MONGO_KEY')}@cluster0.ze7ad.mongodb.net/?retryWrites=true&w=majority"
    )
    db = client["DSIP"]
    post_collection = db["Post"]

    try:
        with post_collection.watch() as stream:
            for change in stream:
                if change["operationType"] in ["update", "replace"]:
                    document_id = change["documentKey"]["_id"]
                    document = post_collection.find_one({"_id": document_id})
                    if document:
                        channel_layer = get_channel_layer()
                        await channel_layer.group_send(
                            "votes",
                            {
                                "type": "vote_update",
                                "message": json.dumps(
                                    {
                                        "post_id": str(document["_id"]),
                                        "upvotes": document.get("upvotes", []),
                                        "downvotes": document.get("downvotes", []),
                                    }
                                ),
                            },
                        )
    except PyMongoError as e:
        print(f"Error watching change stream: {e}")


if __name__ == "__main__":
    asyncio.run(watch_votes())
