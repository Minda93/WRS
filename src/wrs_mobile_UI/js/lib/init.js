function Init(){
    console.log("init");
    joystick_main();

    setTimeout(function(){
        Init_Manual();
    },1000);
}