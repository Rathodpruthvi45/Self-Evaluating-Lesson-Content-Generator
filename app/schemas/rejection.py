from pydantic import BaseModel,Field



class RejectionEntry(BaseModel):
    attempt: int = Field(
        description="The attempt number on which the lesson failed"
    )

    criterion_id: str

    criterion: str

    reason: str

    evidence: str


class RejectionLog(BaseModel):

    topic: str

    entries: list[RejectionEntry] = Field(default_factory=list)

