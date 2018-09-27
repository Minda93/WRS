# Install arduino

1. Download [arduino](https://www.arduino.cc/en/Main/Software)

2. 解壓縮
    ``` bash
    $ tar Jxvf arduino-1.8.7-linux64.tar.xz
    ```
3. move your extracted Arduino file into the opt directory
    ``` bash
    $ sudo mv arduino-1.8.7 /opt
    ```
4. Change into /opt directory and into the Arduino folder
    ``` bash
    $ cd /opt/arduino-1.8.2
    ```
5. edit the `install.sh` script
    ``` bash
    $ sudo vim install.sh
    ```
    * Search in the script for the line "RESOURCE_NAME=cc.arduino.arduinoide" and change it to "RESOURCE_NAME=arduino-arduinoide".
6. make the script executable
    ``` bash
    $ sudo chmod +x install.sh
    ```
7. execute `install.sh`
    ``` bash
    $ ./install.sh
    ```
8. link arduino
    ``` bash
    $ sudo cp arduino /user/local/bin/
    $ sudo ln -sf /opt/arduino-1.8.7/arduino /usr/local/bin/arduino 
    ```
9. reference
    * [download arduino](https://www.arduino.cc/en/Main/Software)
    * [install arduino](https://www.hackster.io/patrickstrasser/install-arduino-ide-1-8-2-on-linux-8ef105)
    * [link arduino](http://imsardine.simplbug.com/note/arduino/install-ubuntu.html) 