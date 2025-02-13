from os import environ

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1.00,
    'participation_fee': 5.00,
    'doc': "",
}

SESSION_CONFIGS = [
    dict(
        name='Individual',
        display_name="Individual",
        num_demo_participants=1,
        app_sequence=['comprehension_i', 'Main_Ind', 'Payment', 'crt', 'survey', 'Measures'],
        treatment='I',
        real_world_currency_per_point = 0.25 # 1 ECUS = 0.25 dollars
    ),
    dict(
        name='Chat',
        display_name="Chat",
        num_demo_participants=2,
        app_sequence=['comprehension_c', 'Main', 'Payment', 'crt', 'survey', 'Measures'],
        treatment='C',
        real_world_currency_per_point =0.25
    ),
    dict(
        name='Team',
        display_name="Team",
        num_demo_participants=2,
        app_sequence=['comprehension_t', 'Main', 'Payment', 'crt', 'survey', 'Measures'],
        treatment='T',
        real_world_currency_per_point =0.25
    ),
]

ROOMS = [
    dict(
        name='Searching',
        display_name='Searching',
        participant_label_file='_rooms/workstation.txt',
        use_secure_urls=False
    ),
]


LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
POINTS_CUSTOM_NAME = 'ECUs'
REAL_WORLD_CURRENCY_DECIMAL_PLACES = 2
USE_POINTS_DECIMAL_PLACES = 0
CSRF_ENABLED = True

ROOMS = []

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = '123'

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'your_secret_key'

INSTALLED_APPS = ['otree']

DEBUG = True