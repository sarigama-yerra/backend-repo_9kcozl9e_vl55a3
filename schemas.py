from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl

# Each Pydantic model corresponds to a Mongo collection with the class name lowercased
# e.g., Product -> "product", Order -> "order"

class Product(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    description: Optional[str] = Field(None, max_length=2000)
    price: float = Field(..., ge=0)
    image: Optional[HttpUrl] = None
    category: Optional[str] = Field(None, max_length=80)
    in_stock: int = Field(0, ge=0)
    featured: bool = False

class OrderItem(BaseModel):
    product_id: str
    quantity: int = Field(..., ge=1)
    unit_price: float = Field(..., ge=0)
    name: str
    image: Optional[str] = None

class CustomerInfo(BaseModel):
    full_name: str
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None

class Order(BaseModel):
    items: List[OrderItem]
    subtotal: float = Field(..., ge=0)
    shipping: float = Field(0, ge=0)
    total: float = Field(..., ge=0)
    customer: Optional[CustomerInfo] = None
    status: str = Field("pending")
