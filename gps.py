import sys
import argparse
#How to run: python your_program.py --starting_city Washington --destination_city Richmond

class City:
    def __init__(self, name):
        """Initialize a City with a given name.
        
        Parameters:
            name (str): The name of the city.
        """
        self.name = name
        self.neighbors = {}  # Storing neighbors by name
        self.visited = False  # Add a visited attribute

    def __repr__(self):
        """Return a string representation of the city, including its name.
        
        Returns:
            str: A string representing the city.
        """
        return self.name

    def add_neighbor(self, neighbor, distance, interstate):
        """Add a neighboring city with distance and interstate information.
        
        Parameters:
            neighbor (City): The neighboring city to be added.
            distance (int): The distance to the neighboring city.
            interstate (str): The interstate highway associated with the connection.
        """
        self.neighbors[neighbor.name] = (distance, interstate)

        # Ensure bidirectional connection by adding the reverse connection in the neighbor
        neighbor.neighbors[self.name] = (distance, interstate)


class Map:
    def __init__(self, relationships):
        """Initialize the map with city relationships.
        
        Parameters:
            relationships (dict): A dictionary mapping city names to a list of tuples,
                                  where each tuple contains a neighbor's name, distance, and interstate.
        """
        self.cities = {}

        for city_name, neighbors in relationships.items():
            if city_name not in self.cities:
                self.cities[city_name] = City(city_name)  # Create a new city if it doesn't exist

            current_city = self.cities[city_name]

            for neighbor_name, distance, interstate in neighbors:
                if neighbor_name not in self.cities:
                    self.cities[neighbor_name] = City(neighbor_name)  # Create the neighbor if it doesn't exist

                neighbor_city = self.cities[neighbor_name]
                current_city.add_neighbor(neighbor_city, distance, interstate)

    def bfs(self, start_name: str, goal_name: str) -> list:
        """Find the shortest path between start and goal using BFS.
        
        Parameters:
            start_name (str): The name of the starting city.
            goal_name (str): The name of the goal city.
        
        Returns:
            list: A list of City objects representing the path from start to goal,
                  or None if no path exists.
        """
        start_city = self.cities.get(start_name)
        goal_city = self.cities.get(goal_name)

        if not start_city or not goal_city:
            return None  # Return None if either city doesn't exist

        if start_city == goal_city:
            return [start_city]  # Return the City object if it's the goal

        queue = [[start_city]]  # Start with the City object in a list
        explored = set()  # Set to track visited cities

        while queue:
            path = queue.pop(0)  # Get the first path from the queue
            city = path[-1]  # Get the last city from the path

            if city.name not in explored:  # Check if the city has not been visited
                explored.add(city.name)  # Mark the city as visited

                # Explore neighbors by name (not by City object)
                for neighbor_name, (distance, highway) in city.neighbors.items():
                    neighbor = self.cities[neighbor_name]
                    new_path = path + [neighbor]
                    if neighbor == goal_city:
                        return new_path  # Return the path of City objects
                    queue.append(new_path)

        return None  # If no path found

    def __repr__(self):
        """Return the string representation of the cities in the map.
        
        Returns:
            str: A string representing the map and its cities.
        """
        return "Map with cities: " + ", ".join(city.name for city in self.cities.values())


def main(start_city, end_city, connections):
    """Find and display the shortest route between two cities.
    
    Parameters:
        start_city (str): The name of the starting city.
        end_city (str): The name of the destination city.
        connections (dict): A dictionary mapping city names to a list of tuples,
                            where each tuple contains a neighbor's name, distance, and interstate.
    """
    city_map = Map(connections)
    path = city_map.bfs(start_city, end_city)  # Call BFS directly on the city_map instance

    if path:
        print(f"Starting at {path[0].name}")
        for i in range(len(path) - 1):
            current, next_city = path[i], path[i + 1]
            distance, highway = current.neighbors[next_city.name]  # Get distance and interstate using name
            print(f"Drive {distance} miles on Interstate {highway} towards {next_city.name}, then")
        print(f"You will arrive at your destination.")
    else:
        print(f"No route found from {start_city} to {end_city}.")


