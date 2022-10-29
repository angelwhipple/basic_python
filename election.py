from state import State


def load_election(filename):
    """
    Reads the contents of a file, with data given in the following tab-separated format:
    State[tab]Democrat_votes[tab]Republican_votes[tab]EC_votes

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a list of State instances
    """
    states = []
    data = open(filename, 'r')
    data.readline()
    for line in data:
        state_data = line.split("\t", 3)
        states.append(State(state_data[0], state_data[1], state_data[2], state_data[3]))
    return states


def election_winner(election):
    """
    Finds the winner of the election based on who has the most amount of EC votes.
    In this simplified representation, all of EC votes from a state go
    to the party with the majority vote.

    Parameters:
    election - a list of State instances

    Returns:
    a tuple, (winner, loser) of the election i.e. ('dem', 'rep') if Democrats won, else ('rep', 'dem')
    """
    dem_votes, rep_votes = 0, 0
    for state in election:
        if state.get_winner() == 'dem':
            dem_votes += state.get_ecvotes()
        else:
            rep_votes += state.get_ecvotes()
    if dem_votes > rep_votes:
        return ('dem', 'rep')
    else:
        return ('rep', 'dem')


def winner_states(election):
    """
    Finds the list of States that were won by the winning candidate (lost by the losing candidate).

    Parameters:
    election - a list of State instances

    Returns:
    A list of State instances won by the winning candidate
    """
    winner_states = []
    winner = election_winner(election)[0]
    for state in election:
        if state.get_winner() == winner:
            winner_states.append(state)
    return winner_states


def ec_votes_to_flip(election, total=538):
    """
    Finds the number of additional EC votes required by the loser to change election outcome.
    Note: A party wins when they earn half the total number of EC votes plus 1.

    Parameters:
    election - a list of State instances
    total - total possible number of EC votes

    Returns:
    int, number of additional EC votes required by the loser to change the election outcome
    """
    loser_votes = 0
    winners_states = winner_states(election)
    for state in election:
        if state not in winners_states:
            loser_votes += state.get_ecvotes()
    votes_to_flip = (total/2 + 1) - loser_votes
    return int(votes_to_flip)


def combinations(L):
    """
    Helper function to generate powerset of all possible combinations
    of items in input list L. E.g., if
    L is [1, 2] it will return a list with elements
    [], [1], [2], and [1,2].

    Parameters:
    L - list of items

    Returns:
    a list of lists that contains all possible
    combinations of the elements of L
    """

    def get_binary_representation(n, num_digits):
        """
        Inner function to get a binary representation of items to add to a subset,
        which combinations() uses to construct and append another item to the powerset.

        Parameters:
        n and num_digits are non-negative ints

        Returns:
            a num_digits str that is a binary representation of n
        """
        result = ''
        while n > 0:
            result = str(n%2) + result
            n = n//2
        if len(result) > num_digits:
            raise ValueError('not enough digits')
        for i in range(num_digits - len(result)):
            result = '0' + result
        return result

    powerset = []
    for i in range(0, 2**len(L)):
        binStr = get_binary_representation(i, len(L))
        subset = []
        for j in range(len(L)):
            if binStr[j] == '1':
                subset.append(L[j])
        powerset.append(subset)
    return powerset

def brute_force_swing_states(winner_states, ec_votes):
    """
    Finds a subset of winner_states that would change an election outcome if
    voters moved into those states, these are our swing states. Iterate over
    all possible move combinations using the helper function combinations(L).
    Return the move combination that minimises the number of voters moved. If
    there exists more than one combination that minimises this, return any one of them.

    Parameters:
    winner_states - a list of State instances that were won by the winner
    ec_votes - int, number of EC votes needed to change the election outcome

    Returns:
    A list of State instances such that the election outcome would change if additional
    voters relocated to those states
    The empty list, if no possible swing states
    """
    best_combo = []
    min_voters = None
    possible_move_combinations = combinations(winner_states)
    for combo in possible_move_combinations:
        flipped_votes = 0
        moved_voters = 0
        for state in combo:
            flipped_votes += state.get_ecvotes()
            moved_voters += state.get_margin()
        if flipped_votes >= ec_votes and (min_voters == None or moved_voters < min_voters):
            best_combo = combo
            min_voters = moved_voters
    return best_combo


