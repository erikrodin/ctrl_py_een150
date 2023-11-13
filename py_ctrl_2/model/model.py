from dataclasses import dataclass
import json
from typing import List, Optional, Dict
from model.operation import Operation, Transition
from predicates.state import State
import predicates.guards
import predicates.actions
from predicates.guards import AlwaysTrue, Guard, And
from predicates.guards import AlwaysFalse

@dataclass
class Model(object):
    initial_state: State
    operations: Dict[str, Operation]
    transitions: List[Transition]

    def __post_init__(self):
        ops = {o: "i" for o in self.operations}
        self.initial_state = self.initial_state.next(**ops)

g = predicates.guards.from_str
a = predicates.actions.from_str

def the_model() -> Model:

    initial_state = State(
        # control variables
        robot_run = False,   # trigger action when true. Change to false and then to true to trigger again
        robot_command = 'move_j',
        robot_velocity = 2.0,
        robot_acceleration = 0.5,
        robot_goal_frame = 'unknown',   # where to go with the tool tcp
        robot_tcp_frame = 'r1_svt_tcp', # the tool tcp to use
        gripper_run = False, # trigger service when true. Change to false and then to true to trigger again
        gripper_command = 'none', # pick_red, pick_green, pick_blue, place_red, place_green, place_blue (innan stod de drop)
        robot_pose = "unknown",
        goal_as_string = "",
        replan = False,

        # measured variables
        robot_state = "initial",  # "exec", "done", "failed" 
        replanned = False,

        #estimated
        green_cube_at = "pose_1", # pose_1, pose_2, pose_3, gripper, buffer
        red_cube_at = "pose_2",  # pose_1, pose_2, pose_3, gripper, buffer
        blue_cube_at = "pose_3",  # pose_1, pose_2, pose_3, gripper, buffer
    )
 

    # we will store all operations in this dict that will be part of the model
    ops = {}
    
    for pos in ["pose_1","pose_2","pose_3","buffer"]:
        for colour in ["blue","red","green"]:
        
            
            ops[f"op_move_to_{pos}"] = Operation(
                name = f"op_move_to_{pos}",
                precondition = Transition("pre", 
                g(f"!robot_run && robot_state == initial && robot_pose == above_{pos}"), 
                a(f"robot_command = move_j, robot_run, robot_goal_frame = {pos}")),
                postcondition = Transition("post", 
                g(f"robot_state == done"), 
                a(f"!robot_run, robot_pose <- {pos}")),
                effects = (),
                to_run = Transition.default()
        )   
            ops[f"op_move_to_above_{pos}"] = Operation(
                name = f"op_move_to_above_{pos}",
                precondition = Transition("pre", 
                g(f"!robot_run && robot_state == initial && robot_pose != above_{pos}"), 
                a(f"robot_command = move_j, robot_run, robot_goal_frame = above_{pos}")),
                postcondition = Transition("post", 
                g(f"robot_state == done"), 
                a(f"!robot_run, robot_pose = above_{pos}")),
                effects = (),
                to_run = Transition.default()
        )

            ops[f"op_pick_up_{colour}_from_{pos}"] = Operation(
                name = f"op_pick_up_{colour}_from_{pos}",
                precondition = Transition("pre", 
                g(f"robot_pose == {pos} && {colour}_cube_at == {pos} && !gripper_run && blue_cube_at != gripper && red_cube_at != gripper && green_cube_at != gripper && !robot_run"), 
                a(f"gripper_run, gripper_command = pick_{colour}")),
                postcondition = Transition("post", 
                g(f"gripper_command == done"), 
                a(f"!gripper_run, {colour}_cube_at = gripper")),
                effects = (),
                to_run = Transition.default()
            )  
        
            ops[f"op_place_{colour}_at_{pos}"] = Operation(
                name = f"op_place_{colour}_at_{pos}",
                precondition = Transition("pre", 
                g(f"robot_pose == {pos} && blue_cube_at != {pos} && {colour}_cube_at == gripper && red_cube_at != {pos} && green_cube_at != {pos}"), 
                a(f"gripper_run, gripper_command = place_{colour}")),
                postcondition = Transition("post", 
                g(f"gripper_command == done"), 
                a(f"!gripper_run, {colour}_cube_at = {pos}")),
                effects = (),
                to_run = Transition.default()
            )


    
    transitions: List[Transition] = []
    for op in ops:
        print(op)
        print("-------")
    return Model(
        initial_state,
        ops,
        transitions
    )

def from_goal_to_goal(state: State) -> Guard:
    """
    Create a goal predicate 
    """
    goal: str = state.get("goal_as_string")
    if goal != "":
        return g(goal)
    
    return AlwaysFalse()