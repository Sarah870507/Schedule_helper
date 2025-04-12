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

#Initialize Firestore
if not firebase_admin._apps:
  cred = credentials.Certificate("/workspaces/Schedule_helper/firebaseconfig.py")
  firebase_admin.initialize_app(cred)

database = firestore.client()

st.title("Schedule_Helper")

choice = st.sidebar.selectbox("Login/Signup", ["Login", "Sign up"])

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if choice == "Sign up":
  #age
  #username
  #grade
  #school
  bday = st.date_input("When is your birthday?")
  gender = st.selectbox("Gender", ("Male", "Female", "Prefer Not to Say"))
  age = st.selectbox("Age", (11, 12, 13, 14, 15, 16, 17, 18))
  username = st.text_input("Username")
  grade = st.text_input("Grade")
  school = st.text_input("School")
  if st.button("Create Account"):
    try:
      user = auth.create_user_with_email_and_password(email, password)
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

# Display user info if logged in
if "user" in st.session_state:
    st.subheader("Welcome!")
    user = st.session_state['user']
    user_info = database.collection("users").document(user['localId']).get().to_dict()
    st.write(f"Username: {user_info['username']}")
    st.write(f"Email: {user_info['email']}")
    if st.button("Logout"):
        st.session_state.pop("user", None)
        st.success("Logged out successfully.")
        st.rerun()

