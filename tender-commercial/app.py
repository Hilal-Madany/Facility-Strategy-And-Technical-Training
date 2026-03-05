import streamlit as st
import os
from jinja2 import Environment, FileSystemLoader
import datetime

# --- DIRECTORY CONFIGURATION ---
# This ensures the app finds the 'templates' folder regardless of the hosting environment
current_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(current_dir, 'templates')
env = Environment(loader=FileSystemLoader(template_path))

st.set_page_config(page_title="Detailed Vendor Assessment", layout="wide")

# --- SESSION STATE INITIALIZATION ---
if 'step' not in st.session_state: st.session_state.step = 1
if 'data' not in st.session_state: st.session_state.data = {}

def next_step(): st.session_state.step += 1
def prev_step(): st.session_state.step -= 1

st.title("🏛️ Vendor / Sub-Vendor Detailed Assessment")
st.write(f"Step {st.session_state.step} of 8")
st.progress(st.session_state.step / 8)

# --- NAVIGATION LOGIC ---
if st.session_state.step == 1:
    st.header("1. Company Identification")
    st.session_state.data['name'] = st.text_input("Full Name of Supplier", st.session_state.data.get('name', "Accumen Techno Marketing Solution"))
    st.session_state.data['reg_office'] = st.text_area("Registered Office Address", st.session_state.data.get('reg_office', "Fatehpur"))
    st.session_state.data['works_addr'] = st.text_area("Factory Address", st.session_state.data.get('works_addr', "Haswa"))
    c1, c2 = st.columns(2)
    st.session_state.data['tel'] = c1.text_input("Mobile No.", st.session_state.data.get('tel', "9650329719"))
    st.session_state.data['email'] = c2.text_input("Email", st.session_state.data.get('email', "info.accumentechno@gmail.com"))
    st.button("Save & Next ➡️", on_click=next_step)

elif st.session_state.step == 2:
    st.header("2. Product & Service Categories")
    st.session_state.data['is_dealer'] = st.radio("Business Role", ["Manufacturer", "Authorized Dealer", "Service Provider"])
    st.session_state.data['prod_category'] = st.multiselect("Select Categories", ["Electrical", "Mechanical", "IT", "Marketing", "Civil"], default=["Marketing"])
    st.session_state.data['main_products'] = st.text_area("Detailed Product/Service Description", st.session_state.data.get('main_products', ""))
    col1, col2 = st.columns(2)
    col1.button("⬅️ Back", on_click=prev_step)
    col2.button("Save & Next ➡️", on_click=next_step)

elif st.session_state.step == 3:
    st.header("3. Statutory Registrations")
    c1, c2 = st.columns(2)
    st.session_state.data['pan'] = c1.text_input("PAN NO.", st.session_state.data.get('pan', "BVGPM3310K"))
    st.session_state.data['gst'] = c2.text_input("GST NO.", st.session_state.data.get('gst', "212601"))
    st.session_state.data['msme_no'] = st.text_input("MSME NO.", st.session_state.data.get('msme_no', "8408"))
    st.session_state.data['msme_type'] = st.selectbox("Category", ["Micro", "Small", "Medium"])
    col1, col2 = st.columns(2)
    col1.button("⬅️ Back", on_click=prev_step)
    col2.button("Save & Next ➡️", on_click=next_step)

elif st.session_state.step == 4:
    st.header("4. Manpower & Infrastructure")
    st.session_state.data['commence_year'] = st.text_input("Years in Business", st.session_state.data.get('commence_year', "4"))
    st.session_state.data['area'] = st.number_input("Area (Sq. m.)", value=250)
    st.session_state.data['power'] = st.text_input("Power Load (kVA)", "2")
    m1, m2, m3 = st.columns(3)
    st.session_state.data['grad_staff'] = m1.number_input("Engg Graduates", value=1)
    st.session_state.data['diploma_staff'] = m2.number_input("Diploma Staff", value=3)
    st.session_state.data['skilled_workers'] = m3.number_input("Skilled Workers", value=5)
    col1, col2 = st.columns(2)
    col1.button("⬅️ Back", on_click=prev_step)
    col2.button("Save & Next ➡️", on_click=next_step)

elif st.session_state.step == 5:
    st.header("5. Technical Machinery")
    st.session_state.data['machinery'] = st.text_area("List Machinery/Equipment", st.session_state.data.get('machinery', "LATHE, MILLING"))
    st.session_state.data['inhouse_test'] = st.radio("In-house Testing?", ["Yes", "No"])
    st.session_state.data['outsourced'] = st.text_input("Outsourced Details", "NO")
    col1, col2 = st.columns(2)
    col1.button("⬅️ Back", on_click=prev_step)
    col2.button("Save & Next ➡️", on_click=next_step)

elif st.session_state.step == 6:
    st.header("6. Performance References")
    st.session_state.data['ref_1'] = st.text_input("Client Reference 1", st.session_state.data.get('ref_1', ""))
    st.session_state.data['ref_2'] = st.text_input("Client Reference 2", st.session_state.data.get('ref_2', ""))
    st.session_state.data['govt_exp'] = st.radio("Worked with PSUs?", ["Yes", "No"])
    col1, col2 = st.columns(2)
    col1.button("⬅️ Back", on_click=prev_step)
    col2.button("Save & Next ➡️", on_click=next_step)

elif st.session_state.step == 7:
    st.header("7. Quality & Financials")
    st.session_state.data['iso9001'] = st.selectbox("ISO 9001 Certified?", ["Yes", "No"])
    st.session_state.data['q_manual'] = st.radio("QC Manual Available?", ["Yes", "No"])
    st.session_state.data['turnover_3'] = st.number_input("Latest Turnover (Cr)", value=2.5)
    st.session_state.data['networth'] = st.number_input("Net Worth (Cr)", value=1.0)
    col1, col2 = st.columns(2)
    col1.button("⬅️ Back", on_click=prev_step)
    col2.button("Save & Next ➡️", on_click=next_step)

elif st.session_state.step == 8:
    st.header("8. Final Technical Report")
    score = 0
    if st.session_state.data.get('iso9001') == "Yes": score += 20
    if st.session_state.data.get('inhouse_test') == "Yes": score += 20
    if st.session_state.data.get('q_manual') == "Yes": score += 20
    if st.session_state.data.get('govt_exp') == "Yes": score += 20
    if st.session_state.data.get('turnover_3', 0) > 1.0: score += 20
    st.session_state.data['score'] = score

    try:
        template = env.get_template('full_report.html')
        report_html = template.render(d=st.session_state.data, date=datetime.date.today().strftime("%d %B %Y"))
        st.components.v1.html(report_html, height=2000, scrolling=True)
    except Exception as e:
        st.error(f"Error: {e}")
    if st.button("⬅️ Back to Step 1"): st.session_state.step = 1
