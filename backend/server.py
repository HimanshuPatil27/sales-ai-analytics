from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List
from datetime import datetime, timezone
from collections import defaultdict


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()
api_router = APIRouter(prefix="/api")


class SalesMetrics(BaseModel):
    revenue: dict
    orders: dict
    customers: dict


class RevenueData(BaseModel):
    month: str
    revenue: float
    orders: int


class OrdersData(BaseModel):
    date: str
    orders: int
    completed: int


class OrderRecord(BaseModel):
    id: str
    customer: str
    amount: float
    status: str
    date: str


@api_router.get("/")
async def root():
    return {"message": "Sales Analytics API", "version": "1.0.0"}


@api_router.get("/analytics/metrics", response_model=SalesMetrics)
async def get_metrics():
    sales = await db.sales.find({}, {"_id": 0}).to_list(1000)
    
    if not sales:
        return {
            "revenue": {"current": 0, "previous": 0, "change": 0, "trend": "neutral"},
            "orders": {"current": 0, "previous": 0, "change": 0, "trend": "neutral"},
            "customers": {"current": 0, "previous": 0, "change": 0, "trend": "neutral"}
        }
    
    total_revenue = sum(sale['amount'] for sale in sales)
    total_orders = len(sales)
    unique_customers = len(set(sale['customer_name'] for sale in sales))
    
    sales_sorted = sorted(sales, key=lambda x: x['date'])
    midpoint = len(sales_sorted) // 2
    first_half = sales_sorted[:midpoint]
    second_half = sales_sorted[midpoint:]
    
    prev_revenue = sum(sale['amount'] for sale in first_half)
    curr_revenue = sum(sale['amount'] for sale in second_half)
    revenue_change = ((curr_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
    
    prev_orders = len(first_half)
    curr_orders = len(second_half)
    orders_change = ((curr_orders - prev_orders) / prev_orders * 100) if prev_orders > 0 else 0
    
    return {
        "revenue": {
            "current": total_revenue,
            "previous": prev_revenue,
            "change": round(revenue_change, 1),
            "trend": "up" if revenue_change > 0 else "down"
        },
        "orders": {
            "current": total_orders,
            "previous": prev_orders,
            "change": round(orders_change, 1),
            "trend": "up" if orders_change > 0 else "down"
        },
        "customers": {
            "current": unique_customers,
            "previous": unique_customers,
            "change": 0,
            "trend": "neutral"
        }
    }


@api_router.get("/analytics/revenue", response_model=List[RevenueData])
async def get_revenue_data():
    sales = await db.sales.find({}, {"_id": 0}).to_list(1000)
    
    if not sales:
        return []
    
    monthly_data = defaultdict(lambda: {"revenue": 0, "orders": 0})
    
    for sale in sales:
        date_obj = datetime.strptime(sale['date'], '%Y-%m-%d')
        month_key = date_obj.strftime('%b')
        monthly_data[month_key]["revenue"] += sale['amount']
        monthly_data[month_key]["orders"] += 1
    
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    result = []
    for month in month_order:
        if month in monthly_data:
            result.append({
                "month": month,
                "revenue": monthly_data[month]["revenue"],
                "orders": monthly_data[month]["orders"]
            })
    
    return result


@api_router.get("/analytics/orders", response_model=List[OrdersData])
async def get_orders_data():
    return [
        {"date": "Week 1", "orders": 412, "completed": 398},
        {"date": "Week 2", "orders": 445, "completed": 430},
        {"date": "Week 3", "orders": 478, "completed": 465},
        {"date": "Week 4", "orders": 512, "completed": 495}
    ]


@api_router.get("/analytics/recent-orders", response_model=List[OrderRecord])
async def get_recent_orders():
    sales = await db.sales.find({}, {"_id": 0}).sort("date", -1).limit(5).to_list(5)
    
    return [
        {
            "id": sale['order_id'],
            "customer": sale['customer_name'],
            "amount": sale['amount'],
            "status": sale['status'],
            "date": sale['date']
        }
        for sale in sales
    ]


app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()