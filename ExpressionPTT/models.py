# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random
import decimal

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json
import json
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer
# </standard imports>

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'ExpressionPTT'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):

    reader_message = models.TextField()
    debug_mode = models.BooleanField()

    def before_session_starts(self):
        group_matrix = []
        empty_messages = []
        readers = max(self.session.config['readerSelection'])
        for reader in range(0, readers):
            empty_messages.append([])
            print(empty_messages)
            print(reader)
        self.reader_message = json.dumps(empty_messages)

        for grouping in self.session.config["group"]:
            print(grouping)
            # assigns groups based on array values in cofig
            group_matrix.append(grouping)

        self.set_group_matrix(group_matrix)
        self.debug_mode = self.session.config['debug']

        i = 0
        for groupx in self.get_groups():
            groupx.treatment_endowment = self.session.config['endowment'][i]
            groupx.treatment_treatment = self.session.config['treatment'][i]
            groupx.target_income = self.session.config['targetIncome'][i]
            groupx.reader_index = self.session.config['readerSelection'][i]
            groupx.price_method = self.session.config['method'][i]
            for player in groupx.get_players():
                player.p_role = self.session.config['role'][i][player.id_in_group-1]

            if groupx.treatment_treatment == 'FM':
                groupx.b_message_price = 0
            else:
                if self.session.config['price'][i] == -1:
                    groupx.b_message_price = random.randrange(0, 300) / 100
                    groupx.price_display = self.session.config['priceDisplay'][i]
                else:
                    groupx.b_message_price = self.session.config['price'][i]
            i += 1
        # message price is different (random) for every group
        print("finished set up before session starts")


class Group(BaseGroup):
    # variables that change for each group
    treatment_endowment = models.IntegerField()
    treatment_treatment = models.TextField()
    a_takes = models.DecimalField(min=0, max=100, max_digits=5, decimal_places=2)
    total_taken = models.CurrencyField()
    b_predicts = models.PositiveIntegerField(min=0, max=100)
    b_willing = models.DecimalField(min=0, max_digits=5, decimal_places=2)
    b_message = models.TextField()
    b_message_price = models.DecimalField(max_digits=5, decimal_places=2)
    price_method = models.TextField()
    price_display = models.TextField()
    b_eligible = models.BooleanField()
    target_income = models.DecimalField(max_digits=5, decimal_places=2)
    reader_index = models.IntegerField()

    def final_pay(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p1.final_reward = self.treatment_endowment+ p1.task_reward + self.total_taken

        if self.price_method != 'WTA':
            if self.b_eligible:
                p2.final_reward = self.treatment_endowment+ p2.task_reward - self.total_taken - self.b_message_price
            else:
                p2.final_reward = self.treatment_endowment + p2.task_reward - self.total_taken
        else:  # WTA
            if self.b_eligible:
                p2.final_reward = self.treatment_endowment + p2.task_reward - self.total_taken
            else:  # gave up right to send message
                p2.final_reward = self.treatment_endowment + p2.task_reward - self.total_taken + self.b_message_price

    def reader_pay(self):
        for p in self.get_players():
            p.final_reward = self.treatment_endowment + p.task_reward


class Player(BasePlayer):
    # variables that change for each player
    task_reward = models.DecimalField(max_digits = 5, decimal_places=2)
    intermediate_reward = models.DecimalField(max_digits=5, decimal_places=2)
    final_reward = models.DecimalField(max_digits=5, decimal_places=2)
    total_pay = models.DecimalField(max_digits=5, decimal_places=2)
    p_role = models.TextField()

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

