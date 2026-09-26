-- Users that are neither archived nor deleted.
SELECT NOT u.archived AND u.deleted_at IS NULL AS active FROM u;

-- Orders that were paid for.
SELECT o.status IN ('paid', 'shipped') AS paid FROM o;
