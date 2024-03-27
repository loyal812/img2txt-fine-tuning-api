from pydantic import BaseModel
from typing import Optional

class ChattingModel(BaseModel):
    api_key: Optional[str] = ""
    user: Optional[str] = ""
    data_id: Optional[str] = ""
    question: Optional[str] = "hi"
