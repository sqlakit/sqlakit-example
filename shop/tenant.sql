-- The SQL of `of_team` in tenant.py. `:team_id` is the value it returns.
SELECT u.team_id = :team_id AS of_team
FROM u;
