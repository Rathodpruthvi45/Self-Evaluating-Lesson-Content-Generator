
from app.agents.lesson_generator import LessonGenerator
from app.schemas.rejection import RejectionEntry, RejectionLog


class RegenerationAgent:

    def __init__(self):

        self.generator = LessonGenerator()


    def regenerate(
        self,
        topic: str,
        level: str,
        rubric: list,
        previous_lesson: str,
        evaluation_results: list,
        attempt: int,
        rejection_log: RejectionLog
    ):

        # Find failed criteria
        failed_results = [
            item
            for item in evaluation_results
            if item.status == "FAIL"
        ]

        if not failed_results:
            raise ValueError("No failed criteria found.")

        # Build specific feedback
        feedback_parts = []

        for item in failed_results:

            feedback_parts.append(
                f"""
                Criterion: {item.criterion}
                Criterion ID: {item.criterion_id}
                Reason for failure: {item.reason}
                Evidence: {item.evidence}

                Required improvement:
                Correct this issue clearly in the revised lesson.
                """
            )

            # Save rejection information
            rejection_log.entries.append(
                RejectionEntry(
                    attempt=attempt,
                    criterion_id=item.criterion_id,
                    criterion=item.criterion,
                    reason=item.reason,
                    evidence=item.evidence
                )
            )

        feedback = "\n".join(feedback_parts)

        print("\nRegeneration feedback:")
        print(feedback)

        # Generate improved lesson
        revised_lesson = self.generator.generate(
            topic=topic,
            level=level,
            rubric=rubric,
            feedback=feedback,
            previous_lesson=previous_lesson
        )

        return revised_lesson
