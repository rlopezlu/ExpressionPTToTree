# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Results(Page):
    pass


class SurveyStart (Page):
    pass


class SurveyWaitPage (WaitPage):
    pass


class Part1 (Page):
    pass


class Part1Game(Page):
    print('got to part1')
    form_model = models.Player
    form_fields = ['task_reward']

    def before_next_page(self):
        print('got to before')
        self.player.final_reward = self.player.task_reward + models.Constants.endowment


class Part1Result(Page):
    pass


class Part1Wait(WaitPage):
    pass


class Part2 (Page):
    pass


class Roles (Page):
    def vars_for_template(self):
        return {
            'partner': self.player.get_partner()
        }


class TakeA(Page):

    form_model = models.Group
    form_fields = ['A_takes']

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        return {
            'partner': self.player.get_partner()
        }


class PredictB(Page):
    form_model = models.Group
    form_fields = ['B_predicts']

    def is_displayed(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):
        return {
            'partner': self.player.get_partner()
        }


class WillingnessB(Page):
    def is_displayed(self):
        return self.player.id_in_group == 2

    form_model = models.Group
    form_fields = ['B_willing']

    def vars_for_template(self):
        return {
            'partner': self.player.get_partner(),
            'taken_amount': self.player.task_reward * (self.group.A_takes * .01)
        }


class WaitForMessage(WaitPage):
    pass


class SurveyEnd (Page):
    pass


class ThankYou (Page):
    pass


page_sequence = [
    SurveyStart,
    # SurveyWaitPage,
    Part1,
    Part1Game,
    Part1Result,
    Part1Wait,
    Part2,
    Roles,
    TakeA,
    PredictB,
    WillingnessB,
    WaitForMessage,
    SurveyEnd,
    ThankYou
]