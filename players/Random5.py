#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file contains useful elements to define a particular player.
    In order to use this player, you need to instanciate it and add it to a game.
    Please refer to example games to see how to do it properly.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
from typing import *
from typing_extensions import *
from numbers import *
import random

# PyRat imports
from pyrat import Player, Maze, GameState, Action

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class Random5 (Player):

    """
        This player is an improvement of the Random4 player.
        A limitation of Random4 is that it go in a dead-end where there is no cheese.
        To avoid this, prior to maze exploration, we update the maze map to remove dead-ends.
        Note that the maze received at every turn is the true maze.
        Therefore, we need to store the updated maze as an attribute of the player.
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self:     Self,
                   *args:    Any,
                   **kwargs: Any
                 ) ->        Self:

        """
            This function is the constructor of the class.
            When an object is instantiated, this method is called to initialize the object.
            This is where you should define the attributes of the object and set their initial values.
            Arguments *args and **kwargs are used to pass arguments to the parent constructor.
            This is useful not to declare again all the parent's attributes in the child class.
            In:
                * self:   Reference to the current object.
                * args:   Arguments to pass to the parent constructor.
                * kwargs: Keyword arguments to pass to the parent constructor.
            Out:
                * A new instance of the class.
        """

        # Inherit from parent class
        super().__init__(*args, **kwargs)

        #Â We create an attribute to keep track of visited cells
        self.visited_cells = set()

        # We create an attribute to keep track of the trajectory
        self.trajectory = []

        # We create an attribute to store the updated maze
        self.updated_maze = None
       
    #############################################################################################################################################
    #                                                               PYRAT METHODS                                                               #
    #############################################################################################################################################

    @override
    def preprocessing ( self:       Self,
                        maze:       Maze,
                        game_state: GameState,
                      ) ->          None:
        
        """
            This method redefines the method of the parent class.
            It is called once at the beginning of the game.
            In:
                * self:       Reference to the current object.
                * maze:       An object representing the maze in which the player plays.
                * game_state: An object representing the state of the game.
            Out:
                * None.
        """
        
        #Â Store location to initialize trajectory
        self.trajectory.append(game_state.player_locations[self.name])
        
        #Â Remove dead-ends from the maze
        self.updated_maze = self.simplify_maze(maze, game_state)

    #############################################################################################################################################

    @override
    def turn ( self:       Self,
               maze:       Maze,
               game_state: GameState,
             ) ->          Action:

        """
            This method redefines the abstract method of the parent class.
            It is called at each turn of the game.
            It returns an action to perform among the possible actions, defined in the Action enumeration.
            In:
                * self:       Reference to the current object.
                * maze:       An object representing the maze in which the player plays.
                * game_state: An object representing the state of the game.
            Out:
                * action: One of the possible actions.
        """

        # Mark current cell as visited and add it to the trajectory
        if game_state.player_locations[self.name] not in self.visited_cells:
            self.visited_cells.add(game_state.player_locations[self.name])
        self.trajectory.append(game_state.player_locations[self.name])

        # Return an action
        action = self.find_next_action(game_state)
        return action
    
    #############################################################################################################################################
    #                                                               OTHER METHODS                                                               #
    #############################################################################################################################################

    def find_next_action ( self:       Self,
                           game_state: GameState,
                         ) ->          Action:

        """
            This method returns an action to perform among the possible actions, defined in the Action enumeration.
            Here, the action is chosen randomly among those that don't hit a wall, and that lead to an unvisited cell if possible.
            If no such action exists, we come back on our trajectory.
            In:
                * self:       Reference to the current object.
                * game_state: An object representing the state of the game.
            Out:
                * action: One of the possible actions.
        """

        # Go to an unvisited neighbor in priority
        neighbors = self.updated_maze.get_neighbors(game_state.player_locations[self.name])
        unvisited_neighbors = [neighbor for neighbor in neighbors if neighbor not in self.visited_cells]
        if len(unvisited_neighbors) > 0:
            neighbor = random.choice(unvisited_neighbors)
            
        #Â If there is no unvisited neighbor, backtrack the trajectory
        else:
            _ = self.trajectory.pop(-1)
            neighbor = self.trajectory.pop(-1)
        
        # Retrieve the corresponding action
        action = self.updated_maze.locations_to_action(game_state.player_locations[self.name], neighbor)
        return action
    
    #############################################################################################################################################

    def simplify_maze ( self:       Self,
                        maze:       Maze,
                        game_state: GameState,
                      ) ->          Maze:

        """
            This method simplifies the maze by removing dead-ends.
            It should not remove dead-ends that contain cheese or the player.
            In:
                * self:       Reference to the current object.
                * maze:       The maze to simplify.
                * game_state: The state of the game.
            Out:
                * updated_maze: The simplified maze.
        """

        #Â Iteratively remove dead-ends from the maze
        # We still keep dead ends that contain cheese or the player
        updated_maze = maze
        removed_something = True
        while removed_something:
            removed_something = False
            for vertex in updated_maze.vertices:
                if len(updated_maze.get_neighbors(vertex)) == 1 and vertex != game_state.player_locations[self.name] and vertex not in game_state.cheese:
                    updated_maze.remove_vertex(vertex)
                    removed_something = True

        #Â Return the updated maze
        return updated_maze

#####################################################################################################################################################
#####################################################################################################################################################