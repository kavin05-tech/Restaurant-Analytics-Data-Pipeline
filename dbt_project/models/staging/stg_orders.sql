select order_id, customer_id, restaurant_id, order_date::date as order_date, order_amount::numeric(10,2) as order_amount, lower(trim(status)) as status
from raw.orders
