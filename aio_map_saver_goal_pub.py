#!/usr/bin/env python3

from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy
from rclpy.duration import Duration
import yaml
import os 
import subprocess
import time

command = "ros2 run nav2_map_server map_saver_cli -f mapped_area"  # Adapt arguments as needed

# # Set the target directory to the Desktop
desktop_path = os.path.expanduser("/home/atul/ros2_ws/src/slambot/maps")

# # Change the working directory to the Desktop
os.chdir(desktop_path)    

def main():
    while True:
        navigator = BasicNavigator()

        subprocess.run(command, shell=True)                                     # Execute the command
        print(f"\n------------------------------------------------------")
        print(f"!! Files mapped_area.pgm & mapped_area.yaml saved   !!")
        print(f"!! Waiting for 5 seconds before accessing the files !!")
        print(f"------------------------------------------------------\n")
        time.sleep(1)  # Wait for 5 seconds

        # Read goal poses from the coordinates.yaml file ----------------------------------------------------------------------------------------------------------------------
        with open("/home/atul/slam-bot-streaming/coordinates.yaml", "r") as file1:
            raw_goal_poses = yaml.safe_load(file1)

            raw_goal_x, raw_goal_y = raw_goal_poses["goal_coordinate"]                                      # values here are in pixels

        # Read origin and resolution from the mapped_area.yaml file ----------------------------------------------------------------------------------------------------------------------
        with open("/home/atul/ros2_ws/src/slambot/maps/mapped_area.yaml", "r") as file2:
            mapped_area_yaml_file = yaml.safe_load(file2)

            resolution_multiplier                    = mapped_area_yaml_file["resolution"]                  # mostly value should be 0.05
            ros_origin_x, ros_origin_y, ros_origin_z = mapped_area_yaml_file["origin"]                      # values here are in meters

        with open("/home/atul/ros2_ws/src/slambot/maps/mapped_area.pgm" , "rb") as file3:
            
            header = file3.readline().decode("ascii").strip()              # Read the header
        
            pgm_width, pgm_height = map(int, file3.readline().decode("ascii").strip().split())              # Read the width and height in pixels
            _ = file3.readline()                                                                            # Skip the maximum gray value line

        #scale down the coordinates since the png file saved is scaled upto scale_factor times
        raw_goal_x = int(raw_goal_x/5)
        raw_goal_y = int(raw_goal_y/5)

        # print(f"Goal Given: {raw_goal_x}, {raw_goal_y} in pixels")

        goal_x_meters = raw_goal_x*0.05
        goal_y_meters = raw_goal_y*0.05
        # print(f"Goal Given: {goal_x_meters}, {goal_y_meters} in in meters")

        # Go to our demos first goal pose
        goal_pose = PoseStamped()
        goal_pose.header.frame_id = 'map'
        goal_pose.header.stamp = navigator.get_clock().now().to_msg()
        goal_pose.pose.position.x = goal_x_meters
        goal_pose.pose.position.y = goal_y_meters
        goal_pose.pose.orientation.w = 1.0

        # sanity check a valid path exists
        # path = navigator.getPath(initial_pose, goal_pose)

        #--------------------------------------------------------check values for debugging-------------------------------------------------------------------
        print(f"{raw_goal_x}")                                                                                                  #in pixels     
        print(f"{raw_goal_y}")                                                                                                  #in pixels    
        print(f"{ros_origin_x}")
        print(f"{ros_origin_y}")
        print(f"{ros_origin_z}")
        print(f"{resolution_multiplier}")
        print(f"{goal_x_meters}")                                                                                               #in meters
        print(f"{goal_y_meters}")                                                                                               #in meters
        print(f"PGM image dimensions: {pgm_height} pixels (height) x {pgm_width} pixels (width)")                               #in pixels
        #-----------------------------------------------------------------------------------------------------------------------------------------------------


        navigator.goToPose(goal_pose)

        i = 0
        while not navigator.isTaskComplete():
            ################################################
            #
            # Implement some code here for your application!
            #
            ################################################

            # Do something with the feedback
            i = i + 1
            feedback = navigator.getFeedback()
            if feedback and i % 5 == 0:
                print(f'Navigating to goal pose: {goal_x_meters}, {goal_y_meters}')

                # Some navigation timeout to demo cancellation
                if Duration.from_msg(feedback.navigation_time) > Duration(seconds=60.0):
                    navigator.cancelTask()

                # Some navigation request change to demo preemption
                if Duration.from_msg(feedback.navigation_time) > Duration(seconds=18.0):
                    goal_pose.pose.position.x = -3.0
                    navigator.goToPose(goal_pose)

        # Do something depending on the return code
        result = navigator.getResult()
        if result == TaskResult.SUCCEEDED:
            print('Goal succeeded!')
        elif result == TaskResult.CANCELED:
            print('Goal was canceled!')
        elif result == TaskResult.FAILED:
            print('Goal failed!')
        else:
            print('Goal has an invalid return status!')

rclpy.init()

if __name__ == '__main__':
    main()
