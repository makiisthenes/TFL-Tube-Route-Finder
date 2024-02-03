# Numerical ID3 algorithm.
import pandas as pd
import os, math

class Node:
	def __init__(self, name):
		self.name = name
		self.children = []
		self.parent = None

	def add_child(self, child, edge_name):
		self.children.append((child, edge_name))
		child.parent = self

	def __repr__(self):
		return f"Node({self.name})"

	def __str__(self):
		return f"Node({self.name})"


def calc_entropy(fraction:float, print_ans=True):
	if fraction in [0,1]:
		return 0
	ex_frac = 1-fraction
	calculation = -(fraction * math.log2(fraction)) -(ex_frac * math.log2(ex_frac))
	if print_ans:
		print(f"- ({fraction:.3f} * log_2({fraction:.3f}) - ({ex_frac:.3f} * log_2({ex_frac:.3f}) = {calculation: .3f})")
	return calculation


def load_dataset():
	"""Load dataset from csv file into pandas dataframe."""
	df = pd.read_csv('exam_practice_1.csv', delimiter=',', header=0)
	return df


def sort_data(df, column_name):
	"""Sort the data based on the column name, largest on the bottom."""
	df = df.sort_values(by=[column_name], ascending=True)
	return df


def find_threshold_points(df, column_name):
	"""Based on column_name which contains numerical data, go through all rows.
		the label is the last column in the dataframe,
		when this alternates, we have a threshold point, in which the threshold is the average of the two rows specified in the column_name.
	"""
	threshold_points = []
	for i in range(len(df)):
		if i == 0:
			continue
		if df.iloc[i, -1] != df.iloc[i-1, -1]:
			threshold_points.append((df.iloc[i, column_name] + df.iloc[i-1, column_name]) / 2)
	return threshold_points


def perform_numerical_entropy(df, column_name):
	"""We can obtain thresholds of given column name, in which we then can obtain entropy for each threshold, which is:
		Entropy(threshold) = H(dataset) - (number of rows that < threshold / total rows) * H(rows < threshold) - (number of rows that >= threshold / total rows) * H(rows >= threshold)
	"""
	# First obtain entropy of the dataset.
	threshold_entropies = []
	print(f"Calculating H(dataset)", end=' ')
	entropy_dataset = calc_entropy(len(df[df.iloc[:, -1] == 'Yes']) / len(df))  # get entropy of dataset by the fraction of number of Yes / total rows, which is all we need to calculate entropy.
	# Obtain threshold points.
	# find index for column name
	print(f"\nCalculating H({column_name.title()})")
	index = df.columns.get_loc(column_name)
	threshold_points = find_threshold_points(df, index)
	print(f"numerical entropy: Threshold points for {column_name}: {threshold_points}")
	for threshold in threshold_points:
		# Obtain entropy of rows < threshold
		print(f"Calculating H(<{threshold})", end=' ')
		# calculation is done by finding fraction of row with that threshold that are yes or no from label.
		yes_fraction = len(df[(df[column_name] < threshold) & (df.iloc[:, -1] == 'Yes')])
		entropy_rows_lt = calc_entropy(yes_fraction / len(df[df[column_name] < threshold]))
		# entropy_rows_lt = calc_entropy(len(df[df[column_name] < threshold]) / len(df))
		# Obtain entropy of rows >= threshold
		print(f"Calculating H(>={threshold})", end=' ')
		yes_fraction = len(df[(df[column_name] >= threshold) & (df.iloc[:, -1] == 'Yes')])
		entropy_rows_gte = calc_entropy(yes_fraction / len(df[df[column_name] >= threshold]))
		# Obtain entropy of threshold
		entropy_threshold = entropy_dataset - ((len(df[df[column_name] < threshold]) / len(df)) * entropy_rows_lt) - ((len(df[df[column_name] >= threshold]) / len(df)) * entropy_rows_gte)
		threshold_entropies.append(entropy_threshold)
		print(f"Entropy of H({threshold}) =  H(dataset) - ({len(df[df[column_name] < threshold])} / {len(df)}) * H(<{threshold}) - ({len(df[df[column_name] >= threshold])} / {len(df)}) * H(>={threshold}) = {entropy_threshold :.4f} \n")
		# print(f"Entropy of H({threshold}) is {entropy_threshold :.3f} \n")

	print("#" * 40)
	return threshold_entropies


