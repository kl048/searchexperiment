from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'Main_game_1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 4
    ENDOWMENT = 20
    ALPHA = 0.5
    THETA = 100
    PERIODS = {1: 5, 2: 7, 3: 5, 4:4}
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
    form_fields = ['reservation_wage']

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):
        set_Max_period(player)


class Searching(Page):
    form_model = 'player'
    form_fields = ['wage_offer','wage_offer_history','accepted']
    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):
        if player.session.config['treatment'] in ['I', 'C']:
            set_earnings_I_C(player)


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

        # Save episode number and earnings to participant variable
        if 'earnings_history' not in player.participant.vars:
            player.participant.vars['earnings_history'] = []

        # Append current episode data
        player.participant.vars['earnings_history'].append({
            'episode': player.round_number,
            'earnings': player.earnings,
        })
        
        return {
            'Treatment': treatment,
            'partner_accepted': partner.accepted if treatment == 'T' else None,
            'partner_earnings_before_sharing': partner.earnings_before_sharing if treatment == 'T' else None,
            'partner_earning_after_sharing': partner.earnings if treatment == 'T' else None,
        }


page_sequence = [WaitForPartner_begin, Chat, SetReservationWage,Searching,WaitForPartner_end, Results]
