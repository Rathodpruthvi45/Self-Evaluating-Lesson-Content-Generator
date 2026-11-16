from langchain_core.prompts import ChatPromptTemplate

from app.llm.gemini_client import get_gemini_client
from app.schemas.rubric import TopicRubric


class TopicRubricGenerator:
    def __init__(self):
        self.llm = get_gemini_client()

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                You are an expert curriculum designer.

                Your task is to create topic-specific learning
                checkpoints for a beginner-friendly lesson.

                Rules:

                1. Generate between 5 and 7 checkpoints.
                2. Focus on concepts specific to the given topic.
                3. Start with fundamental concepts.
                4. Progress from basic to more advanced concepts.
                5. Avoid duplicate checkpoints.
                6. Each checkpoint must be objectively assessable.
                7. Do not include generic quality criteria such
                   as grammar or beginner friendliness.
                8. Use IDs T1, T2, T3, and so on.
                9. Do not include unrelated advanced concepts.
                """,
                ),
                (
                    "human",
                    """
                    Topic: {topic}

                    Learner Level: {level}

                    Generate 5 to 7 essential topic-specific
                    learning checkpoints for this topic.
                """,
                ),
            ]
        )
        self.structured_llm = self.llm.with_structured_output(TopicRubric)
        self.chain = self.prompt | self.structured_llm

    def generate(self, topic: str, level: str = "Beginner") -> TopicRubric:

        if not topic.strip():
            raise ValueError("Topic cannot be empty.")

        result = self.chain.invoke({"topic": topic, "level": level})

        return result
