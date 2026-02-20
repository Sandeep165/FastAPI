from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field, computed_field
from fastapi.responses import JSONResponse
from typing import Literal, Annotated,Optional
import json

class Patient(BaseModel):
    id : Annotated[str, Field(..., description="ID of the patient", examples=["P001"])]
    name : Annotated[str, Field(...,description="Name of the patient", examples=["John Doe"])]
    age : Annotated[int, Field(...,description="Age of the patient", gt= 0, lt=120)]
    gender : Annotated[Literal["Male", "Female", "Other"], Field(..., description="Gender of the patient")]
    city : Annotated[str, Field(..., description="City of the patient", examples=["New York"])]
    weight : Annotated[float, Field(..., description="Weight of the patient in kg", gt=0)]  
    height : Annotated[float, Field(..., description="Height of the patient in meters", gt=0)]
    
    @computed_field
    @property
    def bmi(self)-> float:
        return round(self.weight / ((self.height/100) ** 2), 2)
    
    @computed_field
    @property
    def verdict(self)-> str:
        bmi_value = self.bmi
        if bmi_value < 18.5:
            return "Underweight"
        elif 18.5 <= bmi_value < 25:
            return "Normal weight"
        elif 25 <= bmi_value < 30:
            return "Overweight"
        else:
            return "Obese"

class Update_patient(BaseModel):
    name : Annotated[Optional[str], Field(default=None)]
    age : Annotated[Optional[int], Field(default=None, gt= 0, lt=120)]
    gender : Annotated[Optional[Literal["Male", "Female", "Other"]], Field(default=None)]
    city : Annotated[Optional[str], Field(default=None)]                
    weight : Annotated[Optional[float], Field(default=None, gt=0)]
    height : Annotated[Optional[float], Field(default=None, gt=0)]  
    
'''
GET /patients → list all

GET /patients/{id} → return single record

POST /patients → add new record

PUT /patients/{id} → update record

DELETE /patients/{id} → delete record

''' 
   
app = FastAPI()

def load_data():
    with open("patients.json", "r" ) as f:
        data = json.load(f)
    return data

def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data,f)


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

@app.post("/Create")
def create_patient(patient: Patient):
    '''
    Docstring for create_patient
    :type patient: Patient pydantic model
    '''
    #load the data
    data = load_data()
    
    #check patient id is already exist
    if patient.id in data:
        raise HTTPException(status_code=400,detail="Patient already exist with same patient ID")
    
    #Create new patient for new patient ID
    data[patient.id] = patient.model_dump(exclude={"id"})
    
    #save the entry of new patient in JSON
    save_data(data)
    # return the response after creating the patient data for the given patient id
    return JSONResponse(status_code=201, content="Patient added successfully")

@app.put("/update/{patient_id}")
def update_patient(patient_id : str, patient: Update_patient):
    '''
    Docstring for update_patient
    
    :param patient_id: Description
    :type patient_id: str
    :param patient: Description
    :type patient: Update_patient
    '''
    #load the data
    data = load_data()
    #check patient id is already exist
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found in the data")
    
    # load the existing data for the given patient id
    existing_data = data[patient_id]
    
    # store the updated data for the given patient id in the current_data variable
    current_data = patient.model_dump(exclude_unset=True)
    
    # update the existing data with the current data for the given patient id
    for key, value in current_data.items():
        existing_data[key] = value 
        
    existing_data["id"] = patient_id 
    patient_pydantic_obj = Patient(**existing_data)
    
    existing_data = patient_pydantic_obj.model_dump(exclude={"id"}) 
    
    data[patient_id] = existing_data 
    
    #save the data after updating the patient data for the given patient id
    save_data(data)
    
    # return the response after updating the patient data for the given patient id
    return JSONResponse(status_code=200, content="Patient updated successfully")


@app.delete("/delete/{patient_id}")
def delete_patient(patient_id : str):
    '''
    Docstring for delete_patient
    
    :param patient_id: Description
    :type patient_id: str
    '''
    #load the data
    data = load_data()
    #check patient id is already exist
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient ID not found in data")
    # delete the patient data for the given patient id
    del data[patient_id]
    #save the data after deleting the patient data for the given patient id
    save_data(data)
    # return the response after deleting the patient data for the given patient id
    return JSONResponse(status_code=200,content="Patient deleted successfully")
    
