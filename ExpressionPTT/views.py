# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import json
import random
from decimal import Decimal


class Part1Game (Page):
    form_model = models.Player
    form_fields = ['task_reward']

    def before_next_page(self):
        print('got to before')
        if self.subsession.debug_mode:
            self.player.task_reward = random.uniform(1, 5)
        self.player.intermediate_reward = self.player.task_reward + self.group.treatment_endowment


class PracticeGame (Page):
    def is_displayed(self):
        return not self.subsession.debug_mode
    pass


class SurveyStart (Page):

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

    def before_next_page(self):
        print('got to player response')
        # print(self.player.survey_response)


class SurveyWaitPage (WaitPage):
    def is_displayed(self):
        return not self.subsession.debug_mode
    pass


class Part1 (Page):
    pass


class Video(Page):
    def is_displayed(self):
        return not self.subsession.debug_mode
    pass


class Part1Result(Page):
    def is_displayed(self):
        return not self.subsession.debug_mode

    def vars_for_template(self):
        return {'reward': self.player.task_reward}
    pass


class Part1Wait(WaitPage):
    pass


class Part2 (Page):
    def is_displayed(self):
        return not self.subsession.debug_mode
    pass


class Roles (Page):
    def is_displayed(self):
        return not self.player.p_role == "R"

    def vars_for_template(self):
        return {
            'partner': self.player.get_partner()
        }


class TakeA(Page):

    form_model = models.Group
    form_fields = ['a_takes']

    def is_displayed(self):
        return self.player.p_role == 'A'  # and not self.player.p_role == "R"

    def vars_for_template(self):
        return {
            'partner': self.player.get_partner()
        }

    def before_next_page(self):
        self.group.a_takes *= Decimal(.01)


class TakeWaitPage(WaitPage):

    pass


class PredictB(Page):
    form_model = models.Group
    form_fields = ['b_predicts']

    def is_displayed(self):
        return self.player.p_role == 'B'

    def vars_for_template(self):
        return {
            'partner': self.player.get_partner()
        }

    def before_next_page(self):
        self.group.total_taken = self.player.task_reward * self.group.a_takes


class WillingnessB(Page):
    def is_displayed(self):
        return self.group.price_display == 'CONT' and self.player.p_role == 'B' and (self.group.treatment_treatment == 'DM' or self.group.treatment_treatment == 'TP')

    form_model = models.Group
    form_fields = ['b_willing']

    def b_willing_max(self):
        if self.group.price_method == "WTA":
            return 100
        return self.player.task_reward - self.player.task_reward * self.group.a_takes

    def vars_for_template(self):
        return {
            'a_takes_edited': self.group.a_takes * 100,
            'partner': self.player.get_partner(),
            'taken_amount': round(self.player.task_reward * self.group.a_takes, 2),
            'available_earnings': round(self.player.task_reward - self.player.task_reward * self.group.a_takes, 2)
        }

    def before_next_page(self):
        if self.group.b_message_price <= self.group.b_willing and self.group.price_method == 'WTP':
            self.group.b_eligible = True
        else:
            self.group.b_eligible = False
        #  if they give you more than you ask for, you lose your message and get the money
        if self.group.b_message_price <= self.group.b_willing and self.group.price_method == 'WTA':  # will lose right to send message
            self.group.b_eligible = True
        else:
            self.group.b_eligible = False

        if self.subsession.debug_mode and self.group.price_method != 'WTA':
            self.group.b_eligible = True


class WillingnessBList(Page):
    def is_displayed(self):
        return self.group.price_display == 'LIST' and self.player.p_role == 'B' and (self.group.treatment_treatment == 'DM' or self.group.treatment_treatment == 'TP')

    form_model = models.Group
    form_fields = ['b_willing']

    def b_willing_choices(self):
        available = round(self.player.task_reward - (self.player.task_reward * self.group.a_takes), 2)
        if self.group.price_method == 'WTA':
            return [x * 0.5 for x in range(0, 10 + 1, 20)]
        if self.group.price_method == 'WTP':
            print(available)
            new_available = int(available * 100)
            print(new_available)
            # return [x * 0.5 for x in range(0, 10 + 1)]
            return [x / 100 for x in range(0, new_available + 1, 20)]
        # return range(0, self.player.task_reward, 1)

    def b_willing_max(self):
        if self.group.price_method == "WTA":
            return 100
        return self.player.task_reward - self.player.task_reward * self.group.a_takes

    def vars_for_template(self):
        return {
            'a_takes_edited': self.group.a_takes * 100,
            'partner': self.player.get_partner(),
            'taken_amount': round(self.player.task_reward * self.group.a_takes, 2),
            'available_earnings': round(self.player.task_reward - self.player.task_reward * self.group.a_takes, 2)
        }

    def before_next_page(self):
        if self.group.b_message_price <= self.group.b_willing and self.group.price_method == 'WTP':
            self.group.b_eligible = True
        else:
            self.group.b_eligible = False
        #  if they give you more than you ask for, you lose your message and get the money
        if self.group.b_message_price <= self.group.b_willing and self.group.price_method == 'WTA':  # will lose right to send message
            self.group.b_eligible = True
        else:
            self.group.b_eligible = False

        if self.subsession.debug_mode and self.group.price_method != 'WTA':
            self.group.b_eligible = True


