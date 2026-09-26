-- The active users of one team, passed as a `Team`.
SELECT
    u.id,
    u.name
FROM users AS u
WHERE tpl.of_team(u, :team) AND tpl.active(u)
ORDER BY u.id
