# Setting Up Arduino with ROS Kinetic

1. Install rosserial
    ``` bash
    $ sudo apt-get install ros-kinetic-rosserial-arduino
    $ sudo apt-get install ros-kinetic-rosserial
    ```
2. Giving Administrator privileges to the current user for the Arduino Permission Checker
    ``` bash
    $ sudo usermod -a -G dialout your_user_here
    ```

3. Install the ros_lib library
    ``` bash
    $ cd sketchbook/libraries
    $ source /opt/ros/kinetic/setup.bash 
    $ rosrun rosserial_arduino make_libraries.py .
    ```