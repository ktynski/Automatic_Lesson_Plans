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
    .sidebar .sidebar-content {
        background-color: #f0f0f0;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("Lesson Plan Generator")

grade_levels = [f"Grade {i}" for i in range(1, 13)] + ["Kindergarten"]
subjects = ["Math", "Science", "English", "History", "Social Studies"]
durations = ["30 minutes", "45 minutes", "60 minutes", "90 minutes"]
complexity_levels = ["Beginner", "Intermediate", "Advanced"]

with st.sidebar:
    st.header("API Key")
    openai.api_key = st.text_input("Enter your OpenAI API Key", type="password")
    st.header("Input Options")
    grade_level = st.selectbox("Grade Level", options=grade_levels)
    subject = st.selectbox("Subject", options=subjects)
    topic = st.text_input("Topic")
    duration = st.selectbox("Duration", options=durations)
    complexity = st.selectbox("Complexity Level", options=complexity_levels)
    techniques = st.multiselect("Pedagogical Techniques", options=["Bloom's Taxonomy", "Project-Based Learning", "Differentiated Instruction", "Inquiry-Based Learning"])
    learning_styles = st.multiselect("Learning Styles", options=["Visual", "Auditory", "Kinesthetic"])



def prompt_user_input():
    grade_level = input("Enter the grade level (K-12): ")
    subject = input("Enter the subject: ")
    topic = input("Enter the topic: ")
    duration = input("Enter the duration of the lesson (in minutes): ")
    techniques = input("Enter the pedagogical techniques (comma-separated): ")
    complexity = input("Enter the complexity level (beginner, intermediate, advanced): ")
    learning_styles = input("Enter the learning styles to target (comma-separated): ")
    return grade_level, subject, topic, duration, techniques, complexity, learning_styles


def generate_lesson_plan(grade_level, subject, topic, duration, techniques, complexity, learning_styles):    # Check the length of the transcript
    
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


def save_lesson_plan(lesson_plan, filename):
    with open(filename, "w") as f:
        f.write(lesson_plan)



def generate_class_materials(lesson_plan):
    prompt = f"Based on the following lesson plan, generate class materials, including handouts, slides, and activity sheets:\n\n{lesson_plan}\n"
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=3900,
        n=1,
        stop=None,
        temperature=0.8,
    )

    class_materials = response.choices[0].text.strip()
    return class_materials


if st.button("Generate Lesson Plan"):
    if not topic:
        st.error("Please enter a topic.")
    else:
        lesson_plan = generate_lesson_plan(grade_level, subject, topic, duration, techniques, complexity, learning_styles)
        st.header("Generated Lesson Plan")
        st.write(lesson_plan)

        if st.button("Generate Class Materials"):
            class_materials = generate_class_materials(lesson_plan)
            st.header("Generated Class Materials")
            st.write(class_materials)

