from uuid import uuid4, UUID

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Body
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from src.common.utils.generate_error_details import generate_details
from src.common.utils.generate_logs import logging
from src.db.database import PropertyModel
from src.db.utils import property_collection, property_helper

property_router = APIRouter()


class UpdateItem(BaseModel):
    title: str
    description: str


@property_router.post("/property_upload")
async def property_upload(property: PropertyModel = Body(...)):
    try:
        property.id = uuid4()
        property = jsonable_encoder(property)
        new_property = property_collection.insert_one(property)
        created_property = property_collection.find_one({"_id": new_property.inserted_id})
        return [property_helper(created_property)]

    except Exception:
        error_msg = "property" + str(property.property_name) + "\n"
        logging.warning(error_msg, exc_info=True)
        with open("error.log", "a") as f:
            f.write(
                "================================================================== \n"
            )
        details = generate_details("Internal Server Error", "InternalServerError")
        raise HTTPException(status_code=500, detail=details)


@property_router.get("/property_details")
async def get_all_property_details(city: str):
    try:
        properties = property_collection.find({"city": city})
        property_list = list(properties)
        if property_list:
            return [property_helper(property) for property in property_list]

        else:
            return {"message": f"No properties found in city: {city}"}
        # raise HTTPException(status_code=404, detail=f"No properties found in city: {city}")

    except Exception as e:
        error_msg = (
            f"error +  + {e.message}"
        )
        logging.warning(error_msg, exc_info=True)
        with open("error.log", "a") as f:
            f.write(
                "================================================================== \n"
            )
        details = generate_details(e.message, e.type)
        raise HTTPException(status_code=e.response_code, detail=details)


@property_router.put("/update_item_details/")
async def update_item_details(property_id: str, property: PropertyModel = Body(...)):
    try:
        property = {k: v for k, v in property.dict().items() if v is not None}
        update_result = property_collection.update_one({"_id": ObjectId(property_id)}, {"$set": property})
        if update_result.modified_count == 1:
            updated_property = property_collection.find_one({"_id": ObjectId(property_id)})
            return [property_helper(updated_property)]

        else:
            return {"message": f"Property with id {property_id} not found"}

        # raise HTTPException(status_code=404, detail=f"Property with id {property_id} not found")

    except Exception:
        error_msg = "property" + str(property_id) + "\n"
        logging.warning(error_msg, exc_info=True)
        with open("error.log", "a") as f:
            f.write(
                "================================================================== \n"
            )
        details = generate_details("Internal Server Error", "InternalServerError")
        raise HTTPException(status_code=500, detail=details)


@property_router.get("/get_cities_by_states")
async def get_cities(state: str):
    try:
        cities = property_collection.distinct("city", {"state": state})
        if cities:
            return cities

        else:
            return {"message": f"No properties found in city: {state}"}
        # raise HTTPException(status_code=404, detail=f"No cities found in state: {state}")

    except Exception:
        error_msg = "state" + str(state) + "\n"
        logging.warning(error_msg, exc_info=True)
        with open("error.log", "a") as f:
            f.write(
                "================================================================== \n"
            )
        details = generate_details("Internal Server Error", "InternalServerError")
        raise HTTPException(status_code=500, detail=details)


@property_router.get("/find_similar_properties/")
def find_similar_properties(property_id: str):
    try:
        property_id = UUID(property_id)
        property = property_collection.find_one({"_id": str(property_id)})
        if property:
            properties = property_collection.find({"city": property["city"]})
            return [property_helper(prop) for prop in properties]
        else:
            raise HTTPException(status_code=404, detail=f"No similar properties found in city: {property['city']}")

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    except Exception as e:
        error_msg = f"Error finding similar properties for property_id {property_id}: {str(e)}"
        logging.warning(error_msg, exc_info=True)
        details = {"error": "Internal Server Error", "message": "An unexpected error occurred."}
        raise HTTPException(status_code=500, detail=details)
