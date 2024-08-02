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
- If subject is employed when game ends then earn w, otherwise earn 0 (in addition to the endowment)
- Another period occurs with probability 0.95
Three Treatments: Individual, Chat, Team
"""

class C(BaseConstants):
    NAME_IN_URL = 'search_experiment'
    PLAYERS_PER_GROUP = None  # Dynamic definition
    NUM_ROUNDS = 20
    ENDOWMENT = cu(20)
    ALPHA = 0.5
    THETA = 100
    DELTA = 0.95
    CHAT_DURATION_LONG = 60
    CHAT_DURATION_SHORT = 30
    EXCHANGE_RATE = 0.1
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

    quiz1 = models.IntegerField(label='A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost (in cents)?')
    quiz1_wrong = models.IntegerField(initial=0)

    quiz2 = models.IntegerField(
        label='If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets?')
    quiz2_wrong = models.IntegerField(initial=0)

    quiz3 = models.IntegerField(label='In a lake, there is a patch of lily pads. Every day, the patch doubles in size. If it takes 48 days for the patch to cover the entire lake, how long would it take for the patch to cover half the lake?')
    quiz3_wrong = models.IntegerField(initial=0)

    quiz4 = models.IntegerField(label='A box of staples has a length of 6 cm, a width of 7 cm, and a volume of 378 cm cubed. What is the height of the box?')
    quiz4_wrong = models.IntegerField(initial=0)

    quiz5 = models.IntegerField(label='A basketball player averaged 20 points a game over the course of six games. His scores in five of those games were 23, 18, 16, 24, and 27. How many points did he score in the sixth game?')
    quiz5_wrong = models.IntegerField(initial=0)

    quiz6 = models.IntegerField(label='A physical education class has three times as many girls as boys. During a class basketball game, the girls average 18 points each, and the class as a whole averages 17 points per person. How many points does each boy score on average?')
    quiz6_wrong = models.IntegerField(initial=0)

    quiz7 = models.IntegerField(label='Please enter your label (the number assigned to you).')
    quiz7_wrong = models.IntegerField(initial=0)

def set_wage_offer(player: Player):
    if random.random() < C.ALPHA:
        player.wage_offer = random.randint(1, C.THETA)
    else:
        player.wage_offer = None

def set_earnings(player: Player):
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
    player.total_earnings_with_crt = player.payment_for_correct_answers + player.total_earnings

# Pages

class SetReservationWage(Page):
    form_model = 'player'
    form_fields = ['reservation_wage']

    @staticmethod
    def vars_for_template(player: Player):
        treatment = player.field_maybe_none('treatment')
        return {
            'round_number': player.round_number,
            'endowment': C.ENDOWMENT,
            'ecus': C.ECU_LABEL,
            'chat_group': f'chat_{player.group.id}' if treatment in ['C', 'T'] else None
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):
        set_wage_offer(player)
        set_earnings(player)

class WaitForAllPlayers(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.treatment in ['C', 'T']

    wait_for_all_groups = True

class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'reservation_wage': player.reservation_wage,
            'wage_offer': player.wage_offer if player.field_maybe_none('wage_offer') is not None else 'No offer',
            'accepted': player.accepted,
            'earnings': player.earnings
        }

class TeamResults(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'team_earnings': sum([p.earnings for p in player.group.get_players()]) / 2
        }

    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == 'T'

class CRTQuestions(Page):
    form_model = 'player'
    form_fields = ['quiz1', 'quiz2', 'quiz3', 'quiz4', 'quiz5', 'quiz6', 'quiz7']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        calculate_crt_earnings(player, player.__dict__)

class FinalEarnings(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'total_earnings_with_crt': player.total_earnings_with_crt,
            'show_up_fee': C.SHOW_UP_FEE,
            'conversion_rate': C.EXCHANGE_RATE,
        }

page_sequence = [
    SetReservationWage,
    WaitForAllPlayers,  # Ensure all players wait here to synchronize for Chat and Team treatments
    Results,
    TeamResults,
    CRTQuestions,
    FinalEarnings
]
