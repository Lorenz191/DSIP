from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv("../../../.env")


class DB:
    def __init__(self):
        client = MongoClient(
            "mongodb+srv://"
            + os.getenv("MONGO_UN")
            + ":"
            + os.getenv("MONGO_KEY")
            + "@cluster0.ze7ad.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
            server_api=ServerApi("1"),
            tls=True,
            tlsAllowInvalidCertificates=True,
        )
