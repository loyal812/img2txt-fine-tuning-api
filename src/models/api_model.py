from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class APIModel(BaseModel):
    user: Optional[str] = ""
    api: Optional[str] = ""
    title: Optional[str] = ""
    description: Optional[str] = ""
    is_removed: Optional[bool] = False
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
