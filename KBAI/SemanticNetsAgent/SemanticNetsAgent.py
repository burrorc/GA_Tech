class SemanticNetsAgent:
    def __init__(self):
        #If you want to do any initial processing, add it here.
        pass

    def solve(self, initial_sheep, initial_wolves):
        possible_moves = [(1,0), (0,1), (1,1), (2,0), (0,2)]
        # L/R for boat side, use to determine add/sub
        target_state = (0, 0, 'R')
        initial_state = (initial_sheep, initial_wolves, 'L')
        # just keep track of left side and the boat location
        current_state = initial_state
        seen_states = set((initial_state,))

        process_queue = [(initial_state, [])]

        while process_queue and current_state != target_state:
            current_state, move_history = process_queue.pop(0)
            if current_state == target_state:
                return move_history

            for move in possible_moves:
                if not self.is_allowed_move(current_state, move, initial_state[0], initial_state[1]):
                    continue
                if current_state[2] == 'L':
                    # moving to right, make sure to sub the move values
                    new_state = (current_state[0] - move[0], current_state[1] - move[1], 'R')
                elif current_state[2] == 'R':
                    # moving to left, make sure to add the move values
                    new_state = (current_state[0] + move[0], current_state[1] + move[1], 'L')
                else:
                    continue
                # don't queue already existing states or states not allowed
                if new_state in seen_states or not self.is_allowed_state(new_state, initial_state[0], initial_state[1]):
                    continue
                seen_states.add(new_state)
                new_move_history = move_history+[move]
                process_queue.append((new_state, new_move_history))


        return []

    def is_allowed_move(self, current_state, move, initial_sheep, initial_wolves):
        # prevent moves that cause num less than zero
        if current_state[2] == 'L':
            return current_state[0] - move[0] >= 0 and current_state[1] - move[1] >= 0
        elif current_state[2] == 'R':
            return current_state[0] + move[0] <= initial_sheep and current_state[1] + move[1] <= initial_wolves
        return False

    def is_allowed_state(self, new_state, initial_sheep, initial_wolves):

        left_sheep = new_state[0]
        left_wolves = new_state[1]
        right_sheep = initial_sheep - left_sheep
        right_wolves = initial_wolves - left_wolves
        # prevent neg values
        if (left_sheep < 0 or left_wolves < 0 or right_sheep < 0 or right_wolves < 0):
            return False
        # prevent more wolves than sheep if any sheep
        if (left_wolves > left_sheep and left_sheep > 0):
            return False
        # prevent more wolves than sheep if any sheep
        if (right_wolves > right_sheep and right_sheep > 0):
            return False
        return True

    

