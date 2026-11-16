
from typing import TypedDict


class LessonState(TypedDict):

    run_id: str

    topic: str
    level: str

    rubric: list
    universal_rubric: list
    topic_rubric: list

    lesson: str

    evaluation_results: list
    final_status: str

    attempt: int
    max_retries: int

    rejection_log: dict
