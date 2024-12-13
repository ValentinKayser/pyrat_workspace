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

class Exhaustive (Player):

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
        
        # Get the location of the cheese
        cheese_location = game_state.cheese

        matrice =  self.distance_matrix(initial_location, cheese_location, maze)

        # Find the route from the initial location to the cheese location

        route = self.find_route(matrice, maze, initial_location)


        # Convert the route to actions using maze's method
        self.actions = maze.locations_to_actions(route)

        # Optional: Print the computed actions for debugging




    


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

    def distance_matrix(self, initial_location, cheese_location, graph):

        sources = [initial_location] + cheese_location
        distance = {}
        for s1 in sources:
            distance[s1] = {}
            temp = self.dijkstra(graph, s1)[0]
            for s2 in sources:
                distance[s1][s2] = temp[s2]
        return distance



    def find_route(self, matrice, graph, initial_location):
        """
        Cette fonction trouve le chemin depuis la position initiale jusqu'à la position du fromage
        en utilisant les permutations possibles des points et en minimisant la distance totale.
        """
        all_routing_table = {}
        for s in graph.vertices:
            all_routing_table[s] = self.dijkstra(graph, s)[1]

        
        # Création de la liste des points
        S = []
        for s1 in matrice:
            S.append(s1)

        # Initialisation d'une liste pour stocker les distances des permutations
        Sum_distance = []

        # Calcul des permutations possibles et de leur distance
        S = list(itertools.permutations(S))
        for s in S:
            s_d = 0
            for i in range(len(s) - 1):
                s_d += matrice[s[i]][s[i+1]]
            
            Sum_distance.append([s, s_d])

        # Trier les permutations par la distance totale croissante
        liste_triee = sorted(Sum_distance, key=lambda x: x[1])

        # Recherche du chemin valide qui commence par 'initial_location'
        for path in liste_triee:
            if path[0][0] == initial_location:
                chemin_valide = []
                for a in path[0]:
                    chemin_valide.append(a)
                break  # Une fois le premier chemin valide trouvé, on arrête

        chemin_fini = []
            
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
                current = routing_table[current]  # Move to the parent vertex
                
                # The route is built in reverse, so we need to reverse it
            route.reverse()
                
                # If the source is not in the route (i.e., unreachable), return an empty list
            if route[0] != source:
                return []

            return route

        for s in range(len(chemin_valide) - 1):
            chemin_fini = chemin_fini + rejoin(all_routing_table[chemin_valide[s]], chemin_valide[s], chemin_valide[s+1])
        
        return chemin_fini