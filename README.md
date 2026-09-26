# sqlakit-example

A small shop on SQLite: teams, users and orders, read through
[SQLAKit](https://sqlakit.readthedocs.io/en/stable/) SQL templates. Every kind
of template and macro is here once, in a query that runs, with a test that
checks what it returns.

```console
$ uv sync
$ uv run python -m shop.seed    # writes shop.db
$ uv run python -m shop         # runs every query and prints the rows
$ uv run poe test
```

`uv run poe lint` checks the Python with `ruff` and `ty`, the templates with
`sqlakit check`, and the SQL with `sqruff`. `uv run poe fmt` formats both with
`ruff` and `sqruff fix`.

## What is where

| feature | file |
| --- | --- |
| templates, macros and the database, configured once | [`shop/db.py`](shop/db.py) |
| `:name` parameters, `IN (:teams)`, `LIMIT :limit` with no value | [`users/search.sql`](shop/sql/users/search.sql) |
| `tpl.if_set`, `tpl.order_by` from a sort string | [`users/search.sql`](shop/sql/users/search.sql) |
| a Python macro that builds SQL from values: `owned_by`, `search` | [`shop/macros.py`](shop/macros.py), [`users/owned.sql`](shop/sql/users/owned.sql) |
| a Python macro that asks the dialect: `money`, `period` with `Literal` | [`shop/macros.py`](shop/macros.py), [`orders/monthly.sql`](shop/sql/orders/monthly.sql) |
| macros written in SQL: `active`, `paid` | [`shop/sql/_macros.sql`](shop/sql/_macros.sql) |
| a macro with its SQL in a file and its values from Python: `of_team` | [`shop/tenant.py`](shop/tenant.py), [`shop/tenant.sql`](shop/tenant.sql) |
| `tpl.between`, `tpl.in_list` | [`orders/recent.sql`](shop/sql/orders/recent.sql) |
| `tpl.include`, sharing the parameters, `tpl.string_agg` | [`orders/by_user.sql`](shop/sql/orders/by_user.sql) |
| a dotted parameter, `:team.id`, and `tpl.json_object` | [`orders/monthly.sql`](shop/sql/orders/monthly.sql) |
| `tpl.if_set` around `EXISTS`, `tpl.unless_set` | [`orders/filtered.sql`](shop/sql/orders/filtered.sql) |
| `tpl.values`, a table sent with the call | [`reports/targets.sql`](shop/sql/reports/targets.sql) |
| `Inline.name`, a table name written into the SQL | [`reports/count.sql`](shop/sql/reports/count.sql) |
| `tpl.identifier`, a column the request picks | [`reports/sorted.sql`](shop/sql/reports/sorted.sql) |
| `tpl.on_dialect` | [`reports/version.sql`](shop/sql/reports/version.sql) |
| `tpl.icollate`, a name found whatever its case | [`users/named.sql`](shop/sql/users/named.sql) |
| `tpl.each`, a list outside `IN`, in a CTE | [`reports/statuses.sql`](shop/sql/reports/statuses.sql) |
| a window function in a CTE, and `money` | [`reports/top_spenders.sql`](shop/sql/reports/top_spenders.sql) |
| a function per template, `db.sql("...")` | [`shop/queries.py`](shop/queries.py) |
| tests in a transaction that rolls back, with the pytest plugin | [`tests/`](tests) |

## Tools

`sqlakit check` reads the code, finds the templates and the macros, and checks
every template:

```console
$ uv run sqlakit check
templates: shop/sql (shop/db.py:13)
namespace: tpl (the default)
macros: 5 in Python, 1 file of SQL macros
dialect: sqlite (shop/db.py:11)

14 templates, 0 problems
```

`sqlakit export sqruff` wrote the `[tool.sqruff]` tables of `pyproject.toml`,
so `sqruff` reads the templates as SQL:

```console
$ uv run sqruff lint shop
```

The shop runs every rule `sqruff` has, `rules = "all"`, with keywords in upper
case. It turns off five that a macro's call trips while the template is fine:
`RF01`, `RF02` and `RF03` read a table a macro takes, as in `tpl.paid(o)`, as a
column, and `AL05` and `ST03` miss an alias or a CTE used only inside a
macro's arguments.

The editor extensions run [`sqlakit-lsp`](https://github.com/sqlakit/sqlakit-lsp)
with `uvx`, so the project doesn't install it. A template gets completion after
`tpl.`, hover, go to definition, and references: every call of `tpl.active`,
or everything that reads `orders/recent.sql`.

In VS Code, `.vscode/` recommends the
[SQLAKit extension](https://github.com/sqlakit/sqlakit-vscode), `ty`, `ruff`
and `sqruff`. It runs Python from `.venv`, checks the types with `ty` in place
of the Python extension's server, formats the Python with `ruff` and a
template with `sqruff` on save, and turns on the colours of macros and
parameters. The `sqruff` extension takes its path only from your user
settings, not the project's: add
`"sqruff.executablePath": "${workspaceFolder}/.venv/bin/sqruff"` there.

In Zed, install the [SQLAKit extension](https://github.com/sqlakit/sqlakit-zed).
`.zed/settings.json` runs `ty`, `ruff` and `sqlakit-lsp` for Python, `ty` and
`ruff` from `.venv` whichever Python Zed picked, so run `uv sync` first. On
save it formats the Python, sorts the imports and applies `ruff`'s fixes, and
formats a template with `sqruff fix`. For the colours of macros and
parameters, add `"semantic_tokens": "combined"` to your Zed settings.
