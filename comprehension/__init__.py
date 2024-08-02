from otree.api import *

c = cu

class C(BaseConstants):
    NAME_IN_URL = 'focal_instructions'
    PLAYERS_PER_GROUP = None
    ECU_LABEL = 'ECUs'
    NUM_ROUNDS = 1

    QUIZ_FIELDS = [f'quiz_{n}' for n in range(1, 5)]
    QUIZ_LABELS = [
        "Each search episode will last 20 periods.",
        "A wage offer will be made every period.",
        "You will be paid for one randomly selected search episode.",
        "If you receive a wage offer that is above the lowest wage you state, then your wage will equal the lowest amount you stated."
    ]
    TREATMENT_QUESTIONS = {
        'T': [
            'Question for treatment T only',
            'Question for both T and C treatments'
        ],
        'C': [
            'Question for both T and C treatments'
        ]
    }

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

    treatment_quiz_1 = models.BooleanField(blank=True)
    treatment_quiz_1_wrong_attempts = models.IntegerField(initial=0)

    treatment_quiz_2 = models.BooleanField(blank=True)
    treatment_quiz_2_wrong_attempts = models.IntegerField(initial=0)

# PAGES
class Comprehension(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        fields = C.QUIZ_FIELDS[:]
        if player.session.config['treatment'] in C.TREATMENT_QUESTIONS:
            fields += ['treatment_quiz_1', 'treatment_quiz_2']
        return fields

    @staticmethod
    def vars_for_template(player: Player):
        labels = C.QUIZ_LABELS
        treatment_labels = []

        if player.session.config['treatment'] in C.TREATMENT_QUESTIONS:
            treatment_labels = C.TREATMENT_QUESTIONS[player.session.config['treatment']]

        return dict(
            fields=list(zip(C.QUIZ_FIELDS + ['treatment_quiz_1', 'treatment_quiz_2'], labels + treatment_labels))
        )

    @staticmethod
    def error_message(player: Player, values):
        solutions = dict(
            quiz_1=(False, 'The number of periods in a search episode is determined randomly.'),
            quiz_2=(False, 'There is a 50% chance that a wage offer will be made in any period.'),
            quiz_3=(True, 'Only one of the 20 search episodes will be used to determine your payment.'),
            quiz_4=(False, 'Your wage will equal to the wage offer as long as that wage offer is at least as large as the lowest wage offer you stated.'),
            treatment_quiz_1=(False, 'Feedback for treatment-specific question 1.'),
            treatment_quiz_2=(False, 'Feedback for treatment-specific question 2.'),
        )

        error_msgs = {
            k: solutions[k][1] for k, v in values.items() if v != solutions[k][0]
            if k in values
        }

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
