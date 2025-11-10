# 📁 README: Project 1 - Real-Time Equity Risk & P&L Dashboard

This project demonstrates a full-stack, real-time quantitative application built using **FastAPI** (Python backend) and **Angular** (Frontend), showcasing expertise in **WebSockets, Pandas/NumPy for quantitative finance, and local database integration (SQLite)**.

## 🌟 Project Goals

* Build a **real-time risk dashboard** for equity positions.
* Implement **Mark-to-Market (MtM) P&L** calculation.
* Implement **Historical Value-at-Risk (VaR)** calculation using Pandas/NumPy.
* Utilize **WebSockets** for low-latency market data streaming.
* Establish **REST APIs** for initial data fetching.

## ⚙️ Technology Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Backend** | Python 3.11, FastAPI | REST API, WebSocket server, Business Logic, Quant Calculation |
| **Quant Engine** | Pandas, NumPy | P&L and Historical VaR calculation |
| **Database** | SQLite, SQLAlchemy | Local, file-based persistence for position data |
| **Frontend** | Angular, TypeScript, RxJS | Real-time data consumption, UI rendering, Change Detection |
| **Communication** | WebSockets (Streaming), HTTP (Initial Data) | Data flow |

---

## 🚀 Setup and Run Instructions

### 1. Backend Setup (`quant_dashboard/`)

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the Server:**
    The application uses **SQLite** and will automatically create the `quant_dashboard.db` file and seed initial positions (`AAPL`, `GOOG`) on first run.
    ```bash
    uvicorn app.main:app --reload
    ```
    *The FastAPI server starts on **`http://localhost:8000`** and the background simulator task starts streaming price, P&L, and VaR updates every 0.5 seconds.*

### 2. Frontend Setup (`quant-frontend/`)

1.  **Navigate to the Frontend Directory:**
    ```bash
    cd quant-frontend/
    ```
2.  **Install Node Dependencies:**
    ```bash
    npm install
    ```
3.  **Run the Angular Development Server:**
    ```bash
    ng serve --open
    ```
    *The dashboard opens in your browser, typically at **`http://localhost:4200`**, displaying real-time data from the WebSocket stream.*

---

## 📝 Key Files and Logic

| File | Description | Skill Demonstrated |
| :--- | :--- | :--- |
| `app/main.py` | FastAPI setup, REST endpoints, **WebSocket Manager**, and the background **Market Data Simulator**. | Concurrency, WebSockets, API Design |
| `app/quant_engine.py` | Contains the `calculate_pnl_and_var` function, using NumPy to calculate **Historical 95% VaR**. | Quantitative Development (VaR) |
| `app/database.py` | SQLAlchemy setup for SQLite, demonstrating database connection resilience. | Database Integration |
| `app/app.component.ts` | Angular component that subscribes to the WebSocket stream and uses a `Map` to efficiently update the state. | Real-time UI, RxJS, Change Detection |