def obtain_all_columns(df, numerical=False):
	"""Obtain all columns in the dataframe, except the last column, which is the label,
	which are only numerical columns or categorical columns only based on parameter.
	Ignore the last column.
	"""
	columns_name = []
	for column in df.columns[:-1]:
		if numerical:
			if df[column].dtype == 'float64' or df[column].dtype == 'int64':
				columns_name.append(column)
		else:
			if df[column].dtype == 'object':
				columns_name.append(column)
	return columns_name


def perform_categorical_entropy(df, column_name:str):
	"""Will do entropy for all categorical columns, or ones specified, and return the entropy for each column."""
	print(f"Calculating H(dataset)", end=' ')
	entropy_dataset = calc_entropy(len(df[df.iloc[:, -1] == 'Yes']) / len(
		df))  # get entropy of dataset by the fraction of number of Yes / total rows, which is all we need to calculate entropy.
	print(f"\nCalculating H({column_name.title()})")
	# Now calculate for given column name.
	column_index = df.columns.get_loc(column_name)
	unique_values = df.iloc[:, column_index].unique()
	total_entropy = 0
	for labels in unique_values:
		# handle labels that may be nan
		print(f"Calculating H({labels})", end=' ')
		if type(labels) == float and math.isnan(labels):
			yes_fraction = len(df[(df[column_name].isna()) & (df.iloc[:, -1] == 'Yes')])
			entropy = calc_entropy(yes_fraction / len(df[df[column_name].isna()]))
			total_entropy += (len(df[(df[column_name].isna())]) / len(df)) * entropy

		else:
			yes_fraction = len(df[(df[column_name] == labels) & (df.iloc[:, -1] == 'Yes')])
			entropy = calc_entropy(yes_fraction / len(df[df[column_name] == labels]))
			total_entropy += (len(df[df[column_name] == labels]) / len(df)) * entropy

		print(f"Entropy of H({labels}) = {entropy :.3f}")

	information_gain = entropy_dataset - total_entropy

	print(f"Gain(S, {column_name.title()}) = H(S) - ", end='')
	[print(f"({len(df[df[column_name] == labels])} / {len(df)}) * H({labels}) + ", end='') for labels in unique_values]
	print(f" = {information_gain :.3f}")
	print("#" * 40)
	return information_gain


def recursive_id3(df):
	""" Would be nice to have, but not necessary, we only needed it to work semi-automatically, we can do rest manually for now."""

	numerical_columns = obtain_all_columns(df, numerical=True)
	categorical_columns = obtain_all_columns(df, numerical=False)
	node_entropies = {}  # Column name: entropy.
	entropy_dataset = calc_entropy(len(df[df.iloc[:, -1] == 'Yes']) / len(df))
	for num_column_name in numerical_columns:
		# should not obtain new threshold points, should use the ones from the parent node. fix this part of the code.
		df = sort_data(df, num_column_name)
		threshold_points = find_threshold_points(df, df.columns.get_loc(num_column_name))
		print(f"Threshold points for {num_column_name}: {threshold_points}")
		threshold_entropies = perform_numerical_entropy(df, num_column_name)
		for index, threshold in enumerate(threshold_points):
			node_entropies[f"{num_column_name}_{threshold:.3f}"] = threshold_entropies[index]

	for column in categorical_columns:
		entropy = perform_categorical_entropy(df, column)
		node_entropies[column] = entropy


	print(f"Node entropies: {node_entropies}")
	print(f"Best node to split on: {max(node_entropies, key=node_entropies.get)}")
	print(node_entropies[max(node_entropies, key=node_entropies.get)] == entropy_dataset)

	# if all entropies are 0, then we have a leaf node and should be the value of label, False.
	if all([entropy == 0 for entropy in node_entropies.values()]):
		return Node("False")

	# node name.
	node = Node(max(node_entropies, key=node_entropies.get))


	# Termination Criterion, when to stop recursively, performing entropy calculation.
	if node_entropies[max(node_entropies, key=node_entropies.get)] == entropy_dataset:
		# leaf node.
		# it will be the value of the label present in the dataset, should only be one value.

		node.add_child(Node(str(df.iloc[:, -1].unique()[0])), "True")
		return node
	else:
		# Generate the dataframes based on the best node to split on.
		best_node_name = max(node_entropies, key=node_entropies.get)
		if len(best_node_name.split("_")) > 1:
			# numerical column, need to split on threshold.
			threshold = float(best_node_name.split("_")[1])
			# Split on threshold.
			df_lt = df[df[best_node_name.split("_")[0]] < threshold]
			df_gte = df[df[best_node_name.split("_")[0]] >= threshold]
			distinct_values = [f"<{threshold}", f">={threshold}"]
			dfs = [df_lt, df_gte]
		else:
			# categorical column, need to split on unique values.
			distinct_values = df[best_node_name.split("_")[0]].unique()
			dfs = [df[df[best_node_name] == value] for value in distinct_values]

		for i, df in enumerate(dfs):
			# for each dataframe, we know the edge value, but the node name is the name of the next df run on. (the column name)
			node.add_child(recursive_id3(df), distinct_values[i])

		return node
		# return [recursive_id3(df) for df in dfs]


