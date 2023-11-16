from dataclasses import dataclass
import json
from typing import List, Optional, Dict
from model.operation import Operation, Transition
from predicates.state import State
import predicates.guards
import predicates.actions
from predicates.guards import AlwaysTrue, Guard, And
from predicates.guards import AlwaysFalse
from model.model import Model, from_goal_to_goal

g = predicates.guards.from_str
a = predicates.actions.from_str


def the_model() -> Model:

        initial_state = State(
                # control variables
                r1_robot_run = False,   # trigger action when true. Change to false and then to true to trigger again
                r1_robot_command = 'move_j',
                r1_robot_velocity = 2.0,
                r1_robot_acceleration = 0.5,
                r1_robot_goal_frame = 'unknown',   # where to go with the tool tcp
                r1_robot_tcp_frame = 'r1_svt_tcp', # the tool tcp to use
                r1_gripper_run = False, # trigger service when true. Change to false and then to true to trigger again
                r1_gripper_command = 'none', # pick_red, pick_green, pick_blue, drop_red, drop_green, drop_blue

                r2_robot_run = False,   # trigger action when true. Change to false and then to true to trigger again
                r2_robot_command = 'move_j',
                r2_robot_velocity = 2.0,
                r2_robot_acceleration = 0.5,
                r2_robot_goal_frame = 'unknown',   # where to go with the tool tcp
                r2_robot_tcp_frame = 'r2_svt_tcp', # the tool tcp to use
                r2_gripper_run = False, # trigger service when true. Change to false and then to true to trigger again
                r2_gripper_command = 'none', # pick_red, pick_green, pick_blue, drop_red, drop_green, drop_blue

                goal_as_string = "",
                replan = False,

                # measured variables
                r1_robot_state = "initial",  # "exec", "done", "failed" 
                r1_robot_pose = "unknown",
                r2_robot_state = "initial",  # "exec", "done", "failed" 
                r2_robot_pose = "unknown",
                replanned = False,

                #estimated
                green_cube_at = "pose_1", # pose_1, pose_2, pose_3, r1_gripper, r1_buffer, r2_gripper, r2_buffer
                red_cube_at = "pose_2",  # pose_1, pose_2, pose_3, r1_gripper, r1_buffer, r2_gripper, r2_buffer
                blue_cube_at = "pose_3",  # pose_1, pose_2, pose_3, r1_gripper, r1_buffer, r2_gripper, r2_buffer
        )

        ops = {}

    
        ops[f"r1_to_pose_1"]=Operation(
                        
                        name=f"r1_to_pose_1",
                        precondition= Transition("pre",
                                                g(f"!r1_robot_run && r1_robot_state == initial && r1_robot_pose != pose_1 && r2_robot_pose != pose_1"),
                                                a(f"r1_robot_command = move_j, r1_robot_run, r1_robot_goal_frame = pose_1")),
                        postcondition=Transition("post",
                                                g(f"r1_robot_state == done"),
                                                a(f"!r1_robot_run, r1_robot_pose <-pose_1")),
                        effects= (),
                        to_run= Transition.default()
            )
        ops[f"r1_to_pose_2"]=Operation(
                        
                        name=f"r1_to_pose_2",
                        precondition= Transition("pre",
                                                g(f"!r1_robot_run && r1_robot_state == initial && r1_robot_pose != pose_2 && r2_robot_pose != pose_2"),
                                                a(f"r1_robot_command = move_j, r1_robot_run, r1_robot_goal_frame = pose_2")),
                        postcondition=Transition("post",
                                                g(f"r1_robot_state == done"),
                                                a(f"!r1_robot_run, r1_robot_pose <-pose_2")),
                        effects= (),
                        to_run= Transition.default()
            )
    
        ops[f"r1_to_buffer"]=Operation(
                        
                        name=f"r1_to_buffer",
                        precondition= Transition("pre",
                                                g(f"!r1_robot_run && r1_robot_state == initial && r1_robot_pose != r1_buffer"),
                                                a(f"r1_robot_command = move_j, r1_robot_run, r1_robot_goal_frame = r1_buffer")),
                        postcondition=Transition("post",
                                                g(f"r1_robot_state == done"),
                                                a(f"!r1_robot_run, r1_robot_pose <- r1_buffer")),
                        effects= (),
                        to_run= Transition.default()
            )
    
        ops[f"r2_to_pose_2"]=Operation(
                        
                        name=f"r2_to_pose_2",
                        precondition= Transition("pre",
                                                g(f"!r2_robot_run && r2_robot_state == initial && r2_robot_pose != pose_2 && r1_robot_pose != pose_2"),
                                                a(f"r2_robot_command = move_j, r2_robot_run, r2_robot_goal_frame = pose_2")),
                        postcondition=Transition("post",
                                                g(f"r2_robot_state == done"),
                                                a(f"!r2_robot_run, r2_robot_pose <-pose_2")),
                        effects= (),
                        to_run= Transition.default()
            )


        ops[f"r2_to_pose_3"]=Operation(
                        
                        name=f"r2_to_pose_3",
                        precondition= Transition("pre",
                                                g(f"!r2_robot_run && r2_robot_state == initial && r2_robot_pose != pose_3 && r1_robot_pose != pose_3"),
                                                a(f"r2_robot_command = move_j, r2_robot_run, r2_robot_goal_frame = pose_3")),
                        postcondition=Transition("post",
                                                g(f"r2_robot_state == done"),
                                                a(f"!r2_robot_run, r2_robot_pose <-pose_3")),
                        effects= (),
                        to_run= Transition.default()
            )


        ops[f"r2_to_buffer"]=Operation(
                        
                        name=f"r2_to_buffer",
                        precondition= Transition("pre",
                                                g(f"!r2_robot_run && r2_robot_state == initial && r2_robot_pose != r2_buffer"),
                                                a(f"r2_robot_command = move_j, r2_robot_run, r2_robot_goal_frame = r2_buffer")),
                        postcondition=Transition("post",
                                                g(f"r2_robot_state == done"),
                                                a(f"!r2_robot_run, r2_robot_pose <- r2_buffer")),
                        effects= (),
                        to_run= Transition.default()
            )


        

        for e in [1,2]:

            

            


                for j in ["green","red","blue"]:
                  

                        ops[f"r{e}_pick_up_{j}"]=Operation(
                                name=f"r{e}_pick_up_{j}",
                                precondition= Transition("pre",
                                                        g(f"!r{e}_gripper_run && r{e}_robot_pose == {j}_cube_at"),
                                                        a(f"r{e}_gripper_run, r{e}_gripper_command = pick_{j}")),
                                postcondition= Transition("post",
                                                        g(f"r{e}_gripper_run"),
                                                        a(f"{j}_cube_at <- r{e}_gripper")),
                                effects= (),
                                to_run= Transition.default()

                    )


                        ops[f"r{e}_place_{j}_cube"]=Operation(
                                name=f"r{e}_place_{j}_cube",

                                precondition= Transition("pre",
                                                        g(f"r{e}_gripper_run && {j}_cube_at == r{e}_gripper && r{e}_robot_state == initial && r{e}_robot_pose != blue_cube_at && r{e}_robot_pose != red_cube_at && r{e}_robot_pose != green_cube_at && r{e}_robot_pose != above_pose_1 && r{e}_robot_pose != above_pose_2 && r{e}_robot_pose != above_pose_3 &&r{e}_robot_pose != above_r{e}_buffer"),
                                                        a(f"r{e}_gripper_command = place_{j}")),
                                postcondition=Transition("post",
                                                        g(f"r{e}_gripper_run"),
                                                        a(f"!r{e}_gripper_run, {j}_cube_at <- r{e}_robot_pose")),
                                effects=(),
                                to_run=Transition.default()

                    )
                for pos in ["pose_1","pose_2","pose_3","r1_buffer", "r2_buffer"]:
                
                        ops[f"op_r1_move_to_above_{pos}"] = Operation(
                                name = f"op_r1_move_to_above_{pos}",
                                precondition = Transition("pre", 
                                g(f"!r1_robot_run && r1_robot_state == initial && r1_robot_pose != above_{pos} && r2_robot_pose != above_{pos}&& r2_robot_pose != {pos}"), 
                                a(f"r1_robot_command = move_j, r1_robot_run, r1_robot_goal_frame = above_{pos}")),
                                postcondition = Transition("post", 
                                g(f"r1_robot_state == done"), 
                                a(f"!r1_robot_run, r1_robot_pose = above_{pos}")),
                                effects = (),
                                to_run = Transition.default()
                )
                ops[f"op_r2_move_to_above_{pos}"] = Operation(
                        name = f"op_r2_move_to_above_{pos}",
                        precondition = Transition("pre", 
                        g(f"!r2_robot_run && r2_robot_state == initial && r2_robot_pose != above_{pos} && r1_robot_pose != above_{pos} && r1_robot_pose != {pos}"), 
                        a(f"r2_robot_command = move_j, r2_robot_run, r2_robot_goal_frame = above_{pos}")),
                        postcondition = Transition("post", 
                        g(f"r2_robot_state == done"), 
                        a(f"!r2_robot_run, r2_robot_pose = above_{pos}")),
                        effects = (),
                        to_run = Transition.default()
                )

        transitions: List[Transition] = []

        return Model(
                initial_state,
                ops,
                transitions
    )

def from_goal_to_goal(state: State) -> Guard:
    
    #Create a goal predicate 
    
    goal: str = state.get("goal_as_string")
    if goal != "":
        return g(goal)
    
    return AlwaysFalse()             

