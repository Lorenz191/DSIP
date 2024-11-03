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

    def insert_into_user(self, _id, is_admin):
        user_collection = self.db["User"]
        user_document = {"_id": _id, "is_admin": is_admin}
        user_collection.insert_one(user_document)

    def insert_into_post(self, ms_number, is_anonym, post_body):
        post_body_collection = self.db["Post_Body"]
        post_body_document = post_body
        post_body_collection.insert_one(post_body_document)

        post_collection = self.db["Post"]
        post_document = {
            "fk_ms_number": ms_number,
            "fk_body_id": post_body_document["_id"],
            "upvotes": 0,
            "downvotes": 0,
            "is_anonym": is_anonym,
        }
        post_collection.insert_one(post_document)

    def insert_into_comment(self, post_id, text, ms_number):
        comment_collection = self.db["Comment"]
        comment_document = {
            "fk_post_id": post_id,
            "fk_ms_number": ms_number,
            "text": text,
            "created_on": datetime.now(),
        }
        comment_collection.insert_one(comment_document)

    def insert_into_changed_by(self, post_id, post_body_id, ms_number):
        changed_by_collection = self.db["Changed_By"]
        changed_by_document = {
            "pk_fk_post_id": post_id,
            "pk_fk_user_id": ms_number,
            "fk_body_id": post_body_id,
        }
        changed_by_collection.insert_one(changed_by_document)

    def select_posts(self):
        post_collection = self.db["Post"]
        post_body_collection = self.db["Post_Body"]
        posts = post_collection.find()
        result = []
        for post in posts:
            post_body = post_body_collection.find_one({"_id": post["fk_body_id"]})
            if post_body:
                post["body"] = post_body
                result.append(post)
        return result

    def select_comments_for_post(self, post_id):
        comment_collection = self.db["Comment"]
        comments = comment_collection.find({"fk_post_id": post_id})
        return comments

    def select_posts_for_user(self, ms_number):
        post_collection = self.db["Post"]
        post_body_collection = self.db["Post_Body"]
        posts = post_collection.find({"fk_ms_number": ms_number})
        result = []
        for post in posts:
            post_body = post_body_collection.find_one({"_id": post["fk_body_id"]})
            if post_body:
                post_entry = {
                    "post": post_body["heading"],
                    "status": post_body["status"],
                }
                result.append(post_entry)
        return result

    def update_post_body(self, _id, heading, text, ms_number, post_id):
        post_body_collection = self.db["Post_Body"]
        post_body_collection.update_one(
            {"_id": _id}, {"$set": {"heading": heading, "text": text}}
        )
        self.insert_into_changed_by(post_id, _id, ms_number)

    def update_post_body_status(self, _id, status):
        post_body_collection = self.db["Post_Body"]
        post_body_collection.update_one({"_id": _id}, {"$set": {"status": status}})

    def update_comment(self, _id, text):
        comment_collection = self.db["Comment"]
        comment_collection.update_one({"_id": _id}, {"$set": {"text": text}})

    def delete_post(self, _id):
        post_collection = self.db["Post"]
        post_body_collection = self.db["Post_Body"]
        comment_collection = self.db["Comment"]
        changed_by_collection = self.db["Changed_By"]

        post = post_collection.find_one({"_id": _id})
        if post:
            post_body_collection.delete_one({"_id": post["fk_body_id"]})

            comment_collection.delete_many({"fk_post_id": _id})

            changed_by_collection.delete_many({"pk_fk_post_id": _id})

            post_collection.delete_one({"_id": _id})

    def delete_comment(self, _id):
        comment_collection = self.db["Comment"]
        comment_collection.delete_one({"_id": _id})

    def delete_user(self, _id):
        user_collection = self.db["User"]
        user_collection.delete_one({"_id": _id})
