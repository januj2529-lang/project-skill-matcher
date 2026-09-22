import streamlit as st
import google.generativeai as genai

# 1. Fetch the API Key from secrets.toml automatically
try:
    GENAI_API_KEY = st.secrets["GENAI_API_KEY"]
    genai.configure(api_key=GENAI_API_KEY)
except Exception:
    st.error("⚠️ Could not find 'GENAI_API_KEY' inside your .streamlit/secrets.toml file.")

# 2. Function to ask the AI to perform the matching logic
def match_skills_to_project(student_skills, project_details):
    # Using 'gemini-1.5-flash' for robust alignment logic
    model = genai.GenerativeModel('gemini-3.6-flash')
    
    prompt = f"""
    You are an academic project coordinator. Match the student's skills to the project requirements.
    
    Student's Current Skills:
    {student_skills}
    
    Project Requirements & Description:
    {project_details}
    
    Analyze the inputs and provide a clear report with these exact sections:
    1. **Match Score**: Give a percentage (e.g., 85% or 0%) showing how well they fit.
    2. **Matching Skills**: List any skills the student has that fit the project.
    3. **Missing Skills**: List what the project needs but the student doesn't know.
    4. **What to Learn (If Match is Low/Zero)**: If the student doesn't know about the project, provide a simple, 3-step learning plan (with topics and estimated days) to help them catch up and successfully work on this project.
    """
    
    response = model.generate_content(prompt)
    return response.text

# 3. Designing the Web Page Interface
st.set_page_config(page_title="Project-Skill Matcher", layout="centered")
st.title("🤝 Project-Skill to Project Matcher")
st.write("Match a student to a project. If they don't know the skills, the AI will build a custom learning plan!")

student_input = st.text_area(
    "💡 Step 1: Enter Student Skills (e.g., Python, Graphic Design, HTML, or leave empty if beginner):", 
    height=100,
    placeholder="Example: I know basic Java and HTML, but I am a beginner at databases."
)

project_input = st.text_area(
    "📋 Step 2: Enter Project Details & Requirements:", 
    height=150,
    placeholder="Example: E-commerce Website Project. Needs React, Node.js, and SQL Database experience."
)

st.markdown("---")

# 4. Action button triggers the logic
if st.button("🚀 Match & Analyze", type="primary"):
    if project_input.strip() == "":
        st.warning("Please fill in the project details first!")
    else:
        with st.spinner("AI is calculating the match and creating a roadmap..."):
            try:
                skills_to_send = student_input.strip() if student_input.strip() != "" else "None (Absolute Beginner)"
                result = match_skills_to_project(skills_to_send, project_input)
                
                st.success("Analysis Generation Complete!")
                st.markdown("### 📊 AI Alignment Report")
                st.markdown(result)
                
            except Exception as e:
                st.error(f"Something went wrong: {e}. Check if your Gemini API key inside secrets.toml is correct.")
