import streamlit as st
import json
import pymupdf
import os

# 1. PAGE CONFIG
st.set_page_config(page_title="SpecLogic AI", page_icon="🏗️")

st.title("🏗️ SpecLogic Universal Engine")
st.subheader("Automated Construction Compliance Audit")

# 2. LOAD THE RULES
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    market = st.selectbox("Select Target Market", list(config["markets"].keys()))
    market_data = config["markets"][market]
    rules = market_data["rules"]

    # 3. THE UPLOAD ZONE
    uploaded_file = st.file_uploader("Upload Blueprint or Spec PDF", type="pdf")

    if uploaded_file:
        with st.spinner(f"Auditing against {market} 2026 Codes..."):
            # Save temp file
            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # RUN THE BRAIN
            doc = pymupdf.open("temp.pdf")
            text = "".join([page.get_text() for page in doc])
            
            findings = []
            if rules["insulation_min"] not in text:
                findings.append(f"Standard {rules['insulation_min']} not found.")
            
            # 4. VISUAL RESULTS
            if not findings:
                st.success("✅ 100% COMPLIANT: This project meets all 2026 standards.")
                st.balloons()
            else:
                st.error("⚠️ COMPLIANCE ALERTS FOUND")
                for item in findings:
                    st.write(f"👉 {item}")
                st.info(f"Pro Tip: Update to {rules['insulation_min']} for Green Incentives.")

            doc.close()
            os.remove("temp.pdf")
except FileNotFoundError:
    st.error("Missing config.json file in repository.")
