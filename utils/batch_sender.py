from utils.mail_generator import generate_recruiter_template
from utils.mail_sender import send_email
from utils.history_manager import load_history, save_history
from utils.column_mapper import detect_columns

import pandas as pd


def send_next_batch(df, batch_size, default_role):

    history = load_history()

    columns = detect_columns(df)

    if columns["email"] is None:
        raise Exception("No Email column found.")

    email_col = columns["email"]
    company_col = columns["company"]
    name_col = columns["name"]

    df = df.drop_duplicates(subset=[email_col])

    # Generate ONE template
    template = generate_recruiter_template()

    lines = template.split("\n")

    subject = (
        lines[0]
        .replace("Subject:", "")
        .strip()
    )

    body_template = template

    if body_template.startswith("Subject:"):

        body_template = "\n".join(
            body_template.split("\n")[2:]
        )

    sent = 0
    skipped = 0
    failed = 0

    report = []

    for _, row in df.iterrows():

        email = str(
            row[email_col]
        ).strip().lower()

        if email == "" or email == "nan":
            continue

        if email in history:
            skipped += 1
            continue

        if sent >= batch_size:
            break

        # ==========================
        # Greeting Logic
        # ==========================

        greeting = "Hiring Team"

        # Priority 1 -> Recruiter Name

        if name_col:

            name = row[name_col]

            if pd.notna(name):

                name = str(name).strip()

                if name != "" and name.lower() != "nan":

                    greeting = name.split()[0]

        # Priority 2 -> Company

        if greeting == "Hiring Team" and company_col:

            company = row[company_col]

            if pd.notna(company):

                company = str(company).strip()

                if company != "" and company.lower() != "nan":

                    greeting = f"{company} Team"

        # Personalize email

        body = body_template.replace(
            "{GREETING}",
            greeting
        )

        try:

            print(f"Sending to {email}")

            send_email(
                recipient_email=email,
                subject=subject,
                body=body
            )

            history.add(email)

            report.append(
                {
                    "Email": email,
                    "Greeting": greeting,
                    "Status": "Sent"
                }
            )

            sent += 1

        except Exception as e:

            print(e)

            failed += 1

            report.append(
                {
                    "Email": email,
                    "Greeting": greeting,
                    "Status": str(e)
                }
            )

    save_history(history)

    return sent, skipped, failed, report