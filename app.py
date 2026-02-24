import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. CORE SETUP & BRANDING (SEO Friendly)
# ==========================================
st.set_page_config(page_title="NyayaSahayak | Legal AI by Adv. Shobhit Tiwari", page_icon="⚖️", layout="centered")

# Initialize Gemini AI
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception:
    st.error("System updating. Please check back later.")
    st.stop()

# ==========================================
# 2. UI & LEAD GENERATION HEADER
# ==========================================
st.title("⚖️ NyayaSahayak")
st.markdown("### Digital Legal Assistant | High Court, Lucknow Bench")

# Language Toggle
lang = st.radio("Language / भाषा:", ["English", "Hindi"], horizontal=True)

# Marketing Copy Dictionary
ui = {
    "English": {
        "iam": "I am a:", "btn": "Generate Legal Draft 🚀", "lbl": "Describe the issue:",
        "profile": "Expert Legal Services by Adv. Shobhit Tiwari"
    },
    "Hindi": {
        "iam": "मैं हूँ:", "btn": "कानूनी ड्राफ्ट तैयार करें 🚀", "lbl": "समस्या का विवरण दें:",
        "profile": "अधिवक्ता शोभित तिवारी द्वारा विशेषज्ञ कानूनी सेवाएं"
    }
}[lang]

# High-Visibility Trust Badge (Lead Capture)
st.success(f"**{ui['profile']}**\n\nFiling & Court Representation | 📞 +91 9795971160")
st.divider()

# ==========================================
# 3. NAVIGATION & TOOL SELECTION
# ==========================================
category = st.pills(ui["iam"], ["Citizen", "Advocate"], default="Citizen")

if category == "Citizen":
    tool = st.selectbox("Select Service:", ["1. Police Complaint (FIR)", "2. Cheque Bounce Notice (Sec 138)"])
else:
    tool = st.selectbox("Select Service:", ["1. IPC to BNS Converter", "2. Case Law Summarizer"])

st.divider()

# ==========================================
# 4. OPTIMIZED AI LOGIC & PROMPTS
# ==========================================
# Marketing Watermark to attach to all generated drafts
watermark = f"\n\n---\n**Disclaimer:** *Drafted via NyayaSahayak AI. This is not formal legal advice. For official filing and legal strategy, consult Adv. Shobhit Tiwari (Lucknow High Court) at +91 9795971160.*"

# --- TOOL: INTERACTIVE FIR ---
if tool == "1. Police Complaint (FIR)":
    st.subheader("📝 Interactive FIR Drafter")
    
    if "fir_step" not in st.session_state:
        st.session_state.fir_step = 1

    if st.session_state.fir_step == 1:
        u_story = st.text_area(ui["lbl"], height=120, placeholder="E.g., My bike was stolen yesterday from...")
        if st.button("Analyze & Ask Questions 🔍"):
            if u_story:
                with st.spinner("AI is analyzing legal grounds..."):
                    prompt = f"Role: Senior Police Officer in UP. Read this incident: '{u_story}'. Ask 3 precise questions in {lang} to gather missing facts needed for a strong BNS FIR."
                    st.session_state.fir_qs = model.generate_content(prompt).text
                    st.session_state.fir_story = u_story
                    st.session_state.fir_step = 2
                    st.rerun()
            else:
                st.warning("Please enter incident details.")
                
    elif st.session_state.fir_step == 2:
        st.info(st.session_state.fir_qs)
        u_answers = st.text_area("Your Answers:")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button(ui["btn"]):
                with st.spinner("Drafting official FIR..."):
                    prompt = f"Role: Expert Criminal Lawyer in UP. Draft a formal FIR addressed to the SHO. Story: {st.session_state.fir_story}. Additional facts: {u_answers}. Apply relevant BNS 2023 sections. Language: {lang}."
                    draft = model.generate_content(prompt).text
                    st.markdown("### 📄 Final Document")
                    st.write(draft + watermark)
        with col2:
            if st.button("Start Over 🔄"):
                st.session_state.fir_step = 1
                st.rerun()

# --- TOOL: CHEQUE BOUNCE ---
elif tool == "2. Cheque Bounce Notice (Sec 138)":
    st.subheader("💰 Cheque Bounce Notice")
    details = st.text_area("Enter Details:", placeholder="Sender Name, Defaulter Name, Cheque Number, Date, Amount...", height=120)
    if st.button(ui["btn"]):
        if details:
            with st.spinner("Drafting Legal Notice..."):
                prompt = f"Role: Corporate Lawyer in India. Draft a strict legal notice under Section 138 of the Negotiable Instruments Act based on these details: {details}. Ensure the mandatory 15-day warning is prominent. Language: {lang}."
                draft = model.generate_content(prompt).text
                st.write(draft + watermark)

# --- TOOL: IPC TO BNS ---
elif tool == "1. IPC to BNS Converter":
    st.subheader("⚖️ IPC to BNS Mapper")
    sec = st.text_input("Enter IPC Section (e.g. 302, 420):")
    if st.button(ui["btn"]):
        if sec:
            prompt = f"Role: Indian Law Professor. Map IPC Section {sec} to the exact new BNS 2023 section. Give a 2-line explanation in {lang}."
            st.success(model.generate_content(prompt).text)

# --- TOOL: CASE SUMMARIZER ---
elif tool == "2. Case Law Summarizer":
    st.subheader("🏛️ Judgment Summarizer")
    judgment = st.text_area("Paste Judgment Text:", height=200)
    if st.button(ui["btn"]):
        if judgment:
            with st.spinner("Extracting Ratio Decidendi..."):
                prompt = f"Role: Supreme Court Researcher. Summarize this judgment into exactly 5 bullet points: Core Issue, Key Facts, Ratio Decidendi, Precedents Cited, and Final Verdict. Language: {lang}. Text: {judgment}"
                st.info(model.generate_content(prompt).text)

# ==========================================
# 5. GLOBAL FOOTER
# ==========================================
st.divider()
st.caption("© 2026 NyayaSahayak. Designed for educational purposes and initial drafting assistance.")
