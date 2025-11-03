USE topface_media;

WITH
num AS (
  SELECT
    cur.month,
    COALESCE(NULLIF(TRIM(pd.AM),''),'Без АМ') AS AM,
    SUM(cur.shipment) AS num
  FROM shipments cur
  JOIN shipments prev
    ON prev.id = cur.id
   AND prev.month = DATE_FORMAT(CAST(CONCAT(cur.month,'-01') AS DATE) - INTERVAL 1 MONTH, '%Y-%m')
  JOIN projects_dim pd ON pd.id = cur.id
  WHERE cur.month BETWEEN '2023-01' AND '2023-12'
  GROUP BY cur.month, COALESCE(NULLIF(TRIM(pd.AM),''),'Без АМ')
),
den AS (
  SELECT
    DATE_FORMAT(CAST(CONCAT(s.month,'-01') AS DATE) + INTERVAL 1 MONTH, '%Y-%m') AS month,
    COALESCE(NULLIF(TRIM(pd.AM),''),'Без АМ') AS AM,
    SUM(s.shipment) AS den
  FROM shipments s
  JOIN projects_dim pd ON pd.id = s.id
  GROUP BY DATE_FORMAT(CAST(CONCAT(s.month,'-01') AS DATE) + INTERVAL 1 MONTH, '%Y-%m'),
           COALESCE(NULLIF(TRIM(pd.AM),''),'Без АМ')
),
m AS (
  SELECT n.month, n.AM, n.num, d.den
  FROM num n JOIN den d ON d.month = n.month AND d.AM = n.AM
)
SELECT '2023' AS year, 'Отдел' AS AM,
       SUM(num) AS num_year,
       SUM(den) AS den_year,
       SUM(num)/NULLIF(SUM(den),0) AS coef1_year
FROM m;
