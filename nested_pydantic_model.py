from pydantic import BaseModel


class Address(BaseModel):
    city: str
    state : str
    pincode: int
  
    
class Patient(BaseModel):
    name: str
    age: int
    address : Address  

adress_val = {"city": "Mumbai", "state": "Maharashtra", "pincode": 400001}
address1 = Address(**adress_val)

patient_val = {"name": "Vikram Patel", "age": 55, "address": address1}
patient1 = Patient(**patient_val)


print(patient1.address.city) # it will print Mumbai
print(address1.state) # it will print Maharashtra

'''
Serialization is the process of converting a Python object into a format that can be easily stored or transmitted, such as JSON or dict.
Deserialization is the process of converting a serialized format back into a Python object.
# '''
print(patient1.model_dump()) # it will print the data in the form of dict
print(patient1.model_dump_json()) # it will print the data in the form of json string

print(patient1.model_dump(exclude={"age"})) # it will print the data in the form of dict but it will exclude the age field
print(patient1.model_dump_json(exclude={"age"})) # it will print the data in the form of json string but it will exclude the age field

print(patient1.model_dump(include={"name","address"})) # it will print the data in the form of dict but it will include only name and address field
print(patient1.model_dump_json(include={"name","address"})) # it will print the data in the form of json string but it will include only name and address field