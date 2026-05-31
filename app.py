import streamlit as st
import pandas as pd
import sqlite3
from datetime import date

# Database
conn = sqlite3.connect("health.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS patients (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
dob TEXT,
email TEXT,
glucose REAL,
haemoglobin REAL,
cholesterol REAL,
remarks TEXT
)
""")
conn.commit()

# Prediction Function
def predict_health(glucose, haemoglobin, cholesterol):
    if glucose > 140:
        return "High Diabetes Risk"
    elif cholesterol > 240:
        return "High Cholesterol Risk"
    elif haemoglobin < 12:
        return "Possible Anemia"
    else:
        return "Healthy"

st.title("Health Prediction Application")

menu = ["Create", "View", "Update", "Delete"]
choice = st.sidebar.selectbox("Menu", menu)

# CREATE
if choice == "Create":
    st.subheader("Add Patient")

    name = st.text_input("Full Name")
    dob = st.date_input("Date of Birth")
    email = st.text_input("Email")
    glucose = st.number_input("Glucose", min_value=0.0)
    haemoglobin = st.number_input("Haemoglobin", min_value=0.0)
    cholesterol = st.number_input("Cholesterol", min_value=0.0)

    if st.button("Save"):
        remarks = predict_health(glucose, haemoglobin, cholesterol)

        c.execute("""
        INSERT INTO patients
        (name,dob,email,glucose,haemoglobin,cholesterol,remarks)
        VALUES (?,?,?,?,?,?,?)
        """,
        (name,str(dob),email,glucose,haemoglobin,cholesterol,remarks))

        conn.commit()
        st.success("Patient Added Successfully")
        st.write("Prediction:", remarks)

# VIEW
elif choice == "View":
    st.subheader("Patient Records")

    df = pd.read_sql_query("SELECT * FROM patients", conn)
    st.dataframe(df)

# UPDATE
elif choice == "Update":
    st.subheader("Update Record")

    ids = pd.read_sql_query(
        "SELECT id FROM patients", conn
    )

    if len(ids) > 0:
        selected_id = st.selectbox(
            "Select ID", ids["id"]
        )

        if st.button("Update Prediction"):
            c.execute("""
            UPDATE patients
            SET remarks='Updated'
            WHERE id=?
            """, (selected_id,))
            conn.commit()

            st.success("Updated Successfully")

# DELETE
elif choice == "Delete":
    st.subheader("Delete Record")

    ids = pd.read_sql_query(
        "SELECT id FROM patients", conn
    )

    if len(ids) > 0:
        selected_id = st.selectbox(
            "Select ID", ids["id"]
        )

        if st.button("Delete"):
            c.execute(
                "DELETE FROM patients WHERE id=?",
                (selected_id,)
            )
            conn.commit()

            st.success("Deleted Successfully")