-- Event Count
SELECT event_type, COUNT(*) AS count
FROM 'data/ecommerce.parquet'
GROUP BY event_type;

-- Conversion Rate
SELECT 
  COUNT(CASE WHEN event_type = 'purchase' THEN 1 END) * 100.0 /
  COUNT(CASE WHEN event_type = 'view' THEN 1 END) AS conversion_rate
FROM 'data/ecommerce.parquet';

-- Top Brands
SELECT brand, COUNT(*) AS total
FROM 'data/ecommerce.parquet'
GROUP BY brand
ORDER BY total DESC
LIMIT 10;

-- Revenue
SELECT SUM(price) AS revenue
FROM 'data/ecommerce.parquet'
WHERE event_type = 'purchase';