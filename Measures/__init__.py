from otree.api import *

class Constants(BaseConstants):
    name_in_url = 'Measures'
    players_per_group = None
    num_rounds = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):

        # Store each scenario choice separately
    risk_choice_1 = models.StringField(choices=['Lottery', 'Safe Payment'], label="Scenario 1")
    risk_choice_2 = models.StringField(choices=['Lottery', 'Safe Payment'], label="Scenario 2")
    risk_choice_3 = models.StringField(choices=['Lottery', 'Safe Payment'], label="Scenario 3")
    risk_choice_4 = models.StringField(choices=['Lottery', 'Safe Payment'], label="Scenario 4")
    risk_choice_5 = models.StringField(choices=['Lottery', 'Safe Payment'], label="Scenario 5")
    risk_choice_6 = models.StringField(choices=['Lottery', 'Safe Payment'], label="Scenario 6")
    risk_choice_7 = models.StringField(choices=['Lottery', 'Safe Payment'], label="Scenario 7")
    risk_choice_8 = models.StringField(choices=['Lottery', 'Safe Payment'], label="Scenario 8")
    risk_choice_9 = models.StringField(choices=['Lottery', 'Safe Payment'], label="Scenario 9")
    risk_choice_10 = models.StringField(choices=['Lottery', 'Safe Payment'], label="Scenario 10")
    risk_choice_11 = models.StringField(choices=['Lottery', 'Safe Payment'], label="Scenario 11")
    risk_choice_12 = models.StringField(choices=['Lottery', 'Safe Payment'], label="Scenario 12")
    risk_choice_13 = models.StringField(choices=['Lottery', 'Safe Payment'], label="Scenario 13")
    risk_choice_14 = models.StringField(choices=['Lottery', 'Safe Payment'], label="Scenario 14")
    risk_choice_15 = models.StringField(choices=['Lottery', 'Safe Payment'], label="Scenario 15")
    risk_choice_16 = models.StringField(choices=['Lottery', 'Safe Payment'], label="Scenario 16")
    risk_choice_17 = models.StringField(choices=['Lottery', 'Safe Payment'], label="Scenario 17")
    risk_choice_18 = models.StringField(choices=['Lottery', 'Safe Payment'], label="Scenario 18")
    risk_choice_19 = models.StringField(choices=['Lottery', 'Safe Payment'], label="Scenario 19")
    risk_choice_20 = models.StringField(choices=['Lottery', 'Safe Payment'], label="Scenario 20")
    risk_choice_21 = models.StringField(choices=['Lottery', 'Safe Payment'], label="Scenario 21")
    risk_choice_22 = models.StringField(choices=['Lottery', 'Safe Payment'], label="Scenario 22")
    risk_choice_23 = models.StringField(choices=['Lottery', 'Safe Payment'], label="Scenario 23")
    risk_choice_24 = models.StringField(choices=['Lottery', 'Safe Payment'], label="Scenario 24")
    risk_choice_25 = models.StringField(choices=['Lottery', 'Safe Payment'], label="Scenario 25")
    risk_choice_26 = models.StringField(choices=['Lottery', 'Safe Payment'], label="Scenario 26")
    risk_choice_27 = models.StringField(choices=['Lottery', 'Safe Payment'], label="Scenario 27")
    risk_choice_28 = models.StringField(choices=['Lottery', 'Safe Payment'], label="Scenario 28")
    risk_choice_29 = models.StringField(choices=['Lottery', 'Safe Payment'], label="Scenario 29")
    risk_choice_30 = models.StringField(choices=['Lottery', 'Safe Payment'], label="Scenario 30")
    risk_choice_31 = models.StringField(choices=['Lottery', 'Safe Payment'], label="Scenario 31")


    # Risk preferences self-assessment
    risk_self_assessment = models.IntegerField(
        label="Are you generally a person who is fully prepared to take risks or do you try to avoid taking risks?",
        choices=range(0, 11),  # Slider from 0 to 10
        widget=widgets.RadioSelectHorizontal
    )

    # Risk preferences paired lotteries
    risk_lottery_choices = models.LongStringField(
        label="For the paired lotteries, indicate whether you choose the lottery or the safe payment in each scenario."
    )

    # LOT-R Questions (Corrected Indentation)
    lotr_q1 = models.StringField(
        choices=[('A', 'I agree a lot'),
                 ('B', 'I agree a little'),
                 ('C', 'I neither agree nor disagree'),
                 ('D', 'I disagree a little'),
                 ('E', 'I disagree a lot')],
        label="In uncertain times, I usually expect the best.",
        widget=widgets.RadioSelect
    )
    lotr_q2 = models.StringField(
        choices=[('A', 'I agree a lot'),
                 ('B', 'I agree a little'),
                 ('C', 'I neither agree nor disagree'),
                 ('D', 'I disagree a little'),
                 ('E', 'I disagree a lot')],
        label="If something can go wrong for me, it will.",
        widget=widgets.RadioSelect
    )
    lotr_q3 = models.StringField(
        choices=[('A', 'I agree a lot'),
                 ('B', 'I agree a little'),
                 ('C', 'I neither agree nor disagree'),
                 ('D', 'I disagree a little'),
                 ('E', 'I disagree a lot')],
        label="I'm always optimistic about my future.",
        widget=widgets.RadioSelect
    )
    lotr_q4 = models.StringField(
        choices=[('A', 'I agree a lot'),
                 ('B', 'I agree a little'),
                 ('C', 'I neither agree nor disagree'),
                 ('D', 'I disagree a little'),
                 ('E', 'I disagree a lot')],
        label="I hardly ever expect things to go my way.",
        widget=widgets.RadioSelect
    )
    lotr_q5 = models.StringField(
        choices=[('A', 'I agree a lot'),
                 ('B', 'I agree a little'),
                 ('C', 'I neither agree nor disagree'),
                 ('D', 'I disagree a little'),
                 ('E', 'I disagree a lot')],
        label="I rarely count on good things happening to me.",
        widget=widgets.RadioSelect
    )
    lotr_q6 = models.StringField(
        choices=[('A', 'I agree a lot'),
                 ('B', 'I agree a little'),
                 ('C', 'I neither agree nor disagree'),
                 ('D', 'I disagree a little'),
                 ('E', 'I disagree a lot')],
        label="Overall, I expect more good things to happen to me than bad.",
        widget=widgets.RadioSelect
    )

    # Rosenberg Self-Esteem Scale
    self_esteem_q1 = models.StringField(
        choices=[['1', 'Strongly Disagree'],
                 ['2', 'Disagree'],
                 ['3', 'Neutral'],
                 ['4', 'Agree'],
                 ['5', 'Strongly Agree']],
        label="I feel that I'm a person of worth, at least on an equal basis with others.",
        widget=widgets.RadioSelect
    )
    self_esteem_q2 = models.StringField(
        choices=[['1', 'Strongly Disagree'],
                 ['2', 'Disagree'],
                 ['3', 'Neutral'],
                 ['4', 'Agree'],
                 ['5', 'Strongly Agree']],
        label="I feel that I have a number of good qualities.",
        widget=widgets.RadioSelect
    )
    self_esteem_q3 = models.StringField(
        choices=[['1', 'Strongly Disagree'],
                 ['2', 'Disagree'],
                 ['3', 'Neutral'],
                 ['4', 'Agree'],
                 ['5', 'Strongly Agree']],
        label="All in all, I am inclined to feel that I am a failure.",
        widget=widgets.RadioSelect
    )
    self_esteem_q4 = models.StringField(
        choices=[['1', 'Strongly Disagree'],
                 ['2', 'Disagree'],
                 ['3', 'Neutral'],
                 ['4', 'Agree'],
                 ['5', 'Strongly Agree']],
        label="I am able to do things as well as most other people.",
        widget=widgets.RadioSelect
    )
    self_esteem_q5 = models.StringField(
        choices=[['1', 'Strongly Disagree'],
                 ['2', 'Disagree'],
                 ['3', 'Neutral'],
                 ['4', 'Agree'],
                 ['5', 'Strongly Agree']],
        label="On the whole, I am satisfied with myself.",
        widget=widgets.RadioSelect
    )
    self_esteem_q6 = models.StringField(
        choices=[['1', 'Strongly Disagree'],
                 ['2', 'Disagree'],
                 ['3', 'Neutral'],
                 ['4', 'Agree'],
                 ['5', 'Strongly Agree']],
        label="I certainly feel useless at times.",
        widget=widgets.RadioSelect
    )

    locus_q1_choice = models.StringField(
        choices=[['A', 'What happens to me is my own doing'],
                 ['B', 'Sometimes I feel that I don’t have enough control over the direction my life is taking']],
        label="Which statement is closer to your opinion?",
        widget=widgets.RadioSelect
    )
    locus_q1_closeness = models.StringField(
        choices=[['Somewhat', 'Somewhat Close to My Opinion'],
                 ['Very', 'Very Close to My Opinion']],
        label="How close is the above statement to your opinion",
        widget=widgets.RadioSelect
    )

    # Question Pair 2
    locus_q2_choice = models.StringField(
        choices=[['A', 'When I make plans, I am almost certain that I can make them work'],
                 ['B',
                  'It is not always wise to plan too far ahead because many things turn out to be a matter of good or bad fortune']],
        label="Which statement is closer to your opinion?",
        widget=widgets.RadioSelect
    )
    locus_q2_closeness = models.StringField(
        choices=[['Somewhat', 'Somewhat Close to My Opinion'],
                 ['Very', 'Very Close to My Opinion']],
        label="How close is the above statement to your opinion",
        widget=widgets.RadioSelect
    )

    # Question Pair 3
    locus_q3_choice = models.StringField(
        choices=[['A', 'In my case, getting what I want has little or nothing to do with luck'],
                 ['B', 'Many times we might just as well decide what to do by flipping a coin']],
        label="Which statement is closer to your opinion?",
        widget=widgets.RadioSelect
    )
    locus_q3_closeness = models.StringField(
        choices=[['Somewhat', 'Somewhat Close to My Opinion'],
                 ['Very', 'Very Close to My Opinion']],
        label="How close is the above statement to your opinion",
        widget=widgets.RadioSelect
    )

    # Question Pair 4
    locus_q4_choice = models.StringField(
        choices=[['A', 'Many times I feel that I have little influence over the things that happen to me'],
                 ['B', 'It is impossible for me to believe that chance or luck plays an important role in my life']],
        label="Which statement is closer to your opinion?",
        widget=widgets.RadioSelect
    )
    locus_q4_closeness = models.StringField(
        choices=[['Somewhat', 'Somewhat Close to My Opinion'],
                 ['Very', 'Very Close to My Opinion']],
        label="How close is the above statement to your opinion?",
        widget=widgets.RadioSelect
    )


    greed_q1 = models.StringField(
        label="In selecting a job or career, how important is it to you to have the chance to be a leader?",
        choices=[['1', 'Not at all important'],
                 ['2', 'Slightly important'],
                 ['3', 'Moderately important'],
                 ['4', 'Very important'],
                 ['5', 'Extremely important']],
        widget=widgets.RadioSelect
    )
    greed_q2 = models.StringField(
        label="In selecting a job or career, how important is it to you to make a lot of money?",
        choices=[['1', 'Not at all important'],
                 ['2', 'Slightly important'],
                 ['3', 'Moderately important'],
                 ['4', 'Very important'],
                 ['5', 'Extremely important']],
        widget=widgets.RadioSelect
    )
    greed_q3 = models.StringField(
        label="In selecting a job or career, how important is it to you to be useful to society?",
        choices=[['1', 'Not at all important'],
                 ['2', 'Slightly important'],
                 ['3', 'Moderately important'],
                 ['4', 'Very important'],
                 ['5', 'Extremely important']],
        widget=widgets.RadioSelect
    )


    competitiveness_q1 = models.StringField(
        choices=[['1', 'Strongly Disagree'],
                 ['2', 'Disagree'],
                 ['3', 'Neutral'],
                 ['4', 'Agree'],
                 ['5', 'Strongly Agree']],
        label="I enjoy working in situations involving competition with others.",
        widget=widgets.RadioSelect
    )
    competitiveness_q2 = models.StringField(
        choices=[['1', 'Strongly Disagree'],
                 ['2', 'Disagree'],
                 ['3', 'Neutral'],
                 ['4', 'Agree'],
                 ['5', 'Strongly Agree']],
        label="It is important to me to perform better than others on a task.",
        widget=widgets.RadioSelect
    )
    competitiveness_q3 = models.StringField(
        choices=[['1', 'Strongly Disagree'],
                 ['2', 'Disagree'],
                 ['3', 'Neutral'],
                 ['4', 'Agree'],
                 ['5', 'Strongly Agree']],
        label="I feel that winning is important in both work and games.",
        widget=widgets.RadioSelect
    )
    competitiveness_q4 = models.StringField(
        choices=[['1', 'Strongly Disagree'],
                 ['2', 'Disagree'],
                 ['3', 'Neutral'],
                 ['4', 'Agree'],
                 ['5', 'Strongly Agree']],
        label="It annoys me when other people perform better than I do.",
        widget=widgets.RadioSelect
    )
    competitiveness_q5 = models.StringField(
        choices=[['1', 'Strongly Disagree'],
                 ['2', 'Disagree'],
                 ['3', 'Neutral'],
                 ['4', 'Agree'],
                 ['5', 'Strongly Agree']],
        label="I try harder when I am in competition with other people.",
        widget=widgets.RadioSelect
    )
