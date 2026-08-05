-- ============================================================================
-- SRI LANKA AIR FORCE TRADE TRAINING SCHOOL (TTS) MANAGEMENT PORTAL
-- USER MANAGEMENT MODULE - STORED PROCEDURES & TRIGGERS
-- Database: MySQL 8.0+ / MariaDB
-- ============================================================================

USE slaf_tts_db;

DELIMITER $$

-- ----------------------------------------------------------------------------
-- 1. STORED PROCEDURE: SP_CreateUser
-- Creates a new system user with personnel details
-- ----------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS SP_CreateUser$$
CREATE PROCEDURE SP_CreateUser(
    IN p_id VARCHAR(36),
    IN p_username VARCHAR(50),
    IN p_email VARCHAR(100),
    IN p_service_number VARCHAR(50),
    IN p_rank VARCHAR(50),
    IN p_full_name VARCHAR(100),
    IN p_mobile_number VARCHAR(20),
    IN p_department VARCHAR(100),
    IN p_designation VARCHAR(100),
    IN p_assigned_module VARCHAR(100),
    IN p_hashed_password VARCHAR(255),
    IN p_role_id VARCHAR(36),
    IN p_must_change_password TINYINT(1)
)
BEGIN
    INSERT INTO users (
        id, username, email, service_number, rank, full_name,
        mobile_number, department, designation, assigned_module,
        hashed_password, role_id, is_active, is_locked,
        must_change_password, failed_login_attempts, created_at, updated_at
    ) VALUES (
        p_id, p_username, p_email, p_service_number, p_rank, p_full_name,
        p_mobile_number, p_department, p_designation, p_assigned_module,
        p_hashed_password, p_role_id, 1, 0,
        p_must_change_password, 0, NOW(), NOW()
    );
END$$

-- ----------------------------------------------------------------------------
-- 2. STORED PROCEDURE: SP_UpdateUser
-- Updates existing user information
-- ----------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS SP_UpdateUser$$
CREATE PROCEDURE SP_UpdateUser(
    IN p_id VARCHAR(36),
    IN p_email VARCHAR(100),
    IN p_service_number VARCHAR(50),
    IN p_rank VARCHAR(50),
    IN p_full_name VARCHAR(100),
    IN p_mobile_number VARCHAR(20),
    IN p_department VARCHAR(100),
    IN p_designation VARCHAR(100),
    IN p_assigned_module VARCHAR(100),
    IN p_role_id VARCHAR(36),
    IN p_is_active TINYINT(1)
)
BEGIN
    UPDATE users 
    SET 
        email = p_email,
        service_number = p_service_number,
        rank = p_rank,
        full_name = p_full_name,
        mobile_number = p_mobile_number,
        department = p_department,
        designation = p_designation,
        assigned_module = p_assigned_module,
        role_id = p_role_id,
        is_active = p_is_active,
        updated_at = NOW()
    WHERE id = p_id AND deleted_at IS NULL;
END$$

-- ----------------------------------------------------------------------------
-- 3. STORED PROCEDURE: SP_DeleteUser (Soft Delete)
-- Soft deletes user account preserving referential integrity
-- ----------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS SP_DeleteUser$$
CREATE PROCEDURE SP_DeleteUser(
    IN p_id VARCHAR(36)
)
BEGIN
    -- Prevent soft-deleting protected Super Administrator account
    IF (SELECT username FROM users WHERE id = p_id) = 'admin' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Protected System Administrator account cannot be deleted.';
    ELSE
        UPDATE users 
        SET is_active = 0, deleted_at = NOW(), updated_at = NOW()
        WHERE id = p_id;
    END IF;
END$$

-- ----------------------------------------------------------------------------
-- 4. STORED PROCEDURE: SP_AssignRole
-- Assigns a role to a user
-- ----------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS SP_AssignRole$$
CREATE PROCEDURE SP_AssignRole(
    IN p_user_id VARCHAR(36),
    IN p_role_id VARCHAR(36)
)
BEGIN
    UPDATE users 
    SET role_id = p_role_id, updated_at = NOW()
    WHERE id = p_user_id AND deleted_at IS NULL;
END$$

-- ----------------------------------------------------------------------------
-- 5. STORED PROCEDURE: SP_ResetPassword
-- Resets user password and updates password timestamp
-- ----------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS SP_ResetPassword$$
CREATE PROCEDURE SP_ResetPassword(
    IN p_user_id VARCHAR(36),
    IN p_hashed_password VARCHAR(255),
    IN p_must_change TINYINT(1)
)
BEGIN
    UPDATE users 
    SET 
        hashed_password = p_hashed_password,
        must_change_password = p_must_change,
        failed_login_attempts = 0,
        is_locked = 0,
        password_changed_at = NOW(),
        updated_at = NOW()
    WHERE id = p_user_id;

    -- Record entry in password history table
    INSERT INTO password_history (id, user_id, hashed_password, created_at)
    VALUES (UUID(), p_user_id, p_hashed_password, NOW());
