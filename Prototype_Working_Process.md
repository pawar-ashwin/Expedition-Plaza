When a customer visits a supermarket and obtains a trolley, he should enter his `mobile number` in order for the trolley to be registered in the database under his `mobile number`.

When an item from the grocery store is placed in the trolley, the `RFID tag` of that item is detected by the `RFID scanner` included in the prototype, and the item is registered in the database using the mobile number that the customer provided at the start.

We have a `red LED, a green LED and a buzzer`, so when the item is placed in the trolley and the RFID tag of the item is detected by the scanner, the buzzer makes a beep sound and both red and green LEDs light up. The `green LED here indicates that the data about the product has been sent to the database, and the red LED indicates that the request is being processed. When the `red LED` turns off, it indicates that the request has been **processed** completely, and you can now place other items in the trolley.
