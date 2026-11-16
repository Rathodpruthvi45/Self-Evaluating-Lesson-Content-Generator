
from app.database.repository import MemoryRepository


def main():

    memory = MemoryRepository()

    history = memory.get_run_history()

    print("\nLESSON GENERATION HISTORY")
    print("=" * 60)

    if not history:
        print("No previous lessons found.")
        return

    for run in history:

        print("\nRun ID:", run["run_id"])
        print("Topic:", run["topic"])
        print("Status:", run["final_status"])
        print("Attempts:", run["total_attempts"])
        print("Created:", run["created_at"])

        attempts = memory.get_attempts(
            run["run_id"]
        )

        for attempt in attempts:

            print(
                f"  Attempt {attempt['attempt']}: "
                f"{attempt['status']}"
            )

        rejections = memory.get_rejections(
            run["run_id"]
        )

        for rejection in rejections:

            print(
                "  Failed criterion:",
                rejection["criterion"]
            )

            print(
                "  Reason:",
                rejection["reason"]
            )


if __name__ == "__main__":
    main()