END$$

-- ----------------------------------------------------------------------------
-- 6. STORED PROCEDURE: SP_LockAccount & SP_UnlockAccount
-- Handles locking and unlocking of accounts
-- ----------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS SP_LockAccount$$
CREATE PROCEDURE SP_LockAccount(
    IN p_user_id VARCHAR(36)
)
BEGIN
    UPDATE users 
    SET is_locked = 1, updated_at = NOW()
    WHERE id = p_user_id;
END$$

DROP PROCEDURE IF EXISTS SP_UnlockAccount$$
CREATE PROCEDURE SP_UnlockAccount(
    IN p_user_id VARCHAR(36)
)
BEGIN
    UPDATE users 
    SET is_locked = 0, failed_login_attempts = 0, updated_at = NOW()
    WHERE id = p_user_id;
END$$

-- ----------------------------------------------------------------------------
-- 7. STORED PROCEDURE: SP_RecordLogin & SP_RecordLogout
-- Records login activity history
-- ----------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS SP_RecordLogin$$
CREATE PROCEDURE SP_RecordLogin(
    IN p_id VARCHAR(36),
    IN p_user_id VARCHAR(36),
    IN p_username VARCHAR(50),
    IN p_status VARCHAR(20),
    IN p_ip VARCHAR(45),
    IN p_agent VARCHAR(255)
)
BEGIN
    INSERT INTO login_history (id, user_id, username, status, ip_address, user_agent, created_at)
    VALUES (p_id, p_user_id, p_username, p_status, p_ip, p_agent, NOW());
END$$

DROP PROCEDURE IF EXISTS SP_RecordLogout$$
CREATE PROCEDURE SP_RecordLogout(
    IN p_user_id VARCHAR(36)
)
BEGIN
    UPDATE login_history 
    SET logout_time = NOW()
    WHERE user_id = p_user_id AND logout_time IS NULL
    ORDER BY created_at DESC 
    LIMIT 1;
END$$

-- ============================================================================
-- DATABASE TRIGGERS
-- ============================================================================

-- ----------------------------------------------------------------------------
-- TRIGGER 1: TR_Password_History_Insert
-- Automatically creates password history record whenever a user password changes
-- ----------------------------------------------------------------------------
DROP TRIGGER IF EXISTS TR_Password_History_Insert$$
CREATE TRIGGER TR_Password_History_Insert
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    IF OLD.hashed_password <> NEW.hashed_password THEN
        INSERT INTO password_history (id, user_id, hashed_password, created_at)
        VALUES (UUID(), NEW.id, NEW.hashed_password, NOW());
    END IF;
END$$

-- ----------------------------------------------------------------------------
-- TRIGGER 2: TR_Users_Audit_Update
-- Logs audit trail for user updates
-- ----------------------------------------------------------------------------
DROP TRIGGER IF EXISTS TR_Users_Audit_Update$$
CREATE TRIGGER TR_Users_Audit_Update
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    IF OLD.role_id <> NEW.role_id THEN
        INSERT INTO audit_logs (id, user_id, username, module, action, previous_value, new_value, created_at, details)
        VALUES (
            UUID(), NEW.id, NEW.username, 'User Management', 'ROLE_CHANGED',
            OLD.role_id, NEW.role_id, NOW(), CONCAT('User role updated from ', OLD.role_id, ' to ', NEW.role_id)
        );
    END IF;
    
    IF OLD.is_locked = 0 AND NEW.is_locked = 1 THEN
        INSERT INTO audit_logs (id, user_id, username, module, action, previous_value, new_value, created_at, details)
        VALUES (
            UUID(), NEW.id, NEW.username, 'User Management', 'ACCOUNT_LOCKED',
            '0', '1', NOW(), 'Account automatically locked due to repeated security policy triggers'
        );
    END IF;
    
    IF OLD.is_locked = 1 AND NEW.is_locked = 0 THEN
        INSERT INTO audit_logs (id, user_id, username, module, action, previous_value, new_value, created_at, details)
        VALUES (
            UUID(), NEW.id, NEW.username, 'User Management', 'ACCOUNT_UNLOCKED',
            '1', '0', NOW(), 'Account unlocked by system administrator'
        );
    END IF;
END$$

-- ----------------------------------------------------------------------------
-- TRIGGER 3: TR_Prevent_Admin_Delete
-- Prevents hard deletion of protected system administrator account
-- ----------------------------------------------------------------------------
DROP TRIGGER IF EXISTS TR_Prevent_Admin_Delete$$
CREATE TRIGGER TR_Prevent_Admin_Delete
BEFORE DELETE ON users
FOR EACH ROW
BEGIN
    IF OLD.username = 'admin' OR OLD.id = 'user-slaf-admin' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'CRITICAL SECURITY ERROR: Protected System Administrator account cannot be deleted.';
    END IF;
END$$

DELIMITER ;
