from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range, safe_json
)


author = 'Batson Emotion Survey'

doc = """
This applies the Batson 88 emotion survey
"""


class Constants(BaseConstants):
    name_in_url = 'batson_emo_survey'
    players_per_group = None
    num_rounds = 2


class Subsession(BaseSubsession):

    debug_mode = models.BooleanField()

    def before_session_starts(self):
        self.debug_mode = self.session.config['debug']


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    survey_response0 = models.IntegerField()
    survey_response1 = models.IntegerField()
    survey_response2 = models.IntegerField()
    survey_response3 = models.IntegerField()
    survey_response4 = models.IntegerField()
    survey_response5 = models.IntegerField()
