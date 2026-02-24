import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. CORE SETUP & PLATFORM BRANDING
# ==========================================
st.set_page_config(page_title="NyayaSahayak | India's Free AI Legal Assistant", page_icon="⚖️", layout="centered")

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception:
    st.error("System is currently undergoing maintenance. Please try again later.")
    st.stop()

st.markdown("""
    <div style='text-align: center; padding: 15px;'>
        <h1 style='color: #2c3e50; font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; margin-bottom: 0px;'>⚖️ NyayaSahayak</h1>
        <h4 style='color: #34495e; font-weight: 400; margin-top: 5px;'>India's Premium AI Legal Assistant</h4>
    </div>
""", unsafe_allow_html=True)

st.info("**Powered by the Chambers of Adv. Shobhit Tiwari** \nAllahabad High Court (Lucknow Bench), District Courts & Tribunals | 📞 +91 9795971160")

ui_lang = st.radio("Interface Language / इंटरफ़ेस भाषा:", ["English", "Hindi"], horizontal=True)

# ==========================================
# 2. MASTER TRANSLATION DICTIONARY
# ==========================================
en = {
    "tabs": ["Citizen / Public", "Legal Professional", "Partner Advocate Program"],
    "desks": {
        "citizen": ["🚨 Criminal & Police", "💻 Cyber Crime & Fraud", "🏠 Property & Civil", "💼 Corporate & Money", "🏛️ Government & Employment", "🚦 General & Motor Vehicle"],
        "advocate": ["📝 Legal Drafting Desk", "📚 Research & Statutes"]
    },
    "tools": {
        "🚨 Criminal & Police": ["Police Complaint (FIR) Drafter"],
        "💻 Cyber Crime & Fraud": ["1930 Cyber Fraud Complaint", "Bank Account Unfreeze Application"],
        "🏠 Property & Civil": ["Tenancy/Rent Agreement (UP)", "Tenant Eviction Notice"],
        "💼 Corporate & Money": ["Section 138 (Cheque Bounce) Notice", "MSME Payment Recovery Notice"],
        "🏛️ Government & Employment": ["Show Cause Notice Reply"],
        "🚦 General & Motor Vehicle": ["Traffic Challan Compounding Request"],
        "📝 Legal Drafting Desk": ["Bail Application Drafter", "Affidavit Drafter (Lucknow Bench)", "Writ Petition Grounds (Art. 226)"],
        "📚 Research & Statutes": ["Case Law Summarizer", "IPC to BNS Converter"]
    },
    "btn_analyze": "Analyze & Ask Clarifications 🔍", "btn_draft": "Generate Final Draft 📄", "btn_reset": "Start Over 🔄", "req": "Request Consultation"
}

hi = {
    "tabs": ["नागरिक / आम जनता", "वकील / कानूनी पेशेवर", "पार्टनर एडवोकेट प्रोग्राम"],
    "desks": {
        "citizen": ["🚨 आपराधिक और पुलिस", "💻 साइबर अपराध और धोखाधड़ी", "🏠 संपत्ति और दीवानी", "💼 वाणिज्यिक और धन", "🏛️ सरकारी और रोजगार", "🚦 सामान्य और मोटर वाहन"],
        "advocate": ["📝 कानूनी ड्राफ्टिंग डेस्क", "📚 अनुसंधान और कानून"]
    },
    "tools": {
        "🚨 आपराधिक और पुलिस": ["पुलिस शिकायत (FIR) ड्राफ्टर"],
        "💻 साइबर अपराध और धोखाधड़ी": ["1930 साइबर धोखाधड़ी शिकायत", "बैंक खाता अनफ्रीज आवेदन"],
        "🏠 संपत्ति और दीवानी": ["किरायानामा (रेंट एग्रीमेंट) - यूपी", "किरायेदार बेदखली (Eviction) नोटिस"],
        "💼 वाणिज्यिक और धन": ["धारा 138 (चेक बाउंस) नोटिस", "MSME भुगतान वसूली नोटिस"],
        "🏛️ सरकारी और रोजगार": ["कारण बताओ (Show Cause) नोटिस का जवाब"],
        "🚦 सामान्य और मोटर वाहन": ["ट्रैफिक चालान छूट/माफी आवेदन"],
        "📝 कानूनी ड्राफ्टिंग डेस्क": ["जमानत (Bail) आवेदन ड्राफ्टर", "हलफनामा (Affidavit) ड्राफ्टर", "रिट याचिका के आधार (Art. 226)"],
        "📚 अनुसंधान और कानून": ["अपीलीय निर्णय (Judgment) सारांश", "कानून कनवर्टर: IPC से BNS"]
    },
    "btn_analyze": "विश्लेषण करें और प्रश्न पूछें 🔍", "btn_draft": "अंतिम ड्राफ्ट तैयार करें 📄", "btn_reset": "शुरुआत से शुरू करें 🔄", "req": "परामर्श का अनुरोध करें"
}

