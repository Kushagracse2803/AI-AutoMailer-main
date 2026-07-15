import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_mail(role, company, jd):

    prompt = f"""
You are an expert cold outreach writer helping a fresher apply for AI/ML and Generative AI roles.

Candidate Information

Name: Kushagra Tiwari

Phone:
+91 8127328573

Email:
kushagracse.techai@gmail.com

Portfolio:
https://my-portfolio-flax-three-83.vercel.app/

Skills:
- PyTorch & TensorFlow pipelines
- Pre-training & Fine-tuning LLMs/SLMs (Phi-3.5 via QLoRA)
- Custom GPT Architecture & stacked transformer blocks
- Multi-LLM routing orchestration
- Advanced RAG Pipelines (FAISS, Chroma)
- Python, SQL, Flask, React.js, Streamlit
- Hugging Face Transformers & Diffusers

Projects:

1. Elysium AI
- GenAI platform featuring a custom GPT-style LLM trained from scratch in PyTorch.
- Features custom tokenization, causal self-attention, and stacked transformer blocks.
- Engineered an intelligent multi-LLM router to dynamically split execution between Groq, Gemini, and Ollama.
- Deployed MultiModel tools including a Quiz Generator, Summarizer, and Text-to-Video models.

2. Kriti Support AI
- Enterprise-grade RAG Helpdesk powered by local SLMs for rulebook-bound query resolution.
- Uses TinyLlama via Ollama with strict prompt boundary parameters to eliminate hallucinations.
- Localized indexing pipeline parsing unstructured policy documents into a persistent FAISS vector store.

3. Psyche Track
- Multimodal health analysis pipeline processing text, audio, and video inputs.
- Fine-tuned an on-device Phi-3.5 SLM via QLoRA in PyTorch for risk stratification.
- Combines text NLP, audio MFCCs, and visual CNNs, achieving high structural classification accuracy.

Target Company:
{company}

Target Role:
{role}

Job Description:
{jd}

SUBJECT RULES

- Write a professional subject line.
- Suitable for a fresher.
- Keep it concise.
- Prefer styles like:

  Enquiry Regarding <Role>
  Regarding Your <Role> Opening
  Interest in <Role>
  Enquiry for <Role> Opportunity

- Avoid:
  Application for...
  Job Application...
  Resume Attached...
  Urgent...
  Sales-style subjects

EMAIL RULES

Opening:
- Show that the JD was actually read.
- Reference company, role, technology stack or requirements.

Context:
- Explain why reaching out.

Value:
- Mention only the most relevant 1-2 projects.
- Do NOT simply list projects.
- Explain why those projects are relevant.
- Connect project experience to the JD requirements.
- Mention specific technologies found in the JD whenever relevant.

Portfolio:
- Include naturally.

Resume:
- Mention resume is attached.

CTA:
- Ask for a simple reply.
- Keep it low-pressure and professional.

Tone:
- Human
- Intelligent
- Confident
- Professional
- Conversational
- Not overly enthusiastic
- Not corporate sounding

Length:
- 220 to 300 words

Output Format:

Subject: ...

<email body>

Best Regards,

Kushagra Tiwari
+91 8127328573
kushagracse.techai@gmail.com
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.8
    )

    return response.choices[0].message.content 


def generate_recruiter_template():

    prompt = """
You are an expert technical recruiter outreach writer.

Your task is to write ONE reusable cold email template for a recent Computer Science graduate.

IMPORTANT:

This email is NOT for a specific job.

Do NOT assume any vacancy exists.

Do NOT mention any job description.

Do NOT invent company information.

The greeting will later be replaced automatically.

Start exactly with:

Hi {GREETING},

Candidate Details

Name: Kushagra Tiwari

Education:
B.Tech in Computer Science and Engineering (Artificial Intelligence)

I am currently seeking full-time early-career opportunities where I can contribute and continue learning in areas such as:

- AI/ML Engineering
- Generative AI Development (LLMs / SLMs)
- Core Software Engineering
- MLOps & Advanced RAG System Design
- Backend Development (Python / Flask REST APIs)

Skills:

- Python, PyTorch, TensorFlow, Flask, React.js
- Custom GPT Architecture (Pre-training & Fine-tuning via QLoRA)
- Intelligent Multi-LLM Routing
- Advanced RAG (FAISS, Chroma) & Vector Store Indexing
- Hugging Face Transformers, Diffusers, LangChain

Mention ONLY these projects naturally:

1. Elysium AI (Custom GPT architecture and Multi-LLM router from scratch)
2. Kriti Support AI (Localized Enterprise RAG Helpdesk using local SLMs and FAISS)

Mention:

Portfolio:
https://my-portfolio-flax-three-83.vercel.app/

Resume is attached.

Subject MUST BE:

Open to AI/ML & Software Engineering Opportunities

Tone:

- Friendly
- Human
- Professional
- Short

Length:

140-170 words.

Do NOT use placeholders except:

{GREETING}

Return exactly:

Subject: ...

Email...
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.5
    )

    return response.choices[0].message.content