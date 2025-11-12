# Solar Challenge Week 0

# ☀️ Solar Challenge Week 0 – Interactive Solar Dashboard

1. overview
   An **interactive Streamlit dashboard** for visualizing and analyzing solar energy metrics (GHI and temperature) across multiple countries and regions. The dashboard allows dynamic filtering by country and region, interactive charts, and comparative analysis across countries.

## 🎯 Objective

- Build a responsive Streamlit app to visualize solar energy insights.
- Integrate Python scripts to load and process data dynamically.
- Implement interactive features: dropdowns, multiselects, sliders, and checkboxes.
- Provide visually appealing charts: line charts, area charts, bubble charts, and small multiples.
- Deploy the dashboard to **Streamlit Community Cloud** for public access.

## structure

this structure I use to do the Dashboard
solar-challenge-week0/
│
├── app/
│ ├── **init**.py
│ ├── main.py  
│ └── utils.py  
│
├── scripts/
│ ├── **init**.py
│ └── README.md  
│
├── data/  
│ ├── benin_clean.csv
│ ├── sierraleone_clean.csv
│ └── togo_clean.csv
│
└── requirements.txt

## 📦 Environment Setup

1.  Create & activate a virtual environment (Windows with bash.exe):

    python -m venv venv
    source venv/Scripts/activate

2.  install dependencies

        pip install -r requirements.txt

3.  run the app
    ` streamlit run app/main.py`