def access_memo(key_tuple, solution, memo = {}):
    """

    Parameters:
        A function to pass a dictionary into move_max_voters for memoization.
        
    key_tuple - (int, int) tuple indicating the key to be searched for in memo
    solution - list, the solution associated with the current len(winner_states) 
    and limit ec_votes. None if a solution is being newly added to memo
    memo - dict, default argument to allow for modification
    Returns:
    A list for solution associated with memo[key_tuple], returns None if a solution 
    is being newly added.
    """
    if key_tuple in memo and solution == None:
        return memo[key_tuple]
    elif key_tuple not in memo and solution == None:
        return None
    else:
        memo[key_tuple] = solution
        return None

def move_max_voters(winner_states, ec_votes):
    """
    Finds the largest number of voters needed to relocate to get at most ec_votes
    for the election loser.

    Analogy to the knapsack problem:
        Given a list of states each with a weight(ec_votes) and value(margin+1),
        determine the states to include in a collection so the total weight(ec_votes)
        is less than or equal to the given limit(ec_votes) and the total value(voters displaced)
        is as large as possible.

    Parameters:
    winner_states - a list of State instances that were won by the winner
    ec_votes - int, the maximum number of EC votes

    Returns:
    A list of State instances such that the maximum number of voters need to be relocated
    to these states in order to get at most ec_votes
    The empty list, if every state has a # EC votes greater than ec_votes
    """
    # Initializing dictionary memo within the function for memoization
    # Checking if a dictionary entry already exists for the current list of states and weight limit
    if type(access_memo((len(winner_states), ec_votes), None)) is list:
        solution = access_memo((len(winner_states), ec_votes), None)
    #Base case; winner states list is empty/weight limit is 0, solution list is empty and total value is 0
    elif winner_states == [] or ec_votes == 0:
        solution = ()
    #Check if current state should be neglected from the list if its weight is greater than the weight limit
    elif winner_states[0].get_ecvotes() > ec_votes:
        #Proceed with a recursive call on the remaining states
        solution = move_max_voters(winner_states[1:], ec_votes)
    else:
        next_state = winner_states[0]
        new_weight_lim = ec_votes - next_state.get_ecvotes()
        # "Left" option recursive call; passing list of remaining states and updated
        # weight limit of (original weight limit - weight of current state) as params
        with_state = move_max_voters(winner_states[1:], new_weight_lim)
        val = sum([state.get_margin()+1 for state in with_state]) + (next_state.get_margin()+1)
        # "Right" option recursive call; passing list of remaining states and original 
        # weight limit as params; not adding next_state to the list
        no_state = move_max_voters(winner_states[1:], ec_votes)
        stateless_val = sum([state.get_margin()+1 for state in no_state])
        # Choosing the solution list with a larger value of displaced voters
        if val > stateless_val:
            solution = tuple(with_state) + (next_state,)
        else:
            solution = no_state
    access_memo((len(winner_states), ec_votes), list(solution))
    #print("Iteration")
    #print(list(solution))
    return list(solution)
    
        
        

def move_min_voters(winner_states, ec_votes_needed):
    """
    Finds a subset of winner_states that would change an election outcome if
    voters moved into those states. Should minimize the number of voters being relocated.
    Only return states that were originally won by the winner (lost by the loser)
    of the election.

    Parameters:
    winner_states - a list of State instances that were won by the winner
    ec_votes_needed - int, number of EC votes needed to change the election outcome

    Returns:
    A list of State instances such that the election outcome would change if additional
    voters relocated to those states (also can be referred to as our swing states)
    The empty list, if no possible swing states
    """
        swing_states = []
    total_votes_won = 0
    for state in winner_states:
        total_votes_won += state.get_ecvotes()
    max_ec_votes = total_votes_won - ec_votes_needed
    try:
        non_swing_states = move_max_voters(winner_states, max_ec_votes)
        for state in winner_states:
            if state not in non_swing_states:
                swing_states.append(state)
    except TypeError:
        return swing_states
    return swing_states
    


