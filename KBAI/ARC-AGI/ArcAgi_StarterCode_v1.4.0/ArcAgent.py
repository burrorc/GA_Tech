from dataclasses import dataclass

import numpy as np

from ArcProblem import ArcProblem
from ArcData import ArcData
from ArcSet import ArcSet


@dataclass
class Shape:
    id: int
    object_id: str
    parent_grid_id: str
    color: int
    cells: list[tuple[int, int]]
    pattern: np.ndarray
    top: int
    bottom: int
    left: int
    right: int
    height: int
    width: int
    is_hollow: bool
    region_id: str | None = None


@dataclass
class ProblemAnalysis:
    input_grid: np.ndarray
    output_grid: np.ndarray
    input_grid_analysis: dict
    output_grid_analysis: dict
    input_shapes: list[Shape]
    output_shapes: list[Shape]
    input_regions: list[dict]
    output_regions: list[dict]
    input_relationships: list[dict]
    output_relationships: list[dict]
    input_object_relationships: list[dict]
    output_object_relationships: list[dict]
    input_output_object_relationships: list[dict]
    object_transformations: list[dict]
    grid_transformations: list[dict]
    region_transformations: list[dict]
    color_mappings: list[dict]


class ArcAgent:
    def __init__(self):
        """
        You may add additional variables to this init method. Be aware that it gets called only once
        and then the make_predictions method will get called several times.
        """
        with open("debug_output.txt", "w") as debug_file:
            pass
        # print("here6")
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
        

        target_problem = "b2862040"
        target_training_sets = {1, 2, 3}
        training_analyses = []
        training_change_candidates = []

        count = 1

        for training_set in training_sets:
            analysis = self.analyze_problem(training_set, count)
            training_analyses.append(analysis)
            change_candidates = self.get_change_candidates(
                analysis,
                count,
            )
            training_change_candidates.append(change_candidates)
            
            
            
            if (
                arc_problem.problem_name() == target_problem
                and count in target_training_sets
            ):
                with open("debug_output.txt", "a") as debug_file:
                    print(f"\nPROBLEM: {arc_problem.problem_name()}", file=debug_file)
                    print(f"Training Set {count}", file=debug_file)

                    # for shape in analysis.input_shapes:

                    #     print("INPUT SHAPE", file=debug_file)
                    #     print(f"color = {shape.color}", file=debug_file)
                    #     print(f"cell count = {len(shape.cells)}", file=debug_file)
                    #     print(f"is_hollow = {shape.is_hollow}", file=debug_file)

                    # self.print_frame(analysis.input_grid_analysis, "INPUT GRID", debug_file)
                    # self.print_frame(analysis.output_grid_analysis, "OUTPUT GRID", debug_file)

                    
                    # for shape in analysis.input_shapes:
                    #     print("INPUT SHAPE", file=debug_file)
                    #     print(shape, file=debug_file)

                    # for shape in analysis.output_shapes:
                    #     print("OUTPUT SHAPE", file=debug_file)
                    #     print(shape, file=debug_file)

                    # for relationship in analysis.input_relationships:
                    #     self.print_frame(relationship, "INPUT RELATIONSHIPS", debug_file)

                    # for relationship in analysis.output_relationships:
                    #     self.print_frame(relationship, "OUTPUT RELATIONSHIPS", debug_file)

                    # for region in analysis.input_regions:
                    #     self.print_frame(region, "INPUT REGION", debug_file)

                    # for region in analysis.output_regions:
                    #     self.print_frame(region, "OUTPUT REGION", debug_file)

                    # for relationship in analysis.input_object_relationships:
                    #     self.print_frame(relationship, "INPUT OBJECT RELATIONSHIPS", debug_file)

                    # for relationship in analysis.output_object_relationships:
                    #     self.print_frame(relationship, "OUTPUT OBJECT RELATIONSHIPS", debug_file)

                    # for relationship in analysis.input_output_object_relationships:
                    #     self.print_frame(relationship, "INPUT-OUTPUT OBJECT RELATIONSHIPS", debug_file)

                    # for transformation in analysis.object_transformations:
                    #     self.print_frame(transformation, "INPUT-OUTPUT OBJECT TRANSFORMATIONS", debug_file)

                    # for transformation in analysis.grid_transformations:
                    #     self.print_frame(transformation, "GRID TRANSFORMATIONS", debug_file)

                    # for transformation in analysis.region_transformations:
                    #     self.print_frame(transformation, "REGION COMBO TRANSFORMATIONS", debug_file)

                    for change in change_candidates:
                        self.print_frame(change, "CHANGE CANDIDATES", debug_file)

                    # for mapping in analysis.color_mappings:
                    #     print("COLOR MAPPING", file=debug_file)
                    #     for key, value in mapping.items():
                    #         print(key, "=", value, file=debug_file)          

                    


            count += 1

        validated_changes = self.validate_change_candidates(training_change_candidates)

        
        if (
            arc_problem.problem_name() == target_problem
        ):
            with open("debug_output.txt", "a") as debug_file:
                for change in validated_changes:
                    self.print_frame(change, "VALIDATED_CHANGES", debug_file)


        

        '''
        The next 2 lines are only an example of how to populate the predictions list.
        This will just be an empty answer the size of the input data;
        delete it before you start adding your own predictions.
        '''
        test_grid = arc_problem.test_set().get_input_data().data()
        test_shapes = self.identify_shapes(test_grid, "test_grid")
        my_predictions = self. apply_validated_changes(test_grid, test_shapes, validated_changes)

        

        predictions.append(my_predictions)
        # output = np.zeros_like(arc_problem.test_set().get_input_data().data())
        # predictions.append(output)

        return predictions

    def analyze_problem(self, training_set: ArcSet, count: int) -> ProblemAnalysis:
        input_grid = training_set.get_input_data().data()
        output_grid = training_set.get_output_data().data()

        input_grid_id = "input_grid_" + str(count)
        output_grid_id = "output_grid_" + str(count)

        input_grid_analysis = self.analyze_grid(input_grid, input_grid_id, "full")
        output_grid_analysis = self.analyze_grid(output_grid, output_grid_id, "full")
        input_shapes = self.identify_shapes(input_grid, input_grid_id)
        output_shapes = self.identify_shapes(output_grid, output_grid_id)
        input_relationships = self.get_object_grid_relationships(input_grid, input_shapes)
        output_relationships = self.get_object_grid_relationships(output_grid, output_shapes)
        input_regions = self.get_grid_regions(input_grid, input_grid_id, input_shapes, input_relationships)
        output_regions = self.get_grid_regions(output_grid, output_grid_id, output_shapes, output_relationships)
        self.get_shape_regions(input_shapes, input_regions)
        self.get_shape_regions(output_shapes, output_regions)
        input_object_relationships = self.get_object_to_object_relationships(input_shapes)
        output_object_relationships = self.get_object_to_object_relationships(output_shapes)
        input_output_object_relationships = self.get_object_to_object_relationships(input_shapes, output_shapes)
        object_transformations = self.get_input_output_transformations(
            input_shapes, output_shapes, input_object_relationships, input_output_object_relationships, input_grid, output_grid
        )
        grid_transformations = self.get_grid_transformations(
            input_grid,
            output_grid,
            input_grid_analysis,
            output_grid_analysis,
            input_shapes,
            output_shapes,
            object_transformations,
        )
        region_transformations = []
        if len(input_regions) == 2:
            region1 = self.get_region_grid(input_grid, input_regions[0])
            region2 = self.get_region_grid(input_grid, input_regions[1])
            region_transformations = self.get_region_combo_transformations(region1, region2, output_grid)
        color_mappings = self.get_color_mappings(input_grid, output_grid)

        return ProblemAnalysis(
            input_grid=input_grid,
            output_grid=output_grid,
            input_grid_analysis=input_grid_analysis,
            output_grid_analysis=output_grid_analysis,
            input_shapes=input_shapes,
            output_shapes=output_shapes,
            input_regions=input_regions,
            output_regions=output_regions,
            input_relationships=input_relationships,
            output_relationships=output_relationships,
            input_object_relationships=input_object_relationships,
            output_object_relationships=output_object_relationships,
            input_output_object_relationships=input_output_object_relationships,
            object_transformations=object_transformations,
            grid_transformations=grid_transformations,
            region_transformations=region_transformations,
            color_mappings=color_mappings,
        )

    def print_frame(self, frame: dict, label: str = "", file=None):

        if label:
            print(label, file=file)

        for key, value in frame.items():
            print(f"{key} = {value}", file=file)

    def get_region_grid(self, grid: np.ndarray, region: dict) -> np.ndarray:
        return grid[region["parent_top"]:region["parent_bottom"] + 1,
            region["parent_left"]:region["parent_right"] + 1]

    def get_region_combo_transformations(self, region1:np.ndarray, region2:np.ndarray, output_grid: np.ndarray) -> list[dict]:
        transformations = []
        possible_transforms = [
            ("same", lambda grid: grid),
            ("flipped_h", lambda grid: np.fliplr(grid)),
            ("flipped_v", lambda grid: np.flipud(grid)),
            ("rotation_90", lambda grid: np.rot90(grid, 1)),
            ("rotation_180", lambda grid: np.rot90(grid, 2)),
            ("rotation_270", lambda grid: np.rot90(grid, 3)),
        ]

        if region1.shape != output_grid.shape:
            return transformations

        output_colors = np.unique(output_grid)
        non_background_colors = []
        for color in output_colors:
            if color != 0:
                non_background_colors.append(int(color))

        if(len(non_background_colors) !=1):
            return transformations

        output_color = non_background_colors[0]
        
        for trans_name, trans_lambda in possible_transforms:
            transformed2 = trans_lambda(region2)

            if transformed2.shape != region1.shape:
                continue

            filled1 = region1 !=0
            filled2 = transformed2 !=0

            calculations = {
                "union": np.logical_or(filled1, filled2),
                "intersection": np.logical_and(filled1, filled2),
                "a_minus_b": np.logical_and(filled1, np.logical_not(filled2)),
                "b_minus_a": np.logical_and(filled2, np.logical_not(filled1)),
                "xor": np.logical_xor(filled1, filled2),
                "both_empty": np.logical_and(np.logical_not(filled1),np.logical_not(filled2),),
            }

            for cal_name, result in calculations.items():
                generated_result = np.zeros(output_grid.shape, dtype=int)
                generated_result[result] = output_color

                if(np.array_equal(generated_result, output_grid)):
                    transformations.append({
                        "transformation_type": "grid",
                        "transformation": "combine_regions",
                        "region2_transform": trans_name,
                        "operation": cal_name,
                        "output_color": output_color,
                    })

        return transformations

    def get_color_mappings(self, input_grid: np.ndarray, output_grid: np.ndarray)-> list[dict]:
        mappings = []
        # i dunno what I'm gonna do here, this will only work when grids are same size

        if input_grid.shape != output_grid.shape:
            return mappings
        
        input_colors = np.unique(input_grid)

        for color in input_colors:
            # ignore backgournd
            if color == 0:
                continue

            output_colors = output_grid[input_grid == color]
            unique_output_colors = np.unique(output_colors)

            if(len(unique_output_colors) == 1):
                output_color = unique_output_colors[0]

                if color != output_color:
                    mappings.append({
                        "from_color": int(color),
                        "to_color": int(output_color),
                    })

        return mappings


    def get_shape_by_reference(self, shapes: list[Shape], reference: str) -> Shape | None:
        if not shapes:
            return None
        
        if(reference == "single"):
            if(len(shapes)==1):
                return shapes[0]
        elif reference == "largest":
            largest_shape = shapes[0]
            largest_size = largest_shape.height * largest_shape.width
            largest_count = 1

            for shape in shapes[1:]:
                size = shape.height * shape.width

                if (size > largest_size):
                    largest_shape = shape
                    largest_size = size
                    largest_count = 1

                elif size == largest_size:
                    largest_count += 1

            if largest_count == 1:
                return largest_shape

        elif reference == "smallest":
            smallest_shape = shapes[0]
            smallest_size = smallest_shape.height * smallest_shape.width
            smallest_count = 1

            for shape in shapes[1:]:
                size = shape.height * shape.width

                if (size < smallest_size):
                    smallest_shape = shape
                    smallest_size = size
                    smallest_count = 1

                elif size == smallest_size:
                    smallest_count += 1

            if smallest_count == 1:
                return smallest_shape

        return None


    def get_grid_transformations(self, input_grid:np.ndarray, output_grid:np.ndarray, input_grid_analysis: dict, output_grid_analysis: dict, 
                                 input_shapes: list[Shape], output_shapes: list[Shape],
                                 input_output_transformations)-> list[dict]:
        transformations = []
        input_shapes_map = {}
        output_shapes_map = {}

        
        if np.array_equal(np.rot90(input_grid, 1), output_grid):
            transformations.append({
                "transformation_type": "grid",
                "transformation": "rotation_90",
            })
        if np.array_equal(np.rot90(input_grid, 2), output_grid):
            transformations.append({
                "transformation_type": "grid",
                "transformation": "rotation_180",
            })
        if np.array_equal(np.rot90(input_grid, 3), output_grid):
            transformations.append({
                "transformation_type": "grid",
                "transformation": "rotation_270",
            })
        if np.array_equal(np.flipud(input_grid), output_grid):
                    transformations.append({
                        "transformation_type": "grid",
                        "transformation": "flipped_v",
                    })

        flipped_h = np.fliplr(input_grid)

        if np.array_equal(flipped_h, output_grid):
            transformations.append({
                "transformation_type": "grid",
                "transformation": "flipped_h",
            })
        if np.array_equal(np.rot90(flipped_h, 1), output_grid):
            transformations.append({
                "transformation_type": "grid",
                "transformation": "flipped_h_rotation_90",
            })
        if np.array_equal(np.rot90(flipped_h, 3), output_grid):
            transformations.append({
                "transformation_type": "grid",
                "transformation": "flipped_h_rotation_270",
            })

        intra_grid_tranformations = [
            ("same", lambda grid: grid),
            ("flipped_h", lambda grid: np.fliplr(grid)),
            ("flipped_v", lambda grid: np.flipud(grid)),
            ("rotation_180", lambda grid: np.rot90(grid, 2)),
        ]
        
        if input_grid.shape == output_grid.shape:
            height = input_grid.shape[0]
            width = input_grid.shape[1]

            if height % 2 == 0:
                middle = height // 2

                input_top = input_grid[:middle, :]
                input_bottom = input_grid[middle:, :]

                output_top = output_grid[:middle, :]
                output_bottom = output_grid[middle:, :]
                if(np.all(input_top == 0) and np.array_equal(input_bottom, output_bottom)):
                    for trans_name, trans_lambda in intra_grid_tranformations:
                        transformed = trans_lambda(input_bottom)
                        if np.array_equal(transformed, output_top):
                            transformations.append({
                                "transformation_type": "grid",
                                "transformation": "copy_to_empty_half",
                                "axis": "horizontal",
                                "source_side": "bottom",
                                "target_side": "top",
                                "copy_transform": trans_name,
                            })
                            break
                if(np.all(input_bottom == 0) and np.array_equal(input_top, output_top)):
                    for trans_name, trans_lambda in intra_grid_tranformations:
                        transformed = trans_lambda(input_top)
                        if np.array_equal(transformed, output_bottom):
                            transformations.append({
                                "transformation_type": "grid",
                                "transformation": "copy_to_empty_half",
                                "axis": "horizontal",
                                "source_side": "top",
                                "target_side": "bottom",
                                "copy_transform": trans_name,
                            })
                            break

            if width % 2 == 0:
                middle = width // 2

                input_left = input_grid[:, :middle]
                input_right = input_grid[:,middle:]

                output_left = output_grid[:, :middle]
                output_right = output_grid[:,middle:]
                if(np.all(input_left == 0) and np.array_equal(input_right, output_right)):
                    for trans_name, trans_lambda in intra_grid_tranformations:
                        transformed = trans_lambda(input_right)
                        if np.array_equal(transformed, output_left):
                            transformations.append({
                                "transformation_type": "grid",
                                "transformation": "copy_to_empty_half",
                                "axis": "vertical",
                                "source_side": "right",
                                "target_side": "left",
                                "copy_transform": trans_name,
                            })
                            break
                if(np.all(input_right == 0) and np.array_equal(input_left, output_left)):
                    for trans_name, trans_lambda in intra_grid_tranformations:
                        transformed = trans_lambda(input_left)
                        if np.array_equal(transformed, output_right):
                            transformations.append({
                                "transformation_type": "grid",
                                "transformation": "copy_to_empty_half",
                                "axis": "vertical",
                                "source_side": "left",
                                "target_side": "right",
                                "copy_transform": trans_name,
                            })
                            break


        for shape in input_shapes:
            input_shapes_map[shape.object_id] = shape

        for shape in output_shapes:
            output_shapes_map[shape.object_id] = shape

        # for source_shape in input_shapes:

            # object_reference = self.get_object_reference(
            #     source_shape,
            #     input_shapes,
            # )

            # if object_reference is None:
            #     continue

            # cropped_grid = input_grid[
            #     source_shape.top:source_shape.bottom + 1,
            #     source_shape.left:source_shape.right + 1
            # ]

            # if np.array_equal(cropped_grid, output_grid):
            #     transformations.append({
            #         "transformation_type": "grid",
            #         "transformation": "crop_to_object",
            #         "source_id": source_shape.object_id,
            #         "object_reference": object_reference,
            #     })
        for transformation in input_output_transformations:

            if transformation["transformation"] not in ("none", "color_change"):
                continue

            source_shape = input_shapes_map[transformation["source_id"]]

            object_reference = self.get_object_reference(
                source_shape,
                input_shapes,
            )

            if object_reference is None:
                continue

            if (
                output_grid.shape[0] == source_shape.height
                and output_grid.shape[1] == source_shape.width
            ):
                transformations.append({
                    "transformation_type": "grid",
                    "transformation": "crop_to_object",
                    "source_id": source_shape.object_id,
                    "object_reference": object_reference,
                })

        marker_colors = {}

        for shape in input_shapes:

            if len(shape.cells) != 1:
                continue

            if shape.color not in marker_colors:
                marker_colors[shape.color] = []

            marker_colors[shape.color].append(shape)


        for marker_color, marker_shapes in marker_colors.items():

            if len(marker_shapes) != 4:
                continue

            marker_rows = []
            marker_columns = []

            for shape in marker_shapes:
                marker_rows.append(shape.top)
                marker_columns.append(shape.left)

            unique_rows = sorted(set(marker_rows))
            unique_columns = sorted(set(marker_columns))

            if len(unique_rows) != 2:
                continue

            if len(unique_columns) != 2:
                continue

            top = unique_rows[0]
            bottom = unique_rows[1]
            left = unique_columns[0]
            right = unique_columns[1]

            expected_corners = {
                (top, left),
                (top, right),
                (bottom, left),
                (bottom, right),
            }

            actual_corners = set()

            for shape in marker_shapes:
                actual_corners.add(
                    (shape.top, shape.left)
                )

            if actual_corners != expected_corners:
                continue

            interior_grid = input_grid[
                top + 1:bottom,
                left + 1:right
            ]
            interior_pattern = interior_grid != 0
            output_pattern = output_grid != 0

            if np.array_equal(interior_pattern, output_pattern):

                
                transformations.append({
                    "transformation_type": "grid",
                    "transformation": "crop_to_bounded_region",
                    "marker_reference": {
                        "count": 4,
                        "cell_count": 1,
                        "same_color": True,
                        "arrangement": "rectangle_corners",
                    },
                    "crop_area": "inside_markers",
                    "recolor_to": "marker_color",
                })

        for shape in input_shapes:

            hollow_regions = self.get_hollow_regions(
                input_grid,
                shape,
            )

            if len(hollow_regions) == 0:
                continue

            generated_grid = input_grid.copy()

            # First turn all background into exterior color 3.
            generated_grid[generated_grid == 0] = 3

            # Then recolor enclosed regions to 2.
            for region in hollow_regions:
                for row, column in region:
                    generated_grid[row, column] = 2

            if not np.array_equal(
                generated_grid,
                output_grid,
            ):
                continue

            transformations.append({
                "transformation_type": "grid",
                "transformation": "recolor_hollow_regions",
                "source_color": shape.color,
                "hollow_color": 2,
                "exterior_color": 3,
            })

        if input_grid.shape == output_grid.shape:

            changed_cells = input_grid != output_grid

            if np.any(changed_cells):

                source_colors = np.unique(
                    input_grid[changed_cells]
                )

                target_colors = np.unique(
                    output_grid[changed_cells]
                )

                if (
                    len(source_colors) == 1
                    and len(target_colors) == 1
                ):

                    source_color = int(source_colors[0])
                    target_color = int(target_colors[0])

                    generated_grid = input_grid.copy()

                    for shape in input_shapes:

                        if shape.color != source_color:
                            continue

                        if not shape.is_hollow:
                            continue

                        for row, column in shape.cells:
                            generated_grid[row, column] = target_color

                    if np.array_equal(
                        generated_grid,
                        output_grid,
                    ):

                        transformations.append({
                            "transformation_type": "grid",
                            "transformation": "recolor_hollow_objects",
                            "source_color": source_color,
                            "target_color": target_color,
                        })
        return transformations
    
    def get_object_reference(self, source_shape: Shape, shapes: list[Shape]) -> str | None:
        if(len(shapes) == 1):
            return "single"

        largest_shape = shapes[0]
        largest_size = largest_shape.height * largest_shape.width
        largest_count = 1

        smallest_shape = shapes[0]
        smallest_size = smallest_shape.height * smallest_shape.width
        smallest_count = 1

        for shape in shapes[1:]:
            size = shape.height * shape.width

            if(size > largest_size):
                largest_shape = shape
                largest_size = size
                largest_count = 1
            elif(size == largest_size):
                largest_count +=1

            if size < smallest_size:
                smallest_shape = shape
                smallest_size = size
                smallest_count = 1
            elif size == smallest_size:
                smallest_count += 1

        if(largest_count == 1 and largest_shape.object_id == source_shape.object_id):
            return "largest"
        if(smallest_count == 1 and smallest_shape.object_id == source_shape.object_id):
            return "smallest"

        return None

    def select_object_reference(self, test_shapes: list[Shape], change: dict) -> Shape | None:
        if not test_shapes:
            return None
        if (change["object_reference"] == "single"):
            if(len(test_shapes) == 1):
                return test_shapes[0]
        elif(change["object_reference"] == "largest"):
            largest_shape = test_shapes[0]
            largest_size = largest_shape.height * largest_shape.width
            largest_count = 1

            for shape in test_shapes[1:]:
                size = shape.height * shape.width

                if(size> largest_size):
                    largest_shape = shape
                    largest_size = size
                    largest_count = 1

            if (largest_count == 1):
                return largest_shape            
        return None
            

    def apply_validated_changes(self, test_grid: np.ndarray, test_shapes: list[Shape], validated_changes: list[dict])-> np.ndarray:
        output_grid = test_grid.copy()
        mapped_color = None
        mapped_source_color = None
        test_relationships = self.get_object_grid_relationships(test_grid, test_shapes)
        test_regions = self.get_grid_regions(test_grid, "test_grid", test_shapes, test_relationships)

        for change in validated_changes:
                if(change["change_type"] == "crop_to_object"):
                    shape = self.select_object_reference(test_shapes, change)
                    if shape is not None:
                        output_grid = test_grid[shape.top:shape.bottom + 1, shape.left:shape.right + 1].copy()
                elif change["change_type"] == "crop_to_bounded_region":

                    marker_colors = {}

                    for shape in test_shapes:

                        if len(shape.cells) != change["marker_reference"]["cell_count"]:
                            continue

                        if shape.color not in marker_colors:
                            marker_colors[shape.color] = []

                        marker_colors[shape.color].append(shape)


                    for marker_color, marker_shapes in marker_colors.items():

                        if len(marker_shapes) != change["marker_reference"]["count"]:
                            continue

                        marker_rows = []
                        marker_columns = []

                        for shape in marker_shapes:
                            marker_rows.append(shape.top)
                            marker_columns.append(shape.left)

                        unique_rows = sorted(set(marker_rows))
                        unique_columns = sorted(set(marker_columns))

                        if len(unique_rows) != 2:
                            continue

                        if len(unique_columns) != 2:
                            continue

                        top = unique_rows[0]
                        bottom = unique_rows[1]
                        left = unique_columns[0]
                        right = unique_columns[1]

                        expected_corners = {
                            (top, left),
                            (top, right),
                            (bottom, left),
                            (bottom, right),
                        }

                        actual_corners = set()

                        for shape in marker_shapes:
                            actual_corners.add(
                                (shape.top, shape.left)
                            )

                        if actual_corners != expected_corners:
                            continue

                        output_grid = test_grid[
                            top + 1:bottom,
                            left + 1:right
                        ].copy()

                        if change["recolor_to"] == "marker_color":

                            for row in range(output_grid.shape[0]):
                                for column in range(output_grid.shape[1]):

                                    if output_grid[row, column] != 0:
                                        output_grid[row, column] = marker_color

                        break
                elif change["change_type"] == "rotation_90":
                    output_grid = np.rot90(output_grid, 1).copy()

                elif change["change_type"] == "rotation_180":
                    output_grid = np.rot90(output_grid, 2).copy()

                elif change["change_type"] == "rotation_270":
                    output_grid = np.rot90(output_grid, 3).copy()

                elif change["change_type"] == "flipped_h":
                    output_grid = np.fliplr(output_grid).copy()

                elif change["change_type"] == "flipped_v":
                    output_grid = np.flipud(output_grid).copy()

                elif change["change_type"] == "flipped_h_rotation_90":
                    output_grid = np.rot90(np.fliplr(output_grid), 1).copy()

                elif change["change_type"] == "flipped_h_rotation_270":
                    output_grid = np.rot90(np.fliplr(output_grid), 3).copy()

                elif change["change_type"] == "combine_regions":

                    if len(test_regions) == 2:
                        region1 = self.get_region_grid(test_grid, test_regions[0])
                        region2 = self.get_region_grid(test_grid, test_regions[1])

                        if change["region2_transform"] == "same":
                            transformed2 = region2.copy()

                        elif change["region2_transform"] == "flipped_h":
                            transformed2 = np.fliplr(region2).copy()

                        elif change["region2_transform"] == "flipped_v":
                            transformed2 = np.flipud(region2).copy()

                        elif change["region2_transform"] == "rotation_90":
                            transformed2 = np.rot90(region2, 1).copy()

                        elif change["region2_transform"] == "rotation_180":
                            transformed2 = np.rot90(region2, 2).copy()

                        elif change["region2_transform"] == "rotation_270":
                            transformed2 = np.rot90(region2, 3).copy()

                        filled1 = region1 != 0
                        filled2 = transformed2 != 0

                        if change["operation"] == "union":
                            result = np.logical_or(filled1, filled2)

                        elif change["operation"] == "intersection":
                            result = np.logical_and(filled1, filled2)

                        elif change["operation"] == "a_minus_b":
                            result = np.logical_and(
                                filled1,
                                np.logical_not(filled2)
                            )

                        elif change["operation"] == "b_minus_a":
                            result = np.logical_and(
                                filled2,
                                np.logical_not(filled1)
                            )

                        elif change["operation"] == "xor":
                            result = np.logical_xor(filled1, filled2)

                        elif change["operation"] == "both_empty":
                            result = np.logical_and(
                                np.logical_not(filled1),
                                np.logical_not(filled2)
                            )

                        output_grid = np.zeros(region1.shape, dtype=int)
                        output_grid[result] = change["output_color"]

                elif change["change_type"] == "copy_to_empty_half":
                    height = output_grid.shape[0]
                    width = output_grid.shape[1]
                    if change["axis"] == "horizontal":
                        middle = height // 2
                        if change["source_side"] == "bottom":
                            source = output_grid[middle:, :].copy()
                        else:
                            source = output_grid[:middle, :].copy()
                    else:
                        middle = width // 2
                        if change["source_side"] == "right":
                            source = output_grid[:, middle:].copy()
                        else:
                            source = output_grid[:, :middle].copy()

                    if change["copy_transform"] == "same":
                        transformed = source.copy()

                    elif change["copy_transform"] == "flipped_h":
                        transformed = np.fliplr(source).copy()

                    elif change["copy_transform"] == "flipped_v":
                        transformed = np.flipud(source).copy()

                    elif change["copy_transform"] == "rotation_180":
                        transformed = np.rot90(source, 2).copy()

                    if change["axis"] == "horizontal":
                        if change["target_side"] == "top":
                            output_grid[:middle, :] = transformed
                        else:
                            output_grid[middle:, :] = transformed
                    else:
                        if change["target_side"] == "left":
                            output_grid[:, :middle] = transformed
                        else:
                            output_grid[:, middle:] = transformed

                elif (
                        change["change_type"] == "generate_from_seed"
                        and change.get("source_type") == "object_corner"
                    ):
                    source_shape = self.get_shape_by_reference(
                        test_shapes,
                        change["source_reference"],
                    )

                    source_shape = None

                    if change.get("source_type") == "object_corner":

                        source_reference = change["source_reference"]

                        for shape in test_shapes:

                            if shape.color != source_reference["color"]:
                                continue

                            if shape.height != source_reference["height"]:
                                continue

                            if shape.width != source_reference["width"]:
                                continue

                            if len(shape.cells) != source_reference["cell_count"]:
                                continue

                            source_shape = shape
                            break

                    else:
                        source_shape = self.get_shape_by_reference(
                            test_shapes,
                            change["source_reference"],
                        )

                    if source_shape is None:
                        continue

                    direction_offsets = {
                        "up": (-1, 0),
                        "down": (1, 0),
                        "left": (0, -1),
                        "right": (0, 1),
                        "upper_left": (-1, -1),
                        "upper_right": (-1, 1),
                        "lower_left": (1, -1),
                        "lower_right": (1, 1),
                    }

                    if change.get("source_type") == "object_corner":
                        corner = change["corner"]
                        direction = change["direction"]
                        source_color = source_shape.color

                        if corner == "top_left":
                            seed_row = source_shape.top
                            seed_column = source_shape.left
                        elif corner == "top_right":
                            seed_row = source_shape.top
                            seed_column = source_shape.right
                        elif corner == "bottom_left":
                            seed_row = source_shape.bottom
                            seed_column = source_shape.left
                        elif corner == "bottom_right":
                            seed_row = source_shape.bottom
                            seed_column = source_shape.right
                        else:
                            continue

            

                        direction_offsets = {
                            "up": (-1, 0),
                            "down": (1, 0),
                            "left": (0, -1),
                            "right": (0, 1),
                            "upper_left": (-1, -1),
                            "upper_right": (-1, 1),
                            "lower_left": (1, -1),
                            "lower_right": (1, 1),
                        }

                        delta_row, delta_column = direction_offsets[change["direction"]]

                        current_row = seed_row + delta_row
                        current_column = seed_column + delta_column

                        while (
                            0 <= current_row < output_grid.shape[0]
                            and 0 <= current_column < output_grid.shape[1]
                        ):
                            output_grid[current_row, current_column] = source_color

                            current_row += delta_row
                            current_column += delta_column

                elif change["change_type"] == "generate_from_seed":
                    source_type = change.get(
                        "source_type",
                        "standalone",
                    )

                    if source_type == "embedded":

                        non_background_colors = []

                        for color in np.unique(test_grid):
                            if color != 0:
                                non_background_colors.append(int(color))

                        for seed_color in non_background_colors:

                            seed_cells = np.argwhere(
                                test_grid == seed_color
                            )

                            if len(seed_cells) != 1:
                                continue

                            seed_row = int(seed_cells[0][0])
                            seed_column = int(seed_cells[0][1])

                            surrounding_colors = set()

                            neighbors = [
                                (seed_row - 1, seed_column),
                                (seed_row + 1, seed_column),
                                (seed_row, seed_column - 1),
                                (seed_row, seed_column + 1),
                            ]

                            for neighbor_row, neighbor_column in neighbors:

                                if (
                                    0 <= neighbor_row < test_grid.shape[0]
                                    and 0 <= neighbor_column < test_grid.shape[1]
                                ):
                                    neighbor_color = int(
                                        test_grid[
                                            neighbor_row,
                                            neighbor_column,
                                        ]
                                    )

                                    if (
                                        neighbor_color != 0
                                        and neighbor_color != seed_color
                                    ):
                                        surrounding_colors.add(
                                            neighbor_color
                                        )

                            if len(surrounding_colors) == 0:
                                continue

                            direction = None

                            if seed_row == 0:
                                direction = "down"

                            elif seed_row == test_grid.shape[0] - 1:
                                direction = "up"

                            elif seed_column == 0:
                                direction = "right"

                            elif seed_column == test_grid.shape[1] - 1:
                                direction = "left"

                            else:

                                up_color = test_grid[
                                    seed_row - 1,
                                    seed_column,
                                ]
                                down_color = test_grid[
                                    seed_row + 1,
                                    seed_column,
                                ]
                                left_color = test_grid[
                                    seed_row,
                                    seed_column - 1,
                                ]
                                right_color = test_grid[
                                    seed_row,
                                    seed_column + 1,
                                ]

                                if (
                                    up_color != 0
                                    and down_color == 0
                                ):
                                    direction = "up"

                                elif (
                                    down_color != 0
                                    and up_color == 0
                                ):
                                    direction = "down"

                                elif (
                                    left_color != 0
                                    and right_color == 0
                                ):
                                    direction = "left"

                                elif (
                                    right_color != 0
                                    and left_color == 0
                                ):
                                    direction = "right"

                            if direction is None:
                                continue
                            
                            direction_offsets = {
                                "up": (-1, 0),
                                "down": (1, 0),
                                "left": (0, -1),
                                "right": (0, 1),
                            }

                            row_offset, column_offset = direction_offsets[direction]

                            current_row = seed_row + row_offset
                            current_column = seed_column + column_offset

                            while (
                                0 <= current_row < output_grid.shape[0]
                                and 0 <= current_column < output_grid.shape[1]
                            ):

                                if output_grid[current_row, current_column] == 0:
                                    output_grid[current_row, current_column] = seed_color

                                current_row += row_offset
                                current_column += column_offset

                            break
                    source_shape = self.get_shape_by_reference(
                        test_shapes,
                        change["source_reference"],
                    )

                    if source_shape is not None and len(source_shape.cells) == 1:
                        seed_row, seed_column = source_shape.cells[0]
                        source_color = source_shape.color

                        direction_offsets = {
                            "up": (-1, 0),
                            "down": (1, 0),
                            "left": (0, -1),
                            "right": (0, 1),
                            "upper_left": (-1, -1),
                            "upper_right": (-1, 1),
                            "lower_left": (1, -1),
                            "lower_right": (1, 1),
                        }

                        for extension in change["extensions"]:
                            direction = extension["direction"]
                            stop_type = extension["stop_type"]

                            if direction not in direction_offsets:
                                continue

                            row_offset, column_offset = direction_offsets[direction]

                            current_row = seed_row + row_offset
                            current_column = seed_column + column_offset

                            if stop_type == "grid_edge":
                                while (
                                    0 <= current_row < output_grid.shape[0]
                                    and 0 <= current_column < output_grid.shape[1]
                                ):
                                    output_grid[current_row, current_column] = source_color

                                    current_row += row_offset
                                    current_column += column_offset

                elif change["change_type"] == "expand_objects":
                    source_reference = change["source_reference"]
                    distance = change["distance"]
                    target_color = change["target_color"]

                    for shape in test_shapes:
                        if (
                            source_reference["scope"] == "all_matching"
                            and shape.height == source_reference["height"]
                            and shape.width == source_reference["width"]
                            and len(shape.cells) == source_reference["cell_count"]
                            and shape.color == source_reference["color"]
                        ):

                            for row, column in shape.cells:
                                for row_offset in range(-distance, distance + 1):
                                    for column_offset in range(-distance, distance + 1):

                                        new_row = row + row_offset
                                        new_column = column + column_offset

                                        if (
                                            0 <= new_row < output_grid.shape[0]
                                            and 0 <= new_column < output_grid.shape[1]
                                        ):
                                            output_grid[new_row, new_column] = target_color
                elif change["change_type"] == "move_toward_object":

                    source_reference = change["source_reference"]
                    target_relationship = change.get("target_relationship")
                    target_reference = change.get("target_reference")
                    move_type = change.get("move_type", "until")
                    stop_type = change.get("stop_type")
                    distance = change["distance"]

                    test_object_relationships = self.get_object_to_object_relationships(test_shapes)

                    for source_shape in test_shapes:

                        if len(source_shape.cells) != source_reference["cell_count"]:
                            continue
                        if (
                            "color" in source_reference
                            and source_shape.color != source_reference["color"]
                        ):
                            continue

                        target_shape = None
                        if target_relationship is not None:

                            for relationship in test_object_relationships:

                                if relationship["source_id"] != source_shape.object_id:
                                    continue

                                if relationship["relationship_type"] != target_relationship["relationship_type"]:
                                    continue

                                if relationship["relationship_degree"] != target_relationship["relationship_degree"]:
                                    continue

                                for shape in test_shapes:
                                    if shape.object_id == relationship["target_id"]:
                                        if len(shape.cells) > len(source_shape.cells):
                                            target_shape = shape
                                            break

                                if target_shape is not None:
                                    break

                        elif target_reference is not None:

                            for shape in test_shapes:

                                if shape.object_id == source_shape.object_id:
                                    continue

                                if shape.color != target_reference["color"]:
                                    continue

                                if len(shape.cells) != target_reference["cell_count"]:
                                    continue

                                target_shape = shape
                                break
                        
                        # Remove unmatched small objects.
                        if target_shape is None:
                            for row, column in source_shape.cells:
                                output_grid[row, column] = 0
                            continue
                        if move_type == "step":

                            source_row, source_column = source_shape.cells[0]

                            row_step = 0
                            column_step = 0

                            if target_shape.top > source_row:
                                row_step = 1
                            elif target_shape.top < source_row:
                                row_step = -1

                            if target_shape.left > source_column:
                                column_step = 1
                            elif target_shape.left < source_column:
                                column_step = -1

                            moved_row = source_row + row_step
                            moved_column = source_column + column_step

                            output_grid[source_row, source_column] = 0
                            output_grid[moved_row, moved_column] = source_shape.color

                            continue

                        source_row, source_column = source_shape.cells[0]

                        moved_row = None
                        moved_column = None

                        if (
                            target_shape.left == target_shape.right
                            and target_shape.top <= source_row <= target_shape.bottom
                        ):
                            if source_column < target_shape.left:
                                moved_row = source_row
                                moved_column = target_shape.left - distance

                            elif source_column > target_shape.right:
                                moved_row = source_row
                                moved_column = target_shape.right + distance

                        elif (
                            target_shape.top == target_shape.bottom
                            and target_shape.left <= source_column <= target_shape.right
                        ):
                            if source_row < target_shape.top:
                                moved_row = target_shape.top - distance
                                moved_column = source_column

                            elif source_row > target_shape.bottom:
                                moved_row = target_shape.bottom + distance
                                moved_column = source_column

                        if moved_row is None or moved_column is None:
                            continue

                        # Remove source from its old position.
                        output_grid[source_row, source_column] = 0

                        # Place it at the new position.
                        output_grid[moved_row, moved_column] = source_shape.color

                elif change["change_type"] == "recolor_hollow_objects":

                    output_grid = test_grid.copy()

                    for shape in test_shapes:

                        if shape.color != change["source_color"]:
                            continue

                        if not shape.is_hollow:
                            continue

                        for row, column in shape.cells:
                            output_grid[row, column] = change["target_color"]
                elif change["change_type"] == "recolor_hollow_regions":

                    source_shape = None

                    for shape in test_shapes:
                        hollow_regions = self.get_hollow_regions(
                            test_grid,
                            shape,
                        )

                        if len(hollow_regions) == 0:
                            continue

                        source_shape = shape
                        break

                    if source_shape is None:
                        continue

                    hollow_regions = self.get_hollow_regions(
                        test_grid,
                        source_shape,
                    )

                    output_grid = test_grid.copy()

                    output_grid[output_grid == 0] = change["exterior_color"]

                    for region in hollow_regions:
                        for row, column in region:
                            output_grid[row, column] = change["hollow_color"]
                
        original_grid = output_grid.copy()

        for change in validated_changes:
            if (change["change_type"] == "color_change"and "source_color" in change and change.get("target_reference") == "mapped_color"):
                mapped_source_color = change["source_color"]
                break
        if mapped_source_color is not None:
            for color in np.unique(original_grid):
                if color == 0:
                    continue

                if color == mapped_source_color:
                    continue

                mapped_color = int(color)
                break


        for change in validated_changes:
            if(change["change_type"] == "color_mapping"):
                output_grid[original_grid == change["from_color"]] = change["to_color"]
            elif change["change_type"] == "color_change":
                if ("source_color" in change and change.get("target_reference") == "mapped_color"):
                    if mapped_color is not None:
                        output_grid[original_grid == change["source_color"]] = mapped_color
                elif(change.get("source_reference") == "mapped_color"and "target_color" in change):
                    if mapped_color is not None:
                        output_grid[original_grid == mapped_color] = change["target_color"]
                else:
                    source_shape = self.get_shape_by_reference(test_shapes,change["source_reference"])
                    target_shape = self.get_shape_by_reference( test_shapes,change["target_reference"])

                    if source_shape is not None and target_shape is not None:
                        source_color = source_shape.color
                        target_color = target_shape.color

                        output_grid[original_grid == source_color] = target_color
            elif change["change_type"] == "make_hollow":
                if change["source_reference"] == "all_objects":

                    for shape in test_shapes:
                        top = shape.top
                        bottom = shape.bottom
                        left = shape.left
                        right = shape.right
                        color = shape.color

                        for row in range(top, bottom + 1):
                            for column in range(left, right + 1):

                                if original_grid[row, column] != color:
                                    continue

                                if(row != top and row != bottom and column != left and column != right):
                                    output_grid[row, column] = change["fill_color"]

        return output_grid

    def validate_change_candidates(self, change_candidates: list[list[dict]]) -> list[dict]:
        validated_changes = []
        color_change_keys = ["source_reference", "target_reference","source_color","target_color"]
        if not change_candidates:
            return validated_changes

        first_training_changes = change_candidates[0]

        for change in first_training_changes:
            found_in_all = True

            for candidates in change_candidates[1:]:
                found = False

                for other in candidates:
                    if(change["change_type"] != other["change_type"]):
                        continue

                    if (change.get("exact_solution") == True and other.get("exact_solution") == True):
                        found = True
                        break
                    elif change["change_type"] == "copy_to_empty_half":
                        if (change["axis"] == other["axis"]and change["source_side"] == other["source_side"]
                            and change["target_side"] == other["target_side"]and change["copy_transform"] == other["copy_transform"]):
                            found = True
                            break
                    elif change["change_type"] == "recolor_hollow_regions":

                        if (
                            change["hollow_color"] == other["hollow_color"]
                            and change["exterior_color"] == other["exterior_color"]
                        ):
                            found = True
                            break
                    elif change["change_type"] == "recolor_hollow_objects":

                        if change["source_color"] != other["source_color"]:
                            continue

                        if change["target_color"] != other["target_color"]:
                            continue

                        found = True
                        break
                    elif change["change_type"] == "color_mapping":

                        if change["from_color"] != other["from_color"]:
                            continue

                        if change["to_color"] != other["to_color"]:
                            continue

                        found = True
                        break
                    elif(change["change_type"] == "color_change"):
                        change_values = {}
                        other_values = {}

                        for key in color_change_keys:
                            if key in change:
                                change_values[key] = change[key]

                            if key in other:
                                other_values[key] = other[key]

                        if change_values == other_values:
                            found = True
                            break
                        # if (change["source_reference"] == other["source_reference"]
                        #     and change["target_reference"] == other["target_reference"]):
                        #     found = True
                        #     break
                    elif change["change_type"] == "make_hollow":
                        if (change["source_reference"] == other["source_reference"]and change["fill_color"] == other["fill_color"]):
                            found = True
                            break
                    elif change["change_type"] == "fill_in":
                        if change["source_reference"] == other["source_reference"]:
                            found = True
                            break
                    elif(change["change_type"] == "crop_to_object"):
                        if(change["object_reference"] == other["object_reference"]):
                            found = True
                            break
                    elif change["change_type"] == "combine_regions":
                        if (change["region2_transform"] == other["region2_transform"] and change["operation"] == other["operation"]
                            and change["output_color"] == other["output_color"]):
                            found = True
                            break
                    elif change["change_type"] == "generate_from_seed":

                        if change["source_reference"] != other["source_reference"]:
                            continue

                        if change.get("source_type", "standalone") != other.get(
                            "source_type",
                            "standalone",
                        ):
                            continue

                        if change.get("source_type") == "object_corner":

                            if change.get("corner") != other.get("corner"):
                                continue

                            if change.get("direction") != other.get("direction"):
                                continue

                        if change.get("extensions") != other.get("extensions"):
                            continue

                        if change.get("stop_type") != other.get("stop_type"):
                            continue

                        found = True
                        break
                    elif change["change_type"] == "expand_objects":
                        if (
                            change["source_reference"] == other["source_reference"]
                            and change["target_color"] == other["target_color"]
                            and change["distance"] == other["distance"]
                        ):
                            found = True
                            break
                    elif change["change_type"] == "move_toward_object":
                        if (
                            change["source_reference"] == other["source_reference"]
                            and change.get("target_relationship") == other.get("target_relationship")
                            and change.get("target_reference") == other.get("target_reference")
                            and change.get("move_type", "until") == other.get("move_type", "until")
                            and change.get("stop_type") == other.get("stop_type")
                            and change["distance"] == other["distance"]
                        ):
                            found = True
                            break
                    elif change["change_type"] == "crop_to_bounded_region":

                        if (
                            change["marker_reference"] == other["marker_reference"]
                            and change["crop_area"] == other["crop_area"]
                            and change["recolor_to"] == other["recolor_to"]
                        ):
                            found = True
                            break

                if not found:
                    found_in_all = False
                    break

            if found_in_all:
                if change.get("exact_solution") == True:
                    validated_changes.append({
                        "change_type": change["change_type"],
                        "exact_solution": True,
                    })
                elif change["change_type"] == "copy_to_empty_half":
                    validated_changes.append({
                        "change_type": "copy_to_empty_half",
                        "axis": change["axis"],
                        "source_side": change["source_side"],
                        "target_side": change["target_side"],
                        "copy_transform": change["copy_transform"],
                    })
                elif change["change_type"] == "recolor_hollow_regions":

                    validated_changes.append({
                        "change_type": "recolor_hollow_regions",
                        "hollow_color": change["hollow_color"],
                        "exterior_color": change["exterior_color"],
                    })

                elif change["change_type"] == "recolor_hollow_objects":

                    validated_changes.append({
                        "change_type": "recolor_hollow_objects",
                        "source_color": change["source_color"],
                        "target_color": change["target_color"],
                    })
                elif(change["change_type"] == "color_mapping"):
                    validated_changes.append({
                        "change_type": "color_mapping",
                        "from_color": change["from_color"],
                        "to_color": change["to_color"],
                    })
                elif (change["change_type"] == "color_change"):
                    validated_change = {"change_type": "color_change" }
                    for key in color_change_keys:
                        if key in change:
                            validated_change[key] = change[key]
                    validated_changes.append(validated_change)
                    # validated_changes.append({"change_type": "color_change","source_reference": change["source_reference"],
                    #     "target_reference": change["target_reference"]})
                elif change["change_type"] == "make_hollow":
                    validated_changes.append({
                        "change_type": "make_hollow",
                        "source_reference": change["source_reference"],
                        "fill_color": change["fill_color"],
                    })
                elif change["change_type"] == "fill_in":
                    validated_changes.append({
                        "change_type": "fill_in",
                        "source_reference": change["source_reference"],
                    })
                elif(change["change_type"] == "crop_to_object"):
                    validated_changes.append({
                        "change_type": "crop_to_object",
                        "object_reference": change["object_reference"],
                    })
                elif change["change_type"] == "combine_regions":
                    validated_changes.append({
                        "change_type": "combine_regions",
                        "region2_transform": change["region2_transform"],
                        "operation": change["operation"],
                        "output_color": change["output_color"],
                    })
                elif change["change_type"] == "generate_from_seed":

                    validated_change = {
                        "change_type": "generate_from_seed",
                        "source_reference": change["source_reference"],
                        "source_type": change.get(
                            "source_type",
                            "standalone",
                        ),
                    }

                    if "extensions" in change:
                        validated_change["extensions"] = change["extensions"]

                    if "stop_type" in change:
                        validated_change["stop_type"] = change["stop_type"]

                    if "corner" in change:
                        validated_change["corner"] = change["corner"]

                    if "direction" in change:
                        validated_change["direction"] = change["direction"]

                    validated_changes.append(validated_change)
                elif change["change_type"] == "expand_objects":
                    validated_changes.append({
                        "change_type": "expand_objects",
                        "source_reference": change["source_reference"],
                        "target_color": change["target_color"],
                        "distance": change["distance"],
                    })
                elif change["change_type"] == "move_toward_object":

                    validated_change = {
                        "change_type": "move_toward_object",
                        "source_reference": change["source_reference"],
                        "move_type": change.get("move_type", "until"),
                        "distance": change["distance"],
                    }

                    if "target_relationship" in change:
                        validated_change["target_relationship"] = change["target_relationship"]

                    if "target_reference" in change:
                        validated_change["target_reference"] = change["target_reference"]

                    if "stop_type" in change:
                        validated_change["stop_type"] = change["stop_type"]

                    validated_changes.append(validated_change)
                elif change["change_type"] == "crop_to_bounded_region":

                    validated_changes.append({
                        "change_type": "crop_to_bounded_region",
                        "marker_reference": change["marker_reference"],
                        "crop_area": change["crop_area"],
                        "recolor_to": change["recolor_to"],
                    })
            specific_color_changes = []

            for change in validated_changes:

                if change["change_type"] == "recolor_hollow_objects":
                    specific_color_changes.append(
                        (
                            change["source_color"],
                            change["target_color"],
                        )
                    )

            filtered_changes = []

            for change in validated_changes:

                if change["change_type"] == "color_mapping":

                    color_pair = (
                        change["from_color"],
                        change["to_color"],
                    )

                    if color_pair in specific_color_changes:
                        continue

                filtered_changes.append(change)

            validated_changes = filtered_changes

        return validated_changes


        


    def get_grid_change_candidates(
        self,
        grid_transformations: list[dict],
        training_set: int,
    ) -> list[dict]:
        change_candidates = []
        exact_grid_changes = [
            "rotation_90",
            "rotation_180",
            "rotation_270",
            "flipped_h",
            "flipped_v",
            "flipped_h_rotation_90",
            "flipped_h_rotation_270",
        ]

        for preferred_change in exact_grid_changes:
            for transformation in grid_transformations:
                if transformation["transformation"] == preferred_change:
                    change_candidates.append({
                        "change_type": transformation["transformation"],
                        "exact_solution": True,
                        "training_set": training_set,
                    })
                    return change_candidates

        for transformation in grid_transformations:
            if transformation["transformation"] == "copy_to_empty_half":
                change_candidates.append({
                    "change_type": "copy_to_empty_half",
                    "axis": transformation["axis"],
                    "source_side": transformation["source_side"],
                    "target_side": transformation["target_side"],
                    "copy_transform": transformation["copy_transform"],
                    "training_set": training_set,
                })

            elif transformation["transformation"] == "crop_to_object":
                change_candidates.append({
                    "change_type": "crop_to_object",
                    "source_id": transformation["source_id"],
                    "object_reference": transformation["object_reference"],
                    "training_set": training_set,
                })
            elif transformation["transformation"] == "crop_to_bounded_region":

                change_candidates.append({
                    "change_type": "crop_to_bounded_region",
                    "marker_reference": transformation["marker_reference"],
                    "crop_area": transformation["crop_area"],
                    "recolor_to": transformation["recolor_to"],
                    "training_set": training_set,
                })
            elif transformation["transformation"] == "recolor_hollow_regions":
                change_candidates.append({
                    "change_type": "recolor_hollow_regions",
                    "hollow_color": transformation["hollow_color"],
                    "exterior_color": transformation["exterior_color"],
                    "training_set": training_set,
                })
            elif transformation["transformation"] == "recolor_hollow_objects":
                change_candidates.append({
                    "change_type": "recolor_hollow_objects",
                    "source_color": transformation["source_color"],
                    "target_color": transformation["target_color"],
                    "training_set": training_set,
                })

        return change_candidates

    def get_region_change_candidates(
        self,
        region_combo_transformations: list[dict],
        training_set: int,
    ) -> list[dict]:
        change_candidates = []
        region_transform_changes = [
            "same",
            "flipped_h",
            "flipped_v",
            "rotation_90",
            "rotation_180",
            "rotation_270",
        ]
        region_candidate_found = False

        for preferred_change in region_transform_changes:
            for transformation in region_combo_transformations:
                if transformation["region2_transform"] != preferred_change:
                    continue

                change_candidates.append({
                    "change_type": "combine_regions",
                    "region2_transform": transformation["region2_transform"],
                    "operation": transformation["operation"],
                    "output_color": transformation["output_color"],
                    "training_set": training_set,
                })

                region_candidate_found = True
                break

            if region_candidate_found:
                break

        return change_candidates

    def get_object_change_candidates(
        self,
        object_transformations: list[dict],
        training_set: int,
    ) -> list[dict]:
        change_candidates = []
        color_changes = {}
        make_hollow_count = 0
        fill_in_count = 0
        move_toward_object_found = False

        for transformation in object_transformations:
            if transformation["transformation"] == "make_hollow":
                make_hollow_count += 1
                continue
            elif transformation["transformation"] == "fill_in":
                fill_in_count += 1
                continue

            elif transformation["transformation"] == "generate_from_seed":

                change_candidate = {
                    "change_type": "generate_from_seed",
                    "source_reference": transformation["source_reference"],
                    "source_type": transformation.get(
                        "source_type",
                        "standalone",
                    ),
                    "training_set": training_set,
                }

                if "extensions" in transformation:
                    change_candidate["extensions"] = transformation["extensions"]

                if "direction" in transformation:
                    change_candidate["direction"] = transformation["direction"]

                if "corner" in transformation:
                    change_candidate["corner"] = transformation["corner"]

                if "stop_type" in transformation:
                    change_candidate["stop_type"] = transformation["stop_type"]

                change_candidates.append(change_candidate)

            elif transformation["transformation"] == "expand_objects":
                change_candidates.append({
                    "change_type": "expand_objects",
                    "source_reference": transformation["source_reference"],
                    "target_color": transformation["target_color"],
                    "distance": transformation["distance"],
                    "training_set": training_set,
                })
                continue
            elif transformation["transformation"] == "move_toward_object":

                if move_toward_object_found:
                    continue

                change_candidate = {
                    "change_type": "move_toward_object",
                    "source_reference": transformation["source_reference"],
                    "move_type": transformation.get("move_type", "until"),
                    "distance": transformation["distance"],
                    "training_set": training_set,
                }

                if "target_relationship" in transformation:
                    change_candidate["target_relationship"] = transformation["target_relationship"]

                if "target_reference" in transformation:
                    change_candidate["target_reference"] = transformation["target_reference"]

                if "stop_type" in transformation:
                    change_candidate["stop_type"] = transformation["stop_type"]

                change_candidates.append(change_candidate)

                move_toward_object_found = True
                continue


            if(transformation["transformation"] != "color_change"):
                continue

            if (transformation["source_reference"] is not None
                and transformation["target_reference"] is not None):
                change_candidates.append({
                    "change_type": "color_change",
                    "source_reference": transformation["source_reference"],
                    "target_reference": transformation["target_reference"],
                    "training_set": training_set,
                })

            color_change = (transformation["from_color"], transformation['to_color'])

            if color_change not in color_changes:
                color_changes[color_change] = 0

            color_changes[color_change] +=1



        for color_change, count in color_changes.items():
            change_candidates.append({
                "change_type": "color_mapping",
                "from_color": color_change[0],
                "to_color": color_change[1],
                "count_objects": count,
                "training_set": training_set,
            })

        if (len(object_transformations) > 0 ):
            if(make_hollow_count == len(object_transformations)):

                change_candidates.append({
                    "change_type": "make_hollow",
                    "source_reference": "all_objects",
                    "fill_color": 0,
                    "training_set": training_set,
                })
            elif(fill_in_count == len(object_transformations)):
                change_candidates.append({
                    "change_type": "fill_in",
                    "source_reference": "all_objects",
                    "training_set": training_set,
                })
            
        return change_candidates

    def get_color_change_candidates(
        self,
        color_mappings: list[dict],
        training_set: int,
    ) -> list[dict]:
        change_candidates = []

        for start_mapping in color_mappings:
            for next_mapping in color_mappings:
                if start_mapping == next_mapping:
                    continue

                if(start_mapping["to_color"] == next_mapping["from_color"] and next_mapping["to_color"] == 0):
                    change_candidates.append({
                        "change_type": "color_change",
                        "source_color": start_mapping["from_color"],
                        "target_reference": "mapped_color",
                        "training_set": training_set,
                    })

                    change_candidates.append({
                        "change_type": "color_change",
                        "source_reference": "mapped_color",
                        "target_color": 0,
                        "training_set": training_set,
                    })

        return change_candidates

    def get_change_candidates(
        self,
        analysis: ProblemAnalysis,
        training_set: int,
    ) -> list[dict]:
        change_candidates = []

        grid_candidates = self.get_grid_change_candidates(
            analysis.grid_transformations,
            training_set,
        )
        if any(candidate.get("exact_solution") for candidate in grid_candidates):
            return grid_candidates
        change_candidates.extend(grid_candidates)

        region_candidates = self.get_region_change_candidates(
            analysis.region_transformations,
            training_set,
        )
        change_candidates.extend(region_candidates)

        object_candidates = self.get_object_change_candidates(
            analysis.object_transformations,
            training_set,
        )
        secondary_object_candidates = []
        for candidate in object_candidates:
            if candidate["change_type"] in ("make_hollow", "fill_in"):
                secondary_object_candidates.append(candidate)
            else:
                change_candidates.append(candidate)

        color_candidates = self.get_color_change_candidates(
            analysis.color_mappings,
            training_set,
        )
        change_candidates.extend(color_candidates)

        change_candidates.extend(secondary_object_candidates)
        return change_candidates
    
    
    def get_input_output_transformations(self, input_shapes: list[Shape], output_shapes: list[Shape],input_object_relationships: list[dict],input_output_relationships: list[dict], input_grid: np.ndarray, output_grid: np.ndarray) -> list[dict]:
        transformations = []
        relationship_pairs = {}
        input_shapes_map = {}
        output_shapes_map = {}

        for relationship in input_output_relationships:
            source_id = relationship["source_id"]
            target_id = relationship["target_id"]
            

            for shape in input_shapes:
                input_shapes_map[shape.object_id] = shape

            for shape in output_shapes:
                output_shapes_map[shape.object_id] = shape

            pair = (source_id, target_id)
            if pair not in relationship_pairs:
                relationship_pairs[pair] = []
            relationship_pairs[pair].append(relationship)

        for pair, relationships in relationship_pairs.items():
            same_color = False
            different_color = False
            same_shape = False

            for relationship in relationships:
                if(relationship["relationship_type"] == "color" and relationship["relationship_degree"] == "same_color"):
                    same_color = True
                elif(relationship["relationship_type"] == "color" and relationship["relationship_degree"] == "different_color"):
                    different_color = True
                if(relationship["relationship_type"] == "shape" and relationship["relationship_degree"] == "same"):
                    same_shape = True

            source_shape = input_shapes_map[pair[0]]
            target_shape = output_shapes_map[pair[1]]
            source_cells = set(source_shape.cells)
            target_cells = set(target_shape.cells)

            if(same_color and source_shape.is_hollow != target_shape.is_hollow):
                transformation = None
                if(source_shape.is_hollow == False and target_cells.issubset(source_cells)):
                    transformation = "make_hollow"
                if(source_shape.is_hollow == True and source_cells.issubset(target_cells)):
                    transformation = "fill_in"
                if transformation is not None:
                    transformations.append({
                        "transformation_type": "object",
                        "transformation": transformation,
                        "source_reference": self.get_object_reference(
                            source_shape,
                            input_shapes,
                        ),
                        "source_id": pair[0],
                        "target_id": pair[1],
                    })

            same_grid_size = input_grid.shape == output_grid.shape

            if (
                same_color
                and same_shape
                and (
                    not same_grid_size
                    or (
                        source_shape.top == target_shape.top
                        and source_shape.left == target_shape.left
                    )
                )
            ):
                transformations.append({
                    "transformation_type": "object",
                    "transformation": "none",
                    "source_id": pair[0],
                    "target_id": pair[1],
                })
            elif (
                same_shape
                and different_color
                and (
                    not same_grid_size
                    or (
                        source_shape.top == target_shape.top
                        and source_shape.left == target_shape.left
                    )
                )
            ):
                source_reference = self.get_object_reference(source_shape,input_shapes)
                target_reference = None

                for input_shape in input_shapes:
                    if(input_shape.color != target_shape.color):
                        continue

                    target_reference = self.get_object_reference(input_shape, input_shapes)
                    if target_reference is not None:
                        break

                transformations.append({
                    "transformation_type": "object",
                    "transformation": "color_change",
                    "source_reference": source_reference,
                    "target_reference": target_reference,
                    "from_color": source_shape.color,
                    "to_color": target_shape.color,
                    "source_id": pair[0],
                    "target_id": pair[1],
                })

            if same_color and len(source_shape.cells) == 1 and len(target_shape.cells) > 1:
                direction_offsets = {
                    "up": (-1, 0),
                    "down": (1, 0),
                    "left": (0, -1),
                    "right": (0, 1),
                    "upper_left": (-1, -1),
                    "upper_right": (-1, 1),
                    "lower_left": (1, -1),
                    "lower_right": (1, 1),
                }
                seed_row, seed_column = source_shape.cells[0]
                expected_cells = {(seed_row, seed_column)}
                extensions = []
                grid_height, grid_width = output_grid.shape

                for direction_name, (row_offset, column_offset) in direction_offsets.items():
                    adjacent_row = seed_row + row_offset
                    adjacent_column = seed_column + column_offset

                    if (adjacent_row < 0 or adjacent_row >= grid_height
                        or adjacent_column < 0 or adjacent_column >= grid_width):
                        continue

                    adjacent_cell = (adjacent_row, adjacent_column)
                    if adjacent_cell not in target_cells:
                        continue

                    ray_cells = []
                    current_row = adjacent_row
                    current_column = adjacent_column
                    complete_ray = True

                    while (0 <= current_row < grid_height
                           and 0 <= current_column < grid_width):
                        current_cell = (current_row, current_column)
                        if current_cell not in target_cells:
                            complete_ray = False
                            break

                        ray_cells.append(current_cell)
                        current_row += row_offset
                        current_column += column_offset

                    if complete_ray:
                        expected_cells.update(ray_cells)
                        extensions.append({
                            "direction": direction_name,
                            "stop_type": "grid_edge",
                        })

                if len(extensions) > 0 and expected_cells == target_cells:
                    transformations.append({
                        "transformation_type": "object",
                        "transformation": "generate_from_seed",
                        "source_reference": self.get_object_reference(
                            source_shape,
                            input_shapes,
                        ),
                        "color": source_shape.color,
                        "extensions": extensions,
                        "source_id": pair[0],
                        "target_id": pair[1],
                    })
            
        if len(input_shapes) > 0:

            first_shape = input_shapes[0]

            same_source_pattern = True

            for shape in input_shapes:
                if (
                    shape.height != first_shape.height
                    or shape.width != first_shape.width
                    or len(shape.cells) != len(first_shape.cells)
                    or shape.color != first_shape.color
                ):
                    same_source_pattern = False
                    break

            if same_source_pattern:

                output_colors = np.unique(output_grid)
                non_background_colors = []

                for color in output_colors:
                    if color != 0:
                        non_background_colors.append(int(color))

                if len(non_background_colors) == 1:
                    target_color = non_background_colors[0]

                    grid_height, grid_width = output_grid.shape

                    max_distance = max(grid_height, grid_width)

                    for distance in range(1, max_distance + 1):

                        expected_cells = set()

                        for shape in input_shapes:
                            for row, column in shape.cells:

                                for row_offset in range(-distance, distance + 1):
                                    for column_offset in range(-distance, distance + 1):

                                        new_row = row + row_offset
                                        new_column = column + column_offset

                                        if (
                                            0 <= new_row < grid_height
                                            and 0 <= new_column < grid_width
                                        ):
                                            expected_cells.add(
                                                (new_row, new_column)
                                            )

                        actual_cells = set()

                        for row in range(grid_height):
                            for column in range(grid_width):
                                if output_grid[row, column] == target_color:
                                    actual_cells.add((row, column))

                        if expected_cells == actual_cells:
                            transformations.append({
                                "transformation_type": "object",
                                "transformation": "expand_objects",
                                "source_reference": {
                                    "scope": "all_matching",
                                    "height": first_shape.height,
                                    "width": first_shape.width,
                                    "cell_count": len(first_shape.cells),
                                    "color": first_shape.color,
                                },
                                "target_color": target_color,
                                "distance": distance,
                            })

                            break

            for source_shape in input_shapes:

                if len(source_shape.cells) != 1:
                    continue

                source_relationships = []

                for relationship in input_object_relationships:
                    if relationship["source_id"] == source_shape.object_id:
                        source_relationships.append(relationship)

                for relationship in source_relationships:

                    if relationship["relationship_type"] != "color":
                        continue

                    if relationship["relationship_degree"] != "same_color":
                        continue

                    target_id = relationship["target_id"]

                    target_shape = None

                    for shape in input_shapes:
                        if shape.object_id == target_id:
                            target_shape = shape
                            break

                    if target_shape is None:
                        continue

                    # Don't treat another single-cell object as the movement target.
                    if len(target_shape.cells) == 1:
                        continue

                    source_row, source_column = source_shape.cells[0]

                    moved_row = None
                    moved_column = None
                    move_direction = None

                    if (
                        target_shape.left == target_shape.right
                        and target_shape.top <= source_row <= target_shape.bottom
                    ):
                        if source_column < target_shape.left:
                            moved_row = source_row
                            moved_column = target_shape.left - 1
                            move_direction = "right"

                        elif source_column > target_shape.right:
                            moved_row = source_row
                            moved_column = target_shape.right + 1
                            move_direction = "left"

                    elif (
                        target_shape.top == target_shape.bottom
                        and target_shape.left <= source_column <= target_shape.right
                    ):
                        if source_row < target_shape.top:
                            moved_row = target_shape.top - 1
                            moved_column = source_column
                            move_direction = "down"

                        elif source_row > target_shape.bottom:
                            moved_row = target_shape.bottom + 1
                            moved_column = source_column
                            move_direction = "up"

                    if (
                        moved_row is not None
                        and moved_column is not None
                        and 0 <= moved_row < output_grid.shape[0]
                        and 0 <= moved_column < output_grid.shape[1]
                        and output_grid[moved_row, moved_column] == source_shape.color
                    ):
                        transformations.append({
                            "transformation_type": "object",
                            "transformation": "move_toward_object",
                            "source_reference": {
                                "cell_count": 1,
                            },
                            "target_relationship": {
                                "relationship_type": relationship["relationship_type"],
                                "relationship_degree": relationship["relationship_degree"],
                            },
                            "stop_type": "before_target",
                            "distance": 1,
                            "source_id": source_shape.object_id,
                            "target_id": target_shape.object_id,
                        })
            for source_shape in input_shapes:

                moved_output_shape = None

                for output_shape in output_shapes:

                    if source_shape.color != output_shape.color:
                        continue

                    if source_shape.pattern.shape != output_shape.pattern.shape:
                        continue

                    if not np.array_equal(source_shape.pattern, output_shape.pattern):
                        continue

                    if (
                        source_shape.top == output_shape.top
                        and source_shape.left == output_shape.left
                    ):
                        continue

                    moved_output_shape = output_shape
                    break

                if moved_output_shape is None:
                    continue
                for target_shape in input_shapes:

                    if target_shape.object_id == source_shape.object_id:
                        continue

                    target_is_stationary = False

                    for output_shape in output_shapes:

                        if target_shape.color != output_shape.color:
                            continue

                        if not np.array_equal(target_shape.pattern, output_shape.pattern):
                            continue

                        if (
                            target_shape.top == output_shape.top
                            and target_shape.left == output_shape.left
                        ):
                            target_is_stationary = True
                            break

                    if not target_is_stationary:
                        continue

                    row_step = 0
                    column_step = 0

                    if target_shape.top > source_shape.top:
                        row_step = 1
                    elif target_shape.top < source_shape.top:
                        row_step = -1

                    if target_shape.left > source_shape.left:
                        column_step = 1
                    elif target_shape.left < source_shape.left:
                        column_step = -1

                    expected_row = source_shape.top + row_step
                    expected_column = source_shape.left + column_step

                    if (
                        moved_output_shape.top == expected_row
                        and moved_output_shape.left == expected_column
                    ):
                        transformations.append({
                            "transformation_type": "object",
                            "transformation": "move_toward_object",
                            "source_reference": {
                                "color": source_shape.color,
                                "cell_count": len(source_shape.cells),
                            },
                            "target_reference": {
                                "color": target_shape.color,
                                "cell_count": len(target_shape.cells),
                            },
                            "move_type": "step",
                            "distance": 1,
                            "source_id": source_shape.object_id,
                            "target_id": target_shape.object_id,
                        })
            if input_grid.shape == output_grid.shape:
                for row in range(input_grid.shape[0]):
                    for column in range(input_grid.shape[1]):

                        input_color = input_grid[row, column]
                        output_color = output_grid[row, column]

                        if input_color == 0:
                            continue

                        if input_color != output_color:
                            continue

                        ray_color = int(input_color)

                        directions = {
                            "up": (-1, 0),
                            "down": (1, 0),
                            "left": (0, -1),
                            "right": (0, 1),
                        }

                        for direction, (row_offset, column_offset) in directions.items():

                            generated_grid = input_grid.copy()
                            painted_cells = 0

                            current_row = row + row_offset
                            current_column = column + column_offset

                            while (
                                0 <= current_row < input_grid.shape[0]
                                and 0 <= current_column < input_grid.shape[1]
                            ):

                                if generated_grid[current_row, current_column] == 0:
                                    generated_grid[current_row, current_column] = ray_color
                                    painted_cells += 1

                                current_row += row_offset
                                current_column += column_offset

                            if painted_cells == 0:
                                continue
                            if not np.array_equal(
                                generated_grid,
                                output_grid,
                            ):
                                continue
                            transformations.append({
                                "transformation_type": "object",
                                "transformation": "generate_from_seed",
                                "source_type": "embedded",
                                "source_reference": {
                                    "cell_count": 1,
                                },
                                "direction": direction,
                                "stop_type": "grid_edge",
                                "source_color": ray_color,
                            })
            if input_grid.shape == output_grid.shape:

                    corner_rules = [
                        {
                            "color": 1,
                            "corner": "top_left",
                            "direction": "upper_left",
                            "row_offset": -1,
                            "column_offset": -1,
                        },
                        {
                            "color": 2,
                            "corner": "bottom_right",
                            "direction": "lower_right",
                            "row_offset": 1,
                            "column_offset": 1,
                        },
                    ]

                    for rule in corner_rules:

                        for shape in input_shapes:

                            if shape.color != rule["color"]:
                                continue

                            if shape.height != 2 or shape.width != 2:
                                continue

                            if rule["corner"] == "top_left":
                                start_row = shape.top
                                start_column = shape.left

                            else:
                                start_row = shape.bottom
                                start_column = shape.right

                            current_row = start_row + rule["row_offset"]
                            current_column = start_column + rule["column_offset"]

                            added_cells = 0

                            while (
                                0 <= current_row < input_grid.shape[0]
                                and 0 <= current_column < input_grid.shape[1]
                            ):

                                if (
                                    input_grid[current_row, current_column] == 0
                                    and output_grid[current_row, current_column] == shape.color
                                ):
                                    added_cells += 1

                                current_row += rule["row_offset"]
                                current_column += rule["column_offset"]

                            if added_cells == 0:
                                continue

                            
                            transformations.append({
                                "transformation_type": "object",
                                "transformation": "generate_from_seed",
                                "source_type": "object_corner",
                                "source_reference": {
                                    "color": shape.color,
                                    "height": shape.height,
                                    "width": shape.width,
                                    "cell_count": len(shape.cells),
                                },
                                "corner": rule["corner"],
                                "direction": rule["direction"],
                                "stop_type": "grid_edge",
                            })
                            # with open("debug_output.txt", "a") as debug_file:
                            #     print("RAY SOURCE FOUND", file=debug_file)
                            #     print(
                            #         f"source color = {ray_color}",
                            #         file=debug_file,
                            #     )
                            #     print(
                            #         f"source cell = {(row, column)}",
                            #         file=debug_file,
                            #     )
                            #     print(
                            #         f"direction = {direction}",
                            #         file=debug_file,
                            #     )
        return transformations

    def get_object_to_object_relationships(self, shapes: list[Shape], target_shapes: list[Shape] = None) -> list[dict]:
        relationships = []
        if target_shapes is None:
            target_shapes = shapes
            same_source = True
        else:
            same_source = False

        for source_shape in shapes:
            for target_shape in target_shapes:

                if (same_source and source_shape.id == target_shape.id):
                    continue

                if same_source:
                    position_relationships = self.get_object_object_positions(source_shape, target_shape)
                    relationships.extend(position_relationships)

                
                region_relationships = self.get_object_object_regions(source_shape, target_shape)
                relationships.extend(region_relationships)

                color_relationships = self.get_object_object_colors(source_shape, target_shape)
                relationships.extend(color_relationships)

                shape_relationships = self.get_object_object_shapes(source_shape, target_shape)
                relationships.extend(shape_relationships)

        return relationships

    def get_object_object_shapes(self, source_shape: Shape, target_shape: Shape):
        shape_relationships =[]
        source_pattern = source_shape.pattern
        target_pattern = target_shape.pattern
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
                    "source_id": source_shape.object_id,
                    "relationship_type": "shape",
                    "relationship_degree": degree,
                    "target_item": "object",
                    "target_id": target_shape.object_id
                })  
                if "same" == degree:
                    return shape_relationships    

        return shape_relationships


    def get_object_object_colors(self, source_shape: Shape, target_shape: Shape):
        color_relationships = []

        if source_shape.color == target_shape.color:
            relationship_degree = "same_color"
        else:
            relationship_degree = "different_color"

        color_relationships.append({
            "source_item": "object",
            "source_id": source_shape.object_id,
            "relationship_type": "color",
            "relationship_degree": relationship_degree,
            "target_item": "object",
            "target_id": target_shape.object_id
        })

        return color_relationships

    def get_object_object_regions(self, source_shape: Shape, target_shape: Shape):
        region_relationships = []
        if (
            source_shape.region_id is not None
            and target_shape.region_id is not None
            and source_shape.region_id == target_shape.region_id
        ):
            region_relationships.append({
                "source_item": "object",
                "source_id": source_shape.object_id,
                "relationship_type": "region",
                "relationship_degree": "same_region",
                "target_item": "object",
                "target_id": target_shape.object_id
            })

        return region_relationships
    
    def get_object_object_positions(self, source_shape: Shape, target_shape: Shape):
        position_relationships = []
        if(source_shape.right < target_shape.left):
            position_relationships.append({
                "source_item": "object",
                "source_id": source_shape.object_id,
                "relationship_type": "position",
                "relationship_degree": "left_of",
                "target_item": "object",
                "target_id": target_shape.object_id
            })

        if(source_shape.left > target_shape.right):
            position_relationships.append({
                "source_item": "object",
                "source_id": source_shape.object_id,
                "relationship_type": "position",
                "relationship_degree": "right_of",
                "target_item": "object",
                "target_id": target_shape.object_id
            })

        if source_shape.bottom < target_shape.top:
            position_relationships.append({
                "source_item": "object",
                "source_id": source_shape.object_id,
                "relationship_type": "position",
                "relationship_degree": "above",
                "target_item": "object",
                "target_id": target_shape.object_id
            })

        if source_shape.top > target_shape.bottom:
            position_relationships.append({
                "source_item": "object",
                "source_id": source_shape.object_id,
                "relationship_type": "position",
                "relationship_degree": "below",
                "target_item": "object",
                "target_id": target_shape.object_id
            })

        return position_relationships

    def get_shape_regions(self, shapes: list[Shape], regions:list[dict]):

        for shape in shapes:
            shape.region_id = None

            for region in regions:
                contains_shape = (
                    shape.top >= region["parent_top"]
                    and shape.bottom <= region["parent_bottom"]
                    and shape.left >= region["parent_left"]
                    and shape.right <= region["parent_right"]
                )

                if contains_shape:
                    shape.region_id = region["grid_id"]
                    break


    def get_grid_regions(self, grid: np.ndarray, parent_grid_id: str, shapes: list[Shape], relationships: list[dict]) -> list[dict]:
        # TODO figure out how to properly handle cross grid dividers, my dumbass forgot that we're identifying objects by colors
        # maybe something like if goes across grid with consistent width, except at intersection point then it's a multi-region divider
        # i dunno, but that might work. crap, what if we have different colors that cross but act as divider. dang this is annoying
        regions = []
        vertical_dividers = []
        horizontal_dividers = []
        region_number = 1
        for relationship in relationships:
            if(relationship["relationship"] != "divides_grid"):
                continue

            divider = None

            for shape in shapes:
                if(shape.object_id == relationship["source_id"]):
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

        vertical_dividers.sort(key=lambda shape: shape.left)
        horizontal_dividers.sort(key=lambda shape: shape.top)

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
        #         end_column = divider.left
        #         region_grid = grid[:, start_column:end_column]

        #         if region_grid.shape[1] > 0:
        #             region_id = parent_grid_id+"_region_"+str(region_number)

        #             regions.append(self.analyze_grid(region_grid, region_id, "region", parent_grid_id, 0, grid.shape[0]-1,start_column, end_column-1))
        #             region_number +=1

        #         start_column = divider.right+1

        #     if start_column < grid.shape[1]:
        #         region_grid = grid[:,start_column:]
        #         region_id = region_id = parent_grid_id+"_region_"+str(region_number)
        #         regions.append(self.analyze_grid(region_grid, region_id, "region", parent_grid_id,0, grid.shape[0]-1,start_column, grid.shape[1]-1))

        # if horizontal_dividers:
        #     start_row = 0
        #     region_number = 1

        #     for divider in horizontal_dividers:
        #         end_row = divider.top
        #         region_grid = grid[start_row:end_row,:]

        #         if region_grid.shape[0] > 0:
        #             region_id = parent_grid_id+"_region_"+str(region_number)

        #             regions.append(self.analyze_grid(region_grid, region_id, "region", parent_grid_id, start_row, end_row-1, 0, grid.shape[1]-1))
        #             region_number +=1

        #         start_row = divider.bottom+1

        #     if start_row < grid.shape[0]:
        #             region_grid = grid[start_row:,:]
        #             region_id = parent_grid_id+"_region_"+str(region_number)
        #             regions.append(self.analyze_grid(region_grid, region_id, "region", parent_grid_id,start_row,grid.shape[0]-1,0,grid.shape[1]-1))

        return regions

    def get_row_splits(self, grid:np.ndarray, horizontal_dividers: list[Shape]) -> list[tuple[int,int]]:
        row_splits = []
        start_row = 0

        for divider in horizontal_dividers:
            end_row = divider.top-1

            if (start_row <= end_row):
                row_splits.append((start_row, end_row))

            start_row = divider.bottom+1

        if(start_row <= grid.shape[0] -1):
            row_splits.append((start_row, grid.shape[0]-1))

        return row_splits

    def get_column_splits(self, grid:np.ndarray, vertical_dividers: list[Shape]) -> list[tuple[int,int]]:
        column_splits = []
        start_column = 0

        for divider in vertical_dividers:
            end_column = divider.left-1

            if (start_column <= end_column):
                column_splits.append((start_column, end_column))

            start_column = divider.right+1

        if(start_column <= grid.shape[1] -1):
            column_splits.append((start_column, grid.shape[1]-1))

        return column_splits


    def get_object_grid_relationships(self, grid: np.ndarray, shapes: list[Shape]) -> list[dict]:
        relationships = []

        for shape in shapes:
            fills_grid = (shape.top == 0 and shape.bottom == grid.shape[0]-1 and shape.left == 0 and shape.right ==grid.shape[1]-1)

            if fills_grid:
                relationship = {
                    "source_item": "object",
                    "source_id": shape.object_id,
                    "relationship": "fills_grid",
                    "target_item": "grid"
                }
                relationships.append(relationship)

            divides_grid_vertical = (shape.top == 0 and shape.bottom == grid.shape[0] - 1 and shape.width == 1 and shape.left > 0 and shape.right < grid.shape[1] - 1)
            if divides_grid_vertical:
                relationship = {
                    "source_item": "object",
                    "source_id": shape.object_id,
                    "relationship": "divides_grid",
                    "target_item": "grid",
                    "orientation": "vertical",
                    "region_count": 2
                }
                relationships.append(relationship)

            divides_grid_horizontal = (shape.top > 0 and shape.bottom < grid.shape[0] - 1 and shape.height == 1 and shape.left == 0 and shape.right == grid.shape[1] - 1)
            if divides_grid_horizontal:
                relationship = {
                    "source_item": "object",
                    "source_id": shape.object_id,
                    "relationship": "divides_grid",
                    "target_item": "grid",
                    "orientation": "horizontal",
                    "region_count": 2
                }
                relationships.append(relationship)

        return relationships

    def identify_shapes(self, grid: np.ndarray, parent_grid_id: str, connections: int = 8) -> list[Shape]:

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

                shape = Shape(
                    id=shape_id,
                    object_id=parent_grid_id + "_object_" + str(shape_id),
                    parent_grid_id=parent_grid_id,
                    color=color,
                    cells=cells,
                    pattern=pattern,
                    top=boundaries["top"],
                    bottom=boundaries["bottom"],
                    left=boundaries["left"],
                    right=boundaries["right"],
                    height=boundaries["height"],
                    width=boundaries["width"],
                    is_hollow=False,
                )
                shape.is_hollow = self.is_hollow(grid, shape)
                shapes.append(shape)

                shape_id +=1
        return shapes

    def is_hollow(self, grid: np.ndarray, shape: Shape) -> bool:
        hollow_regions = self.get_hollow_regions(grid, shape)
        return len(hollow_regions) > 0

    def get_hollow_regions(
            self,
            grid: np.ndarray,
            shape: Shape,
        ) -> list[list[tuple[int, int]]]:

            hollow_regions = []
            visited = set()
            colors, counts = np.unique(
                grid,
                return_counts=True,
            )

            background_color = int(
                colors[np.argmax(counts)]
            )

            top = shape.top
            bottom = shape.bottom
            left = shape.left
            right = shape.right

            shape_cells = set(shape.cells)

            directions = [
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1),
            ]

            for row in range(top, bottom + 1):
                for column in range(left, right + 1):

                    if (row, column) in shape_cells:
                        continue

                    if (row, column) in visited:
                        continue

                    if grid[row, column] != background_color:
                        continue

                    region = []
                    region_stack = [(row, column)]
                    touches_boundary = False

                    while region_stack:

                        current_row, current_column = region_stack.pop()

                        if (current_row, current_column) in visited:
                            continue

                        visited.add(
                            (current_row, current_column)
                        )

                        region.append(
                            (current_row, current_column)
                        )

                        if (
                            current_row == top
                            or current_row == bottom
                            or current_column == left
                            or current_column == right
                        ):
                            touches_boundary = True

                        for row_offset, column_offset in directions:

                            next_row = current_row + row_offset
                            next_column = current_column + column_offset

                            if (
                                next_row < top
                                or next_row > bottom
                                or next_column < left
                                or next_column > right
                            ):
                                continue

                            if (
                                next_row,
                                next_column,
                            ) in visited:
                                continue

                            if (
                                next_row,
                                next_column,
                            ) in shape_cells:
                                continue

                            if grid[next_row, next_column] != background_color:
                                continue

                            region_stack.append(
                                (next_row, next_column)
                            )

                    if not touches_boundary:
                        hollow_regions.append(region)

            return hollow_regions
    # def is_hollow(self, grid: np.ndarray, shape: Shape) -> bool:
        # color = shape.color
        # cells = shape.cells
        # top = shape.top
        # bottom = shape.bottom
        # left = shape.left
        # right = shape.right

        # for row in range(top,bottom+1):
        #     for column in range(left,right+1):
        #         current_cell = (row, column)
        #         if current_cell in cells:
        #             continue

        #         top_blocked = False
        #         bottom_blocked = False
        #         left_blocked = False
        #         right_blocked = False

        #         for row_to_check in range(row-1, top -1, -1):
        #             if(grid[row_to_check, column] == color):
        #                 top_blocked = True
        #                 break

        #         for row_to_check in range(row+1, bottom+1,1):
        #             if(grid[row_to_check, column] == color):
        #                 bottom_blocked = True
        #                 break

        #         for column_to_check in range(column-1, left-1,-1):
        #             if(grid[row, column_to_check] == color):
        #                 left_blocked = True
        #                 break

        #         for column_to_check in range(column+1, right+1,1):
        #             if(grid[row, column_to_check] == color):
        #                 right_blocked = True
        #                 break

        #         if top_blocked and bottom_blocked and left_blocked and right_blocked:
        #             return True
                
        # return False



    def get_shape_boundaries(self, cells: list[tuple[int, int]]) -> dict:
        rows =  [cell[0] for cell in cells]
        columns = [cell[1] for cell in cells]

        top = min(rows)
        bottom = max(rows)
        left = min(columns)
        right = max(columns)
        height = bottom-top+1
        width = right-left+1

        return {
            "top": top,
            "bottom": bottom,
            "left": left,
            "right": right,
            "height": height,
            "width": width,
        }



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
                full_rows.append({
                    "index": row,
                    "color": current_row[0].item(),
                })

        for column in range(grid.shape[1]):
            current_column = grid[:, column]

            if np.all(current_column == current_column[0]):
                full_columns.append({
                    "index": column,
                    "color": current_column[0].item(),
                })

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

    