from app.generator.lesson_generator import LessonGenerator


def main():

    generator = LessonGenerator()

    topic = input("Enter topic: ").strip()

    level = input(
        "Enter learner level: "
    ).strip() or "Beginner"

    try:

        print("\nGenerating lesson...\n")

        lesson = generator.generate(
            topic=topic,
            level=level
        )

        print("\n" + "=" * 60)
        print("GENERATED LESSON")
        print("=" * 60)

        print(lesson)

    except Exception as error:
        print(f"Generation failed: {error}")


if __name__ == "__main__":
    main()
