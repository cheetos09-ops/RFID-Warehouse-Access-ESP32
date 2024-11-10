from mfrc522 import MFRC522
from machine import Pin, SPI
import time
import usocket as socket
import network
import _thread

# Define the SPI bus and pins
spi = SPI(2, baudrate=2500000, polarity=0, phase=0)
spi.init()

# Initialize the MFRC522 RFID reader with SPI and reset/cs pins
rdr = MFRC522(spi=spi, gpioRst=4, gpioCs=5)

# Define the relay pin (to control a lock or door)
relay = Pin(12, Pin.OUT)

# Define warehouse sections with authorized RFID tags, items, and statuses
warehouse_access = {
    "0xbcb23202": {"section": "Section A", "items": "Resistors", "quantity": 100, "authorized": True, "status": "Not Scanned"},
    "0x533c11da": {"section": "Section B", "items": "Wooden Crates", "quantity": 75, "authorized": True, "status": "Not Scanned"},
    "0x2907b498": {"section": "Section C", "items": "Electrical Cables", "quantity": 50, "authorized": False, "status": "Not Scanned"},  # Unauthorized
    "0x29eec498": {"section": "Section D", "items": "Steel Beams", "quantity": 120, "authorized": True, "status": "Not Scanned"},
    "0x59e1f097": {"section": "Section E", "items": "Plastic Containers", "quantity": 60, "authorized": False, "status": "Not Scanned"}   # Unauthorized
}

# Global variable to store the latest RFID scan information
access_log = "Waiting for RFID scan..."

# Function to check access to warehouse section and update status
def check_access(uid):
    global access_log
    if uid in warehouse_access:
        section_info = warehouse_access[uid]
        section = section_info["section"]
        authorized = section_info["authorized"]
        
        if authorized:
            section_info["status"] = "Granted"
            access_log = f"Access granted to {section}."
            print(access_log)
            # Simulate unlocking the door (activating relay)
            relay.on()
            time.sleep(3)  # Keep the door open for 3 seconds
            relay.off()  # Lock the door again
        else:
            section_info["status"] = "Denied"
            access_log = f"Access denied to {section}. Unauthorized RFID tag."
            print(access_log)
    else:
        access_log = "RFID tag not recognized."
        print(access_log)

# Function to generate the web page HTML with the status table
def web_page():
    table_rows = ""
    for uid, section_info in warehouse_access.items():
        row = f"""
        <tr>
            <td>{section_info['section']}</td>
            <td>{section_info['items']}</td>
            <td>{section_info['quantity']}</td>
            <td>{section_info['status']}</td>
        </tr>
        """
        table_rows += row
    
    html = """<!DOCTYPE HTML><html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    html { font-family: Arial; display: inline-block; margin: 0px auto; text-align: center; }
    h2 { font-size: 2.0rem; }
    table { width: 100%; border-collapse: collapse; }
    th, td { padding: 8px 12px; border: 1px solid #ddd; text-align: center; }
    th { background-color: #f2f2f2; }
    </style>
    <script>
    // Function to fetch RFID scan data and update the page
    function fetchAccessLog() {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                document.getElementById("status_table").innerHTML = this.responseText;
            }
        };
        xhr.open("GET", "/log", true);  // Fetch the log from the '/log' route
        xhr.send();
    }
    // Update every 2 seconds
    setInterval(fetchAccessLog, 2000);
    </script>
    </head>
    <body>
    <h2>Warehouse Inventory & RFID Access</h2>
    <table>
        <tr>
            <th>Section</th>
            <th>Item Description</th>
            <th>Quantity</th>
            <th>Status</th>
        </tr>
        <tbody id="status_table">
        """ + table_rows + """
        </tbody>
    </table>
    <p>Status: <span id="access_log">""" + access_log + """</span></p>
    </body></html>"""
    return html

# Function to return the latest access status table in plain text (for AJAX)
def access_status_table():
    table_rows = ""
    for uid, section_info in warehouse_access.items():
        row = f"""
        <tr>
            <td>{section_info['section']}</td>
            <td>{section_info['items']}</td>
            <td>{section_info['quantity']}</td>
            <td>{section_info['status']}</td>
        </tr>
        """
        table_rows += row
    return table_rows

# Setup ESP32 as Access Point
def setup_ap():
    ap = network.WLAN(network.AP_IF)  # Set as Access Point
    ap.active(True)
    ap.config(essid='ESP32-RFID-AccessPoint')  # Network SSID
    ap.config(authmode=network.AUTH_WPA_WPA2_PSK, password='123456789')  # Network password
    
    while not ap.active():
        pass  # Wait for the AP to activate
    print('Access Point Active')
    print('AP IP:', ap.ifconfig()[0])  # Display AP IP address

# Start the web server
def start_web_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024).decode()

        # Log for request parsing
        print('Request:', request)
        
        # Serve the main page
        if 'GET / ' in request or 'GET /favicon.ico' in request:
            response = web_page()
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)

        # Serve the access log data (only the table rows)
        elif 'GET /log' in request:
            response = access_status_table()  # Update only the table rows
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)

        conn.close()

# Main function for RFID scanning
def rfid_scanner():
    global access_log
    print("Place card to scan...")

    while True:
        # Request tag in IDLE state
        (stat, tag_type) = rdr.request(rdr.REQIDL)

        if stat == rdr.OK:
            # Read the UID of the card
            (stat, raw_uid) = rdr.anticoll()

            if stat == rdr.OK:
                # Construct the card ID in a hex format
                card_id = "0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
                print("UID:", card_id)

                # Check if the UID has access
                check_access(card_id)

                # Wait a short time before scanning again
                time.sleep(1)

# Run the web server and RFID scanner simultaneously
try:
    setup_ap()  # Set up the ESP32 as Access Point

    # Start the web server in a separate thread
    _thread.start_new_thread(start_web_server, ())

    # Continue scanning RFID tags infinitely
    rfid_scanner()

except KeyboardInterrupt:
    print("Program stopped")

