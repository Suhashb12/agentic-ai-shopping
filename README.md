# 🛒 Agentic AI Shopping Assistant

A production-style **Agentic AI Shopping Assistant** built using Python and Flask, designed to demonstrate **agentic AI behavior**, multi-step reasoning, and real-world e-commerce workflows.  
This project was developed with **hackathon evaluation criteria** and **production extensibility** in mind.

---

## 🚀 Key Highlights

- 🤖 **Agent-based AI Architecture**
- 🧠 Multi-turn conversational reasoning
- 🛍️ Product discovery across **Mobiles, Fashion, Cosmetics**
- 💳 Order placement with **COD & Online Payment simulation**
- 📦 Order tracking lifecycle
- 🔁 Return & replacement workflows
- 💰 Refund lifecycle with **Admin approval**
- 🧾 SQLite-backed persistent storage
- 💬 ChatGPT-style chat interface
- 🧪 Hackathon-ready & production-oriented design

---

## 🧠 Agentic Architecture

The assistant is designed as an **agentic system**, not a static chatbot.

User Query
↓
Intent Classification
↓
Agent Selection
├── Shopping Agent
├── Order Tracking Agent
├── Complaint / Return Agent
└── Admin Approval Agent
↓
Database / Tool Execution
↓
Natural Language Response

Each agent operates independently and manages its own logic and state.

---

## 🧩 Supported Use Cases

### 🛒 Product Discovery
- Budget-based search (e.g., phones under ₹20,000)
- Category-based browsing
- Gender-specific fashion filtering
- Stock-aware responses

### 🧾 Order Placement
- Guided, multi-step checkout
- COD & Online payment simulation
- Unique order ID generation

### 📦 Order Tracking
- Track orders using order ID
- Real-time order status from database

### 🔁 Returns & Replacements
- Initiate return or replacement via chat
- Automatic order status updates

### 💰 Refund Lifecycle
CONFIRMED → RETURN_REQUESTED → REFUND_INITIATED → REFUNDED

Admin approval simulation


### 🛡️ Admin Operations
- Admin login
- View refund requests
- Approve refunds

---

## 🏗️ Project Structure

agent-ai/
├── app.py # Flask application entry point
├── shopping.db # SQLite database
│
├── agents/
│ ├── shopping_agent.py
│ ├── order_tracking_agent.py
│ └── complaint_agent.py
│
├── llm/
│ └── intent_classifier.py
│
├── auth/ # Optional auth extension
│ ├── init.py
│ ├── auth_routes.py
│ ├── security.py
│ └── email_utils.py
│
├── db/
│ ├── init_db.py
│ ├── generate_mobiles.py
│ ├── generate_fashion.py
│ └── generate_cosmetics.py
│
├── templates/
│ ├── chat.html
│ ├── payment.html
│ ├── payment_success.html
│ ├── admin_login.html
│ └── admin_dashboard.html
│
└── static/
├── chat.js
└── style.css


---

## 🗄️ Database & Data

- **SQLite** used for portability and simplicity
- Tables include:
  - `mobiles`
  - `fashion`
  - `cosmetics`
  - `orders`
  - `complaints`
- **300+ synthetic products** generated per category

---

## 🛠️ Technology Stack

| Layer | Technology |
|-----|-----------|
| Backend | Python, Flask |
| AI Logic | Intent-based agent routing |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |
| Architecture | Agent-based |
| Deployment | Local / VM / Cloud-ready |

---

## ▶️ How to Run the Project

### 1️⃣ Clone Repository
```bash
git clone <your-repo-url>
cd agent-ai
```
```bash
2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Linux / Mac
```

```bash
3️⃣ Install Dependencies
pip install flask
```
```bash
4️⃣ Initialize Database
python db/init_db.py
python db/generate_mobiles.py
python db/generate_fashion.py
python db/generate_cosmetics.py
```

```bash
5️⃣ Start the Application
python app.py
```

Open in browser:
```bash
http://127.0.0.1:5000
```

🔐 Admin Access
```bash
URL: /admin/login
Username: admin
Password: admin@4sy6
```bash

🧪 Sample Chat Prompts
Which phone under 20000?
Rainy clothes for men
Buy this Casual Polo T-Shirt
Track order ORD-XXXXXX
Raise complaint ORD-XXXXXX
Return order ORD-XXXXXX