 🌿 HealthGuard – Sanjeevani AI 🌿  
_Your Intelligent Companion for Disease Prediction & Holistic Healing_

![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-blue.svg)
![Python](https://img.shields.io/badge/Language-Python-yellow)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)


---

 📜 About the Project

**HealthGuard – Sanjeevani** is an innovative AI-powered platform that predicts lifestyle diseases (Diabetes, Heart Disease, Parkinson’s) using ML models and offers holistic Indian wellness guidance via an intelligent companion rooted in **Ayurveda, Yoga, Naturopathy, and local diets**.

This solution bridges the gap between **modern diagnosis** and **traditional healing**, making healthcare **personal, proactive, and culturally rooted**.

---

 🎯 Key Objectives

- Early detection of chronic illnesses using Machine Learning
- Encourage preventive care via Indian traditional health sciences
- Provide local doctor recommendations using geolocation
- Offer guided yoga, pranayama, and diet plans per user profile


 🧠 Features

| Feature                        | Description                                           |
|-------------------------------|-------------------------------------------------------|
| 🧪 Disease Prediction          | AI models for Diabetes, Heart, Parkinson’s            |
| 🧘 Sanjeevani Companion        | Yoga, Diet, Ayurveda, Pranayama modules               |
| 🌍 Doctor Finder               | Nearest doctor suggestions based on GPS              |
| 📱 Streamlit UI                | Clean, responsive, and mobile-friendly interface      |
| 🇮🇳 Indian Wellness Mapping     | Local recipes, seasonal health routines               |

---

 🔩 System Architecture

[User Input] → [Preprocessing] → [Trained ML Models] → [Prediction Output]
         ↘                                    ↙
     [User Profile]                [Sanjeevani Holistic Guide]
         ↘                                    ↙
        [Nearby Doctors via Geopy & Custom Filters]

⚙️ Technologies Used
Frontend: Streamlit + CSS customization

Backend: Python, Pickle, Machine Learning

Models: Random Forest, Decision Tree, SVM

Geolocation: Geopy

Libraries: Numpy, Pandas, Scikit-learn, streamlit_option_menu

🔍 ML Algorithms
Disease	Algorithm(s) Used	Accuracy
Diabetes	Random Forest, SVM	91%
Heart Disease	Decision Tree, Random Forest	90.4%
Parkinson’s	SVM, Logistic Regression	92%

🧘 Sanjeevani Modules
Yoga & Pranayama: Age-specific asanas, stress-relief techniques

Naturopathy: Mud packs, sun therapy, detox tips

Ayurveda: Personalized herbs, seasonal remedies

Diet Plans: Balanced Indian meals & local recipes

📍 Doctor Recommender
Uses user location + doctor database with:

Location (lat/long)

Distance calculation via Geopy

Filters for rating, specialty, and city

📊 Observations & Impact
Cultural alignment improves user trust

Multi-modal health empowers users to act

Geolocation makes it action-oriented, not just theoretical

🧑‍💻 Developed & Presented By

Er. Varad Vijay Bakshi 

Er. Atharva Arun Kadam 

Er. Aryan Mahesh Lad 

Er. Prathmesh Prashant Vhatkar 

HealthGuard/
│
├── app.py                    # Main Streamlit app
├── saved_models/             # Pickled ML models
├── doctor_data/              # Geolocation + doctor details
├── resources/                # Yoga, Ayurveda JSON/text files
├── images/                   # Assets for frontend
├── README.md                 # You are here

🧭 Getting Started
pip install streamlit scikit-learn geopy pandas numpy
streamlit run app.py
Make sure your model .sav files are inside saved_models/

💬 Feedback or Suggestions?
Feel free to open an Issue or connect via:

📧 Email: varadbakshi@gmail.com
🔗 LinkedIn: linkedin.com/in/varadbakshi

🌱 "Bridging AI with Ayurveda – a smarter, healthier tomorrow."
🛑 This project is proprietary and not open-sourced. All rights reserved to Varad Bakshi (VBHARAT AI).

