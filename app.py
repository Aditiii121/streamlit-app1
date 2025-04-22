import streamlit as st
import pandas as pd

from database import (
    create_event_table,
    create_registration_table,
    create_users_table,
    add_event,
    delete_event,
    register_user_for_event,
    get_participants_for_event,
    add_user,
    verify_user,
    is_event_name_unique,
    account_exists,
    get_user_info,
    already_registered,
    registered_events,
    fetch_events
)

# Updated CSS block
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #eef2f3, #8e9eab);
        padding: 0;
        margin: 0;
    }
    .main {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0px 0px 15px rgba(0,0,0,0.1);
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3, h4 {
        color: #003366;
    }
    .custom-btn {
        background-color: #003366;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        margin-top: 0.5rem;
    }
    .event-box {
        border: 1px solid #ccc;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        background-color: #f9fbff;
    }
    </style>
""", unsafe_allow_html=True)


# Initialize the database tables
create_users_table()
create_event_table()
create_registration_table()

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"

def login():
    st.markdown("<div class='main'>", unsafe_allow_html=True)
    st.title("🎉 Campus Event Management System")
    option = st.selectbox("Login / Sign-Up", ["Login", "Signup"])

    if option == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login", type="primary"):
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                st.session_state["logged_in"] = True
                st.session_state["is_admin"] = True
                st.session_state["view"] = "admin"
                st.success("✅ Logged in as Admin!")
                st.rerun()
            elif verify_user(username, password):
                st.session_state["logged_in"] = True
                st.session_state["is_admin"] = False
                st.session_state["username"] = username
                st.session_state["view"] = "user"
                st.success("✅ Logged in as User!")
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")

    elif option == "Signup":
        signup()
    st.markdown("</div>", unsafe_allow_html=True)

def signup():
    st.markdown("<div class='main'>", unsafe_allow_html=True)
    st.title("📝 User Registration")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    username = st.text_input("Choose a Username")
    password = st.text_input("Create a Password", type="password")

    if st.button("Sign Up"):
        if not name.strip() or not email.strip() or not username.strip() or not password.strip():
            st.error("All fields must be filled.")
        elif account_exists(username, email):
            add_user(name, email, username, password)
            st.success("🎉 Registration successful! Please log in.")
            st.session_state["view"] = "login"
        else:
            st.error("Username or Email already exists.")
    st.markdown("</div>", unsafe_allow_html=True)

def logout():
    if st.sidebar.button("🚪 Logout"):
        st.session_state["logged_in"] = False
        st.session_state["is_admin"] = False
        st.session_state["view"] = "login"
        st.rerun()

def admin_view():
    st.sidebar.title("🛠️ Admin Menu")
    options = st.sidebar.radio("Select Action", ["Create Event", "Manage Events"])

    logout()

    st.markdown("<div class='main'>", unsafe_allow_html=True)

    if options == "Create Event":
        st.title("➕ Add New Event")
        title = st.text_input("Event Title")
        description = st.text_area("Event Description")
        date = st.date_input("Event Date")
        location = st.text_input("Event Location")

        if st.button("Add Event", type="primary"):
            if not title.strip() or not description.strip() or not location.strip():
                st.error("All fields must be filled.")
            elif is_event_name_unique(title):
                add_event(title, description, date.strftime("%Y-%m-%d"), location)
                st.success("✅ Event added successfully!")
            else:
                st.error("Event title already exists.")

    elif options == "Manage Events":
        st.title("📋 All Events")
        search_query = st.text_input("Search Events", "")
        events = fetch_events(search_query if search_query.strip() else None)

        if events:
            for event in events:
                st.markdown(f"""
                <div class="event-box">
                    <h4>{event[1]}</h4>
                    <p><strong>Description:</strong> {event[2]}</p>
                    <p><strong>Date:</strong> {event[3]}</p>
                    <p><strong>Location:</strong> {event[4]}</p>
                </div>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("👥 View Participants", key=f"view_{event[0]}"):
                        participants = get_participants_for_event(event[0])
                        if participants:
                            df = pd.DataFrame(participants, columns=["Name", "Email"])
                            st.table(df)
                        else:
                            st.info("No participants yet.")
                with col2:
                    if st.button("❌ Delete Event", key=f"delete_{event[0]}"):
                        delete_event(event[0])
                        st.success("🗑️ Event deleted.")
                        st.rerun()
        else:
            st.info("No events found.")

    st.markdown("</div>", unsafe_allow_html=True)

def user_view():
    logout()
    user_info = get_user_info(st.session_state["username"])
    if not user_info:
        st.error("User info not found.")
        return

    name, email = user_info
    st.sidebar.title("👤 User Menu")
    choice = st.sidebar.radio("Go To", ["View Events", "Registered Events"])

    st.markdown("<div class='main'>", unsafe_allow_html=True)

    if choice == "View Events":
        st.title("📅 Upcoming Events")
        search_query = st.text_input("Search Events", "")
        events = fetch_events(search_query if search_query.strip() else None)

        if events:
            for event in events:
                st.markdown(f"""
                <div class="event-box">
                    <h4>{event[1]}</h4>
                    <p><strong>Description:</strong> {event[2]}</p>
                    <p><strong>Date:</strong> {event[3]}</p>
                    <p><strong>Location:</strong> {event[4]}</p>
                </div>
                """, unsafe_allow_html=True)

                if st.button("✅ Register", key=f"reg_{event[0]}"):
                    if already_registered(event[0], email):
                        st.warning("Already registered for this event.")
                    else:
                        register_user_for_event(event[0], name, email)
                        st.success("🎟️ Registered successfully!")
        else:
            st.info("No events found.")

    elif choice == "Registered Events":
        st.title("🎟️ My Registered Events")
        events = registered_events(email)
        if events:
            for event in events:
                st.markdown(f"""
                <div class="event-box">
                    <h4>{event[1]}</h4>
                    <p><strong>Description:</strong> {event[2]}</p>
                    <p><strong>Date:</strong> {event[3]}</p>
                    <p><strong>Location:</strong> {event[4]}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No registered events.")
    
    st.markdown("</div>", unsafe_allow_html=True)

def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["is_admin"] = False
        st.session_state["view"] = "login"

    if not st.session_state["logged_in"]:
        login()
    else:
        if st.session_state["is_admin"]:
            admin_view()
        else:
            user_view()

if __name__ == "__main__":
    main()
