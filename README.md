# Dhan Disha

A free, private money planner for Indian households, built with Streamlit for the AI Conclave.

**What it does**
- Financial health score, goal planner, child education and retirement planners
- Investment ideas: a suggested equity, debt and gold mix (types of investments, never specific products)
- Tax Saver: old vs new regime for FY 2026-27, with rebate, marginal relief, surcharge and cess
- EMI Manager: pay-off plans for several loans, plus a new-loan check
- Calculators: GST, gratuity and capital gains
- Mutual fund lookup, money news from India, and an AI advisor

**Privacy.** The app stores nothing you type. Please keep PAN, Aadhaar and bank details out of the AI box.

**Educational use only. This is not SEBI-registered investment advice.** Tax slabs are set in the code for one financial year and must be updated every year.

**Run it on your computer**
```
pip install -r requirements.txt
streamlit run app.py
```
For the AI Advisor, add a key in `.streamlit/secrets.toml` (never commit that file):
```
NVIDIA_API_KEY = "your-key"
```
