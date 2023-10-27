from fastapi import FastAPI
import uvicorn
import urllib
from pymongo import MongoClient

class Database:
    def __init__(self, connection_string, db_name):
        self.client = MongoClient(connection_string)
        self.db = self.client.get_database(db_name)

app = FastAPI()

mongoDbString = "mongodb+srv://<username>:<password>@devfest.gpvcsdk.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp"

escaped_username = urllib.parse.quote_plus("devfest")
escaped_password = urllib.parse.quote_plus("gdgbbsr-devfest")
mongoDbString = mongoDbString.replace("<username>", escaped_username).replace("<password>", escaped_password)

database = Database(mongoDbString, "DevFest2023")

@app.get("/")
def index():
    return {"backend status": "running"}

# get api to return all records of the collection
@app.get("/registrations")
def get_registrations():
    collection = database.db["member-registrations"]
    data = collection.find()
    
    serialized_data = []
    for item in data:
        serialized_item = {
            "_id": str(item["_id"]),
            "name": item.get("name", ""),
            "emailAddress": item.get("emailAddress", ""),
            "workEmailAddress": item.get("workEmailAddress", ""),
            "occupation": item.get("occupation", ""),
            "designation": item.get("designation", ""),
            "nameInstitute": item.get("nameInstitute", ""),
            "gender": item.get("gender", ""),
            "city": item.get("city", ""),
            "is_paid": item.get("is_paid", ""),
            "check_in": item.get("check_in", ""),
            "is_paid": item.get("is_paid", ""),
            "lunch": item.get("lunch", ""),
            "swag": item.get("swag", ""),
            "unique_id": item.get("unique_id", ""),
            
            
        }
        serialized_data.append(serialized_item)
    
    return {"data": serialized_data}

# put api to take unique_id, search user and change check_in status
@app.put("/checkin/{unique_id}")
def checkin(unique_id: str):
    collection = database.db["member-registrations"]
    data = collection.find_one({"unique_id": unique_id})
    if data:
        collection.update_one({"unique_id": unique_id}, {"$set": {"check_in": True}})
        return {"message": "checkin successful"}
    else:
        return {"message": "user not found"}
    
# put api to take unique_id, search user and change lunch status
@app.put("/lunch/{unique_id}")
def lunch(unique_id: str):
    collection = database.db["member-registrations"]
    data = collection.find_one({"unique_id": unique_id})
    if data:
        collection.update_one({"unique_id": unique_id}, {"$set": {"lunch": True}})
        return {"message": "lunch successful"}
    else:
        return {"message": "user not found"}
    
# put api to take unique_id, search user and change swag status
@app.put("/swag/{unique_id}")
def swag(unique_id: str):
    collection = database.db["member-registrations"]
    data = collection.find_one({"unique_id": unique_id})
    if data:
        collection.update_one({"unique_id": unique_id}, {"$set": {"swag": True}})
        return {"message": "swag successful"}
    else:
        return {"message": "user not found"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)