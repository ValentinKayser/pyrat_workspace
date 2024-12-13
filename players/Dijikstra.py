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
import heapq

# PyRat imports
from pyrat import Player, Maze, GameState, Action, Graph
from collections import deque
#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class Dijikstra (Player):

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



    def traversal (self:   Self,
                        graph:  Graph,
                        source: int
                        ) ->          Action:

        """
            Implementation of Dijkstra's algorithm using a min-heap to find the shortest paths
            from a source node to all other nodes in the graph.
                In:
                    * self: Reference to the current object.
                    * routing_table: The routing table.
                    * source: The source vertex.
                    * target: The target vertex.
                Out:
                    * route: The route from the source to the target.
        """

        # Initialisation des distances et de la table de routage
        distances = {vertex: float('inf') for vertex in graph.vertices}
        distances[source] = 0
        routing_table = {vertex: None for vertex in graph.vertices}

        # Utilisation d'une file de priorité pour gérer les sommets à explorer
        priority_queue = [(0, source)]

        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)

            # Si la distance actuelle est supérieure à la distance enregistrée, continuer
            if current_distance > distances[current_vertex]:
                continue

            # Exploration des voisins
            for neighbor in graph.get_neighbors(current_vertex):
                weight = graph.get_weight(current_vertex, neighbor)
                distance = current_distance + weight

                # Si une distance plus courte est trouvée
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    routing_table[neighbor] = current_vertex
                    heapq.heappush(priority_queue, (distance, neighbor))

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
