from otree.api import *

c = cu


class C(BaseConstants):
    NAME_IN_URL = 'crt'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    REWARD_PER_CORRECT_ANSWER = 0.20  # 20 cents per correct answer


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    num_failed_attempts = models.IntegerField(initial=0)
    failed_too_many = models.BooleanField(initial=False)

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

    quiz7 = models.FloatField(
        label="Suppose you flip a fair coin, meaning that the probability of heads is 0.5 and the probability of tails is 0.5. Suppose you flip the coin twice. If the first time that you flip the coin it comes up heads, "
              "what is the probability that it will be heads on the second flip? <b> (Enter as a decimal.) </b>",
        min=0, max=1
    )
    quiz7_wrong = models.IntegerField(initial=0)

    quiz8 = models.FloatField(
        label=" Suppose that the probability that Ken shows up to work in a green shirt on any given day is 0.3 and that the probability that Jill shows up to work in a green shirt on any given day is 0.4. "
              "Assuming that Ken and Jill do not coordinate the shirts that they wear to work on any given day, what is the probability of both Ken and Jill showing up to work in green shirts on the same day? <b> (Enter as a decimal.) </b>",
        min=0, max=1
    )
    quiz8_wrong = models.IntegerField(initial=0)

    quiz9 = models.FloatField(
        label="Suppose that the probability that a pregnant pig gives birth to one pig is 0.2 and the probability that she gives birth to two pigs is 0.8. "
              "The expected number of pigs that the pregnant pig will give birth to is What is the expected number of piglets? <b> (Enter as a decimal.) </b>",
        min=0, max=2
    )
    quiz9_wrong = models.IntegerField(initial=0)

    quiz10 = models.FloatField(
        label="Suppose that the probability of rain tomorrow is 0.3.  On days when it rains, the probability of 1 inch of rainfall is 0.5, the probability of 2 inches of rainfall is 0.3, "
              "and the probability of 3 inches of rainfall is 0.2. The expected amount of rainfall tomorrow is. What is the expected rainfall? <b> (Enter as a decimal.) </b>",
        min=0, max=2
    )
    quiz10_wrong = models.IntegerField(initial=0)
    def calculate_crt_payoff(self):
        # Define correct answers
        solutions = {
            'quiz1': 5,
            'quiz2': 5,
            'quiz3': 47,
            'quiz4': 9,
            'quiz5': 12,
            'quiz6': 14,
            'quiz7': 0.5,
            'quiz8': 0.12,  # 0.3 * 0.4
            'quiz9': 1.8,  # (0.2 * 1) + (0.8 * 2)
            'quiz10': 1.3,  # 0.3 * (0.5*1 + 0.3*2 + 0.2*3)
        }

        # Count correct answers
        correct_count = sum(
            1 for quiz, answer in solutions.items() if getattr(self, quiz) == answer
        )

        # Add a fixed 20 cents per correct answer directly to player.payoff
        crt_earnings = correct_count * C.REWARD_PER_CORRECT_ANSWER
        self.payoff += crt_earnings

        # Store CRT earnings in participant.vars for use in other apps if needed
        self.participant.vars['crt_earnings'] = crt_earnings


class CRT(Page):
    form_model = 'player'
    form_fields = ['quiz1', 'quiz2', 'quiz3', 'quiz4', 'quiz5', 'quiz6', 'quiz7', 'quiz8', 'quiz9', 'quiz10']

    @staticmethod
    def error_message(player: Player, values):
        solutions = dict(
            quiz1=(5, 5),
            quiz2=(5, 5),
            quiz3=(47, 47),
            quiz4=(9, 9),
            quiz5=(12, 12),
            quiz6=(14, 14),
            quiz7=(0.5, 0.5),
            quiz8=(0.12, 0.12),  # 0.3 * 0.4
            quiz9=(1.8, 1.8),  # (0.2 * 1) + (0.8 * 2)
            quiz10=(1.3, 1.3),
        )

        # ✅ Identify incorrect responses
        errors = {
            k: solutions[k][1] for k, v in values.items() if v != solutions[k][0]
        }

        for k in errors.keys():
            wrong_field = f'{k}_wrong'

            # ✅ Correct way to handle uninitialized fields in oTree
            num = player.field_maybe_none(wrong_field) or 0  # Uses 0 if None

            setattr(player, wrong_field, num + 1)  # ✅ Increment safely

        if errors:
            player.num_failed_attempts += 1
            if player.num_failed_attempts >= 1:
                player.failed_too_many = True
            else:
                return errors  # ✅ Return errors only if below failure threshold

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Calculate and add the CRT payoff
        player.calculate_crt_payoff()


class Next(Page):
    @staticmethod
    def vars_for_template(player: Player):
        # Retrieve search earnings from participant.vars
        search_earnings = player.participant.vars.get('final_payment', 0)
        # Retrieve CRT earnings from participant.vars
        crt_earnings = player.participant.vars.get('crt_earnings', 0)

        # Calculate combined total earnings
        total_earnings = search_earnings + crt_earnings

        # Set participant.payoff for use in the payment tab
        player.participant.vars['total_earnings'] = total_earnings
        player.participant.payoff = total_earnings

        return {
            'total_earnings': total_earnings
        }

    @staticmethod
    def is_displayed(player: Player):
        return player.failed_too_many


page_sequence = [CRT, Next]