def visualise_tree_recursive(node, level=0):
	"""
		Visualise the tree recursively, print the node name,
		and the edge name, which is the value of the parent node.
		Plot the tree using graphviz, matplotlib.
	"""
	pass


if __name__ == "__main__":
	df = load_dataset()
	# df = sort_data(df, 'price')
	node = recursive_id3(df)

	exit(0)

	df = sort_data(df, 'price')
	# print(df)


	threshold_points = find_threshold_points(df, 0)
	print(threshold_points)

	numerical_columns = obtain_all_columns(df, numerical=True)
	categorical_columns = obtain_all_columns(df, numerical=False)

	# First iteration.
	# Termination Criterion, when to stop recursively, performing entropy calculation.
	# When entropy is the same as H(S), which is the entropy of the dataset.

	node_entropies = {}  # Column name: entropy.

	for num_column_name in numerical_columns:
		threshold_points = find_threshold_points(df, df.columns.get_loc(num_column_name))
		threshold_entropies = perform_numerical_entropy(df, num_column_name)
		for index, threshold in enumerate(threshold_points):
			node_entropies[f"{num_column_name}_{threshold:.3f}"] = threshold_entropies[index]

	for column in categorical_columns:
		entropy = perform_categorical_entropy(df, column)
		node_entropies[column] = entropy

	# perform_numerical_entropy(df, "price")
	# perform_categorical_entropy(df, 'change')
	# perform_categorical_entropy(df, 'quality')
	# perform_categorical_entropy(df, 'ads')

	print(f"Node entropies: {node_entropies}")
	print(f"Best node to split on: {max(node_entropies, key=node_entropies.get)}")
	# Generate the dataframes based on the best node to split on.
	best_node_name = max(node_entropies, key=node_entropies.get)
	if len(best_node_name.split("_")) > 1:
		# numerical column, need to split on threshold.
		threshold = float(best_node_name.split("_")[1])
		# Split on threshold.
		df_lt = df[df[best_node_name.split("_")[0]] < threshold]
		df_gte = df[df[best_node_name.split("_")[0]] >= threshold]
		distinct_values = [f"<{threshold}", f">={threshold}"]
		dfs = [df_lt, df_gte]
	else:
		# categorical column, need to split on unique values.
		distinct_values = df[best_node_name.split("_")[0]].unique()
		dfs = [df[df[best_node_name] == value] for value in distinct_values]

	print(f"Dataframes {best_node_name} {distinct_values[0]}:\n {dfs[0]}")
	# Recursively perform entropy calculation on dataframes, split by the column name and the unqiue values in that column.
	# Three unique values, three dataframes.


	# testing recursion
	node_entropies = {}  # Column name: entropy.
	df = dfs[0]
	entropy_dataset = calc_entropy(len(df[df.iloc[:, -1] == 'Yes']) / len(df))
	for num_column_name in numerical_columns:
		threshold_points = find_threshold_points(df, df.columns.get_loc(num_column_name))
		threshold_entropies = perform_numerical_entropy(df, num_column_name)
		for index, threshold in enumerate(threshold_points):
			node_entropies[f"{num_column_name}_{threshold:.3f}"] = threshold_entropies[index]

	for column in categorical_columns:
		entropy = perform_categorical_entropy(df, column)
		node_entropies[column] = entropy

	print(f"Node entropies: {node_entropies}")
	print(f"Best node to split on: {max(node_entropies, key=node_entropies.get)}")
	print(node_entropies[max(node_entropies, key=node_entropies.get)] == entropy_dataset)

