from fastapi import FastAPI, Path, Query, Body, HTTPException
# from pydantic import BaseModel
# from typing import Optional
import json
# class Item(BaseModel):
#     name: str
#     status_code: int

app = FastAPI()

def load_data():
    with open("patients.json", "r" ) as f:
        data = json.load(f)
    return data

'''
GET /patients → list all

GET /patients/{id} → return single record

POST /patients → add new record

PUT /patients/{id} → update record

DELETE /patients/{id} → delete record

'''
@app.get("/")
def home():
    return{"message" : f"Welcome to the Patient Detail application! This is the home page."}

@app.get("/about-us")
def about_us():
    return {"message" : "Welcome to our first demo project"}

@app.get("/patients")
def view():
    data = load_data()
    return data

@app.get("/patients/{patient_id}")
def get_patient_details(patient_id : str = Path(..., description="The ID of the patient to retrieve", example="P001")):
    patient_data = load_data()
    if patient_id in patient_data:
        return patient_data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort")
def sort_patients(sort_by :str = Query(...,description="Sort on the base of age and weight"), order :str = Query("Asc",description="sort in Asc or Desc")):
    valid_fields = ["age", "weight"]
    order_list = ["Asc", "Desc"]
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f"Entered field is not from {valid_fields}")
    
    if order not in order_list:
        raise HTTPException(status_code=400, detail=f"order is not from {order_list}")
    
    sort_order = True if order == "Desc" else False
    
    data = load_data()
    result = sorted(data.items(), key=lambda x: x[1][sort_by], reverse=sort_order)
    return result