# PAGES (Corrected `LOTR(Page)` Placement)
class RiskSelfAssessment(Page):
    form_model = 'player'
    form_fields = ['risk_self_assessment']


class RiskLottery(Page):
    form_model = 'player'
    form_fields = [
        'risk_choice_1', 'risk_choice_2', 'risk_choice_3', 'risk_choice_4', 'risk_choice_5',
        'risk_choice_6', 'risk_choice_7', 'risk_choice_8', 'risk_choice_9', 'risk_choice_10',
        'risk_choice_11', 'risk_choice_12', 'risk_choice_13', 'risk_choice_14', 'risk_choice_15',
        'risk_choice_16', 'risk_choice_17', 'risk_choice_18', 'risk_choice_19', 'risk_choice_20',
        'risk_choice_21', 'risk_choice_22', 'risk_choice_23', 'risk_choice_24', 'risk_choice_25',
        'risk_choice_26', 'risk_choice_27', 'risk_choice_28', 'risk_choice_29', 'risk_choice_30',
        'risk_choice_31'
    ]

    def vars_for_template(self):
        # Ensure scenarios are passed to the template
        return {
            'scenarios': [
                {'number': i, 'safe_payment': (i - 1) * 10, 'formfield_name': f'risk_choice_{i}'}
                for i in range(1, 32)
            ]
        }



