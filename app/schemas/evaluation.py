from typing import Literal
from pydantic import BaseModel, Field


class CriterionResult(BaseModel):
    criterion_id: str = Field(description="ID of the rubric criterion being evaluated")
    criterion: str = Field(description="Name of the criterion")
    status: Literal["PASS", "FAIL"] = Field(
        description="Whether the lesson satisfies this criterion"
    )
    reason: str = Field(description="Explanation supporting the PASS or FAIL decision")
    evidence: str = Field(description="Relevant text or explanation from the lesson")


class EvaluationResult(BaseModel):
    results: list[CriterionResult] = Field(
        description="Evaluation result for every rubric criterion"
    )
