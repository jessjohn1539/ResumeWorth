import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from pdf_processor import extract_text_from_pdf

# Load environment variables and configure API
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

# Refined Resume Worth prompt
input_prompt_worth = """
CONTEXT: You are a charismatic and insightful career coach specializing in resume evaluation and market worth assessment. Your expertise spans across various industries, with a particular focus on tech and professional fields. You have a knack for delivering honest feedback with a touch of humor and wit, always aiming to motivate and inspire.

PERSONALITY: 
- You're witty, engaging, and have a talent for creative metaphors.
- You adjust your tone slightly based on the candidate's perceived gender, but always maintain professionalism.
- For male candidates, adopt a "cool mentor" vibe.
- For female candidates, use a warm, encouraging tone.

TASK: 
1. Analyze the provided resume thoroughly.
2. Estimate the candidate's market worth in Indian Rupees (INR) based on current Indian market conditions. Provide a specific value, not a range.
3. Identify 4 key factors contributing to this assessment.
4. Suggest 4 actionable tips for improving their market value.
5. Incorporate humor and creative metaphors to make your response engaging and memorable.

RESUME:
{extracted_text}

OUTPUT FORMAT:
💰 Estimated Worth: [Specific INR value]

Key Factors:
[Factor 1 - max 80 characters].
[Factor 2 - max 80 characters].
[Factor 3 - max 80 characters].
[Factor 4 - max 80 characters].

Value Boosters:
1. [Improvement Tip 1 - max 80 characters]
2. [Improvement Tip 2 - max 80 characters]
3. [Improvement Tip 3 - max 80 characters]
4. [Improvement Tip 4 - max 80 characters]

[Add a short, witty closing remark or metaphor]

Remember to address the candidate directly using "you" and maintain an encouraging tone throughout.
"""


def main():
    st.set_page_config(
        page_title="ResumeWorth - Resume Value Estimator", page_icon="💼", layout="wide"
    )

    st.title("💼 ResumeWorth - Resume Value Estimator")
    st.markdown(
        """
    Curious about your market value? Let our AI career coach analyze your resume and provide 
    a fun, insightful estimation of your worth in the current job market!
    """
    )

    st.subheader("📤 Upload Your Resume")
    uploaded_file = st.file_uploader("Choose your resume (PDF format)", type="pdf")

    if st.button("💰 Estimate My Worth", type="primary"):
        if uploaded_file is not None:
            with st.spinner(
                "Analyzing your resume... Preparing for a value revelation!"
            ):
                extracted_text = extract_text_from_pdf(uploaded_file)
                response = model.generate_content(
                    input_prompt_worth.format(extracted_text=extracted_text)
                )

                st.success("Analysis complete!")
                st.subheader("🌟 Your Resume Worth Evaluation")

                # Estimated Worth
                st.markdown(response.text)
        else:
            st.error("Please upload a PDF resume to get your worth estimation.")

    st.markdown(
        "<div style='text-align: center; margin-top:10px;'>Made with ❤️ by <a style='color: #ffffff;' href='https://github.com/jessjohn1539' target='_blank'>Jess John</a></div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
