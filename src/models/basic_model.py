from pydantic import BaseModel
from typing import Optional

class BasicModel(BaseModel):
    api_key: Optional[str] = ""
    user: Optional[str] = ""
    data_id: Optional[str] = ""