ui = en if ui_lang == "English" else hi

# ==========================================
# 3. THE PROMPT VAULT (Centralized AI Brain)
# ==========================================
PROMPT_VAULT = {
    "Police Complaint (FIR) Drafter": {
        "info": "Draft a formal Police Complaint under the BNS 2023.", "init": "Describe the incident roughly / घटना का विवरण दें:",
        "qr": "Veteran Police IO in UP", "qt": "Identify missing facts for a BNS 2023 FIR (time, weapons, witnesses).",
        "dr": "Elite Criminal Defense Counsel", "dt": "Draft a formal FIR to the SHO.", "dc": "Apply BNS 2023. Do not invent fake facts. Use objective legal prose."
    },
    "1930 Cyber Fraud Complaint": {
        "info": "Draft a chronological complaint for the National Cyber Crime Reporting Portal (1930).", "init": "How were you scammed? / आपके साथ धोखाधड़ी कैसे हुई?:",
        "qr": "Cyber Crime Investigator", "qt": "Identify missing financial facts (UTR numbers, transaction times, bank names).",
        "dr": "Cyber Law Expert", "dt": "Draft a highly technical, chronological cyber fraud complaint.", "dc": "Include all technical transaction details clearly for cyber cell ingestion."
    },
    "Bank Account Unfreeze Application": {
        "info": "Draft an application under Sec 457 CrPC / 503 BNSS to de-freeze a bank account.", "init": "Why was your account frozen? / आपका खाता फ्रीज क्यों हुआ?:",
        "qr": "Economic Offences Lawyer", "qt": "Identify missing facts (date of freeze, bank name, investigating agency, transaction link).",
        "dr": "Criminal Trial Advocate", "dt": "Draft an application to the Magistrate for de-freezing a bank account.", "dc": "Assert innocence in chain transactions. Cite BNSS provisions."
    },
    "Tenancy/Rent Agreement (UP)": {
        "info": "Create a legally binding 11-month residential or commercial rent agreement.", "init": "Provide Details (Names, Rent, Deposit) / विवरण दें:",
        "qr": "Civil Real Estate Lawyer in UP", "qt": "Identify missing lease terms (address, lock-in period, notice period).",
        "dr": "Civil Real Estate Lawyer in UP", "dt": "Draft an 11-month Lease Agreement.", "dc": "Adhere to UP tenancy laws. Include lock-in, notice, and anti-subletting clauses."
    },
    "Tenant Eviction Notice": {
        "info": "Draft a strict 30-day statutory notice for a tenant to vacate premises.", "init": "Why are you evicting them? / आप उन्हें बेदखल क्यों कर रहे हैं?:",
        "qr": "Property Dispute Advocate", "qt": "Identify missing eviction grounds (months of default, specific damages).",
        "dr": "Property Dispute Advocate", "dt": "Draft a strict 30-day statutory eviction notice.", "dc": "Cite UP Rent Control laws. Demand vacating to avoid civil suit and mesne profits."
    },
    "Section 138 (Cheque Bounce) Notice": {
        "info": "Generate a strict 15-day statutory legal notice for a dishonored cheque.", "init": "Provide Cheque Details (Amount, Names) / चेक का विवरण दें:",
        "qr": "Corporate Litigator", "qt": "Identify missing NI Act requirements (cheque date, return memo date, bounce reason).",
        "dr": "Corporate Litigator", "dt": "Draft Sec 138 NI Act notice.", "dc": "Tone must be stern. Explicitly state the 15-day statutory warning for criminal proceedings."
    },
    "MSME Payment Recovery Notice": {
        "info": "Draft a strong payment recovery notice referencing MSME Samadhaan.", "init": "Who owes you money? / आप पर किसका पैसा बकाया है?:",
        "qr": "Corporate Advocate", "qt": "Identify missing MSME facts (Udyam Registration number, invoice dates, amount).",
        "dr": "Corporate Advocate", "dt": "Draft MSME payment recovery notice.", "dc": "Invoke MSMED Act 2006 (compound interest). Set a strict 15-day deadline before legal action."
    },
    "Show Cause Notice Reply": {
        "info": "Draft a respectful but legally defensive reply to a disciplinary notice.", "init": "What are the charges against you? / आप पर क्या आरोप हैं?:",
        "qr": "Service Law Advocate", "qt": "Identify missing disciplinary facts (date of notice, specific charges, user's defense).",
        "dr": "Service Law Advocate", "dt": "Draft a formal reply to a Show Cause Notice.", "dc": "Tone should be respectful but legally defensive. Invoke principles of natural justice."
    },
    "Traffic Challan Compounding Request": {
        "info": "Generate an application to the Traffic Magistrate to request waiver of an e-challan.", "init": "Provide challan details (Vehicle No., Offense) / चालान का विवरण दें:",
        "qr": "Traffic Court Advocate", "qt": "Identify missing compounding facts (challan number, compelling reason/hardship for waiver).",
        "dr": "Traffic Court Advocate", "dt": "Draft compounding/waiver application.", "dc": "Address to Traffic Magistrate/Lok Adalat. Tone should be respectful and request leniency."
    },
    "Bail Application Drafter": {
        "info": "Draft a comprehensive regular bail application under Section 483 of the BNSS.", "init": "Provide basic FIR Details & Sections:",
        "qr": "Senior Criminal Defense Advocate", "qt": "Identify missing bail grounds (date of arrest, applicant's specific role, parity).",
        "dr": "Top-tier Criminal Defense Advocate", "dt": "Draft Regular Bail App under Sec 483 BNSS.", "dc": "Address to District & Sessions Judge. Argue the 'Triple Test'. Demand parity if applicable."
    },
    "Affidavit Drafter (Lucknow Bench)": {
        "info": "Generate Counter-Affidavits adhering to the formatting of the Lucknow Bench.", "init": "Provide Case Title and brief subject matter:",
        "qr": "High Court Counsel", "qt": "Identify missing facts for the affidavit (Deponent details, para-wise rebuttals).",
        "dr": "High Court Counsel", "dt": "Draft Counter-Affidavit.", "dc": "Adhere strictly to archaic legal phrasing of the Allahabad High Court, Lucknow Bench. Use numbered paragraphs."
    },
    "Writ Petition Grounds (Art. 226)": {
        "info": "Draft specific constitutional grounds for a Writ Petition in Service/Administrative Matters.", "init": "Provide details of the wrongful government action:",
        "qr": "High Court Service Law Counsel", "qt": "Identify missing constitutional grounds (fundamental rights breached, exact impugned order).",
        "dr": "High Court Counsel", "dt": "Draft the 'Grounds' section for an Article 226 Writ Petition.", "dc": "Focus on arbitrary state action, violation of Article 14/16/21, and Wednesbury unreasonableness."
    }
}

