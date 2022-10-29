"""
A class representing the election results for a given state. 
Assumes there are no ties between dem and rep votes. The party with a 
majority of votes receives all the Electoral College (EC) votes for 
the given state.
"""

class State():
    def __init__(self, name, dem, rep, ec):
        """
        Parameters:
        name - the 2 letter abbreviation of a state
        dem - number of Democrat votes cast
        rep - number of Republican votes cast
        ec - number of EC votes a state has 

        Attributes:
        self.name - str, the 2 letter abbreviation of a state
        self.dem - int, number of Democrat votes cast
        self.rep - int, number of Republican votes cast
        self.ec - int, number of EC votes a state has
        """
        self.name = name
        self.dem = int(dem)
        self.rep = int(rep)
        self.ec = int(ec)
        

    def get_name(self):
        """
        Returns:
        str, the 2 letter abbreviation of the state  
        """
        return self.name

    def get_ecvotes(self):
        """
        Returns:
        int, the number of EC votes the state has 
        """
        return self.ec

    def get_margin(self):
        """
        Returns: 
        int, difference in votes cast between the two parties, a positive number
        """
        return abs(int(self.dem)-int(self.rep))

    def get_winner(self):
        """
        Returns:
        str, the winner of the state, "dem" or "rep"
        """
        if int(self.dem)-int(self.rep) > 0:
            return "dem"
        else:
            return "rep"
    
    def add_losing_candidate_voters(self, voters):
        """
        Increases voters for this state's losing party by voters amount
        Parameters:
        voters - int, voters to add
        """
        if self.get_winner() == "dem":
            self.rep += voters
        else:
            self.dem += voters

    def subtract_winning_candidate_voters(self, voters):
        """
        Decreases voters for this state's winning party by voters amount
        Parameters:
        voters - int, voters to subtract
        """
        if self.get_winner() == "dem":
            self.dem -= voters
        else:
            self.rep -= voters

    def __copy__(self):
        """
        Returns:
        State, a copy of this one
        """
        return State(self.name, self.dem, self.rep, self.ec)

    def __lt__(self, other):
        """
        Determines if this State instance is less other. 
        We will say self is less than other: 
         - if self.margin < other.margin,
         - in case of a tie, we will look at alphabetical order
        Used for comparison during sorting

        Param:
        other - State object to compare against  

        Returns: 
        bool, True if self is less than other, False otherwise
        """
        if self.get_margin() == other.get_margin():
            return self.name < other.name 
        return self.get_margin() < other.get_margin()
    
    def __eq__(self, other):
        """
        Determines if two State instances are the same.
        They are the same if they have the same state name, winner, margin and ec votes.
        Be sure to check for instance type equality as well! 

        Param:
        other - State object to compare against  

        Returns:
        bool, True if the two states are the same, False otherwise
        """
        if isinstance(other, State):
            return self.name == other.name and self.get_winner() == other.get_winner() and self.get_margin() == other.get_margin() and self.ec == other.ec
        return False

    def __str__(self):
        """
        Returns:
        str, representation of this state in the following format,
        "In <state>, <ec> EC votes were won by <winner> by a <margin> vote margin."
        """
        return "In %s, %s EC votes were won by %s by a %s vote margin." % (self.name, self.ec, self.get_winner(), self.get_margin())

    def __repr__(self):
        """
        Used to show the states that are in the list 
        Returns:
        str, formal string representation of the state
        """
        return self.name
