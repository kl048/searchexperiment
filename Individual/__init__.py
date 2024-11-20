from otree.api import *
import random

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'Treament_Indivudal'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 95
    ENDOWMENT = 20
    ALPHA = 0.5
    THETA = 100
    PERIODS = {1: 5, 2: 7, 3: 5, 4:4, 5:6, 6:3, 7:5, 8:4, 9:6, 10:2, 11:4, 12:3, 13:6, 14:7, 15:4, 16:5, 17:3, 18:8, 19:6, 20:6}
    MAX_EPISODE = 20


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
    current_episode = models.IntegerField()
    period_in_episode = models.IntegerField()
    max_period_in_episode = models.IntegerField()
    check = models.IntegerField()

#function:
def creating_session(subsession:Subsession):
    for player in subsession.get_players():
        if "New_episode" not in player.participant.vars:
            player.participant.vars["New_episode"] = True
            player.current_episode = 1

            
def set_Max_period(player: Player):
    player.max_period_in_episode = C.PERIODS[player.current_episode]



def set_wage_offer(player: Player):
    if random.random() < C.ALPHA:  # 50% chance to make a wage offer
        player.wage_offer = random.randint(1, C.THETA)  # Draw wage from U[1,100]
    else:
        player.wage_offer = None  # No offer

def set_earnings(player: Player):
    if player.field_maybe_none('wage_offer') is not None and player.wage_offer >= player.reservation_wage:
        player.accepted = True
        player.earnings = player.wage_offer
    else:
        player.accepted = False
        if player.period_in_episode == player.max_period_in_episode:
            # Only set earnings to 20 ECUs at the end of the episode
            player.earnings = C.ENDOWMENT
        else:
            player.earnings = 0  # Earnings remain 0 until the last period



# PAGES
class SetReservationWage(Page):
    form_model = 'player'
    form_fields = ['reservation_wage']

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.vars.get("New_episode") == True

    @staticmethod
    def vars_for_template(player: Player):
        if player.round_number > 1:
            player.current_episode = player.in_round(player.round_number - 1).current_episode + 1  
        return {
            'search_episode_number': player.current_episode,
            'endowment': C.ENDOWMENT,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):
        player.participant.vars["Reservation"] = player.reservation_wage
        player.period_in_episode = 1

    


class Searching(Page):

    @staticmethod
    def vars_for_template(player: Player):
        player.participant.vars["New_episode"] = False
        if not player.field_maybe_none('current_episode'):
            player.current_episode = player.in_round(player.round_number - 1).current_episode
        set_Max_period(player)    
        if not player.field_maybe_none('period_in_episode'):
            player.period_in_episode = player.in_round(player.round_number - 1).period_in_episode + 1   
        if player.period_in_episode > 1:
            player.reservation_wage = player.participant.vars.get("Reservation")
        set_wage_offer(player)
        wage_offer = player.field_maybe_none('wage_offer') or 'No offer'
        set_earnings(player)


        return {
            'search_episode_number': player.current_episode,
            'period_number': player.period_in_episode,
            'wage_offer': wage_offer,
            'reservation_wage': player.reservation_wage,
            'accepted': player.accepted,
        }



class Results(Page):

    @staticmethod
    def is_displayed(player: Player):
        return player.accepted or player.period_in_episode == player.max_period_in_episode
    def before_next_page(player: Player, timeout_happened=False):
        player.participant.vars["New_episode"] = True
        
    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.current_episode == C.MAX_EPISODE:
            return upcoming_apps[0]    

page_sequence = [SetReservationWage,Searching, Results]
