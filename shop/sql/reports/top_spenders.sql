-- The users who spent most on paid orders in each team, and their place.
WITH spent AS (
    SELECT
        u.team_id,
        u.name,
        sum(o.total_cents) AS cents,
        rank() OVER (
            PARTITION BY u.team_id
            ORDER BY sum(o.total_cents) DESC
        ) AS place
    FROM users AS u
    INNER JOIN orders AS o ON u.id = o.user_id
    WHERE tpl.paid(o)
    GROUP BY u.team_id, u.name
)

SELECT
    t.name AS team,
    s.name,
    s.place,
    tpl.money(s.cents) AS spent
FROM spent AS s
INNER JOIN teams AS t ON s.team_id = t.id
WHERE s.place <= :top
ORDER BY t.name, s.place
