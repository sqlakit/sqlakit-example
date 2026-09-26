-- The version of the database, which each one reports its own way.
SELECT
    tpl.on_dialect(sqlite = sqlite_version(), postgresql = version()) AS version
