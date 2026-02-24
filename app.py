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
st.markdown("""
    <div style='text-align: center; padding: 20px; border-bottom: 2px solid #2c3e50;'>
        <h2 style='color: #2c3e50; font-family: "Georgia", serif; margin-bottom: 0px;'>CHAMBERS OF ADV. SHOBHIT TIWARI</h2>
        <p style='color: #7f8c8d; font-size: 16px; margin-top: 5px;'>Allahabad High Court, Lucknow Bench, Lucknow</p>
        <p style='color: #34495e; font-size: 14px; margin-top: -10px;'>Contact: +91 9795971160 | Litigation & Dispute Resolution</p>
    </div>
""", unsafe_allow_html=True)
st.write("")

# Language Toggle
lang = st.radio("Preferred Language / भाषा चुनें:", ["English", "Hindi"], horizontal=True)

# ==========================================
# 3. MASTER TRANSLATION DICTIONARY
# ==========================================
en = {
    "cat_cit": "Citizen / Client", "cat_adv": "Legal Professional",
    "t_cit": ["1. Police Complaint (FIR)", "2. Section 138 (Cheque Bounce) Notice", "3. Tenancy/Rent Agreement (UP)", "4. Traffic Challan Compounding"],
    "t_adv": ["1. Case Law Summarizer", "2. IPC to BNS Converter", "3. Affidavit Drafter (Lucknow Bench)", "4. Bail Application Writer"],
    "btn_draft": "Draft Legal Document", "btn_analyze": "Analyze Legal Grounds", "btn_reset": "Reset Form", "req": "Submit Request",
    "fir_h": "Police Complaint (FIR) Drafting Desk", "fir_1": "Provide a detailed account of the incident:", "fir_2": "Provide Clarifications:",
    "cb_h": "Section 138 NI Act Notice", "cb_1": "Provide Details (Sender, Defaulter, Cheque No., Date, Amount):",
    "ra_h": "Tenancy & Lease Agreement (UP)", "ra_1": "Provide Details (Lessor, Lessee, Rent ₹, Security Deposit ₹, Address):",
    "tc_h": "Traffic Challan Compounding Request", "tc_1": "Provide Details (Vehicle Reg, Challan No., Offense, Grounds for Waiver):",
    "cs_h": "Appellate Judgment Summarizer", "cs_1": "Paste Judgment Text:",
    "ipc_h": "Statute Converter: IPC to BNS", "ipc_1": "Enter IPC Section / Offense Name:",
    "aff_h": "Affidavit Drafting Desk (Lucknow Bench)", "aff_1": "Provide Details (Case Title, Deponent Name/Age/Address, Material Facts):",
    "bail_h": "Bail Application Drafting Desk", "bail_1": "Provide Details (FIR No., Police Station, Applied BNS Sections, Grounds for Bail):",
    "intake_h": "### Schedule a Consultation", "intake_sub": "For formal representation at the Allahabad High Court, Lucknow Bench, please submit your case details below.",
    "i_name": "Full Name:", "i_phone": "Contact Number:", "i_issue": "Matter Type:", "i_options": ["Criminal Litigation / Bail", "Civil & Property Disputes", "Commercial & Arbitration", "Matrimonial Disputes", "Other Legal Matters"],
    "fb_h": "Submit Feedback / Suggestion", "fb_1": "Please describe any additional legal tools that would be beneficial:"
}

hi = {
    "cat_cit": "नागरिक / मुवक्किल (Client)", "cat_adv": "वकील / कानूनी पेशेवर",
    "t_cit": ["1. पुलिस शिकायत (FIR) ड्राफ्टर", "2. धारा 138 (चेक बाउंस) नोटिस", "3. किरायानामा (रेंट एग्रीमेंट) - यूपी", "4. ट्रैफिक चालान छूट आवेदन"],
    "t_adv": ["1. अपीलीय निर्णय (Judgment) सारांश", "2. IPC से BNS कनवर्टर", "3. हलफनामा (Affidavit) ड्राफ्टर", "4. जमानत (Bail) आवेदन"],
    "btn_draft": "कानूनी ड्राफ्ट तैयार करें", "btn_analyze": "कानूनी आधार का विश्लेषण करें", "btn_reset": "फॉर्म रीसेट करें", "req": "अनुरोध सबमिट करें",
    "fir_h": "पुलिस शिकायत (FIR) ड्राफ्टिंग डेस्क", "fir_1": "घटना का विस्तृत विवरण दें:", "fir_2": "स्पष्टीकरण (Clarifications) दें:",
    "cb_h": "धारा 138 (चेक बाउंस) नोटिस", "cb_1": "विवरण दें (प्रेषक, डिफाल्टर, चेक नंबर, तिथि, राशि):",
    "ra_h": "किरायानामा (रेंट एग्रीमेंट) - यूपी", "ra_1": "विवरण दें (मकान मालिक, किरायेदार, मासिक किराया, जमा राशि, पता):",
    "tc_h": "ट्रैफिक चालान छूट/माफी आवेदन", "tc_1": "विवरण दें (गाड़ी नंबर, चालान नंबर, अपराध, छूट का कारण):",
    "cs_h": "अपीलीय निर्णय (Judgment) सारांश", "cs_1": "जजमेंट का टेक्स्ट पेस्ट करें:",
    "ipc_h": "कानून कनवर्टर: IPC से BNS", "ipc_1": "IPC की धारा या अपराध का नाम लिखें:",
    "aff_h": "हलफनामा (Affidavit) ड्राफ्टिंग डेस्क", "aff_1": "विवरण दें (केस का विवरण, शपथकर्ता का नाम/उम्र/पता, मुख्य तथ्य):",
    "bail_h": "जमानत (Bail) आवेदन ड्राफ्टिंग डेस्क", "bail_1": "विवरण दें (FIR नंबर, थाना, BNS धाराएं, जमानत का आधार):",
    "intake_h": "### परामर्श (Consultation) बुक करें", "intake_sub": "इलाहाबाद उच्च न्यायालय, लखनऊ खंडपीठ में कानूनी प्रतिनिधित्व के लिए, कृपया अपने केस का विवरण नीचे सबमिट करें।",
    "i_name": "पूरा नाम:", "i_phone": "संपर्क नंबर (WhatsApp):", "i_issue": "मामले का प्रकार:", "i_options": ["आपराधिक / जमानत", "दीवानी / संपत्ति विवाद", "वाणिज्यिक / चेक बाउंस", "पारिवारिक / तलाक", "अन्य कानूनी मामले"],
    "fb_h": "फीडबैक / सुझाव दें", "fb_1": "कृपया बताएं कि आपको और कौन से कानूनी टूल चाहिए:"
}

