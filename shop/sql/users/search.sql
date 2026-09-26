-- Active users, narrowed by whatever the request sends, one page at a time.
SELECT
    u.id,
    u.name,
    u.email
FROM users AS u
WHERE
    tpl.active(u)
    AND tpl.if_set(:teams, u.team_id IN (:teams))
    AND tpl.search(:q, u.name, u.email)
ORDER BY tpl.order_by(:sort, id, name, email, 'name')
LIMIT :limit OFFSET :offset
