import streamlit as st
import pandas as pd
import re

from utils.excel_reader import read_excel
from utils.jd_parser import (
    extract_email,
    extract_company,
    extract_role
)
from utils.mail_generator import generate_mail
from utils.mail_sender import send_email
from utils.batch_sender import send_next_batch
from utils.history_manager import load_history
from utils.column_mapper import detect_columns


# ==========================
# SESSION STATE
# ==========================

if "generated_mail" not in st.session_state:
    st.session_state.generated_mail = ""

if "email" not in st.session_state:
    st.session_state.email = ""


# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="AI AutoMailer",
    page_icon="📧",
    layout="wide"
)

st.title("📧 AI AutoMailer")


# ==========================
# INPUTS
# ==========================

role = st.text_input(
    "Enter Default Role",
    placeholder="AI/ML Engineer"
)

contact_source = st.radio(
    "Choose Contact Source",
    [
        "JD Paste",
        "Contact List Paste",
        "Excel Upload"
    ]
)


# ==========================
# JD INPUT
# ==========================

if contact_source == "JD Paste":

    jd_text = st.text_area(
        "Paste Job Description",
        height=250
    )


# ==========================
# CONTACT LIST INPUT
# ==========================

elif contact_source == "Contact List Paste":

    contacts = st.text_area(
        "Paste Emails",
        height=250,
        placeholder="""
hr@google.com
jobs@microsoft.com
careers@adobe.com
"""
    )


# ==========================
# EXCEL INPUT
# ==========================

elif contact_source == "Excel Upload":

    uploaded_file = st.file_uploader(
        "Upload Excel / CSV",
        type=[
            "xlsx",
            "xls",
            "csv"
        ]
    )


# ==========================
# CONTINUE BUTTON
# ==========================

if st.button("Continue"):

    # ==========================
    # JD MODE
    # ==========================

    if contact_source == "JD Paste":

        company = extract_company(jd_text)
        email = extract_email(jd_text)
        jd_role = extract_role(jd_text)

        st.subheader("📋 Detected Information")

        st.write("🏢 Company:", company)
        st.write("💼 Role:", jd_role)
        st.write("📧 Email:", email)

        try:

            st.session_state.generated_mail = generate_mail(
                role=role,
                company=company or "",
                jd=jd_text
            )

            st.session_state.email = email

        except Exception as e:

            st.error(
                f"Mail generation failed: {str(e)}"
            )

    # ==========================
    # CONTACT LIST MODE
    # ==========================

    elif contact_source == "Contact List Paste":

        emails = re.findall(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            contacts
        )

        st.subheader("📧 Detected Emails")

        if emails:

            st.success(
                f"{len(emails)} emails found"
            )

            for email in emails:

                st.write(email)

        else:

            st.warning(
                "No valid emails found"
            )
# ==========================
# EXCEL MODE
# ==========================

if contact_source == "Excel Upload":

    if uploaded_file is None:

        st.warning(
            "Please upload an Excel or CSV file."
        )

    else:

        df = read_excel(uploaded_file)

        columns = detect_columns(df)

        if columns["email"] is None:

            st.error(
                "❌ No Email column found."
            )

            st.stop()

        email_column = columns["email"]

        history = load_history()

        total = len(df)

        already_sent = len(

            df[
                df[email_column]
                .astype(str)
                .str.lower()
                .isin(history)
            ]

        )

        remaining = total - already_sent

        st.subheader("📊 Recruiter Summary")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total Recruiters",
                total
            )

        with col2:

            st.metric(
                "Already Contacted",
                already_sent
            )

        with col3:

            st.metric(
                "Remaining",
                remaining
            )

        st.dataframe(
            df.head(),
            use_container_width=True
        )

        batch_size = st.slider(
            "Emails Per Batch",
            min_value=1,
            max_value=100,
            value=50
        )

        if st.button("🚀 Send Next Batch"):

            with st.spinner(
                "Generating mails and sending..."
            ):

                sent, skipped, failed, report = send_next_batch(
                    df=df,
                    batch_size=batch_size,
                    default_role=role
                )

            st.success(
                f"✅ Sent : {sent}"
            )

            st.info(
                f"⏭ Skipped : {skipped}"
            )

            if failed:

                st.error(
                    f"❌ Failed : {failed}"
                )

            if report:

                st.subheader(
                    "📄 Batch Report"
                )

                report_df = pd.DataFrame(
                    report
                )

                st.dataframe(
                    report_df,
                    use_container_width=True
                )
# ==========================
# GENERATED MAIL SECTION
# ==========================

if st.session_state.generated_mail:

    st.subheader("✉️ Generated Mail")

    st.text_area(
        "Mail Draft",
        st.session_state.generated_mail,
        height=450
    )

    if st.button("📨 Send Mail Now"):

        try:

            lines = st.session_state.generated_mail.split("\n")

            subject = ""

            if len(lines):

                subject = (
                    lines[0]
                    .replace("Subject:", "")
                    .strip()
                )

            body = st.session_state.generated_mail

            if body.startswith("Subject:"):

                body = "\n".join(
                    body.split("\n")[2:]
                )

            send_email(
                recipient_email=st.session_state.email,
                subject=subject,
                body=body
            )

            st.success(
                f"✅ Mail sent successfully to {st.session_state.email}"
            )

        except Exception as e:

            st.error(
                f"❌ Mail sending failed : {e}"
            )


# ==========================
# FOOTER
# ==========================

st.markdown("---")

st.caption(
    "🚀 AI AutoMailer | Built with Streamlit + Groq + Gmail SMTP"
)