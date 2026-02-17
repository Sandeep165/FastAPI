from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: Annotated[ 
        str,
        # field is used to provide additional information about the field such as validation rules, description, examples etc.
        Field(
            min_length=3,
            max_length=50,
            description="Name of the patient",
            json_schema_extra={"examples": ["Vikram Patel"]},
        ),
    ]
    gmail: Annotated[
        Optional[EmailStr],
        Field(
            default=None,
            description="Email of the patient",
            json_schema_extra={"example": "vikram.patel@example.com"},
        ),
    ]
    age: Annotated[
        int ,
        Field(
            gt=0,
            le=120,
            description="Age of the patient"
            )
        ]  
    weight: Annotated[
        int ,
        Field(
            gt=0,
            description="Weight of the patient"
            )
        ]
    
    height: Annotated[
        Optional[int],  
        Field(
            default=None,
            gt=0,
            description="Height of the patient in cm"
        )
    ]
    is_married: Annotated[
        Optional[bool] ,
        Field(
            description="Marital status of the patient",
            default=False
            )
        ]      
    allergies: Annotated[
        List[str],
        Field(
            description="Allergies of the patient",
            example=["dust", "AC"] # using example is deprecated in pydantic v2, we have to use json_schema_extra to provide example
        )
    ]
    contact_details : Annotated[
        Dict[str,str],
        Field(
            description="Contact details of the patient",
            example={"phone":"+91 9892775564","email":"vikram.patel@example.com"}
        )
    ]
    
    '''
    field validator is used to create custom validation for a specific field in the model. It is a class method that takes the value of the field as an argument and performs validation on it.
    If the validation fails, it raises a ValueError with an appropriate error message.
    bydefault, the field validator runs before the standard validation of the field, but we can change this behavior by setting the mode parameter to "after" or "wrap".
    '''
    @field_validator("gmail",mode="after") 
    @classmethod
    def validate_gmail(cls, value):
        valid_domain = ["gmail.com","yahoo.com"]
        result = value.split("@")
        if result[-1] not in valid_domain:
            raise ValueError("Domain is not authenticate ")
        else :
            print("valid domain")
            
    
    '''
    model validator is used to create custom validation for the entire model. 
    It is a class method that takes the values of all the fields in the model as an argument and performs validation on them.
    If the validation fails, it raises a ValueError with an appropriate error message.
    '''
    @model_validator(mode="after")
    def validate_emergency_contact(cls, model):
        if model.age > 60 and "emergency_contact" not in model.contact_details:
            raise ValueError("Emergency contact is required for patients above 60 years old")   
        return model
        
    '''
    computed field is used to create a field that is not stored in the database but is computed based on the values of other fields in the model.
    It is a method that takes the values of other fields as arguments and returns the computed value
    '''
    @computed_field
    def bmi(self) -> Optional[float]:
        if self.height is not None and self.weight is not None:
            height_in_meters = self.height / 100
            bmi_value = self.weight / (height_in_meters ** 2)
            return round(bmi_value, 2)
        return None
    
patient_info = {
    "name": "Vikram Patel",
    "gmail":"test@gmail.com",
    "age": 55,
    "city": "Mumbai",
    "weight": 85,
    "height": 175,
    "allergies": ["dust","AC"],
    "contact_details" : {"phone":"+91 9892775564","email":"vikram.patel@example.com"}
  }

patient1 = Patient(**patient_info)

print(patient1.weight) #it will print None because we have not provided any value for is_married field and it is an optional field
print(patient1.model_dump()) #it will print the data in the form of dict

def get_patient_info(patient : Patient):
    print(f"name of the patient is :- {patient.name}")
    print(f"age of the patient is :- {patient.age}")
    print(f"weight of the patient is :- {patient.weight}")
    print(type(patient.weight))
    
    
# get_patient_info(patient1)