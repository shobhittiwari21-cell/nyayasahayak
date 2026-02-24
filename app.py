import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. CORE SETUP & LAW FIRM BRANDING
# ==========================================
st.set_page_config(
    page_title="Chambers of Adv. Shobhit Tiwari | Allahabad High Court, Lucknow Bench", 
    page_icon="⚖️", 
    layout="centered"
)

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception:
    st.error("System is currently undergoing maintenance. Please try again later.")
    st.stop()

# ==========================================
# 2. PROFESSIONAL HEADER & CHAMBER INFO
# ==========================================
# Sleek, professional law-firm style header using HTML/CSS
st.markdown("""
    <div style='text-align: center; padding: 20px; border-bottom: 2px solid #2c3e50;'>
        <h2 style='color: #2c3e50; font-family: "Georgia", serif; margin-bottom: 0px;'>CHAMBERS OF ADV. SHOBHIT TIWARI</h2>
        <p style='color: #7f8c8d; font-size: 16px; margin-top: 5px;'>Allahabad High Court, Lucknow Bench, Lucknow</p>
        <p style='color: #34495e; font-size: 14px; margin-top: -10px;'>Contact: +91 9795971160 | Litigation & Dispute Resolution</p>
    </div>
""", unsafe_allow_html=True)

st.write("") # Spacer

# Language Toggle
lang = st.radio("Preferred Language / भाषा:", ["English", "Hindi"], horizontal=True)

ui = {
    "English": {"iam": "Access Portal As:", "btn": "Draft Legal Document", "req": "Submit Request"},
    "Hindi": {"iam": "पोर्टल एक्सेस करें:", "btn": "कानूनी ड्राफ्ट तैयार करें", "req": "अनुरोध सबमिट करें"}
}[lang]

# ==========================================
# 3. NAVIGATION (PRACTICE AREAS)
# ==========================================
category = st.pills(ui["iam"], ["Citizen / Client", "Legal Professional"], default="Citizen / Client")

if category == "Legal Professional":
    tool = st.selectbox("Select Legal Tool:", [
        "1. Case Law Summarizer", 
        "2. IPC to BNS Converter", 
        "3. Affidavit Drafter (Lucknow Bench)", 
        "4. Bail Application Writer"
    ])
else:
    tool = st.selectbox("Select Legal Service:", [
        "1. Police Complaint (FIR) Drafter", 
        "2. Section 138 (Cheque Bounce) Notice", 
        "3. UP Commercial/Residential Rent Agreement", 
        "4. Traffic Challan Compounding Application"
    ])

st.divider()

# ==========================================
# 4. TOOL LOGIC & LEGAL DRAFTING
# ==========================================
watermark = f"\n\n---\n**Note:** *This document was generated via the NyayaSahayak portal. It serves as a preliminary draft. For formal court submissions, execution of Vakalatnama, and legal strategy, please schedule a consultation with the Chambers of Adv. Shobhit Tiwari (Allahabad High Court, Lucknow Bench).* \n\n**Contact:** +91 9795971160"

# --- CLIENT TOOLS ---
if tool == "1. Police Complaint (FIR) Drafter":
    st.subheader("Police Complaint (FIR) Drafting Desk")
    if "fir_step" not in st.session_state:
        st.session_state.fir_step = 1

    if st.session_state.fir_step == 1:
        u_story = st.text_area("Provide a detailed account of the incident:", height=120)
        if st.button("Analyze Legal Grounds"):
            if u_story:
                with st.spinner("Reviewing incident against BNS provisions..."):
                    q_prompt = f"Role: Senior Legal Counsel in UP. Read: '{u_story}'. Ask 3 formal questions in {lang} to gather missing facts required for a robust BNS FIR."
                    st.session_state.fir_qs = model.generate_content(q_prompt).text
                    st.session_state.fir_story = u_story
                    st.session_state.fir_step = 2
                    st.rerun()
    elif st.session_state.fir_step == 2:
        st.info(st.session_state.fir_qs)
        u_answers = st.text_area("Provide Clarifications:")
        if st.button(ui["btn"]):
            with st.spinner("Drafting official complaint..."):
                prompt = f"Role: Expert Criminal Lawyer at Allahabad High Court. Draft a formal FIR. Story: {st.session_state.fir_story}. Clarifications: {u_answers}. Apply BNS 2023. Language: {lang}."
                st.write(model.generate_content(prompt).text + watermark)
        if st.button("Reset Form"):
            st.session_state.fir_step = 1
            st.rerun()

elif tool == "2. Section 138 (Cheque Bounce) Notice":
    st.subheader("Section 138 NI Act Notice")
    details = st.text_area("Provide Details (Sender, Defaulter, Cheque Number, Date, Amount):", height=120)
    if st.button(ui["btn"]):
        with st.spinner("Drafting Legal Notice..."):
            prompt = f"Role: Corporate Lawyer in India. Draft a formal statutory notice under Section 138 of the Negotiable Instruments Act using: {details}. Ensure the mandatory 15-day statutory period is clearly stated. Language: {lang}."
            st.write(model.generate_content(prompt).text + watermark)

