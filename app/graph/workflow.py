from langgraph.graph import StateGraph, START, END

from app.graph.state import LessonState

from app.agents.lesson_generator import LessonGenerator
from app.agents.regenerator import RegenerationAgent

from app.evaluator.evaluator import LessonEvaluator
from app.evaluator.rubric import calculate_final_status

from app.schemas.evaluation import CriterionResult
from app.schemas.rejection import RejectionLog

from app.database.repository import MemoryRepository





class LessonWorkflow:
    def __init__(self):
        self.generator=LessonGenerator()
        self.evaluator=LessonEvaluator()
        self.memory = MemoryRepository()



    # NODE 1: Generate initial lesso
    def generate_lesson(self, state: LessonState):

        print("\nGenerating lesson...")

        lesson = self.generator.generate(
            topic=state["topic"],
            level=state["level"],
            rubric=state["rubric"]
        )

        return {
            "lesson": lesson,
            "attempt": 1
        }


    # NODE 2: Evaluate lesso

    def evaluate_lesson(self, state: LessonState):

        print(
            f"\nEvaluating lesson - Attempt {state['attempt']}"
        )

        evaluation = self.evaluator.evaluate(
            topic=state["topic"],
            lesson=state["lesson"],
            universal_rubric=state["universal_rubric"],
            topic_rubric=state["topic_rubric"]
        )

        results = evaluation.results
        expected_ids = {
            item["id"] for item in state["rubric"]
        }

        actual_ids = {
            item.criterion_id for item in results
        }
        print("actual_ids",actual_ids)
        print("expected_ids",expected_ids)
        
        if (
            actual_ids != expected_ids
            or len(results) != len(expected_ids)
        ):
            raise ValueError(
                "Evaluator returned missing or duplicate criteria."
            )

        final_status = calculate_final_status(results)
        self.memory.save_attempt(
            run_id=state["run_id"],
            attempt=state["attempt"],
            lesson=state["lesson"],
            evaluation_results=[
                item.model_dump() for item in results
            ],
            status=final_status
        )

        for item in results:
            print(
                item.criterion,
                "->",
                item.status
            )

        print("\nEvaluation status:", final_status)

        return {
            "evaluation_results": [
                item.model_dump() for item in results
            ],
            "final_status": final_status
        }


    # NODE 3: Regenerate failed lesson

    def regenerate_lesson(self, state: LessonState):

        print(
            f"\nRegenerating lesson after attempt "
            f"{state['attempt']}..."
        )

        results = [
            CriterionResult.model_validate(item)
            for item in state["evaluation_results"]
        ]

        rejection_log = RejectionLog.model_validate(
            state["rejection_log"]
        )

        revised_lesson = self.regenerator.regenerate(
            topic=state["topic"],
            level=state["level"],
            rubric=state["rubric"],
            previous_lesson=state["lesson"],
            evaluation_results=results,
            attempt=state["attempt"],
            rejection_log=rejection_log
        )

        return {
            "lesson": revised_lesson,
            "attempt": state["attempt"] + 1,
            "rejection_log": rejection_log.model_dump()
        }


    def decide_next_step(self, state: LessonState):

        if state["final_status"] == "PASS":
            print("\nLesson passed. Workflow completed.")
            return END

        if state["attempt"] > state["max_retries"]:
            print("\nMaximum retry limit reached.")
            return END

        return "regenerate_lesson"


    # BUILD GRAPH

    def build(self):

        graph = StateGraph(LessonState)

        # Register nodes
        graph.add_node(
            "generate_lesson",
            self.generate_lesson
        )

        graph.add_node(
            "evaluate_lesson",
            self.evaluate_lesson
        )

        graph.add_node(
            "regenerate_lesson",
            self.regenerate_lesson
        )

        # Register edges
        graph.add_edge(
            START,
            "generate_lesson"
        )

        graph.add_edge(
            "generate_lesson",
            "evaluate_lesson"
        )

        graph.add_conditional_edges(
            "evaluate_lesson",
            self.decide_next_step
        )

        graph.add_edge(
            "regenerate_lesson",
            "evaluate_lesson"
        )

        return graph.compile()
