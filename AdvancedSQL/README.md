# Advanced SQL — SQL Mastery Project

## Overview

This project demonstrates advanced PostgreSQL database design, data integrity, relational queries, transaction safety, audit history, and index validation.

The project uses a dedicated `sql_mastery` schema inside the `sql_practice` database. It is separate from the existing `myapp` application database.

## Project Structure

```text
AdvancedSQL/
├── 01_create_schema.sql
├── 02_seed_data.sql
├── 03_validation_queries.sql
└── README.md
```

## Database Design

### Users

Stores the users who create and receive assigned support tickets.

- Identity-generated primary key
- Required username and email
- Unique username and email constraints
- Creation timestamp

### Tickets

Stores support tickets and their current status.

- Required title and creator
- Optional description and assignee
- Status values: `OPEN`, `IN_PROGRESS`, `RESOLVED`, `CLOSED`
- Priority values: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`
- Resolution timestamp validation
- Foreign keys for creator and assignee

### Audit Records

Stores events associated with tickets.

- Required ticket reference and event type
- Optional actor reference
- JSONB details
- Creation timestamp
- Approved event types enforced by a check constraint
- Append-only trigger rejecting ordinary `UPDATE` and `DELETE` operations

**Security note:** The trigger is a learning-project safeguard, not tamper-proof auditing. A table owner or sufficiently privileged database role may be able to change or bypass the protection. Production systems should use separate ownership, restricted application permissions, and additional audit controls.

## Supporting Indexes

The project includes indexes for:

- Tickets by creator
- Tickets by assignee
- Tickets by status and priority
- Audit history by ticket and timestamp

PostgreSQL query plans were inspected with `EXPLAIN`. Index use depends on table size, statistics, and query selectivity; a sequential scan can be the correct plan for a small table.

## Learning Outcomes

This project practices:

- Primary keys, identity columns, and unique constraints
- `NOT NULL`, `CHECK`, and foreign-key constraints
- `ON DELETE RESTRICT` and `ON DELETE SET NULL`
- `INNER JOIN` and `LEFT JOIN`
- Counting tickets while preserving users with zero tickets
- Calculating average resolution duration
- Atomic ticket creation and audit logging with transactions
- Audit-history integrity checks
- Index design and query-plan inspection
- Negative testing of invalid data

## Script Order

The intended order for a **fresh, empty `sql_mastery` schema** is:

1. `01_create_schema.sql`
2. `02_seed_data.sql`
3. `03_validation_queries.sql`

The schema script is not a migration tool. `CREATE TABLE IF NOT EXISTS` does not repair existing objects, and the audit-trigger section recreates its named trigger. Review the target database before running setup scripts.

The seed script expects a clean schema and is not designed to be run repeatedly. Do not run it against the populated learning schema used during development.

## Validation Summary

During development, the existing schema was checked for:

- Expected columns and identity-generation settings
- Foreign-key relationships and deletion rules
- Check constraints and uniqueness rules
- Supporting indexes
- Rejection of duplicate usernames and emails
- Rejection of invalid ticket statuses and priorities
- Rejection of missing or nonexistent creators
- Rejection of invalid audit event types
- Rejection of resolution timestamps earlier than creation
- Append-only trigger behavior
- Transaction rollback behavior
- Ticket counts, audit integrity, and query plans

The existing learning database was verified to contain 3 users, 4 tickets, and 4 audit records after negative testing.

## Environment

- Database engine: PostgreSQL
- Database: `sql_practice`
- Project schema: `sql_mastery`
- Query tool: `psql`
- Editor: Visual Studio Code

## Future Improvements

- Make seed data safely repeatable or provide a dedicated reset procedure for a disposable test database.
- Add automated assertions for expected query results.
- Use a separate restricted application role for production-grade permissions.
- Capture actual query execution statistics when useful, using `EXPLAIN (ANALYZE, BUFFERS)` only for queries that are safe to execute.
