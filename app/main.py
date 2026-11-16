from app.agents.lesson_generator import LessonGenerator

from app.evaluator.topic_rubric import TopicRubricGenerator

from app.evaluator.evaluator import LessonEvaluator

from app.evaluator.rubric import UNIVERSAL_RUBRIC, calculate_final_status


def main():

    topic = input("Enter topic: ").strip()

    if not topic:
        print("Topic cannot be empty.")
        return

    level = "Beginner"

    # STEP 1: Generate topic-specific rubric

    print("\nGenerating topic-specific rubric...")

    rubric_generator = TopicRubricGenerator()

    topic_rubric = rubric_generator.generate(topic=topic, level=level)

    # STEP 2: Combine both rubrics

    combined_rubric = UNIVERSAL_RUBRIC + [
        item.model_dump() for item in topic_rubric.criteria
    ]

    print("\nLearning checkpoints:")

    for item in combined_rubric:
        print(item["id"], "-", item["criterion"])

    # STEP 3: Generate lesson

    print("\nGenerating lesson...")

    generator = LessonGenerator()

    lesson = generator.generate(topic=topic, level=level, rubric=combined_rubric)

    print("\nGENERATED LESSON")
    print("=" * 60)
    print(lesson)

    # STEP 4: Evaluate lesson

    print("\nEvaluating lesson...")

    evaluator = LessonEvaluator()

    evaluation = evaluator.evaluate(
        topic=topic,
        lesson=lesson,
        universal_rubric=UNIVERSAL_RUBRIC,
        topic_rubric=[item.model_dump() for item in topic_rubric.criteria],
    )

    # STEP 5: Calculate final status

    final_status = calculate_final_status(evaluation.results)

    print("\nEVALUATION RESULTS")
    print("=" * 60)

    for item in evaluation.results:

        print("\nCriterion:", item.criterion)
        print("Status:", item.status)
        print("Reason:", item.reason)
        print("Evidence:", item.evidence)

    print("\nFINAL STATUS:", final_status)


if __name__ == "__main__":
    main()
