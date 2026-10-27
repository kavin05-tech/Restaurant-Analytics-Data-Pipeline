select restaurant_id, trim(name) as restaurant_name, trim(city) as city, trim(cuisine) as cuisine, rating::numeric(2,1) as rating, average_cost_for_two::integer as average_cost_for_two, case lower(trim(online_order)) when 'yes' then true when 'no' then false else null end as online_order
from raw.restaurants
