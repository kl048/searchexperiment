from otree.api import *
import random

doc = """
players chat but make individual decisions
"""


class C(BaseConstants):
    NAME_IN_URL = 'Treament_Chat'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 95
    ENDOWMENT = 20
    ALPHA = 0.5
    THETA = 100
    PERIODS = {1: 5, 2: 7, 3: 5, 4: 4, 5: 6, 6: 3, 7: 5, 8: 4, 9: 6, 10: 2, 11: 4, 12: 3, 13: 6, 14: 7, 15: 4, 16: 5,
               17: 3, 18: 8, 19: 6, 20: 6}
    MAX_EPISODE = 20
    CHAT_TIME_LONG = 60
    CHAT_TIME_SHORT = 30


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
    nickname = models.StringField()
    chat_duration = models.IntegerField()


# function:
def creating_session(subsession: Subsession):
    for player in subsession.get_players():
        if "New_episode" not in player.participant.vars:
            player.participant.vars["New_episode"] = True
            player.current_episode = 1
            player.period_in_episode = 1
            player.nickname = f"Player {player.id_in_group}"


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

class WaitForPartner(WaitPage):
    wait_for_all_groups = False  # Ensures only paired participants are synchronized


class Chat(Page):
    timeout_seconds = 60  # Set a fixed timeout directly

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.vars.get("New_episode") == True

    @staticmethod
    def vars_for_template(player: Player):
        # Use a temporary variable for template purposes
        current_episode = player.field_maybe_none('current_episode') or 1
        nickname = player.field_maybe_none('nickname') or f"Player {player.id_in_group}"

        return {
            'search_episode_number': current_episode,  # Use the safe variable in the template
            'nickname': nickname,
            'chat_duration': 60
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):
        pass



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
        player.participant.vars["New_episode"] = False  # Reset here, not in Chat

class Searching(Page):

    @staticmethod
    def vars_for_template(player: Player):
        # Set New_episode to False only after SetReservationWage, not in Chat or Searching
        player.participant.vars["New_episode"] = False

        # Ensure current_episode and period_in_episode are handled independently per player
        if player.round_number > 1:
            # Retrieve the current episode from the last round or initialize if it's the first period
            player.current_episode = player.in_round(player.round_number - 1).current_episode or 1

        # Set the max period in the episode based on the predefined dictionary
        set_Max_period(player)

        # Retrieve and increment period_in_episode if it's not the first period
        if player.round_number > 1:
            previous_period = player.in_round(player.round_number - 1).period_in_episode or 1
            player.period_in_episode = previous_period + 1 if not player.accepted else previous_period
        else:
            player.period_in_episode = 1  # Initialize for the first round

        # Ensure period progression and wage acceptance check are individual to the player
        if player.period_in_episode > 1:
            player.reservation_wage = player.participant.vars.get("Reservation")

        set_wage_offer(player)  # Generate a wage offer individually for each player
        wage_offer = player.field_maybe_none('wage_offer') or 'No offer'
        set_earnings(player)  # Set earnings individually based on the player's wage offer and acceptance

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

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'search_episode_number': player.current_episode,  # Pass the current episode number
            'period_number': player.period_in_episode,       # Pass the period number if needed
            'earnings': player.earnings                       # Pass earnings to the template
        }

    def before_next_page(player: Player, timeout_happened=False):
        player.participant.vars["New_episode"] = True

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.current_episode == C.MAX_EPISODE:
            return upcoming_apps[0]



page_sequence = [WaitForPartner, Chat, SetReservationWage, Searching, Results]
