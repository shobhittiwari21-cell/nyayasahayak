import streamlit as st
import google.generativeai as genai
import sqlite3
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# ==========================================
# 1. CORE SETUP & PLATFORM BRANDING
# ==========================================
st.set_page_config(page_title="NyayaSahayak | India's AI Legal Assistant", page_icon="⚖️", layout="centered")

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception:
    st.error("System is currently undergoing maintenance. Please try again later.")
    st.stop()

# ==========================================
# 2. DATABASE & LEAD ROUTING SETUP
# ==========================================
# Initialize SQLite Database (creates file in your app directory)
conn = sqlite3.connect('leads.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS leads 
             (name TEXT, phone TEXT, matter_type TEXT, stage TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

def save_and_notify(name, phone, matter, stage):
    """Saves lead to DB and attempts to email the Chamber."""
    # 1. Save to Database
    try:
        c.execute("INSERT INTO leads (name, phone, matter_type, stage) VALUES (?, ?, ?, ?)", (name, phone, matter, stage))
        conn.commit()
    except Exception as e:
        st.error(f"Database error: {e}")

    # 2. Send Email Alert (Will silently pass if secrets aren't configured yet)
    try:
        if "SENDER_EMAIL" in st.secrets and "CHAMBER_EMAIL" in st.secrets:
            msg = MIMEText(f"🚨 NEW HIGH-INTENT LEAD ALERT 🚨\n\nName: {name}\nWhatsApp: {phone}\nMatter/Tool Used: {matter}\nStage: {stage}\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            msg['Subject'] = f"NyayaSahayak Lead: {matter} - {name}"
            msg['From'] = st.secrets["SENDER_EMAIL"]
            msg['To'] = st.secrets["CHAMBER_EMAIL"]
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(st.secrets["SENDER_EMAIL"], st.secrets["EMAIL_PASSWORD"])
                server.send_message(msg)
    except Exception:
        pass # Do not crash the app if email fails; DB still captured the lead.

# ==========================================
# 3. UI STRINGS & TRANSLATION
# ==========================================
st.markdown("""
    <div style='text-align: center; padding: 15px;'>
        <h1 style='color: #2c3e50; font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; margin-bottom: 0px;'>⚖️ NyayaSahayak</h1>
        <h4 style='color: #34495e; font-weight: 400; margin-top: 5px;'>India's Premium AI Legal Assistant</h4>
    </div>
""", unsafe_allow_html=True)

st.info("**Powered by the Chambers of Adv. Shobhit Tiwari** \nAllahabad High Court (Lucknow Bench), District Courts & Tribunals | 📞 +91 9795971160")

ui_lang = st.radio("Interface Language / इंटरफ़ेस भाषा:", ["English", "Hindi"], horizontal=True)

en = {
    "tabs": ["Citizen / Public", "Legal Professional", "Partner Advocate Program"],
    "tools_cit": ["Police Complaint (FIR) Drafter", "1930 Cyber Fraud Complaint", "Bank Account Unfreeze Application", "Tenancy/Rent Agreement (UP)", "Tenant Eviction Notice", "Section 138 (Cheque Bounce) Notice", "MSME Payment Recovery Notice", "Show Cause Notice Reply", "Traffic Challan Compounding Request"],
    "tools_adv": ["Bail Application Drafter", "Affidavit Drafter (Lucknow Bench)", "Writ Petition Grounds (Art. 226)", "Case Law Summarizer", "IPC to BNS Converter"],
    "btn_analyze": "Analyze & Ask Clarifications 🔍", "btn_reset": "Start Over 🔄", "req": "Request Consultation"
}

hi = {
    "tabs": ["नागरिक / आम जनता", "वकील / कानूनी पेशेवर", "पार्टनर एडवोकेट प्रोग्राम"],
    "tools_cit": ["पुलिस शिकायत (FIR) ड्राफ्टर", "1930 साइबर धोखाधड़ी शिकायत", "बैंक खाता अनफ्रीज आवेदन", "किरायानामा (रेंट एग्रीमेंट) - यूपी", "किरायेदार बेदखली (Eviction) नोटिस", "धारा 138 (चेक बाउंस) नोटिस", "MSME भुगतान वसूली नोटिस", "कारण बताओ (Show Cause) नोटिस का जवाब", "ट्रैफिक चालान छूट/माफी आवेदन"],
    "tools_adv": ["जमानत (Bail) आवेदन ड्राफ्टर", "हलफनामा (Affidavit) ड्राफ्टर", "रिट याचिका के आधार (Art. 226)", "अपीलीय निर्णय (Judgment) सारांश", "कानून कनवर्टर: IPC से BNS"],
    "btn_analyze": "विश्लेषण करें और प्रश्न पूछें 🔍", "btn_reset": "शुरुआत से शुरू करें 🔄", "req": "परामर्श का अनुरोध करें"
}

ui = en if ui_lang == "English" else hi

# ==========================================
# 4. THE PROMPT VAULT
# ==========================================
# (Keeping your original prompts intact for brevity, they are excellent)
PROMPT_VAULT = {
    "Police Complaint (FIR) Drafter": {"info": "Draft a formal Police Complaint under the BNS 2023.", "init": "Describe the incident roughly / घटना का विवरण दें:", "qr": "Veteran Police IO in UP", "qt": "Identify missing facts for a BNS 2023 FIR (time, weapons, witnesses).", "dr": "Elite Criminal Defense Counsel", "dt": "Draft a formal FIR to the SHO.", "dc": "Apply BNS 2023. Do not invent fake facts. Use objective legal prose."},
    "1930 Cyber Fraud Complaint": {"info": "Draft a chronological complaint for the National Cyber Crime Reporting Portal (1930).", "init": "How were you scammed? / आपके साथ धोखाधड़ी कैसे हुई?:", "qr": "Cyber Crime Investigator", "qt": "Identify missing financial facts (UTR numbers, transaction times, bank names).", "dr": "Cyber Law Expert", "dt": "Draft a highly technical, chronological cyber fraud complaint.", "dc": "Include all technical transaction details clearly for cyber cell ingestion."},
    "Bank Account Unfreeze Application": {"info": "Draft an application under Sec 457 CrPC / 503 BNSS to de-freeze a bank account.", "init": "Why was your account frozen? / आपका खाता फ्रीज क्यों हुआ?:", "qr": "Economic Offences Lawyer", "qt": "Identify missing facts (date of freeze, bank name, investigating agency, transaction link).", "dr": "Criminal Trial Advocate", "dt": "Draft an application to the Magistrate for de-freezing a bank account.", "dc": "Assert innocence in chain transactions. Cite BNSS provisions."},
    "Tenancy/Rent Agreement (UP)": {"info": "Create a legally binding 11-month residential or commercial rent agreement.", "init": "Provide Details (Names, Rent, Deposit) / विवरण दें:", "qr": "Civil Real Estate Lawyer in UP", "qt": "Identify missing lease terms (address, lock-in period, notice period).", "dr": "Civil Real Estate Lawyer in UP", "dt": "Draft an 11-month Lease Agreement.", "dc": "Adhere to UP tenancy laws. Include lock-in, notice, and anti-subletting clauses."},
    "Tenant Eviction Notice": {"info": "Draft a strict 30-day statutory notice for a tenant to vacate premises.", "init": "Why are you evicting them? / आप उन्हें बेदखल क्यों कर रहे हैं?:", "qr": "Property Dispute Advocate", "qt": "Identify missing eviction grounds (months of default, specific damages).", "dr": "Property Dispute Advocate", "dt": "Draft a strict 30-day statutory eviction notice.", "dc": "Cite UP Rent Control laws. Demand vacating to avoid civil suit and mesne profits."},
    "Section 138 (Cheque Bounce) Notice": {"info": "Generate a strict 15-day statutory legal notice for a dishonored cheque.", "init": "Provide Cheque Details (Amount, Names) / चेक का विवरण दें:", "qr": "Corporate Litigator", "qt": "Identify missing NI Act requirements (cheque date, return memo date, bounce reason).", "dr": "Corporate Litigator", "dt": "Draft Sec 138 NI Act notice.", "dc": "Tone must be stern. Explicitly state the 15-day statutory warning for criminal proceedings."},
    "MSME Payment Recovery Notice": {"info": "Draft a strong payment recovery notice referencing MSME Samadhaan.", "init": "Who owes you money? / आप पर किसका पैसा बकाया है?:", "qr": "Corporate Advocate", "qt": "Identify missing MSME facts (Udyam Registration number, invoice dates, amount).", "dr": "Corporate Advocate", "dt": "Draft MSME payment recovery notice.", "dc": "Invoke MSMED Act 2006 (compound interest). Set a strict 15-day deadline before legal action."},
    "Show Cause Notice Reply": {"info": "Draft a respectful but legally defensive reply to a disciplinary notice.", "init": "What are the charges against you? / आप पर क्या आरोप हैं?:", "qr": "Service Law Advocate", "qt": "Identify missing disciplinary facts (date of notice, specific charges, user's defense).", "dr": "Service Law Advocate", "dt": "Draft a formal reply to a Show Cause Notice.", "dc": "Tone should be respectful but legally defensive. Invoke principles of natural justice."},
    "Traffic Challan Compounding Request": {"info": "Generate an application to the Traffic Magistrate to request waiver of an e-challan.", "init": "Provide challan details (Vehicle No., Offense) / चालान का विवरण दें:", "qr": "Traffic Court Advocate", "qt": "Identify missing compounding facts (challan number, compelling reason/hardship for waiver).", "dr": "Traffic Court Advocate", "dt": "Draft compounding/waiver application.", "dc": "Address to Traffic Magistrate/Lok Adalat. Tone should be respectful and request leniency."},
    "Bail Application Drafter": {"info": "Draft a comprehensive regular bail application under Section 483 of the BNSS.", "init": "Provide basic FIR Details & Sections:", "qr": "Senior Criminal Defense Advocate", "qt": "Identify missing bail grounds (date of arrest, applicant's specific role, parity).", "dr": "Top-tier Criminal Defense Advocate", "dt": "Draft Regular Bail App under Sec 483 BNSS.", "dc": "Address to District & Sessions Judge. Argue the 'Triple Test'. Demand parity if applicable."},
    "Affidavit Drafter (Lucknow Bench)": {"info": "Generate Counter-Affidavits adhering to the formatting of the Lucknow Bench.", "init": "Provide Case Title and brief subject matter:", "qr": "High Court Counsel", "qt": "Identify missing facts for the affidavit (Deponent details, para-wise rebuttals).", "dr": "High Court Counsel", "dt": "Draft Counter-Affidavit.", "dc": "Adhere strictly to archaic legal phrasing of the Allahabad High Court, Lucknow Bench. Use numbered paragraphs."},
    "Writ Petition Grounds (Art. 226)": {"info": "Draft specific constitutional grounds for a Writ Petition in Service/Administrative Matters.", "init": "Provide details of the wrongful government action:", "qr": "High Court Service Law Counsel", "qt": "Identify missing constitutional grounds (fundamental rights breached, exact impugned order).", "dr": "High Court Counsel", "dt": "Draft the 'Grounds' section for an Article 226 Writ Petition.", "dc": "Focus on arbitrary state action, violation of Article 14/16/21, and Wednesbury unreasonableness."}
}

# ==========================================
# 5. THE GATED ELITE ENGINE
# ==========================================
watermark = f"\n\n---\n**⚠️ CRITICAL LEGAL WARNING:** *This document is an AI-generated preliminary draft. Under the new BNS/BNSS framework, submitting improperly formatted documents or omitting statutory precedents can lead to immediate dismissal of your case or adverse court orders. Courts do not show leniency for technical errors.* \n\n**Do not file this blindly.** For strategic review, formal signature, and court representation at the Allahabad High Court or District Courts, immediately contact **Adv. Shobhit Tiwari at +91 9795971160** to secure your legal rights."

def run_engine(en_name, display_title, cfg):
    st.subheader(display_title)
    st.info(cfg["info"], icon="ℹ️")
    
    # State Keys (Ensure unique state per tool so they don't cross-contaminate)
    step_key = f"{en_name}_step"
    qs_key = f"{en_name}_qs"
    story_key = f"{en_name}_story"
    draft_key = f"{en_name}_final_draft"

    if step_key not in st.session_state: st.session_state[step_key] = 1
    
    # STEP 1: FREE ANALYSIS (Top of Funnel)
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

    # STEP 2: THE GATED DRAFT (Lead Capture)
    elif st.session_state[step_key] == 2:
        st.success("✅ Analysis Complete! Please answer the questions below.")
        st.write(st.session_state[qs_key])
        u_answers = st.text_area("Provide Clarifications / स्पष्टीकरण दें:", height=100)
        doc_lang = st.radio("Select Output Language for Final Document:", ["English", "Hindi"], horizontal=True, key=f"doc_{en_name}")
        
        st.markdown("### 🔒 Unlock Your Final Legal Draft")
        st.warning("To generate your final, customized legal document, please provide your contact details. Adv. Shobhit Tiwari's chamber will review this analysis to ensure legal validity.")
        
        # We do NOT use st.form here to prevent Streamlit execution flow issues with generating state.
        c_name = st.text_input("Full Name / पूरा नाम:", key=f"name_{en_name}")
        c_phone = st.text_input("WhatsApp Number / संपर्क नंबर:", key=f"phone_{en_name}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Unlock & Generate Final Draft 📄"):
                if not c_name or not c_phone:
                    st.error("⚠️ Please provide both your Name and WhatsApp Number to unlock the draft.")
                elif not u_answers:
                    st.error("⚠️ Please provide clarifications to the questions above to ensure an accurate draft.")
                else:
                    with st.spinner("Securing lead and drafting document..."):
                        # 1. Weaponized Action: Save the lead to DB and email the Chamber
                        save_and_notify(c_name, c_phone, en_name, "Tool Final Draft Stage")
                        
                        # 2. Generate the Draft
                        prompt = f"ROLE: {cfg['dr']}. TASK: {cfg['dt']}. CONTEXT: Base Story: '{st.session_state[story_key]}'. Clarifications: '{u_answers}'. CONSTRAINTS: {cfg['dc']}. OUTPUT: Formal legal document in {doc_lang}."
                        generated_text = model.generate_content(prompt).text + watermark
                        
                        # 3. Save to state so it doesn't vanish on rerun
                        st.session_state[draft_key] = generated_text
                        st.session_state[step_key] = 3
                        st.rerun()
        with col2:
            if st.button(ui["btn_reset"]): st.session_state[step_key] = 1; st.rerun()

    # STEP 3: OUTPUT & DOWNLOAD
    elif st.session_state[step_key] == 3:
        st.success("Draft successfully generated. Please review the critical legal warning at the bottom.")
        st.write(st.session_state[draft_key])
        
        # Crucial UX Addition: Let them download what they just "paid" for with their data.
        st.download_button(
            label="📥 Download Legal Draft (.txt)",
            data=st.session_state[draft_key],
            file_name=f"{en_name.replace(' ', '_')}_Draft.txt",
            mime="text/plain"
        )
        
        st.divider()
        if st.button(ui["btn_reset"], key=f"reset3_{en_name}"): 
            st.session_state[step_key] = 1
            st.rerun()

# ==========================================
# 6. NAVIGATION & ROUTING
# ==========================================
st.divider()
category = st.pills("Access Portal / पोर्टल एक्सेस करें:", ui["tabs"], default=ui["tabs"][0])
st.divider()

if category == ui["tabs"][0] or category == ui["tabs"][1]:
    is_citizen = (category == ui["tabs"][0])
    current_tools = ui["tools_cit"] if is_citizen else ui["tools_adv"]
    en_tools_list = en["tools_cit"] if is_citizen else en["tools_adv"]

    tool = st.selectbox("Select Tool:", current_tools)
    tool_idx = current_tools.index(tool)
    en_tool = en_tools_list[tool_idx]

    # Handle 1-Step Research Tools (No Step 2 Gating Required)
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
        # Run the powerful Gated Engine
        run_engine(en_tool, tool, PROMPT_VAULT[en_tool])

# ==========================================
# 7. PARTNER ADVOCATE & LEAD CAPTURE FORMS
# ==========================================
elif category == ui["tabs"][2]:
    st.markdown("### 🤝 Grow Your Practice with NyayaSahayak")
    st.write("Receive verified, high-intent legal leads directly from citizens in your specific city and practice area.")
    with st.form("partner_form", clear_on_submit=True):
        adv_name, adv_bar = st.text_input("Advocate Name:"), st.text_input("Bar Council Enrollment Number:")
        adv_city, adv_phone = st.text_input("City / District Court:"), st.text_input("WhatsApp Number:")
        st.multiselect("Preferred Lead Categories:", ["Criminal/Bail", "Cyber Crime", "Property/Civil", "Corporate", "Service Law", "Family"])
        if st.form_submit_button("Apply to Join Network"):
            if adv_name and adv_bar: 
                save_and_notify(adv_name, adv_phone, "B2B Partner Program", adv_city)
                st.success(f"Application Submitted! We will contact you regarding leads in {adv_city}.")
            else: st.error("Please fill in Name and Bar Council Number.")

st.divider()

if category == ui["tabs"][0]:
    st.markdown("### 👨‍⚖️ Need Formal Representation?" if ui_lang == "English" else "### 👨‍⚖️ औपचारिक प्रतिनिधित्व की आवश्यकता है?")
    st.write("For official court filing, tribunal representation, or case strategy, schedule a consultation." if ui_lang == "English" else "आधिकारिक कोर्ट फाइलिंग के लिए परामर्श बुक करें।")
    with st.form("intake_form", clear_on_submit=True):
        c_name, c_phone = st.text_input("Full Name / पूरा नाम:"), st.text_input("WhatsApp Number / संपर्क नंबर:")
        matter_type = st.selectbox("Matter Type / मामले का प्रकार:", ["Criminal Defense", "Cyber Fraud", "Property Disputes", "Corporate", "Service Matters", "Family", "Other"])
        current_stage = st.selectbox("Current Stage / वर्तमान स्थिति:", ["Not yet filed", "Police/Cyber Cell", "District Court", "Tribunals (RERA, CAT)", "High Court"])
        if st.form_submit_button(ui["req"]):
            if c_name and c_phone: 
                save_and_notify(c_name, c_phone, matter_type, current_stage)
                st.success(f"Request Received. Adv. Shobhit Tiwari's office will contact {c_name} shortly." if ui_lang == "English" else f"अनुरोध प्राप्त हुआ। कार्यालय जल्द संपर्क करेगा।")
            else: 
                st.error("Please provide both your name and contact number." if ui_lang == "English" else "कृपया नाम और नंबर दें।")

# ==========================================
# 8. LOCAL SEO & LEGAL FOOTER
# ==========================================
st.divider()
st.markdown("""
<div style='text-align: justify; font-size: 11px; color: gray;'>
    <b>NyayaSahayak platform is intended for educational and preliminary drafting assistance. It does not establish an attorney-client relationship.</b><br><br>
    <b>Full-Service Litigation Chamber:</b> Representing clients in Criminal Defense, Cyber Law, Service Matters, Arbitration, and Property Disputes. Serving clients across Uttar Pradesh at the Allahabad High Court (Lucknow Bench), District & Sessions Courts, and Specialized Tribunals (CAT, RERA, DRT).<br>
    © 2026 NyayaSahayak. Chief Legal Advisor: Adv. Shobhit Tiwari.
</div>
""", unsafe_allow_html=True)
