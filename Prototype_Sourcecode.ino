#include <WiFi.h>
#include <FirebaseESP32.h>

#include <Keypad.h>

#include <SPI.h>
#include <MFRC522.h>

#define WIFI_SSID "YOUR_WIFI_SSID"
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"

#define FIREBASE_HOST "YOUR_DB_URL"
#define FIREBASE_AUTH "YOUR_AUTH_CODE"

FirebaseData fbdo;

FirebaseJson json;





const byte ROWS = 4; //four rows
const byte COLS = 4; //four columns
//define the cymbols on the buttons of the keypads
char hexaKeys[ROWS][COLS] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};
byte rowPins[ROWS] = {14, 27, 26, 25}; //connect to the row pinouts of the keypad
byte colPins[COLS] = {33, 32, 35, 34};





#define RST_PIN         22          // Configurable, see typical pin layout above
#define SS_PIN          5         // Configurable, see typical pin layout above
#define buzz            15
#define green           13
#define red             12

String path = "/Customers";
String temp = "";
unsigned long st = 0;
unsigned long phno = 0;
int cus = 0;
int num;
int flg = 0;
//unsigned long v1 = 0;

MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create MFRC522 instance

Keypad customKeypad = Keypad( makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS); 

void setup() {
  // put your setup code here, to run once:
  int cus = 0;
  unsigned long phno;
  int num;
  Serial.begin(115200);
  pinMode(buzz, OUTPUT);
  pinMode(green, OUTPUT);
  pinMode(red, OUTPUT);// Initialize serial communications with the PC
  while (!Serial);    // Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4)
  SPI.begin();      // Init SPI bus
  mfrc522.PCD_Init();   // Init MFRC522
  delay(4);       // Optional delay. Some board do need more time after init to be ready, see Readme
  mfrc522.PCD_DumpVersionToSerial();  // Show details of PCD - MFRC522 Card Reader details
  Serial.println(F("Scan PICC to see UID, SAK, type, and data blocks..."));
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  Firebase.reconnectWiFi(true);

  Firebase.setReadTimeout(fbdo, 1000 * 60);

  Firebase.setwriteSizeLimit(fbdo, "medium");
  
  Serial.println("Please Enter the Phone Number : ");

//  while(phno == 0)
//  {
//    phno = GetNumber();
//    Serial.println(phno);
//  }

//  temp = path + "/" + (phno) + "/";
//  Serial.println(temp);
//  Serial.println("Connecting to Database...");
  

}


void loop(){

  while(phno == 0)
  {
    phno = GetNumber();
    Serial.println(phno);
  }
  if(phno != 0 && flg == 0)
  {
    temp = path + "/" + (phno) + "/";
    Serial.println(temp);
    Serial.println("Connecting to Database...");
    Serial.print("Scan the Product : ");
    flg = 1;
  }
  while (cus < 10)
  {
    if ( ! mfrc522.PICC_IsNewCardPresent()) {
    return;
  }

  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) {
    return;
  }
//    Serial.print("Scan the Product : ");
//    num = random(100, 900);
//    Serial.println(num);
    Serial.print("\n");
    Serial.println("**Card Detected**");
    digitalWrite(buzz, HIGH);
    digitalWrite(green, HIGH);
    digitalWrite(red, HIGH);
    delay(500);
    digitalWrite(buzz, LOW);
    delay(500);
    digitalWrite(green, LOW);
    /* Print UID of the Card */
    Serial.print(F("Card UID:"));
    for (byte i = 0; i < mfrc522.uid.size; i++)
    {
//      Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
//      Serial.print(mfrc522.uid.uidByte[i], HEX);
      st = st + (mfrc522.uid.uidByte[i]);
    }
    Serial.print("\n");
    Serial.println(st);
//    st = "";
//    delay(2000);
//    digitalWrite(red, LOW);

    if (Firebase.setInt(fbdo, temp + (cus+1) + "/ID", st) && Firebase.setInt(fbdo, temp + (cus+1) + "/Qty", 1))
    {
      Serial.println("PASSED");
      Serial.print("\n");
      Serial.print("Scan the Product : ");
//      Serial.println("PATH: " + fbdo.dataPath());
//      Serial.println("TYPE: " + fbdo.dataType());
    }
    else
    {
      Serial.println("FAILED");
      Serial.println("REASON: " + fbdo.errorReason());
      Serial.println("------------------------------------");
      Serial.println();
    }
    cus = cus + 1;
    delay(2000);
    digitalWrite(red, LOW);
    st = 0;
  }
}

int GetNumber()
{
   int num = 0;
   char key = customKeypad.getKey();
   while(key != '*')
   {
      switch (key)
      {
         case NO_KEY:
            break;

         case '0': case '1': case '2': case '3': case '4':
         case '5': case '6': case '7': case '8': case '9':
            num = num * 10 + (key - '0');
            break;
      }

      key = customKeypad.getKey();
      if(key == '*')
      {
        break;
      }
      Serial.print(key);
   }

   return num;
}











  
  
