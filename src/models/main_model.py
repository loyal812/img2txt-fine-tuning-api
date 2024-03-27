from pydantic import BaseModel
from typing import Optional

class MainModel(BaseModel):
    user: Optional[str] = ""
    title: Optional[str] = ""
    description: Optional[str] = ""
    data_id: Optional[str] = ""
    question: Optional[str] = "hi"
