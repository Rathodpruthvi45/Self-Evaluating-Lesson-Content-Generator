
from app.evaluator.analyzer import EvoluationsAnalyzer


class SelfEvolutionEngine:

    def __init__(self, memory):

        self.memory = memory

        self.analyzer = EvoluationsAnalyzer()


    def run(self):

        print("\nAnalyzing historical failures...")

        # 1. Find repeated failures

        patterns = self.memory.get_failure_patterns(
            min_runs=2
        )

        if not patterns:

            print(
                "No repeated failure patterns found yet."
            )

            return None

        print("\nRepeated failure patterns found:")

        for pattern in patterns:

            print(
                pattern["criterion"],
                "-",
                pattern["run_count"],
                "different runs"
            )

        # 2. Generate improvement proposal

        print("\nGenerating prompt improvement proposal...")

        proposal = self.analyzer.analyze(patterns)

        print("\nPROPOSED IMPROVEMENT")

        print(proposal.model_dump_json(indent=2))

        # 3. Save proposal as pending

        version = self.memory.save_prompt_candidate(
            guidance=proposal.proposed_guidance,
            source_patterns=patterns
        )

        print("\nPrompt candidate created.")

        print("Version:", version)

        print("Status: PENDING")

        return {
            "version": version,
            "proposal": proposal
        }
