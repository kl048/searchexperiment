from otree.api import *

c = cu

class C(BaseConstants):
    NAME_IN_URL = 'comprehension_quiz'
    PLAYERS_PER_GROUP = None
    ECU_LABEL = 'ECUs'
    NUM_ROUNDS = 1

    # Removed quiz_6 → now 7 questions total
    QUIZ_FIELDS = [f'quiz_{n}' for n in range(1, 8)]
    QUIZ_LABELS = [
        "Each job search will last 20 periods.",
        "A wage offer will be made every period.",
        "You will be paid for one randomly selected job search.",
        "If you receive a wage offer that is above the lowest wage you state, then your wage will equal the lowest amount you stated.",
        "The length of a job search is:",
        # REMOVED: "If a period begins and you have not already accepted a wage offer, there is:",
        "At the end of the study you will be paid for:",
        "If you receive a wage offer that is above the reservation wage you set, then your wage will equal:",
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

    quiz_5 = models.StringField(
        choices=[("a", "Exactly 20 periods."), ("b", "Uncertain. There is always a 90% chance a job search will continue for another period"),
                 ("c", " Uncertain. There is always a 50% chance a job search will continue for another period.")],
        widget=widgets.RadioSelect)
    quiz_5_wrong_attempts = models.IntegerField(initial=0)

    # REMOVED quiz_6

    quiz_6 = models.StringField(
        choices=[("a", "The one job search you will complete."), ("b", "One of the twenty job searches you will complete selected at random."),
                 ("c", "All twenty of the job searches you will complete."), ("d", "The one job search out of the twenty you will complete where you earned the most.")],
        widget=widgets.RadioSelect)
    quiz_6_wrong_attempts = models.IntegerField(initial=0)

    quiz_7 = models.StringField(
        choices=[("a", "10 because you would not accept the wage offer."), ("b", "Your reservation wage."), ("c", "The wage you are offered.")],
        widget=widgets.RadioSelect)
    quiz_7_wrong_attempts = models.IntegerField(initial=0)

class Comprehension(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        return C.QUIZ_FIELDS[:]

    @staticmethod
    def vars_for_template(player: Player):
        fields = list(zip(C.QUIZ_FIELDS, C.QUIZ_LABELS))
        return dict(fields=fields)

    @staticmethod
    def error_message(player: Player, values):
        solutions = dict(
            quiz_1=(False, "The number of periods in a job search is uncertain."),
            quiz_2=(True, "A wage offer will be made every period. "),
            quiz_3=(True, "You will be paid based on one randomly selected job search."),
            quiz_4=(False, "If you receive a wage offer that is above your stated lowest acceptable wage, your wage will equal the wage offer."),
            quiz_5=("b", "The number of periods in a job search is uncertain. There is always a 90% chance a job search will continue for another period. "),
            # REMOVED quiz_6
            quiz_6=("b", "Only one of the 20 job search will be selected randomly to determine your payment."),
            quiz_7=("c", "Your wage will equal the wage offer if the offer is at least as large as the lowest wage you stated."),
        )

        error_msgs = {}
        for k, v in values.items():
            if v != solutions[k][0]:
                error_msgs[k] = f"Incorrect. {solutions[k][1]}"
                wrong_attempts_field = f"{k}_wrong_attempts"
                if hasattr(player, wrong_attempts_field):
                    num = getattr(player, wrong_attempts_field, 0)
                    setattr(player, wrong_attempts_field, num + 1)

        return error_msgs if error_msgs else None

class EndComprehension(Page):
    pass

class Instructions(Page):
    pass

class VideoIntro(Page):
    def is_displayed(self):
        return self.round_number == 1

class Video1(Page):
    def is_displayed(self):
        return self.round_number == 1

class Video2(Page):
    def is_displayed(self):
        return self.round_number == 1

class Video3(Page):
    def is_displayed(self):
        return self.round_number == 1

class Video4(Page):
    def is_displayed(self):
        return self.round_number == 1

class Video56(Page):
    def is_displayed(self):
        return self.round_number == 1

class Video78(Page):
    def is_displayed(self):
        return self.round_number == 1

page_sequence = [
    Instructions, VideoIntro, Video1, Video2, Video3, Video4, Video56, Video78, Comprehension, EndComprehension
]
