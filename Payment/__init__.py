from otree.api import *
import random

doc = """
Your app description
"""

class C(BaseConstants):
    NAME_IN_URL = 'payment'
    PLAYERS_PER_GROUP = None  # Still dynamic
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    episode_drawn = models.IntegerField()
    earning_drawn = models.CurrencyField(initial=0)

class Player(BasePlayer):
    episode_drawn = models.IntegerField()
    earning_drawn = models.CurrencyField(initial=0)

# ✅ **WaitPage for Teams**
class PaymentWaitPage(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.vars.get('treatment') == 'T'  # Only for Team Treatment

    @staticmethod
    def after_all_players_arrive(group: Group):
        """Selects a random payment round ONCE for both players in the team"""
        player1 = group.get_players()[0]  # Get the first player in the team
        earnings_history = player1.participant.vars.get('earnings_history', [])
        selected_episode = random.choice(earnings_history)
        group.episode_drawn = selected_episode['episode']
        group.earning_drawn = cu(selected_episode['earnings'])

# ✅ **Payment Page**
class Payment(Page):
    @staticmethod
    def vars_for_template(player: Player):
        # Assign the selected round for Team Treatment
        if player.participant.vars.get('treatment') == 'T':
            player.episode_drawn = player.group.episode_drawn
            player.earning_drawn = player.group.earning_drawn
        else:  # Individual and Chat Treatments
            earnings_history = player.participant.vars.get('earnings_history', [])
            selected_episode = random.choice(earnings_history)
            player.episode_drawn = selected_episode['episode']
            player.earning_drawn = cu(selected_episode['earnings'])

        # Store the selected earnings as the final payoff
        player.participant.payoff = player.earning_drawn

        return {
            'selected_episode_number': player.episode_drawn,
            'selected_earnings': player.earning_drawn,
            'final_payment': player.participant.payoff_plus_participation_fee(),
        }

page_sequence = [PaymentWaitPage, Payment]
