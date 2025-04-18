import json
from otree.api import *

doc = """

"""


class C(BaseConstants):
    NAME_IN_URL = 'Main_game_1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 20
    ENDOWMENT = 10
    THETA = 100
    PERIODS = {
        1: 10,
        2: 8,
        3: 3,
        4: 3,
        5: 1,
        6: 32,
        7: 3,
        8: 9,
        9: 35,
        10: 4,
        11: 8,
        12: 13,
        13: 23,
        14: 9,
        15: 7,
        16: 5,
        17: 11,
        18: 5,
        19: 16,
        20: 2,
    }
    CHAT_LONG = 60
    CHAT_SHORT = 30
    NUM_CHAT_LONG = 5


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    reservation_wage = models.IntegerField(
        min=0,
        max=C.THETA,
        label="Set your reservation wage",
        initial=0
    )
    wage_offer_history = models.StringField()
    wage_offer = models.IntegerField(blank=True)
    accepted = models.BooleanField(initial=False)
    earnings = models.CurrencyField(initial=0)
    earnings_before_sharing = models.CurrencyField(initial=0)
    max_period_in_episode = models.IntegerField()
    instructions_count = models.IntegerField(initial=0)
    decision_history = models.StringField()
    continue_history = models.StringField()

    def serialize_history(self, history_list):
        return json.dumps(history_list)

    def deserialize_history(self, history_str):
        return json.loads(history_str) if history_str else []


# Function
def set_Max_period(player: Player):
    player.max_period_in_episode = C.PERIODS[player.round_number]


def set_earnings_I_C(player: Player):
    if player.accepted == True:
        player.earnings = player.wage_offer
    else:
        player.earnings = C.ENDOWMENT


def set_earnings_T(group: Group):
    total_earnings = 0

    for player in group.get_players():
        # Calculate earnings before sharing
        if player.accepted:
            player.earnings_before_sharing = player.wage_offer
        else:
            player.earnings_before_sharing = C.ENDOWMENT

        # Add to total group earnings
        total_earnings += player.earnings_before_sharing

    # Calculate shared earnings
    shared_earnings = total_earnings / len(group.get_players())

    # Assign shared earnings to each player
    for player in group.get_players():
        player.earnings = shared_earnings


# PAGES
class WaitForPartner_begin(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.session.config['treatment'] in ['C', 'T']


class Chat(Page):
    timer_text = 'Time left for chatting:'

    @staticmethod
    def get_timeout_seconds(player: Player):
        if player.round_number <= C.NUM_CHAT_LONG:
            return C.CHAT_LONG
        else:
            return C.CHAT_SHORT

    @staticmethod
    def is_displayed(player: Player):
        return player.session.config['treatment'] in ['C', 'T']

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'chat_duration': C.CHAT_LONG if player.round_number <= C.NUM_CHAT_LONG else C.CHAT_SHORT
        }


class SetReservationWage(Page):
    form_model = 'player'
    form_fields = ['reservation_wage', 'instructions_count']

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):
        set_Max_period(player)


class Searching(Page):
    form_model = 'player'
    form_fields = [
        'wage_offer',
        'accepted',
        'wage_offer_history',
        'decision_history',
        'continue_history'
    ]

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):
        wage_offer_history = player.deserialize_history(player.wage_offer_history)
        decision_history = player.deserialize_history(player.decision_history)
        continue_history = player.deserialize_history(player.continue_history)

        # DO NOT CHANGE THESE HISTORY VALUES; they come correctly from JS already.
        player.wage_offer_history = player.serialize_history(wage_offer_history)
        player.decision_history = player.serialize_history(decision_history)
        player.continue_history = player.serialize_history(continue_history)

        # Earnings for individual treatment explicitly calculated here
        if player.accepted:
            player.earnings = player.wage_offer
        else:
            player.earnings = C.ENDOWMENT



class WaitForPartner_end(WaitPage):
    after_all_players_arrive = set_earnings_T

    @staticmethod
    def is_displayed(player: Player):
        return player.session.config['treatment'] == 'T'


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        #  Ensure `earnings_history` is stored properly for Payment
        if 'earnings_history' not in player.participant.vars:
            player.participant.vars['earnings_history'] = []  #  Ensure the variable exists

        #  Append episode number and earnings to `participant.vars`
        player.participant.vars['earnings_history'].append({
            'episode': player.round_number,
            'earnings': player.earnings,
        })

        #  Debugging: Print `earnings_history` to confirm it's being stored
        print(f"DEBUG: Earnings history in Results Page: {player.participant.vars['earnings_history']}")

        # Deserialize history data to ensure it's available
        wage_offer_history = json.loads(player.wage_offer_history) if player.wage_offer_history else []
        decision_history = json.loads(player.decision_history) if player.decision_history else []
        continue_history = json.loads(player.continue_history) if player.continue_history else []

        #  Ensure all lists are the same length
        max_length = max(len(wage_offer_history), len(decision_history), len(continue_history))

        while len(wage_offer_history) < max_length:
            wage_offer_history.append({"wageOffer": "No offer", "period": len(wage_offer_history) + 1})
        while len(decision_history) < max_length:
            decision_history.append("Reject")
        while len(continue_history) < max_length:
            continue_history.append("Yes")

        #  Prepare data for results table (no changes from your version)
        earnings_history_data = []
        for i in range(len(wage_offer_history)):
            offer = wage_offer_history[i]['wageOffer'] if isinstance(wage_offer_history[i], dict) else "No offer"
            decision = decision_history[i] if decision_history[i] else "Reject"
            continue_status = continue_history[i] if continue_history[i] else "Yes"

            earnings_history_data.append({
                'period': i + 1,
                'offer': offer,
                'decision': decision,
                'continue': continue_status
            })

        return {
            'earnings_history_data': earnings_history_data,
            'player_earnings': player.earnings,
            'reservation_wage': player.reservation_wage
        }

class ReflectionPage(Page):
    @staticmethod
    def is_displayed(player: Player):
        return True

    @staticmethod
    def vars_for_template(player: Player):
        # 60 seconds for rounds 1–5, otherwise 30 seconds
        duration = 60 if player.round_number <= 5 else 30
        return {'duration': duration}



page_sequence = [WaitForPartner_begin, Chat, ReflectionPage, SetReservationWage, Searching, WaitForPartner_end, Results]