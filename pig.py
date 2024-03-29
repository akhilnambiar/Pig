"""The Game of Pig"""

from dice import make_fair_die, make_test_die
from ucb import main, trace, log_current_line, interact

goal = 100  # The goal of pig is always to score 100 points.

# Taking turns

def roll(turn_total, outcome):
    """Performs the roll action, which adds outcome to turn_total, or loses the
    turn on outcome == 1.

    Arguments:
    turn -- number of points accumulated by the player so far during the turn
    outcome -- the outcome of the roll (the number generated by the die)

    Returns three values in order:
    - the number of points the player scores after the roll
      Note: If the turn is not over after this roll, this return value is 0.
            No points are scored until the end of the turn.
    - the player turn point total after the roll
    - a boolean; whether or not the player's turn is over
    
    >>> roll(7, 3)
    (0, 10, False)
    >>> roll(99, 1)
    (1, 0, True)
    """
    if outcome==1:
        return (1,0,True)
    else:
        return(0,turn_total+outcome,False)
    
    

def hold(turn_total, outcome):
    """Performs the hold action, which adds turn_total to the player's score.

    Arguments:
    turn -- number of points accumulated by the player so far during the turn
    outcome -- the outcome of the roll, ie. the number generated by the die

    Returns three values in order:
    - the number of points the player scores after holding
    - the player turn total after the roll (always 0)
    - a boolean; whether or not the player's turn is over
    
    >>> hold(99, 1)
    (99, 0, True)
    """
    "*** YOUR CODE HERE ***"
    return (turn_total,0,True)


def take_turn(plan, dice=make_fair_die(), who='Someone', comments=True):
    """Simulate a single turn and return the points scored for the whole turn.

    Important: The d function should be called once, **and only once**, for
               every action taken!  Testing depends upon this fact.
    
    Arguments:
    plan -- a function that takes the turn total and returns an action function
    dice -- a function that takes no args and returns an integer outcome.
            Note: dice is non-pure!  Call it exactly once per action.
    who -- name of the current player
    comments -- a boolean; whether commentary is enabled
    """
    score_for_turn = 0  # Points scored in the whole turn (after holding)
    "*** YOUR CODE HERE ***"
    turn_over=False # Is the turn over or not?
    turn_value=0 # The number of points that the player has (before holding)
    dice_outcome=0 # The outcome of the dice
    while turn_over==False:
        dice_outcome=dice()
        func1=plan(turn_value)
        score_for_turn,turn_value,turn_over = func1(turn_value,dice_outcome)
        if comments==True:
            commentate(func1,dice_outcome,score_for_turn,turn_value,turn_over,who='Someone')
    return score_for_turn

def take_turn_test():
    """Test the take_turn function using deterministic test dice."""
    plan = make_roll_until_plan(10)  # plan is a function (see problem 2)
    "*** YOUR CODE HERE ***"
    assert take_turn(plan,dice=make_test_die(6,4,1),who='someone',comments=False)==10
    print(take_turn(plan,dice=make_test_die(6,4,1),who='someone',comments=False),"= 10") # Not deterministic
    assert take_turn(plan,dice=make_test_die(6,5,6,6),who='someone',comments=False)==11
    print(take_turn(plan,dice=make_test_die(6,5,6,6),who='someone',comments=False),"= 11")
    assert take_turn(plan,dice=make_test_die(1,4,3),who='someone',comments=False)==1
    print(take_turn(plan,dice=make_test_die(1,4,3),who='someone',comments=False),"= 1")


# Commentating

def commentate(action, outcome, score_for_turn, turn_total, over, who):
    """Print descriptive comments about a game event.
    
    action -- the action function chosen by the current player
    outcome -- the outcome of the die roll
    score_for_turn -- the points scored in this turn by the current player
    turn_total -- the current turn total
    over -- a boolean that indicates whether the turn is over
    who -- the name of the current player 
    """
    print(draw_number(outcome))
    print(who, describe_action(action))
    if over:
        print(who, 'scored', score_for_turn, 'point(s) on this turn.')
    else:
        print(who, 'now has a turn total of', turn_total, 'point(s).')

def describe_action(action):
    """Generate a string that describes an action.

    action -- a function, which should be either hold or roll    

    If action is neither the hold nor roll function, the description should
    announce that cheating has occurred.

    >>> describe_action(roll)
    'chose to roll.'
    >>> describe_action(hold)
    'decided to hold.'
    >>> describe_action(commentate)
    'took an illegal action!'
    """
    "*** YOUR CODE HERE ***"
    if action==roll:
        return 'chose to roll'
    elif action==hold:
        return 'decided to hold'
    else:
        return'took an illegal action'
 
