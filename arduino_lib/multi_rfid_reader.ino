
#include <ros.h>
#include <std_msgs/String.h>
#include <std_msgs/Int32.h>
#include <std_msgs/Empty.h>
#include <SPI.h>
#include <MFRC522.h>     // 引用程式庫

constexpr uint8_t RST_PIN = 5;     // Configurable, see typical pin layout above
constexpr uint8_t SS_1_PIN = 26;   // Configurable, take a unused pin, only HIGH/LOW required, must be diffrent to SS 2
constexpr uint8_t SS_2_PIN = 53;    // Configurable, take a unused pin, only HIGH/LOW required, must be diffrent to SS 1

constexpr uint8_t NR_OF_READERS = 2;

byte ssPins[] = {SS_1_PIN, SS_2_PIN};

MFRC522 mfrc522[NR_OF_READERS];   // Create MFRC522 instance.
ros::NodeHandle  nh;

std_msgs::String str_msg;
std_msgs::Int32 int32;
ros::Publisher chatter("rfid", &str_msg);

void setup()
{
  Serial.begin(57600);
  while (!Serial);    // Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4)
  
  SPI.begin(); // Init SPI bus

  for(uint8_t reader = 0; reader < NR_OF_READERS; reader++){
    mfrc522[reader].PCD_Init(ssPins[reader], RST_PIN); // Init each MFRC522 card
    Serial.print(F("Reader "));
    Serial.print(reader);
    Serial.print(F(": "));
  }
  nh.initNode();
  nh.advertise(chatter);
}

void loop()
{ 
  for (uint8_t reader = 0; reader < NR_OF_READERS; reader++) {
    if (mfrc522[reader].PICC_IsNewCardPresent() && mfrc522[reader].PICC_ReadCardSerial()) {
      Serial.print(F("Reader "));
      Serial.print(reader);
      Serial.print(F(": Card UID:"));
      Serial.println();
      byte* id = mfrc522[reader].uid.uidByte;
      dump_byte_array(id, mfrc522[reader].uid.size);
      pub_topic(id, "90", 101, 183, 231, 43);
      pub_topic(id, "91", 167, 227, 232, 43);
      pub_topic(id, "90", 176, 53, 41, 164);
      pub_topic(id, "91", 80, 16, 112, 163);
      pub_topic(id, "0", 16, 200, 16, 168);
      pub_topic(id, "1", 192, 110, 209, 87);
      pub_topic(id, "2", 96, 191, 31, 168);
    }
  }
  nh.spinOnce();
}


/**
 * Helper routine to dump a byte array as hex values to Serial.
 */
void dump_byte_array(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i] , DEC);
  }
  Serial.println();
}
void pub_topic(byte *buffer, const char out_str[], byte arg0, byte arg1, byte arg2, byte arg3){
  if(buffer[0] == arg0
    && buffer[1] == arg1
    && buffer[2] == arg2
    && buffer[3] == arg3){
      str_msg.data = out_str;
      chatter.publish(&str_msg);
    }
}
