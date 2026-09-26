-- Users sorted by a column the request picks, among those listed.
SELECT
    u.id,
    u.name,
    u.email
FROM users AS u
ORDER BY tpl.identifier(:sort_by, id, name, email), u.id
