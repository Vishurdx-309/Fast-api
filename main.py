from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import Basemodel, Field, computed_field
from typing import Annotated, Literal
import json

with open("patients.json", "r") as file:
    data = json.load(file)

app = FastAPI()

class Patient(Basemodel):
    id : Annotated[str, Field(..., description = 'ID OF THE PATIENT', examples = ['P001'])]
    name : Annotated[str, Field(...,description = 'NAME OF THE PATEINT', examples = ['Vishal Bokhare'])]
    age : Annotated[int, Field(...,gt = 0, lt = 150,description = 'AGE OF THE PATEINT', examples = [20])]
    gender : Annotated[Literal['male','female','others'],Field(...,description='gender of the pateint')]
    phone : Annotated[str, Field(...,description = 'Phone number insaan ka 10 letters wala hi hona')]
    address : str
    # diseases : list
    height_cm : Annotated[float,Field(...,gt = 0,description='height in cm')]
    weight_kg : Annotated[float,Field(...,gt = 0,description='weight in kg')]
    
# bmi ko inpit data se calculate kardege


    @computed_field 
    @property
    def bmi(self) -> float:
        bmi = round(self.weight_kg/self.height_cm)
        return bmi
     
    
@app.get("/")

def hello():
    return {'message':' Doctor\'s Patient Management System API Testing '}

@app.get("/about")

def about():
    return {'message':' Manage Records of the patients of the doctor'}

@app.get("/view")

def view():
    return data


@app.get("/view/sort")

def sort_patients(sort_by: str = Query(..., description = 'Sort on the basis of Hieght, Wieght or B MI'), 
                  order : str = Query("asc",description = 'sort by ascending or descending order')):
    
    valid_fields = ["height_cm" , "weight_kg" , "bmi", "age"]
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code = 400, detail = f"Invalid fields select from {valid_fields}")
    
    if(order not in ["asc","desc"]):
        raise HTTPException(status_code = 400, detail = "Invalid fields select between asc or desc")
    
    sort_order = True if order == "desc" else False
        
    sorted_data = sorted(data.values(), key= lambda x : x.get(sort_by,0), reverse= sort_order)
    
    return sorted_data

@app.get("/view/{patient_id}")

def view_id(patient_id: str = Path(...,description = 'ID of the patient to view details', example = 'P001')):
    # Check if patient exists
    if patient_id in data:
        return data[patient_id]
    # If not found, return error
    raise HTTPException(status_code = 404 , detail = 'Pateint not found')
        
        
# post ka endpoint create karna hai ab
