import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. PAGE CONFIGURATION & BRANDING
# ==========================================
st.set_page_config(page_title="NyayaSahayak | Legal AI Hub", page_icon="⚖️", layout="wide")

# ==========================================
# 2. THE SIDEBAR (LEAD GENERATION & NAVIGATION)
# ==========================================
with st.sidebar:
    st.markdown("## ⚖️ NyayaSahayak")
    st.write("Your Digital Legal Assistant")
    st.markdown("---")
    
    # Navigation Menu
    st.markdown("### 🗂️ Select a Tool")
    category = st.radio("Audience:", ["For Advocates", "For Citizens"])
    
    if category == "For Advocates":
        tool_choice = st.selectbox("Select Tool:", [
            "1. Case Law Summarizer", 
            "2. IPC to BNS Converter", 
            "3. Lucknow HC Affidavit Drafter", 
            "4. Bail Application Writer"
        ])
    else:
        tool_choice = st.selectbox("Select Tool:", [
            "5. Police Complaint (FIR) Drafter", 
            "6. Cheque Bounce Notice (Sec 138)", 
            "7. UP Rent Agreement Maker", 
            "8. Traffic Challan Fighter"
        ])
    
    st.markdown("---")
    # The "Client Magnet" Profile Card
    st.markdown("### 👨‍⚖️ Reviewed by")
    st.success("**Adv. Shobhit Tiwari**\n\nHigh Court, Lucknow Bench")
    st.write("📞 **+91 9795971160**")
    st.write("✉️ **shobhittiwari21@gmail.com**")
    st.caption("Need expert filing or court representation? Book a consultation today.")

# ==========================================
# 3. API SETUP (THE BRAIN)
# ==========================================
# This fetches your free Gemini API key from Streamlit's hidden secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
except KeyError:
    st.error("⚠️ API Key missing! Please add GEMINI_API_KEY to your Streamlit secrets.")
    st.stop()

# Helper function to generate and display the AI response
def generate_legal_document(prompt):
    with st.spinner("⚖️ Analyzing Legal Data... Please wait..."):
        try:
            response = model.generate_content(prompt)
            st.markdown("### 📄 Generated Draft")
            st.info(response.text)
            
            # Add a download button for the text
            st.download_button(
                label="📥 Download Draft as Text File",
                data=response.text,
                file_name="Legal_Draft_NyayaSahayak.txt",
                mime="text/plain"
            )
        except Exception as e:
            st.error(f"An error occurred: {e}")

# ==========================================
# 4. MAIN DASHBOARD & TOOL LOGIC
# ==========================================
st.title(tool_choice)
st.markdown("---")

# ------------------------------------------
# TOOL 1: Case Law Summarizer
# ------------------------------------------
if tool_choice == "1. Case Law Summarizer":
    st.write("Paste a 100-page judgment, get a 5-point summary instantly.")
    judgment_text = st.text_area("Paste Judgment Text Here:", height=250)
    
    if st.button("Generate Summary 🚀"):
        if judgment_text:
            hidden_prompt = f"""
            Role: Senior Legal Researcher at the Allahabad High Court.
            Task: Summarize the provided Indian Court Judgment into a 'Quick-Brief' for a busy litigating advocate.
            Rules: Ignore procedural boilerplate. Focus heavily on the Ratio Decidendi. 
            Output format: 🏛️ CASE BRIEF \n 1. Core Issue \n 2. Key Facts \n 3. Ratio Decidendi \n 4. Final Verdict \n 5. Cited Precedents.
            
            Judgment Text: {judgment_text}
            """
            generate_legal_document(hidden_prompt)
        else:
            st.warning("Please paste the judgment text first.")

