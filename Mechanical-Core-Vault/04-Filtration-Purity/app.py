import streamlit as st
import math
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="ASCF SME Calculator", page_icon="🌀", layout="wide")

# --- CUSTOM CSS FOR PROFESSIONAL BRANDING ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .footer { position: fixed; bottom: 0; width: 100%; text-align: center; color: gray; padding: 10px; background: white; }
    .report-box { border: 2px solid #1f77b4; padding: 20px; border-radius: 10px; background-color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER WITH HTML/CSS ---
st.markdown("""
    <div style="background-color:#1f77b4;padding:20px;border-radius:10px">
    <h1 style="color:white;text-align:center;margin:0;">ASCF General Filter Design Tool</h1>
    <p style="color:white;text-align:center;font-size:18px;margin:5px;">Industrial & EPC Consultant | 14+ Yrs India-Gulf Experience</p>
    </div>
    """, unsafe_allow_html=True)

st.write("") # Spacing

# --- SIDEBAR: INPUTS ---
st.sidebar.header("🛠️ Design Parameters")
u_unit = st.sidebar.radio("Unit System", ["Metric (mm)", "Imperial (inch)"])
mult = 25.4 if u_unit == "Imperial (inch)" else 1.0

od = st.sidebar.number_input(f"Outer Diameter ({u_unit})", value=100.0)
length = st.sidebar.number_input(f"Element Length ({u_unit})", value=500.0)
n_pleats = st.sidebar.number_input("Number of Pleats", value=65)
p_depth = st.sidebar.slider(f"Pleat Depth ({u_unit})", 5.0, 50.0, 15.0)

st.sidebar.divider()
st.sidebar.header("🌊 Process Conditions")
fluid_type = st.sidebar.selectbox("Fluid Type", ["Water", "Lube Oil", "Fuel", "Chemical"])
flux_map = {"Water": 12, "Lube Oil": 3, "Fuel": 8, "Chemical": 6}
design_flux = flux_map[fluid_type]

# --- SME CALCULATION ENGINE ---
area_mm2 = n_pleats * 2 * p_depth * length
area_m2 = area_mm2 / 1_000_000
capacity = area_m2 * design_flux
circumference = math.pi * od
pitch = circumference / n_pleats if n_pleats > 0 else 0

# --- MAIN DASHBOARD ---
st.subheader("📊 Technical Summary")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Effective Area", f"{area_m2:.3f} m²")
c2.metric("Flow Capacity", f"{capacity:.2f} m³/h")
c3.metric("Pleat Pitch", f"{pitch:.2f} mm")
c4.metric("Fluid Type", fluid_type)



# --- SME VALIDATION LOGIC ---
st.markdown("### 🛠️ SME Compliance Check")
status = "APPROVED"
remarks = "Design conforms to SME manufacturing standards."

if pitch < 1.5:
    status = "REJECTED"
    remarks = f"CRITICAL: Pleat pitch ({pitch:.2f}mm) is too tight. Risk of bridge-over and poor backwash cleaning."
    st.error(f"❌ **{status}**: {remarks}")
elif p_depth > (od / 3):
    status = "WARNING"
    remarks = f"WARNING: Pleat depth ({p_depth}mm) is excessive for {od}mm OD. Check for internal core clearance."
    st.warning(f"⚠️ **{status}**: {remarks}")
else:
    st.success(f"✅ **{status}**: {remarks}")

# --- DETAILED TECHNICAL REPORT GENERATION ---
report_text = f"""==================================================
        ENGINEERING TECHNICAL DATA SHEET
==================================================
Project Ref: ASCF-AUTO-GEN
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Consultant: Syed Hilaluddin Madany
Experience: 14+ Years (EPC & Industrial O&M)
--------------------------------------------------
PHYSICAL SPECIFICATIONS:
- Outer Diameter:  {od} {u_unit}
- Element Length:  {length} {u_unit}
- Pleat Count:     {n_pleats} Nos
- Pleat Depth:     {p_depth} {u_unit}
--------------------------------------------------
CALCULATED DATA:
- Gross Filtration Area: {area_m2:.4f} m2
- Design Flux:           {design_flux} m3/h/m2 ({fluid_type})
- Max Flow Capacity:     {capacity:.2f} m3/hr
- Calculated Pitch:      {pitch:.2f} mm
--------------------------------------------------
COMPLIANCE STATUS: {status}
SME Remarks: {remarks}
--------------------------------------------------
Disclaimer: Calculation based on standard SME logic. 
Verification by site engineer recommended.
=================================================="""

with st.expander("📄 Preview Technical Report"):
    st.code(report_text)

st.download_button(
    label="📥 Download Official Technical Report",
    data=report_text,
    file_name=f"SME_Report_{od}x{length}.txt",
    mime="text/plain"
)

# --- FOOTER ---
st.markdown("""
    <div class="footer">
    <p>#NoToRacism | #AskAndWeSolve | Industrial & EPC Consultant Portfolio</p>
    </div>
    """, unsafe_allow_html=True)
