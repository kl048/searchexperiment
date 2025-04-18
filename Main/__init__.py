import json
from otree.api import *

doc = """

"""

class C(BaseConstants):
    NAME_IN_URL = 'Main_game_2'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 20
    ENDOWMENT = 10
    THETA = 100
    CHAT_LONG = 60
    CHAT_SHORT = 30
    NUM_CHAT_LONG = 5
    EXCHANGE_RATE = 0.20
    PERIODS = {
        1: (10, 5),
        2: (8, 8),
        3: (3, 2),
        4: (3, 4),
        5: (1, 22),
        6: (32, 18),
        7: (3, 4),
        8: (9, 8),
        9: (35, 4),
        10: (4, 11),
        11: (8, 50),
        12: (13, 22),
        13: (23, 3),
        14: (9, 3),
        15: (7, 1),
        16: (5, 38),
        17: (11, 21),
        18: (5, 6),
        19: (16, 3),
        20: (2, 8),
    }


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
    wage_offer_history = models.StringField()  # Store as a JSON string
    wage_offer = models.IntegerField(blank=True)
    accepted = models.BooleanField(initial=False)
    earnings = models.CurrencyField(initial=0)
    earnings_before_sharing = models.CurrencyField(initial=0)
    max_period_in_episode = models.IntegerField()
    instructions_count = models.IntegerField(initial=0)
    decision_history = models.StringField(initial='')  # Store as a JSON string
    continue_history = models.StringField(initial='')  # Store as a JSON string

    # Function to serialize a list to a JSON string
    def serialize_history(self, history_list):
        return json.dumps(history_list)

    # Function to deserialize a JSON string to a list
    def deserialize_history(self, history_str):
        return json.loads(history_str) if history_str else []

# Function to set max period for each round
def set_Max_period(player: Player):
    i = player.id_in_group  # 1 or 2
    player.max_period_in_episode = C.PERIODS[player.round_number][i - 1]


# Function to set earnings for Individual and Chat treatment
def set_earnings_I_C(player: Player):
    if player.accepted == True:
        player.earnings = player.wage_offer
    else:
        player.earnings = C.ENDOWMENT

# Function to set earnings for Team treatment
def set_earnings_T(group: Group):
    total_earnings = 0

    for player in group.get_players():
        if player.accepted:
            player.earnings_before_sharing = player.wage_offer
        else:
            player.earnings_before_sharing = C.ENDOWMENT

        total_earnings += player.earnings_before_sharing

    shared_earnings = total_earnings / len(group.get_players())

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

    @staticmethod
    def vars_for_template(player: Player):
        treatment = player.session.config['treatment']

        return {
            'Treatment': treatment,
        }


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

        # 🔍 Debug earnings before updating
        print(f"DEBUG: Player {player.id_in_group} - Treatment {player.session.config['treatment']} - Earnings BEFORE updating: {player.earnings}")

        #  Ensure earnings are set correctly for Individual and Chat treatments
        if player.session.config['treatment'] in ['I', 'C']:  # Individual and Chat Treatments
            if player.accepted:
                player.earnings = player.wage_offer  #  Assign the accepted wage
            else:
                player.earnings = C.ENDOWMENT  #  Assign the fixed endowment

        # 🔍 Debug earnings after updating
        print(f"DEBUG: Player {player.id_in_group} - Treatment {player.session.config['treatment']} - Earnings AFTER updating: {player.earnings}")

        #  Store updated history values
        player.wage_offer_history = player.serialize_history(wage_offer_history)
        player.decision_history = player.serialize_history(decision_history)
        player.continue_history = player.serialize_history(continue_history)


class WaitForPartner_end(WaitPage):
    after_all_players_arrive = set_earnings_T

    @staticmethod
    def is_displayed(player: Player):
        return player.session.config['treatment'] == 'T'


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        treatment = player.session.config['treatment']
        partner = player.get_others_in_group()[0] if treatment == 'T' else None

        # Debug earnings before storing in earnings_history
        print(f"DEBUG: Player {player.id_in_group} - Treatment {treatment} - Episode {player.round_number} Earnings BEFORE Storing: {player.earnings}")

        # Ensure earnings_history exists
        if 'earnings_history' not in player.participant.vars:
            player.participant.vars['earnings_history'] = []
            print(f"DEBUG: Created new earnings_history for Player {player.id_in_group}")

        # Store earnings history for this episode
        player.participant.vars['earnings_history'].append({
            'episode': player.round_number,
            'earnings': player.earnings,
        })

        # Debug after updating earnings_history
        print(f"DEBUG: Updated Earnings History in Results Page for Player {player.id_in_group}: {player.participant.vars['earnings_history']}")

        # Deserialize stored JSON history
        wage_offer_history = json.loads(player.wage_offer_history) if player.wage_offer_history else []
        decision_history = json.loads(player.decision_history) if player.decision_history else []
        continue_history = json.loads(player.continue_history) if player.continue_history else []

        # Debug history data lengths before adjustment
        print(f"DEBUG: Player {player.id_in_group} - Wage Offer History Length: {len(wage_offer_history)}, Decision History Length: {len(decision_history)}, Continue History Length: {len(continue_history)}")

        # Ensure all lists are the same length
        max_length = max(len(wage_offer_history), len(decision_history), len(continue_history))
        while len(wage_offer_history) < max_length:
            wage_offer_history.append({"wageOffer": "No offer", "period": len(wage_offer_history) + 1})
        while len(decision_history) < max_length:
            decision_history.append("Reject")
        while len(continue_history) < max_length:
            continue_history.append("Yes")

        # Debug final history data after adjustments
        print(f"DEBUG: Final Wage Offer History for Player {player.id_in_group}: {wage_offer_history}")
        print(f"DEBUG: Final Decision History for Player {player.id_in_group}: {decision_history}")
        print(f"DEBUG: Final Continue History for Player {player.id_in_group}: {continue_history}")

        # Ensure earnings history isn't exceeding allowed periods
        if len(wage_offer_history) > player.max_period_in_episode:
            wage_offer_history = wage_offer_history[:player.max_period_in_episode]
            decision_history = decision_history[:player.max_period_in_episode]
            continue_history = continue_history[:player.max_period_in_episode]

        # Construct earnings history data for display
        earnings_history_data = []
        for i in range(len(wage_offer_history)):
            offer = wage_offer_history[i]['wageOffer'] if isinstance(wage_offer_history[i], dict) else "No offer"
            decision = decision_history[i]
            continue_status = continue_history[i]

            earnings_history_data.append({
                'period': i + 1,
                'offer': offer,
                'decision': decision,
                'continue': continue_status
            })

        # Final debug before returning vars_for_template
        print(f"DEBUG: Final earnings_history_data for Player {player.id_in_group}: {earnings_history_data}")

        return {
            'Treatment': treatment,
            'partner_accepted': partner.accepted if treatment == 'T' else None,
            'partner_reservation_wage': partner.reservation_wage if treatment == 'T' else None,
            'partner_earnings_before_sharing': partner.earnings_before_sharing if treatment == 'T' else None,
            'partner_earnings_after_sharing': partner.earnings if treatment == 'T' else None,
            'earnings_history_data': earnings_history_data,
        }


page_sequence = [WaitForPartner_begin, Chat, SetReservationWage, Searching, WaitForPartner_end, Results ]
