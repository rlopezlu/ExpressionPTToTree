from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range, safe_json
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'searchTask'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    def before_session_starts(self):
        group_matrix = []
        for grouping in self.session.config["group"]:
            print(grouping)
            # assigns groups based on array values in cofig
            group_matrix.append(grouping)
        self.set_group_matrix(group_matrix)
        i = 0
        for groupx in self.get_groups():
            groupx.target_income = self.session.config['targetIncome'][i]


class Group(BaseGroup):
    target_income = models.DecimalField(max_digits=5, decimal_places=2)


class Player(BasePlayer):
    task_reward = models.DecimalField(max_digits=5, decimal_places=2)