class SendMessage(Page):
    form_model = models.Group
    form_fields = ['b_message']

    def is_displayed(self):
        return (self.group.b_eligible and (
            self.group.treatment_treatment == 'DM' or self.group.treatment_treatment == 'TP') or self.group.treatment_treatment == 'FM') and self.player.p_role == 'B'

    # add message to list of reader messages
    def before_next_page(self):
        jsonDec = json.decoder.JSONDecoder()
        messages_list = jsonDec.decode(self.subsession.reader_message)
        print(messages_list)
        reader = self.group.reader_index - 1

        messages_list[reader].append(self.group.b_message)
        print(messages_list)
        print(messages_list[reader])
        self.subsession.reader_message = json.dumps(messages_list)
        print(self.subsession.reader_message)


class WaitForMessage(WaitPage):
    def is_displayed(self):
        return not self.group.treatment_treatment == 'TP'
    pass


class WaitForManyMessage(WaitPage):
    def is_displayed(self):
        return self.group.treatment_treatment == 'TP' or self.group.treatment_treatment == 'TPE'
    wait_for_all_groups = True
    pass


class ReaderManyMessages(Page):
    def is_displayed(self):
        return (self.group.treatment_treatment == 'TP' or self.group.treatment_treatment == 'TPE') \
               and self.player.p_role == "R"

    def vars_for_template(self):
        jsonDec = json.decoder.JSONDecoder()
        messages_list = jsonDec.decode(self.subsession.reader_message)
        return {
            'messages': messages_list[self.player.id_in_group - 1],
            'allMessages': messages_list
        }


class DisplayMessage(Page):
    def is_displayed(self):
        play = self.player
        group = self.group
        # play.total_pay = play.intermediate_reward + play.task_reward * self.group.a_takes
        return play.p_role == 'A' and (
            group.treatment_treatment == 'DM' or group.treatment_treatment == 'FM') or (
            play.p_role == 'R' and group.treatment_treatment == 'TP')

    def before_next_page(self):
        self.player.total_pay = self.group.treatment_endowment + self.player.task_reward + self.group.total_taken


class MessageReadWait(WaitPage):
    pass


class MessageRead(Page):

    def is_displayed(self):
        # old
        # return self.player.p_role == 'B' and (
        #     self.group.treatment_treatment == 'DM' or self.group.treatment_treatment == 'FM' or self.group.treatment_treatment == 'TP')
        # new
        return self.player.p_role == 'B' and (self.group.b_eligible and (
            self.group.treatment_treatment == 'DM' or self.group.treatment_treatment == 'TP') or self.group.treatment_treatment == 'FM')


    def before_next_page(self):
        self.group.final_pay()


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            if p.p_role == 'R':
                self.group.reader_pay()
            else:
                self.group.final_pay()


class Results(Page):
    def vars_for_template(self):
        if self.player.p_role != 'R':
            return {
                'partner': self.player.get_partner(),
                'paycheck': self.group.treatment_endowment + self.player.task_reward + self.group.total_taken,
            }
        else:
            return {
                'partner': "no partner",
                'paycheck': self.group.treatment_endowment + self.player.task_reward
            }


class SurveyEnd (Page):
    form_model = models.Player
    form_fields = ['survey_responseA',
                   'survey_responseB',
                   'survey_responseC',
                   'survey_responseD',
                   'survey_responseE',
                   'survey_responseF',
                   ]


class ThankYou (Page):
    pass


page_sequence = [
    SurveyStart,
    SurveyWaitPage,
    Part1,
    Video,
    PracticeGame,
    Part1Game,
    Part1Result,
    Part1Wait,
    Part2,
    Roles,
    TakeA,
    TakeWaitPage,
    PredictB,
    WillingnessB,
    WillingnessBList,
    SendMessage,
    WaitForMessage,
    WaitForManyMessage,
    ReaderManyMessages,
    DisplayMessage,
    MessageReadWait,
    MessageRead,
    ResultsWaitPage,
    Results,
    SurveyEnd,
]
