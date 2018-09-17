/* node list

    motion node
        pub:
            /motion/remote
            /motion/cmd_vel
        sub:

    stratgy node
        pub:
        sub:
    scan_black node
        pub:
        sub:
    qrcode node
        pub:
        sub
*/
/*========================================================*/
/*
    Motion node
 */
/*--------------------------------------------------------*/
//MotionRemote
function Init_Manual(){
    var msg = new ROSLIB.Message({
        data: false
    });
    topicRemote.Pub(msg);
}

function Manual_button(){
    var obj = document.getElementById("manual_button");
    var checked = document.getElementById("manual_button_checked").checked;

    if(checked){
        obj.style.cssText="color:#efbf67;";
        var msg = new ROSLIB.Message({
            data: true
        });
    }else{
        obj.style.cssText="color:#000000;";
        var msg = new ROSLIB.Message({
            data: false
        });
    }
    topicRemote.Pub(msg);
    // console.log(checked);
}
/*--------------------------------------------------------*/
// cmd_vel

function Robot_Vel(vec) {
    var checked = document.getElementById("manual_button_checked").checked;
    var msg = new ROSLIB.Message({
        linear: {
            x: vec.y,
            y: -vec.x,
            z: 0
        },
        angular: {
            x: 0,
            y: 0,
            z: vec.z
        }
    });
    if(checked){
        console.log(msg.linear.x,msg.linear.y,msg.angular.z);
        topicCmdvel.Pub(msg);
    }else{
        console.log("don't start up Manual!!!!")
    }
    
}

function Robot_Stop() {
    var msg = new ROSLIB.Message({
        linear: {
            x: 0,
            y: 0,
            z: 0
        },
        angular: {
            x: 0,
            y: 0,
            z: 0
        }
    });
    topicCmdvel.Pub(msg);
}
/*========================================================*/
/*
    Strategy node
 */
/*--------------------------------------------------------*/
// start
function pub_topic() {
    console.log(1111);
    var msg = new ROSLIB.Message({
        data: true
    });
    topicStart.Pub(msg)
}
/*--------------------------------------------------------*/
// behavior
document.getElementsByName("strategy_button")[0].addEventListener("click", function(){
    console.log('mobile');
    var msg = new ROSLIB.Message({
        data: 0
    });
    topicBehavior.Pub(msg);
});
document.getElementsByName("strategy_button")[1].addEventListener("click", function(){
    console.log('correction');
    var msg = new ROSLIB.Message({
        data: 1
    });
    topicBehavior.Pub(msg);
});
document.getElementsByName("strategy_button")[2].addEventListener("click", function(){
    console.log('platform');
    var msg = new ROSLIB.Message({
        data: 2
    });
    topicBehavior.Pub(msg);
});
document.getElementsByName("strategy_button")[3].addEventListener("click", function(){
    console.log('next');
    var msg = new ROSLIB.Message({
        data: 3
    });
    topicBehavior.Pub(msg);
});
document.getElementsByName("strategy_button")[4].addEventListener("click", function(){
    console.log('home');
    var msg = new ROSLIB.Message({
        data: 4
    });
    topicBehavior.Pub(msg);
});
document.getElementsByName("strategy_button")[5].addEventListener("click", function(){
    console.log('manual');
    var msg = new ROSLIB.Message({
        data: 5
    });
    topicBehavior.Pub(msg);
});



