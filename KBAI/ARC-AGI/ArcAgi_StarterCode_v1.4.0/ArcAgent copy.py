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

        target_problem = "0520fde7"
        target_training_sets = {1, 2, 3}     

        count = 1

        for training_set in training_sets:
            input_grid = training_set.get_input_data().data()
            output_grid = training_set.get_output_data().data()

            input_grid_analysis = self.analyze_grid(input_grid, "input_grid", "full")
            output_grid_analysis = self.analyze_grid(output_grid, "output_grid", "full")
            input_shapes = self.identify_shapes(input_grid, "input_grid")
            output_shapes = self.identify_shapes(output_grid,"output_grid")
            input_relationships = self.get_object_grid_relationships(input_grid, input_shapes)
            output_relationships = self.get_object_grid_relationships(output_grid,output_shapes)
            input_regions = self.get_grid_regions(input_grid, "input_grid",input_shapes,input_relationships)
            output_regions = self.get_grid_regions(output_grid, "output_grid",output_shapes,output_relationships)
            self.get_shape_regions(input_shapes,input_regions)
            self.get_shape_regions(output_shapes,output_regions)
            input_object_relationships = self.get_object_to_object_relationships(input_shapes)
            output_object_relationships = self.get_object_to_object_relationships(output_shapes)
            input_output_object_relationships = self.get_object_to_object_relationships(input_shapes, output_shapes)
            
            if (
                arc_problem.problem_name() == target_problem
                and count in target_training_sets
            ):
                with open("debug_output.txt", "w") as debug_file:
                    print(f"\nPROBLEM: {arc_problem.problem_name()}", file=debug_file)
                    print(f"Training Set {count}", file=debug_file)

                    # self.print_frame(input_grid_analysis, "INPUT GRID", debug_file)
                    # self.print_frame(output_grid_analysis, "OUTPUT GRID", debug_file)

                    # for shape in input_shapes:
                    #     self.print_frame(shape, "INPUT SHAPES", debug_file)

                    # for shape in output_shapes:
                    #     self.print_frame(shape, "OUTPUT SHAPES", debug_file)

                    # for relationship in input_relationships:
                    #     self.print_frame(relationship, "INPUT RELATIONSHIPS", debug_file)

                    # for relationship in output_relationships:
                    #     self.print_frame(relationship, "OUTPUT RELATIONSHIPS", debug_file)

                    # for region in input_regions:
                    #     self.print_frame(region, "INPUT REGION", debug_file)

                    # for region in output_regions:
                    #     self.print_frame(region, "OUTPUT REGION", debug_file)

                    # for relationship in input_object_relationships:
                    #     self.print_frame(relationship, "INPUT OBJECT RELATIONSHIPS", debug_file)

                    # for relationship in output_object_relationships:
                    #     self.print_frame(relationship, "OUTPUT OBJECT RELATIONSHIPS", debug_file)

                    for relationship in input_output_object_relationships:
                        self.print_frame(relationship, "INPUT-OUTPUT OBJECT RELATIONSHIPS", debug_file)


            count += 1


        '''
        The next 2 lines are only an example of how to populate the predictions list.
        This will just be an empty answer the size of the input data;
        delete it before you start adding your own predictions.
        '''
        output = np.zeros_like(arc_problem.test_set().get_input_data().data())
        predictions.append(output)

        return predictions

    def print_frame(self, frame: dict, label: str = "", file=None):

        if label:
            print(label, file=file)

        for key, value in frame.items():
            print(f"{key} = {value}", file=file)
        

    def get_object_to_object_relationships(self, shapes:list[dict], target_shapes: list[dict] = None) -> list[dict]:
        relationships = []
        if target_shapes is None:
            target_shapes = shapes
            same_source = True
        else:
            same_source = False

        for source_shape in shapes:
            for target_shape in target_shapes:

                if (same_source and source_shape["id"] == target_shape["id"]):
                    continue

                position_relationships = self.get_object_object_positions(source_shape, target_shape)
                relationships.extend(position_relationships)

                if same_source:
                    region_relationships = self.get_object_object_regions(source_shape, target_shape)
                    relationships.extend(region_relationships)

                color_relationships = self.get_object_object_colors(source_shape, target_shape)
                relationships.extend(color_relationships)

                shape_relationships = self.get_object_object_shapes(source_shape, target_shape)
                relationships.extend(shape_relationships)

        return relationships

    def get_object_object_shapes(self, source_shape, target_shape):
        shape_relationships =[]
        source_pattern = source_shape["pattern"]
        target_pattern = target_shape["pattern"]
        source_flipped = np.fliplr(source_pattern)

        relationship_degrees = [
            ("same", source_pattern),
            ("rotation_90", np.rot90(source_pattern, 1)),
            ("rotation_180", np.rot90(source_pattern, 2)),
            ("rotation_270", np.rot90(source_pattern, 3)),
            ("flipped_h", source_flipped),
            ("flipped_v", np.flipud(source_pattern)),
            ("flipped_h_rotation_90", np.rot90(source_flipped, 1)),
            ("flipped_h_rotation_270", np.rot90(source_flipped, 3))
        ]

        for degree, transformed in relationship_degrees:
            if(np.array_equal(transformed, target_pattern)):
                shape_relationships.append({
                    "source_item": "object",
                    "source_id": source_shape["id"],
                    "relationship_type": "shape",
                    "relationship_degree": degree,
                    "target_item": "object",
                    "target_id": target_shape["id"]
                })  
                if "same" == degree:
                    return shape_relationships    

        return shape_relationships


    def get_object_object_colors(self, source_shape, target_shape):
        color_relationships = []

        if source_shape["color"] == target_shape["color"]:
            color_relationships.append({
                "source_item": "object",
                "source_id": source_shape["id"],
                "relationship_type": "color",
                "relationship_degree": "same_color",
                "target_item": "object",
                "target_id": target_shape["id"]
            })

        return color_relationships

    def get_object_object_regions(self, source_shape, target_shape):
        region_relationships = []
        if (
            source_shape["region_id"] is not None
            and target_shape["region_id"] is not None
            and source_shape["region_id"] == target_shape["region_id"]
        ):
            region_relationships.append({
                "source_item": "object",
                "source_id": source_shape["id"],
                "relationship_type": "region",
                "relationship_degree": "same_region",
                "target_item": "object",
                "target_id": target_shape["id"]
            })

        return region_relationships
    
    def get_object_object_positions(self, source_shape, target_shape):
        position_relationships = []
        if(source_shape["right"] < target_shape["left"]):
            position_relationships.append({
                "source_item": "object",
                "source_id": source_shape["id"],
                "relationship_type": "position",
                "relationship_degree": "left_of",
                "target_item": "object",
                "target_id": target_shape["id"]
            })

        if(source_shape["left"] > target_shape["right"]):
            position_relationships.append({
                "source_item": "object",
                "source_id": source_shape["id"],
                "relationship_type": "position",
                "relationship_degree": "right_of",
                "target_item": "object",
                "target_id": target_shape["id"]
            })

        if source_shape["bottom"] < target_shape["top"]:
            position_relationships.append({
                "source_item": "object",
                "source_id": source_shape["id"],
                "relationship_type": "position",
                "relationship_degree": "above",
                "target_item": "object",
                "target_id": target_shape["id"]
            })

        if source_shape["top"] > target_shape["bottom"]:
            position_relationships.append({
                "source_item": "object",
                "source_id": source_shape["id"],
                "relationship_type": "position",
                "relationship_degree": "below",
                "target_item": "object",
                "target_id": target_shape["id"]
            })

        return position_relationships

    def get_shape_regions(self, shapes: list[dict], regions:list[dict]):

        for shape in shapes:
            shape["region_id"] = None

            for region in regions:
                contains_shape = (
                    shape["top"] >= region["parent_top"]
                    and shape["bottom"] <= region["parent_bottom"]
                    and shape["left"] >= region["parent_left"]
                    and shape["right"] <= region["parent_right"]
                )

                if contains_shape:
                    shape["region_id"] = region["grid_id"]
                    break


    def get_grid_regions(self, grid: np.ndarray, parent_grid_id: str, shapes: list[dict], relationships: list[dict]) -> list[dict]:
        # TODO figure out how to properly handle cross grid dividers, my dumbass forgot that we're identifying objects by colors
        regions = []
        vertical_dividers = []
        horizontal_dividers = []
        region_number = 1
        for relationship in relationships:
            if(relationship["relationship"] != "divides_grid"):
                continue

            divider = None

            for shape in shapes:
                if(shape["id"] == relationship["source_id"]):
                    divider = shape
                    break

            if divider is None:
                continue

            if (relationship["orientation"] == "vertical"):
                vertical_dividers.append(divider)
            elif(relationship["orientation"] == "horizontal"):
                horizontal_dividers.append(divider)

        if not vertical_dividers and not horizontal_dividers:
            return []

        vertical_dividers.sort(key=lambda shape: shape["left"])
        horizontal_dividers.sort(key=lambda shape: shape["top"])

        row_splits = self.get_row_splits(grid, horizontal_dividers)
        column_splits = self.get_column_splits(grid, vertical_dividers)

        for row_start, row_end in row_splits:
            for column_start,column_end in column_splits:
                region_grid = grid[row_start:row_end+1, column_start:column_end+1]
                region_id = (parent_grid_id+"_region_"+str(region_number))
                regions.append(self.analyze_grid(region_grid, region_id, "region", parent_grid_id, row_start, row_end, column_start, column_end))
                region_number +=1
            
        # if vertical_dividers:
        #     start_column = 0
        #     region_number = 1

        #     for divider in vertical_dividers:
        #         end_column = divider["left"]
        #         region_grid = grid[:, start_column:end_column]

        #         if region_grid.shape[1] > 0:
        #             region_id = parent_grid_id+"_region_"+str(region_number)

        #             regions.append(self.analyze_grid(region_grid, region_id, "region", parent_grid_id, 0, grid.shape[0]-1,start_column, end_column-1))
        #             region_number +=1

        #         start_column = divider["right"]+1

        #     if start_column < grid.shape[1]:
        #         region_grid = grid[:,start_column:]
        #         region_id = region_id = parent_grid_id+"_region_"+str(region_number)
        #         regions.append(self.analyze_grid(region_grid, region_id, "region", parent_grid_id,0, grid.shape[0]-1,start_column, grid.shape[1]-1))

        # if horizontal_dividers:
        #     start_row = 0
        #     region_number = 1

        #     for divider in horizontal_dividers:
        #         end_row = divider["top"]
        #         region_grid = grid[start_row:end_row,:]

        #         if region_grid.shape[0] > 0:
        #             region_id = parent_grid_id+"_region_"+str(region_number)

        #             regions.append(self.analyze_grid(region_grid, region_id, "region", parent_grid_id, start_row, end_row-1, 0, grid.shape[1]-1))
        #             region_number +=1

        #         start_row = divider["bottom"]+1

        #     if start_row < grid.shape[0]:
        #             region_grid = grid[start_row:,:]
        #             region_id = parent_grid_id+"_region_"+str(region_number)
        #             regions.append(self.analyze_grid(region_grid, region_id, "region", parent_grid_id,start_row,grid.shape[0]-1,0,grid.shape[1]-1))

        return regions

    def get_row_splits(self, grid:np.ndarray, horizontal_dividers: list[dict]) -> list[tuple[int,int]]:
        row_splits = []
        start_row = 0

        for divider in horizontal_dividers:
            end_row = divider["top"]-1

            if (start_row <= end_row):
                row_splits.append((start_row, end_row))

            start_row = divider["bottom"]+1

        if(start_row <= grid.shape[0] -1):
            row_splits.append((start_row, grid.shape[0]-1))

        return row_splits

    def get_column_splits(self, grid:np.ndarray, vertical_dividers: list[dict]) -> list[tuple[int,int]]:
        column_splits = []
        start_column = 0

        for divider in vertical_dividers:
            end_column = divider["left"]-1

            if (start_column <= end_column):
                column_splits.append((start_column, end_column))

            start_column = divider["right"]+1

        if(start_column <= grid.shape[1] -1):
            column_splits.append((start_column, grid.shape[1]-1))

        return column_splits


    def get_object_grid_relationships(self, grid: np.ndarray, shapes:list[dict]) -> list[dict]:
        relationships = []

        for shape in shapes:
            fills_grid = (shape["top"] == 0 and shape["bottom"] == grid.shape[0]-1 and shape["left"] == 0 and shape["right"] ==grid.shape[1]-1)

            if fills_grid:
                relationship = {
                    "source_item": "object",
                    "source_id": shape["id"],
                    "relationship": "fills_grid",
                    "target_item": "grid"
                }
                relationships.append(relationship)

            divides_grid_vertical = (shape["top"] == 0 and shape["bottom"] == grid.shape[0] - 1 and shape["width"] == 1 and shape["left"] > 0 and shape["right"] < grid.shape[1] - 1)
            if divides_grid_vertical:
                relationship = {
                    "source_item": "object",
                    "source_id": shape["id"],
                    "relationship": "divides_grid",
                    "target_item": "grid",
                    "orientation": "vertical",
                    "region_count": 2
                }
                relationships.append(relationship)

            divides_grid_horizontal = (shape["top"] > 0 and shape["bottom"] < grid.shape[0] - 1 and shape["height"] == 1 and shape["left"] == 0 and shape["right"] == grid.shape[1] - 1)
            if divides_grid_horizontal:
                relationship = {
                    "source_item": "object",
                    "source_id": shape["id"],
                    "relationship": "divides_grid",
                    "target_item": "grid",
                    "orientation": "horizontal",
                    "region_count": 2
                }
                relationships.append(relationship)

        return relationships

    def identify_shapes(self, grid: np.ndarray, parent_grid_id: str, connections: int = 8) -> list[dict]:

        shapes = []
        visited_cells = set()
        shape_id = 1

        if connections == 4:
            connection_points = [(-1, 0),(0, -1),(0, 1),(1, 0)]
        elif connections == 8:
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
                pattern = np.zeros((boundaries["height"],boundaries["width"]), dtype=int)
                for row,column in cells:
                    pattern[row - boundaries["top"], column - boundaries["left"]] = 1

                shape = {"id": shape_id, "parent_grid_id": parent_grid_id, "color": color, "cells": cells, "pattern": pattern, 
                               "top": boundaries["top"], "bottom":boundaries["bottom"], 
                               "left":boundaries["left"], "right": boundaries["right"], 
                               "height": boundaries["height"], "width": boundaries["width"]}
                shape["is_hollow"] = self.is_hollow(grid, shape)
                shapes.append(shape)

                shape_id +=1
        return shapes


    def is_hollow(self, grid: np.ndarray, shape: dict) -> bool:
        color = shape["color"]
        cells = shape["cells"]
        top = shape["top"]
        bottom = shape["bottom"]
        left = shape["left"]
        right = shape["right"]

        for row in range(top,bottom+1):
            for column in range(left,right+1):
                current_cell = (row, column)
                if current_cell in cells:
                    continue

                top_blocked = False
                bottom_blocked = False
                left_blocked = False
                right_blocked = False

                for row_to_check in range(row-1, top -1, -1):
                    if(grid[row_to_check, column] == color):
                        top_blocked = True
                        break

                for row_to_check in range(row+1, bottom+1,1):
                    if(grid[row_to_check, column] == color):
                        bottom_blocked = True
                        break

                for column_to_check in range(column-1, left-1,-1):
                    if(grid[row, column_to_check] == color):
                        left_blocked = True
                        break

                for column_to_check in range(column+1, right+1,1):
                    if(grid[row, column_to_check] == color):
                        right_blocked = True
                        break

                if top_blocked and bottom_blocked and left_blocked and right_blocked:
                    return True
                
        return False



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



    def analyze_grid(self, grid: np.ndarray, grid_id: str, grid_type: str = "full", parent_id = None, parent_top = None,
            parent_bottom = None, parent_left = None, parent_right = None) -> dict:
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
            "grid_id": grid_id,
            "grid_type": grid_type,
            "parent_id": parent_id,
            "parent_top": parent_top,
            "parent_bottom": parent_bottom,
            "parent_left": parent_left,
            "parent_right": parent_right,
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

    