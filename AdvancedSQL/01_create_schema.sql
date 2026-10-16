
-- ============================================================
-- Advanced SQL / SQL Mastery Project
-- File: 01_create_schema.sql
-- Purpose: Create the SQL Mastery schema, tables, constraints,
--          indexes, and append-only audit protection.
-- Database: sql_practice
--
-- IMPORTANT:
-- This is a fresh-schema setup script, not a migration script.
-- Review the target database before running it.
-- CREATE TABLE IF NOT EXISTS does not repair existing tables.
-- Do not run this script against an existing populated schema
-- as a substitute for a reviewed migration.
-- ============================================================

CREATE SCHEMA IF NOT EXISTS sql_mastery;

-- ============================================================
-- 1. Users
-- ============================================================

CREATE TABLE IF NOT EXISTS sql_mastery.users (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_sql_mastery_users_username UNIQUE (username),
    CONSTRAINT uq_sql_mastery_users_email UNIQUE (email)
);

-- ============================================================
-- 2. Tickets
-- ============================================================

CREATE TABLE IF NOT EXISTS sql_mastery.tickets (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'OPEN',
    priority VARCHAR(20) NOT NULL DEFAULT 'MEDIUM',
    created_by_user_id BIGINT NOT NULL,
    assigned_to_user_id BIGINT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMPTZ,

    CONSTRAINT ck_sql_mastery_tickets_status
        CHECK (status IN ('OPEN', 'IN_PROGRESS', 'RESOLVED', 'CLOSED')),

    CONSTRAINT ck_sql_mastery_tickets_priority
        CHECK (priority IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),

    CONSTRAINT ck_sql_mastery_tickets_resolution_time
        CHECK (resolved_at IS NULL OR resolved_at >= created_at),

    CONSTRAINT fk_sql_mastery_tickets_creator
        FOREIGN KEY (created_by_user_id)
        REFERENCES sql_mastery.users(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_sql_mastery_tickets_assignee
        FOREIGN KEY (assigned_to_user_id)
        REFERENCES sql_mastery.users(id)
        ON DELETE SET NULL
);

-- ============================================================
-- 3. Audit Records
-- ============================================================

CREATE TABLE IF NOT EXISTS sql_mastery.audit_records (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    ticket_id BIGINT NOT NULL,
    actor_user_id BIGINT,
    event_type VARCHAR(50) NOT NULL,
    details JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_sql_mastery_audit_ticket
        FOREIGN KEY (ticket_id)
        REFERENCES sql_mastery.tickets(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_sql_mastery_audit_actor
        FOREIGN KEY (actor_user_id)
        REFERENCES sql_mastery.users(id)
        ON DELETE SET NULL,

    CONSTRAINT ck_sql_mastery_audit_event_type
        CHECK (
            event_type IN (
                'TICKET_CREATED',
                'TICKET_ASSIGNED',
                'STATUS_CHANGED',
                'PRIORITY_CHANGED',
                'TICKET_RESOLVED',
                'TICKET_CLOSED',
                'COMMENT_ADDED'
            )
        )
);

-- ============================================================
-- 4. Indexes
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_sql_mastery_tickets_creator
    ON sql_mastery.tickets (created_by_user_id);

CREATE INDEX IF NOT EXISTS idx_sql_mastery_tickets_assignee
    ON sql_mastery.tickets (assigned_to_user_id);

CREATE INDEX IF NOT EXISTS idx_sql_mastery_tickets_status_priority
    ON sql_mastery.tickets (status, priority);

CREATE INDEX IF NOT EXISTS idx_sql_mastery_audit_ticket_created
    ON sql_mastery.audit_records (ticket_id, created_at);

-- ============================================================
-- 5. Append-only audit protection
-- ============================================================

CREATE OR REPLACE FUNCTION sql_mastery.prevent_audit_mutation()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    RAISE EXCEPTION
        'Audit records are append-only: UPDATE and DELETE are not allowed.';
END;
$$;

-- Drop only this project's named trigger if it already exists.
DROP TRIGGER IF EXISTS trg_sql_mastery_audit_append_only
    ON sql_mastery.audit_records;

CREATE TRIGGER trg_sql_mastery_audit_append_only
BEFORE UPDATE OR DELETE
ON sql_mastery.audit_records
FOR EACH ROW
EXECUTE FUNCTION sql_mastery.prevent_audit_mutation();
