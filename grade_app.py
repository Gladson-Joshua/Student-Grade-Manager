import html

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Student Grade Manager",
    page_icon="🎓",
    layout="wide"
)

# Store student records during the Streamlit session
if "students" not in st.session_state:
    st.session_state.students = []
if "next_id" not in st.session_state:
    st.session_state.next_id = 1


# ---------- Styling (social-feed look) ----------
st.markdown("""
<style>
:root {
    --brand: #1877F2;
    --brand-dark: #166FE5;
    --page-bg: #F0F2F5;
    --card-bg: #FFFFFF;
    --text: #050505;
    --muted: #65676B;
    --divider: #E4E6EB;
}
.stApp { background: var(--page-bg); }
header[data-testid="stHeader"] { display: none; }
.block-container { padding-top: 4.5rem; max-width: 1200px; }

/* Top navigation bar */
.topbar {
    position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
    height: 56px; background: var(--card-bg);
    box-shadow: 0 1px 2px rgba(0,0,0,.15);
    display: flex; align-items: center; padding: 0 16px; gap: 10px;
}
.topbar .logo {
    width: 40px; height: 40px; border-radius: 50%;
    background: var(--brand); color: #fff;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
}
.topbar .title { font-size: 22px; font-weight: 700; color: var(--brand); }
.topbar .search {
    margin-left: 12px; background: var(--page-bg); border-radius: 20px;
    padding: 8px 14px; color: var(--muted); font-size: 14px;
}

/* Cards: any container whose key starts with "card" */
div[class*="st-key-card"] {
    background: var(--card-bg);
    border-radius: 8px;
    box-shadow: 0 1px 2px rgba(0,0,0,.2);
    padding: 12px 16px;
}
.card-title { font-size: 17px; font-weight: 700; color: var(--text); margin: 0 0 6px; }
.muted { color: var(--muted); font-size: 13px; }

/* Avatar + post header */
.avatar {
    width: 40px; height: 40px; border-radius: 50%;
    display: inline-flex; align-items: center; justify-content: center;
    color: #fff; font-weight: 700; font-size: 16px; flex-shrink: 0;
}
.post-head { display: flex; align-items: center; gap: 10px; }
.post-name { font-weight: 600; color: var(--text); font-size: 15px; line-height: 1.2; }
.post-body { margin: 10px 0 4px; color: var(--text); font-size: 15px; }
.grade-badge {
    display: inline-block; padding: 2px 10px; border-radius: 12px;
    font-weight: 700; font-size: 13px; color: #fff;
}
.bar { height: 8px; background: var(--divider); border-radius: 4px; overflow: hidden; }
.bar > div { height: 100%; border-radius: 4px; }

/* Sidebar shortcut rows */
.shortcut {
    display: flex; align-items: center; gap: 10px;
    padding: 8px 6px; border-radius: 8px; color: var(--text); font-weight: 500;
}
.shortcut .icon {
    width: 36px; height: 36px; border-radius: 50%; background: var(--divider);
    display: flex; align-items: center; justify-content: center; font-size: 18px;
}
.stat-row { display: flex; justify-content: space-between; padding: 6px 0;
            border-bottom: 1px solid var(--divider); font-size: 15px; }
.stat-row:last-child { border-bottom: none; }
.stat-row b { color: var(--text); }

/* Primary (blue) buttons */
button[kind="primaryFormSubmit"], button[kind="primary"] {
    background: var(--brand) !important; border-color: var(--brand) !important;
    font-weight: 600;
}
button[kind="primaryFormSubmit"]:hover, button[kind="primary"]:hover {
    background: var(--brand-dark) !important;
}
/* Rounded "What's on your mind" style input */
div[class*="st-key-card_composer"] input {
    border-radius: 20px !important; background: var(--page-bg) !important;
}
</style>
<div class="topbar">
    <div class="logo">🎓</div>
    <div class="title">gradebook</div>
    <div class="search">🔍 Student Grade Manager</div>
</div>
""", unsafe_allow_html=True)


# ---------- Logic ----------
GRADE_COLORS = {
    "A": "#31A24C",
    "B": "#1877F2",
    "C": "#F7B928",
    "D": "#F02849",
    "E": "#8A8D91",
}
AVATAR_COLORS = ["#1877F2", "#31A24C", "#F7B928", "#F02849", "#9360F7", "#FF7A00"]
MAX_NAME_LENGTH = 50


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


def initials(name):
    parts = name.split()
    letters = [p[0] for p in parts if p[0].isalpha()][:2]
    return "".join(letters).upper() or "?"


def avatar_html(name, size=40):
    color = AVATAR_COLORS[sum(map(ord, name)) % len(AVATAR_COLORS)]
    return (f'<div class="avatar" style="background:{color};width:{size}px;'
            f'height:{size}px;">{html.escape(initials(name))}</div>')


