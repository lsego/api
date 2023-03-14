from pydantic import BaseModel, Field
from typing import Optional

class Movie(BaseModel):
	# indicamos que el id puede ser optional.
	id: Optional[int] = None
	title: str = Field(min_length=5, max_length=15)
	overview: str = Field(min_length=15, max_length=50)
	year: int = Field(le=2022)
	rating: float = Field(ge=1, le=10)
	category: str = Field(min_length=5, max_length=15)
    
