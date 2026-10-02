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
        with open("debug_output.txt", "w") as debug_file:
            pass
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

        target_problem = "4347f46a"
        target_training_sets = {1, 2, 3}
        training_change_candidates = []     

        count = 1

        for training_set in training_sets:
            input_grid = training_set.get_input_data().data()
            output_grid = training_set.get_output_data().data()

            input_grid_id = "input_grid_" + str(count)
            output_grid_id = "output_grid_" + str(count)

            input_grid_analysis = self.analyze_grid(input_grid, input_grid_id, "full")
            output_grid_analysis = self.analyze_grid(output_grid, output_grid_id, "full")
            input_shapes = self.identify_shapes(input_grid, input_grid_id)
            output_shapes = self.identify_shapes(output_grid, output_grid_id)
            input_relationships = self.get_object_grid_relationships(input_grid, input_shapes)
            output_relationships = self.get_object_grid_relationships(output_grid,output_shapes)
            input_regions = self.get_grid_regions(input_grid, input_grid_id, input_shapes, input_relationships)
            output_regions = self.get_grid_regions(output_grid, output_grid_id, output_shapes, output_relationships)
            self.get_shape_regions(input_shapes,input_regions)
            self.get_shape_regions(output_shapes,output_regions)
            input_object_relationships = self.get_object_to_object_relationships(input_shapes)
            output_object_relationships = self.get_object_to_object_relationships(output_shapes)
            input_output_object_relationships = self.get_object_to_object_relationships(input_shapes, output_shapes)
            input_output_transformations = self.get_input_output_transformations(input_shapes, output_shapes,input_output_object_relationships)
            grid_transformations = self.get_grid_transformations(input_grid_analysis, output_grid_analysis, input_shapes, output_shapes, input_output_transformations)
            color_mappings = self.get_color_mappings(input_grid,output_grid)
            change_candidates = self.get_change_candidates(input_output_transformations,grid_transformations,color_mappings,count)
            training_change_candidates.append(change_candidates)
            
            
            
            if (
                arc_problem.problem_name() == target_problem
                and count in target_training_sets
            ):
                with open("debug_output.txt", "a") as debug_file:
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

                    # for relationship in input_output_object_relationships:
                    #     self.print_frame(relationship, "INPUT-OUTPUT OBJECT RELATIONSHIPS", debug_file)

                    for transformation in input_output_transformations:
                        self.print_frame(transformation, "INPUT-OUTPUT OBJECT TRANSFORMATIONS", debug_file)

                    for transformation in grid_transformations:
                        self.print_frame(transformation, "GRID TRANSFORMATIONS", debug_file)

                    for change in change_candidates:
                        self.print_frame(change, "CHANGE CANDIDATES", debug_file)

                    for mapping in color_mappings:
                        print("COLOR MAPPING", file=debug_file)
                        for key, value in mapping.items():
                            print(key, "=", value, file=debug_file)          

                    # for change in validated_changes:
                    #     self.print_frame(change, "VALIDATED_CHANGES", debug_file)


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

        if (
            arc_problem.problem_name() == target_problem
        ):
            with open("debug_output.txt", "a") as debug_file:
                for prediction in my_predictions:
                    print(f"\nPREDICTION: {prediction}", file=debug_file)

        predictions.append(my_predictions)
        output = np.zeros_like(arc_problem.test_set().get_input_data().data())
        predictions.append(output)

        return predictions

    def print_frame(self, frame: dict, label: str = "", file=None):

        if label:
            print(label, file=file)

        for key, value in frame.items():
            print(f"{key} = {value}", file=file)

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
                    mappings.append({"from_color": int(color), "to_color": int(output_color)})

        return mappings


    def get_shape_by_reference(self, shapes:list[dict], reference: str)->dict|None:
        if not shapes:
            return None
        
        if(reference == "single"):
            if(len(shapes)==1):
                return shapes[0]
        elif reference == "largest":
            largest_shape = shapes[0]
            largest_size = largest_shape["height"] * largest_shape["width"]
            largest_count = 1

            for shape in shapes[1:]:
                size = shape["height"] * shape["width"]

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
            smallest_size = smallest_shape["height"] * smallest_shape["width"]
            smallest_count = 1

            for shape in shapes[1:]:
                size = shape["height"] * shape["width"]

                if (size < smallest_size):
                    smallest_shape = shape
                    smallest_size = size
                    smallest_count = 1

                elif size == smallest_size:
                    smallest_count += 1

            if smallest_count == 1:
                return smallest_shape

        return None


    def get_grid_transformations(self, input_grid_analysis: dict, output_grid_analysis: dict, 
                                 input_shapes: list[dict], output_shapes: list[dict],
                                 input_output_transformations)-> list[dict]:
        transformations = []
        input_shapes_map = {}
        output_shapes_map = {}

        for shape in input_shapes:
            input_shapes_map[shape["object_id"]] = shape

        for shape in output_shapes:
            output_shapes_map[shape["object_id"]] = shape

        for transformation in input_output_transformations:
            if transformation["transformation"] not in ("none", "color_change"):
                continue
            source_shape = input_shapes_map[transformation["source_id"]]
            object_reference = self.get_object_reference(source_shape, input_shapes)

            if(object_reference is None):
                continue

            if (output_grid_analysis["height"] == source_shape["height"]
                and output_grid_analysis["width"] == source_shape["width"]):

                transformations.append({
                    "transformation_type": "grid",
                    "transformation": "crop_to_object",
                    "source_id": source_shape["object_id"],
                    "object_reference": object_reference
                })

        return transformations
    
    def get_object_reference(self, source_shape: dict, shapes: list[dict]) -> str|None:
        if(len(shapes) == 1):
            return "single"

        largest_shape = shapes[0]
        largest_size = largest_shape["height"]*largest_shape["width"]
        largest_count = 1

        smallest_shape = shapes[0]
        smallest_size = smallest_shape["height"]*smallest_shape["width"]
        smallest_count = 1

        for shape in shapes[1:]:
            size = shape["height"]*shape["width"]

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

        if(largest_count == 1 and largest_shape["object_id"] == source_shape["object_id"]):
            return "largest"
        if(smallest_count == 1 and smallest_shape["object_id"] == source_shape["object_id"]):
            return "smallest"

        return None

    def select_object_reference(self, test_shapes: list[dict], change: dict) -> dict|None:
        if not test_shapes:
            return None
        if (change["object_reference"] == "single"):
            if(len(test_shapes) == 1):
                return test_shapes[0]
        elif(change["object_reference"] == "largest"):
            largest_shape = test_shapes[0]
            largest_size = largest_shape["height"] * largest_shape["width"]
            largest_count = 1

            for shape in test_shapes[1:]:
                size = shape["height"] * shape["width"]

                if(size> largest_size):
                    largest_shape = shape
                    largest_size = size
                    largest_count = 1

            if (largest_count == 1):
                return largest_shape            
        return None
            

    def apply_validated_changes(self, test_grid: np.ndarray, test_shapes: list[dict], validated_changes: list[dict])-> np.ndarray:
        output_grid = test_grid.copy()
        mapped_color = None
        mapped_source_color = None

        for change in validated_changes:
                if(change["change_type"] == "crop_to_object"):
                    shape = self.select_object_reference(test_shapes, change)
                    if shape is not None:
                        output_grid = test_grid[shape["top"]:shape["bottom"] + 1, shape["left"]:shape["right"] + 1].copy()
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
                        source_color = source_shape["color"]
                        target_color = target_shape["color"]

                        output_grid[original_grid == source_color] = target_color
            elif change["change_type"] == "make_hollow":
                if change["source_reference"] == "all_objects":

                    for shape in test_shapes:
                        top = shape["top"]
                        bottom = shape["bottom"]
                        left = shape["left"]
                        right = shape["right"]
                        color = shape["color"]

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
                    
                    if(change["change_type"] == "color_mapping"):
                        if(change["from_color"] == other["from_color"]
                            and change["to_color"] == other["to_color"]):
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
                    elif change["change_type"] in ("make_hollow", "fill_in"):
                        if change["source_reference"] == other["source_reference"] and change["fill_color"] == other["fill_color"]:
                            found = True
                            break
                    elif(change["change_type"] == "crop_to_object"):
                        if(change["object_reference"] == other["object_reference"]):
                            found = True
                            break

                if not found:
                    found_in_all = False
                    break

            if found_in_all:
                if(change["change_type"] == "color_mapping"):
                    validated_changes.append({"change_type": "color_mapping", "from_color": change["from_color"], 
                        "to_color": change["to_color"]})
                elif (change["change_type"] == "color_change"):
                    validated_change = {"change_type": "color_change" }
                    for key in color_change_keys:
                        if key in change:
                            validated_change[key] = change[key]
                    validated_changes.append(validated_change)
                    # validated_changes.append({"change_type": "color_change","source_reference": change["source_reference"],
                    #     "target_reference": change["target_reference"]})
                elif change["change_type"] in ("make_hollow", "fill_in"):
                    validated_changes.append({"change_type": change["change_type"],"source_reference": change["source_reference"],
                        "fill_color": change["fill_color"]})
                elif(change["change_type"] == "crop_to_object"):
                    validated_changes.append({"change_type":"crop_to_object", "object_reference":change["object_reference"]})

        return validated_changes


        


    def get_change_candidates(self, object_transformations: list[dict], grid_transformations: list[dict], color_mappings: list[dict], training_set: int) -> list[dict]:
        change_candidates = []
        color_changes = {}
        make_hollow_count = 0
        fill_in_count = 0

        for transformation in grid_transformations:
            if (transformation["transformation"] == "crop_to_object"):
                change_candidates.append({
                    "change_type": "crop_to_object",
                    "source_id": transformation["source_id"],
                    "object_reference": transformation["object_reference"], 
                    "training_set": training_set
                })

        for transformation in object_transformations:
            if transformation["transformation"] == "make_hollow":
                make_hollow_count += 1
                continue
            elif transformation["transformation"] == "fill_in":
                fill_in_count += 1
                continue

            if(transformation["transformation"] != "color_change"):
                continue

            if (transformation["source_reference"] is not None
                and transformation["target_reference"] is not None):
                change_candidates.append({
                    "change_type": "color_change",
                    "source_reference": transformation["source_reference"],
                    "target_reference": transformation["target_reference"],
                    "training_set": training_set
                })

            color_change = (transformation["from_color"], transformation['to_color'])

            if color_change not in color_changes:
                color_changes[color_change] = 0

            color_changes[color_change] +=1



        for color_change, count in color_changes.items():
            change_candidates.append({"change_type": "color_mapping", "from_color": color_change[0], 
                                      "to_color": color_change[1], "count_objects": count, "training_set": training_set})

        for start_mapping in color_mappings:
            for next_mapping in color_mappings:
                if start_mapping == next_mapping:
                    continue

                if(start_mapping["to_color"] == next_mapping["from_color"] and next_mapping["to_color"] == 0):
                    change_candidates.append({"change_type": "color_change","source_color": start_mapping["from_color"],
                        "target_reference": "mapped_color","training_set": training_set})

                    change_candidates.append({"change_type": "color_change","source_reference": "mapped_color",
                        "target_color": 0,"training_set": training_set})

        if (len(object_transformations) > 0 ):
            if(make_hollow_count == len(object_transformations)):

                change_candidates.append({"change_type": "make_hollow","source_reference": "all_objects", "fill_color": 0, "training_set": training_set})
            elif(fill_in_count == len(object_transformations)):
                change_candidates.append({"change_type": "fill_in","source_reference": "all_objects","training_set": training_set})
            
        return change_candidates
    
    
    def get_input_output_transformations(self, input_shapes: list[dict], output_shapes: list[dict],input_output_relationships: list[dict]) -> list[dict]:
        transformations = []
        relationship_pairs = {}
        input_shapes_map = {}
        output_shapes_map = {}

        for relationship in input_output_relationships:
            source_id = relationship["source_id"]
            target_id = relationship["target_id"]
            

            for shape in input_shapes:
                input_shapes_map[shape["object_id"]] = shape

            for shape in output_shapes:
                output_shapes_map[shape["object_id"]] = shape

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
            source_cells = set(source_shape["cells"])
            target_cells = set(target_shape["cells"])

            if(same_color and source_shape["is_hollow"] != target_shape['is_hollow']):
                transformation = None
                if(source_shape["is_hollow"]== False and target_cells.issubset(source_cells)):
                    transformation = "make_hollow"
                if(source_shape["is_hollow"]== True and source_cells.issubset(target_cells)):
                    transformation = "fill_in"
                if transformation is not None:
                    transformations.append({"transformation_type": "object","transformation": transformation,
                        "source_reference": self.get_object_reference(source_shape,input_shapes ), 
                        "source_id": pair[0],"target_id": pair[1]}) 

            if same_color and same_shape:
                transformations.append({"transformation_type": "object", "transformation": "none", 
                                        "source_id": pair[0], "target_id": pair[1]})
            elif same_shape and different_color:
                source_reference = self.get_object_reference(source_shape,input_shapes)
                target_reference = None

                for input_shape in input_shapes:
                    if(input_shape["color"] != target_shape["color"]):
                        continue

                    target_reference = self.get_object_reference(input_shape, input_shapes)
                    if target_reference is not None:
                        break

                transformations.append({"transformation_type": "object", "transformation": "color_change", 
                                        "source_reference": source_reference, "target_reference": target_reference,
                                        "from_color": source_shape["color"], "to_color": target_shape["color"],
                                        "source_id": pair[0], "target_id": pair[1]})
            

        return transformations

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
                    "source_id": source_shape["object_id"],
                    "relationship_type": "shape",
                    "relationship_degree": degree,
                    "target_item": "object",
                    "target_id": target_shape["object_id"]
                })  
                if "same" == degree:
                    return shape_relationships    

        return shape_relationships


    def get_object_object_colors(self, source_shape, target_shape):
        color_relationships = []

        if source_shape["color"] == target_shape["color"]:
            relationship_degree = "same_color"
        else:
            relationship_degree = "different_color"

        color_relationships.append({
            "source_item": "object",
            "source_id": source_shape["object_id"],
            "relationship_type": "color",
            "relationship_degree": relationship_degree,
            "target_item": "object",
            "target_id": target_shape["object_id"]
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
                "source_id": source_shape["object_id"],
                "relationship_type": "region",
                "relationship_degree": "same_region",
                "target_item": "object",
                "target_id": target_shape["object_id"]
            })

        return region_relationships
    
    def get_object_object_positions(self, source_shape, target_shape):
        position_relationships = []
        if(source_shape["right"] < target_shape["left"]):
            position_relationships.append({
                "source_item": "object",
                "source_id": source_shape["object_id"],
                "relationship_type": "position",
                "relationship_degree": "left_of",
                "target_item": "object",
                "target_id": target_shape["object_id"]
            })

        if(source_shape["left"] > target_shape["right"]):
            position_relationships.append({
                "source_item": "object",
                "source_id": source_shape["object_id"],
                "relationship_type": "position",
                "relationship_degree": "right_of",
                "target_item": "object",
                "target_id": target_shape["object_id"]
            })

        if source_shape["bottom"] < target_shape["top"]:
            position_relationships.append({
                "source_item": "object",
                "source_id": source_shape["object_id"],
                "relationship_type": "position",
                "relationship_degree": "above",
                "target_item": "object",
                "target_id": target_shape["object_id"]
            })

        if source_shape["top"] > target_shape["bottom"]:
            position_relationships.append({
                "source_item": "object",
                "source_id": source_shape["object_id"],
                "relationship_type": "position",
                "relationship_degree": "below",
                "target_item": "object",
                "target_id": target_shape["object_id"]
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
                if(shape["object_id"] == relationship["source_id"]):
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
                    "source_id": shape["object_id"],
                    "relationship": "fills_grid",
                    "target_item": "grid"
                }
                relationships.append(relationship)

            divides_grid_vertical = (shape["top"] == 0 and shape["bottom"] == grid.shape[0] - 1 and shape["width"] == 1 and shape["left"] > 0 and shape["right"] < grid.shape[1] - 1)
            if divides_grid_vertical:
                relationship = {
                    "source_item": "object",
                    "source_id": shape["object_id"],
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
                    "source_id": shape["object_id"],
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

                shape = {"id": shape_id, "object_id": parent_grid_id + "_object_" + str(shape_id), "parent_grid_id": parent_grid_id, "color": color, "cells": cells, "pattern": pattern, 
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

    