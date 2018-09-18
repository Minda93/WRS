function Init(){
    console.log("init");
    joystick_main();

    setTimeout(function(){
        Init_Manual();
    },1000);

    setTimeout(function(){
        Init_ScanBlack_Param();
    },500);
}