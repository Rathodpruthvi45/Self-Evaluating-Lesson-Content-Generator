
from app.graph.workflow import LessonWorkflow
import uuid

from app.database.repository import MemoryRepository
from app.evaluator.topic_rubric import TopicRubricGenerator
from app.evaluator.rubric import UNIVERSAL_RUBRIC

from app.schemas.rejection import RejectionLog


def main():

    run_id = str(uuid.uuid4())

    # Initialize persistent memory

   

    topic = input("Enter topic: ").strip()

    if not topic:
        print("Topic cannot be empty.")
        return

    level = "Beginner"

    # STEP 1: Generate topic rubric

    print("\nGenerating topic-specific rubric...")

    rubric_generator = TopicRubricGenerator()

    topic_rubric_result = rubric_generator.generate(
        topic=topic,
        level=level
    )

    topic_rubric = [
        item.model_dump()
        for item in topic_rubric_result.criteria
    ]

    # STEP 2: Combine rubrics

    combined_rubric = UNIVERSAL_RUBRIC + topic_rubric

    memory = MemoryRepository()
    
        # Save initial request
    
    memory.create_run(
        run_id=run_id,
        topic=topic,
        level=level,
        rubric=combined_rubric
    )

    # STEP 3: Create initial state

    initial_state = {

        "topic": topic,
        "level": level,
        "run_id": run_id,
        "rubric": combined_rubric,

        "universal_rubric": UNIVERSAL_RUBRIC,

        "topic_rubric": topic_rubric,

        "lesson": "",

        "evaluation_results": [],

        "final_status": "",

        "attempt": 0,

        "max_retries": 2,

        "rejection_log": RejectionLog(
            topic=topic
        ).model_dump()

    }

    # STEP 4: Build workflow

    workflow_builder = LessonWorkflow()

    workflow = workflow_builder.build()

    # STEP 5: Execute workflow

    print("\nStarting LangGraph workflow...")

    result = workflow.invoke(initial_state)


    memory.finish_run(
    run_id=run_id,
    final_status=result["final_status"],
    total_attempts=result["attempt"],
    final_lesson=result["lesson"],
    rejection_log=result["rejection_log"]
)

    print("\nMemory successfully saved to SQLite.")

    # STEP 6: Display final result

    print("\n" + "=" * 60)
    print("FINAL LESSON")
    print("=" * 60)

    print(result["lesson"])

    print("\nFINAL STATUS:", result["final_status"])

    print("\nTOTAL ATTEMPTS:", result["attempt"])

    # STEP 7: Display rejection history

    print("\nREJECTION LOG")
    print("=" * 60)

    for entry in result["rejection_log"]["entries"]:

        print("\nAttempt:", entry["attempt"])
        print("Criterion:", entry["criterion"])
        print("Reason:", entry["reason"])


if __name__ == "__main__":
    main()
