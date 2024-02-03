# A Star Search Algorithm is not working, we aim to make this work, so we can use it on
# an offline map of the tube, on our iOS application, for our CV personal projects.

# Michael Peres
# 29/10/23

# For this question 2.4, we need to implement my heuristic Best First Search algorithm, mentioned in Week 4 lecture,
# (not A* Search)

# Potential Heuristics, confirm with lecturer in the lab:
# H1 -> ABS distance between zones from start to end, (not sure if this is admissible). Different zones differences.
# H2 -> Number of minutes on average from station to target station.
# H3 -> Euclidian distance between block of station, that is present in map, this is admissable, as it is always going to be lower than the actual distance. More than one station in a block.
# H4 -> Euclidian distance between station and target station, not sure how to obtain this number.

# Information given. Src: https://madeby.tfl.gov.uk/2019/07/29/tube-trivia-and-facts/
# In the London Underground, the average speed of a train is 33km/h
# Using the length between stations and dividing by 33km/h we can obtain the average time between stations.
# The average distance between stations is 1.5km
# Longest Distance between stations is 6.3km
# Shortest Distance between stations is 0.3km
# The number of stations in this network is 271 (calculated in util.py)

# We could obtain all distances for 271 stations, but this would lead to 73,441 entries, which is a lot of data to store.

