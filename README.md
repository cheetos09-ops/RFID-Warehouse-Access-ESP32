# **RFID Warehouse Access Control System**

This project implements an RFID-based access control system for managing access to different sections in a warehouse, along with basic inventory management. The system utilizes an ESP32 microcontroller, a MFRC522 RFID reader, and a web interface to monitor and control warehouse sections based on authorized RFID tags.

## :black_nib:**Key Features**

1. _RFID-based Access Control:_  Grants or denies access to warehouse sections based on authorized RFID tags.
2. _Inventory Management:_  Displays a list of warehouse sections, items, and quantities on a web page.
3. _Real-time Access Log:_  Shows the current status (granted or denied) for each section.
4. _ESP32 Web Server:_  Hosts a local web server allowing easy access to the system via any device on the same network.
5. _Relay Control:_  Simulates locking/unlocking a door to grant access to authorized personnel.

## :toolbox: Components Used

### :gear: Hardware: 
ESP32 Microcontroller, MFRC522 RFID Reader Module ,Warehouse sections (simulated as inventory data in the code)

### :keyboard: Software: 
Thonny IDE- MicroPython (running on the ESP32), HTML, CSS, and JavaScript for the web interface, mfrc522 library for RFID scanning, network and socket for creating a web server on the ESP32.

## :rocket: Installation And Setup

### :hammer_and_wrench: Hardware Connections:
Connect the MFRC522 RFID reader to the ESP32 via SPI

<img width="554" alt="Connections" src="https://github.com/user-attachments/assets/32d0395b-3ec1-42f0-96d9-294169ed1396">

### :computer: Software Setup:
- Install MicroPython on the ESP32.
- Upload the provided Python code to the ESP32 using an IDE like Thonny or uPyCraft.
- Ensure that your ESP32 is connected to a network. This project sets up the ESP32 as an Access Point (AP), so your device can connect directly to the ESP32’s Wi-Fi network.

### :crystal_ball: Running the Web Server:

- Once the code is uploaded and the ESP32 is powered on, it will create a Wi-Fi access point named `ESP32-RFID-AccessPoint`.
- Connect to this network with the password `123456789`.
- Open a web browser and navigate to the ESP32’s IP address (which will be displayed in the serial monitor when the ESP32 is running).

###  :control_knobs: Access Control:

- Present authorized RFID tags to the RFID reader. If the tag is authorized, the corresponding warehouse section will be unlocked for 3 seconds (simulating a door opening).
- Unauthorized tags will be denied access.

### :pushpin: Web Interface:

- The web interface will display a table with warehouse sections, item descriptions, quantities, and the current access status (Granted/Denied).
- The status will update every 2 seconds to reflect the latest RFID scan results.

## :desktop_computer:	Code Overview

`main.py`: Contains the core logic for reading RFID tags, checking access rights, and controlling the relay for door locking/unlocking.

`Web Interface`: A simple HTML page is served by the ESP32 that displays the current warehouse access log and inventory details.

`web_page()`: Generates the HTML page with a table showing the current warehouse status, which updates every 2 seconds.

`rfid_scanner()_`: Handles scanning RFID tags and determining whether access should be granted or denied based on the predefined list of authorized tags.

## :mag_right: Future Enhancements
Database Integration: Integrate with a backend database to manage authorized users and inventory data more dynamically.
User Authentication: Implement a login system to manage access control settings securely.
Real-time Notifications: Send notifications when unauthorized access is attempted.

## Citations:
mfrc522.py RFID driver library taken from:
https://github.com/cefn/micropython-mfrc522/blob/master/mfrc522.py
