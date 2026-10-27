import csv
from datetime import date, timedelta
from pathlib import Path

OUT = Path(__file__).resolve().parent

restaurants = [
    (101, "Spice Route", "Bengaluru", "Indian", 4.3, 450, "Yes"),
    (102, "Namma Dosa", "Bengaluru", "South Indian", 4.1, 220, "Yes"),
    (103, "Wok This Way", "Mumbai", "Chinese", 4.0, 500, "No"),
    (104, "The Green Bowl", "Delhi", "Healthy", 4.5, 380, "Yes"),
    (105, "Pizza Yard", "Mumbai", "Italian", 3.9, 600, "Yes"),
]
orders = [
    (1001, 1, 101, "2025-01-03", 520, "delivered"),
    (1002, 2, 102, "2025-01-04", 240, "delivered"),
    (1003, 1, 103, "2025-01-05", 680, "delivered"),
    (1004, 3, 104, "2025-01-06", 410, "cancelled"),
    (1005, 4, 105, "2025-01-07", 750, "delivered"),
    (1006, 2, 101, "2025-01-08", 460, "delivered"),
    (1007, 5, 103, "2025-01-09", 540, "delivered"),
    (1008, 3, 104, "2025-01-10", 390, "delivered"),
    (1009, 4, 102, "2025-01-11", 260, "delivered"),
    (1010, 5, 105, "2025-01-12", 610, "delivered"),
    (1011, 1, 104, "2025-01-13", 430, "delivered"),
    (1012, 2, 103, "2025-01-14", 570, "delivered"),
]
reviews = [
    (2001, 1, 101, 1001, 5, "Aromatic food and quick delivery", "2025-01-04"),
    (2002, 2, 102, 1002, 4, "Crispy dosa, chutney was fresh", "2025-01-05"),
    (2003, 1, 103, 1003, 3, "Good flavors but arrived a little late", "2025-01-06"),
    (2004, 4, 105, 1005, 5, "Excellent pizza, will order again", "2025-01-08"),
    (2005, 2, 101, 1006, 4, "Tasty biryani and generous portion", "2025-01-09"),
    (2006, 5, 103, 1007, 2, "Too salty and the noodles were cold", "2025-01-10"),
    (2007, 3, 104, 1008, 5, "Fresh ingredients, healthy and delicious", "2025-01-11"),
    (2008, 4, 102, 1009, 3, "Decent meal, packaging could improve", "2025-01-12"),
    (2009, 5, 105, 1010, 4, "Great crust, slightly expensive", "2025-01-13"),
    (2010, 1, 104, 1011, 5, "Loved the bowl and fast service", "2025-01-14"),
    (2011, 2, 103, 1012, 4, "Fresh and flavorful stir fry", "2025-01-15"),
]

def write(name, rows):
    with (OUT / name).open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(rows[0])
        w.writerows(rows[1])

write("restaurants.csv", [("restaurant_id", "name", "city", "cuisine", "rating", "average_cost_for_two", "online_order"), restaurants])
write("orders.csv", [("order_id", "customer_id", "restaurant_id", "order_date", "order_amount", "status"), orders])
write("reviews.csv", [("review_id", "customer_id", "restaurant_id", "order_id", "rating", "review_text", "review_date"), reviews])
print(f"Generated 5 restaurants, {len(orders)} orders, {len(reviews)} reviews in {OUT}")
