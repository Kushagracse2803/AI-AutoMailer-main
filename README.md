# 📧 AI AutoMailer

AI AutoMailer is an automated cold outreach orchestration platform optimized for AI/ML engineers and tech professionals looking to scale their job application process. Built with Streamlit, Groq (Llama 3.3), and Gmail SMTP, it dynamically parses target recruiter contexts and executes hyper-personalized outreach campaigns in just a single click.

## 🚀 Key Features
* **One-Click Batch Processing:** Upload your target recruiter Excel/CSV list and dynamically generate/send out customized applications simultaneously.
* **Context-Aware Generation:** Leverages the `llama-3.3-70b-versatile` model to construct personalized email copies mapping candidate project metrics directly to specific job parameters.
* **Smart Column Mapping:** Automatically identifies key data parameters (Emails, Company names, Recruiter names) regardless of irregular Excel structural layouts.
* **Duplication Prevention Matrix:** Built-in transaction logging tracks outreach history to guarantee zero redundant communications to the same hiring manager.
* **Resume Engine Integration:** Automatic parsing attaches localized PDF files securely through secure SSL/TLS server connections.

## 📂 Project Architecture
```text
AI-AutoMailer/
├── .env                  # Secure credential matrix
├── .gitignore            # Version control filters
├── requirements.txt      # Production dependencies
├── app.py                # Core Streamlit application entrypoint
├── Kushagra_Resume.pdf   # Localized candidate profile attachment
├── data/
│   └── sent_history.csv  # Transaction safety logs
└── utils/
    ├── __init__.py
    ├── batch_sender.py   # Bulk sequence logic
    ├── column_mapper.py  # Flexible parameter matcher
    ├── excel_reader.py   # Dataset ingestion layer
    ├── history_manager.py# Integrity tracker
    ├── jd_parser.py      # Plaintext entity extractor
    ├── mail_generator.py # Groq LLM prompt orchestrator
    └── mail_sender.py    # SMTP network delivery layer
