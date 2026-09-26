-- Users of any of the teams or the users named, and none when neither is.
SELECT u.id, u.name
FROM users AS u
WHERE tpl.owned_by(u, :teams, :users)
ORDER BY u.id
