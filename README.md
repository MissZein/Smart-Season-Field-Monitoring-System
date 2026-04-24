🌾 SmartSeason: Field Monitoring & Management System
SmartSeason is a specialized agricultural ERP designed to bridge the gap between farm administrators and field agents. It provides real-time monitoring of crop lifecycles, automates risk detection, and streamlines task delegation through a high-performance, modern web interface.

🛠️ Design Decisions
1. The "Smart" Logic (Automated Risk Detection)
Unlike traditional systems where a user manually flags an issue, SmartSeason uses a time-based risk algorithm. By calculating the delta between the planting_date and the current_stage, the system automatically flags fields as "At Risk" if they stagnate in the "Planted" or "Growing" phase beyond industry-standard durations.

2. Interactivity with HTMX
To provide a SaaS-like experience without the complexity of a heavy frontend framework (like React), we used HTMX. This allows for:

Live Search: Filtering the field database instantly as the user types.

Partial Page Updates: Modals and table rows update without a full browser refresh, significantly reducing server load and improving UX.

3. UI/UX: Recognition over Recall
The dashboard utilizes Material Symbols and a color-coded badge system. Icons for "Yields," "At Risk," and "Alerts" provide immediate visual context, allowing users to assess farm health in seconds.

📋 Assumptions Made
Crop Durations: For the "At Risk" logic, it is assumed that germination (Planted → Growing) should occur within 14 days and standard growth within 60-100 days depending on the crop.

User Roles: The system assumes two primary personas:

Admins: Full CRUD (Create, Read, Update, Delete) access.

Agents: Read-only access to assigned fields with the ability to update growth stages.

Connectivity: The system assumes a stable internet connection for HTMX to communicate with the Django backend.

⚙️ Setup Instructions
1. Clone & Environment Setup
Bash
git clone https://github.com/MissZein/Smart-Season-Field-Monitoring-System
cd Smart-Season
python -m venv venv
# Windows:
venv\Scripts\activate 
# Mac/Linux:
source venv/bin/activate
2. Install Dependencies
Bash
pip install -r requirements.txt
3. Database Initialization
Bash
python manage.py makemigrations
python manage.py migrate
4. Create Superuser (Admin)
Bash
python manage.py createsuperuser
5. Run the System
Bash
python manage.py runserver
Access the dashboard at http://127.0.0.1:8000/dashboard/

SYSTEM LOGIN PASSWORDS/ DEMO CREDENTIALS
Admin1 - @87654321
agent1,agent2,agent3,agent4 - @12345678

🚀 Deployment Live link
https://smart-season-ei7k.onrender.com