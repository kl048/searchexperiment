from otree.api import *
import random

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'payment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    episode_drawn = models.IntegerField()
    earning_drawn = models.CurrencyField(initial=0)


# PAGES
class Payment(Page):
    @staticmethod
    def vars_for_template(player: Player):
        # Access the earnings history from participant variables
        earnings_history = player.participant.vars.get('earnings_history', [])
        selected_episode = random.choice(earnings_history)
        selected_earnings = selected_episode['earnings']
        selected_episode_number = selected_episode['episode']
        player.earning_drawn = selected_earnings
        player.episode_drawn = selected_episode_number
        player.participant.payoff = selected_earnings

        return {
            'selected_episode_number': selected_episode_number,
            'selected_earnings': selected_earnings,
            'final_payment': player.participant.payoff_plus_participation_fee(),
        }

page_sequence = [Payment]
