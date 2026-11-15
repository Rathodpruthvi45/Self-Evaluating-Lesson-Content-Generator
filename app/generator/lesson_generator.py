from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.llm.gemini_client import get_gemini_client

class LessonGenerator:
    def __init__(self):
        self.llm=get_gemini_client()
        self.prompt=ChatPromptTemplate([
            (
                "system",
                """ 
                You are an expert technical teacher.
                your responsibility is to teach students
                who have absolutely no background knowlwdge.

                use simple English.
                Explain technical terminology.
                Teach concepts step by step.
                Use practical examples.
                Never assume prior knowledge.
                """
            )
            ,
            (
                "human",
                """ 
                Create a complete beginner-frindly lesson.
                Topic:{topic}
                 Learner Level: {level}

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

                Explain everything in simple language.

                
                """
            )
        ])
        self.parser=StrOutputParser()
        self.chain=self.prompt | self.llm | self.parser
    def generate(self, topic: str, level: str = "Beginner"):

        if not topic.strip():
            raise ValueError("Topic cannot be empty.")

        lesson = self.chain.invoke({
            "topic": topic,
            "level": level
        })

        return lesson