# ==========================================
# 4. THE ELITE ENGINE
# ==========================================
watermark = f"\n\n---\n**Important Disclaimer:** *This preliminary document was generated by NyayaSahayak AI. It does not constitute formal legal advice. For official court submissions, tribunal representation, and strategic legal execution, please consult Adv. Shobhit Tiwari at +91 9795971160.*"

def run_engine(en_name, display_title, cfg):
    st.subheader(display_title)
    st.info(cfg["info"], icon="ℹ️")
    
    step_key, qs_key, story_key = f"{en_name}_step", f"{en_name}_qs", f"{en_name}_story"
    if step_key not in st.session_state: st.session_state[step_key] = 1
    
    if st.session_state[step_key] == 1:
        u_story = st.text_area(cfg["init"], height=120)
        if st.button(ui["btn_analyze"]):
            if u_story:
                with st.spinner("Analyzing legal grounds..."):
                    q_prompt = f"ROLE: {cfg['qr']}. TASK: {cfg['qt']} Context: '{u_story}'. CONSTRAINTS: Identify critical missing facts. OUTPUT: Ask strictly necessary investigative questions (1 to 5). Provide EACH question in BOTH English and Hindi."
                    st.session_state[qs_key] = model.generate_content(q_prompt).text
                    st.session_state[story_key] = u_story
                    st.session_state[step_key] = 2
                    st.rerun()
    elif st.session_state[step_key] == 2:
        st.success(st.session_state[qs_key])
        u_answers = st.text_area("Provide Clarifications / स्पष्टीकरण दें:")
        doc_lang = st.radio("Select Output Language for Final Document / दस्तावेज़ की भाषा चुनें:", ["English", "Hindi"], horizontal=True, key=f"doc_{en_name}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button(ui["btn_draft"]):
                with st.spinner("Drafting document..."):
                    prompt = f"ROLE: {cfg['dr']}. TASK: {cfg['dt']}. CONTEXT: Base Story: '{st.session_state[story_key]}'. Clarifications: '{u_answers}'. CONSTRAINTS: {cfg['dc']}. OUTPUT: Formal legal document in {doc_lang}."
                    st.write(model.generate_content(prompt).text + watermark)
        with col2:
            if st.button(ui["btn_reset"]): st.session_state[step_key] = 1; st.rerun()

# ==========================================
# 5. NAVIGATION & ROUTING
# ==========================================
st.divider()
category = st.pills("Access Portal / पोर्टल एक्सेस करें:", ui["tabs"], default=ui["tabs"][0])
st.divider()

if category == ui["tabs"][0] or category == ui["tabs"][1]:
    # Dynamic Dictionary Lookup Mapping
    cat_key = "citizen" if category == ui["tabs"][0] else "advocate"
    desk = st.selectbox("Select Legal Desk:", ui["desks"][cat_key])
    tool = st.selectbox("Select Tool:", ui["tools"][desk])
    
    # Get the precise English name to fetch from Vault
    desk_idx = ui["desks"][cat_key].index(desk)
    en_desk = en["desks"][cat_key][desk_idx]
    tool_idx = ui["tools"][desk].index(tool)
    en_tool = en["tools"][en_desk][tool_idx]

    # Handle 1-Step Research Tools differently
    if en_tool == "Case Law Summarizer":
        st.subheader(tool); st.info("Extract the core Issue, Facts, Ratio Decidendi, and Precedents from lengthy judgments.", icon="ℹ️")
        judgment = st.text_area("Paste Judgment Text:", height=200)
        doc_lang = st.radio("Select Output Language:", ["English", "Hindi"], horizontal=True, key="doc_sum")
        if st.button("Generate Summary"):
            with st.spinner("Analyzing Ratio Decidendi..."):
                st.success(model.generate_content(f"ROLE: Judicial Clerk. TASK: Deep analysis of: '{judgment}'. CONSTRAINTS: Output strictly using 5 headers: 1. Issue, 2. Facts, 3. Ratio Decidendi, 4. Precedents, 5. Verdict. OUTPUT: Legal brief in {doc_lang}.").text)
    
    elif en_tool == "IPC to BNS Converter":
        st.subheader(tool); st.info("Instantly map old Indian Penal Code (IPC) sections to the exact matching provisions of the new BNS 2023.", icon="ℹ️")
        sec = st.text_input("Enter IPC Section / Offense Name:")
        doc_lang = st.radio("Select Output Language:", ["English", "Hindi"], horizontal=True, key="doc_ipc")
        if st.button("Convert to BNS 2023"):
            st.success(model.generate_content(f"ROLE: Law Professor. TASK: Map IPC Section {sec} to BNS 2023 section. OUTPUT: Direct section mapping and 2-line explanation in {doc_lang}.").text)
    
    else:
        # Run the powerful Engine for all other tools!
        run_engine(en_tool, tool, PROMPT_VAULT[en_tool])

# ==========================================
# 6. PARTNER ADVOCATE & LEAD CAPTURE FORMS
# ==========================================
elif category == ui["tabs"][2]:
    st.markdown("### 🤝 Grow Your Practice with NyayaSahayak")
    st.write("Receive verified, high-intent legal leads directly from citizens in your specific city and practice area.")
    with st.form("partner_form", clear_on_submit=True):
        adv_name, adv_bar = st.text_input("Advocate Name:"), st.text_input("Bar Council Enrollment Number:")
        adv_city, adv_phone = st.text_input("City / District Court:"), st.text_input("WhatsApp Number:")
        st.multiselect("Preferred Lead Categories:", ["Criminal/Bail", "Cyber Crime", "Property/Civil", "Corporate", "Service Law", "Family"])
        if st.form_submit_button("Apply to Join Network"):
            if adv_name and adv_bar: st.success(f"Application Submitted! We will contact you regarding leads in {adv_city}.")
            else: st.error("Please fill in Name and Bar Council Number.")

st.divider()

if category == ui["tabs"][0]:
    st.markdown("### 👨‍⚖️ Need Formal Representation?" if ui_lang == "English" else "### 👨‍⚖️ औपचारिक प्रतिनिधित्व की आवश्यकता है?")
    st.write("For official court filing, tribunal representation, or case strategy, schedule a consultation." if ui_lang == "English" else "आधिकारिक कोर्ट फाइलिंग के लिए परामर्श बुक करें।")
    with st.form("intake_form", clear_on_submit=True):
        c_name, c_phone = st.text_input("Full Name / पूरा नाम:"), st.text_input("WhatsApp Number / संपर्क नंबर:")
        st.selectbox("Matter Type / मामले का प्रकार:", ["Criminal Defense", "Cyber Fraud", "Property Disputes", "Corporate", "Service Matters", "Family", "Other"])
        st.selectbox("Current Stage / वर्तमान स्थिति:", ["Not yet filed", "Police/Cyber Cell", "District Court", "Tribunals (RERA, CAT)", "High Court"])
        if st.form_submit_button(ui["req"]):
            if c_name and c_phone: st.success(f"Request Received. Adv. Shobhit Tiwari's office will contact {c_name} shortly." if ui_lang == "English" else f"अनुरोध प्राप्त हुआ। कार्यालय जल्द संपर्क करेगा।")
            else: st.error("Please provide both your name and contact number." if ui_lang == "English" else "कृपया नाम और नंबर दें।")

# ==========================================
# 7. LOCAL SEO & LEGAL FOOTER
# ==========================================
st.divider()
st.markdown("""
<div style='text-align: justify; font-size: 11px; color: gray;'>
    <b>NyayaSahayak platform is intended for educational and preliminary drafting assistance. It does not establish an attorney-client relationship.</b><br><br>
    <b>Full-Service Litigation Chamber:</b> Representing clients in Criminal Defense, Cyber Law, Service Matters, Arbitration, and Property Disputes. Serving clients across Uttar Pradesh at the Allahabad High Court (Lucknow Bench), District & Sessions Courts, and Specialized Tribunals (CAT, RERA, DRT).<br>
    © 2026 NyayaSahayak. Chief Legal Advisor: Adv. Shobhit Tiwari.
</div>
""", unsafe_allow_html=True)
