# ar2landing_neural
This is the repository that contains the complete work on Searching and Precision Landing of an AR Drone 2.0 on a stationary landing platform using Neural Network. Watch the following video to get a better overview what it does.

[![video ar2landing_neural](https://i.ytimg.com/vi_webp/WrEmulklfXU/mqdefault.webp)](https://www.youtube.com/watch?v=WrEmulklfXU)

## Install

Following installation steps assume you hav a ROS Indigo installed in an Ubuntu 14.04 Linux Distro.

First create a workspace

```bash
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src
catkin_init_workspace
```

### ardrone_autonomy
Clone this repository and make it.

```bash
cd ~/catkin_ws/src
git clone https://github.com/AutonomyLab/ardrone_autonomy.git -b indigo-devel
cd ~/catkin_ws
rosdep install --from-paths src -i
catkin_make
```
If you face any problems with ardrone_autonomy ref this site [http://ardrone-autonomy.readthedocs.org/en/latest/installation.html]. If you just getting started go through the link to get an overview. This package is only needed if you are implementing this on a real drone (Not in a simulator like Gazebo).
