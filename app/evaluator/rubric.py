UNIVERSAL_RUBRIC = [
    {
        "id": "U1",
        "criterion": "Accuracy",
        "description": (
            "All explanations must be factually correct "
            "and must not contain misleading information."
        ),
    },
    {
        "id": "U2",
        "criterion": "Beginner Friendly",
        "description": (
            "The lesson must be understandable to someone "
            "with zero background knowledge."
        ),
    },
    {
        "id": "U3",
        "criterion": "Practical Example",
        "description": (
            "The lesson must include at least one relevant "
            "and understandable practical example."
        ),
    },
    {
        "id": "U4",
        "criterion": "Technical Terminology",
        "description": (
            "Technical terms must be explained before " "or when they are introduced."
        ),
    },
    {
        "id": "U5",
        "criterion": "Teaching Flow",
        "description": (
            "The lesson must progress logically from "
            "basic concepts to more advanced concepts."
        ),
    },
    {
        "id": "U6",
        "criterion": "Completeness",
        "description": (
            "The lesson must cover the essential concepts "
            "required to understand the requested topic."
        ),
    },
    {
        "id": "U7",
        "criterion": "Summary and Exercises",
        "description": (
            "The lesson must include a useful summary "
            "and beginner-level practice questions."
        ),
    },
]


def calculate_final_status(results):

    if not results:
        return "FAIL"

    for item in results:
        if item.status != "PASS":
            return "FAIL"

    return "PASS"