ui = en if lang == "English" else hi

# ==========================================
# 4. NAVIGATION (INDEX BASED)
# ==========================================
category = st.pills("Access Portal / पोर्टल एक्सेस करें:", [ui["cat_cit"], ui["cat_adv"]], default=ui["cat_cit"])

if category == ui["cat_cit"]:
    tool = st.selectbox("Select Service:", ui["t_cit"])
    tool_idx = ui["t_cit"].index(tool)
    is_citizen = True
else:
    tool = st.selectbox("Select Service:", ui["t_adv"])
    tool_idx = ui["t_adv"].index(tool)
    is_citizen = False

st.divider()

# ==========================================
# 5. TOOL LOGIC
# ==========================================
watermark = f"\n\n---\n**Note:** *This document was generated via the NyayaSahayak portal. It serves as a preliminary draft. For formal court submissions, execution of Vakalatnama, and legal strategy, please schedule a consultation with the Chambers of Adv. Shobhit Tiwari (Allahabad High Court, Lucknow Bench, Lucknow).* \n\n**Contact:** +91 9795971160"

if is_citizen:
    # 1. FIR Drafter
    if tool_idx == 0:
        st.subheader(ui["fir_h"])
        if "fir_step" not in st.session_state:
            st.session_state.fir_step = 1

        if st.session_state.fir_step == 1:
            u_story = st.text_area(ui["fir_1"], height=120)
            if st.button(ui["btn_analyze"]):
                if u_story:
                    with st.spinner("Reviewing incident against BNS provisions..."):
                        q_prompt = f"Role: Senior Legal Counsel in UP. Read: '{u_story}'. Ask 3 formal questions in {lang} to gather missing facts required for a robust BNS FIR."
                        st.session_state.fir_qs = model.generate_content(q_prompt).text
                        st.session_state.fir_story = u_story
                        st.session_state.fir_step = 2
                        st.rerun()
        elif st.session_state.fir_step == 2:
            st.info(st.session_state.fir_qs)
            u_answers = st.text_area(ui["fir_2"])
            if st.button(ui["btn_draft"]):
                with st.spinner("Drafting official complaint..."):
                    prompt = f"Role: Expert Criminal Lawyer at Allahabad High Court. Draft a formal FIR. Story: {st.session_state.fir_story}. Clarifications: {u_answers}. Apply BNS 2023. Language: {lang}."
                    st.write(model.generate_content(prompt).text + watermark)
            if st.button(ui["btn_reset"]):
                st.session_state.fir_step = 1
                st.rerun()

    # 2. Cheque Bounce
    elif tool_idx == 1:
        st.subheader(ui["cb_h"])
        details = st.text_area(ui["cb_1"], height=120)
        if st.button(ui["btn_draft"]):
            with st.spinner("Drafting Legal Notice..."):
                prompt = f"Role: Corporate Lawyer in India. Draft a formal statutory notice under Section 138 of the Negotiable Instruments Act using: {details}. Ensure the mandatory 15-day statutory period is clearly stated. Language: {lang}."
                st.write(model.generate_content(prompt).text + watermark)

    # 3. Rent Agreement
    elif tool_idx == 2:
        st.subheader(ui["ra_h"])
        details = st.text_area(ui["ra_1"], height=120)
        if st.button(ui["btn_draft"]):
            with st.spinner("Drafting Agreement..."):
                prompt = f"Role: Civil Litigation Lawyer in UP. Draft an 11-month Rent Agreement using: {details}. Include standard indemnity, lock-in, and eviction clauses as per UP tenancy laws. Language: {lang}."
                st.write(model.generate_content(prompt).text + watermark)

    # 4. Traffic Challan
    elif tool_idx == 3:
        st.subheader(ui["tc_h"])
        details = st.text_area(ui["tc_1"], height=120)
        if st.button(ui["btn_draft"]):
            with st.spinner("Drafting Application..."):
                prompt = f"Role: Practicing Advocate in Lucknow. Draft a formal application to the Traffic Magistrate or Lok Adalat requesting compounding or waiver of the challan using: {details}. Language: {lang}."
                st.write(model.generate_content(prompt).text + watermark)

