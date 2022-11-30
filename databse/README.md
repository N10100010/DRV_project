## Notes

- Foreign Key / Integrity checking: https://docs.sqlalchemy.org/en/14/core/constraints.html
- JSON typed columns with SQLAlchemy: https://amercader.net/blog/beware-of-json-fields-in-sqlalchemy/
    - Use: `Column(MutableDict.as_mutable(JSONB))`
