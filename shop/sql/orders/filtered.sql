-- Orders of the user the call names, if it names one, and only the paid ones
-- unless the call asks for every order.
SELECT o.id, o.status
FROM orders AS o
WHERE
    tpl.if_set(
        :user_name,
        EXISTS (
            SELECT 1
            FROM users AS u
            WHERE u.id = o.user_id AND u.name = :user_name
        )
    )
    AND tpl.unless_set(:include_unpaid, tpl.paid(o))
ORDER BY o.id
