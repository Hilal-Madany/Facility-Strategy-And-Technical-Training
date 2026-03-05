import streamlit as st
import os
from jinja2 import Environment, FileSystemLoader
import datetime

# --- DIRECTORY CONFIG ---
current_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(current_dir, 'templates')
env = Environment(loader=FileSystemLoader(template_path))

st.set_page_config(page_title="Vendor Portal", layout="wide")

# --- DATA RESET LOGIC ---
# This function wipes the memory so a new vendor can start fresh
def restart_form():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.session_state.step = 1
    st.session_state.data = {}

# Initialize Session State if not present
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'data' not in st.session_state:
    st.session_state.data = {}

def next_step(): st.session_state.step += 1
def prev_step(): st.session_state.step -= 1

# --- UI HEADER ---
col_t, col_r = st.columns([4, 1])
with col_t:
    st.title("🏛️ Vendor Assessment System")
with col_r:
    if st.button("🆕 New Entry"):
        restart_form()
        st.rerun()

st.write(f"Section {st.session_state.step} of 8")
st.progress(st.session_state.step / 8)

# --- STEPS 1-7 (CAPTURING DATA) ---
if st.session_state.step == 1:
    st.header("1. Company Identity")
    st.session_state.data['name'] = st.text_input("Company Name", st.session_state.data.get('name', ""))
    st.session_state.data['reg_office'] = st.text_area("Registered Office", st.session_state.data.get('reg_office', ""))
    st.button("Next ➡️", on_click=next_step)

elif st.session_state.step == 2:
    st.header("2. Legal & Statutory")
    st.session_state.data['pan'] = st.text_input("PAN No.", st.session_state.data.get('pan', ""))
    st.session_state.data['gst'] = st.text_input("GST No.", st.session_state.data.get('gst', ""))
    c1, c2 = st.columns(2)
    c1.button("⬅️ Back", on_click=prev_step)
    c2.button("Next ➡️", on_click=next_step)

# ... (Steps 3-7 remain same as previous version) ...
# Assuming Step 8 is the Report Generation

elif st.session_state.step == 8:
    st.header("8. Final Assessment Report")
    
    # Calculate Score
    score = 0
    if st.session_state.data.get('pan'): score += 50 
    if st.session_state.data.get('gst'): score += 50
    st.session_state.data['score'] = score

    try:
        template = env.get_template('full_report.html')
        report_html = template.render(d=st.session_state.data, date=datetime.date.today().strftime("%d-%m-%Y"))
        
        # DISPLAY REPORT
        st.components.v1.html(report_html, height=1200, scrolling=True)
        
        st.success("Report Generated. Click 'New Entry' at the top to clear this data.")
    except Exception as e:
        st.error(f"Template Error: {e}")
