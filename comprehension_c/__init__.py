from otree.api import *

c = cu

class C(BaseConstants):
    NAME_IN_URL = 'comprehension_quiz_c'
    PLAYERS_PER_GROUP = None
    ECU_LABEL = 'ECUs'
    NUM_ROUNDS = 1

    QUIZ_FIELDS = [f'quiz_{n}' for n in range(1, 7)]
    QUIZ_LABELS = [
        "Each search episode will last 20 periods.",
        "A wage offer will be made every period.",
        "You will be paid for one randomly selected search episode.",
        "If you receive a wage offer that is above the lowest wage you state, then your wage will equal the lowest amount you stated.",
        'You will have the same partner throughout the the study who you can chat with.',
        'You will not share your earnings with your partner.',
    ]

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    quiz_1 = models.BooleanField()
    quiz_1_wrong_attempts = models.IntegerField(initial=0)

    quiz_2 = models.BooleanField()
    quiz_2_wrong_attempts = models.IntegerField(initial=0)

    quiz_3 = models.BooleanField()
    quiz_3_wrong_attempts = models.IntegerField(initial=0)

    quiz_4 = models.BooleanField()
    quiz_4_wrong_attempts = models.IntegerField(initial=0)

    quiz_5 = models.BooleanField(blank=True)
    quiz_5_wrong_attempts = models.IntegerField(initial=0)

    quiz_6 = models.BooleanField(blank=True)
    quiz_6_wrong_attempts = models.IntegerField(initial=0)

# PAGES
class Comprehension(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        # Return list of fields for the form
        return C.QUIZ_FIELDS[:]

    @staticmethod
    def vars_for_template(player: Player):
        # Prepare fields with labels for the HTML template
        fields = list(zip(C.QUIZ_FIELDS, C.QUIZ_LABELS))
        return dict(fields=fields)

    @staticmethod
    def error_message(player: Player, values):
        solutions = dict(
            quiz_1=(False, 'The number of periods in a search episode is determined randomly.'),
            quiz_2=(False, 'There is a 50% chance that a wage offer will be made in any period.'),
            quiz_3=(True, 'Only one of the 20 search episodes will be used to determine your payment.'),
            quiz_4=(False, 'Your wage will equal to the wage offer as long as that wage offer is at least as large as the lowest wage offer you stated.'),
            quiz_5=(True, 'You will have the same partner throughout the study who you can chat with.'),
            quiz_6=(True, 'You will not share your earnings with your partner.'),
        )

        # Only check fields that are part of `form_fields`
        error_msgs = {
            k: solutions[k][1] for k, v in values.items() if v != solutions[k][0] and k in values
        }

        # Increment wrong attempt counters only for the fields in `form_fields`
        for k in error_msgs.keys():
            num = getattr(player, f'{k}_wrong_attempts')
            setattr(player, f'{k}_wrong_attempts', num + 1)

        return error_msgs

class EndComprehension(Page):
    pass

class Instructions(Page):
    pass

page_sequence = [
    Instructions, Comprehension, EndComprehension
]
