//Joystick

//Speed
// var speed = 30

var joystick_Area = document.getElementById('Joystick');
var joystick_canvas = document.getElementById("Joystick_Canvas");
var joy_ctx = joystick_canvas.getContext("2d");
var Round_r = 125; //var Round_r = 60;
var mouse_click = 0;
var logButton = -1;
var windowWidth = window.innerWidth;
var windowHeight = window.innerHeight;
var windowWidthToHeight = windowWidth / windowHeight;
var joystickcenter = {
    x: joystick_Area.offsetWidth / 2,
    y: joystick_Area.offsetHeight / 2
};
var joystick_V = {
    x: 0,
    y: 0,
    ang: 0
};
// =======================================================================
// flag 


// =======================================================================
/*  ros topic  

    Rostopic(connect, name, type)
        connect: ros 連到的IP 
            ex: connect = new ROSLIB.Ros({ursl:'ws://127.0.0.1:9090'});
        name: ros topic name 
        type: ros topic messageType

        function 
            pub(msg): ros topic publish
                msg: roslib message (根據type不同 內容會改變)
                    ex: var msg = new ROSLIB.Message({
                            data: value
                        });
            一直監聽(目前辦法)
                宣告變數名稱.object.subscribe(function(msg) {});
                msg: roslib message (根據type不同 內容會改變)
                    ex: start.object.subscribe(function(msg){return msg.data});

*/

var topicRemote = new RosTopic(ros, '/motion/remote', '/std_msgs/Bool')
var topicCmdvel = new RosTopic(ros, '/motion/cmd_vel', '/geometry_msgs/Twist')

var topicStart = new RosTopic(ros, '/scan_black/scan_start', '/std_msgs/Bool')
var topicBehavior = new RosTopic(ros, '/scan_black/strategy_behavior', '/std_msgs/Int32')
// =======================================================================