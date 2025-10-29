from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Product API",
    description="API with CI/CD",
    version="1.0.0"
)

products = {}
next_id = 1


class Product(BaseModel):
    name: str
    price: float
    description: Optional[str] = None


class ProductResponse(Product):
    id: int


@app.get("/")
def read_root():
    return {
    "message": "Product API with CI/CD",
    "version": "1.0.0",
    "health": "/health",
    "port": 14125
}



@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/products", response_model=List[ProductResponse])
def get_products():
    return [{"id": k, **v} for k, v in products.items()]


@app.post("/products", response_model=ProductResponse, status_code=201)
def create_product(product: Product):
    global next_id
    products[next_id] = product.dict()
    next_id_value = next_id
    next_id += 1
    return {"id": next_id_value, **product.dict()}


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"id": product_id, **products[product_id]}
