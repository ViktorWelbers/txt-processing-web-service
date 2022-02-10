from pydantic import BaseModel
from typing import Optional, List

class OneLiner(BaseModel):
    """ """
    random_line: Optional[str] = None

class AdditionalOneLiner(OneLiner):
    line_number: Optional[str] = None
    file_name: Optional[str] = None
    most_common: Optional[str] = None

class LongestHundredLines(BaseModel):
    """100 longest lines of all files uploaded"""
    lines: Optional[List[str]] = None

class TwentyLongestLines(BaseModel):
    """20 longest lines of one file uploaded """
    lines: Optional[List[str]] = None