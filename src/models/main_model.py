from pydantic import BaseModel
from typing import Optional

class MainModel(BaseModel):
    api_key: Optional[str] = ""
    user: Optional[str] = ""
    data_id: Optional[str] = ""
