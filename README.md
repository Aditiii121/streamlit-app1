👥 User Interface
Authentication:
Users can sign in or register through a dedicated login page. Admin access is restricted to a predefined username and password.

🧑‍🎓 User Dashboard
Event Listings:
All upcoming events are showcased in visually distinct cards displaying the event name, description, date, and venue, along with a "Register" button.

My Registrations:
A personalized section where users can review the list of events they have registered for.

🛠️ Admin Panel
Admin Login:
Secured admin login using a designated username and password.

Event Controls:
Admins can seamlessly add, edit, view, and delete events.

Participant Overview:
View a list of registered users for each event, categorized accordingly.

🗃️ Database Design
Database Used: SQLite

Tables:

events: Contains event-specific details like title, description, date, and location.

registrations: Stores participant data including name, roll number, and email address.

👨‍💻 Team Members
Aditi Shirke – 23102C0053

Asees Kaur Dham – 23102C0050

Vedanti Ghanekar – 23102C0008

🧰 Technologies Implemented
Frontend & Backend Framework: Streamlit (Python)

Database: SQLite (used for storing and managing all records)

🚀 How to Run the Project
Download and unzip the project folder.

Open the folder in Command Prompt.

Install the required dependencies using:

bash
Copy
Edit
pip install -r requirements.txt
Launch the application with:

bash
Copy
Edit
streamlit run app.py
The web interface will open in your browser, ready to use.
