import openai
import os
import streamlit as st

# Custom color scheme
st.markdown(
    """
<style>
    .reportview-container {
        background-color: #f0f0f0;
    }
    .main {
        background-color: #f0f0f0;
    }
    h2 {
        color: #0080FF;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("Lesson Plan & Class Materials Generator")

with st.sidebar:
    st.header("API Key")
    openai.api_key = st.text_input("Enter your OpenAI API Key", type="password")

grade_levels = [f"Grade {i}" for i in range(1, 13)] + ["Kindergarten"]
subjects = ["Math", "Science", "English", "History", "Social Studies"]
durations = ["30 minutes", "45 minutes", "60 minutes", "90 minutes"]
complexity_levels = ["Beginner", "Intermediate", "Advanced"]

# Input options
cols = st.beta_columns(4)
grade_level = cols[0].selectbox("Grade Level", options=grade_levels)
subject = cols[1].selectbox("Subject", options=subjects)
duration = cols[2].selectbox("Duration", options=durations)
complexity = cols[3].selectbox("Complexity Level", options=complexity_levels)
techniques = st.multiselect("Pedagogical Techniques", options=["Bloom's Taxonomy", "Project-Based Learning", "Differentiated Instruction", "Inquiry-Based Learning"])
learning_styles = st.multiselect("Learning Styles", options=["Visual", "Auditory", "Kinesthetic"])

def generate_lesson_plan_and_materials(grade_level, subject, topic, duration, techniques, complexity, learning_styles):
    techniques_str = ', '.join(techniques)
    learning_styles_str = ', '.join(learning_styles)
    prompt = f"Create a lesson plan and corresponding class materials for a {complexity} {subject} lesson on '{topic}' for {grade_level} students. The lesson should be {duration} long and incorporate the following pedagogical techniques: {techniques_str}. It should cater to the following learning styles: {learning_styles_str}. Please provide a well-organized lesson plan with a clear hierarchy, sections, and detailed instructions, followed by the class materials."
    
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.8,
    )

    output = response.choices[0].text.strip()
    return output

if st.button("Generate Lesson Plan & Class Materials"):
    if not topic:
        st.error("Please enter a topic.")
    else:
        try:
            output = generate_lesson_plan_and_materials(grade_level, subject, topic, duration, techniques, complexity, learning_styles)
            lesson_plan, class_materials = output.split('\n\nClass Materials\n\n')
            st.header("Generated Lesson Plan")
            st.write(lesson_plan)
            st.header("Generated Class Materials")
            st.write(class_materials)
        except Exception as e:
            st.error(f"An error occurred while generating the lesson plan and class materials. Please make sure you have entered a valid API key and try again. Error: {e}")
