-- What each user spent on the orders of orders/recent.sql, which shares
-- this template's parameters.
SELECT
    u.name,
    count(*) AS orders,
    tpl.money(sum(r.total_cents)) AS spent,
    tpl.string_agg(cast(r.id AS TEXT), ', ') AS order_ids
FROM (SELECT * FROM tpl.include('orders/recent.sql') AS o) AS r
JOIN users AS u ON u.id = r.user_id
GROUP BY u.name
ORDER BY
    tpl.order_by(:sort, name, orders, spent = sum(r.total_cents), 'spent.desc')
