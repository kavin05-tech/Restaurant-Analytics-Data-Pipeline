select restaurant_id, restaurant_name, city, cuisine, rating as listed_rating, average_cost_for_two, online_order
from {{ ref('stg_restaurants') }}