# Implementing mapping for heuristics to be implemented in our best first search algorith.
# stations = ['Harrow & Wealdstone', 'Kenton', 'South Kenton', 'North Wembley', 'Wembley Central', 'Stonebridge Park', 'Harlesden', 'Willesden Junction', 'Kensal Green', "Queen's Park", 'Kilburn Park', 'Maida Vale', 'Warwick Avenue', 'Paddington', 'Edgware Road', 'Marylebone', 'Baker Street', "Regent's Park", 'Oxford Circus', 'Piccadilly Circus', 'Charing Cross', 'Embankment', 'Waterloo', 'Lambeth North', 'Elephant & Castle', 'West Ruislip', 'Ruislip Gardens', 'South Ruislip', 'Northolt', 'Greenford', 'Perivale', 'Hanger Lane', 'North Acton', 'Ealing Broadway', 'West Acton', 'East Acton', 'White City', "Shepherd's Bush", 'Holland Park', 'Notting Hill Gate', 'Queensway', 'Lancaster Gate', 'Marble Arch', 'Bond Street', 'Tottenham Court Road', 'Holborn', 'Chancery Lane', "St. Paul's", 'Bank/Monument', 'Liverpool Street', 'Bethnal Green', 'Mile End', 'Stratford', 'Leyton', 'Leytonstone', 'Wanstead', 'Redbridge', 'Gants Hill', 'Newbury Park', 'Barkingside', 'Fairlop', 'Hainault', 'Grange Hill', 'Chigwell', 'Roding Valley', 'Woodford', 'Snaresbrook', 'South Woodford', 'Buckhurst Hill', 'Loughton', 'Debden', 'Theydon Bois', 'Epping', 'Great Portland Street', 'Euston Square', "King's Cross St. Pancras", 'Farringdon', 'Barbican', 'Moorgate', 'Aldgate', 'Tower Hill', 'Cannon Street', 'Mansion House', 'Blackfriars', 'Temple', 'Westminster', "St. James' Park", 'Victoria', 'Sloane Square', 'South Kensington', 'Gloucester Road', 'High Street Kensington', 'Bayswater', 'Ealing Common', 'Acton Town', 'Chiswick Park', 'Turnham Green', 'Wimbledon', 'Wimbledon Park', 'Southfields', 'East Putney', 'Putney Bridge', 'Parsons Green', 'Fulham Broadway', 'West Brompton', "Earls' Court", 'Olympia', 'Richmond', 'Kew Gardens', 'Gunnersbury', 'Stamford Brook', 'Ravenscourt Park', 'Hammersmith', 'Barons Court', 'West Kensington', 'Aldgate East', 'Whitechapel', 'Stepney Green', 'Bow Road', 'Bromley-by-Bow', 'West Ham', 'Plaistow', 'Upton Park', 'East Ham', 'Barking', 'Upney', 'Becontree', 'Dagenham Heathway', 'Dagenham East', 'Elm Park', 'Hornchurch', 'Upminster Bridge', 'Upminster', 'Shoreditch', 'Shadwell', 'Wapping', 'Rotherhithe', 'Canada Water', 'Surrey Quays', 'New Cross Gate', 'New Cross', 'Goldhawk Road', 'Latimer Road', 'Ladbroke Grove', 'Westbourne Park', 'Royal Oak', 'Stanmore', 'Canons Park', 'Queensbury', 'Kingsbury', 'Wembley Park', 'Neasden', 'Dollis Hill', 'Willesden Green', 'Kilburn', 'West Hampstead', 'Finchley Road', 'Swiss Cottage', "St. John's Wood", 'Green Park', 'Southwark', 'London Bridge', 'Bermondsey', 'Canary Wharf', 'North Greenwich', 'Canning Town', 'Preston Road', 'Northwick Park', 'Harrow-on-the-Hill', 'North Harrow', 'Pinner', 'Northwood Hills', 'Northwood', 'Moor Park', 'West Harrow', 'Rayners Lane', 'Eastcote', 'Ruislip Manor', 'Ruislip', 'Ickenham', 'Hillingdon', 'Uxbridge', 'Croxley', 'Watford', 'Rickmansworth', 'Chorleywood', 'Chalfont & Latimer', 'Chesham', 'Amersham', 'Mill Hill East', 'Finchley Central', 'High Barnet', 'Totteridge & Whetstone', 'Woodside Park', 'West Finchley', 'East Finchley', 'Highgate', 'Archway', 'Tufnell Park', 'Kentish Town', 'Camden Town', 'Edgware', 'Burnt Oak', 'Colindale', 'Hendon Central', 'Brent Cross', 'Golders Green', 'Hampstead', 'Belsize Park', 'Chalk Farm', 'Mornington Crescent', 'Euston', 'Warren Street', 'Goodge Street', 'Leicester Square', 'Kennington', 'Angel', 'Old Street', 'Borough', 'Oval', 'Stockwell', 'Clapham North', 'Clapham Common', 'Clapham South', 'Balham', 'Tooting Bec', 'Tooting Broadway', 'Colliers Wood', 'South Wimbledon', 'Morden', 'Cockfosters', 'Oakwood', 'Southgate', 'Arnos Grove', 'Bounds Green', 'Wood Green', 'Turnpike Lane', 'Manor House', 'Finsbury Park', 'Arsenal', 'Holloway Road', 'Caledonian Road', 'Russell Square', 'Covent Garden', 'Hyde Park Corner', 'Knightsbridge', 'South Ealing', 'Northfields', 'Boston Manor', 'Osterley', 'Hounslow East', 'Hounslow Central', 'Hounslow West', 'Hatton Cross', 'Heathrow Terminal 3', 'Heathrow Terminal 4', 'Heathrow Terminals 1-2-3', 'North Ealing', 'Park Royal', 'Alperton', 'Sudbury Town', 'Sudbury Hill', 'South Harrow', 'Walthamstow Central', 'Blackhorse Road', 'Tottenham Hale', 'Seven Sisters', 'Highbury & Islington', 'Pimlico', 'Vauxhall', 'Brixton']
# heuristic_three_coord = {}
# for station in stations:
#     coord = input("Enter the coordinates for " + station + ": ")
#     heuristic_three_coord[station] = coord
#
#
# print(heuristic_three_coord)

# Imports
from utils import load_graph_from_dict, print_format_route
from undirected_map import obtain_station_data
import networkx as nx
from math import sqrt

# for line in s.splitlines():
#     #obtain station name by the format of "Enter the coordinates for <station name>: <coordinates>"
#
#     # station_name may have spaces
#     station_name = line.split(":")[0].split("Enter the coordinates for ")[1].strip()
#
#     #obtain coordinates by the format of "Enter the coordinates for <station name>: <coordinates>"
#     coordinates = line.split(":")[1].strip()
#     heuristic_three_coord[station_name] = coordinates
#
# print(heuristic_three_coord)


