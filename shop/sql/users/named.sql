-- The user of a name, whatever its case: `ada` finds Ada.
SELECT
    u.id,
    u.name
FROM users AS u
WHERE tpl.icollate(u.name) = tpl.icollate(:name)
