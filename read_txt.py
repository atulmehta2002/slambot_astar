import yaml

with open("coordinates.yaml", "r") as file:
  safe_data = yaml.safe_load(file)

# Access data as before
start_x, start_y = safe_data["start_coordinate"]
goal_x, goal_y = safe_data["goal_coordinate"]


print(f"start_coordinate: {start_x}, {start_y}")
print(f"goal_coordinate: {goal_x}, {goal_y}")
