import streamlit as st
import sqlite3
from datetime import datetime

# Function to create a connection to the SQLite database
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('hospital.db')
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

# Function to create tables in the database
def create_tables(conn):
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS patients 
                     (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, gender TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS doctors 
                     (id INTEGER PRIMARY KEY, name TEXT, specialization TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS appointments 
                     (id INTEGER PRIMARY KEY, patient_id INTEGER, doctor_id INTEGER, date TEXT, time TEXT, 
                     FOREIGN KEY(patient_id) REFERENCES patients(id), FOREIGN KEY(doctor_id) REFERENCES doctors(id))''')
    except sqlite3.Error as e:
        print(e)

# Function to add a patient
def add_patient(conn, name, age, gender):
    try:
        c = conn.cursor()
        c.execute('''INSERT INTO patients (name, age, gender) VALUES (?, ?, ?)''', (name, age, gender))
        conn.commit()
        st.success('Patient added successfully!')
    except sqlite3.Error as e:
        print(e)
        st.error('Error adding patient')

# Function to add a doctor
def add_doctor(conn, name, specialization):
    try:
        c = conn.cursor()
        c.execute('''INSERT INTO doctors (name, specialization) VALUES (?, ?)''', (name, specialization))
        conn.commit()
        st.success('Doctor added successfully!')
    except sqlite3.Error as e:
        print(e)
        st.error('Error adding doctor')

# Function to schedule an appointment
def schedule_appointment(conn, patient_id, doctor_id, date, time):
    try:
        c = conn.cursor()
        c.execute('''INSERT INTO appointments (patient_id, doctor_id, date, time) VALUES (?, ?, ?, ?)''', 
                  (patient_id, doctor_id, date, time))
        conn.commit()
        st.success('Appointment scheduled successfully!')
    except sqlite3.Error as e:
        print(e)
        st.error('Error scheduling appointment')

# Function to fetch data from the database
def fetch_data(conn, table):
    try:
        c = conn.cursor()
        c.execute('''SELECT * FROM {}'''.format(table))
        rows = c.fetchall()
        return rows
    except sqlite3.Error as e:
        print(e)

# Main function
def main():
    st.title('Hospital Management System')

    # Create a database connection and tables
    conn = create_connection()
    if conn is not None:
        create_tables(conn)
    else:
        st.error('Error creating database connection')

    # Sidebar navigation
    menu = ['Home', 'Add Patient', 'Add Doctor', 'Schedule Appointment']
    choice = st.sidebar.selectbox('Menu', menu)

    # Display selected page
    if choice == 'Home':
        st.subheader('Home Page')
        st.write('Welcome to the Hospital Management System!')

    elif choice == 'Add Patient':
        st.subheader('Add Patient')
        name = st.text_input('Name')
        age = st.number_input('Age', min_value=0, max_value=150)
        gender = st.selectbox('Gender', ['Male', 'Female', 'Other'])
        if st.button('Add Patient'):
            if name and age and gender:
                add_patient(conn, name, age, gender)
            else:
                st.warning('Please provide all information')

    elif choice == 'Add Doctor':
        st.subheader('Add Doctor')
        name = st.text_input('Name')
        specialization = st.text_input('Specialization')
        if st.button('Add Doctor'):
            if name and specialization:
                add_doctor(conn, name, specialization)
            else:
                st.warning('Please provide all information')

    elif choice == 'Schedule Appointment':
        st.subheader('Schedule Appointment')
        patients = fetch_data(conn, 'patients')
        doctors = fetch_data(conn, 'doctors')

        patient_names = [row[1] for row in patients]
        doctor_names = [row[1] for row in doctors]

        patient_name = st.selectbox('Patient', patient_names)
        doctor_name = st.selectbox('Doctor', doctor_names)
        date = st.date_input('Date', min_value=datetime.today())
        time = st.time_input('Time')

        patient_id = patients[patient_names.index(patient_name)][0]
        doctor_id = doctors[doctor_names.index(doctor_name)][0]

        if st.button('Schedule Appointment'):
            schedule_appointment(conn, patient_id, doctor_id, date.strftime('%Y-%m-%d'), time.strftime('%H:%M'))

if __name__ == '__main__':
    main()
