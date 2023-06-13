import tkinter as tk
import mysql.connector
from demo import fingerprint_matching_score

myuidai = None

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkcalendar import DateEntry
import mysql.connector
from mysql.connector import Error





def check_uidai():
    global myuidai
    myuidai = uidai_entry.get()
    score = fingerprint_matching_score(myuidai)
    if score > 3:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="uni_db"
        )  # Connect to the MySQL database
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pancard WHERE UIDAI=%s", (myuidai,))
        row = cursor.fetchone()
        if row is None:
            result_label.config(text="Pan Card not found")
            add_button.config(state=tk.NORMAL)
        else:
            result_label.config(text="Pan Card found")
            update_button.config(state=tk.NORMAL)
        conn.close()
    else:
        result_label.config(text="Fingerprint matching score is less than 3")


def add_uidai():
    uidai = uidai_entry.get()
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="uni_db"
    )  # Connect to the MySQL database
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pancard (UIDAI) VALUES (%s)", (uidai,))
    conn.commit()
    conn.close()
    result_label.config(text="Pan Card added to database")
    add_button.config(state=tk.DISABLED)
    update_button.config(state=tk.DISABLED)


def AddAadharcard():
    def submit_data():
        # Function to handle submit button click event
        global myuidai
        name = name_entry.get()
        father_name = father_name_entry.get()
        mobile_no = mobile_no_entry.get()
        dob = dob_entry.get_date().strftime('%Y-%m-%d')
        aadhar_file_path = file_path.get()
        with open(aadhar_file_path, 'rb') as file:
            aadhar_card = file.read()

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="uni_db"
            )  # Connect to the MySQL database
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO pancard (UIDAI, Name, father_name, MobileNo, DOB, pan_card) VALUES (%s, %s, %s, %s, %s, %s)",
                (myuidai, name, father_name, mobile_no, dob, aadhar_card,))
            conn.commit()
            conn.close()
            result_label.config(text="Data inserted successfully")
        except Error as e:
            print("Error inserting data: ", e)
            result_label.config(text="Error inserting data")

    # Create main window
    root = tk.Tk()
    root.title("Add Pan Card")
    root.geometry("400x300")  # Set window height and width

    # Create Name entry field
    name_label = tk.Label(root, text="Name:")
    name_label.pack()
    name_entry = tk.Entry(root)
    name_entry.pack()

    # Create Father Name entry field
    father_name_label = tk.Label(root, text="Father's Name:")
    father_name_label.pack()
    father_name_entry = tk.Entry(root)
    father_name_entry.pack()

    # Create Mobile No entry field
    mobile_no_label = tk.Label(root, text="Mobile No:")
    mobile_no_label.pack()
    mobile_no_entry = tk.Entry(root)
    mobile_no_entry.pack()

    # Create DOB calendar entry field
    dob_label = tk.Label(root, text="Date of Birth:")
    dob_label.pack()
    dob_entry = DateEntry(root, width=12, background='darkblue',
                           foreground='white', date_pattern='yyyy-mm-dd')
    dob_entry.pack()

    # Create Aadhar Card file selection button
    aadhar_file_label = tk.Label(root, text="Pan Card:")
    aadhar_file_label.pack()
    file_path = tk.StringVar()
    file_selection_button = tk.Button(root, text="Select Pan Card", command=lambda: file_path.set(filedialog.askopenfilename()))
    file_selection_button.pack()

    # Create Submit button
    submit_button = tk.Button(root, text="Submit", command=submit_data)
    submit_button.pack()

    # Create result label
    result_label = tk.Label(root, text="")
    result_label.pack()

    root.mainloop()


def update_data(myuidai):
    # Create the GUI window
    window = tk.Tk()
    window.title("Update Data")

    # Create labels and entry fields
    tk.Label(window, text="Name:").grid(row=0, column=0, sticky="E")
    name_entry = tk.Entry(window)
    name_entry.grid(row=0, column=1)

    tk.Label(window, text="Date of Birth:").grid(row=1, column=0, sticky="E")
    dob_entry = DateEntry(window)
    dob_entry.grid(row=1, column=1)

    tk.Label(window, text="Father's Name:").grid(row=2, column=0, sticky="E")
    father_entry = tk.Entry(window)
    father_entry.grid(row=2, column=1)

    tk.Label(window, text="Mobile No.:").grid(row=3, column=0, sticky="E")
    mobile_entry = tk.Entry(window)
    mobile_entry.grid(row=3, column=1)

    def select_file():
        file_path = filedialog.askopenfilename()
        file_label.config(text=file_path)

    tk.Label(window, text="Select File:").grid(row=4, column=0, sticky="E")
    file_label = tk.Label(window, text="")
    file_label.grid(row=4, column=1, sticky="W")
    select_file_button = tk.Button(window, text="Browse", command=select_file)
    select_file_button.grid(row=4, column=2)

    def update():
    # Get user input values
        name = name_entry.get()
        dob = dob_entry.get_date().strftime('%Y-%m-%d')  # Convert date format
        father_name = father_entry.get()
        mobile_no = mobile_entry.get()
        file_path = file_label.cget("text")

    # Update the database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="uni_db"
        )
        cursor = connection.cursor()
        sql = "UPDATE pancard SET Name = %s, DOB = %s, father_name = %s, MobileNo = %s, pan_card = %s WHERE UIDAI = %s"
        with open(file_path, "rb") as file:
            aadhar_card = file.read()
        values = (name, dob, father_name, mobile_no, aadhar_card, myuidai)
        cursor.execute(sql, values)
        connection.commit()

    # Close the database connection
        cursor.close()
        connection.close()

    # Close the GUI window
        window.destroy()
    

    update_button = tk.Button(window, text="Update", command=update)
    update_button.grid(row=5, column=0, columnspan=2)

    # Start the GUI event loop
    window.mainloop()

# Example usage



# Create main window
root = tk.Tk()
root.title("Pan Card Update/Add")
root.geometry("400x200")  # Set window height and width

# Create UIDAI entry field
uidai_entry = tk.Entry(root)
uidai_entry.pack()

# Create Submit button
submit_button = tk.Button(root, text="Submit", command=check_uidai)
submit_button.pack()

# Create result label
result_label = tk.Label(root, text="")
result_label.pack()

# Create Add button
# Create Add button
add_button = tk.Button(root, text="Add Pan Card",
                       command=AddAadharcard, state=tk.DISABLED)
add_button.pack()

# Create Update button
update_button = tk.Button(root, text="Update Data", command=lambda: update_data(myuidai), state=tk.DISABLED)
update_button.pack()


root.mainloop()
