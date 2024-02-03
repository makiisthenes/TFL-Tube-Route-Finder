from undirected_map import get_maps, get_lined_maps
from utils import print_format_route

# Exclusive Uniform Cost Search

def ex_ucs(tube_dict:dict, start_station:str, end_station:str, reversed:bool=False):
	"""Simple is better always."""
	agenda = [{"cost": 0, "current": {"station":start_station, "line": None}, "indv_cost": 0, "path": None}]

	explored = {start_station}
	stations_expanded = 0

	while agenda:
		# print("Agenda: ", agenda)
		node = agenda.pop(0)
		node_name = node["current"]["station"]
		if node_name == end_station:
			print(f"Reached goal! Stations Expanded: {stations_expanded}")
			return stations_expanded, node
		node_cost = node["cost"]
		node_line = node["current"]["line"]
		#print("Node name: ", node_name)
		stations_expanded += 1
		explored.add(node_name)
		#print("Explored: ", explored)


		child_nodes = tube_dict[node_name]
		set_child_nodes = []
		line_info = []
		for child in child_nodes:
			station, cost, child_line = child
			if station not in explored:
				# Check if tube line is the same as parent, if not then cost += 2
				if node_line != child_line and node_line is not None:
					cost += 2
				total = node_cost + cost
				entry = (station, cost, total)
				if entry not in set_child_nodes:
					set_child_nodes.append(entry)
					line_info.append(child_line)

		for index, child in enumerate(set_child_nodes):
			station, cost, total = child

			agenda.append({"cost": total, "current": {"station": station, "line": line_info[index]},  "indv_cost": cost, "previous": node })
			explored.add(station)

		agenda.sort(key=lambda x: x["cost"])
	return None, None


if __name__ == "__main__":
	# Load graph
	station_dict, _ = get_lined_maps()

	# Run search
	stations_expanded, node = ex_ucs(tube_dict=station_dict, start_station="Ealing Broadway", end_station="South Kensington")
	print_format_route(node)
	print(f"Stations Expanded: {stations_expanded}")
	#print("Node traceback: ", node)