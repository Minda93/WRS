
#include <ros.h>
#include <std_msgs/String.h>
#include <std_msgs/Int32.h>
#include <std_msgs/Empty.h>
#include <SPI.h>
#include <MFRC522.h>     // 引用程式庫

#define RST_PIN      5        // 讀卡機的重置腳位
#define SS_PIN       53        // 晶片選擇腳位

MFRC522 mfrc522(SS_PIN, RST_PIN);  // 建立MFRC522物件
ros::NodeHandle  nh;

std_msgs::String str_msg;
std_msgs::Int32 int32;
ros::Publisher chatter("rfid", &str_msg);

void setup()
{
  
  SPI.begin(); // Init SPI bus
  mfrc522.PCD_Init(); // Init MFRC522 
  Serial.begin(57600);
  nh.initNode();
  nh.advertise(chatter);
}

void loop()
{ 
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    byte *id = mfrc522.uid.uidByte;   // 取得卡片的UID
    byte idSize = mfrc522.uid.size;   // 取得UID的長度
    if(id[0] == 16 
        && id[1] == 200
        && id[2] == 16
        && id[3] == 168){ 
      char hello[2] = "0";
      str_msg.data = hello;
      chatter.publish( &str_msg );
    }
    else if(id[0] == 192 
        && id[1] == 110
        && id[2] == 209
        && id[3] == 87){  
          char hello[2] = "1";
          str_msg.data = hello;
          chatter.publish( &str_msg );
        }
    else if(id[0] == 96 
        && id[1] == 191
        && id[2] == 31
        && id[3] == 168){  
          char hello[2] = "2";
          str_msg.data = hello;
          chatter.publish( &str_msg );
        }
    else if(id[0] == 176 
        && id[1] == 53
        && id[2] == 41
        && id[3] == 164){  
          char hello[2] = "3";
          str_msg.data = hello;
          chatter.publish( &str_msg );
        }
  }
  nh.spinOnce();
//  delay(1);
}
