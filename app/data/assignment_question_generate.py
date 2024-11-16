RESPONSE_STRUCTURE = """
```json
{
    "questions": [
        {
            "type": "<question_type>",
            "mcq": true/false,
            "difficulty": "easy"/"medium"/"hard",
            "question": "Question text here?",
            "options": ["Option 1", "Option 2", "Option 3", "Option 4"] or [],
            "correct_answers": ["Correct answer(s)"],
            "explanation": "Explanation text here"
        }
    ]
}
```
"""

EXAMPLE_CONFIGURATION = """
{
    "question_bank_mcq": 2,
    "question_bank_broad": 1,
    "adaptive_learning_mcq": 0,
    "adaptive_learning_broad": 0,
    "application_based_mcq": 0,
    "application_based_broad": 0,
    "writing_assignment_mcq": 0,
    "writing_assignment_broad": 0,
    "scenario_based_mcq": 0,
    "scenario_based_broad": 0
}
"""


EXPECTED_OUTPUT = """
{
    "questions": [
        {
            "type": "question bank",
            "mcq": true,
            "difficulty": "easy",
            "question": "What are the four main types of tissues in the human body?",
            "options": [
                "Epithelial, Connective, Muscle, Nervous",
                "Epithelial, Bone, Blood, Nervous",
                "Muscle, Skin, Blood, Nervous",
                "Epithelial, Fat, Muscle, Blood"
            ],
            "correct_answers": ["Epithelial, Connective, Muscle, Nervous"],
            "explanation": "The human body has four main tissue types: epithelial, connective, muscle, and nervous tissues, each serving distinct functions."
        },
        {
            "type": "question bank",
            "mcq": true,
            "difficulty": "medium",
            "question": "Which tissue type forms the lining of blood vessels?",
            "options": [
                "Epithelial tissue",
                "Connective tissue",
                "Muscle tissue",
                "Nervous tissue"
            ],
            "correct_answers": ["Epithelial tissue"],
            "explanation": "Blood vessels are lined with epithelial tissue, specifically endothelium, which is a specialized type of epithelial tissue."
        },
        {
            "type": "question bank",
            "mcq": false,
            "difficulty": "hard",
            "question": "Describe the structural and functional characteristics of epithelial tissue.",
            "options": [],
            "correct_answers": ["Epithelial tissue is characterized by closely packed cells with little intercellular space, has a basement membrane, and serves functions including protection, secretion, and absorption."],
            "explanation": "This question tests deep understanding of epithelial tissue characteristics and functions."
        }
    ]
}
"""
