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

# PyRat imports
from pyrat import Player, Maze, GameState, Action, Graph

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class DFS (Player):

    """
        This player is basically a player that does nothing except printing the phase of the game.
        It is meant to be used as a template to create new players.
        Methods "preprocessing" and "postprocessing" are optional.
        Method "turn" is mandatory.
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self:     Self,
                   *args:    Any,
                   **kwargs: Any
                 ) ->        None:

        # Inherit from parent class
        super().__init__(*args, **kwargs)
        self.actions = []
        # Print phase of the game
        print("Constructor")
        # No return statement needed as the return type is None



    #############################################################################################################################################
    #                                                               PYRAT METHODS                                                               #
    #############################################################################################################################################

    @override
    def preprocessing(self: Self,
                    maze: Maze,
                    game_state: GameState,
                    ) -> None:
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
        
        # Print phase of the game
        print("Preprocessing")

        # Get the player's initial location
        initial_location = game_state.player_locations[self.name]
        
        # Get the location of the cheese
        cheese_location = game_state.cheese[0]
        
        # Perform a traversal from the initial location
        distances, routing_table = self.traversal(maze, initial_location)

        # Find the route from the initial location to the cheese location
        route = self.find_route(routing_table, initial_location, cheese_location)

        # Convert the route to actions using maze's method
        self.actions = maze.locations_to_actions(route)

        # Optional: Print the computed actions for debugging
        print("Computed Actions:", self.actions)


    
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

        # Print phase of the game
        print("Turn", game_state.turn)
        if self.actions:
        # Pop the next action from the list
            return self.actions.pop(0)

        # Return an action
        return Action.NOTHING

#############################################################################################################################################

    @override
    def postprocessing ( self:       Self,
                         maze:       Maze,
                         game_state: GameState,
                         stats:      Dict[str, Any],
                       ) ->          None:

        """
            This method redefines the method of the parent class.
            It is called once at the end of the game.
            In:
                * self:       Reference to the current object.
                * maze:       An object representing the maze in which the player plays.
                * game_state: An object representing the state of the game.
                * stats:      Statistics about the game.
            Out:
                * None.
        """

        # Print phase of the game
        print("Postprocessing")


#####################################################################################################################################################
#####################################################################################################################################################



    def traversal(self, 
                graph,  # No strict type here to accommodate BigHolesRandomMaze
                source: Integral
                ) -> Tuple[Dict[Integral, Integral], Dict[Integral, Optional[Integral]]]:
        """
        Perform a depth-first search traversal from a source vertex.
        Returns a tuple of distances and the routing table (parents of each vertex).
        """
        distances = {}  # To store the distances from the source
        routing_table = {}  # To store the parent of each vertex
        visited = set()  # To track visited vertices
        stack = [source]  # Stack for DFS

        # Initialize the source vertex
        distances[source] = 0
        routing_table[source] = None

        # DFS traversal using a stack
        while stack:
            current = stack.pop()  # Use LIFO for DFS

            if current not in visited:
                visited.add(current)

                # Traverse neighbors
                for neighbor in graph.get_neighbors(current):
                    if neighbor not in visited:
                        # Add neighbor to stack for DFS exploration
                        stack.append(neighbor)
                        
                        # Set the parent and distance for the neighbor
                        routing_table[neighbor] = current
                        distances[neighbor] = distances[current] + 1

        return distances, routing_table
    
    def find_route(self: Self,
                routing_table: Dict[Integral, Optional[Integral]],
                source: Integral,
                target: Integral
                ) -> List[Integral]:
        """
        This method finds the route from the source to the target using the routing table.
        In:
            * self: Reference to the current object.
            * routing_table: The routing table.
            * source: The source vertex.
            * target: The target vertex.
        Out:
            * route: The route from the source to the target.
        """

        # Initialize the route as an empty list
        route = []
        
        # Start from the target and backtrack to the source
        current = target
        
        while current is not None:
            route.append(current)
            current = routing_table[current]  # Move to the parent vertex
        
        # The route is built in reverse, so we need to reverse it
        route.reverse()
        
        # If the source is not in the route (i.e., unreachable), return an empty list
        if route[0] != source:
            return []

        return route


    # Your code here

#####################################################################################################################################################
