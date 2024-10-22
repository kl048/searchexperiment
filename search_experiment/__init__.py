import random
from otree.api import *

doc = """
Comparing Single Search and Joint Search
Basic Job Search
- Subject starts with an endowment (outside option) of 20 ECUs
- Subject sets reservation wage r 
- Each period an unemployed subject receives an offer with probability 0.50
- Wage offer, w, drawn from U[1,100]
- If w >= r subject becomes employed
- If subject is employed when search episode ends then earn w, otherwise earn 0 (in addition to the endowment)
Three Treatments: Individual, Chat, Team
"""


class C(BaseConstants):
    NAME_IN_URL = 'search_experiment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 93  # Define the number of episodes as rounds
    ENDOWMENT = cu(20)
    ALPHA = 0.5
    THETA = 100
    CHAT_DURATION_LONG = 60
    CHAT_DURATION_SHORT = 30
    EXCHANGE_RATE = 1
    SHOW_UP_FEE = 7
    ECU_LABEL = 'ECUs'
    PAYMENT_PER_CORRECT_ANSWER = 0.50


class Subsession(BaseSubsession):
    block = models.IntegerField()
    round_in_block = models.IntegerField()


def creating_session(subsession: Subsession):
    subsessions = subsession.in_all_rounds()
    for subsession in subsessions:
        current_round = subsession.round_number
        if current_round <= 5:
            subsession.block = 1
            subsession.round_in_block = current_round
        elif current_round <= 12:
            subsession.block = 2
            subsession.round_in_block = current_round - 5
        elif current_round <= 16:
            subsession.block = 3
            subsession.round_in_block = current_round - 12
        elif current_round <= 22:
            subsession.block = 4
            subsession.round_in_block = current_round - 16
        elif current_round <= 29:
            subsession.block = 5
            subsession.round_in_block = current_round - 22
        elif current_round <= 34:
            subsession.block = 6
            subsession.round_in_block = current_round - 29
        elif current_round <= 37:
            subsession.block = 7
            subsession.round_in_block = current_round - 34
        elif current_round <= 43:
            subsession.block = 8
            subsession.round_in_block = current_round - 37
        elif current_round <= 47:
            subsession.block = 9
            subsession.round_in_block = current_round - 43
        elif current_round <= 52:
            subsession.block = 10
            subsession.round_in_block = current_round - 47
        elif current_round <= 57:
            subsession.block = 11
            subsession.round_in_block = current_round - 52
        elif current_round <= 63:
            subsession.block = 12
            subsession.round_in_block = current_round - 57
        elif current_round <= 67:
            subsession.block = 13
            subsession.round_in_block = current_round - 63
        elif current_round <= 72:
            subsession.block = 14
            subsession.round_in_block = current_round - 67
        elif current_round <= 76:
            subsession.block = 15
            subsession.round_in_block = current_round - 72
        elif current_round <= 80:
            subsession.block = 16
            subsession.round_in_block = current_round - 76
        elif current_round <= 85:
            subsession.block = 17
            subsession.round_in_block = current_round - 80
        elif current_round <= 89:
            subsession.block = 18
            subsession.round_in_block = current_round - 85
        elif current_round <= 93:
            subsession.block = 19
            subsession.round_in_block = current_round - 89
        else:
            subsession.block = 20
            subsession.round_in_block = current_round - 93

    for player in subsession.get_players():
        player.current_episode = subsession.block
        player.period_in_episode = subsession.round_in_block
        player.treatment = subsession.session.config['treatment']
        player.endowment = C.ENDOWMENT
        player.is_employed = False
        player.round_payoff = 0


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment = models.StringField()
    reservation_wage = models.IntegerField(
        min=0,
        max=C.THETA,
        label="Set your reservation wage",
        initial=0
    )
    wage_offer = models.IntegerField(blank=True)
    accepted = models.BooleanField(initial=False)
    earnings = models.CurrencyField(initial=0)
    is_employed = models.BooleanField(initial=False)
    round_payoff = models.CurrencyField(initial=0)
    total_earnings = models.CurrencyField(initial=0)
    num_correct_answers = models.IntegerField(initial=0)
    payment_for_correct_answers = models.CurrencyField(initial=0)
    total_earnings_with_crt = models.CurrencyField(initial=0)
    chat_content = models.LongStringField(blank=True)
    endowment = models.CurrencyField(initial=C.ENDOWMENT)
    current_episode = models.IntegerField()
    period_in_episode = models.IntegerField()


def set_wage_offer(player: Player):
    if random.random() < C.ALPHA:  # 50% chance to make a wage offer
        player.wage_offer = random.randint(1, C.THETA)  # Draw wage from U[1,100]
        print(f"Wage offer in period {player.period_in_episode}: {player.wage_offer}")
    else:
        player.wage_offer = None  # No offer
        print(f"No wage offer in period {player.period_in_episode}")


def set_earnings(player: Player):
    if player.field_maybe_none('wage_offer') is not None and player.wage_offer >= player.reservation_wage:
        player.accepted = True
        player.is_employed = True
        player.earnings = player.wage_offer
    else:
        player.accepted = False
        if player.period_in_episode == player.subsession.round_in_block:
            # Only set earnings to 20 ECUs at the end of the episode
            player.earnings = C.ENDOWMENT
        else:
            player.earnings = 0  # Earnings remain 0 until the last period


