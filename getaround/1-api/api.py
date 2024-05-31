from typing import List
import joblib
import pandas as pd
import numpy as np
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import warnings
warnings.filterwarnings("ignore")

class VehicleData(BaseModel):
    age: int
    model_key: str
    mileage: int
    engine_power: int
    fuel: str
    paint_color: str
    car_type: str
    private_parking_available: bool
    has_gps: bool
    has_air_conditioning: bool
    automatic_car: bool
    has_getaround_connect: bool
    has_speed_regulator: bool
    winter_tires: bool

class InputData(BaseModel):
    input: List[VehicleData]

app = FastAPI()

@app.get("/data")
async def load_data():
    data_file_delay = 'https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx'
    data_file_pricing = 'https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv'
    data_delay = pd.read_excel(data_file_delay)
    data_pricing = pd.read_csv(data_file_pricing)
    return data_delay, data_pricing

@app.post("/predict")
async def predict(data: InputData):
    try:
        vehicle_dicts = [vehicle.dict() for vehicle in data.input]
        input_data = pd.DataFrame(vehicle_dicts)
        pricing_model = joblib.load('pricing_model.joblib')
        prediction = pricing_model.predict(input_data)
        response = {
            "prediction": prediction.tolist()
        }
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=4000)