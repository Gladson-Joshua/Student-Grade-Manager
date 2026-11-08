
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Student Grade Manager",
    page_icon="🎓",
    layout="centered"
)

# Store student records during the Streamlit session
if "students" not in st.session_state:
    st.session_state.students = []


def get_grade(mark):
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "E"


st.title("🎓 Student Grade Manager")
st.write("Add students, calculate grades, and view class performance.")

# Add student form
with st.form("student_form"):
    name = st.text_input("Student Name")
    mark = st.number_input(
        "Student Mark",
        min_value=0,
        max_value=100,
        value=50,
        step=1
    )

    submitted = st.form_submit_button("Add Student")

    if submitted:
        if not name.strip():
            st.error("Please enter a student name.")
        else:
            st.session_state.students.append({
                "Name": name.strip(),
                "Mark": mark,
                "Grade": get_grade(mark)
            })
            st.success(f"{name.strip()} added successfully!")

# Show student results
st.subheader("Student Results")

if st.session_state.students:
    df = pd.DataFrame(st.session_state.students)

    st.dataframe(df, use_container_width=True, hide_index=True)

    average = df["Mark"].mean()
    highest = df["Mark"].max()
    lowest = df["Mark"].min()

    col1, col2, col3 = st.columns(3)

    col1.metric("Average", f"{average:.1f}")
    col2.metric("Highest", highest)
    col3.metric("Lowest", lowest)

    if st.button("Clear All Students"):
        st.session_state.students = []
        st.rerun()
else:
    st.info("No students added yet.")
