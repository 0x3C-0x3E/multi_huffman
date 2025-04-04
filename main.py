import sys, heapq




class TreeNode:
	def __init__(self, node_cost, input_char = ''):
		self.parent_node = []
		self.child_nodes = []
		self.node_cost = node_cost

		self.char = input_char

	def set_parent_node(self, parent_node):
		self.parent_node = parent_node

	def set_child_nodes(self, child_nodes):
		self.child_nodes = child_nodes

	def calculate_node_cost(self):
		for child_node in self.child_nodes:
			self.node_cost += child_node.node_cost

		return self.node_cost

	def get_char(self):
		if self.char == '':
			output = []
			for child_node in self.child_nodes:
				output.append(child_node.get_char())
			return output
		else:
			return self.char


DEBUG = True
PEARL_COUNT = 3

def print_debug(message):
	if not DEBUG:
		return

	print(f"[DEBUG] {message}")


def get_file_contents(file_path):
	lines = []
	with open(file_path, "r") as file:
		lines = file.readlines()

	#remove \n from the file
	for line in lines:
		lines[lines.index(line)] = line.translate({ord('\n'): None})

	return lines

def get_char_probability_dict(lines):

	probability_dict = {}

	for line in lines:
		for char in line:
			if char in probability_dict:
				probability_dict[char] += 1
			else:
				probability_dict[char] = 1

	return probability_dict

def sort_dict_by_value(dictonary, should_reverse = True):

	dictonary = dict(sorted(dictonary.items(), key=lambda x: x[1], reverse=should_reverse))
	return dictonary

def find_n_smallest(input_list, n):
	return heapq.nsmallest(n, input_list, key=lambda node: node.node_cost)

def find_element_path(lst, target, path=None):
    if path is None:
        path = []

    for index, item in enumerate(lst):
        new_path = path + [index]

        if item == target:
            return new_path
        elif isinstance(item, list):
            result = find_element_path(item, target, new_path)
            if result:
                return result

    return None

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("not enough args")
		exit()

	lines = get_file_contents(sys.argv[1])

	sorted_dict = sort_dict_by_value(get_char_probability_dict(lines[2]))

	PEARL_COUNT = int(lines[0])

	print_debug(f"Pearl Count: {PEARL_COUNT}")

	print_debug(f"sorted dict {sorted_dict}")

	tree_nodes = []

	for character, node_cost in sorted_dict.items():
		tree_nodes.append(TreeNode(node_cost, character))

	top_most_nodes = len(sorted_dict)

	while top_most_nodes > 1:
		print_debug("New optimisation phase")

		smallest_cost_nodes = find_n_smallest(tree_nodes, PEARL_COUNT)

		parent_node_cost = 0
		
		for node in smallest_cost_nodes:
			print_debug(f"{node.char}, {node.node_cost}")
			parent_node_cost += node.calculate_node_cost()
		
		parent_node = TreeNode(parent_node_cost)

		for node in smallest_cost_nodes:
			node.set_parent_node(parent_node)

		parent_node.set_child_nodes(smallest_cost_nodes)


		tree_nodes.append(parent_node)

		print_debug(f"Newly generated parent_node: ['{parent_node.char}'], [{parent_node.node_cost}], {parent_node.get_char()}")

		#TODO CHANGE THAT
		top_most_nodes = top_most_nodes - PEARL_COUNT + 1

		if top_most_nodes == 1:
			print_debug("reached root node")
			break

		#remove the unnessesary node (while still not being garbage collected bc of the refrence from parent_node)
		tree_nodes = [node for node in tree_nodes if node not in smallest_cost_nodes]

		#debug statement to check if they werent garbage collected
		for child_node in parent_node.child_nodes:
			print_debug(f"child node of new parent_node: ['{child_node.char}'], [{child_node.node_cost}]")

	translation_dict = {}

	for character in sorted_dict.keys():
		nested_list = parent_node.get_char()
		path = find_element_path(nested_list, character)
		print(f"[RESULT] Character: {character} => {path}")
		translation_dict[character] = path

	for key, value in translation_dict.items():
		print_debug(f"Translation Dict: {key} : {value}")

	message = ''
	message_len = 0
	for character in lines[2]:
		string = ''
		for byte in translation_dict[character]:
			string += str(byte)
		message += string
		message_len += len(translation_dict[character])

	print(f"\n[FINAL] Message => {message}, len => {message_len}")

