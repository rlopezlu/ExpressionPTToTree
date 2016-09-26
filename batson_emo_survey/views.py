from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants



class EmotionSurvey(Page):

    def is_displayed(self):
        return not self.subsession.debug_mode

    form_model = models.Player
    form_fields = ['survey_response0',
                   'survey_response1',
                   'survey_response2',
                   'survey_response3',
                   'survey_response4',
                   'survey_response5',
                   ]

class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


page_sequence = [
    EmotionSurvey
]
