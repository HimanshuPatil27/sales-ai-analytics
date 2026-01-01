import csv
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import asyncio
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def ingest_sales_data():
    csv_file = ROOT_DIR / 'data' / 'sample_sales.csv'
    
    print(f"Reading CSV file: {csv_file}")
    
    await db.sales.delete_many({})
    print("Cleared existing sales data")
    
    sales_records = []
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            record = {
                'order_id': row['order_id'],
                'customer_name': row['customer_name'],
                'amount': float(row['amount']),
                'status': row['status'],
                'date': row['date']
            }
            sales_records.append(record)
    
    if sales_records:
        result = await db.sales.insert_many(sales_records)
        print(f"Inserted {len(result.inserted_ids)} sales records")
    else:
        print("No records to insert")
    
    total = await db.sales.count_documents({})
    print(f"Total records in database: {total}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(ingest_sales_data())