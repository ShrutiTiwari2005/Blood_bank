# Hemo-Sync Database Schema (MySQL)

This document outlines the complete database schema for the Hemo-Sync platform. If you are migrating back from the SQLite mirror or starting fresh on a production MySQL database, please use these structural definitions to rebuild the database.

## Database Information
- **Database Name**: `blood_bank` (or whatever you configure in `.env`)
- **Default Port**: `3306`
- **Tables**: `users`, `patients`, `stock`, `requests`, `donors`

---

## 1. `users` Table
Handles Personnel Registration, Authentication, and Role-Based Access Control (RBAC).

| Column Name | Data Type | Attributes | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Unique identifier for the user. |
| `username` | `VARCHAR(255)` | `UNIQUE`, `NOT NULL` | The unique "Personnel ID" used for login. |
| `email` | `VARCHAR(255)` | `UNIQUE`, `NOT NULL` | The institutional contact email. |
| `password_hash` | `VARCHAR(255)` | `NOT NULL` | The Bcrypt hashed password. |
| `role` | `VARCHAR(50)` | `DEFAULT 'viewer'` | Access control ('admin', 'viewer', etc.). |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Account creation timeline. |
| `last_login` | `TIMESTAMP` | `NULL` | Last successful authentication. |

---

## 2. `patients` Table
The Institutional Patient Registry. Tracks priority levels and critical blood characteristics.

| Column Name | Data Type | Attributes | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Unique patient identifier. |
| `name` | `VARCHAR(255)` | `NOT NULL` | Full name of the patient. |
| `blood_group` | `VARCHAR(10)` | `NOT NULL` | The patient's blood phenotype (e.g., A+, O-). |
| `current_hb` | `FLOAT` | `NOT NULL` | The patient's hemoglobin concentration. |
| `city` | `VARCHAR(100)` | `NOT NULL` | Clinical Node / Regional City. |
| `priority_level` | `VARCHAR(50)` | `DEFAULT 'stable'` | Computed priority ('critical', 'high', 'stable'). |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Time of registration in the Hub. |

---

## 3. `stock` Table
The Global Inventory Node. Tracks available phenotypes across the entire network.

| Column Name | Data Type | Attributes | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Unique stock record identifier. |
| `blood_group` | `VARCHAR(10)` | `UNIQUE`, `NOT NULL` | The blood phenotype (A+, O-, etc.). |
| `units_available` | `INT` | `DEFAULT 0` | Total cumulative units in the repository. |
| `last_updated` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Time of last inventory modification. |

> **Note on Upserts**: To safely increment this table in MySQL, the `stock_repo.py` handles conflicts based on the `blood_group` UNIQUE constraint.

---

## 4. `requests` Table
The Blood Requisition Node. Tracks pending and fulfilled medical orders.

| Column Name | Data Type | Attributes | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Unique requisition identifier. |
| `blood_group` | `VARCHAR(10)` | `NOT NULL` | Phenotype required for the procedure. |
| `units_required` | `INT` | `NOT NULL` | Number of units requested. |
| `city` | `VARCHAR(100)` | `NOT NULL` | Target medical facility / city. |
| `status` | `VARCHAR(50)` | `DEFAULT 'pending'` | Workflow status ('pending', 'fulfilled'). |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Request initialization timestamp. |

---

## 5. `donors` Table
The Institutional Donor Hub. Registers individuals for regional blood acquisition.

| Column Name | Data Type | Attributes | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Unique internal identifier. |
| `name` | `VARCHAR(255)` | `NOT NULL` | Donor's full legal name. |
| `blood_group` | `VARCHAR(10)` | `NOT NULL` | Donor's phenotype. |
| `contact` | `VARCHAR(100)` | `NOT NULL` | Phone number or secure comms link. |
| `city` | `VARCHAR(100)` | `NOT NULL` | Regional City. |
| `status` | `VARCHAR(50)` | `DEFAULT 'active'` | Eligibility state ('active', 'deferred'). |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Hub registration timeline. |

---

## Connection Reversal (SQLite -> MySQL)
If you are transitioning back to MySQL from the temporary SQLite Mirror:
1. Ensure your MySQL Server is running locally on Port `3306`.
2. Open `app/utils/db.py` and replace the SQLite `DatabaseManager` logic with the `mysql.connector.pooling` connection. (It was previously structured to use `Config.DB_USER`, `Config.DB_PASSWORD`, etc.)
3. Update `app/repositories/stock_repo.py` to revert `ON CONFLICT` to MySQL's `ON DUPLICATE KEY UPDATE`.