else:
    # 1. Case Summarizer
    if tool_idx == 0:
        st.subheader(ui["cs_h"])
        judgment = st.text_area(ui["cs_1"], height=200)
        if st.button(ui["btn_draft"]):
            with st.spinner("Analyzing Ratio Decidendi..."):
                prompt = f"Role: Judicial Clerk. Summarize this judgment into 5 concise legal points: Core Issue, Key Facts, Ratio Decidendi, Cited Precedents, Final Order. Language: {lang}. Text: {judgment}"
                st.info(model.generate_content(prompt).text)

    # 2. IPC to BNS
    elif tool_idx == 1:
        st.subheader(ui["ipc_h"])
        sec = st.text_input(ui["ipc_1"])
        if st.button(ui["btn_draft"]):
            prompt = f"Map IPC {sec} to the corresponding Bharatiya Nyaya Sanhita (BNS) 2023 section. Provide a brief legal explanation in {lang}."
            st.success(model.generate_content(prompt).text)

    # 3. Affidavit Drafter
    elif tool_idx == 2:
        st.subheader(ui["aff_h"])
        details = st.text_area(ui["aff_1"], height=120)
        if st.button(ui["btn_draft"]):
            with st.spinner("Formatting Affidavit..."):
                prompt = f"Role: High Court Counsel. Draft a formal Counter-Affidavit strictly adhering to the drafting conventions of the Allahabad High Court, Lucknow Bench. Details: {details}. Language: {lang}."
                st.write(model.generate_content(prompt).text + watermark)

    # 4. Bail Writer
    elif tool_idx == 3:
        st.subheader(ui["bail_h"])
        details = st.text_area(ui["bail_1"], height=120)
        if st.button(ui["btn_draft"]):
            with st.spinner("Structuring Bail Arguments..."):
                prompt = f"Role: Criminal Defense Advocate in UP. Draft a bail application under Section 483 BNSS using: {details}. Address to the Ld. District & Sessions Judge. Include standard conditions in the prayer. Language: {lang}."
                st.write(model.generate_content(prompt).text + watermark)

st.divider()

# ==========================================
# 6. CLIENT INTAKE & CONSULTATION
# ==========================================
st.markdown(ui["intake_h"])
st.write(ui["intake_sub"])

with st.form("intake_form", clear_on_submit=True):
    client_name = st.text_input(ui["i_name"])
    client_phone = st.text_input(ui["i_phone"])
    client_issue = st.selectbox(ui["i_issue"], ui["i_options"])
    
    submitted = st.form_submit_button(ui["req"])
    if submitted:
        if client_name and client_phone:
            # Bilingual success message
            success_msg = f"Request Received. The Chambers of Adv. Shobhit Tiwari will contact {client_name} at {client_phone} regarding this matter." if lang == "English" else f"अनुरोध प्राप्त हुआ। अधिवक्ता शोभित तिवारी का कार्यालय जल्द ही {client_phone} पर {client_name} से संपर्क करेगा।"
            st.success(success_msg)
        else:
            error_msg = "Please provide both your name and contact number." if lang == "English" else "कृपया अपना नाम और संपर्क नंबर दोनों प्रदान करें।"
            st.error(error_msg)

# ==========================================
# 7. FEEDBACK
# ==========================================
with st.expander(ui["fb_h"]):
    with st.form("feedback_form", clear_on_submit=True):
        feedback = st.text_area(ui["fb_1"])
        fb_submitted = st.form_submit_button(ui["req"])
        if fb_submitted:
            msg = "Thank you for your feedback." if lang == "English" else "आपके सुझाव के लिए धन्यवाद।"
            st.success(msg)

# ==========================================
# 8. SEO & LEGAL FOOTER
# ==========================================
st.divider()
st.markdown("""
<div style='text-align: justify; font-size: 11px; color: gray;'>
    <b>Confidentiality Notice:</b> The information provided on this portal is for preliminary drafting and educational assistance only. It does not establish an attorney-client relationship. All formal legal actions should be pursued only after consulting a registered legal practitioner.<br><br>
    <b>Practice Areas:</b> Criminal Defense, Civil Litigation, Arbitration, Property Law, Corporate Disputes. Serving clients at the Allahabad High Court, Lucknow Bench, Lucknow, and District Courts across Uttar Pradesh.<br>
    © 2026 Chambers of Adv. Shobhit Tiwari. All Rights Reserved.
</div>
""", unsafe_allow_html=True)
