# 🛒 AI Shopping Assistant — Agentic AI (Hackathon Build)

An **Agentic AI–powered Shopping Assistant** built using **Python, Flask, LangChain, Groq LLM, and SQLite**, designed to simulate a real-world e-commerce assistant with memory, authentication, and grounded product recommendations.

This project demonstrates **agentic reasoning**, **LLM orchestration**, **user memory**, and **safe AI behavior** — similar to ChatGPT, but tailored for shopping use-cases.

---

## 🚀 Key Capabilities

### 🤖 AI Capabilities
- Fully LLM-based intent understanding
- Agentic reasoning (not rule-based)
- Calm, professional, step-by-step responses
- Safe handling of sensitive topics (no OTP/payment misuse)
- Category understanding (mobile, cosmetics, fashion)
- Budget & feature-aware recommendations

### 🧠 Agent Memory
- User chat history (per logged-in user)
- Preference memory (e.g., last category searched)
- Guest users get temporary memory (lost on refresh)

### 🛍️ Shopping Use-Cases Supported
- Product discovery
- Budget-based recommendations
- Feature-based filtering
- Category switching
- Expert-style product explanation

---

## 🏗️ Tech Stack

| Layer | Technology |
|-----|-----------|
Backend | Python + Flask |
LLM | Groq (via LangChain) |
Agent Framework | LangChain (`langchain_core`) |
Database | SQLite |
Frontend | HTML + CSS + Vanilla JS |
Auth | Flask Session + SQLite |
Deployment | Local VM / Hackathon demo |

---

## 📁 Project Structure


---

## 🔐 Authentication & User Management

### ✅ Implemented
- User signup
- Login & logout
- Password hashing
- Session-based authentication
- Per-user chat persistence

### 📧 Email Verification (Hackathon Mode)
- Verification links are **printed to terminal**
- No real SMTP used (intentional for demo safety)

Example:

### 🔁 Forgot Password (OTP)
- OTP generated and stored securely
- OTP printed to terminal (demo mode)
- Password reset via OTP validation

> ℹ️ Real email delivery can be added later using SMTP.

---

## 🧾 Database Design

### users.db
Tables:
- users
- chats
- password_otps
- user_preferences

### products.db
Generic product schema:
- Supports multiple categories
- Flexible attributes via JSON
- Used for grounding AI responses

---

## 🧠 Agent Architecture


---

## 🖥️ Frontend Experience

- ChatGPT-style UI
- 80% width centered chat
- Async chat (no reload)
- “Thinking…” indicator
- Signup modal popup after 2 seconds (guest only)
- Guest mode vs logged-in mode
- Chat history auto-restores on login

---

## ⚙️ Setup Instructions

### 1️⃣ Create virtual environment
```bash
python -m venv aiagent
source aiagent/bin/activate


2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Set Groq API Key
export GROQ_API_KEY="your_groq_api_key"


(Windows PowerShell)

setx GROQ_API_KEY "your_groq_api_key"

4️⃣ Initialize databases
python db/init_auth_chat_db.py
python db/generate_cosmetics_fashion.py

5️⃣ Run the application
python app.py


Open in browser:

http://<VM-IP>:5000

🧪 Example Prompts

Which phone under 20000 has a 50MP camera?

Suggest good cosmetics under 1000

Recommend fashion clothes for casual wear

Compare two budget mobiles


## 📄 License

MIT License

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a pull request.