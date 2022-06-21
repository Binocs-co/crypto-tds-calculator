from pydantic import BaseModel, Field
from datetime import datetime

class BinocsModel(BaseModel):
    create_date: datetime = Field(None)
    updated_date: datetime = Field(None)

class BinocsId(BinocsModel):
    id: str = Field(None)