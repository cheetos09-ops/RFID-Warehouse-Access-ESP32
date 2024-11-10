**RFID Warehouse Access Control System:**

This project implements an RFID-based access control system for managing access to different sections in a warehouse, along with basic inventory management. The system utilizes an ESP32 microcontroller, a MFRC522 RFID reader, and a web interface to monitor and control warehouse sections based on authorized RFID tags.

**Key Features:**

1. _RFID-based Access Control:_ Grants or denies access to warehouse sections based on authorized RFID tags.
2. _Inventory Management:_ Displays a list of warehouse sections, items, and quantities on a web page.
3. _Real-time Access Log:_ Shows the current status (granted or denied) for each section.
4. _ESP32 Web Server:_ Hosts a local web server allowing easy access to the system via any device on the same network.
5. _Relay Control: _Simulates locking/unlocking a door to grant access to authorized personnel.

**Components Used:** 

:hammer_and_wrench: Hardware: ESP32 Microcontroller, MFRC522 RFID Reader Module ,Warehouse sections (simulated as inventory data in the code)

:computer: Software: Thonny IDE- MicroPython (running on the ESP32), HTML, CSS, and JavaScript for the web interface, mfrc522 library for RFID scanning, network and socket for creating a web server on the ESP32.

`#000000`
