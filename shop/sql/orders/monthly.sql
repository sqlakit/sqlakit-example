-- Orders of a team's users per month, each month as a JSON summary.
SELECT
    tpl.period(o.placed_at, 'month') AS month,
    tpl.json_object('orders', count(*), 'cents', sum(o.total_cents)) AS summary
FROM orders AS o
JOIN users AS u ON u.id = o.user_id
WHERE u.team_id = :team.id AND tpl.paid(o)
GROUP BY month
ORDER BY month
