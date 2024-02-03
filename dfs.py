from undirected_map import get_maps

# Depth First Search

def dfs(tube_dict:dict, start_station:str, end_station:str, reversed:bool=False):
	""" Very simple and naive implementation based on lecture, because simple is good."""

	agenda = [{"current": {"station":start_station}, "previous": None, "cost": 0}]
	# print(agenda)
	explored = {start_station}
	stations_expanded = 0

	while agenda:
		# print("Agenda: ", agenda)
		node = agenda.pop(0)
		node_name = node["current"]["station"]
		print("Node name: ", node_name)
		stations_expanded += 1
		explored.add(node_name)
		print("Explored: ", explored)

		if node_name == end_station:
			print(f"Reached goal! Stations Expanded: {stations_expanded}")
			return stations_expanded, node

		child_nodes = tube_dict[node_name]
		for child in child_nodes:
			station, cost = child
			if station not in explored:
				agenda.insert(0, {"current": {"station": station},
		                    "indv_cost": cost, "previous": node})
			explored.add(station)
	return None, None


if __name__ == "__main__":
	# Load graph
	station_dict, zone_dict = get_maps()

	# Run search
	stations_expanded, node = dfs(tube_dict=station_dict, start_station="Wembley Central", end_station="Harrow & Wealdstone")
	print(f"Stations Expanded: {stations_expanded}")
	print("Node traceback: ", node)



