# Stick Balancing

This is a small project that tells you how to implement a PID controller to balance a stick.

## Deployment

To deploy this project:-

```bash
  git clone https://github.com/Bhajneet-Singh-Bedi/stick_balancing.git
```

Make a ros2 workspace and build the project.

```bash
  colcon build --packages-select stick_balancing
```

Run these commands in two different terminals. \
Terminal:- 1 
```bash
  ros2 launch stick_balancing stick_velocity.launch.py 
```
Terminal:- 2
```bash
  ros2 run stick_balancing stick_balance.py
```

## Explanation
 - stick_velocity.launch.py launches gazebo empty_world and the spawns the stick_balancing physical model.
 - It also loads a velocity_controller which is defined in controller_configuration_velocity.yaml file.
 - stick_balance.py has PID implemented in it which publishes velocity commands to "/velocity_controller/commands" topic which is create using ros2_control.
