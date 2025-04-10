from synthex import Synthex


synthex = Synthex()

out = synthex.jobs.generate_data(
    schema_definition= {
        "question": {"type": "string"},
        "option-a": {"type": "string"},
        "option-b": {"type": "string"},
        "option-c": {"type": "string"},
        "option-d": {"type": "string"},
        "answer": {"type": "string"}
    },
    examples = [
        {
            "question": "A gas occupies 6.0 L at 300 K and 1 atm. What is its volume at 600 K and 0.5 atm, assuming ideal gas behavior?",
            "option-a": "12.0 L",
            "option-b": "24.0 L",
            "option-c": "6.0 L",
            "option-d": "3.0 L",
            "answer": "option-b"
        }
    ],
    requirements = [
        "Question Type: Multiple-choice questions (MCQs)",
        "Difficulty Level: High difficulty, comparable to SAT or AIEEE (JEE Main)",
        "Topic Coverage: Wide range of chemistry topics (physical, organic, inorganic)",
        "Number of Options: Each question must have four answer options",
        "Correct Answer: One of the four options must be correct and clearly marked",
        "Calculation-Based: Include mathematical/calculation-based questions",
        "Indirect Approach: Questions should be indirect and require knowledge application",
        "Conceptual Focus: Emphasize conceptual understanding, problem-solving, and analytical thinking"
    ],
    number_of_samples = 20,
    output_type = "csv",
    output_path = f"./test_data/output.pdf"
)

print(out)