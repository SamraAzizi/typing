# Application settings
APP_SETTINGS = {
    'SAVE_DIR': 'data',
    'DEFAULT_THEME': 'Light',
    'ENABLE_SOUND': True,
    'MIN_ACCURACY': 95,
    'LESSONS_PER_LEVEL': 4,
}

# Database configuration
DB_CONFIG = {
    'type': 'json',
    'path': 'data/user_data.json'
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