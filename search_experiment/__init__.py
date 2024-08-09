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
    PLAYERS_PER_GROUP = None  # Dynamic definition
    NUM_SEARCH_EPISODES = 20
    NUM_ROUNDS = NUM_SEARCH_EPISODES  # Define the number of rounds
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
    pass


def creating_session(subsession: Subsession):
    session = subsession.session
    players_per_group = session.config['players_per_group']
    num_participants = session.num_participants

    if num_participants % players_per_group != 0:
        raise ValueError('Number of participants must be a multiple of players_per_group')

    players = subsession.get_players()
    group_matrix = [players[i:i + players_per_group] for i in range(0, len(players), players_per_group)]

    subsession.set_group_matrix(group_matrix)
    for player in players:
        player.treatment = session.config['treatment']
        player.endowment = C.ENDOWMENT
        player.is_employed = False
        player.round_payoff = 0
        player.current_episode = 1  # Ensure episodes start from 1
        player.current_period = 1  # Ensure periods start from 1
        player.max_periods = get_max_periods(1)  # Initialize with the max periods for the first episode


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment = models.StringField()
    reservation_wage = models.IntegerField(
        min=0,
        max=C.THETA,
        label="Set your reservation wage"
    )
    wage_offer = models.IntegerField(blank=True)
    accepted = models.BooleanField(initial=False)
    earnings = models.CurrencyField()
    is_employed = models.BooleanField(initial=False)
    round_payoff = models.CurrencyField()
    total_earnings = models.CurrencyField()
    num_correct_answers = models.IntegerField(initial=0)
    payment_for_correct_answers = models.CurrencyField(initial=0)
    total_earnings_with_crt = models.CurrencyField(initial=0)
    chat_content = models.LongStringField(blank=True)
    endowment = models.CurrencyField(initial=C.ENDOWMENT)
    current_episode = models.IntegerField(initial=1)
    current_period = models.IntegerField(initial=1)
    max_periods = models.IntegerField(initial=3)

    quiz1 = models.IntegerField(
        label='A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost (in cents)?')
    quiz1_wrong = models.IntegerField(initial=0)

    quiz2 = models.IntegerField(
        label='If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets?')
    quiz2_wrong = models.IntegerField(initial=0)

    quiz3 = models.IntegerField(
        label='In a lake, there is a patch of lily pads. Every day, the patch doubles in size. If it takes 48 days for the patch to cover the entire lake, how long would it take for the patch to cover half the lake?')
    quiz3_wrong = models.IntegerField(initial=0)

    quiz4 = models.IntegerField(
        label='A box of staples has a length of 6 cm, a width of 7 cm, and a volume of 378 cm cubed. What is the height of the box?')
    quiz4_wrong = models.IntegerField(initial=0)

    quiz5 = models.IntegerField(
        label='A basketball player averaged 20 points a game over the course of six games. His scores in five of those games were 23, 18, 16, 24, and 27. How many points did he score in the sixth game?')
    quiz5_wrong = models.IntegerField(initial=0)

    quiz6 = models.IntegerField(
        label='A physical education class has three times as many girls as boys. During a class basketball game, the girls average 18 points each, and the class as a whole averages 17 points per person. How many points does each boy score on average?')
    quiz6_wrong = models.IntegerField(initial=0)

    quiz7 = models.IntegerField(label='Please enter your label (the number assigned to you).')
    quiz7_wrong = models.IntegerField(initial=0)


def get_max_periods(episode):
    if episode in [1, 5, 8, 11]:
        return 5
    elif episode in [2, 6, 9, 12]:
        return 7
    elif episode in [3, 7, 10, 13]:
        return 4
    elif episode in [4, 16, 19, 20]:
        return 6
    else:
        return 3


def set_wage_offer(player: Player):
    if random.random() < C.ALPHA:
        player.wage_offer = random.randint(1, C.THETA)
    else:
        player.wage_offer = None
    print("end of set wage")


def set_earnings(player: Player):
    print("set earning")
    if player.field_maybe_none('wage_offer') is not None and player.wage_offer >= player.reservation_wage:
        player.accepted = True
        player.is_employed = True
        player.earnings = player.wage_offer
    else:
        player.accepted = False
        player.earnings = 0
    player.round_payoff = player.earnings + C.ENDOWMENT


def get_chat_duration(player: Player):
    return C.CHAT_DURATION_LONG if player.round_number < 5 else C.CHAT_DURATION_SHORT


def set_total_earnings(player: Player):
    selected_round = random.randint(1, C.NUM_SEARCH_EPISODES)
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
    print(
        f"Before End Period: Episode {player.current_episode}, Period {player.current_period}, Employed: {player.is_employed}")
    if player.current_period <= player.max_periods:
        player.earnings = player.earnings if player.max_periods else C.ENDOWMENT
        player.max_periods = get_max_periods(player.current_episode)
        print(f"New Episode: {player.current_episode}, Max Periods: {player.max_periods}")

    elif player.current_period >= player.max_periods or not player.is_employed:
        player.current_episode += 1
    elif player.is_employed:
        player.current_episode += 1
        print(f"Next Period: {player.current_period}")


# Pages
class SetReservationWage(Page):
    form_model = 'player'
    form_fields = ['reservation_wage']

    @staticmethod
    def is_displayed(player: Player):
        # Show this page only at the beginning of each search episode
        return player.current_period == 1

    @staticmethod
    def vars_for_template(player: Player):
        treatment = player.field_maybe_none('treatment')
        chat_duration = get_chat_duration(player)
        return {
            'search_episode_number': player.current_episode,
            'endowment': C.ENDOWMENT,
            'ecus': C.ECU_LABEL,
            'chat_group': f'chat_{player.group.id}' if treatment in ['C', 'T'] else None,
            'chat_duration': chat_duration
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):
        set_wage_offer(player)


class WaitForAllPlayers(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.treatment in ['C', 'T']

    wait_for_all_groups = True


class WageOffer(Page):
    form_model = 'player'

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'search_episode_number': player.current_episode,
            'period_number': player.current_period,
            'wage_offer': player.wage_offer if player.field_maybe_none('wage_offer') is not None else 'No offer',
            'accepted': player.accepted,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):
        set_earnings(player)
        end_period(player)
        set_wage_offer(player)
        print("after end period")




class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'search_episode_number': player.current_episode,
            'period_number': player.current_period,
            'reservation_wage': player.reservation_wage,
            'wage_offer': player.earnings if player.field_maybe_none('earnings') is not None else 'No offer',
            'accepted': player.accepted,
            'earnings': player.earnings
        }

    @staticmethod
    def is_displayed(player: Player):
        # Show results at the end of each period or when an episode ends
        return True

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        pass


class TeamResults(Page):
    @staticmethod
    def vars_for_template(player: Player):
        team_earnings = sum([p.field_maybe_none('earnings') or 0 for p in player.group.get_players()]) / 2
        return {
            'search_episode_number': player.current_episode - 1,
            'period_number': player.current_period,
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
        return player.round_number == C.NUM_SEARCH_EPISODES

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        calculate_crt_earnings(player, player.__dict__)


class FinalEarnings(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_SEARCH_EPISODES

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
    WaitForAllPlayers,  # Ensure all players wait here to synchronize for Chat and Team treatments
    WageOffer,
    Results,
    TeamResults,
    CRTQuestions,
    FinalEarnings
]
