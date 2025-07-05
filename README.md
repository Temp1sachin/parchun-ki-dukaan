# 🛍️ Walmart Kirana Digital Twin

**Simulate district-wise SKU recommendations for Walmart's rural micro-franchise expansion using geo-demographics, festivals, and kirana collaboration logic.**

---

## 📁 Project Structure

walmart-kirana-digital-twin/
├── backend/ # FastAPI backend API
│ ├── main.py
│ └── recommend.py
├── frontend/ # Streamlit dashboard
│ └── app.py
├── data/ # Simulated CSV data
│ ├── districts.csv
│ ├── festivals.csv
│ └── kirana_skus.csv
├── requirements.txt # Dependencies
└── README.md

## ⚙️ Setup Instructions

### 1. 📦 Create virtual environment (optional)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

# Terminal 1: Backend
cd backend
uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend
streamlit run app.py

App runs at: http://localhost:8501

