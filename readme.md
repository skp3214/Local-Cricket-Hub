
# LOCAL CRICKET HUB🏏 

## Project Overview
**LOCAL CRICKET HUB** is a web application built with Django to manage local cricket tournaments. It allows users to register cricket clubs, manage teams, create tournaments (20 or 50 overs), generate match fixtures, and track scores.

The goal is to provide a modern, scalable platform for local cricket enthusiasts to organize and participate in tournaments efficiently.
Here's a more concise and structured version of your **Local Cricket Hub** project documentation:

---

## **🎯 Core Features**  

### **1. User & Club Management**  
✔️ **User Auth**: Signup/login at `/`  
✔️ **Club Registration**: Name, logo, city, pincode  
✔️ **Dashboard**: Joined teams + tournament creation  

### **2. Team & Players**  
✔️ **Team Creation**: Name, logo, owner details  
✔️ **Player Management**: 11 players per team (roles: batsman/bowler/all-rounder)  
✔️ **Designations**: Captain, Vice-Captain, Wicketkeeper  

### **3. Tournaments & Matches**  
✔️ **Tournament Types**: 20-over or 50-over formats  
✔️ **Fixture Generation**: Customizable dates, venues, gaps  
✔️ **Live Scores**: Track runs, balls, strike rates  

### **4. Stats & Profiles**  
✔️ **Team Profiles**: Player lists + management  
✔️ **Tournament Stats**: Leaderboards for teams/players  



---

## **⚙️ Setup Guide**  

### **1. Prerequisites**  
```bash
git clone https://github.com/skp3214/Local-Cricket-Hub.git
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

### **2. Install & Run**  
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
→ Access at `http://127.0.0.1:8000`  

---

## **🤝 Contribution**  
1. Fork → Create feature branch  
2. Follow Django coding standards  
3. Submit PR with clear description  
4. Report bugs via Issues  

--- 
