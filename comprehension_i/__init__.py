from otree.api import *

c = cu

class C(BaseConstants):
    NAME_IN_URL = 'comprehension_quiz'
    PLAYERS_PER_GROUP = None
    ECU_LABEL = 'ECUs'
    NUM_ROUNDS = 1

    # Define four quiz questions
    QUIZ_FIELDS = [f'quiz_{n}' for n in range(1, 9)]
    QUIZ_LABELS = [
        "Each search episode will last 20 periods.",
        "A wage offer will be made every period.",
        "You will be paid for one randomly selected search episode.",
        "If you receive a wage offer that is above the lowest wage you state, then your wage will equal the lowest amount you stated.",  # ✅ Fixed missing comma
        "The length of a job search is:",
        "If a period begins and you have not already accepted a wage offer, there is:",
        "At the end of the study you will be paid for:",
        "If you receive a wage offer that is above the reservation wage you set, then your wage will equal:",
    ]

class Subsession(BaseSubsession):
    pass  # ✅ Removed unnecessary `creating_session()` function

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    # Define fields for four quiz questions with wrong attempt counters
    quiz_1 = models.BooleanField()
    quiz_1_wrong_attempts = models.IntegerField(initial=0)

    quiz_2 = models.BooleanField()
    quiz_2_wrong_attempts = models.IntegerField(initial=0)

    quiz_3 = models.BooleanField()
    quiz_3_wrong_attempts = models.IntegerField(initial=0)

    quiz_4 = models.BooleanField()
    quiz_4_wrong_attempts = models.IntegerField(initial=0)

    # Multiple Choice Questions (Radio Select)
    quiz_5 = models.StringField(
        choices=[("a", "Exactly 20 periods."), ("b", "Uncertain."), ("c", "There is always a 95% chance a job search will continue for another period.")],
        widget=widgets.RadioSelect)
    quiz_5_wrong_attempts = models.IntegerField(initial=0)

    quiz_6 = models.StringField(
        choices=[("a", "A 25% chance a wage offer will be made."), ("b", "A 50% chance a wage offer will be made."), ("c", "A 100% chance a wage offer will be made.")],
        widget=widgets.RadioSelect)
    quiz_6_wrong_attempts = models.IntegerField(initial=0)

    quiz_7 = models.StringField(
        choices=[("a", "The one job search you will complete."), ("b", "One of the twenty job searches you will complete selected at random."),
                 ("c", "All twenty of the job searches you will complete."), ("d", "The one job search out of the twenty you will complete where you earned the most.")],
        widget=widgets.RadioSelect)
    quiz_7_wrong_attempts = models.IntegerField(initial=0)

    quiz_8 = models.StringField(
        choices=[("a", "20 because you would not accept the wage offer."), ("b", "Your reservation wage."), ("c", "The wage you are offered.")],
        widget=widgets.RadioSelect)
    quiz_8_wrong_attempts = models.IntegerField(initial=0)

# Pages
class Comprehension(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        return C.QUIZ_FIELDS[:]  # Ensures all quiz fields are displayed

    @staticmethod
    def vars_for_template(player: Player):
        fields = list(zip(C.QUIZ_FIELDS, C.QUIZ_LABELS))
        return dict(fields=fields)

    @staticmethod
    def error_message(player: Player, values):
        solutions = dict(
            quiz_1=(False, "The number of periods in a search episode is uncertain ."),
            quiz_2=(False, "There is a 50% chance that there will be a wage offered in each period."),  # Fixed
            quiz_3=(True, "You will be paid based on one randomly selected search episode."),
            quiz_4=(False, "If you receive a wage offer that is above your stated lowest acceptable wage, your wage will equal the wage offer."),  # ✅ Fixed
            quiz_5=("b", "The number of periods in a search episode is uncertain."),
            quiz_6=("b", "There is a 50% chance that a wage offer will be made in any period."),
            quiz_7=("b", "Only one of the 20 search episodes will be selected randomly to determine your payment."),
            quiz_8=("c", "Your wage will equal the wage offer if the offer is at least as large as the lowest wage you stated."),
        )

        error_msgs = {}
        for k, v in values.items():
            if v != solutions[k][0]:  # If the answer is incorrect
                error_msgs[k] = f"Incorrect. {solutions[k][1]}"

                #  Fix: Use `getattr()` with a default value to prevent `None` errors
                wrong_attempts_field = f"{k}_wrong_attempts"
                if hasattr(player, wrong_attempts_field):
                    num = getattr(player, wrong_attempts_field, 0)  #  If None, default to 0
                    setattr(player, wrong_attempts_field, num + 1)

        return error_msgs if error_msgs else None  #  Return error messages only if incorrect answers exist


class EndComprehension(Page):
    pass

class Instructions(Page):
    pass

page_sequence = [
    Instructions, Comprehension, EndComprehension
]
