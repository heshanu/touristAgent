from pydantic import BaseModel, Field

class DrinkInfo(BaseModel):
    budget: int = Field(description="Budget in USD")
    comfort_level: str = Field(description="Comfort level: low/medium/high")
    food_Style: str = Field(description="Preferred food style: vegan/vegetarian/non-vegetarian")
    food_type: str = Field(description="Type of food: SriLanka/Indian/Chinese/Italian/Mexican/etc.")
    group_size: int = Field(description="Number of people")
