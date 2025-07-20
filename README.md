# 🚀 VIKSIT.AI

> U N D E R S T A N D I N G   T H O U S A N D S  O F  L I N E S  O F
C O D E  J U S T  G O T  E A S I E R

## 📌 Problem Statement


## 🎯 Objective

Developers spend up to 60% of their time reading and understanding complex, undocumented codebases, leading to slow onboarding, reduced productivity, and frustration, especially for new hires. Viksit.AI addresses this by automatically generating clear documentation, answering code-related queries, and making technical knowledge easily accessible by helping users visualize the project as well as providing a real time compilation support — empowering all developers, including those from socially backward communities, to contribute efficiently and confidently.

This project empowers developers, students, and individuals worldwide by providing equitable access to AI, breaking barriers of privilege and opportunity.

---
## 🧪 How to Run the Project

### Requirements:
- Python (Django & Streamlit)
- API's 
    => Groq
    => Sarvam
    => JDoodle
    => Google Custom Search API 

- .env file setup 
    
    => GROQ_API_KEY=""
    => GOOGLE_API_KEY=""
    => GOOGLE_CSE_ID=""
    => SARVAM_API_KEY=""
    => DJANGO_SECRET_KEY=""
    => GITHUB_TOKEN=""

### Local Setup:
```bash
# Clone the repo
git clone https://github.com/Sudharsan278/Viksit

# Install dependencies

mkdir github_browser
cd github_browser
mkdir backend frontend

pip install django djangorestframework django-cors-headers requests streamlit

cd backend
django-admin startproject backend .
python manage.py startapp github_app
mkdir -p github_app\management\commands


# Start development server

backend - python manage.py runserver [port]
frontend - streamlit run app.py

## 📎 Resources / Credits

- Groq, Sarvam, JDoodle, Google Custom Search & Oauth
- Langchain groq  

---