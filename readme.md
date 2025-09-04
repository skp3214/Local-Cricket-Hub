
# LOCAL CRICKET HUB🏏 

## Project Overview
**LOCAL CRICKET HUB** is a web application built with Django to manage local cricket tournaments. It allows users to register, create cricket clubs, manage teams, create tournaments (20 or 50 overs), generate match fixtures, and track scores.

The goal is to provide a modern, scalable platform for local cricket enthusiasts to organize and participate in tournaments efficiently.

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
## ScreenShots
![Screenshot_4-9-2025_135725_local-cricket-hub onrender com](https://github.com/user-attachments/assets/814bed72-72a8-4fbb-820a-a3404b537983)
![image](https://github.com/user-attachments/assets/b6aa59c0-d4d1-48b2-8efe-5d0470e5ff5f)
![image](https://github.com/user-attachments/assets/9053c72a-bbe6-4fd9-9ecd-cc91ee90f006)
![image](https://github.com/user-attachments/assets/808d4b65-ed56-41af-98c9-dc3922d65020)
![image](https://github.com/user-attachments/assets/f506a77a-a3c6-465c-ad22-ee89cc0b25cc)
![image](https://github.com/user-attachments/assets/0814f3e5-f1c0-454a-848c-fd542b659d1a)
![image](https://github.com/user-attachments/assets/4b5b4866-5a8d-40af-8479-f3bbe6f248c6)
![image](https://github.com/user-attachments/assets/46052c25-a9e6-464d-b3cc-87f27619eb20)
![image](https://github.com/user-attachments/assets/cc444730-85ec-468f-bff0-2351857191c9)
![image](https://github.com/user-attachments/assets/3532358a-5f0a-44a3-95b5-2bda0a64e8fa)
![image](https://github.com/user-attachments/assets/2a9c4f7c-4293-43e8-9f63-51307481dddb)


