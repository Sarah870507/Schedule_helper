import streamlit as st
from firebase_utils import initialize_firebase

auth, database = initialize_firebase()


def signup(email, password, username, bday, gender, age, grade, school):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        user_id = user['localId']
        database.collection("users").document(user_id).set({
            "email": email,
            "username": username,
            "gender": gender,
            "age": age,
            "grade": grade,
            "school": school,
            "bday": bday.isoformat()
        })
        st.success("Account created successfully. Please login.")
        return True
    except Exception as e:
        st.error(f"Error creating account: {e}")
        return False


def login(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        st.session_state['user'] = user
        st.session_state['is_authenticated'] = True
        st.session_state['user_id'] = user['localId']
        st.session_state['user_token'] = user['idToken']
        user_doc = database.collection("users").document(user['localId']).get()
        if user_doc.exists:
            st.session_state['username'] = user_doc.to_dict().get(
                'username', 'User')
        else:
            st.session_state['username'] = "User"

        st.success(f"Welcome, {st.session_state['username']}!")
        st.rerun()
        return True
    except Exception as e:
        st.error(f"Error logging in: {e}")
        st.session_state['is_authenticated'] = False
        if 'user_id' in st.session_state:
            del st.session_state['user_id']
        if 'user_token' in st.session_state:
            del st.session_state['user_token']
        if 'username' in st.session_state:
            del st.session_state['username']

        return False


def logout():
    st.session_state['is_authenticated'] = False
    if 'user_id' in st.session_state:
        del st.session_state['user_id']
    if 'user_token' in st.session_state:
        del st.session_state['user_token']
    if 'username' in st.session_state:
        del st.session_state['username']
    st.success("Logged out successfully.")
    st.rerun()


def show_login_signup_form():
    st.sidebar.title("Authentication")
    choice = st.sidebar.radio("Choose Action", ["Login", "Signup"])

    if choice == "Login":
        email = st.sidebar.text_input("Email")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login", key="login_btn"):
            login(email, password)

    elif choice == "Signup":
        email = st.sidebar.text_input("Email")
        password = st.sidebar.text_input("Password", type="password")
        username = st.sidebar.text_input("Username")
        bday = st.date_input("When is your birthday?")
        gender = st.selectbox(
            "Gender", ("Male", "Female", "Prefer Not to Say"))
        age = st.selectbox("Age", (11, 12, 13, 14, 15, 16, 17, 18))
        grade = st.text_input("Grade")
        school = st.text_input("School")
        if st.sidebar.button("Create Account", key="signup_btn"):
            signup(email, password, username, bday, gender, age, grade, school)


def is_authenticated():
    return st.session_state.get('is_authenticated', False)