heuristic_three_coord = {'Harrow & Wealdstone': '3B', 'Kenton': '3B', 'South Kenton': '3B', 'North Wembley': '3B', 'Wembley Central': '3B', 'Stonebridge Park': '3B', 'Harlesden': '3B', 'Willesden Junction': '3B', 'Kensal Green': '3C', "Queen's Park": '3C', 'Kilburn Park': '3C', 'Maida Vale': '3C', 'Warwick Avenue': '3C', 'Paddington': '3C', 'Edgware Road': '4C', 'Marylebone': '4C', 'Baker Street': '4C', "Regent's Park": '4C', 'Oxford Circus': '4C', 'Piccadilly Circus': '4D', 'Charing Cross': '5D', 'Embankment': '5D', 'Waterloo': '5D', 'Lambeth North': '5E5', 'Elephant & Castle': '5E', 'West Ruislip': '1A', 'Ruislip Gardens': '1B', 'South Ruislip': '1B', 'Northolt': '1B', 'Greenford': '1C', 'Perivale': '2C', 'Hanger Lane': '2C', 'North Acton': '3D', 'Ealing Broadway': '2D', 'West Acton': '2D', 'East Acton': '3D', 'White City': '3D', "Shepherd's Bush": '3D', 'Holland Park': '3D', 'Notting Hill Gate': '3D', 'Queensway': '4D', 'Lancaster Gate': '4D', 'Marble Arch': '4C', 'Bond Street': '4C', 'Tottenham Court Road': '5C', 'Holborn': '5C', 'Chancery Lane': '5C', "St. Paul's": '5D', 'Bank/Monument': '6D', 'Liverpool Street': '6C', 'Bethnal Green': '7C', 'Mile End': '7C', 'Stratford': '8C', 'Leyton': '8B', 'Leytonstone': '8B', 'Wanstead': '8B', 'Redbridge': '8B', 'Gants Hill': '8B', 'Newbury Park': '8B', 'Barkingside': '8B', 'Fairlop': '8A', 'Hainault': '8A', 'Grange Hill': '8A', 'Chigwell': '8A', 'Roding Valley': '8A', 'Woodford': '8A', 'Snaresbrook': '8B', 'South Woodford': '8B', 'Buckhurst Hill': '8A', 'Loughton': '8A', 'Debden': '8A', 'Theydon Bois': '8A', 'Epping': '8A', 'Great Portland Street': '4C', 'Euston Square': '5C', "King's Cross St. Pancras": '5C', 'Farringdon': '5C', 'Barbican': '6C', 'Moorgate': '6C', 'Aldgate': '6D', 'Tower Hill': '6D', 'Cannon Street': '6D', 'Mansion House': '5D', 'Blackfriars': '5D', 'Temple': '5D', 'Westminster': '5D', "St. James' Park": '4D', 'Victoria': '4D', 'Sloane Square': '4D', 'South Kensington': '4D', 'Gloucester Road': '4D', 'High Street Kensington': '3D', 'Bayswater': '3C', 'Ealing Common': '2D', 'Acton Town': '2D', 'Chiswick Park': '2D', 'Turnham Green': '2D', 'Wimbledon': '3E', 'Wimbledon Park': '3E', 'Southfields': '3E', 'East Putney': '3E', 'Putney Bridge': '3E', 'Parsons Green': '3E', 'Fulham Broadway': '3E', 'West Brompton': '3D', "Earls' Court": '3D', 'Olympia': '3D', 'Richmond': '2E', 'Kew Gardens': '2E', 'Gunnersbury': '2D', 'Stamford Brook': '2D', 'Ravenscourt Park': '3D', 'Hammersmith': '3D', 'Barons Court': '3D', 'West Kensington': '3D', 'Aldgate East': '6C', 'Whitechapel': '7C', 'Stepney Green': '7C', 'Bow Road': '7C', 'Bromley-by-Bow': '8C', 'West Ham': '8C', 'Plaistow': '8C', 'Upton Park': '8C', 'East Ham': '8C', 'Barking': '8C', 'Upney': '8C', 'Becontree': '9C', 'Dagenham Heathway': '9B', 'Dagenham East': '9B', 'Elm Park': '9B', 'Hornchurch': '9B', 'Upminster Bridge': '9B', 'Upminster': '9B', 'Shoreditch': '7C', 'Shadwell': '7D', 'Wapping': '7D', 'Rotherhithe': '7D', 'Canada Water': '7D', 'Surrey Quays': '7D', 'New Cross Gate': '7E', 'New Cross': '7E', 'Goldhawk Road': '3D', 'Latimer Road': '3C', 'Ladbroke Grove': '3C', 'Westbourne Park': '3C', 'Royal Oak': '3C', 'Stanmore': '3A', 'Canons Park': '3B', 'Queensbury': '3B', 'Kingsbury': '3B', 'Wembley Park': '3B', 'Neasden': '3B', 'Dollis Hill': '3B', 'Willesden Green': '4B', 'Kilburn': '4B', 'West Hampstead': '4B', 'Finchley Road': '4B', 'Swiss Cottage': '4C', "St. John's Wood": '4C', 'Green Park': '4D', 'Southwark': '5D', 'London Bridge': '6D', 'Bermondsey': '6D', 'Canary Wharf': '7D', 'North Greenwich': '8D', 'Canning Town': '8D', 'Preston Road': '3B', 'Northwick Park': '3B', 'Harrow-on-the-Hill': '2B', 'North Harrow': '2B', 'Pinner': '2B', 'Northwood Hills': '2A', 'Northwood': '2A', 'Moor Park': '2A', 'West Harrow': '2B', 'Rayners Lane': '2B', 'Eastcote': '2B', 'Ruislip Manor': '2B', 'Ruislip': '1B', 'Ickenham': '1B', 'Hillingdon': '1A', 'Uxbridge': '1A', 'Croxley': '2A', 'Watford': '2A', 'Rickmansworth': '2A', 'Chorleywood': '2A', 'Chalfont & Latimer': '1A', 'Chesham': '1A', 'Amersham': '1A', 'Mill Hill East': '5A', 'Finchley Central': '5A', 'High Barnet': '5A', 'Totteridge & Whetstone': '5A', 'Woodside Park': '5A', 'West Finchley': '5A', 'East Finchley': '5B', 'Highgate': '5B', 'Archway': '5B', 'Tufnell Park': '5B', 'Kentish Town': '5B', 'Camden Town': '5B', 'Edgware': '4A', 'Burnt Oak': '4A', 'Colindale': '4A', 'Hendon Central': '4B', 'Brent Cross': '4B', 'Golders Green': '4B', 'Hampstead': '5B', 'Belsize Park': '5B', 'Chalk Farm': '5B', 'Mornington Crescent': '5C', 'Euston': '5C', 'Warren Street': '5C', 'Goodge Street': '5C', 'Leicester Square': '5D', 'Kennington': '5E', 'Angel': '6C', 'Old Street': '6C', 'Borough': '5E', 'Oval': '5E', 'Stockwell': '5E', 'Clapham North': '4E', 'Clapham Common': '4F', 'Clapham South': '4F', 'Balham': '4F', 'Tooting Bec': '4F', 'Tooting Broadway': '4F', 'Colliers Wood': '4F', 'South Wimbledon': '4F', 'Morden': '4F', 'Cockfosters': '6A', 'Oakwood': '6A', 'Southgate': '6A', 'Arnos Grove': '6A', 'Bounds Green': '6A', 'Wood Green': '6A', 'Turnpike Lane': '6B', 'Manor House': '6B', 'Finsbury Park': '6B', 'Arsenal': '6B', 'Holloway Road': '6B', 'Caledonian Road': '6B', 'Russell Square': '5C', 'Covent Garden': '5D', 'Hyde Park Corner': '4D', 'Knightsbridge': '4D', 'South Ealing': '2D', 'Northfields': '2D', 'Boston Manor': '2D', 'Osterley': '2D', 'Hounslow East': '1D', 'Hounslow Central': '1D', 'Hounslow West': '1D', 'Hatton Cross': '1E', 'Heathrow Terminal 3': '1E', 'Heathrow Terminal 4': '1E', 'Heathrow Terminals 1-2-3': '1E', 'North Ealing': '2C', 'Park Royal': '2C', 'Alperton': '2C', 'Sudbury Town': '2B', 'Sudbury Hill': '2B', 'South Harrow': '2B', 'Walthamstow Central': '7B', 'Blackhorse Road': '7B', 'Tottenham Hale': '7B', 'Seven Sisters': '6B', 'Highbury & Islington': '6B', 'Pimlico': '4E', 'Vauxhall': '4E', 'Brixton': '5F'}


