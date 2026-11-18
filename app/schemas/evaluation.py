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






class EvolutionProposal(BaseModel):

    pattern_summary: str = Field(
        description="Summary of repeated failures found in history"
    )

    target_criterion: str = Field(
        description="The criterion that needs improvement"
    )

    proposed_guidance: str = Field(
        description="Specific instructions to improve lesson generation"
    )

    expected_improvement: str = Field(
        description="How the proposed guidance should improve lesson quality"
    )

    risks: str = Field(
        description="Possible negative effects of this prompt change"
    )
