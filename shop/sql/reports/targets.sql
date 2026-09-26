-- Each team's target, sent with the call, against the orders it placed.
SELECT t.name, v.column2 AS target, count(o.id) AS orders
FROM tpl.values(:targets) AS v
JOIN teams AS t ON t.id = v.column1
LEFT JOIN users AS u ON u.team_id = t.id
LEFT JOIN orders AS o ON o.user_id = u.id AND tpl.paid(o)
GROUP BY t.name, v.column2
ORDER BY t.name
