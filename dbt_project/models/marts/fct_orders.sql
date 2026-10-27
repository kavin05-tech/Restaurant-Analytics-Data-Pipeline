select o.order_id, o.customer_id, o.restaurant_id, o.order_date, o.order_amount, o.status, (o.status = 'delivered') as is_delivered, rv.review_count, rv.average_review_rating
from {{ ref('stg_orders') }} o
left join (
    select order_id, count(*) as review_count, round(avg(rating)::numeric, 2) as average_review_rating
    from {{ ref('stg_reviews') }}
    group by order_id
) rv on o.order_id = rv.order_id
