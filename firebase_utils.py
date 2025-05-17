import streamlit as st
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
import traceback


@st.cache_resource
def initialize_firebase():
    firebase_config = {
        "apiKey": st.secrets["firebase_client_config"]["apiKey"],
        "authDomain": st.secrets["firebase_client_config"]["authDomain"],
        "databaseURL": st.secrets["firebase_client_config"]["databaseURL"],
        "projectId": st.secrets["firebase_client_config"]["projectId"],
        "storageBucket": st.secrets["firebase_client_config"]["storageBucket"],
        "messagingSenderId": st.secrets["firebase_client_config"]["messagingSenderId"],
        "appId": st.secrets["firebase_client_config"]["appId"],
    }

    # firebase_config = {
    #     "apiKey": "AIzaSyDiYUjiegPOAq4Ss-GZgsi38gPM9odW32k",
    #     "authDomain": "schedule-helper-e7613.firebaseapp.com",
    #     "databaseURL": "https://dummy.firebaseio.com",
    #     "projectId": "schedule-helper-e7613",
    #     "storageBucket": "schedule-helper-e7613.firebasestorage.app",
    #     "messagingSenderId": "1063953113120",
    #     "appId": "1:1063953113120:web:4afa41425ba64b195f9c45"
    # }

    firebase = pyrebase.initialize_app(firebase_config)
    auth = firebase.auth()

    try:
        service_account_info = dict(st.secrets["firebase_admin_sdk"])
        # service_account_info = "/workspaces/Schedule_helper/schedule-helper-e7613-firebase-adminsdk-fbsvc-3f2468cc6d.json"
        cred = credentials.Certificate(service_account_info)
    except Exception:
        st.error("Could not load Firebase Admin service account from secrets.")
        st.text(traceback.format_exc())
        st.stop()

    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

    database = firestore.client()

    return auth, database
