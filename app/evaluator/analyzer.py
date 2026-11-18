from langchain_core.prompts import ChatPromptTemplate

from app.llm.gemini_client import get_gemini_client

from app.schemas.evaluation import EvolutionProposal


class EvoluationsAnalyzer:
    def __init__(self):
        self.llm=get_gemini_client()
        self.prompt=ChatPromptTemplate.from_messages([
            (
            "system",
            """ 
            You are an AI prompt optimization expert.
            Analyze historical lesson evaluation failures.
            Your responsibility is to propose improvements
            to the lesson genration instructions.

            Rules:
            1.Identify recurring failure patterns.
            2.Suggest specific and actionable instructions.
            3. Focus on improving and actionable instructions.
            4. do not remove any evaluation critera.
            5. do not instruct the genrator to manipulate the evaluator.
            6. Avoid unnecessary changes to successful genration instructions.
            8.Explain possible risks of the improvement.
            9.Use only the supplied failure information.

            Return one focused improvement proposal. 
            """
            ),
            (
                "human",
                """ 
                Historical failure patterns:
                {failure_patterns}

                Analyze these failures and propose an
                improvement to the lesson generation prompt.
                """
            )
        ])
        structured_llm=self.llm.with_structured_output(
            EvolutionProposal
        )
        self.chain=self.prompt|structured_llm

    def analyze(self,failure_patterns):
        if not failure_patterns:
            raise ValueError("No failure patterns provided. ")

        return self.chain.invoke({
            "failure_patterns":failure_patterns
        })


