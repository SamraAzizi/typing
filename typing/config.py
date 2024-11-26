import os

# Get the base directory
BASE_DIR = os.path.dirname(__file__)

# Application settings
APP_SETTINGS = {
    'SAVE_DIR': os.path.join(BASE_DIR, 'data'),
    'DEFAULT_THEME': 'Light',
    'ENABLE_SOUND': True,
    'MIN_ACCURACY': 95,
    'LESSONS_PER_LEVEL': 4,
    'SCORING': {
        'MISTAKE_PENALTY': 5,
        'PERFECT_BONUS': 20,
        'SPEED_MULTIPLIER': 1.5
    },
    'PERFORMANCE_LEVELS': {
        'MASTER': 90,
        'EXPERT': 70,
        'INTERMEDIATE': 50,
        'BEGINNER': 0
    }
}

# Database configuration
DB_CONFIG = {
    'type': 'json',
    'path': os.path.join(BASE_DIR, 'data', 'user_data.json')
}

# Theme settings
THEMES = {
    'Light': {
        'background': '#ffffff',
        'text': '#000000',
        'accent': '#1f77b4'
    },
    'Dark': {
        'background': '#0e1117',
        'text': '#ffffff',
        'accent': '#00ff00'
    }
} 