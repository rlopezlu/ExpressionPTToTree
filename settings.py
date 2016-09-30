import os
from os import environ

import dj_database_url
from boto.mturk import qualification

import otree.settings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# the environment variable OTREE_PRODUCTION controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
if environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
    DEBUG = False
else:
    DEBUG = True

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'otree'

# don't share this with anybody.
# Change this to something unique (e.g. mash your keyboard),
# and then delete this comment.
SECRET_KEY = 'zzzzzzzzzzzzzzzzzzzzzzzzzzz'

PAGE_FOOTER = ''

# To use a database other than sqlite,
# set the DATABASE_URL environment variable.
# Examples:
# postgres://USER:PASSWORD@HOST:PORT/NAME
# mysql://USER:PASSWORD@HOST:PORT/NAME

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    )
}

# AUTH_LEVEL:
# If you are launching a study and want visitors to only be able to
# play your app if you provided them with a start link, set the
# environment variable OTREE_AUTH_LEVEL to STUDY.
# If you would like to put your site online in public demo mode where
# anybody can play a demo version of your game, set OTREE_AUTH_LEVEL
# to DEMO. This will allow people to play in demo mode, but not access
# the full admin interface.

AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

# ACCESS_CODE_FOR_DEFAULT_SESSION:
# If you have a "default session" set,
# then an access code will be appended to the URL for authentication.
# You can change this as frequently as you'd like,
# to prevent unauthorized server access.

ACCESS_CODE_FOR_DEFAULT_SESSION = 'my_access_code'

# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')


# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False


# e.g. en-gb, de-de, it-it, fr-fr.
# see: https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = []

# SENTRY_DSN = ''

DEMO_PAGE_INTRO_TEXT = """
<ul>
    <li>
        <a href="https://github.com/oTree-org/otree" target="_blank">
            Source code
        </a> for the below games.
    </li>
    <li>
        <a href="http://www.otree.org/" target="_blank">
            oTree homepage
        </a>.
    </li>
</ul>
<p>
    Below are various games implemented with oTree. These games are all open
    source, and you can modify them as you wish to create your own variations.
    Click one to learn more and play.
</p>
"""

# from here on are qualifications requirements for workers
# see description for requirements on Amazon Mechanical Turk website:
# http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html
# and also in docs for boto:
# https://boto.readthedocs.org/en/latest/ref/mturk.html?highlight=mturk#module-boto.mturk.qualification

mturk_hit_settings = {
    'keywords': ['easy', 'bonus', 'choice', 'study'],
    'title': 'Title for your experiment',
    'description': 'Description for your experiment',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 60,
    'expiration_hours': 7*24, # 7 days
    #'grant_qualification_id': 'YOUR_QUALIFICATION_ID_HERE',# to prevent retakes
    'qualification_requirements': [
        # qualification.LocaleRequirement("EqualTo", "US"),
        # qualification.PercentAssignmentsApprovedRequirement("GreaterThanOrEqualTo", 50),
        # qualification.NumberHitsApprovedRequirement("GreaterThanOrEqualTo", 5),
        # qualification.Requirement('YOUR_QUALIFICATION_ID_HERE', 'DoesNotExist')
    ]
}

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.01,
    'participation_fee': 10.00,
    'num_bots': 12,
    'doc': "",
    'mturk_hit_settings': mturk_hit_settings,
}

SESSION_CONFIGS = [
    {
        'name': 'ExpressionPTTv1',
        'display_name': "ExpressionPTTv1",
        'real_world_currency_per_point': 1,
        'num_demo_participants': 8,
        'treatment': ['TP', 'TP', 'TP', 'TPE'],
        'targetIncome': [4, 8, 10, 5],
        'price': [-1, -1, .50, -1],
        'endowment': [3, 5, 3, 5],
        'group': [[1, 2], [3, 4], [5, 6], [7, 8]],
        'role': [['A', 'B'], ['A', 'B'], ['A', 'B'], ['R', 'R']],
        'readerSelection': [1, 2, 1, 0],
        'method': ['WTP', 'WTA', 'WTP', 'WTA'],
        'priceDisplay': ['LIST', 'LIST', 'LIST', 'LIST'],
        'app_sequence': ['ExpressionPTT', 'payment_info'],
        'video': "youtube.com/watch?v=YgdR5FvnNPc",
        'debug': False
    },
    {
        'name': 'ExpressionPTT_DM_CONT_WTP',
        'display_name': "ExpressionPTT_DM_CONT_WTP",
        'real_world_currency_per_point': 2,
        'num_demo_participants': 2,
        'treatment': ['DM'],
        'targetIncome': [4],
        'price': [2],
        'endowment': [3],
        'group': [[1, 2]],
        'role': [['A', 'B']],
        'readerSelection': [0],
        'method': ['WTP'],
        'priceDisplay': ['CONT'],
        'app_sequence': ['batson_emo_survey', 'searchTask', 'ExpressionPTT'],
        'video': "youtube.com/watch?v=YgdR5FvnNPc",
        'debug': False
    },
    {
        'name': 'ExpressionPTT22',
        'display_name': "WTP_Test",
        'real_world_currency_per_point': 1,
        'num_demo_participants': 4,
        'treatment': ['DM', 'DM'],
        'targetIncome': [4, 8],
        'price': [-1, -1],
        'endowment': [3, 5],
        'group': [[1, 2], [3, 4]],
        'role': [['A', 'B'], ['A', 'B']],
        'readerSelection': [1, 2],
        'method': ['WTP', 'WTA'],
        'priceDisplay': ['LIST', 'LIST'],
        'app_sequence': ['ExpressionPTT', 'payment_info'],
        'debug': True
    },
    {
        'name': 'Testing_Debugging',
        'display_name': "Debug_and_testing",
        'real_world_currency_per_point': 1,
        'num_demo_participants': 4,
        'treatment': ['DM', 'NM'],
        'targetIncome': [4, 8],
        'price': [-1, -1],
        'video': "youtube.com/watch?v=YgdR5FvnNPc",
        'endowment': [3, 5],
        'group': [[1, 2], [3, 4]],
        'role': [['A', 'B'], ['A', 'B']],
        'readerSelection': [1, 2],
        'method': ['WTP', 'WTA'],
        'priceDisplay': ['LIST', 'LIST'],
        'app_sequence': ['ExpressionPTT', 'payment_info'],
        'debug': True
    },
    {
        'name': 'Batson_Survey',
        'display_name': 'Batson 1988 Survey',
        'num_demo_participants': 1,
        'app_sequence': ['batson_emo_survey'],
        'debug': False
    },
    {
        'name': 'searchTask',
        'display_name': 'searchTask',
        'num_demo_participants': 4,
        'app_sequence': ['searchTask'],
        'debug': True,
        'targetIncome': [4]
    }
]

# don't put anything after this point.
otree.settings.augment_settings(globals())
