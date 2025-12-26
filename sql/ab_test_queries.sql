-- 1. Overall metrics by A/B group
SELECT 
    ab_group,
    COUNT(*) as total_listings,
    ROUND(AVG(price), 2) as avg_price,
    ROUND(AVG(booking_rate), 4) as avg_booking_rate,
    ROUND(AVG(bookings), 2) as avg_bookings,
    ROUND(AVG(revenue), 2) as avg_revenue
FROM listings
GROUP BY ab_group;

-- 2. Statistical comparison
WITH group_stats AS (
    SELECT 
        ab_group,
        AVG(booking_rate) as avg_booking_rate,
        AVG(revenue) as avg_revenue,
        COUNT(*) as sample_size
    FROM listings
    GROUP BY ab_group
)
SELECT 
    a.ab_group as group_a,
    b.ab_group as group_b,
    ROUND((b.avg_booking_rate - a.avg_booking_rate) / a.avg_booking_rate * 100, 2) as booking_rate_lift_pct,
    ROUND((b.avg_revenue - a.avg_revenue) / a.avg_revenue * 100, 2) as revenue_lift_pct
FROM group_stats a
CROSS JOIN group_stats b
WHERE a.ab_group = 'A' AND b.ab_group = 'B';

-- 3. Metrics by room type
SELECT 
    ab_group,
    room_type,
    COUNT(*) as listings,
    ROUND(AVG(price), 2) as avg_price,
    ROUND(AVG(bookings), 2) as avg_bookings,
    ROUND(AVG(revenue), 2) as avg_revenue
FROM listings
GROUP BY ab_group, room_type
ORDER BY ab_group, avg_revenue DESC;

-- 4. Metrics by neighborhood
SELECT 
    ab_group,
    neighborhood,
    COUNT(*) as listings,
    ROUND(AVG(booking_rate), 4) as avg_booking_rate,
    ROUND(SUM(revenue), 2) as total_revenue
FROM listings
GROUP BY ab_group, neighborhood
ORDER BY ab_group, total_revenue DESC;

-- 5. Top performers in each group
SELECT 
    ab_group,
    listing_id,
    name,
    price,
    bookings,
    revenue
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY ab_group ORDER BY revenue DESC) as rank
    FROM listings
)
WHERE rank <= 10
ORDER BY ab_group, revenue DESC;