class LOTR(Page):
    form_model = 'player'
    form_fields = ['lotr_q1', 'lotr_q2', 'lotr_q3', 'lotr_q4', 'lotr_q5', 'lotr_q6']

class SelfEsteem(Page):
    form_model = 'player'
    form_fields = ['self_esteem_q1', 'self_esteem_q2', 'self_esteem_q3', 'self_esteem_q4', 'self_esteem_q5', 'self_esteem_q6']

class LocusControl(Page):
    form_model = 'player'
    form_fields = [
        'locus_q1_choice', 'locus_q1_closeness',
        'locus_q2_choice', 'locus_q2_closeness',
        'locus_q3_choice', 'locus_q3_closeness',
        'locus_q4_choice', 'locus_q4_closeness'
    ]

class Probability(Page):
    form_model = 'player'
    form_fields = ['prob_q1', 'prob_q2', 'prob_q3', 'prob_q4']

class Greed(Page):
    form_model = 'player'
    form_fields = ['greed_q1', 'greed_q2', 'greed_q3']

class Competitiveness(Page):
    form_model = 'player'
    form_fields = ['competitiveness_q1', 'competitiveness_q2', 'competitiveness_q3', 'competitiveness_q4', 'competitiveness_q5']

class Thankyou(Page):
    pass

page_sequence = [
    RiskSelfAssessment,
    RiskLottery,
    LOTR,  # LOT-R questions now correctly placed
    SelfEsteem,
    LocusControl,
    Greed,
    Competitiveness,
    Thankyou
]
