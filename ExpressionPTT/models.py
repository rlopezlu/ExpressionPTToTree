# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random
import decimal

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



class Subsession(BaseSubsession):

    def before_session_starts(self):
        group_matrix = []
        i = 0
        for group in self.get_groups():
            group.treatment_endowment = self.session.config['endowment'][i]
            group.treatment_treatment = self.session.config['treatment'][i]
            group_matrix.append( self.session.config['group'][i] )
            i += 1
        self.set_groups()
        self.get_groups()[0].b_message_price = random.randrange(0, 300)/100


class Group(BaseGroup):
    treatment_endowment = models.IntegerField()
    treatment_treatment = models.TextField()
    a_takes = models.DecimalField(min=0, max=100, max_digits=5, decimal_places=2)
    total_taken = models.CurrencyField()
    b_predicts = models.PositiveIntegerField(min=0, max=100)
    b_willing = models.CurrencyField(min=0)
    b_message = models.TextField()
    b_message_price = models.DecimalField(max_digits=5, decimal_places=2)
    b_charged = models.BooleanField()

    def final_pay(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p1.final_reward = self.treatment_endowment+ p1.task_reward + self.total_taken

        if self.b_charged:
            p2.final_reward = self.treatment_endowment+ p2.task_reward - self.total_taken - self.b_message_price
        else:
            p2.final_reward = self.treatment_endowment + p2.task_reward - self.total_taken


class Player(BasePlayer):
    task_reward = models.DecimalField(max_digits = 5, decimal_places=2)
    intermediate_reward = models.DecimalField(max_digits=5, decimal_places=2)
    final_reward = models.DecimalField(max_digits=5, decimal_places=2)
    total_pay = models.DecimalField(max_digits=5, decimal_places=2)

    survey_response0 = models.IntegerField()
    survey_response1 = models.IntegerField()
    survey_response2 = models.IntegerField()
    survey_response3 = models.IntegerField()
    survey_response4 = models.IntegerField()
    survey_response5 = models.IntegerField()

    survey_responseA = models.IntegerField()
    survey_responseB = models.IntegerField()
    survey_responseC = models.IntegerField()
    survey_responseD = models.IntegerField()
    survey_responseE = models.IntegerField()
    survey_responseF = models.IntegerField()

    def get_partner(self):
        return self.get_others_in_group()[0]