def parse_args(args_list):
    """Takes a list of strings from the command prompt and passes them through as arguments
    
    Args:
        args_list (list) : the list of strings from the command prompt
    Returns:
        args (ArgumentParser)
    """

    parser = argparse.ArgumentParser()
    
    parser.add_argument('--starting_city', type=str, help='The starting city in a route.')
    parser.add_argument('--destination_city', type=str, help='The destination city in a route.')
    
    args = parser.parse_args(args_list)
    
    return args


if __name__ == "__main__":
    connections = {  
        "Baltimore": [("Washington", 39, "95"), ("Philadelphia", 106, "95")],
        "Washington": [("Baltimore", 39, "95"), ("Fredericksburg", 53, "95"), ("Bedford", 137, "70"), ("Philadelphia", 139, "95")],
        "Fredericksburg": [("Washington", 53, "95"), ("Richmond", 60, "95")],
        "Richmond": [("Charlottesville", 71, "64"), ("Williamsburg", 51, "64"), ("Durham", 151, "85"), ("Fredericksburg", 60, "95"), ("Raleigh", 171, "95")],
        "Durham": [("Richmond", 151, "85"), ("Raleigh", 29, "40"), ("Greensboro", 54, "40")],
        "Raleigh": [("Durham", 29, "40"), ("Wilmington", 129, "40"), ("Richmond", 171, "95")],
        "Greensboro": [("Charlotte", 92, "85"), ("Durham", 54, "40"), ("Ashville", 173, "40")],
        "Ashville": [("Greensboro", 173, "40"), ("Charlotte", 130, "40"), ("Knoxville", 116, "40"), ("Atlanta", 208, "85")],
        "Charlotte": [("Atlanta", 245, "85"), ("Ashville", 130, "40"), ("Greensboro", 92, "85")],
        "Jacksonville": [("Atlanta", 346, "75"), ("Tallahassee", 164, "10"), ("Daytona Beach", 86, "95")],
        "Daytona Beach": [("Orlando", 56, "4"), ("Miami", 95, "268"), ("Jacksonville", 86, "95")],
        "Orlando": [("Tampa", 94, "4"), ("Daytona Beach", 56, "4")],
        "Tampa": [("Miami", 281, "75"), ("Orlando", 94, "4"), ("Atlanta", 456, "75"), ("Tallahassee", 243, "98")],
        "Atlanta": [("Charlotte", 245, "85"), ("Ashville", 208, "85"), ("Chattanooga", 118, "75"), ("Macon", 83, "75"), ("Tampa", 456, "75"), ("Jacksonville", 346, "75"), ("Tallahassee", 273, "27")],
        "Chattanooga": [("Atlanta", 118, "75"), ("Knoxville", 112, "75"), ("Nashville", 134, "24"), ("Birmingham", 148, "59")],
        "Knoxville": [("Chattanooga", 112, "75"), ("Lexington", 172, "75"), ("Nashville", 180, "40"), ("Ashville", 116, "40")],
        "Nashville": [("Knoxville", 180, "40"), ("Chattanooga", 134, "24"), ("Birmingam", 191, "65"), ("Memphis", 212, "40"), ("Louisville", 176, "65")],
        "Louisville": [("Nashville", 176, "65"), ("Cincinnati", 100, "71"), ("Indianapolis", 114, "65"), ("St. Louis", 260, "64"), ("Lexington", 78, "64")],
        "Cincinnati": [("Louisville", 100, "71"), ("Indianapolis", 112, "74"), ("Columbus", 99, "71")],
        "Columbus": [("Cincinnati", 99, "71"), ("Indianapolis", 175, "70"), ("Cleveland", 143, "71")],
        "Indianapolis": [("Columbus", 175, "70"), ("Cincinnati", 112, "74"), ("Louisville", 114, "65"), ("Chicago", 179, "65")],
        "Chicago": [("Indianapolis", 179, "65"), ("Columbus", 143, "71"), ("St. Louis", 291, "55"), ("Detroit", 281, "94")],
        "St. Louis": [("Indianapolis", 261, "65"), ("Louisville", 260, "64"), ("Chicago", 291, "55"), ("Kansas City", 239, "70")],
        "Detroit": [("Chicago", 281, "94"), ("Cleveland", 170, "71"), ("Toledo", 52, "75")],
        "Cleveland": [("Detroit", 170, "71"), ("Columbus", 143, "71")],
    }

    args = parse_args(sys.argv[1:])
    main(args.starting_city, args.destination_city, connections)