# ------------------------------------------
# TOOL 2: IPC to BNS Converter
# ------------------------------------------
elif tool_choice == "2. IPC to BNS Converter":
    st.write("Stop searching the bare acts. Instantly map old IPC sections to the new BNS 2023.")
    old_law = st.text_input("Enter Old IPC Section or Offense Name (e.g., '420' or 'Murder'):")
    
    if st.button("Find BNS Section 🚀"):
        if old_law:
            hidden_prompt = f"""
            Role: Expert in Indian Criminal Law and BNS 2023.
            Task: Map the following old IPC section or offense to the exact new BNS section.
            Output format: ⚖️ BNS CONVERSION RESULT \n - Old IPC Reference \n - New BNS Section \n - Offense Description \n - Maximum Punishment.
            
            User Input: {old_law}
            """
            generate_legal_document(hidden_prompt)
        else:
            st.warning("Please enter a section or offense.")

# ------------------------------------------
# TOOL 3: Lucknow HC Affidavit Drafter
# ------------------------------------------
elif tool_choice == "3. Lucknow HC Affidavit Drafter":
    st.write("Generate a Counter/Rejoinder strictly following the Lucknow Bench format.")
    col1, col2 = st.columns(2)
    with col1:
        case_title = st.text_input("Case Title (e.g., Ram vs State of UP):")
        deponent_name = st.text_input("Deponent Name:")
    with col2:
        deponent_age = st.text_input("Deponent Age:")
        deponent_address = st.text_input("Deponent Address:")
    
    facts = st.text_area("Enter the main facts/grounds (Paragraph wise):", height=150)
    
    if st.button("Draft Affidavit 🚀"):
        if facts:
            hidden_prompt = f"""
            Role: Expert drafting counsel practicing at the High Court of Judicature at Allahabad, Lucknow Bench.
            Task: Draft a formal Counter-Affidavit.
            Rules: MUST use traditional Lucknow High Court formatting (e.g., 'That the deponent is well conversant with the facts...').
            
            Details:
            Case: {case_title}
            Deponent: {deponent_name}, Age: {deponent_age}, Address: {deponent_address}
            Facts to include: {facts}
            """
            generate_legal_document(hidden_prompt)
        else:
            st.warning("Please enter the facts.")

# ------------------------------------------
# TOOL 4: Bail Application Writer
# ------------------------------------------
elif tool_choice == "4. Bail Application Writer":
    st.write("Draft a regular bail application under Section 483 BNSS (Old 439 CrPC).")
    fir_no = st.text_input("FIR Number & Year:")
    ps = st.text_input("Police Station & District:")
    sections = st.text_input("BNS Sections Applied:")
    grounds = st.text_area("Grounds for Bail (e.g., parity, false implication, student):")
    
    if st.button("Draft Bail Application 🚀"):
        if grounds:
            hidden_prompt = f"""
            Role: Criminal Defense Counsel in Uttar Pradesh.
            Task: Draft a regular bail application under Section 483 of the BNSS.
            Rules: Address to the District & Sessions Judge. Include standard bail conditions in the prayer clause.
            
            Details: FIR {fir_no}, PS: {ps}, Sections: {sections}, Grounds: {grounds}.
            """
            generate_legal_document(hidden_prompt)
        else:
            st.warning("Please enter grounds for bail.")

# ------------------------------------------
# TOOL 5: Police Complaint (FIR) Drafter
# ------------------------------------------
elif tool_choice == "5. Police Complaint (FIR) Drafter":
    st.write("Convert a rough story into a formal SHO complaint with BNS sections.")
    incident = st.text_area("Describe what happened in plain English or Hindi:", height=150)
    
    if st.button("Draft Formal Complaint 🚀"):
        if incident:
            hidden_prompt = f"""
            Role: Legal aid assistant specializing in Indian Police procedures.
            Task: Translate this plain-language story into a formal written complaint addressed to the Station House Officer (SHO).
            Rules: Identify and explicitly list the potential BNS (Bharatiya Nyaya Sanhita) sections at the top. 
            Append text at the bottom: 'Drafting an FIR is step one. If the police refuse to register this, contact Adv. [Your Name] to file an application under Section 175(3) BNSS in court.'
            
            Incident: {incident}
            """
            generate_legal_document(hidden_prompt)
        else:
            st.warning("Please describe the incident.")

