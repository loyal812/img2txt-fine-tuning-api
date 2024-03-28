from pydantic import BaseModel, Field
from typing import Optional

class MainModel(BaseModel):
    user: str = Field(default='')
    title: str = Field(default='')
    description: str = Field(default='')
    data_id: str = Field(default='')
    question: str = Field(default='')