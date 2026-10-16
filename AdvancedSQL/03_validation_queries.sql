
-- ============================================================
-- Advanced SQL / SQL Mastery Project
-- File: 03_validation_queries.sql
-- Purpose: Reporting, integrity checks, and query-plan review.
--
-- Run against the sql_practice database.
-- These queries are intended to be read-only.
-- ============================================================

-- ============================================================
-- 1. Ticket details with creator and assignee
-- ============================================================

SELECT
    t.id AS ticket_id,
    t.title,
    t.status,
    t.priority,
    creator.username AS created_by,
    assignee.username AS assigned_to,
    t.created_at,
    t.resolved_at
FROM sql_mastery.tickets AS t
JOIN sql_mastery.users AS creator
    ON creator.id = t.created_by_user_id
LEFT JOIN sql_mastery.users AS assignee
    ON assignee.id = t.assigned_to_user_id
ORDER BY t.id;


-- ============================================================
-- 2. Ticket counts per user, including users with zero tickets
-- ============================================================

SELECT
    u.id AS user_id,
    u.username,
    COUNT(t.id) AS tickets_created
FROM sql_mastery.users AS u
LEFT JOIN sql_mastery.tickets AS t
    ON t.created_by_user_id = u.id
GROUP BY u.id, u.username
ORDER BY u.id;


-- ============================================================
-- 3. Average resolution duration
-- Only resolved tickets with a resolution timestamp qualify.
-- ============================================================

SELECT
    COUNT(*) AS resolved_ticket_count,
    AVG(resolved_at - created_at) AS average_resolution_duration
FROM sql_mastery.tickets
WHERE status = 'RESOLVED'
  AND resolved_at IS NOT NULL;


-- ============================================================
-- 4. Audit history for each ticket
-- ============================================================

SELECT
    a.id AS audit_id,
    a.ticket_id,
    a.actor_user_id,
    a.event_type,
    a.details,
    a.created_at
FROM sql_mastery.audit_records AS a
ORDER BY a.ticket_id, a.created_at, a.id;


-- ============================================================
-- 5. Check for audit records without a matching ticket
-- Expected result: zero rows.
-- ============================================================

SELECT a.*
FROM sql_mastery.audit_records AS a
LEFT JOIN sql_mastery.tickets AS t
    ON t.id = a.ticket_id
WHERE t.id IS NULL;


-- ============================================================
-- 6. Record counts
-- ============================================================

SELECT 'users' AS table_name, COUNT(*) AS row_count
FROM sql_mastery.users

UNION ALL

SELECT 'tickets', COUNT(*)
FROM sql_mastery.tickets

UNION ALL

SELECT 'audit_records', COUNT(*)
FROM sql_mastery.audit_records;


-- ============================================================
-- 7. Query plan: tickets by creator
-- ============================================================

EXPLAIN
SELECT id, title, status, priority
FROM sql_mastery.tickets
WHERE created_by_user_id = (
    SELECT id
    FROM sql_mastery.users
    WHERE username = 'chris'
);


-- ============================================================
-- 8. Query plan: tickets by status and priority
-- ============================================================

EXPLAIN
SELECT id, title, created_by_user_id
FROM sql_mastery.tickets
WHERE status = 'OPEN'
  AND priority = 'HIGH';


-- ============================================================
-- 9. Query plan: audit history for one ticket
-- ============================================================

EXPLAIN
SELECT id, event_type, details, created_at
FROM sql_mastery.audit_records
WHERE ticket_id = (
    SELECT id
    FROM sql_mastery.tickets
    WHERE title = 'VPN connection failure'
)
ORDER BY created_at;
