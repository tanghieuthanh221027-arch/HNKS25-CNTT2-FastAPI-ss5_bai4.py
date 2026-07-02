from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

products = [
    {"id": 1, "code": "SP001", "name": "Keyboard", "price": 500000, "stock": 10},
    {"id": 2, "code": "SP002", "name": "Mouse", "price": 300000, "stock": 5}
]

class ProductUpdate(BaseModel):
    code: str
    name: str
    price: float
    stock: int


@app.put("/products/{product_id}")
def update_product(product_id: int, request: ProductUpdate):
    product = None

    for item in products:
        if item["id"] == product_id:
            product = item
            break

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    for item in products:
        if (item["code"] == request.code and item["id"] != product_id):
            raise HTTPException(
                status_code=400,
                detail="Product code already exists"
            )

    if request.name.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Product name cannot be empty"
        )

    if request.price <= 0:
        raise HTTPException(
            status_code=400,
            detail="Price must be greater than 0"
        )

    if request.stock < 0:
        raise HTTPException(
            status_code=400,
            detail="Stock must be greater than or equal to 0"
        )

    product["code"] = request.code
    product["name"] = request.name
    product["price"] = request.price
    product["stock"] = request.stock

    return {
        "message": "Product updated successfully",
        "data": product
    }