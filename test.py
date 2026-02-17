from pydantic import BaseModel, EmailStr, Field
from typing import List, Dict, Optional, Annotated


class Patient(BaseModel):
    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=50,
            description="Name of the patient",
            examples=["Vikram Patel"],
        ),
    ]  # it will validate the data is str and also validate the length of the string should be between 3 and 50
    age: int
    weight: int
    city: Optional[str] = None
    allergies: List[
        str
    ]  # it will not only validate the data is list but also validate the data type of each element in the list
    contact_details: Dict[
        str, str
    ]  # it will validate the data is dict and also validate the data type of key and value in the dict


patient_info = {
    "name": "Vikram Patel",
    "age": 55,
    "city": "Mumbai",
    "weight": 85,
    "allergies": ["dust", "AC"],
    "contact_details": {"phone": "+91 9892775564"},
}

# patient1 = Patient(**patient_info)
# print(patient1.weight) #it will print None because we have not provided any value for is_married field and it is an optional field
# print(patient1.model_dump()) #it will print the data in the form of dict

value = "test@gmail.com"


def validate_gmail(value):
    result = value.split("@")
    print(result)
    # if  result[-1] != "gmail.com":
    if not value.endswith("@gmail.com"):
        raise ValueError("Email must be a Gmail address")
    return "valid email address"


print(validate_gmail(value))
