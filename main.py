import streamlit as st
import pandas as pd
import random

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Timetable Generator",
    page_icon="📅",
    layout="wide"
)

st.title("📅 AI Automated College Timetable Generator")
st.markdown("Generate a **conflict-free weekly timetable** using AI logic.")

# ---------------------------------------------------
# Days & Teaching Time Slots
# ---------------------------------------------------

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# Teaching periods only
teaching_slots = [
    "09:00–09:50",
    "09:50–10:40",
    "10:50–11:40",
    "11:40–12:30",
    "01:20–02:10",
    "02:10–03:00",
    "03:10–04:00",
    "04:00–04:50"
]

periods_per_day = len(teaching_slots)

# ---------------------------------------------------
# Sidebar Inputs
# ---------------------------------------------------

st.sidebar.header("⚙️ Timetable Configuration")

st.sidebar.write("Days:", days)
st.sidebar.write("College Timing: 9:00 AM – 4:50 PM")

# Subjects
st.sidebar.subheader("Subjects")

subjects = []
for i in range(6):
    sub = st.sidebar.text_input(f"Subject {i+1}", key=f"sub{i}")
    if sub:
        subjects.append(sub)

# Labs
st.sidebar.subheader("Labs")

labs = []
for i in range(3):
    lab = st.sidebar.text_input(f"Lab {i+1}", key=f"lab{i}")
    if lab:
        labs.append(lab)

# ---------------------------------------------------
# Helper Function
# Prevent Consecutive Subjects
# ---------------------------------------------------

def get_non_repeating_subject(prev_subject, subjects):

    available = [s for s in subjects if s != prev_subject]

    if not available:
        return random.choice(subjects)

    return random.choice(available)

# ---------------------------------------------------
# Generate Timetable
# ---------------------------------------------------

if st.button("🚀 Generate Timetable"):

    if not subjects or not labs:

        st.warning("⚠️ Please enter at least one subject and one lab!")

    else:

        # Assign labs to random days
        available_days = days.copy()
        random.shuffle(available_days)

        lab_assignments = {}

        for lab in labs:
            if available_days:
                lab_assignments[lab] = available_days.pop(0)

        timetable = []

        # Generate Rows
        for day in days:

            row = [""] * periods_per_day
            prev_subject = None

            lab_today = None

            for lab, assigned_day in lab_assignments.items():
                if assigned_day == day:
                    lab_today = lab
                    break

            # Place Lab Randomly (3 continuous)
            if lab_today:

                lab_start = random.randint(
                    0,
                    periods_per_day - 3
                )

                for i in range(
                    lab_start,
                    lab_start + 3
                ):
                    row[i] = lab_today

            # Fill Subjects
            for p in range(periods_per_day):

                if row[p] == "":

                    subject = get_non_repeating_subject(
                        prev_subject,
                        subjects
                    )

                    row[p] = subject
                    prev_subject = subject

                else:
                    prev_subject = row[p]

            timetable.append(row)

        # Create DataFrame
        df = pd.DataFrame(
            timetable,
            index=days,
            columns=teaching_slots
        )

        # ---------------------------------------------------
        # Insert Break Columns
        # ---------------------------------------------------

        df.insert(
            2,
            "Mini Break\n10:40–10:50",
            "BREAK"
        )

        df.insert(
            5,
            "Lunch Break\n12:30–01:20",
            "LUNCH"
        )

        df.insert(
            8,
            "Mini Break\n03:00–03:10",
            "BREAK"
        )

        st.success("✅ Timetable Generated Successfully!")

        # ---------------------------------------------------
        # Lab Distribution Info
        # ---------------------------------------------------

        lab_info = ", ".join(
            [f"{lab} on {day}"
             for lab, day in lab_assignments.items()]
        )

        st.info(f"📋 Lab Distribution: {lab_info}")

        # ---------------------------------------------------
        # HTML + CSS Styled Table
        # ---------------------------------------------------

        html_table = """
        <style>

        table {
            border-collapse: collapse;
            width: 100%;
            font-family: Arial;
        }

        th {
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            text-align: center;
        }

        td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: center;
            font-weight: bold;
        }

        .break {
            background-color: #FFD54F;
        }

        .lunch {
            background-color: #FF7043;
            color: white;
        }

        .day {
            background-color: #2196F3;
            color: white;
        }

        tr:nth-child(even) {
            background-color: #f2f2f2;
        }

        </style>
        """

        html_table += "<table>"

        # Header Row
        html_table += "<tr>"
        html_table += "<th>Day / Time</th>"

        for col in df.columns:
            html_table += f"<th>{col}</th>"

        html_table += "</tr>"

        # Data Rows
        for day in days:

            html_table += "<tr>"
            html_table += f"<td class='day'>{day}</td>"

            for value in df.loc[day]:

                if value == "BREAK":
                    html_table += "<td class='break'>BREAK</td>"

                elif value == "LUNCH":
                    html_table += "<td class='lunch'>LUNCH</td>"

                else:
                    html_table += f"<td>{value}</td>"

            html_table += "</tr>"

        html_table += "</table>"

        st.subheader("📊 Weekly Timetable")

        st.markdown(
            html_table,
            unsafe_allow_html=True
        )

        # ---------------------------------------------------
        # Download CSV
        # ---------------------------------------------------

        st.download_button(
            label="⬇ Download Timetable CSV",
            data=df.to_csv(),
            file_name="college_timetable.csv",
            mime="text/csv"
        )

# ---------------------------------------------------
# Footer
# ---------------------------------------------------

st.markdown("---")

st.markdown("✔ College Timing: 9:00 – 4:50")
st.markdown("✔ Mini Break: 10:40–10:50")
st.markdown("✔ Lunch Break: 12:30–01:20")
st.markdown("✔ Mini Break: 03:00–03:10")
st.markdown("✔ No consecutive subjects")
st.markdown("✔ Labs in 3 continuous periods")