def h(current_state, goal_state):
    """Heuristic function that obtains estimate cost for given current state to goal state based on grid squares defined on tube map."""
    # Based on grid system, column x row format. Eucledian distance.
    # Admissable number of stops within a specific grid block is 3.

    current_state = heuristic_three_coord[current_state]
    goal_state = heuristic_three_coord[goal_state]  # Oxford Circus: '4C'
    # Handling column
    char_int_mapping = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7}

    try:
        current_column = int(current_state[0])
        goal_column = int(goal_state[0])
    except:
        print("current state: ", current_state)
        raise ValueError("Error with current state")
    current_row = char_int_mapping[current_state[1]]
    goal_row = char_int_mapping[goal_state[1]]

    # Calculate euclidean distance with column and row value.
    euc_cost = sqrt((goal_row-current_row)**2 + (goal_column- current_column)**2)
    return euc_cost


def test_hueristic_three():
    h_cost = h(current_state="Harlesden", goal_state="Oxford Circus")
    print(f"H cost for Harlesden when target is Oxford Circus: {h_cost}")

    h_cost = h(current_state="Marylebone", goal_state="Oxford Circus")
    print(f"H cost for Marylebone when target is Oxford Circus: {h_cost} should be less than initial")

    h_cost = h(current_state="West Hampstead", goal_state="Oxford Circus")
    print(f"H cost for West Hampstead when target is Oxford Circus: {h_cost} should be less than initial")

    print("This confirms that heuristic cost is working.")

