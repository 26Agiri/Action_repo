from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["webhook_db"]
collection = db["github_events"]
