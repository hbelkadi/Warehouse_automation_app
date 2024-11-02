# Warehouse Automation with UHF RFID Integration

This repository contains an Odoo 15 module for automating warehouse management using UHF RFID technology. The module allows for automatic inventory management by scanning RFID tags at the warehouse entrance and exit to add or remove product records and update stock quantities and locations in real time.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Demo Mode (No RFID Reader)](#demo-mode-no-rfid-reader)
- [References](#references)

## Features
- Automated stock quantity updates based on RFID tag scans.
- Automatic location updates for products based on scan location.
- Independent menus for managing RFID tags and monitoring product inventory.
- Demo mode for testing without a physical RFID reader.

## Prerequisites
- Ubuntu 20.04 or later
- Python 3.8 or later
- PostgreSQL
- Odoo 15 (you can refer to the [Odoo 15 GitHub repository](https://github.com/odoo/odoo/tree/15.0) for installation instructions)
- UHF RFID reader (optional for demo mode)

## Installation

### 1. **Clone the Repository**
```bash
git clone https://github.com/hbelkadi/warehouse_automation_app.git
cd warehouse-automation
```
### 2. **Set Up a Python Virtual Environment**
   - Create a virtual environment for Python dependencies.
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```    
### 3. **Install Dependencies**
   - Install the required Python packages for Odoo integration.
   ```bash
   pip install -r requirements.txt
   ```
     
### 4. **Install Odoo 15**
   - Follow the [Odoo 15 installation guide on GitHub](https://github.com/odoo/odoo/tree/15.0) to install Odoo on Ubuntu.

### 5. **Configure PostgreSQL**
   - Set up a PostgreSQL database and configure your Odoo instance to use it.

### 6. **Configure the Odoo Module**
   - Add this module to your Odoo instance and update the database.
   ```bash
   ./odoo-bin -c <config_file_path> -u all -d <DB_name>
   ```
   
### 7. **Run the Application**
   - Start the Odoo instance with the configured database.

## Configuration
After installation, configure the RFID reader settings:
1. Access the **RFID Tag** menu from the module.
2. Link each RFID tag to a product and location.
3. For each RFID reader location, assign the appropriate product and tracking configurations.


## Demo Mode (No RFID Reader)
If you do not have an RFID reader, you can simulate RFID scans using demo data:
1. Use the Odoo interface to create demo RFID tags in the **RFID Tag** menu.
2. Run the demo script in the `demos` folder to simulate scanning events, which will update stock and location changes as if they were triggered by a real RFID scan.
```bash
python3 demo.py
```

## References
- [Odoo 15 Repository](https://github.com/odoo/odoo/tree/15.0)
- [Odoo Documentation](https://www.odoo.com/documentation/15.0/)
- [XML-RPC in Python](https://docs.python.org/3/library/xmlrpc.client.html)

## Good Practices
- Use a Python virtual environment (`venv`) to manage dependencies and avoid conflicts.
- Regularly back up your Odoo database to prevent data loss.
- Follow production best practices, such as configuring Nginx as a reverse proxy for Odoo.

## License
This project is licensed under the AGPL License.
