# ESG & Thematic Investment Screener + Optimizer

A full-stack portfolio analytics platform for ESG-focused investment screening, comparison, optimization, and ML-powered return predictions.

**Built by [Nhat Nguyen](mailto:Nhatmn114@gmail.com)**

## Features

### 🔍 ESG Screener
- Browse 79 securities (stocks + ETFs) with comprehensive ESG data
- Filter by ESG score, carbon intensity, sector, region, themes
- Sort by any metric — real-time filtering

### ⚖️ Security Comparison
- Side-by-side comparison of 2-6 securities
- ESG radar charts (Environmental, Social, Governance)
- Carbon intensity & green revenue bar charts
- FinBERT-style sentiment analysis with controversy flags
- Theme overlap visualization

### 📊 Portfolio Optimizer
- Mean-variance optimization with ESG constraints (scipy.optimize)
- Objectives: Maximize Sharpe, Minimize Variance, Maximize ESG
- Constraints: min ESG score, max carbon, max single/sector weight
- Interactive efficient frontier visualization
- PDF report generation & download

### 🧠 ML Predictions
- Random Forest model (scikit-learn) trained on 9 ESG features
- 12-month return predictions with confidence intervals
- Global feature importance analysis
- Risk vs. return scatter plot
- Per-security feature driver breakdown

## Tech Stack

| Layer    | Technology |
|----------|-----------|
| Frontend | Next.js 16, TypeScript, Tailwind CSS, Recharts, Lucide |
| Backend  | FastAPI, Python 3.11+, Pandas, NumPy |
| ML       | scikit-learn (Random Forest), scipy (optimizer) |
| NLP      | Pre-computed FinBERT sentiment (with HuggingFace API fallback) |
| PDF      | fpdf2 |
| Deploy   | Vercel (frontend) + Railway (backend) |

## Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
python -m uvicorn app.main:app --reload --port 8080
```

### Frontend
```bash
cd frontend
npm install
echo "NEXT_PUBLIC_API_URL=http://localhost:8080" > .env.local
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/screener/securities` | List & filter securities |
| GET | `/api/screener/filters` | Available filter options |
| POST | `/api/screener/compare` | Compare 2-6 securities |
| POST | `/api/optimizer/optimize` | Run portfolio optimization |
| POST | `/api/optimizer/report` | Generate PDF report |
| GET | `/api/ml/predictions` | ML return predictions |
| GET | `/api/ml/feature-importance` | Feature importance |
| GET | `/api/ml/sentiment/{ticker}` | ESG sentiment analysis |

## ESG Data

The dataset includes 79 securities across 14 sectors with:
- ESG scores (Overall, Environmental, Social, Governance) — 0 to 100
- Carbon intensity (tCO2e per $M revenue)
- Green revenue percentage
- Thematic tags (35 themes including clean energy, AI, water, etc.)
- Controversy scores and summaries

*Data is illustrative and based on publicly available ESG rating ranges.*

## License

MIT
