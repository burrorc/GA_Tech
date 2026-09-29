import numpy as np

from ArcProblem import ArcProblem
from ArcData import ArcData
from ArcSet import ArcSet


class ArcAgent:
    def __init__(self):
        """
        You may add additional variables to this init method. Be aware that it gets called only once
        and then the make_predictions method will get called several times.
        """
        pass

    def make_predictions(self, arc_problem: ArcProblem) -> list[np.ndarray]:
        """
        Write the code in this method to solve the incoming ArcProblem.
        Your agent will receive 1 problem at a time.

        You can add up to THREE (3) the predictions to the
        predictions list provided below that you need to
        return at the end of this method.

        In the Autograder, the test data output in the arc problem will be set to None
        so your agent cannot peek at the answer (even on the public problems).

        Also, if you return more than 3 predictions in the list it
        is considered an ERROR and the test will be automatically
        marked as INCORRECT.
        """

        # predictions: list[np.ndarray] = [
        #     np.array([[0, 0, 5], [0, 0, 5], [0, 5, 0]])
        # ]

        predictions: list[np.ndarray] = []

        training_sets = arc_problem.training_set()

        target_problem = "1cf80156"
        target_training_sets = {1, 2, 3}     

        count = 1

        for training_set in training_sets:
            input_grid = training_set.get_input_data().data()
            output_grid = training_set.get_output_data().data()

            input_grid_analysis = self.analyze_grid(input_grid)
            output_grid_analysis = self.analyze_grid(output_grid)
            input_shapes = self.identify_shapes(input_grid)
            output_shapes = self.identify_shapes(output_grid)
            
            if (
                arc_problem.problem_name() == target_problem
                and count in target_training_sets
            ):
                print(f"\nPROBLEM: {arc_problem.problem_name()}")
                print(f"Training Set {count}")

                for shape in input_shapes:
                    print(
                        "Input:",
                        "id =", shape["id"],
                        "color =", shape["color"],
                        "top =", shape["top"],
                        "bottom =", shape["bottom"],
                        "left =", shape["left"],
                        "right =", shape["right"],
                        "height =", shape["height"],
                        "width =", shape["width"]
                    )

                for shape in output_shapes:
                    print(
                        "Output:",
                        "id =", shape["id"],
                        "color =", shape["color"],
                        "top =", shape["top"],
                        "bottom =", shape["bottom"],
                        "left =", shape["left"],
                        "right =", shape["right"],
                        "height =", shape["height"],
                        "width =", shape["width"]
                    )

            count += 1


        '''
        The next 2 lines are only an example of how to populate the predictions list.
        This will just be an empty answer the size of the input data;
        delete it before you start adding your own predictions.
        '''
        output = np.zeros_like(arc_problem.test_set().get_input_data().data())
        predictions.append(output)

        return predictions

    def identify_shapes(self, grid: np.ndarray) -> list[dict]:

        shapes = []
        visited_cells = set()
        shape_id = 1

        connection_points = [(-1,-1), (-1,0), (-1,1),
                             (0,-1), (0,1),
                             (1,-1), (1,0), (1,1)]

        for row in range(grid.shape[0]):
            for column in range(grid.shape[1]):
                if(grid[row,column] == 0):
                    continue
                elif(row,column) in visited_cells:
                    continue

                color = grid[row,column].item()

                cells = []
                connection_stack = [(row,column)]
                visited_cells.add((row,column))

                while connection_stack:
                    current_cell = connection_stack.pop()
                    cells.append(current_cell)

                    for row_shift, column_shift in connection_points:
                        
                        adjacent_row = current_cell[0] + row_shift
                        adjacent_column = current_cell[1] + column_shift
                        adjacent_cell = (adjacent_row, adjacent_column)

                        if(adjacent_row < 0 or adjacent_row >= grid.shape[0] or adjacent_column < 0 or adjacent_column >= grid.shape[1]):
                            continue
                        elif(adjacent_cell) in visited_cells:
                            continue
                        elif grid[adjacent_row,adjacent_column] != color:
                            continue

                        visited_cells.add(adjacent_cell)
                        connection_stack.append(adjacent_cell)

                boundaries = self.get_shape_boundaries(cells)
                shapes.append({"id": shape_id, "color": color, "cells": cells, 
                               "top": boundaries["top"], "bottom":boundaries["bottom"], 
                               "left":boundaries["left"], "right": boundaries["right"], 
                               "height": boundaries["height"], "width": boundaries["width"]})

                shape_id +=1
        return shapes

    def get_shape_boundaries(self, cells: list[tuple[int, int]]) -> dict:
        rows =  [cell[0] for cell in cells]
        columns = [cell[1] for cell in cells]

        top = min(rows)
        bottom = max(rows)
        left = min(columns)
        right = max(columns)
        height = bottom-top+1
        width = right-left+1

        return{"top": top, "bottom":bottom, "left": left, "right": right, "height": height, "width": width}



    def analyze_grid(self, grid: np.ndarray) -> dict:
        colors, counts = np.unique(grid, return_counts=True)

        colors_list = colors.tolist()
        counts_list = counts.tolist()

        color_counts= dict(zip(colors_list, counts_list))

        full_rows = []
        full_columns = []

        for row in range(grid.shape[0]):
            current_row = grid[row]

            if np.all(current_row == current_row[0]):
                full_rows.append({"index": row, "color": current_row[0].item()})

        for column in range(grid.shape[1]):
            current_column = grid[:, column]

            if np.all(current_column == current_column[0]):
                full_columns.append({"index": column, "color": current_column[0].item()})

        corners = {
            "top_left": grid[0, 0].item(),
            "top_right": grid[0, -1].item(),
            "bottom_left": grid[-1, 0].item(),
            "bottom_right": grid[-1, -1].item()
        }

        edges = {
            "top": grid[0, :].tolist(),
            "bottom": grid[-1, :].tolist(),
            "left": grid[:, 0].tolist(),
            "right": grid[:, -1].tolist()
        }

        return {
            "height": grid.shape[0],
            "width": grid.shape[1],
            "colors": set(int(color) for color in colors),
            "color_counts": color_counts,
            "is_solid": len(colors) == 1,
            "full_rows": full_rows,
            "full_columns": full_columns,
            "corners": corners,
            "edges": edges
        }

    