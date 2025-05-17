import streamlit as st
import datetime 
from ai_template import get_json_response
from firebase_utils import initialize_firebase

auth_instance, database_instance = initialize_firebase()

system_prompt = """
You are a smart scheduling assistant called “Schedule_Helper”. Your job is to create a clear, manageable weekly schedule for the user based on the information they provide.

When building the schedule:
* Prioritize imminent due dates (homework, projects, tests).
* Spread study sessions and work evenly through the week to avoid cramming.
* Insert short breaks and leave buffer time; never overload any single day.
* Categorize each block as Classes, Homework, Projects, Tests/Quizzes, or Other.
* Suggest specific time blocks (e.g. “Monday 16:00‑17:00 – Study for Math test”).

Output rules (very important):
1. Respond only with valid JSON (no extra text).
2. The JSON must have exactly two top‑level keys:
   • "events" – an array of event objects compatible with streamlit‑calendar.
   • "motivational_message" – a single inspiring sentence.
3. Each event object must contain:
   {
     "title": "📚 English essay",      // short label, emoji optional
     "start": "2025-05-07T14:00:00",   // ISO‑8601
     "end":   "2025-05-07T16:00:00",   // ISO‑8601
     "allDay": false,                  // optional, default false
     "category": "Homework"            // one of the five categories above
   }
4. Use the user’s local timezone (America/Los_Angeles) when generating start and end.
5. Ensure every event’s duration is realistic (30‑ to 120‑minute study blocks work best).
"""

def show(database):
   classes = st.text_area("Type classes (separated by comma)")
   homework = st.text_area("Type homework (separated by comma)")
   upcoming_tests = st.text_input("Type tests (separated by comma)")
   projects = st.text_input("Type projects (separated by comma)")
   date = st.date_input("Enter the date of the week you want to schedule", min_value=datetime.date.today())  

   if st.button("Submit"):

      user_prompt = classes.join(homework).join(upcoming_tests).join(projects)

      schedule = get_json_response(system_prompt, user_prompt)

      st.write(schedule)
      
      data = {
         "userData": {
            "classes": classes,
            "homework": homework,
            "upcoming_tests": upcoming_tests,
            "projects": projects,
            "schedule": schedule,
            "date": date.isoformat()     }
      }
      user = st.session_state['user']
      database.collection("users").document(user['localId']).set(data)

show(database_instance)