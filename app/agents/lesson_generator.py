
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.llm.gemini_client import get_gemini_client


class LessonGenerator:

    def __init__(self):

        self.llm = get_gemini_client()

        self.prompt = ChatPromptTemplate.from_messages([

            (
                "system",
                """
                You are an expert technical teacher.

                Teach students who have absolutely no background
                knowledge.

                Rules:

                1. Use simple English.
                2. Explain technical terminology.
                3. Teach concepts step by step.
                4. Include practical examples.
                5. Never assume prior knowledge.
                6. Cover every required learning checkpoint.
                7. Ensure factual accuracy.
                8. Follow the evaluator's feedback when provided.
                9. Correct failed explanations instead of merely
                   adding unrelated content.
                10. Preserve correct explanations from the previous
                    lesson wherever appropriate.
                """
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

                PREVIOUS LESSON:
                {previous_lesson}

                EVALUATOR FEEDBACK:
                {feedback}

                Follow this structure:

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

                Important:
                - Cover every required checkpoint.
                - Fix all issues identified by the evaluator.
                - Explain concepts clearly.
                - Return the complete revised lesson.
                """
            )

        ])

        self.parser = StrOutputParser()

        self.chain = self.prompt | self.llm | self.parser


    def generate(
        self,
        topic: str,
        level: str = "Beginner",
        rubric: list | None = None,
        feedback: str = "",
        previous_lesson: str = ""
    ) -> str:

        if not topic.strip():
            raise ValueError("Topic cannot be empty.")

        if not rubric:
            raise ValueError("Learning rubric cannot be empty.")

        return self.chain.invoke({

            "topic": topic,
            "level": level,
            "rubric": rubric,
            "feedback": feedback,
            "previous_lesson": previous_lesson

        })
