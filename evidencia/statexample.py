from functools import reduce

products = [
    {"name": "Laptop", "price": 800, "stock": 5},
    {"name": "Mouse", "price": 20, "stock": 0},
    {"name": "Teclado", "price": 50, "stock": 10}
]

names = list(map(lambda p: p["name"], products))

available = list(filter(lambda p: p["stock"] > 0, products))

total_value = reduce(
    lambda acc, p: acc + p["price"] * p["stock"],
    products,
    0
)

avg_price = sum(p["price"] for p in products) / len(products)

expensive = [p["name"] for p in products if p["price"] > 100]

print("Nombres:", names)
print("Disponibles:", available)
print("Valor total:", total_value)
print("Precio promedio:", avg_price)
print("Caros:", expensive)
