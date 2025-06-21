# /graph/schemas.py
from pydantic import BaseModel, Field
from typing import Literal, Annotated

class PhoneName(BaseModel):
    """This class is responsible for extracting the phone name from the user query."""
    phone_name: Annotated[
        str, 
        Field(description="Extract the phone name only from the user query and follow this rule: each word starts with a capital letter, numbers and suffixes are as in model name")
    ]

class SelectPath(BaseModel):
    """Schema for the supervisor's routing decision."""
    path: Annotated[
        Literal["RAG_CALL", "REVIEW_CALL", "LLM_CALL"], 
        Field(description="Based on the user query select one path only. if the user want to review any Phone the select the 'REVIEW_CALL' and if user want to know about phone specs, example display size, camera, or any kind of phone related query then select 'RAG_CAL' and if user ask normal query like hi, hello or any normal question which is not related to Phone then do 'LLM_CALL'.")
    ]
    reason: Annotated[str, Field(description="Why you select a specific path give reason in one sentence.")]