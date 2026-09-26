-- Each team's target, sent with the call, against the orders it placed.
SELECT
    t.name,
    v.column2 AS target,
    count(o.id) AS orders
FROM tpl.values(:targets) AS v
INNER JOIN teams AS t ON v.column1 = t.id
LEFT JOIN users AS u ON t.id = u.team_id
LEFT JOIN orders AS o ON u.id = o.user_id AND tpl.paid(o)
GROUP BY t.name, v.column2
ORDER BY t.name
