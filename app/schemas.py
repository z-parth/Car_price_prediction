from pydantic import BaseModel

class CarInput(BaseModel):
    manufacturer: str
    model: str
    engine_size: float
    fuel_type: str
    year_of_manufacture: int
    mileage: int

    
