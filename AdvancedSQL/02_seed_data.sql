
-- ============================================================
-- 02_seed_data.sql
-- Purpose: Seed a fresh, empty sql_mastery schema.
--
-- IMPORTANT:
-- Run only when sql_mastery.users, tickets, and audit_records
-- are empty. This is not a repeatable seed script.
-- Never run against the existing populated learning database.
-- ============================================================

BEGIN;
-- Refuse to seed if any target table already contains data.
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM sql_mastery.users)
       OR EXISTS (SELECT 1 FROM sql_mastery.tickets)
       OR EXISTS (SELECT 1 FROM sql_mastery.audit_records)
    THEN
        RAISE EXCEPTION
            'Seed aborted: sql_mastery tables must be empty.';
    END IF;
END;
$$;

-- 1. Create the sample users.
INSERT INTO sql_mastery.users (username, email)
VALUES
    ('chris', 'chris@example.com'),
    ('alex', 'alex@example.com'),
    ('jordan', 'jordan@example.com');

-- 2. Create sample tickets and capture their actual IDs.
CREATE TEMP TABLE seed_ticket_ids (
    ticket_id BIGINT PRIMARY KEY,
    creator_user_id BIGINT NOT NULL,
    ticket_title VARCHAR(200) NOT NULL,
    ticket_priority VARCHAR(20) NOT NULL
) ON COMMIT DROP;

WITH inserted_tickets AS (
    INSERT INTO sql_mastery.tickets (
        title,
        description,
        status,
        priority,
        created_by_user_id,
        assigned_to_user_id
    )
    VALUES
        (
            'VPN connection failure',
            'User cannot connect to the company VPN.',
            'OPEN',
            'HIGH',
            (SELECT id FROM sql_mastery.users
             WHERE username = 'chris'),
            (SELECT id FROM sql_mastery.users
             WHERE username = 'alex')
        ),
        (
            'Email service outage',
            'Users report that email is unavailable.',
            'OPEN',
            'CRITICAL',
            (SELECT id FROM sql_mastery.users
             WHERE username = 'alex'),
            NULL
        ),
        (
            'Printer setup',
            'A new printer needs to be configured.',
            'IN_PROGRESS',
            'LOW',
            (SELECT id FROM sql_mastery.users
             WHERE username = 'jordan'),
            (SELECT id FROM sql_mastery.users
             WHERE username = 'chris')
        ),
        (
            'Successful transaction test',
            'Sample ticket for transaction and audit demonstrations.',
            'OPEN',
            'MEDIUM',
            (SELECT id FROM sql_mastery.users
             WHERE username = 'chris'),
            NULL
        )
    RETURNING id, title, priority, created_by_user_id
)
INSERT INTO seed_ticket_ids (
    ticket_id,
    creator_user_id,
    ticket_title,
    ticket_priority
)
SELECT
    id,
    created_by_user_id,
    title,
    priority
FROM inserted_tickets;

-- 3. Create audit records for only the tickets inserted above.
INSERT INTO sql_mastery.audit_records (
    ticket_id,
    actor_user_id,
    event_type,
    details
)
SELECT
    ticket_id,
    creator_user_id,
    'TICKET_CREATED',
    jsonb_build_object(
        'title', ticket_title,
        'priority', ticket_priority
    )
FROM seed_ticket_ids;

COMMIT;
