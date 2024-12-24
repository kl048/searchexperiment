from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'T_individual'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 95
    ENDOWMENT = 20
    ALPHA = 0.5
    THETA = 100
    PERIODS = {1: 5, 2: 7, 3: 5, 4:4}


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    reservation_wage = models.IntegerField(
        min=1,
        max=C.THETA,
        label="Set your reservation wage",
        initial=0
    )
    wage_offer = models.IntegerField(blank=True)
    accepted = models.BooleanField(initial=False)
    earnings = models.CurrencyField(initial=0)
    max_period_in_episode = models.IntegerField()

# Function
def set_Max_period(player: Player):
    player.max_period_in_episode = C.PERIODS[player.current_episode]


def set_earnings(player: Player):
    if player.accepted == True:
        player.earnings = player.wage_offer
    else:
        player.earnings = C.ENDOWMENT

# PAGES
class SetReservationWage(Page):
    form_model = 'player'
    form_fields = ['reservation_wage']

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):
        set_Max_period(player)


class Searching(WaitPage):
    form_model = 'player'
    form_fields = ['wage_offer','accepted']

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):
        set_earnings(player)


class Results(Page):
    pass


page_sequence = [SetReservationWage,Searching, Results]
