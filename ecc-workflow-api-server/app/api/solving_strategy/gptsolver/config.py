import os

# Get absolute path to the current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_config: dict = {
    "MODEL_CHOICES": {
        1: "gpt-3.5-turbo",
        2: "gpt-4o", 
        3: "o1-mini"
    },
    "N_OF_SERVICES": 5,
    "TEMPERATURE": 0.0,
    "DEVELOPER_TEXT": "I want you to be my AWS Architecture expert. I have a workflow that I want to deploy on AWS.",
    "PERFORMANCE_PATH": os.path.join(BASE_DIR, 'data', 'performance.json'),
    "USE_TAGS": True
}