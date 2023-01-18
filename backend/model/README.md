# Database Model Notes

## Command line helpers

Create tables

    python -m backend.model.dbutils --create

Drop tables

    python -m backend.model.dbutils --drop

Insert a rowing competition from JSON file (World ROwing API Data Structure)

    python -m backend.model.dbutils --insert competition.json