# Workbench Assistant

A lightweight personal work assistant API for organizing bookkeeping records,
project tasks, research notes, drafts, general notes, and email triage.

Repository target: `github.com/swordenkisk/workbench-assistant`

## Features

- Store and organize items by category.
- Track status, priority, due date, and optional monetary amount.
- Filter items by category or status.
- Update and delete records.
- Triage pasted email text with explainable keyword rules.
- Use SQLite by default; configure another SQLAlchemy-supported database with
  `DATABASE_URL`.

## Requirements

- Python 3.11 or later

## Setup

```bash
git clone https://github.com/swordenkisk/workbench-assistant.git
cd workbench-assistant

python -m venv .venv
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1

pip install -e ".[dev]"
cp .env.example .env
```

## Run

```bash
uvicorn app.main:app --reload
```

Interactive API documentation is available at `/docs`; the health check is
available at `/health`.

## Example requests

Create a project task:

```bash
curl -X POST http://127.0.0.1:8000/items \
  -H "Content-Type: application/json" \
  -d '{
    "category": "project",
    "title": "Prepare launch checklist",
    "content": "Collect final review items.",
    "priority": "high",
    "details": {"project": "Website launch"}
  }'
```

Create a bookkeeping record:

```bash
curl -X POST http://127.0.0.1:8000/items \
  -H "Content-Type: application/json" \
  -d '{
    "category": "bookkeeping",
    "title": "Hosting invoice",
    "amount": 24.00,
    "details": {"currency": "USD", "type": "expense"}
  }'
```

List research records:

```bash
curl "http://127.0.0.1:8000/items?category=research"
```

Triage an email without connecting to an email account:

```bash
curl -X POST http://127.0.0.1:8000/triage/email \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Invoice payment due",
    "body": "Please confirm payment by the deadline today."
  }'
```

## API overview

- `GET /health` — service status
- `POST /items` — create an item
- `GET /items` — list items; optional `category`, `status`, and `limit`
- `GET /items/{item_id}` — retrieve an item
- `PATCH /items/{item_id}` — update an item
- `DELETE /items/{item_id}` — delete an item
- `POST /triage/email` — classify pasted email text

Valid item categories are `bookkeeping`, `project`, `research`, `draft`,
`email`, and `note`. Priority values are `low`, `normal`, `high`, and `urgent`.

## Configuration

`DATABASE_URL` defaults to `sqlite:///./workbench.db`. Copy `.env.example` to
`.env` and change the value to configure another SQLAlchemy-supported database.

No AI provider key is required by this MVP. Email triage is rule-based, and
the service does not connect to an inbox or send messages.

## Scope

This is a starter application, not accounting software or a complete project
management system. Bookkeeping records are basic records, not double-entry
accounting. Before production use, add authentication, authorization,
database migrations, backups, audit logging, and tests. Add email-provider
OAuth only when a specific provider and permission scope are selected.


Run it with uvicorn app.main:app --reload. The generated database file is created automatically on startup.