# Coursework 1
# Michael Peres
# 29/10/23
from collections import defaultdict
from typing import Tuple, Any

# Imports

def print_format_route(route: dict):
	""" Print the route from nested dictionary format to a more readable format. We use tube_dict to obtain additional information useful for the user.
		Should print the change of lines when this occurs in path, with use of context.
	"""
	path_list = []
	# print(f"route: {route}")
	while route.get("previous", None) is not None:
		# Obtain route name
		station_name = route["current"]["station"]
		previous_station_name = route["previous"]["current"]["station"]
		station_line = route["current"]["line"]
		path_cost = route["indv_cost"]
		# tube_line = route["current"]["station"][station_name]["line"]

		path_list.append((previous_station_name, path_cost, station_line, station_name))
		route = route["previous"]
	station_name = route["current"]["station"]
	path_list.append((None, route.get("indv_cost", 0), route["current"]["line"], route["current"]["station"]))  # Last station

	total_cost = 0
	# print(f"Route: {path_list[::-1]}")

	for index, path in enumerate(path_list[::-1]):
		#print("path:", path)
		if index == 0:
			print(f"Start at {path[3]}.")
		else:
			if path[2] != path_list[::-1][index-1][2] and index > 1:
				print(f"Change from {path_list[::-1][index-1][2]} to {path[2]} at {path_list[::-1][index-1][3]}.")

			print(f"Take [{path[2]}] line from {path[0]} to {path[3]} | Cost ({path[1]}).")
			total_cost += path[1]  # Add cost to total cost.
	print(f"Total Cost: {total_cost}")

# The problem is with the line for each station given, when in fact each station can handle more than one line at a time.
