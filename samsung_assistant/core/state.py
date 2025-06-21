# /core/state.py
from typing import TypedDict, Sequence, Annotated
from langchain_core.messages import BaseMessage
from pydantic import Field
import operator

class AgentState(TypedDict):
    """
    This is the graph state where all conversations and intermediate results are stored.
    """
    messages: Annotated[Sequence[BaseMessage], operator.add]
    path: Annotated[str, Field(description="The next node to execute based on user query.")]
    ph_raw_data: Annotated[str, Field(description="Raw data extracted from the MySQL DB for reviews.")]