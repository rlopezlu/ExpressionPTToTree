# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer
# </standard imports>

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'ExpressionPTT'
    players_per_group = 2
    num_rounds = 1

    endowment = c(3)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    a_takes = models.PositiveIntegerField(min=0, max=100)
    total_taken = models.CurrencyField()
    b_predicts = models.PositiveIntegerField(min=0, max=100)
    b_willing = models.CurrencyField(min=0)
    b_message = models.TextField()


class Player(BasePlayer):
    task_reward = models.CurrencyField()
    intermediate_reward = models.CurrencyField()

    survey_response0 = models.CurrencyField()
    survey_response1 = models.CurrencyField()
    survey_response2 = models.CurrencyField()
    survey_response3 = models.CurrencyField()
    survey_response4 = models.CurrencyField()
    survey_response5 = models.CurrencyField()

    total_pay = models.CurrencyField()

    def get_partner(self):
        return self.get_others_in_group()[0]



