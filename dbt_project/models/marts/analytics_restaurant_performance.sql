select r.restaurant_id, r.restaurant_name, r.city, r.cuisine, count(o.order_id) as total_orders, count(*) filter (where o.is_delivered) as delivered_orders, coalesce(sum(o.order_amount) filter (where o.is_delivered), 0)::numeric(12,2) as delivered_revenue, round(avg(o.average_review_rating)::numeric, 2) as average_review_rating
from {{ ref('dim_restaurants') }} r left join {{ ref('fct_orders') }} o using (restaurant_id)
group by r.restaurant_id, r.restaurant_name, r.city, r.cuisine
