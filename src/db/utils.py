from pymongo import MongoClient
from bson.objectid import ObjectId

from src.common.utils.constants import DB_CONNECTION_LINK

client = MongoClient(DB_CONNECTION_LINK)
database = client.property_management

property_collection = database.get_collection("properties")


def property_helper(property) -> dict:
    return {
        "id": str(property["_id"]),
        "property_name": property["property_name"],
        "address": property["address"],
        "city": property["city"],
        "state": property["state"]
    }