def best_first_search(network_graph: nx.Graph, tube_dict:dict, start_station: str, end_station: str):
    """ Runs best first search based on heuristic three which is composed of grid calculations"""

    agenda = [{"current": {"station": {
        start_station: {"line": None, "zone": tube_dict[start_station]["zone"]}}},
        "previous": None, "cost": 0}]
    explored = {start_station}
    stations_expanded = 0
    while agenda:

        agenda = sorted(agenda, key=lambda x: x["cost"], reverse=True)
        print(f"agenda: {[(elem['current']['station'], elem['cost']) for elem in agenda]}")
        node = agenda.pop()
        print(f"frontier {print_format_route(node)}")
        node_name = next(iter(node["current"]["station"]))
        print(f"Node chosen: {node_name}")
        parent_line = node["current"]["station"][node_name].get("line", None)
        stations_expanded += 1
        explored.add(node_name)
        if node_name == end_station:
            print(f"Reached goal! Stations Expanded: {stations_expanded}")
            return node

        # Add children to the agenda
        child_nodes = list(network_graph[node_name]) if not reversed else list(network_graph[node_name])[::-1]
        for child in child_nodes:
            if child not in explored and child != node_name:
                cost = h(current_state=child, goal_state=end_station)
                # Here we check if child node is on the same line as the parent node.
                # Extension adds 2 lines, not sure whether this is worth 10% of CW...

                line, true_path_cost = tube_dict[node_name]["paths"][child][0]
                cost += true_path_cost  # considering the cost of the path also.
                if line != parent_line and parent_line != None:
                    print(f"Line has changed additional cost added.  {line}, {parent_line}")
                    cost += 2.5  # add 2 minutes for transfer.

                print(f"Child: {child} | Huersitic Cost: {cost} | Path Cost: {node['cost']}")
                total_cost = cost + node["cost"]

                agenda.insert(0, {"current": {
                    "station": {child: {"line":line, "zone": tube_dict[child]["zone"]}}},
                                  "previous": node, "indv_cost": cost, "cost": total_cost})
                explored.add(child)
    return None


# Testing heuristic cost
if __name__ == "__main__":
    # Load graph
    tube_dict = obtain_station_data('tubedata.csv')
    tube_graph = load_graph_from_dict(tube_dict, visible=False)

    # Run Best First Search Algorithm between given stations.
    # route = best_first_search(tube_graph, tube_dict, 'Mile End', 'Ealing Broadway')
    # print_format_route(route)
    route = best_first_search(tube_graph, tube_dict, 'Harlesden', 'Mile End')
    print_format_route(route)

    # route = best_first_search(tube_graph, tube_dict, 'Mile End', 'Harlesden')
    # print_format_route(route)
    #
    # # Root node used is Northwood
    # route = best_first_search(tube_graph, tube_dict, 'Northwood', 'East Ham')
    # print_format_route(route)



#Error:
# Because Stratford has been assigned as Central line,
# West Ham,Stratford,Jubilee,3,3,0, this is classed as transfer from west ham to stratfod via Central line but in fact Jubilee.
# Should check previous line used.