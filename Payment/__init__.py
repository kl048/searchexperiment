from otree.api import *
import random

doc = """
Payment application: Randomly selects an episode for payment.
Ensures the same episode is selected for both players in Team (T) treatment.
"""

class C(BaseConstants):
    NAME_IN_URL = 'payment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    episode_drawn = models.IntegerField()
    earning_drawn = models.CurrencyField(initial=0)

class Player(BasePlayer):
    episode_drawn = models.IntegerField()
    earning_drawn = models.CurrencyField(initial=0)

def assign_payment_episode(group: Group):
    """ Ensures both teammates receive the same randomly chosen episode before moving to Payment """
    if group.field_maybe_none('episode_drawn') is None:  # Safely check for None values
        player1 = group.get_players()[0]
        earnings_history = player1.participant.vars.get('earnings_history', [])

        selected_episode = random.choice(earnings_history)
        group.episode_drawn = selected_episode['episode']
        group.earning_drawn = cu(selected_episode['earnings'])

    for p in group.get_players():
        p.episode_drawn = group.episode_drawn
        p.earning_drawn = group.earning_drawn


class PaymentWaitPage(WaitPage):
    wait_for_all_groups = False
    after_all_players_arrive = assign_payment_episode

    @staticmethod
    def is_displayed(player: Player):
        treatment = player.session.config['treatment']
        print(f"Checking if WaitPage is displayed for Player {player.id_in_group} in treatment {treatment}")
        return treatment == 'T'

class Payment(Page):
    @staticmethod
    def vars_for_template(player: Player):
        if player.session.config['treatment'] == 'T':
            player.episode_drawn = player.group.episode_drawn
            player.earning_drawn = player.group.earning_drawn
        else:
            earnings_history = player.participant.vars.get('earnings_history', [])
            selected_episode = random.choice(earnings_history)
            player.episode_drawn = selected_episode['episode']
            player.earning_drawn = selected_episode['earnings']  # Keep in ECUs

        # ✅ Store earnings in ECUs (oTree will convert it automatically)
        player.participant.vars['final_payment'] = player.earning_drawn
        player.payoff = player.earning_drawn  # Store as ECU

        # ✅ Debugging: Confirm the correct value is stored
        print(f"DEBUG: In Payment App, stored final_payment (ECU) = {player.earning_drawn}")

        return {
            'selected_episode_number': player.episode_drawn,
            'selected_earnings': player.earning_drawn,
            'final_payment': player.participant.payoff_plus_participation_fee(),
        }


page_sequence = [PaymentWaitPage, Payment]
