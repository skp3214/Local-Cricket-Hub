
# 🏏 LOCAL CRICKET HUB - Development Phase 

## Project Overview
**LOCAL CRICKET HUB** is a web application built with Django to manage local cricket tournaments. It allows users to register cricket clubs, manage teams, create tournaments (20 or 50 overs), generate match fixtures, and track live scores using Django Channels. The application is currently in the **development phase**, with core features being implemented and tested.

The goal is to provide a modern, scalable platform for local cricket enthusiasts to organize and participate in tournaments efficiently.

---

## Current Status
- **Phase**: Development
- **Version**: 0.1 (Pre-alpha)
- **Date**: March 16, 2025

---

## Features in Development
1. **🔐 User Authentication**
    - Login and signup functionality at the root endpoint (`/`).
2. **🏏 Club Management**
    - Register a cricket club with details like club name, image, city, and pincode.
    - Dashboard to view joined teams and create tournaments (20 or 50 overs).
3. **👥 Team Management**
    - Register a team with team name, image, and owner's name.
    - Join an existing cricket club and add up to 11 players with details (name, type: bowler/batsman/allrounder, designation: captain/vc/wk/normal).
4. **🏆 Tournament Management**
    - Create tournaments with options for team participation limits.
    - Generate match fixtures with start date, end date, gap days, number of venues, and venue names.
    - Display today's match on the club dashboard.
5. **📊 Live Scoring**
    - Score page with player stats (runs, balls, strike rate, bowler info) and live updates using Django Channels.
6. **📈 Stats and Profiles**
    - Tournament stats for teams and players.
    - Team profile with player management options.

---

## Planned Features
- 🎨 Full CSS styling for a modern UI (to be added later).
- 🗓️ Tournament scheduling algorithm for automatic fixture generation.
- 🔔 Real-time notifications for match updates.
- 📱 Mobile responsiveness.
- 🛠️ Admin panel enhancements for tournament oversight.
- 📊 Player performance analytics and leaderboards.

---

## Setup Instructions (Development Environment)
1. **Prerequisites**
    - Python 3.9+
    - Django 4.x
    - Django Channels (for live updates)
    - PostgreSQL (recommended, SQLite for initial dev)
    - Redis (for Channels backend)
    - Git

2. **Clone the Repository**
    - Clone this repository to your local machine.

3. **Virtual Environment**
    - Create and activate a virtual environment:
      - `python -m venv venv`
      - `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)

4. **Install Dependencies**
    - Install required packages using `requirements.txt` (to be created):
      - `pip install -r requirements.txt`

5. **Database Setup**
    - Configure your database in `settings.py`.
    - Run migrations:
      - `python manage.py makemigrations`
      - `python manage.py migrate`

6. **Redis Setup**
    - Install and run Redis locally or use a hosted service for Channels.

7. **Run the Server**
    - Start the Django development server:
      - `python manage.py runserver`
    - Access the app at `http://127.0.0.1:8000/`.

8. **Channels Setup**
    - Ensure WebSocket functionality is tested with Redis running.

---

## Development Notes
- **🗄️ Database**: Currently using a relational database; schema is subject to change as features evolve.
- **🔐 Authentication**: Basic Django auth is implemented; consider adding OAuth/social logins later.
- **📡 Live Updates**: Django Channels is integrated for real-time scoring—test WebSocket connections thoroughly.
- **🎨 CSS**: Styling is minimal; a modern UI will be added in a later phase.
- **🧪 Testing**: Unit tests are not yet implemented—focus is on core functionality.
- **📈 Scalability**: Models and views are designed with scalability in mind, but optimization will come after core completion.

---

## Known Issues
- 🛠️ Fixture generation logic is manual; automation is pending.
- 🖥️ Live scoring UI is basic and needs refinement.
- ⚠️ Error handling for edge cases (e.g., duplicate club/team names) is incomplete.
- 🖼️ Image uploads lack validation and resizing.

---

## How to Contribute
- 🍴 Fork the repository and create feature branches for specific tasks.
- 🛠️ Follow Django best practices for models, views, and templates.
- 📜 Submit pull requests with clear descriptions of changes.
- 🐛 Report bugs or suggest features via issues.

---

## Next Steps
1. Complete core models and views for club/team/tournament management.
2. Implement Django Channels for live score updates.
3. Add basic templates with minimal styling.
4. Test authentication and user workflows.
5. Plan CSS framework integration (e.g., Bootstrap/Tailwind).

---

*This README will be updated as the project progresses. Stay tuned for more details!*

