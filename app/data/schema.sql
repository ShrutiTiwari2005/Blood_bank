-- BLOOD BANK INTELLIGENCE SaaS v4.0 - UNIFIED PRODUCTION SCHEMA
-- Author: Senior Product Architect
-- Target: MySQL 8.0+

CREATE DATABASE IF NOT EXISTS blood_bank;
USE blood_bank;

-- 1. Users Table (Auth & RBAC)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'staff', 'viewer') DEFAULT 'viewer',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    INDEX (username),
    INDEX (email)
) ENGINE=InnoDB;

-- 2. Donors Table (Medical Registry)
CREATE TABLE IF NOT EXISTS donors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    blood_group VARCHAR(5) NOT NULL,
    city VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    last_donation_date DATE NULL,
    reliability_score FLOAT DEFAULT 8.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX (blood_group),
    INDEX (city)
) ENGINE=InnoDB;

-- 3. Blood Stock Table (Real-time Inventory)
CREATE TABLE IF NOT EXISTS blood_stock (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(50) NOT NULL,
    blood_group VARCHAR(5) NOT NULL,
    units_available INT NOT NULL DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY (city, blood_group),
    INDEX (city)
) ENGINE=InnoDB;

-- 4. Blood Requests Table (Procurement Logs)
CREATE TABLE IF NOT EXISTS blood_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(50) NOT NULL,
    blood_group VARCHAR(5) NOT NULL,
    units_required INT NOT NULL,
    status ENUM('pending', 'approved', 'fulfilled', 'rejected') DEFAULT 'pending',
    user_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX (status),
    INDEX (city)
) ENGINE=InnoDB;

-- 5. Activity Logs Table (Medical Audit Trail)
CREATE TABLE IF NOT EXISTS activity_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(255) NOT NULL,
    resource VARCHAR(100),
    affected_id INT,
    metadata JSON,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX (user_id),
    INDEX (timestamp)
) ENGINE=InnoDB;

-- 6. Institutional Patients Table (Health Intelligence Node)
CREATE TABLE IF NOT EXISTS patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    blood_group VARCHAR(5) NOT NULL,
    current_hb FLOAT NOT NULL,
    condition_status VARCHAR(100), -- e.g., Thalassemia, Chronic Anemia
    priority_level ENUM('critical', 'high', 'normal') DEFAULT 'normal',
    city VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX (priority_level),
    INDEX (blood_group)
) ENGINE=InnoDB;

-- INNITIALIZE SEED DATA (Optional)
-- INSERT INTO users (username, email, password_hash, role) VALUES ('admin', 'admin@bloodbank.ai', 'REPLACE_WITH_BCRYPT_HASH', 'admin');
