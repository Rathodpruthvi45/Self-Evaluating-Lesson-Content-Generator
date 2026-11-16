from langchain_core.prompts import ChatPromptTemplate

from app.llm.gemini_client import get_gemini_client
from app.schemas.evaluation import EvaluationResult


class LessonEvaluator:
    def __init__(self):
        self.llm = get_gemini_client()
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """ 
                You are a strict educational quality evaluator.

                Your job is to evaluate a generated lesson against
                the supplied rubric criteria.

                Rules:

                1. Evaluate every criterion independently.
                2. Return PASS only when the lesson clearly satisfies
                   the criterion.
                3. Return FAIL if the explanation is missing,
                   incorrect, misleading, or insufficient.
                4. Do not assume information that is not present
                   in the lesson.
                5. Provide a clear reason for every decision.
                6. Include evidence from the lesson wherever possible.
                7. Do not skip any rubric criterion.
                8. Do not create additional criteria.

                Be strict and objective.
                """,
                ),
                (
                    "human",
                    """ 
                    Evaluate the following lesson.

                TOPIC:
                {topic}

                LESSON:
                {lesson}

                UNIVERSAL RUBRIC:
                {universal_rubric}

                TOPIC-SPECIFIC RUBRIC:
                {topic_rubric}

                Evaluate all the supplied criteria.
                    """,
                ),
            ]
        )
        structured_llm = self.llm.with_structured_output(EvaluationResult)
        self.chain = self.prompt | structured_llm

    def evaluate(
        self, topic: str, lesson: str, universal_rubric: list, topic_rubric: list
    ):
        if not lesson:
            raise ValueError("Lesson cannot be empty.")

        if not universal_rubric and not topic_rubric:
            raise ValueError("At least one rubric criterion is required.")

        result = self.chain.invoke(
            {
                "topic": topic,
                "lesson": lesson,
                "universal_rubric": universal_rubric,
                "topic_rubric": topic_rubric,
            }
        )

        return result
