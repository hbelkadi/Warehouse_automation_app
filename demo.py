import sys
import xmlrpc.client
from datetime import datetime

# Odoo XML-RPC credentials and endpoint
ODOO_URL = 'http://localhost:8069/'
ODOO_DB = 'warehouseDB'
ODOO_USER = 'admin'
ODOO_PASSWORD = 'admin'
ODOO_RFID_MODEL = 'rfid.tag'
ODOO_PRODUCT_MODEL = 'product.product'
ODOO_LOCATION_MODEL = 'stock.location'
ODOO_QUANT_MODEL = 'stock.quant'

def update_inventory(product_id, location_id, is_new_epc):
    """Updates inventory levels in Odoo only for new EPCs."""
    try:
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(ODOO_URL))
        uid = common.authenticate(ODOO_DB, ODOO_USER, ODOO_PASSWORD, {})

        if uid:
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(ODOO_URL))

            # Search for existing stock.quant for the product and location
            quant_ids = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
                ODOO_QUANT_MODEL, 'search', [[['product_id', '=', product_id], ['location_id', '=', location_id]]])

            if quant_ids and is_new_epc:
                # Update the existing stock.quant (e.g., increment quantity by 1 for new EPCs)
                quant = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, ODOO_QUANT_MODEL, 'read', [quant_ids, ['quantity']])
                new_quantity = quant[0]['quantity'] + 1  # Increase quantity by 1 (example)
                models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, ODOO_QUANT_MODEL, 'write', [
                    quant_ids, {'quantity': new_quantity}
                ])
                print(f"Updated stock.quant for product {product_id} at location {location_id}, new quantity: {new_quantity}")
            elif not quant_ids and is_new_epc:
                # Create a new stock.quant (assuming quantity is 1 for demonstration purposes)
                models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, ODOO_QUANT_MODEL, 'create', [{
                    'product_id': product_id,
                    'location_id': location_id,
                    'quantity': 1
                }])
                print(f"Created new stock.quant for product {product_id} at location {location_id} with quantity 1.")
        else:
            print("Failed to authenticate to Odoo.")
    except Exception as e:
        print(f"Error updating inventory in Odoo: {str(e)}")

def send_to_odoo(epc, location_name, product_name):
    """Sends or updates EPC data in Odoo via XML-RPC, and updates inventory."""
    try:
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(ODOO_URL))
        uid = common.authenticate(ODOO_DB, ODOO_USER, ODOO_PASSWORD, {})

        if uid:
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(ODOO_URL))

            # Find product_id based on product name
            product_ids = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
                ODOO_PRODUCT_MODEL, 'search', [[['name', '=', product_name]]])
            product_id = product_ids[0] if product_ids else False

            # Find last_scan_location based on location_name
            location_ids = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
                ODOO_LOCATION_MODEL, 'search', [[['name', '=', location_name]]])
            location_id = location_ids[0] if location_ids else False

            # Set current time as last_scan_time
            last_scan_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

            # Search for existing EPC record
            existing_ids = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
                ODOO_RFID_MODEL, 'search', [[['epc_code', '=', epc]]])

            if existing_ids:
                # Check if the existing EPC is linked to a different product
                existing_record = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
                                                    ODOO_RFID_MODEL, 'read', [existing_ids, ['product_id']])
                existing_product_id = existing_record[0]['product_id'][0]

                if existing_product_id != product_id:
                    raise ValueError(f"Error: The same EPC ({epc}) is associated with two different products.")

                # Update existing record if it's the same product
                models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, ODOO_RFID_MODEL, 'write', [
                    existing_ids, {
                        'last_scan_time': last_scan_time,
                        'last_scan_location': location_id
                    }
                ])
                print(f"Successfully updated record in Odoo: EPC={epc}, Product Name={product_name}, Location={location_name}, Timestamp={last_scan_time}")

                # No need to update inventory as the same EPC exists for the same product
                update_inventory(product_id, location_id, is_new_epc=False)

            else:
                # Create new record for a new EPC
                data = {
                    'epc_code': epc,
                    'product_id': product_id,
                    'last_scan_time': last_scan_time,
                    'last_scan_location': location_id,
                }
                models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, ODOO_RFID_MODEL, 'create', [data])
                print(f"Successfully created record in Odoo: EPC={epc}, Product Name={product_name}, Location={location_name}, Timestamp={last_scan_time}")

                # Update the inventory for this product and location (new EPC means new quantity)
                update_inventory(product_id, location_id, is_new_epc=True)

        else:
            print("Failed to authenticate to Odoo.")
    except Exception as e:
        print(f"Error sending to Odoo: {str(e)}")

def main():
    if len(sys.argv) != 4:
        print("Usage: python create_or_update_odoo_record.py <EPC> <Location> <Product Name>")
        sys.exit(1)

    epc = sys.argv[1]
    location_name = sys.argv[2]
    product_name = sys.argv[3]

    send_to_odoo(epc, location_name, product_name)

if __name__ == "__main__":
    main()
