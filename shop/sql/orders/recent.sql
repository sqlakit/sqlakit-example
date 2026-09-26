-- Paid orders in a period, with statuses left out or kept.
SELECT
    o.id,
    o.user_id,
    o.status,
    o.total_cents,
    o.placed_at
FROM orders AS o
WHERE
    tpl.paid(o)
    AND tpl.between(o.placed_at, :since, :until, '[)')
    AND tpl.in_list(o.status, :statuses, :exclude)
