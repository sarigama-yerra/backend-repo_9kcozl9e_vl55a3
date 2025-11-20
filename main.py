from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
from database import db, create_document, get_documents
from schemas import Product, Order

app = FastAPI(title="E-Commerce API", version="1.0.0")

# Enable CORS for all origins for dev convenience
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test")
async def test_connection():
    # simple ping to verify database connectivity
    try:
        await db.command("ping")
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

# Products Endpoints

@app.post("/products", response_model=dict)
async def create_product(product: Product):
    doc_id = await create_document("product", product.dict())
    return {"id": str(doc_id)}

@app.get("/products", response_model=List[dict])
async def list_products(category: Optional[str] = None, featured: Optional[bool] = None, limit: int = 50):
    filter_dict = {}
    if category:
        filter_dict["category"] = category
    if featured is not None:
        filter_dict["featured"] = featured
    items = await get_documents("product", filter_dict, limit)
    return items

# Orders Endpoints

@app.post("/orders", response_model=dict)
async def create_order(order: Order):
    doc_id = await create_document("order", order.dict())
    return {"id": str(doc_id)}

@app.get("/orders", response_model=List[dict])
async def list_orders(limit: int = 50):
    items = await get_documents("order", {}, limit)
    return items