# ------------------------------------------
# TOOL 6: Cheque Bounce Notice (Sec 138)
# ------------------------------------------
elif tool_choice == "6. Cheque Bounce Notice (Sec 138)":
    st.write("Draft a strict 15-day legal notice under the Negotiable Instruments Act.")
    sender = st.text_input("Sender Name:")
    defaulter = st.text_input("Defaulter Name:")
    cheque_details = st.text_input("Cheque No., Date, and Amount:")
    reason = st.text_input("Reason for Return (e.g., Funds Insufficient):")
    
    if st.button("Generate Legal Notice 🚀"):
        if cheque_details:
            hidden_prompt = f"""
            Role: Corporate Lawyer in India.
            Task: Draft a mandatory legal notice under Section 138 of the Negotiable Instruments Act.
            Rules: The tone must be strict. Give the mandatory 15 days' time to make the payment.
            Append text at the bottom: 'This notice MUST be sent via Registered Post. To ensure it is legally watertight and dispatched on Advocate Letterhead, contact Adv. [Your Name].'
            
            Details: Sender: {sender}, Defaulter: {defaulter}, Cheque: {cheque_details}, Reason: {reason}.
            """
            generate_legal_document(hidden_prompt)
        else:
            st.warning("Please fill in the cheque details.")

# ------------------------------------------
# TOOL 7: UP Rent Agreement Maker
# ------------------------------------------
elif tool_choice == "7. UP Rent Agreement Maker":
    st.write("Generate an 11-month tenancy contract compliant with UP laws.")
    col1, col2 = st.columns(2)
    with col1:
        landlord = st.text_input("Landlord Name:")
        tenant = st.text_input("Tenant Name:")
    with col2:
        rent = st.text_input("Monthly Rent (₹):")
        deposit = st.text_input("Security Deposit (₹):")
    property_address = st.text_area("Complete Property Address:")
    
    if st.button("Draft Rent Agreement 🚀"):
        if property_address:
            hidden_prompt = f"""
            Role: Civil Lawyer in Uttar Pradesh.
            Task: Draft an 11-month residential Rent Agreement.
            Rules: Include standard clauses: 11-month lock-in, one month notice period, prohibition on subletting. 
            
            Details: Landlord: {landlord}, Tenant: {tenant}, Rent: {rent}, Deposit: {deposit}, Address: {property_address}.
            """
            generate_legal_document(hidden_prompt)
        else:
            st.warning("Please enter the property address.")

# ------------------------------------------
# TOOL 8: Traffic Challan Fighter
# ------------------------------------------
elif tool_choice == "8. Traffic Challan Fighter":
    st.write("Draft an application to the Traffic Magistrate to reduce or waive a fine.")
    vehicle = st.text_input("Vehicle Number:")
    offense = st.text_input("Offense Type (e.g., No Parking, Speeding):")
    reason = st.text_area("Reason for Contesting (e.g., Medical emergency, wrong identity):")
    
    if st.button("Draft Waiver Application 🚀"):
        if reason:
            hidden_prompt = f"""
            Role: Traffic Court Advocate.
            Task: Draft a polite, formal application addressed to the Traffic Magistrate/Lok Adalat requesting the waiver/reduction of a traffic challan.
            
            Details: Vehicle: {vehicle}, Offense: {offense}, Reason: {reason}.
            """
            generate_legal_document(hidden_prompt)
        else:
            st.warning("Please provide a reason.")

# ==========================================
# 5. GLOBAL DISCLAIMER
# ==========================================
st.markdown("---")

st.caption("⚠️ **Legal Disclaimer:** This platform provides automated drafts using Artificial Intelligence for educational and reference purposes only. It does not constitute formal legal advice. Always consult a registered advocate before submitting any document to a Court of Law or Police Station.")

