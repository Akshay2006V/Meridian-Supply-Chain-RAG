import sys
from rag import ask


TESTS = [
    {
        "name": "Highest-spend supplier",
        "question": "Which supplier had the highest spend in Q1, and what was its on-time delivery percentage?",
        "expected": [
            "Shenzhen Rui Electronics",
            "21.9",
            "79.5",
        ],
    },
    {
        "name": "Line stoppages",
        "question": "How many line stoppages happened in Q1, what was the total downtime, and what caused them?",
        "expected": [
            "seven",
            "41 hours",
            "Shenzhen Rui Electronics",
            "Trident Circuit Boards",
        ],
    },
    {
        "name": "PO approval",
        "question": "What is the approval authority for a purchase order worth ₹1.4 crore?",
        "expected": [
            "Chief Operating Officer",
        ],
    },
    {
        "name": "Critical supplier classification",
        "question": "What are the four supplier classification categories, and what qualifies a supplier as Critical?",
        "expected": [
            "Critical",
            "Strategic",
            "Standard",
            "Tail",
            "single-source",
            "₹10 crore",
            "safety-related",
        ],
    },
    {
        "name": "Safety stock",
        "question": "Microcontrollers are imported with a 46-day lead time. Using the safety-stock policy, how many days of stock should be held for this part?",
        "expected": [
            "30 days",
        ],
    },
    {
        "name": "Unsupported question",
        "question": "What is the annual salary of the Head of Procurement?",
        "expected": [
            "I cannot answer that from the supplied documents.",
        ],
    },
]


def main():
    print("=" * 70)
    print("MERIDIAN RAG AUTOMATED TESTS")
    print("=" * 70)

    passed = 0
    failed = 0

    for index, test in enumerate(TESTS, start=1):

        print()
        print(f"[TEST {index}/{len(TESTS)}] {test['name']}")
        print("-" * 70)
        print(test["question"])

        try:
            answer, retrieved, timing = ask(test["question"])

            answer_lower = answer.lower()

            missing = [
                expected
                for expected in test["expected"]
                if expected.lower() not in answer_lower
            ]

            if not missing:
                print("PASS")
                print(
                    f"Time: {timing['total_seconds']:.2f}s "
                    f"(retrieval {timing['retrieval_seconds']:.2f}s, "
                    f"generation {timing['generation_seconds']:.2f}s)"
                )
                passed += 1

            else:
                print("FAIL")
                print("Missing expected content:")
                for item in missing:
                    print(f"  - {item}")

                print("\nActual answer:")
                print(answer)

                failed += 1

        except Exception as exc:
            print("ERROR")
            print(exc)
            failed += 1

    print()
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total : {len(TESTS)}")

    if failed:
        print()
        print("RESULT: TESTS FAILED")
        sys.exit(1)

    print()
    print("RESULT: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
