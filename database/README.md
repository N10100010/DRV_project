## Docker commands

### Start and create tables

Compose up

    docker-compose up

Create tables

    python -m backend.model.dbutils --create

### Purge container instance and volume

Drop tables (optional)

    python -m backend.model.dbutils --drop

Compose down

    docker-compose down -v

## Notes

- Foreign Key / Integrity checking: https://docs.sqlalchemy.org/en/14/core/constraints.html
- JSON typed columns with SQLAlchemy: https://amercader.net/blog/beware-of-json-fields-in-sqlalchemy/
    - Use: `Column(MutableDict.as_mutable(JSONB))`
