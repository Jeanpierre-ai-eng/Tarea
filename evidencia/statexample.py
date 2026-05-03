from functools import reduce

products = [
    {"name": "Laptop", "price": 800, "stock": 5},
    {"name": "Mouse", "price": 20, "stock": 0},
    {"name": "Teclado", "price": 50, "stock": 10}
]

# map → nombres
names = list(map(lambda p: p["name"], products))

# filter → disponibles
available = list(filter(lambda p: p["stock"] > 0, products))

# reduce → valor total
total_value = reduce(
    lambda acc, p: acc + p["price"] * p["stock"],
    products,
    0
)

# promedio
avg_price = sum(p["price"] for p in products) / len(products)

# comprehension → productos caros
expensive = [p["name"] for p in products if p["price"] > 100]

print("Nombres:", names)
print("Disponibles:", available)
print("Valor total:", total_value)
print("Precio promedio:", avg_price)
print("Caros:", expensive)