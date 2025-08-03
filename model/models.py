from pydantic import BaseModel, Field, RootModel
from typing import Optional, List, Dict, Any, Union


class Metadata(BaseModel):
    Summary: List[str] = Field(default_factory=list, description="Summary of the document")
    Title: str
    Author: str
    DateCreated: str   
    LastModifiedDate: str
    Publisher: str
    Language: str
    PageCount: Union[int, str]  # Can be "Not Available"
    SentimentTone: str

class ChangeFormat(BaseModel):
    """
    ChangeFormat is a Pydantic model that represents the format of the change. 
    """
    Page: str
    changes: str

class SummaryResponse(RootModel[list[ChangeFormat]]):
    """
    SummaryResponse is a Pydantic model that represents a list of changes.
    It inherits from RootModel to allow for a list of ChangeFormat objects.
    """
    pass
    


    