elif tool == "3. UP Commercial/Residential Rent Agreement":
    st.subheader("Tenancy & Lease Agreement (UP)")
    details = st.text_area("Provide Details (Lessor, Lessee, Monthly Rent, Security Deposit, Property Address):", height=120)
    if st.button(ui["btn"]):
        with st.spinner("Drafting Agreement..."):
            prompt = f"Role: Civil Litigation Lawyer in UP. Draft an 11-month Rent Agreement using: {details}. Include standard indemnity, lock-in, and eviction clauses as per UP tenancy laws. Language: {lang}."
            st.write(model.generate_content(prompt).text + watermark)

elif tool == "4. Traffic Challan Compounding Application":
    st.subheader("Traffic Challan Compounding Request")
    details = st.text_area("Provide Details (Vehicle Registration, Challan Number, Offense, Grounds for Waiver):", height=120)
    if st.button(ui["btn"]):
        with st.spinner("Drafting Application..."):
            prompt = f"Role: Practicing Advocate in Lucknow. Draft a formal application to the Traffic Magistrate or Lok Adalat requesting compounding or waiver of the challan using: {details}. Language: {lang}."
            st.write(model.generate_content(prompt).text + watermark)

# --- PROFESSIONAL TOOLS ---
elif tool == "1. Case Law Summarizer":
    st.subheader("Appellate Judgment Summarizer")
    judgment = st.text_area("Paste Judgment Text:", height=200)
    if st.button(ui["btn"]):
        with st.spinner("Analyzing Ratio Decidendi..."):
            prompt = f"Role: Judicial Clerk. Summarize this judgment into 5 concise legal points: Core Issue, Key Facts, Ratio Decidendi, Cited Precedents, Final Order. Language: {lang}. Text: {judgment}"
            st.info(model.generate_content(prompt).text)

elif tool == "2. IPC to BNS Converter":
    st.subheader("Statute Converter: IPC to BNS")
    sec = st.text_input("Enter IPC Section / Offense Name:")
    if st.button(ui["btn"]):
        prompt = f"Map IPC {sec} to the corresponding Bharatiya Nyaya Sanhita (BNS) 2023 section. Provide a brief legal explanation in {lang}."
        st.success(model.generate_content(prompt).text)

elif tool == "3. Affidavit Drafter (Lucknow Bench)":
    st.subheader("Affidavit Drafting Desk (Lucknow Bench)")
    details = st.text_area("Provide Details (Case Details, Deponent Name/Age/Address, Material Facts):", height=120)
    if st.button(ui["btn"]):
        with st.spinner("Formatting Affidavit..."):
            prompt = f"Role: High Court Counsel. Draft a formal Counter-Affidavit strictly adhering to the drafting conventions of the Allahabad High Court, Lucknow Bench. Details: {details}. Language: {lang}."
            st.write(model.generate_content(prompt).text + watermark)

elif tool == "4. Bail Application Writer":
    st.subheader("Bail Application Drafting Desk")
    details = st.text_area("Provide Details (FIR Number, Police Station, Applied BNS Sections, Legal Grounds for Bail):", height=120)
    if st.button(ui["btn"]):
        with st.spinner("Structuring Bail Arguments..."):
            prompt = f"Role: Criminal Defense Advocate in UP. Draft a bail application under Section 483 BNSS using: {details}. Address to the Ld. District & Sessions Judge. Include standard conditions in the prayer. Language: {lang}."
            st.write(model.generate_content(prompt).text + watermark)

st.divider()

# ==========================================
# 5. CLIENT INTAKE & CONSULTATION
# ==========================================
st.markdown("### Schedule a Consultation")
st.write("For formal representation at the Allahabad High Court, Lucknow Bench, please submit your case details below.")

with st.form("intake_form", clear_on_submit=True):
    client_name = st.text_input("Full Name:")
    client_phone = st.text_input("Contact Number:")
    client_issue = st.selectbox("Matter Type:", ["Criminal Litigation / Bail", "Civil & Property Disputes", "Commercial & Arbitration", "Matrimonial Disputes", "Other Legal Matters"])
    
    submitted = st.form_submit_button(ui["req"])
    if submitted:
        if client_name and client_phone:
            st.success(f"Request Received. The Chambers of Adv. Shobhit Tiwari will contact {client_name} at {client_phone} regarding this matter.")
        else:
            st.error("Please provide both your name and contact number.")

# ==========================================
# 6. FEEDBACK
# ==========================================
with st.expander("Submit Feedback / Suggestion"):
    with st.form("feedback_form", clear_on_submit=True):
        feedback = st.text_area("Please describe any additional legal tools that would be beneficial:")
        fb_submitted = st.form_submit_button("Submit")
        if fb_submitted:
            st.success("Thank you for your feedback.")

# ==========================================
# 7. SEO & LEGAL FOOTER
# ==========================================
st.divider()
st.markdown("""
<div style='text-align: justify; font-size: 11px; color: gray;'>
    <b>Confidentiality Notice:</b> The information provided on this portal is for preliminary drafting and educational assistance only. It does not establish an attorney-client relationship. All formal legal actions should be pursued only after consulting a registered legal practitioner.<br><br>
    <b>Practice Areas:</b> Criminal Defense, Civil Litigation, Arbitration, Property Law, Corporate Disputes. Serving clients at the Allahabad High Court, Lucknow Bench, Lucknow, and District Courts across Uttar Pradesh.<br>
    © 2026 Chambers of Adv. Shobhit Tiwari. All Rights Reserved.
</div>
""", unsafe_allow_html=True)
