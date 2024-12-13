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
import itertools
import heapq

# PyRat imports
from pyrat import Player, Maze, GameState, Action, Graph

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class GreedyEachTurn (Player):

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


        # Print phase of the game
        print("Constructor")
       
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
        
        # Print phase of the game
        print("Preprocessing")
        # Get the player's initial location
        initial_location = game_state.player_locations[self.name]
        cheese_location = game_state.cheese
        matrice =  self.distance_matrice(initial_location, cheese_location, maze)
        self.routing = self.all_routing(maze)
        route = self.find_route(self.routing, matrice, initial_location,maze)
        
        self.actions = maze.locations_to_actions(route)



    


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

        initial_location = game_state.player_locations[self.name]
        cheese_location = game_state.cheese
        matrice =  self.distance_matrice(initial_location, cheese_location, maze)
        route = self.find_route(self.routing, matrice, initial_location,maze)
        self.actions = maze.locations_to_actions(route)

        return self.actions.pop(0)
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
    def dijkstra(self:   Self,
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

#####################################################################################################################################################

    def distance_matrice(self, initial_location, cheese_location, graph):
        
        distance = {}
        for s1 in cheese_location:
            distance[s1] = self.dijkstra(graph, initial_location)[0][s1]          
        return distance

    def all_routing(self,graph):
        all_routing_table = {}
        for s in graph.vertices:
            all_routing_table[s] = self.dijkstra(graph, s)[1]

        return all_routing_table

    def find_route(self,all_routing, distance_matrice, initial_location, graph):
        """
        Cette fonction trouve le chemin depuis la position initiale jusqu'à la position du fromage
        en utilisant les permutations possibles des points et en minimisant la distance totale.
        """
        matrice = distance_matrice
        all_routing_table = all_routing

        
        mini_L = min((k for k in matrice if matrice[k] != 0), key=lambda k: matrice[k])
        chemin_valide = [initial_location, mini_L]
            
        def rejoin(
                routing_table: Dict[Integral, Optional[Integral]],
                source: Integral,
                target: Integral
                ) -> List[Integral]:
        
            route = []
                
                # Start from the target and backtrack to the source
            current = target
                
            while current is not None:
                route.append(current)
                current = routing_table[current]

                
               
            route.reverse()

            return route

        
        chemin_fini = rejoin(all_routing_table[chemin_valide[0]], chemin_valide[0], chemin_valide[1])

        
        return chemin_fini