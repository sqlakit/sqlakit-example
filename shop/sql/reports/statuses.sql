-- The orders in each status the call names, and 0 for a status with none.
-- `tpl.each` writes a parameter per status, for a list outside `IN`.
WITH wanted AS (
    SELECT value AS status
    FROM json_each(json_array(tpl.each(:statuses)))
)

SELECT
    w.status,
    count(o.id) AS orders
FROM wanted AS w
LEFT JOIN orders AS o ON w.status = o.status
GROUP BY w.status
ORDER BY w.status