def delete_student(student_id):
    st.session_state.students = [
        s for s in st.session_state.students if s["id"] != student_id
    ]


# ---------- Layout ----------
left, center, right = st.columns([1, 2, 1], gap="medium")

# Left column: shortcuts
with left:
    with st.container(key="card_shortcuts"):
        st.markdown("""
        <div class="shortcut"><div class="icon">🎓</div>Student Grade Manager</div>
        <div class="shortcut"><div class="icon">➕</div>Add students</div>
        <div class="shortcut"><div class="icon">📋</div>Student feed</div>
        <div class="shortcut"><div class="icon">📊</div>Class summary</div>
        """, unsafe_allow_html=True)

    with st.container(key="card_scale"):
        st.markdown('<p class="card-title">Grading scale</p>', unsafe_allow_html=True)
        scale = [("A", "90–100"), ("B", "80–89"), ("C", "70–79"), ("D", "60–69"), ("E", "0–59")]
        st.markdown("".join(
            f'<div class="stat-row"><span><span class="grade-badge" '
            f'style="background:{GRADE_COLORS[g]}">{g}</span></span><b>{rng}</b></div>'
            for g, rng in scale
        ), unsafe_allow_html=True)

# Center column: composer + feed
with center:
    with st.container(key="card_composer"):
        with st.form("student_form", clear_on_submit=True, border=False):
            st.markdown('<p class="card-title">Add a student</p>', unsafe_allow_html=True)
            name = st.text_input(
                "Student Name",
                placeholder="Who are you adding today?",
                label_visibility="collapsed",
            )
            c1, c2 = st.columns([2, 1], vertical_alignment="bottom")
            mark = c1.number_input(
                "Student Mark", min_value=0, max_value=100, value=50, step=1
            )
            submitted = c2.form_submit_button("Post", type="primary", width="stretch")

        if submitted:
            clean_name, error = validate_name(name)
            if error:
                st.error(error)
            else:
                st.session_state.students.append({
                    "id": st.session_state.next_id,
                    "Name": clean_name,
                    "Mark": mark,
                    "Grade": get_grade(mark),
                })
                st.session_state.next_id += 1
                st.success(f"{clean_name} added successfully!")

    if not st.session_state.students:
        with st.container(key="card_empty"):
            st.markdown(
                '<p class="card-title">No students yet</p>'
                '<p class="muted">Posts appear here when you add a student.</p>',
                unsafe_allow_html=True,
            )

    # Newest first, like a feed
    for s in reversed(st.session_state.students):
        with st.container(key=f"card_post_{s['id']}"):
            head, menu = st.columns([6, 1], vertical_alignment="center")
            head.markdown(
                f'<div class="post-head">{avatar_html(s["Name"])}'
                f'<div><div class="post-name">{html.escape(s["Name"])}</div>'
                f'<div class="muted">Student · Mark recorded</div></div></div>',
                unsafe_allow_html=True,
            )
            menu.button(
                "✕", key=f"del_{s['id']}", help="Remove student",
                on_click=delete_student, args=(s["id"],), type="tertiary",
            )
            color = GRADE_COLORS[s["Grade"]]
            st.markdown(
                f'<div class="post-body">Scored <b>{s["Mark"]}/100</b> &nbsp;'
                f'<span class="grade-badge" style="background:{color}">Grade {s["Grade"]}</span></div>'
                f'<div class="bar"><div style="width:{s["Mark"]}%;background:{color}"></div></div>',
                unsafe_allow_html=True,
            )

# Right column: class summary
with right:
    with st.container(key="card_summary"):
        st.markdown('<p class="card-title">Class summary</p>', unsafe_allow_html=True)
        if st.session_state.students:
            df = pd.DataFrame(st.session_state.students)
            st.markdown(f"""
            <div class="stat-row"><span>Students</span><b>{len(df)}</b></div>
            <div class="stat-row"><span>Average</span><b>{df["Mark"].mean():.1f}</b></div>
            <div class="stat-row"><span>Highest</span><b>{df["Mark"].max()}</b></div>
            <div class="stat-row"><span>Lowest</span><b>{df["Mark"].min()}</b></div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<p class="muted">Add students to see statistics.</p>',
                        unsafe_allow_html=True)

    if st.session_state.students:
        with st.container(key="card_table"):
            st.markdown('<p class="card-title">All results</p>', unsafe_allow_html=True)
            st.dataframe(
                df[["Name", "Mark", "Grade"]], width="stretch", hide_index=True
            )
            if st.button("Clear All Students", width="stretch"):
                st.session_state.students = []
                st.rerun()
