import streamlit as st
import os
from jinja2 import Environment, FileSystemLoader
import datetime

# --- DIRECTORY SETUP ---
current_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(current_dir, 'templates')
env = Environment(loader=FileSystemLoader(template_path))

st.set_page_config(page_title="Vendor Assessment Form", layout="wide")

# Initialize Session State
if 'step' not in st.session_state: st.session_state.step = 1
if 'data' not in st.session_state: st.session_state.data = {}

def next_step(): st.session_state.step += 1
def prev_step(): st.session_state.step -= 1

st.title("📋 VENDOR / SUB-VENDOR ASSESSMENT FORM")
st.write(f"**Section {st.session_state.step} of 6**")
st.progress(st.session_state.step / 6)

# --- STEP 1: BASIC IDENTITY ---
if st.session_state.step == 1:
    st.header("1. Name & Registered Office")
    st.session_state.data['name'] = st.text_input("Name of Supplier / Sub-Vendor in Full", st.session_state.data.get('name', "Accumen Techno Marketing Solution"))
    st.session_state.data['reg_office'] = st.text_area("Registered Office Address", st.session_state.data.get('reg_office', "Fatehpur"))
    st.session_state.data['works_addr'] = st.text_area("Factory / Works Address", st.session_state.data.get('works_addr', "Haswa"))
    
    col1, col2 = st.columns(2)
    st.session_state.data['tel'] = col1.text_input("Telephone / Mobile", st.session_state.data.get('tel', "9650329719"))
    st.session_state.data['email'] = col2.text_input("Email ID", st.session_state.data.get('email', "info.accumentechno@gmail.com"))
    st.button("Save & Next ➡️", on_click=next_step)

# --- STEP 2: STATUTORY REGISTRATIONS ---
elif st.session_state.step == 2:
    st.header("2. Statutory & Tax Registrations")
    c1, c2 = st.columns(2)
    st.session_state.data['pan'] = c1.text_input("PAN / TAN No.", st.session_state.data.get('pan', "BVGPM3310K"))
    st.session_state.data['gst'] = c2.text_input("GST / TIN No.", st.session_state.data.get('gst', "212601"))
    st.session_state.data['msme_no'] = st.text_input("MSME Registration No.", st.session_state.data.get('msme_no', "8408"))
    st.session_state.data['msme_type'] = st.selectbox("Category of Industry", ["Micro", "Small", "Medium", "Large"])
    
    colb, coln = st.columns(2)
    colb.button("⬅️ Back", on_click=prev_step)
    coln.button("Save & Next ➡️", on_click=next_step)

# --- STEP 3: MANPOWER & ORGANISATION ---
elif st.session_state.step == 3:
    st.header("3. Organisational Soundness")
    st.session_state.data['commence_year'] = st.text_input("Year of Commencement of Business", st.session_state.data.get('commence_year', "2020"))
    st.session_state.data['area'] = st.number_input("Total Covered Area (Sq. m.)", value=st.session_state.data.get('area', 250))
    st.session_state.data['power'] = st.text_input("Connected Load (kVA)", st.session_state.data.get('power', "2"))
    
    st.subheader("Employee Details")
    m1, m2, m3 = st.columns(3)
    st.session_state.data['grad_staff'] = m1.number_input("Graduate Engineers", value=st.session_state.data.get('grad_staff', 1))
    st.session_state.data['diploma_staff'] = m2.number_input("Diploma Staff", value=st.session_state.data.get('diploma_staff', 3))
    st.session_state.data['skilled_workers'] = m3.number_input("Skilled Workers", value=st.session_state.data.get('skilled_workers', 5))

    colb, coln = st.columns(2)
    colb.button("⬅️ Back", on_click=prev_step)
    coln.button("Save & Next ➡️", on_click=next_step)

# --- STEP 4: TECHNICAL & MACHINERY ---
elif st.session_state.step == 4:
    st.header("4. Technical & Manufacturing Capability")
    st.session_state.data['machinery'] = st.text_area("List of Machinery (e.g. LATHE, MILLING)", st.session_state.data.get('machinery', "LATHE, MILLING"))
    st.session_state.data['inhouse_test'] = st.radio("In-house Testing Facilities Available?", ["Yes", "No"], index=0)
    st.session_state.data['outsourced'] = st.text_input("Outsourced Process (if any)", st.session_state.data.get('outsourced', "NO"))
    
    colb, coln = st.columns(2)
    colb.button("⬅️ Back", on_click=prev_step)
    coln.button("Save & Next ➡️", on_click=next_step)

# --- STEP 5: QUALITY & FINANCIALS ---
elif st.session_state.step == 5:
    st.header("5. Quality Control & Financial Soundness")
    st.session_state.data['iso9001'] = st.selectbox("Is company ISO 9001 Certified?", ["Yes", "No"], index=0)
    st.session_state.data['q_manual'] = st.radio("Written QC Manual available?", ["Yes", "No"], index=0)
    st.session_state.data['traceability'] = st.radio("System for Traceability?", ["Yes", "No"], index=0)
    
    st.subheader("Financial Performance (Last 3 Years)")
    st.session_state.data['turnover_3'] = st.number_input("Turnover Year 3 (Cr)", value=st.session_state.data.get('turnover_3', 2.5))
    st.session_state.data['networth'] = st.number_input("Current Net Worth (Cr)", value=st.session_state.data.get('networth', 1.0))

    colb, coln = st.columns(2)
    colb.button("⬅️ Back", on_click=prev_step)
    coln.button("Save & Next ➡️", on_click=next_step)

# --- STEP 6: FINAL REPORT PREVIEW ---
elif st.session_state.step == 6:
    st.header("6. Final Assessment Report")
    
    # Simple Compliance Score Logic
    score = 0
    if st.session_state.data.get('iso9001') == "Yes": score += 25
    if st.session_state.data.get('inhouse_test') == "Yes": score += 25
    if st.session_state.data.get('q_manual') == "Yes": score += 25
    if st.session_state.data.get('turnover_3', 0) > 1: score += 25
    st.session_state.data['score'] = score

    try:
        template = env.get_template('full_report.html')
        report_html = template.render(d=st.session_state.data, date=datetime.date.today().strftime("%d/%m/%Y"))
        
        # Display the HTML Report
        st.components.v1.html(report_html, height=1200, scrolling=True)
        
        st.success("Assessment Generated. Use Browser Print (Ctrl+P) to save as PDF.")
        if st.button("⬅️ Back to Edit"): st.session_state.step = 1
        
    except Exception as e:
        st.error(f"Template Error: Ensure 'templates/full_report.html' exists in your GitHub folder. Error: {e}")
