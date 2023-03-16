import openai
import os
import streamlit as st

# Custom color scheme and styles
st.markdown(
    """
<style>
    .reportview-container {
        background-color: #f0f0f0;
    }
    .main {
        background-color: #f0f0f0;
    }
    h1 {
        color: #0080FF;
    }
    .stButton>button {
        background-color: #0080FF;
    }
    .expanderHeader {
        font-weight: bold;
    }
</style>
""",
    unsafe_allow_html=True,
)



subject_areas = [
    "Math",
    "Science",
    "English",
    "History",
    "Social Studies",
    "Art",
    "Music",
    "Physical Education",
    "Health",
    "Computer Science",
    "Foreign Language",
    "Environmental Science",
    "Geography",
    "Economics",
    "Psychology",
    "Philosophy",
    "Engineering",
    "Drama/Theater",
    "Creative Writing",
]

ped_techniques = [
    "Bloom's Taxonomy",
    "Project-Based Learning",
    "Differentiated Instruction",
    "Inquiry-Based Learning",
    "Socratic Method",
    "Gamification",
    "Cooperative Learning",
    "Flipped Classroom",
    "Problem-Based Learning",
    "Peer Teaching",
    "Concept Mapping",
    "Role-Playing",
    "Storytelling",
    "Self-Directed Learning",
    "Blended Learning",
    "Microlearning",
    "Mnemonic Techniques",
]




st.title("Lesson Plan & Class Materials Generator")

with st.beta_expander("Enter OpenAI API Key", expanded=True):
    openai.api_key = st.text_input("API Key", type="password")

grade_levels = [f"Grade {i}" for i in range(1, 13)] + ["Kindergarten"]
subjects= cols[1].selectbox("Subject", options=subject_areas)
durations = ["30 minutes", "45 minutes", "60 minutes", "90 minutes"]
complexity_levels = ["Beginner", "Intermediate", "Advanced"]

# Input options
st.markdown("### Select Options")
cols = st.beta_columns(4)
grade_level = cols[0].selectbox("Grade Level", options=grade_levels)
subject = cols[1].selectbox("Subject", options=subject_areas)
duration = cols[2].selectbox("Duration", options=durations)
complexity = cols[3].selectbox("Complexity Level", options=complexity_levels)
techniques = st.multiselect("Pedagogical Techniques", options=ped_techniques)
learning_styles = st.multiselect("Learning Styles", options=["Visual", "Auditory", "Kinesthetic"])

st.markdown("### Enter Topic")
topic = st.text_input("Topic")

    
def generate_lesson_plan_and_materials(grade_level, subject, topic, duration, techniques, complexity, learning_styles):    # Check the length of the transcript
    
      # Generate the summary using the OpenAI ChatCompletion API
      response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
              {"role": "system", "content": "You are an all-knowing AI that is extraordinarily creative and a world expert at k-12 teaching/learning. You specialize in creating customized lesson plans that are fun, engaging, and exciting to do. You will be helping write complex but effective lesson plans."},
              {"role": "user", "content": f"Please Create a lesson plan for a {complexity} {subject} lesson on '{topic}' for grade {grade_level} students. The lesson should be {duration} minutes long and incorporate the following pedagogical techniques: {techniques}. It should cater to the following learning styles: {learning_styles}. Please provide a well-organized lesson plan with a clear hierarchy, sections, and detailed instructions."},
              {"role": "system", "content": "Absolutely, I will provide a well organized lesson plan that fits this criteria and engages the student in a way that isnt boring, rote, or templated. I will incorporate all known best practices to create the maximally interesting lesson plan."},
              {"role": "user", "content": "Excellent, please continue and provide the lesson plan."}
          ],
          max_tokens=3500,
          n=1,
          stop=None,
          temperature=0.5,
      )

      # Extract the generated summary from the response
      lesson_plan = response['choices'][0]['message']['content']
      print(lesson_plan)
      return lesson_plan


def generate_class_materials(grade_level, subject, topic, duration, techniques, complexity, learning_styles, lesson_plan):
    techniques_str = ', '.join(techniques)
    learning_styles_str = ', '.join(learning_styles)
    prompt = f"Based on the following lesson plan for a {complexity} {subject} lesson on '{topic}' for {grade_level} students, create class materials:\n\n{lesson_plan}\n\nThe lesson should be {duration} long and incorporate the following pedagogical techniques: {techniques_str}. It should cater to the following learning styles: {learning_styles_str}. Please provide the class materials."
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
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
            lesson_plan = generate_lesson_plan_and_materials(grade_level, subject, topic, duration, techniques, complexity, learning_styles)
            class_materials = generate_class_materials(grade_level, subject, topic, duration, techniques, complexity, learning_styles, lesson_plan)
            st.header("Generated Lesson Plan")
            st.write(lesson_plan)
            st.header("Generated Class Materials")
            st.write(class_materials)
        except Exception as e:
            st.error(f"An error occurred while generating the lesson plan and class materials. Please make sure you have entered a valid API key and try again. Error: {e}")
