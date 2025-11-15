from pydantic import BaseModel, Field

class TravelInfo(BaseModel):
    distance_km: int = Field(description="Distance in km")
    budget: int = Field(description="Budget in USD")
    comfort_level: str = Field(description="Comfort level: low/medium/high")
    group_size: int = Field(description="Number of people")
