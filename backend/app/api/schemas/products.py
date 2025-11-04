from pydantic import BaseModel, ConfigDict

class CategoryIn(BaseModel):
    category_name: str

class CategoryOut(CategoryIn):
    category_id: str

    model_config = ConfigDict(from_attributes=True)