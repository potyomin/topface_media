USE topface_media;

WITH
base AS (
  SELECT COALESCE(NULLIF(TRIM(pd.AM),''),'Без АМ') AS AM,
         p2.id, p2.month AS m2, p2.shipment AS ship2
  FROM shipments p2
  JOIN projects_dim pd ON pd.id = p2.id
  LEFT JOIN shipments p1
    ON p1.id = p2.id
   AND p1.month = DATE_FORMAT(CAST(CONCAT(p2.month,'-01') AS DATE) + INTERVAL 1 MONTH, '%Y-%m')
  WHERE p1.id IS NULL
),
den AS (
  SELECT
    DATE_FORMAT(CAST(CONCAT(b.m2,'-01') AS DATE) + INTERVAL 2 MONTH, '%Y-%m') AS month,
    b.AM,
    SUM(b.ship2) AS den2
  FROM base b
  GROUP BY DATE_FORMAT(CAST(CONCAT(b.m2,'-01') AS DATE) + INTERVAL 2 MONTH, '%Y-%m'),
           b.AM
),
num AS (
  SELECT
    DATE_FORMAT(CAST(CONCAT(b.m2,'-01') AS DATE) + INTERVAL 2 MONTH, '%Y-%m') AS month,
    b.AM,
    SUM(c.shipment) AS num2
  FROM base b
  JOIN shipments c
    ON c.id = b.id
   AND c.month = DATE_FORMAT(CAST(CONCAT(b.m2,'-01') AS DATE) + INTERVAL 2 MONTH, '%Y-%m')
  GROUP BY DATE_FORMAT(CAST(CONCAT(b.m2,'-01') AS DATE) + INTERVAL 2 MONTH, '%Y-%m'),
           b.AM
),
m AS (
  SELECT n.month, n.AM, n.num2, d.den2
  FROM num n JOIN den d ON d.month = n.month AND d.AM = n.AM
  WHERE n.month BETWEEN '2023-01' AND '2023-12'
)
SELECT month, 'Отдел' AS AM,
       SUM(num2) AS num2, SUM(den2) AS den2,
       SUM(num2)/NULLIF(SUM(den2),0) AS coef2
FROM m
GROUP BY month
ORDER BY month;
