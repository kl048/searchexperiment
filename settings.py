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
        name='Chat_1',
        display_name='Chat_1',
        participant_label_file='_rooms/workstation.txt',
    ),
    dict(
        name='Chat_2',
        display_name='Chat_2',
        participant_label_file='_rooms/workstation.txt',
    ),
    dict(
        name='Chat_3',
        display_name='Chat_3',
        participant_label_file='_rooms/workstation.txt',
    ),
    dict(
        name='Chat_4',
        display_name='Chat_4',
        participant_label_file='_rooms/workstation.txt',
    ),
    dict(
        name='Chat_5',
        display_name='Chat_5',
        participant_label_file='_rooms/workstation.txt',
    ),
    dict(
        name='Chat_6',
        display_name='Chat_6',
        participant_label_file='_rooms/workstation.txt',
    ),
    dict(
        name='Chat_7',
        display_name='Chat_7',
        participant_label_file='_rooms/workstation.txt',
    ),
    dict(
        name='Chat_8',
        display_name='Chat_8',
        participant_label_file='_rooms/workstation.txt',
    ),
dict(
        name='Team_1',
        display_name='Team_1',
        participant_label_file='_rooms/workstation.txt',
    ),
    dict(
        name='Team_2',
        display_name='Team_2',
        participant_label_file='_rooms/workstation.txt',
    ),
    dict(
        name='Team_3',
        display_name='Team_3',
        participant_label_file='_rooms/workstation.txt',
    ),
    dict(
        name='Team_4',
        display_name='Team_4',
        participant_label_file='_rooms/workstation.txt',
    ),
    dict(
        name='Team_5',
        display_name='Team_5',
        participant_label_file='_rooms/workstation.txt',
    ),
    dict(
        name='Team_6',
        display_name='Team_6',
        participant_label_file='_rooms/workstation.txt',
    ),
    dict(
        name='Team_7',
        display_name='Team_7',
        participant_label_file='_rooms/workstation.txt',
    ),
    dict(
        name='Team_8',
        display_name='Team_8',
        participant_label_file='_rooms/workstation.txt',
    ),
]



LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
POINTS_CUSTOM_NAME = 'ECUs'
REAL_WORLD_CURRENCY_DECIMAL_PLACES = 2
USE_POINTS_DECIMAL_PLACES = 0
CSRF_ENABLED = True

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = '123'

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'your_secret_key'

INSTALLED_APPS = ['otree']

DEBUG = True