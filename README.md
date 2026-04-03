# Blood Bank AI System - Production Backend

This repository contains a professional, production-grade backend for a Blood Bank Management System with integrated AI for shortage prediction and donor behavior analysis.

---

## 🏗️ System Architecture (Layered)

The system follows a strict **Layered Architecture** (Layered Pattern) to ensure separation of concerns, maintainability, and scalability.

### 📁 Folder Structure & Responsibilities

| Folder | Layer | Responsibility |
| :--- | :--- | :--- |
| **`app/routes/`** | **API Layer** | Handles logic-less HTTP requests/responses. Calls the Service Layer. |
| **`app/services/`** | **Business Layer** | Core application logic, validations, and workflow orchestration. |
| **`app/repositories/`** | **Data Layer** | Pure SQL interface. Responsible for data persistence and retrieval. |
| **`app/ml/`** | **ML Layer** | Isolated model loading and inference logic for predictions. |
| **`app/utils/`** | **Infrastructure** | Centralized utilities like Database Connection Pooling and Shared Validators. |
| **`app/models/`** | **Domain Layer** | Data structures and schemas used across layers. |
| **`migrations/`** | **Schema** | SQL scripts for database schema versioning. |
| **`tests/`** | **QA** | Unit and Integration test suites. |

---

## 🔄 Request Lifecycle

1. **Client** → sends Request to a **Route** (`app/routes/`).
2. **Route** → extracts data and calls a **Service** (`app/services/`).
3. **Service** → performs validations, business logic, and MB inference.
4. **Service** → calls a **Repository** (`app/repositories/`) for DB operations.
5. **Repository** → uses **Connection Pool** (`app/utils/db.py`) to talk to **Database**.
6. **Response** → flows back up through the layers to the **Client**.

---

## 🛠️ Tech Stack

- **Backend:** Python (Flask)
- **Database:** MySQL (Relational)
- **ML:** Scikit-Learn, Joblib, Pandas
- **Infrastructure:** Dotenv (Config), MySQL-Connector (Pooling)

---

## 🚀 Getting Started

1.  **Clone the Repository**
2.  **Setup Virtual Environment**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure Environment**
    Update the `.env` file with your MySQL credentials.
5.  **Run Application**
    ```bash
    python run.py
    ```

---

## 🔐 Security & Reliability

- **Connection Pooling:** Ensures thread-safe concurrent database access.
- **Environment Isolation:** All secrets are kept in `.env` and loaded via `config.py`.
- **Factory Pattern:** The application is initialized using the `create_app()` factory for better testing and scalability.
