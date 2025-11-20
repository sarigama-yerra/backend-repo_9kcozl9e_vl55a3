from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
from database import db, create_document, get_documents
from schemas import Product, Order

app = FastAPI(title="E-Commerce API", version="1.1.0")

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

@app.post("/products/seed", response_model=dict)
async def seed_products():
    # Check if at least one product exists
    existing = await get_documents("product", {}, 1)
    if existing:
        return {"status": "skipped", "message": "Products already exist"}

    samples = [
        Product(
            name="Aurora Wireless Headphones",
            description="Immersive sound, active noise cancellation, 40h battery, and a lightweight fit.",
            price=149.0,
            image="https://images.unsplash.com/photo-1518444132496-8893f3a2f8db?q=80&w=1200&auto=format&fit=crop",
            category="Audio",
            in_stock=25,
            featured=True,
        ),
        Product(
            name="Nebula Smartwatch",
            description="AMOLED display, 7-day battery life, fitness + sleep tracking, Bluetooth calls.",
            price=199.0,
            image="https://images.unsplash.com/photo-1511732351157-1865efcb7b7b?q=80&w=1200&auto=format&fit=crop",
            category="Wearables",
            in_stock=30,
            featured=True,
        ),
        Product(
            name="Flux Mechanical Keyboard",
            description="Hot-swappable switches, per-key RGB, wireless + USB-C, compact 75% layout.",
            price=129.0,
            image="https://images.unsplash.com/photo-1515879218367-8466d910aaa4?q=80&w=1200&auto=format&fit=crop",
            category="Accessories",
            in_stock=40,
            featured=False,
        ),
        Product(
            name="Prism 4K Monitor",
            description="Ultra-thin bezels, HDR10, 144Hz, color-accurate IPS panel for creators & gamers.",
            price=399.0,
            image="https://images.unsplash.com/photo-1517336714731-489689fd1ca8?q=80&w=1200&auto=format&fit=crop",
            category="Displays",
            in_stock=12,
            featured=False,
        ),
        Product(
            name="Halo Portable Speaker",
            description="Splash-proof, deep bass, 12h playtime, stereo pairing with multi-room support.",
            price=89.0,
            image="https://images.unsplash.com/photo-1546435770-a3e426bf472b?q=80&w=1200&auto=format&fit=crop",
            category="Audio",
            in_stock=50,
            featured=False,
        ),
        Product(
            name="Zen Laptop Stand",
            description="Ergonomic aluminum stand with adjustable height and cable management.",
            price=49.0,
            image="https://images.unsplash.com/photo-1516387938699-a93567ec168e?q=80&w=1200&auto=format&fit=crop",
            category="Accessories",
            in_stock=60,
            featured=False,
        ),
    ]

    created = 0
    for prod in samples:
        await create_document("product", prod.dict())
        created += 1

    return {"status": "created", "count": created}

# Orders Endpoints

@app.post("/orders", response_model=dict)
async def create_order(order: Order):
    doc_id = await create_document("order", order.dict())
    return {"id": str(doc_id)}

@app.get("/orders", response_model=List[dict])
async def list_orders(limit: int = 50):
    items = await get_documents("order", {}, limit)
    return items
