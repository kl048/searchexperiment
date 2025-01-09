from os import environ

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1.00,
    'participation_fee': 0.00,
    'doc': "",
}

SESSION_CONFIGS = [
    dict(
        name='search_experiment_Individual',
        display_name="Search Experiment (Individual)",
        num_demo_participants=1,
        app_sequence=['comprehension_i',  'crt', 'survey'],
        treatment='I',
        players_per_group=1
    ),
    dict(
        name='search_experiment_chat',
        display_name="Search Experiment (Chat)",
        num_demo_participants=2,
        app_sequence=['chat', 'crt', 'survey'],
        treatment='C',
        players_per_group=2
    ),
    dict(
        name='search_experiment_team',
        display_name="Search Experiment (Team)",
        num_demo_participants=2,
        app_sequence=['comprehension_t', 'team', 'crt', 'survey'],
        treatment='T',
        players_per_group=2
    ),
    dict(
        name='Demo_Individual',
        display_name="Demo_I",
        num_demo_participants=1,
        app_sequence=['Main_1','Payment'],
        treatment='I',
        real_world_currency_per_point = 0.5 # 1 ECUS = 0.5 dollars
    ),
    dict(
        name='Demo_Chat',
        display_name="Demo_C",
        num_demo_participants=2,
        app_sequence=['Main_2','Payment'],
        treatment='C',
        real_world_currency_per_point =0.5
    ),
    dict(
        name='Demo_Team',
        display_name="Demo_T",
        num_demo_participants=2,
        app_sequence=['Main_2','Payment'],
        treatment='T',
        real_world_currency_per_point =0.5
    ),
]

LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
POINTS_CUSTOM_NAME = 'ECUs'
REAL_WORLD_CURRENCY_DECIMAL_PLACES = 2
USE_POINTS_DECIMAL_PLACES = 0

ROOMS = []

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'your_secret_key'

INSTALLED_APPS = ['otree']

DEBUG = True
