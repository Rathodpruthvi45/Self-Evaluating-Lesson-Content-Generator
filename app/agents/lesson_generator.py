from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.llm.gemini_client import get_gemini_client


class LessonGenerator:

    def __init__(self):

        self.llm = get_gemini_client()

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                You are an expert technical teacher.

                Your responsibility is to teach students
                who have absolutely no background knowledge.

                Teaching rules:

                1. Use simple English.
                2. Explain technical terminology.
                3. Teach concepts step by step.
                4. Use practical examples.
                5. Never assume prior knowledge.
                6. Avoid unnecessary complexity.
                7. Cover every supplied learning checkpoint.
                8. Do not simply list concepts. Explain them.
                9. Ensure the lesson is factually accurate.
                """,
                ),
                (
                    "human",
                    """
                Create a complete beginner-friendly lesson.

                TOPIC:
                {topic}

                LEARNER LEVEL:
                {level}

                REQUIRED LEARNING CHECKPOINTS:
                {rubric}

                Follow this lesson structure:

                1. Introduction
                2. What is the topic?
                3. Why do we need it?
                4. How does it work?
                5. Step-by-step explanation
                6. Real-world example
                7. Advantages
                8. Limitations
                9. Summary
                10. Practice questions

                IMPORTANT:

                - Cover every required learning checkpoint.
                - Explain each checkpoint clearly.
                - Use examples wherever useful.
                - Keep the lesson appropriate for the learner level.
                """,
                ),
            ]
        )

        self.parser = StrOutputParser()

        self.chain = self.prompt | self.llm | self.parser

    def generate(
        self, topic: str, level: str = "Beginner", rubric: list | None = None
    ) -> str:

        if not topic.strip():
            raise ValueError("Topic cannot be empty.")

        if not rubric:
            raise ValueError("Learning rubric cannot be empty.")

        lesson = self.chain.invoke({"topic": topic, "level": level, "rubric": rubric})

        return lesson
