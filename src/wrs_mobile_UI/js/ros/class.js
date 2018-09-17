
/* 
Vision1.subscribe(function(msg) {
    return msg.data
}); 
*/

class RosTopic {
    constructor(rosConnect, name, type) {
        this.object = new ROSLIB.Topic({
            ros: rosConnect,
            name: name,
            messageType: type
        });
    }

    Pub(msg) {
        this.object.publish(msg);
    }
    // Sub(){
    //     this.object.subscribe(function(msg){
    //         return msg
    //     });
    // }
}
// =======================================================================
class RosParam {
    constructor(rosConnect, name) {
        this.object = new ROSLIB.Param({
            ros: rosConnect,
            name: name,
        });
    }

    Set(value) {
        this.object.set(value);
    }

    Get(){
        this.object.get(function(value) {
            return value;
        });
    }
}
// =======================================================================
/* 
var request = new ROSLIB.ServiceRequest({
    receive: 1
}); 
*/

class RosService{
    constructor(rosConnect, name, type) {
        this.object = new ROSLIB.Service({
            ros: rosConnect,
            name: name,
            serviceType: type
        });
    }

    Call(request){
        this.object.callService(request, function(res) {
            return res;
        });
    }
}