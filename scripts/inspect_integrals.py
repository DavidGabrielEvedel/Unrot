import json
from pathlib import Path
from collections import Counter

SOURCE_DIR = Path("data_sources/integration-test-suites/data")
OUTPUT_FILE = Path("content/integrals/integrals.jsonl")

ALLOWED_SUITES = {"rubi", "independent"}


def main():

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    total = 0
    compiled = 0
    missing = 0

    suite_counts = Counter()

    with OUTPUT_FILE.open("w", encoding="utf-8") as output:

        for file_path in SOURCE_DIR.rglob("*.jsonl"):

            with file_path.open("r", encoding="utf-8") as source:

                for line in source:

                    try:
                        record = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    if not isinstance(record, dict):
                        continue

                    if "integrand" not in record:
                        continue

                    total += 1

                    suite = record.get("suite", "unknown")
                    suite_counts[suite] += 1

                    if suite not in ALLOWED_SUITES:
                        continue

                    integrand = record.get("integrand")
                    answer = record.get("integral")

                    if not integrand or not answer:
                        missing += 1
                        continue

                    compiled += 1

                    question = {
                        "id": f"unrot_int_{compiled:06d}",
                        "integrand": integrand,
                        "variable": record.get("variable", "x"),
                        "answer": answer,
                        "source_suite": suite,
                        "source": record.get("source", ""),
                        "source_index": record.get("index")
                    }

                    output.write(
                        json.dumps(question) + "\n"
                    )

    print("\nUNROT INTEGRAL COLLECTION")
    print("=" * 40)

    print(f"Total source questions: {total}")

    print("\nSource breakdown:")

    for suite, count in suite_counts.items():
        print(f"{suite}: {count}")

    print("\nCompilation:")
    print(f"Compiled: {compiled}")
    print(f"Missing answers skipped: {missing}")

    print(f"\nSaved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()