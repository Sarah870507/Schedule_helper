import streamlit as st
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
from firebaseconfig import firebaseConfig

# client_config = st.secrets["firebase_client_config"]
# admin_cred_dict = st.secrets ["firebase_admin_sdk"]

# with open("/tmp/service_account.json", "w") as f:
#     json.dump(admin_cred_dict, f)

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Initialize Firestore
if not firebase_admin._apps:
    cred = credentials.Certificate(
        "schedule-helper-e7613-firebase-adminsdk-fbsvc-3f2468cc6d.json")
    firebase_admin.initialize_app(cred)

database = firestore.client()

st.title("Schedule_Helper")

# Display user info if logged in
if "user" in st.session_state:

    page = st.sidebar.radio(
        "Go to", ["Home", "Settings", "Work", "Calendar"], key="main_nav_radio")
    if page == "Home":
        from pages import home
        home.show()
    elif page == "Settings":
        from pages import settings
        settings.show(database=database)
    elif page == "Work":
        from pages import work
        work.show(database)
    elif page == "Calendar":
        from pages import calendar
        calendar.show(database=database)

else:
    choice = st.sidebar.selectbox("Login/Signup", ["Login", "Sign up"])
    email = st.text_input("Email", value="lisarah837@gmail.com")
    password = st.text_input(
        "Password", value="Aliceinborderland10", type="password")

    if choice == "Sign up":
        # age
        # username
        # grade
        # school
        bday = st.date_input("When is your birthday?")
        gender = st.selectbox(
            "Gender", ("Male", "Female", "Prefer Not to Say"))
        age = st.selectbox("Age", (11, 12, 13, 14, 15, 16, 17, 18))
        username = st.text_input("Username")
        grade = st.text_input("Grade")
        school = st.text_input("School")
        if st.button("Create Account"):
            try:
                user = auth.create_user_with_email_and_password(
                    email, password)
                st.success("Account created successfully")
                database.collection("users").document(user['localId']).set({
                    "email": email,
                    "username": username,
                    "gender": gender,
                    "age": age,
                    "grade": grade,
                    "school": school,
                    "bday": bday.isoformat()
                })
            except Exception as e:
                st.error(f"Error: {e}")

    elif choice == "Login":
        if st.button("Login"):
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.success("Login Successful")
                st.session_state['user'] = user
            except Exception as e:
                st.error(f"Error: {e}")
