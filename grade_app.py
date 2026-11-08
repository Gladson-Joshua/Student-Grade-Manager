
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


MAX_NAME_LENGTH = 50


def validate_name(raw_name):
    """Return (cleaned_name, error_message). error_message is None if valid."""
    # Collapse surrounding and repeated internal whitespace
    cleaned = " ".join(raw_name.split())

    if not cleaned:
        return cleaned, "Please enter a student name."
    if not any(ch.isalpha() for ch in cleaned):
        return cleaned, "Student name must contain at least one letter."
    if len(cleaned) > MAX_NAME_LENGTH:
        return cleaned, f"Student name must be {MAX_NAME_LENGTH} characters or fewer."

    existing = {s["Name"].casefold() for s in st.session_state.students}
    if cleaned.casefold() in existing:
        return cleaned, f"A student named '{cleaned}' has already been added."

    return cleaned, None


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
        clean_name, error = validate_name(name)
        if error:
            st.error(error)
        else:
            st.session_state.students.append({
                "Name": clean_name,
                "Mark": mark,
                "Grade": get_grade(mark)
            })
            st.success(f"{clean_name} added successfully!")

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
