from fastapi import FastAPI, Query

app = FastAPI()

# ------------------ DATA ------------------

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics"},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery"},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics"},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery"},
]

orders = []

# ------------------ HOME ------------------

@app.get("/")
def home():
    return {"message": "FastAPI Working 🚀"}
@app.get("/products/search")
def search_products(keyword: str = Query(...)):
    result = []

    for p in products:
        if keyword.lower() in p["name"].lower():
            result.append(p)

    if len(result) == 0:
        return {"message": f"No products found for: {keyword}"}

    return {
        "keyword": keyword,
        "total_found": len(result),
        "products": result
    }
@app.get("/products/sort")
def sort_products(
    sort_by: str = Query("price"),
    order: str = Query("asc")
):
    if sort_by not in ["price", "name"]:
        return {"error": "sort_by must be 'price' or 'name'"}

    sorted_products = sorted(
        products,
        key=lambda p: p[sort_by],
        reverse=(order == "desc")
    )

    return {
        "sort_by": sort_by,
        "order": order,
        "products": sorted_products
    }
@app.get("/products/page")
def paginate_products(
    page: int = Query(1),
    limit: int = Query(2)
):
    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "limit": limit,
        "total_products": len(products),
        "products": products[start:end]
    }


@app.post("/orders")
def create_order(
    customer_name: str = Query(...),
    product_id: int = Query(...)
):
    product = None

    # find product
    for p in products:
        if p["id"] == product_id:
            product = p
            break

    # if not found
    if product is None:
        return {"error": "Product not found"}

    # create order
    order = {
        "order_id": len(orders) + 1,
        "customer_name": customer_name,
        "product": product
    }

    orders.append(order)

    return {
        "message": "Order created successfully",
        "order": order
    }
@app.get("/orders/search")
def search_orders(customer_name: str = Query(...)):
    result = []

    for o in orders:
        if customer_name.lower() in o["customer_name"].lower():
            result.append(o)

    if len(result) == 0:
        return {"message": f"No orders found for: {customer_name}"}

    return {
        "customer_name": customer_name,
        "total_found": len(result),
        "orders": result
    }
@app.get("/test-orders")
def test_orders():
    return orders
@app.get("/products")
def get_products():
    return {
        "total": len(products),
        "products": products
    }
@app.get("/orders")
def get_orders():
    return {
        "total_orders": len(orders),
        "orders": orders
    }
@app.get("/products/{product_id}")
def get_product(product_id: int):
    for p in products:
        if p["id"] == product_id:
            return p

    return {"error": "Product not found"}