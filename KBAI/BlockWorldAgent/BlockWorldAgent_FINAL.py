class BlockWorldAgent:
	def __init__(self):
		#If you want to do any initial processing, add it here.
		pass

	def solve(self, initial_arrangement, goal_arrangement):
		#Add your code here! Your solve method should receive
		#as input two arrangements of blocks. The arrangements
		#will be given as lists of lists. The first item in each
		#list will be the bottom block on a stack, proceeding
		#upward. For example, this arrangement:
		#
		#[["A", "B", "C"], ["D", "E"]]
		#
		#...represents two stacks of blocks: one with B on top
		#of A and C on top of B, and one with E on top of D.
		#
		#Your goal is to return a list of moves that will convert
		#the initial arrangement into the goal arrangement.
		#Moves should be represented as 2-tuples where the first
		#item in the 2-tuple is what block to move, and the
		#second item is where to put it: either on top of another
		#block or on the table (represented by the string "Table").
		#
		#For example, these moves would represent moving block B
		#from the first stack to the second stack in the example
		#above:
		#
		#("C", "Table")
		#("B", "E")
		#("C", "A")
		current_stacks = [stack[:] for stack in initial_arrangement]
		moves = []
		seen_stacks = set()
		block_bases = {}
		blocks_in_position = set()
		
		starting_stacks = tuple(sorted(tuple(stack) for stack in current_stacks))
		seen_stacks.add(starting_stacks)

		for stack in goal_arrangement:
			for i in range(len(stack)):
				if(i == 0):
					block_bases[stack[i]] = "Table"
				else:
					block_bases[stack[i]] = stack[i - 1]

		self.get_blocks_in_position(current_stacks, block_bases, blocks_in_position)

		while len(blocks_in_position) < len(block_bases):
			movable_blocks = self.get_movable_blocks(current_stacks, blocks_in_position)
			quick_win_move = self.get_first_single_move_win(
				current_stacks, movable_blocks, block_bases, blocks_in_position
			)
			if (quick_win_move is not None):
				self.apply_move(current_stacks, quick_win_move)
				moves.append(quick_win_move)
				blocks_in_position.add(quick_win_move[0])
				new_stacks = tuple(sorted(tuple(stack) for stack in current_stacks))
				seen_stacks.add(new_stacks)
			else:
				blocks_above_map = self.get_blocks_above(current_stacks)
				
				position_costs = self.get_position_costs(blocks_above_map, block_bases, blocks_in_position)

				next_best_move = None

				obstacle_moves = set()

				for block in position_costs:

					obstacle_moves.update(self.get_obstacle_moves(block, blocks_above_map, block_bases))
					next_best_move = self.get_progressive_move(current_stacks, obstacle_moves, seen_stacks, block_bases, blocks_in_position)

				if (next_best_move is not None):

					self.apply_move(current_stacks, next_best_move)
					moves.append(next_best_move)

					new_stacks = tuple(sorted(tuple(stack) for stack in current_stacks))
					seen_stacks.add(new_stacks)
				else:
					break
		return moves

	def get_blocks_in_position(self, stacks, block_bases, blocks_in_position):
		for stack in stacks:
			for i in range(len(stack)):
				block = stack[i]
				if (i == 0):
					if (block_bases[block] == "Table"):
						blocks_in_position.add(block)
				elif (block_bases[block] == stack[i - 1] and stack[i - 1] in blocks_in_position):
					blocks_in_position.add(block)


	def get_movable_blocks(self, stacks, blocks_in_position):
		movable_blocks = set()
		for stack in stacks:
			if (stack[-1] not in blocks_in_position):
				movable_blocks.add(stack[-1])
		return movable_blocks


	def get_first_single_move_win(self, stacks, movable_blocks, block_bases, blocks_in_position):
		for block in movable_blocks:
			block_base = block_bases[block]
			if (block_base == "Table"):
				return (block, "Table")
			elif(block_base in blocks_in_position):
				for stack in stacks:
					if (stack[-1] == block_base):
						return (block, block_base)
		return None

	
	def apply_move(self, stacks, move):
		move_to_stack = None
		move_from_stack = None
		for stack in stacks:
			if (stack[-1] == move[0]):
				move_from_stack = stack
			if (move[1] != "Table" and stack[-1] == move[1]):
				move_to_stack = stack
				
		move_from_stack.pop()
		
		if (len(move_from_stack) == 0):
			stacks.remove(move_from_stack)
		
		if (move[1] == "Table"):
			stacks.append([move[0]])
		else:
			move_to_stack.append(move[0])

	
	def get_blocks_above(self, stacks):
		blocks_above_map = {}
		for stack in stacks:
			blocks_above = []
			for block in reversed(stack):
				blocks_above_map[block] = blocks_above.copy()
				blocks_above.append(block)
		return blocks_above_map
	
	
	def get_position_costs(self, blocks_above_map, block_bases, blocks_in_position):
		position_costs = {}
		
		for block in block_bases:
			if (block in blocks_in_position):
				continue
			
			block_base = block_bases[block]
			
			if (block_base == "Table" or block_base in blocks_in_position):
				moves_needed = set(blocks_above_map[block])
				
				if (block_base != "Table"):
					moves_needed.update(blocks_above_map[block_base])
				position_costs[block] = len(moves_needed) + 1
			 
		return position_costs


	def get_obstacle_moves(self, next_target_block, blocks_above_map, block_bases):

		obstacle_moves = set()
		target_obstacles = blocks_above_map[next_target_block]

		if(len(target_obstacles) > 0):
			obstacle_moves.add((target_obstacles[0], "Table"))

		target_base = block_bases[next_target_block]

		if(target_base != "Table"):
			base_obstacle = blocks_above_map[target_base]

			if(len(base_obstacle) > 0):
				obstacle_moves.add((base_obstacle[0], "Table"))

		return obstacle_moves


	def get_progressive_move(self, stacks, obstacle_moves, seen_stacks, block_bases, blocks_in_position):
		best_move = None
		best_move_cost = None

		for move in obstacle_moves:
			temp_stacks = [stack[:] for stack in stacks]

			self.apply_move(temp_stacks, move)

			proposed_stacks = tuple(sorted(tuple(stack) for stack in temp_stacks))

			if (proposed_stacks in seen_stacks):
				continue

			temp_blocks_above_map = self.get_blocks_above(temp_stacks)

			proposed_position_costs = self.get_position_costs(temp_blocks_above_map, block_bases, blocks_in_position)

			proposed_cost = sum(proposed_position_costs.values())

			if (best_move_cost is None or proposed_cost < best_move_cost):
				best_move_cost = proposed_cost
				best_move = move

		return best_move
