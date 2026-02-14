from pydantic import BaseModel, Field
from typing import Optional

# single credit record
class CreditRecord(BaseModel):
    person_age: int = Field(..., example=22)
    person_income: float = Field(..., example=59000)
    person_home_ownership: str = Field(..., example="RENT")
    person_emp_length: float = Field(..., example=3.0)

    loan_intent: str = Field(..., example="PERSONAL")
    loan_grade: str = Field(..., example="D")
    loan_amnt: float = Field(..., example=35000)
    loan_int_rate: float = Field(..., example=16.02)

    loan_percent_income: float = Field(..., example=0.59)
    cb_person_default_on_file: str = Field(..., example="Y")
    cb_person_cred_hist_length: int = Field(..., example=3)

    loan_status: Optional[int] = Field(None, example=1)