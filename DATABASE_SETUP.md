# Hemo-Sync v5.2 - Database Architecture & Configuration Guide

This document outlines the database schema, table structures, and instructions for resolving the "Node Offline" (Error 10061) issue by configuring a production-ready MySQL instance for the Blood Bank Intelligence platform.

---

## 1. Database Configuration (Solving the Offline Error)

The "Sync: Node Offline" error occurs because the platform is attempting to connect to a MySQL database on `localhost:3306`, but the service is either not running or not installed.

### Step-by-Step MySQL Setup:
1. **Install MySQL Server**: Ensure MySQL Server is installed and running on your local machine.
2. **Create the Database**: Connect to your MySQL instance (using a client like MySQL Workbench or the CLI) and execute:
   ```sql
   CREATE DATABASE blood_bank;
   ```
3. **Configure Environment Variables**: Ensure your `.env` file in the root directory matches your MySQL credentials:
   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=Shruti@2005
   DB_NAME=blood_bank
   ```
4. **Restart the Application**: Once the MySQL service is verified and the `.env` is configured, restart the application. The system will automatically construct the required tables if they are missing.

*(Note: The system currently includes a SQLite Seamless Mirror in `app/utils/db.py` to allow the institutional hub to function even when MySQL is offline. When you are ready for production, revert `db.py` back to the MySQL connector logic.)*

---

## 2. Institutional Schema Definitions

The platform utilizes 5 relational data nodes. Below are the classes, their attributes, and primary keys.

### A. Personnel Node (`users`)
Authenticates institutional medical staff.
*   `id` (INTEGER, **Primary Key**, Auto-Increment)
*   `username` (TEXT, **Unique**, Not Null) - The Hub ID.
*   `email` (TEXT, **Unique**, Not Null) - Medical contact string.
*   `password_hash` (TEXT, Not Null) - Bcrypt hashed secret.
*   `role` (TEXT, Default: 'viewer') - RBAC designation ('admin', 'viewer').
*   `last_login` (TIMESTAMP)

### B. Patient Registry (`patients`)
Tracks clinical patients and their prioritization metrics.
*   `id` (INTEGER, **Primary Key**, Auto-Increment)
*   `name` (TEXT, Not Null)
*   `blood_group` (TEXT, Not Null)
*   `current_hb` (REAL, Not Null) - Hemoglobin levels used for AI predictions.
*   `city` (TEXT, Not Null) - Institutional sector.
*   `priority_level` (TEXT) - ('critical', 'high', 'stable') calculated via logic.

### C. Inventory Stock (`stock`)
Manages regional blood unit availability.
*   `id` (INTEGER, **Primary Key**, Auto-Increment)
*   `blood_group` (TEXT, **Unique**, Not Null) - The phenotype identifier.
*   `units_available` (INTEGER, Default: 0) - Real-time stock count.
*   `last_updated` (TIMESTAMP, Default: CURRENT_TIMESTAMP)

### D. Blood Requisitions (`requests`)
Logs institutional requests for stock depletion.
*   `id` (INTEGER, **Primary Key**, Auto-Increment)
*   `blood_group` (TEXT, Not Null)
*   `units_required` (INTEGER, Not Null)
*   `city` (TEXT, Not Null)
*   `status` (TEXT, Default: 'pending') - ('pending', 'fulfilled').

### E. Donor Pool (`donors`)
Registers independent donors for the regional network.
*   `id` (INTEGER, **Primary Key**, Auto-Increment)
*   `name` (TEXT, Not Null)
*   `blood_group` (TEXT, Not Null)
*   `contact` (TEXT, Not Null)
*   `city` (TEXT, Not Null)
*   `status` (TEXT, Default: 'active')
