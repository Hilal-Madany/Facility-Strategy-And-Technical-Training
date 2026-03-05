import streamlit as st
import os
from jinja2 import Environment, FileSystemLoader
import datetime

# --- SYSTEM & PATH CONFIG ---
current_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(current_dir, 'templates')
env = Environment(loader=FileSystemLoader(template_path))

st.set_page_config(page_title="Vendor Assessment Full-Stack", layout="wide")

# Initialize State
if 'step' not in st.session_state: st.session_state.step = 1
if 'data' not in st.session_state: st.session_state.data = {}

def next_s(): st.session_state.step += 1
def prev_s(): st.session_state.step -= 1

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("Navigation")
    st.info(f"Current Section: {st.session_state.step}/8")
    if st.button("Reset Form"):
        st.session_state.data = {}
        st.session_state.step = 1
        st.rerun()

# --- FORM SEGMENTS ---
if st.session_state.step == 1:
    st.header("Step 1: Company Profile")
    st.session_state.data['name'] = st.text_input("Company Name", st.session_state.data.get('name', "Accumen Techno Marketing Solution"))
    st.session_state.data['reg_office'] = st.text_area("Registered Office", st.session_state.data.get('reg_office', "Fatehpur"))
    st.session_state.data['works_addr'] = st.text_area("Factory Address", st.session_state.data.get('works_addr', "Haswa"))
    st.button("Next ➡️", on_click=next_s)

elif st.session_state.step == 2:
    st.header("Step 2: Contact & Identity")
    c1, c2 = st.columns(2)
    st.session_state.data['tel'] = c1.text_input("Mobile", st.session_state.data.get('tel', "9650329719"))
    st.session_state.data['email'] = c2.text_input("Email", st.session_state.data.get('email', "info.accumentechno@gmail.com"))
    st.session_state.data['pan'] = st.text_input("PAN NO.", st.session_state.data.get('pan', "BVGPM3310K"))
    col1, col2 = st.columns(2)
    col1.button("⬅️ Back", on_click=prev_s)
    col2.button("Next ➡️", on_click=next_s)

elif st.session_state.step == 3:
    st.header("Step 3: Statutory Details")
    st.session_state.data['gst'] = st.text_input("GST NO.", st.session_state.data.get('gst', "212601"))
    st.session_state.data['msme_no'] = st.text_input("MSME NO.", st.session_state.data.get('msme_no', "8408"))
    st.session_state.data['msme_type'] = st.selectbox("Category", ["Micro", "Small", "Medium"])
    col1, col2 = st.columns(2)
    col1.button("⬅️ Back", on_click=prev_s)
    col2.button("Next ➡️", on_click=next_s)

elif st.session_state.step == 4:
    st.header("Step 4: Infrastructure")
    st.session_state.data['commence_year'] = st.text_input("Year Business Started", "2020")
    st.session_state.data['area'] = st.number_input("Factory Area (Sq. m.)", value=250)
    st.session_state.data['power'] = st.text_input("Power Load (kVA)", "2")
    col1, col2 = st.columns(2)
    col1.button("⬅️ Back", on_click=prev_s)
    col2.button("Next ➡️", on_click=next_s)

elif st.session_state.step == 5:
    st.header("Step 5: Technical Capability")
    st.session_state.data['machinery'] = st.text_area("Machinery List", "LATHE, MILLING")
    st.session_state.data['inhouse_test'] = st.radio("In-house Testing?", ["Yes", "No"])
    m1, m2 = st.columns(2)
    st.session_state.data['grad_staff'] = m1.number_input("Engineers", value=1)
    st.session_state.data['skilled_workers'] = m2.number_input("Skilled Workers", value=5)
    col1, col2 = st.columns(2)
    col1.button("⬅️ Back", on_click=prev_s)
    col2.button("Next ➡️", on_click=next_s)

elif st.session_state.step == 6:
    st.header("Step 6: Products & Performance")
    st.session_state.data['prod_category'] = st.multiselect("Category", ["IT", "Mechanical", "Electrical", "Marketing"], default=["Marketing"])
    st.session_state.data['ref_1'] = st.text_area("Project Reference 1", "SJVN Limited - Digital Branding")
    st.session_state.data['govt_exp'] = st.radio("PSU Experience?", ["Yes", "No"])
    col1, col2 = st.columns(2)
    col1.button("⬅️ Back", on_click=prev_s)
    col2.button("Next ➡️", on_click=next_s)

elif st.session_state.step == 7:
    st.header("Step 7: Quality & Financials")
    st.session_state.data['iso9001'] = st.selectbox("ISO 9001?", ["Yes", "No"])
    st.session_state.data['turnover_3'] = st.number_input("Turnover FY 24-25 (Cr)", value=2.5)
    st.session_state.data['networth'] = st.number_input("Net Worth (Cr)", value=1.0)
    col1, col2 = st.columns(2)
    col1.button("⬅️ Back", on_click=prev_s)
    col2.button("Generate Final Report 📄", on_click=next_s)

elif st.session_state.step == 8:
    st.header("Step 8: Final Detailed Report")
    
    # Calculate Final Score
    score = 0
    if st.session_state.data.get('iso9001') == "Yes": score += 25
    if st.session_state.data.get('govt_exp') == "Yes": score += 25
    if st.session_state.data.get('inhouse_test') == "Yes": score += 25
    if st.session_state.data.get('turnover_3', 0) > 1: score += 25
    st.session_state.data['score'] = score

    try:
        template = env.get_template('full_report.html')
        report_html = template.render(d=st.session_state.data, date=datetime.date.today().strftime("%d %B %Y"))
        
        # Multi-page iframe display
        st.components.v1.html(report_html, height=2000, scrolling=True)
        
        if st.button("⬅️ Edit Information"): st.session_state.step = 1
    except Exception as e:
        st.error(f"Search Error: Check 'templates/full_report.html'. Error: {e}")
