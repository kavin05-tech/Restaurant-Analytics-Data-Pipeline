select review_id, customer_id, restaurant_id, order_id, rating::integer as rating, trim(review_text) as review_text, review_date::date as review_date
from raw.reviews
