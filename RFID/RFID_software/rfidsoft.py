import serial
import time
import configparser

# Dictionary to store last scanned EPCs by location
last_epc_by_location = {}

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Global configuration
SERIAL_PORT = config['GLOBAL']['serial_port']
READ_INTERVAL = int(config['GLOBAL']['read_interval'])

def open_serial_connection(port, baudrate):
    """Opens and returns a serial connection."""
    try:
        return serial.Serial(port, baudrate, timeout=1)
    except Exception as e:
        print(f"Error opening serial port: {e}")
        return None

def read_epc_and_metadata(serial_connection):
    """Reads EPC and metadata (including Reader ID) from the RFID reader."""
    try:
        if serial_connection.in_waiting > 0:
            # Read the incoming data from the serial connection
            raw_data = serial_connection.readline().decode('utf-8').strip()
            # Assuming data format: "reader_id,epc,metadata"
            reader_id, epc, metadata = raw_data.split(',')
            return reader_id, epc, metadata
        return None, None, None
    except Exception as e:
        print(f"Error reading from serial port: {e}")
        return None, None, None

def validate_epc_format(epc):
    """Validates the EPC format based on GS1 standards."""
    if len(epc) == 24:  # Example length for EPC
        return True
    return False

def is_duplicate(epc, location, last_epc_by_location, duplicate_time_window):
    """Checks if the EPC is a duplicate at the given location."""
    if location in last_epc_by_location:
        last_epc, last_time = last_epc_by_location[location]
        current_time = time.time()
        # If the EPC matches and it was read within the time window, it is a duplicate
        if epc == last_epc and (current_time - last_time) < duplicate_time_window:
            return True
    return False

def store_epc(epc, location, last_epc_by_location):
    """Stores the latest EPC read for the given location."""
    current_time = time.time()
    last_epc_by_location[location] = (epc, current_time)

def main():
    # Open serial connection to RFID reader
    serial_connection = open_serial_connection(SERIAL_PORT, int(config['READER_1']['baud_rate']))

    if not serial_connection:
        print("Failed to establish serial connection.")
        return

    print("RFID reader connected. Ready to read tags...")

    while True:
        reader_id, epc, metadata = read_epc_and_metadata(serial_connection)

        if epc:
            print(f"Read EPC: {epc} from Reader: {reader_id}, Metadata: {metadata}")

            # Get reader-specific configuration
            if f'READER_{reader_id}' not in config:
                print(f"Unknown reader ID: {reader_id}")
                continue

            reader_config = config[f'READER_{reader_id}']
            location = reader_config['location']
            duplicate_time_window = int(reader_config['duplicate_time_window'])

            # Validate the EPC format
            if not validate_epc_format(epc):
                print(f"Invalid EPC format: {epc}")
                continue

            # Check for duplicates at the current location
            if is_duplicate(epc, location, last_epc_by_location, duplicate_time_window):
                print(f"Duplicate EPC detected: {epc} at {location}. Ignoring...")
                continue

            # Store the valid EPC with its timestamp and location
            store_epc(epc, location, last_epc_by_location)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            print(f"EPC: {epc}, Location: {location}, Time: {timestamp}")

        time.sleep(READ_INTERVAL)

if __name__ == "__main__":
    main()