def draw_number(n, dot='*'):
    """Return an ascii art representation of rolling the number n.

    >>> print(draw_number(5))
     -------
    | *   * |
    |   *   |
    | *   * |
     -------
    """
    "*** YOUR CODE HERE ***"
    if n==1:
        return draw_die(True,False,False,False,dot)
    elif n==2:
        return draw_die(False,False,True,False,dot)
    elif n==3:
        return draw_die(True,False,False,True,dot)
    elif n==4:
        return draw_die(False,True,True,False,dot)
    elif n==5:
        return draw_die(True,True,True,False,dot)
    elif n==6:
        return draw_die(False,True,True,True,dot)
    else:
        return 'this is not a valid number'

def draw_die(c, f, b, s, dot):
    """Return an ascii art representation of a die.

    c, f, b, & s are boolean arguments. This function returns a multi-line
    string of the following form, where the letters in the diagram are either
    filled if the corresponding argument is true, or empty if it is false.
    
     -------
    | b   f |
    | s c s |
    | f   b |
     -------    

    Note: The sides with 2 and 3 dots have 2 possible depictions due to
          rotation. Either representation is acceptable. 

    Note: This function uses Python syntax not yet covered in the course.
    
    c, f, b, s -- booleans; whether to place dots in corresponding positions
    dot        -- A length-one string to use for a dot
    """
    border = ' -------'
    def draw(b): 
        return dot if b else ' '
    c, f, b, s = map(draw, [c, f, b, s])
    top =    ' '.join(['|', b, ' ', f, '|'])
    middle = ' '.join(['|', s, c,   s, '|'])
    bottom = ' '.join(['|', f, ' ', b, '|'])
    return '\n'.join([border, top, middle, bottom, border])


# Game simulator

def play(strategy, opponent_strategy):
    """Simulate a game and return 0 if the first player wins and 1 otherwise.
    
    strategy -- The strategy function for the first player (who plays first)
    opponent_strategy -- The strategy function for the second player
    """
    "*** YOUR CODE HERE ***"
    
    who = 0 # Which player is about to take a turn, 0 (first) or 1 (second)
    player1_score=0 #Total score for player 1
    player2_score=0 #Total score for player 2
    is_game_over=False
    while player1_score<100 and player2_score<100:
        while is_game_over==False:
            if(player1_score+player2_score)%7==0:
                dice=make_fair_die(4)
            else:
                dice=make_fair_die()
            if who==0:
                player1_score=player1_score+take_turn(strategy(player1_score,player2_score),dice,who='Player',comments=False)
                if player1_score>=100:
                    is_game_over=True
                    return 0
                else:
                    who=1
            elif who==1:
                player2_score=player2_score+take_turn(opponent_strategy(player2_score,player1_score),dice,who='Enemy',comments=False)
                if player2_score>=100:
                    is_game_over=True
                    return 1
                else:
                    who=0
                                

    
            
        
    
    
    return who

def other(who):
    """Return the other player, for players numbered 0 and 1.
    
    >>> other(0)
    1
    >>> other(1)
    0
    """
    return (who + 1) % 2


# Basic Strategies

def make_roll_until_plan(turn_goal=20):
    """Return a plan to roll until turn total is at least turn_goal."""
    def plan(turn):
        if turn >= turn_goal:
            return hold
        else:
            return roll
    return plan

def make_roll_until_strategy(turn_goal):
    """Return a strategy to always adopt a plan to roll until turn_goal.
    
    A strategy is a function that takes two game scores as arguments and
    returns a plan (which is a function from turn totals to actions).
    """
    "*** YOUR CODE HERE ***"
    def game_strategy(player1_score,player2_score):
        return make_roll_until_plan(turn_goal)
    return game_strategy
        

def make_roll_until_strategy_test():
    """Test that make_roll_until_strategy gives a strategy that returns correct
    roll-until plans."""
    strategy = make_roll_until_strategy(15)    
    plan = strategy(0, 0)
    assert plan(14) == roll, 'Should have returned roll'
    assert plan(15) == hold, 'Should have returned hold'
    assert plan(16) == hold, 'Should have returned hold'


# Experiments (Phase 2)

def average_value(fn, num_samples):
    """Compute the average value returned by fn over num_samples trials.
    
    >>> d = make_test_die(1, 3, 5, 7)
    >>> average_value(d, 100)
    4.0
    """
    "*** YOUR CODE HERE ***"
    total_value,k=0,0
    while k<num_samples:
        k,total_value=k+1,total_value+fn()
    return total_value/num_samples

def averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of fn when called.

    Note: To implement this function, you will have to use *args syntax, a new
          Python feature introduced in this project.  See the project
          description for details.

    >>> die = make_test_die(3, 1, 5, 7)
    >>> avg_die = averaged(die)
    >>> avg_die()
    4.0
    >>> avg_turn = averaged(take_turn)
    >>> avg_turn(make_roll_until_plan(4), die, 'The player', False)
    3.0

    In this last example, two different turn scenarios are averaged.  
    - In the first, the player rolls a 3 then a 1, receiving a score of 1.
    - In the other, the player rolls a 5 (then holds on the 7), scoring 5.
    Thus, the average value is 3.0

    Note: If this last test is called with comments=True in take_turn, the
    doctests will fail because of the extra output.
    """
    "*** YOUR CODE HERE ***"
    def avg_value(*args):
        total_value,k=0,0
        while k<num_samples:
            k,total_value=k+1,total_value+fn(*args)
        return total_value/num_samples
    return avg_value

            
        

def compare_strategies(strategy, baseline=make_roll_until_strategy(20)):
    """Return the average win rate (out of 1) of strategy against baseline."""
    as_first = 1 - averaged(play)(strategy, baseline)
    as_second = averaged(play)(baseline, strategy)
    return (as_first + as_second) / 2  # Average the two results

def eval_strategy_range(make_strategy, lower_bound, upper_bound):
    """Return the best integer argument value for make_strategy to use against
    the roll-until-20 baseline, between lower_bound and upper_bound (inclusive).

    make_strategy -- A one-argument function that returns a strategy.
    lower_bound -- lower bound of the evaluation range
    upper_bound -- upper bound of the evaluation range
    """
    """Within the Range of 15 to 25, they all seem to be fairly even"""
    
    best_value, best_win_rate = 0, 0
    value = lower_bound
    while value <= upper_bound:
        strategy = make_strategy(value)
        win_rate = compare_strategies(strategy)
        print(value, 'win rate against the baseline:', win_rate)
        if win_rate > best_win_rate:
            best_win_rate, best_value = win_rate, value
        value += 1
    return best_value

def run_strategy_experiments():
    """Run a series of strategy experiments and report results."""
    "*** YOUR CODE HERE ***"""
    """print("First Experiment...")
    print(eval_strategy_range(make_roll_until_strategy,15,25))
    print("Second Experiment...")
    print(eval_strategy_range(make_die_specific_strategy,5,25))
    print("Third Experiment...")
    print(eval_strategy_range(make_pride_strategy,15,25))"""
    

def make_die_specific_strategy(four_side_goal, six_side_goal=20):
    """Return a strategy that returns a die-specific roll-until plan.
    
    four_side_goal -- the roll-until goal whenever the turn uses a 4-sided die
    six_side_goal -- the roll-until goal whenever the turn uses a 6-sided die

    """
    "*** YOUR CODE HERE ***"
    def game_strategy(player1_score,player2_score):
        if (player1_score+player2_score)%7==0:
            return make_roll_until_plan(four_side_goal)
        else:
            return make_roll_until_plan(six_side_goal)
    return game_strategy
    

def make_pride_strategy(margin, turn_goal=20):
    """Return a strategy that wants to finish a turn winning by at least margin.

    margin -- the size of the lead that the player requires
    turn_goal -- the minimum roll-until turn goal, even when winning
    """
    "*** YOUR CODE HERE ***"
    
    def game_strategy(player1_score,player2_score):
        gap = player2_score+margin
        margin_goal=gap-player1_score
        if player1_score<=gap and margin_goal>turn_goal:
            return make_roll_until_plan(margin_goal)
        else:
            return make_roll_until_plan(turn_goal)
    return game_strategy
    

def final_strategy(player1_score, player2_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    Final strategy that accounts for if the opponent will get a four sided die, a new strategy if you get a for sided die, and how to roll if you are behind.
    The second part of the plan tries to aim to make the opponent get the 4 sided die
    """
    "*** YOUR CODE HERE ***"
    def plan(turn_total):
        gap=player2_score-player1_score
        if player1_score >=goal-15:
            return make_roll_until_plan(goal-player1_score)(turn_total)
        elif ((player1_score+player2_score+turn_total)%7==0) and turn_total!=0 and (player1_score+turn_total)!=0:
            return hold
        else:
            return make_roll_until_plan(22)(turn_total)
    return plan

    

def interactive_strategy(score, opponent_score):
    """Prints total game scores and returns an interactive plan.
    
    Note: this function uses Python syntax not yet covered in the course.
    """
    print('You have', score, 'and they have', opponent_score, 'total score')
    def plan(turn):
        if turn > 0:
            print('You now have a turn total of', turn, 'points')
        while True:
            response = input('(R)oll or (H)old?')
            if response.lower()[0] == 'r':
                return roll
            elif response.lower()[0] == 'h':
                return hold
            print('Huh?')
    return plan

@main
def run():
    take_turn_test()

    # Uncomment the next line to play an interactive game
    # play(interactive_strategy, make_roll_until_strategy(20))

    # Uncomment the next line to test make_roll_until_strategy
    # make_roll_until_strategy_test()

    run_strategy_experiments()

