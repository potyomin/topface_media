USE topface_media;

WITH
num AS (  -- числитель: деньги в M у тех, кто платил в M-1
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
den AS (  -- знаменатель: сумма M-1, «сдвинутая» на M
  SELECT
    DATE_FORMAT(CAST(CONCAT(s.month,'-01') AS DATE) + INTERVAL 1 MONTH, '%Y-%m') AS month,
    COALESCE(NULLIF(TRIM(pd.AM),''),'Без АМ') AS AM,
    SUM(s.shipment) AS den
  FROM shipments s
  JOIN projects_dim pd ON pd.id = s.id
  GROUP BY DATE_FORMAT(CAST(CONCAT(s.month,'-01') AS DATE) + INTERVAL 1 MONTH, '%Y-%m'),
           COALESCE(NULLIF(TRIM(pd.AM),''),'Без АМ')
)
SELECT n.month, n.AM, n.num, d.den, n.num/NULLIF(d.den,0) AS coef1
FROM num n
JOIN den d ON d.month = n.month AND d.AM = n.AM
ORDER BY n.month, n.AM;
