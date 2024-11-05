from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv("../../../.env")


class DB:
    def __init__(self):
        self.client = MongoClient(
            "mongodb+srv://"
            + os.getenv("MONGO_UN")
            + ":"
            + os.getenv("MONGO_KEY")
            + "@cluster0.ze7ad.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
            server_api=ServerApi("1"),
            tls=True,
            tlsAllowInvalidCertificates=True,
        )
        self.db = self.client["DSIP"]

    def insert_into_user(self, ms_number, is_admin):
        user_collection = self.db["User"]
        if user_collection.find_one({"ms_number": ms_number}):
            return False
        user_document = {"ms_number": ms_number, "is_admin": is_admin}
        result = user_collection.insert_one(user_document)
        return bool(result.inserted_id)

    def insert_into_post(self, fk_author, title, content, is_anonym, status="draft"):
        post_collection = self.db["Post"]
        post_document = {
            "fk_author": fk_author,
            "body": {"title": title, "content": content},
            "upvotes": 0,
            "downvotes": 0,
            "is_anonym": is_anonym,
            "status": status,
            "created_at": datetime.now(),
        }
        result = post_collection.insert_one(post_document)
        return bool(result.inserted_id)

    def select_posts(self):
        post_collection = self.db["Post"]
        posts = post_collection.find()
        return list(posts) if posts else []

    def select_posts_for_user(self, user_id):
        user_collection = self.db["User"]
        user = user_collection.find_one({"_id": user_id})
        if user:
            post_collection = self.db["Post"]
            posts = post_collection.find({"fk_author": user_id})
            result = [
                {
                    "title": post["body"]["title"],
                    "content": post["body"]["content"],
                    "status": post["status"],
                    "created_at": post["created_at"],
                }
                for post in posts
            ]
            return result
        return []

    def select_post_stati(self, user_id):
        user_collection = self.db["User"]
        user = user_collection.find_one({"_id": user_id})
        if not user:
            return []
        post_collection = self.db["Post"]
        posts = post_collection.find({"fk_author": user_id})
        return [
            {"status": post["status"], "title": post["body"]["title"]} for post in posts
        ]

    def update_post_body(self, post_id, title, content):
        post_collection = self.db["Post"]
        result = post_collection.update_one(
            {"_id": post_id}, {"$set": {"body.title": title, "body.content": content}}
        )
        return result.modified_count > 0

    def update_post_status(self, post_id, status):
        post_collection = self.db["Post"]
        result = post_collection.update_one(
            {"_id": post_id}, {"$set": {"status": status}}
        )
        return result.modified_count > 0

    def add_post_votes(self, post_id, vote_type="upvote"):
        post_collection = self.db["Post"]
        update_field = "upvotes" if vote_type == "upvote" else "downvotes"
        result = post_collection.update_one(
            {"_id": post_id}, {"$inc": {update_field: 1}}
        )
        return result.modified_count > 0

    def add_user_vote(self, user_id, post_id, vote_type="upvote"):
        user_collection = self.db["User"]
        update_field = "upvotes" if vote_type == "upvote" else "downvotes"
        if user_collection.find_one(
            {"_id": user_id, update_field: {"$elemMatch": {"post": post_id}}}
        ):
            return False
        user_result = user_collection.update_one(
            {"_id": user_id}, {"$push": {update_field: {"post": post_id}}}
        )
        post_result = self.add_post_votes(post_id, vote_type)
        return user_result.modified_count > 0 and post_result

    def remove_post_vote(self, post_id, vote_type="upvote"):
        post_collection = self.db["Post"]
        update_field = "upvotes" if vote_type == "upvote" else "downvotes"
        result = post_collection.update_one(
            {"_id": post_id}, {"$inc": {update_field: -1}}
        )
        return result.modified_count > 0

    def remove_user_vote(self, user_id, post_id, vote_type="upvote"):
        user_collection = self.db["User"]
        update_field = "upvotes" if vote_type == "upvote" else "downvotes"
        if not user_collection.find_one(
            {"_id": user_id, update_field: {"$elemMatch": {"post": post_id}}}
        ):
            return False
        user_result = user_collection.update_one(
            {"_id": user_id}, {"$pull": {update_field: {"post": post_id}}}
        )
        post_result = self.remove_post_vote(post_id, vote_type)
        return user_result.modified_count > 0 and post_result

    def delete_post(self, post_id):
        post_collection = self.db["Post"]
        result = post_collection.delete_one({"_id": post_id})
        return result.deleted_count > 0

    def delete_user(self, _id):
        user_collection = self.db["User"]
        result = user_collection.delete_one({"_id": _id})
        return result.deleted_count > 0
