-- 1. Conversion funnel
SELECT 
    ab_group,
    COUNT(*) as total_listings,
    SUM(CASE WHEN has_reviews = 1 THEN 1 ELSE 0 END) as with_reviews,
    SUM(CASE WHEN bookings > 0 THEN 1 ELSE 0 END) as with_bookings,
    ROUND(100.0 * SUM(CASE WHEN bookings > 0 THEN 1 ELSE 0 END) / COUNT(*), 2) as booking_conversion_pct
FROM listings
GROUP BY ab_group;

-- 2. Revenue distribution
SELECT 
    ab_group,
    price_tier,
    COUNT(*) as listings,
    ROUND(SUM(revenue), 2) as total_revenue,
    ROUND(AVG(revenue), 2) as avg_revenue
FROM listings
GROUP BY ab_group, price_tier
ORDER BY ab_group, total_revenue DESC;

-- 3. Instant bookable impact
SELECT 
    ab_group,
    instant_bookable,
    COUNT(*) as listings,
    ROUND(AVG(booking_rate), 4) as avg_booking_rate,
    ROUND(AVG(revenue), 2) as avg_revenue
FROM listings
GROUP BY ab_group, instant_bookable;

-- 4. Summary statistics
SELECT 
    'Overall' as metric_type,
    ROUND(AVG(price), 2) as avg_price,
    ROUND(AVG(bookings), 2) as avg_bookings,
    ROUND(AVG(revenue), 2) as avg_revenue,
    ROUND(SUM(revenue), 2) as total_revenue
FROM listings
UNION ALL
SELECT 
    'Group A' as metric_type,
    ROUND(AVG(price), 2) as avg_price,
    ROUND(AVG(bookings), 2) as avg_bookings,
    ROUND(AVG(revenue), 2) as avg_revenue,
    ROUND(SUM(revenue), 2) as total_revenue
FROM listings
WHERE ab_group = 'A'
UNION ALL
SELECT 
    'Group B' as metric_type,
    ROUND(AVG(price), 2) as avg_price,
    ROUND(AVG(bookings), 2) as avg_bookings,
    ROUND(AVG(revenue), 2) as avg_revenue,
    ROUND(SUM(revenue), 2) as total_revenue
FROM listings
WHERE ab_group = 'B';