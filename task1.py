import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from fpdf import FPDF
import unicodedata
from datetime import datetime

# Clean special characters that latin-1 can't handle
def clean_text(text):
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

st.set_page_config(page_title="AI Interview Coach", layout="centered")
st.title("🤖 AI Interview Coach")
st.markdown("Practice mock interviews, get feedback, and improve your answers in real-time!")

# ---- Task 2: Candidate Name Input ----
if "candidate_name" not in st.session_state:
    st.session_state.candidate_name = ""

st.session_state.candidate_name = st.text_input(
    "Enter your name (this will appear on your final report):", 
    value=st.session_state.candidate_name
)

# Interview questions per domain
questions_by_domain = {
    "Data Science": [
        "Tell me about yourself.",
        "What are your favorite ML algorithms and why?",
        "Explain a data project you've worked on.",
    ],
    "Web Development": [
        "Tell me about yourself.",
        "What frameworks have you worked with?",
        "How do you optimize a web app’s performance?",
    ],
    "Human Resources": [
        "Tell me about yourself.",
        "How do you resolve conflicts in a team?",
        "What strategies do you use for employee retention?",
    ],
    "Marketing": [
        "Tell me about yourself.",
        "Describe a successful campaign you’ve worked on.",
        "How do you analyze customer behavior?",
    ],
    "Software Engineering": [
        "Tell me about yourself.",
        "How do you approach debugging a complex issue?",
        "Describe a time you worked on a team project.",
    ]
}

# Domain selection
selected_domain = st.selectbox("Select Interview Domain:", list(questions_by_domain.keys()))

# Initialize session state
if "question_index" not in st.session_state:
    st.session_state.question_index = 0
if "answers" not in st.session_state:
    st.session_state.answers = []
if "show_next" not in st.session_state:
    st.session_state.show_next = False

questions = questions_by_domain[selected_domain]
current_question = questions[st.session_state.question_index]

st.markdown(f"### Interview Domain: {selected_domain}")
st.markdown(f"**Question {st.session_state.question_index + 1}:** {current_question}")

# Text area for answer
user_answer = st.text_area("Your Answer:", height=150)

# Handle submission
if st.button("Submit Answer"):
    if user_answer.strip() == "":
        st.warning("Please provide an answer before submitting.")
    else:
        with st.spinner("Analyzing your answer..."):
            prompt = f"""
You are an AI interview coach. Provide a detailed evaluation for the candidate's answer.

Include:
1. Summary  
2. Strengths  
3. Areas of Improvement  
4. Score out of 10 with reasoning  
5. An improved version of the answer  

Interview Domain: {selected_domain}  
Interview Question: {current_question}  
Candidate's Answer: "{user_answer}"
"""
            try:
                response = model.generate_content(prompt)
                st.success("✅ Feedback received!")
                st.markdown("### 📋 Feedback")
                st.write(response.text)

                st.session_state.answers.append({
                    "question": current_question,
                    "answer": user_answer,
                    "feedback": response.text
                })
                st.session_state.show_next = True
            except Exception as e:
                st.error(f"Error: {e}")

# Handle next question
if st.session_state.show_next:
    if st.session_state.question_index + 1 < len(questions):
        if st.button("Next Question"):
            st.session_state.question_index += 1
            st.session_state.show_next = False
            st.rerun()
    else:
        st.markdown("🎉 **You’ve completed the mock interview! Great job!**")

        # PDF Generation
        if st.button("Generate PDF Report"):
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)

            # Cover Page
            pdf.add_page()
            pdf.set_font("Arial", "B", 22)
            pdf.cell(0, 10, "AI Interview Coach Report", ln=True, align="C")

            # Optional logo
            logo_path = "logo.png"
            if os.path.exists(logo_path):
                pdf.image(logo_path, x=80, y=30, w=50)
                pdf.ln(60)
            else:
                pdf.ln(30)

            pdf.set_font("Arial", size=14)
            candidate_name = st.session_state.candidate_name or "Candidate Name"
            pdf.cell(0, 10, clean_text(f"Candidate: {candidate_name}"), ln=True, align="C")
            pdf.cell(0, 10, clean_text(f"Interview Domain: {selected_domain}"), ln=True, align="C")
            pdf.cell(0, 10, f"Date: {datetime.today().strftime('%B %d, %Y')}", ln=True, align="C")
            pdf.ln(15)

            pdf.set_font("Arial", "I", 12)
            pdf.multi_cell(0, 10, clean_text("This report includes your answers and detailed feedback generated by the AI Interview Coach. Use it to improve your skills and confidence."))

            # Add interview content
            pdf.add_page()
            for idx, item in enumerate(st.session_state.answers, 1):
                pdf.set_font("Arial", "B", 12)
                pdf.multi_cell(0, 10, clean_text(f"Question {idx}: {item['question']}"))
                pdf.ln(2)

                pdf.set_font("Arial", "B", 11)
                pdf.multi_cell(0, 8, "Your Answer:")
                pdf.set_font("Arial", "", 11)
                pdf.multi_cell(0, 8, clean_text(item["answer"]))
                pdf.ln(2)

                pdf.set_font("Arial", "B", 11)
                pdf.multi_cell(0, 8, "Feedback:")
                pdf.set_font("Arial", "", 11)
                pdf.multi_cell(0, 8, clean_text(item["feedback"]))
                pdf.ln(8)

                pdf.set_draw_color(200, 200, 200)
                pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                pdf.ln(8)

            pdf_output = pdf.output(dest='S').encode('latin1')

            st.download_button(
                label="📥 Download Your Beautified PDF Report",
                data=pdf_output,
                file_name=f"interview_report_{selected_domain.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
