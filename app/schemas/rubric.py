from pydantic import BaseModel, Field


class RubricCriterion(BaseModel):
    id: str = Field(description="Unique criterion ID, such as T1, T2, T3")
    criterion: str = Field(description="Name of the learning checkpoint")
    description: str = Field(
        description="What the lesson must explain to satisfy this checkpoint"
    )


class TopicRubric(BaseModel):

    criteria: list[RubricCriterion] = Field(
        min_length=5,
        max_length=7,
        description="Five to seven essential topic-specific checkpoints",
    )
