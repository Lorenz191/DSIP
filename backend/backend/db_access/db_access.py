from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables


class DB:
    def __init__(self):
        self.client = MongoClient(
            f"mongodb+srv://{os.getenv('MONGO_UN')}:{os.getenv('MONGO_KEY')}@cluster0.ze7ad.mongodb.net/?retryWrites=true&w=majority",
            server_api=ServerApi("1"),
            tls=True,
            tlsAllowInvalidCertificates=True,
        )
        self.db = self.client["DSIP"]

    # Insert into User
    def insert_into_user(self, user_id, is_admin):
        user_collection = self.db["User"]
        if user_collection.find_one({"uuid": user_id}):
            return False
        user_document = {"uuid": user_id, "is_admin": is_admin}
        result = user_collection.insert_one(user_document)
        return str(result.inserted_id) if result.inserted_id else False

    # Insert into Post
    def insert_into_post(self, post_document):
        post_collection = self.db["Post"]
        result = post_collection.insert_one(post_document)
        return str(result.inserted_id) if result.inserted_id else False

    # Select all Posts
    def select_posts(self):
        post_collection = self.db["Post"]
        posts = post_collection.find()
        return list(posts) if posts else []

    # Select Post by ID
    def select_post_by_id(self, post_id):
        post_collection = self.db["Post"]
        try:
            object_id = ObjectId(post_id)
            post = post_collection.find_one({"_id": object_id})
            return post
        except Exception as e:
            print(f"Error selecting post by ID: {e}")
            return None

    # Select Posts for a specific User
    def select_posts_for_user(self, user_id):
        try:
            user_id = ObjectId(user_id)
            post_collection = self.db["Post"]
            posts = post_collection.find({"fk_author": user_id})
            return [
                {
                    "title": post["body"]["title"],
                    "content": post["body"]["content"],
                    "status": post["status"],
                    "created_at": post["created_at"],
                }
                for post in posts
            ]
        except Exception as e:
            print(f"Error selecting posts for user: {e}")
            return []

    # Select Post Statuses for a specific User
    def select_post_stati(self, user_id):
        try:
            user_id = ObjectId(user_id)
            post_collection = self.db["Post"]
            posts = post_collection.find({"fk_author": user_id})
            return [
                {"status": post["status"], "title": post["body"]["title"]}
                for post in posts
            ]
        except Exception as e:
            print(f"Error selecting post statuses: {e}")
            return []

    # Update Post Body
    def update_post_body(self, post_id, body):
        try:
            post_id = ObjectId(post_id)
            post_collection = self.db["Post"]
            result = post_collection.update_one(
                {"_id": post_id},
                {
                    "$set": {
                        "body.title": body.get("title"),
                        "body.content": body.get("content"),
                    }
                },
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating post body: {e}")
            return False

    # Update Post Status
    def update_post_status(self, post_id, status):
        try:
            post_id = ObjectId(post_id)
            post_collection = self.db["Post"]
            result = post_collection.update_one(
                {"_id": post_id}, {"$set": {"status": status}}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating post status: {e}")
            return False

    # Add Votes to a Post
    def add_post_votes(self, post_id, user_id, vote_type="upvote"):
        try:
            post_id = ObjectId(post_id)
            user_id = ObjectId(user_id)
            post_collection = self.db["Post"]

            update_field = "upvotes" if vote_type == "upvote" else "downvotes"

            existing_vote = post_collection.find_one(
                {"_id": post_id, update_field: {"$elemMatch": {"user": user_id}}}
            )

            print(existing_vote)

            if existing_vote:
                return False

            result = post_collection.update_one(
                {"_id": post_id}, {"$push": {update_field: {"user": user_id}}}
            )

            return result.modified_count > 0

        except Exception as e:
            print(f"Error adding vote: {e}")
            return False

    def remove_post_vote(self, post_id, user_id, vote_type="upvote"):
        try:
            post_id = ObjectId(post_id)
            user_id = ObjectId(user_id)
            post_collection = self.db["Post"]

            update_field = "upvotes" if vote_type == "upvote" else "downvotes"

            # Check if the user has voted
            existing_vote = post_collection.find_one(
                {"_id": post_id, update_field: {"$elemMatch": {"user": user_id}}}
            )

            if not existing_vote:
                return False

            result = post_collection.update_one(
                {"_id": post_id}, {"$pull": {update_field: {"user": user_id}}}
            )

            return result.modified_count > 0

        except Exception as e:
            print(f"Error removing vote: {e}")
            return False

    # Delete a Post
    def delete_post(self, post_id):
        try:
            post_id = ObjectId(post_id)
            post_collection = self.db["Post"]
            result = post_collection.delete_one({"_id": post_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting post: {e}")
            return False

    # Delete a User
    def delete_user(self, user_id):
        try:
            user_id = ObjectId(user_id)
            user_collection = self.db["User"]
            result = user_collection.delete_one({"_id": user_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