def get_chat_duration(player: Player):
    return C.CHAT_DURATION_LONG if player.round_number < 5 else C.CHAT_DURATION_SHORT


def set_total_earnings(player: Player):
    selected_round = random.randint(1, C.NUM_ROUNDS)
    selected_round_payoff = player.in_round(selected_round).round_payoff
    player.total_earnings = selected_round_payoff * C.EXCHANGE_RATE + C.SHOW_UP_FEE


def calculate_crt_earnings(player: Player, values):
    solutions = {
        'quiz1': 5,
        'quiz2': 5,
        'quiz3': 47,
        'quiz4': 9,
        'quiz5': 12,
        'quiz6': 14,
        'quiz7': 1,
    }

    correct_answers = 0
    for field_name, correct_value in solutions.items():
        if values[field_name] == correct_value:
            correct_answers += 1
        else:
            setattr(player, f'{field_name}_wrong', getattr(player, f'{field_name}_wrong') + 1)

    player.num_correct_answers = correct_answers
    player.payment_for_correct_answers = correct_answers * C.PAYMENT_PER_CORRECT_ANSWER
    total_earnings = player.participant.vars.get('total_earnings', 0)
    player.total_earnings_with_crt = player.payment_for_correct_answers + total_earnings


def end_period(player: Player):
    print(f"Before End Period: Episode {player.current_episode}, Period {player.period_in_episode}, Employed: {player.is_employed}")

    if player.accepted:
        # If the wage is accepted, the episode ends immediately, and we move to the next episode
        player.current_episode += 1
        player.period_in_episode = 1  # Reset period for the new episode
        print(f"Accepted wage, moving to new Episode: {player.current_episode}, Reset Period: {player.period_in_episode}")
    else:
        # Increment period only if the wage was not accepted
        if player.period_in_episode < player.subsession.round_in_block:
            player.period_in_episode += 1
        else:
            player.earnings = C.ENDOWMENT  # Outside option if no wage accepted by the last period
            player.current_episode += 1
            player.period_in_episode = 1  # Reset period for the new episode
            print(f"New Episode: {player.current_episode}, Reset Period: {player.period_in_episode}")

    print(f"End of Period: Episode {player.current_episode}, Period {player.period_in_episode}")


# Pages
class SetReservationWage(Page):
    form_model = 'player'
    form_fields = ['reservation_wage']

    @staticmethod
    def is_displayed(player: Player):
        return player.period_in_episode == 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):
        player.participant.vars[f'reservation_wage_episode_{player.current_episode}'] = player.reservation_wage

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'search_episode_number': player.current_episode,
            'endowment': C.ENDOWMENT,
            'ecus': C.ECU_LABEL,
        }


class WaitForAllPlayers(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.treatment in ['C', 'T']

    wait_for_all_groups = True


class WageOffer(Page):
    form_model = 'player'

    @staticmethod
    def vars_for_template(player: Player):
        set_wage_offer(player)

        return {
            'search_episode_number': player.current_episode,
            'period_number': player.period_in_episode,
            'wage_offer': player.field_maybe_none('wage_offer'),
            'accepted': player.accepted,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):
        if player.period_in_episode > 1:
            player.reservation_wage = player.participant.vars.get(f'reservation_wage_episode_{player.current_episode}',
                                                                  player.reservation_wage)
        set_earnings(player)
        # Now we call the end_period function to handle the episode/period transition.
        end_period(player)


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        # Correct the episode and period logic
        reservation_wage = player.participant.vars.get(f'reservation_wage_episode_{player.current_episode}', player.reservation_wage)
        wage_offer = player.field_maybe_none('wage_offer') or 'No offer'

        # Earnings should not be updated until the round is finished
        earnings = player.earnings if player.accepted or player.period_in_episode == player.subsession.round_in_block else None

        return {
            'search_episode_number': player.current_episode,  # Correct the display of the current episode
            'period_number': player.period_in_episode,
            'reservation_wage': reservation_wage,
            'wage_offer': wage_offer,
            'accepted': player.accepted,
            'earnings': earnings,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):
        # Call end_period to ensure the correct transition
        end_period(player)


class TeamResults(Page):
    @staticmethod
    def vars_for_template(player: Player):
        team_earnings = sum([p.earnings for p in player.group.get_players()]) / 2
        return {
            'search_episode_number': player.current_episode,
            'period_number': player.period_in_episode,
            'team_earnings': team_earnings
        }

    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == 'T'


class CRTQuestions(Page):
    form_model = 'player'
    form_fields = ['quiz1', 'quiz2', 'quiz3', 'quiz4', 'quiz5', 'quiz6', 'quiz7']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        calculate_crt_earnings(player, player.__dict__)


class FinalEarnings(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        set_total_earnings(player)
        player.participant.vars['total_earnings'] = player.total_earnings
        total_earnings_with_crt = player.total_earnings_with_crt + C.SHOW_UP_FEE
        return {
            'total_earnings_with_crt': total_earnings_with_crt,
            'total_payoff_in_dollars': total_earnings_with_crt * C.EXCHANGE_RATE,
            'show_up_fee': C.SHOW_UP_FEE,
            'conversion_rate': C.EXCHANGE_RATE,
        }


page_sequence = [
    SetReservationWage,
    WaitForAllPlayers,
    WageOffer,
    Results,
    TeamResults,
    CRTQuestions,
    FinalEarnings
]