def relocate_voters(election, swing_states, states_with_pride = ['AL', 'AZ', 'CA', 'TX']):
    """
    Finds a way to shuffle voters in order to flip an election outcome. Moves voters
    from states that were won by the losing candidate (states not in winner_states), to
    each of the states in swing_states. To win a swing state, you must move (margin + 1)
    new voters into that state. Any state that voters are moved from should still be won
    by the loser even after voters are moved. Also finds the number of EC votes gained by
    this rearrangement, as well as the minimum number of voters that need to be moved.
    Note: You cannot move voters out of Alabama, Arizona, California, or Texas.

    Parameters:
    election - a list of State instances representing the election
    swing_states - a list of State instances where people need to move to flip the election outcome
                   (result of move_min_voters or greedy_swing_states)
    states_with_pride - a list of Strings holding the names of states where residents cannot be moved from
                    (default states are AL, AZ, CA, TX)

    Return:
    A tuple that has 3 elements in the following order:
        - an int, the total number of voters moved
        - a dictionary with the following (key, value) mapping:
            - Key: a 2 element tuple of str, (from_state, to_state), the 2 letter State names
            - Value: int, number of people that are being moved
        - an int, the total number of EC votes gained by moving the voters
    None, if it is not possible to sway the election
    """
      total_moved, flip_map, ec_gain = 0, {}, 0
    winners_states, losing_states = winner_states(election), []
    l_margins = []
    for state in election:
        if state not in winners_states:
            losing_states.append(state)
            l_margins.append(state.get_margin())
    try:
        for state in swing_states:
            voters_needed = state.get_margin()+1
            for i in range(len(losing_states)):
                if losing_states[i].get_name() in states_with_pride:
                    continue
                moved = 0
                if l_margins[i] == 1:
                    continue
                elif l_margins[i] > voters_needed:
                    losing_states[i].subtract_winning_candidate_voters(voters_needed)
                    state.add_losing_candidate_voters(voters_needed)
                    moved += voters_needed
                    total_moved += moved
                    flip_map[(losing_states[i].get_name(), state.get_name())] = moved
                    voters_needed = 0
                    l_margins[i] -= moved
                else:
                    losing_states[i].subtract_winning_candidate_voters(l_margins[i]-1)
                    state.add_losing_candidate_voters(l_margins[i]-1)
                    moved += l_margins[i]-1
                    total_moved += moved
                    flip_map[(losing_states[i].get_name(), state.get_name())] = moved
                    voters_needed = voters_needed % moved
                    l_margins[i] = 1
                if voters_needed == 0:
                    break
            if voters_needed != 0:
                raise AssertionError
            else:
                ec_gain += state.get_ecvotes()
        return (total_moved, flip_map, ec_gain)
    except AssertionError:
        return None
    


if __name__ == "__main__":
    year = 2012
    election = load_election("%s_results.txt" % year)
    print(len(election))
    print(election[0])

       winner, loser = election_winner(election)
    won_states = winner_states(election)
    names_won_states = [state.get_name() for state in won_states]
    reqd_ec_votes = ec_votes_to_flip(election)
    print("Winner:", winner, "\nLoser:", loser)
    print("States won by the winner: ", names_won_states)
    print("EC votes needed:",reqd_ec_votes, "\n")

       brute_election = load_election("60002_results.txt")
    brute_won_states = winner_states(brute_election)
    brute_ec_votes_to_flip = ec_votes_to_flip(brute_election, total=14)
    brute_swing = brute_force_swing_states(brute_won_states, brute_ec_votes_to_flip)
    names_brute_swing = [state.get_name() for state in brute_swing]
    voters_brute = sum([state.get_margin()+1 for state in brute_swing])
    ecvotes_brute = sum([state.get_ecvotes() for state in brute_swing])
    print("Brute force swing states results:", names_brute_swing)
    print("Brute force voters displaced:", voters_brute, "for a total of", ecvotes_brute, "Electoral College votes.\n")

       print("move_max_voters")
    total_lost = sum(state.get_ecvotes() for state in won_states)
    non_swing_states = move_max_voters(won_states, total_lost-reqd_ec_votes)
    non_swing_states_names = [state.get_name() for state in non_swing_states]
    max_voters_displaced = sum([state.get_margin()+1 for state in non_swing_states])
    max_ec_votes = sum([state.get_ecvotes() for state in non_swing_states])
    print("States with the largest margins (non-swing states):", non_swing_states_names)
    print("Max voters displaced:", max_voters_displaced, "for a total of", max_ec_votes, "Electoral College votes.", "\n")

       print("move_min_voters")
    swing_states = move_min_voters(won_states, reqd_ec_votes)
    swing_state_names = [state.get_name() for state in swing_states]
    min_voters_displaced = sum([state.get_margin()+1 for state in swing_states])
    swing_ec_votes = sum([state.get_ecvotes() for state in swing_states])
    print("Complementary knapsack swing states results:", swing_state_names)
    print("Min voters displaced:", min_voters_displaced, "for a total of", swing_ec_votes, "Electoral College votes. \n")

    # # tests Problem 5: relocate_voters
    print("relocate_voters")
    flipped_election = relocate_voters(election, swing_states)
    print("Flip election mapping:", flipped_election)