import tkinter as tk
from tkinter import filedialog
import mysql.connector
from datetime import date

# Create a GUI window using Tkinter
window = tk.Tk()
window.title("Medical Document Upload")

# Create labels and entry fields for user input
uidai_label = tk.Label(text="Enter your 12 digit UIDAI number: ")
uidai_entry = tk.Entry(width=20)

hospital_label = tk.Label(text="Enter hospital code: ")
hospital_entry = tk.Entry(width=20)

disease_label = tk.Label(text="Enter disease name: ")
disease_entry = tk.Entry(width=20)

# Define a function to upload the data to the MySQL database
def upload_data():
    # Get user input from the entry fields
    uidai = uidai_entry.get()
    hospital_code = hospital_entry.get()
    disease_name = disease_entry.get()
    file_path = file_path_label.cget("text")
    upload_date = date.today()

    # Read the binary data from the selected file
    with open(file_path, "rb") as file:
        blob_data = file.read()

    # Connect to the MySQL database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="uni_db"
    )
    cursor = db.cursor()

    # Define the SQL query and insert the data into the 'medicaldoc' table
    query = "INSERT INTO medicaldoc (UIDAI, HospitalCode, Records, Daterec, Filename) VALUES (%s, %s, %s, %s, %s)"
    values = (uidai, hospital_code, blob_data, upload_date, disease_name)
    cursor.execute(query, values)

    # Commit the changes to the database and close the connection
    db.commit()
    db.close()

    # Display a message to the user confirming successful upload
    tk.messagebox.showinfo("Success", "Data uploaded successfully!")

# Create a label and button to allow users to upload a file
file_path_label = tk.Label(text="")
def browse_file():
    file_path = filedialog.askopenfilename()
    file_path_label.config(text=file_path)

browse_button = tk.Button(text="Browse", command=browse_file)

# Create a button to submit the data and call the upload_data() function
submit_button = tk.Button(text="Submit", command=upload_data)

# Pack the labels, entry fields, and buttons into the window
uidai_label.pack()
uidai_entry.pack()
hospital_label.pack()
hospital_entry.pack()
disease_label.pack()
disease_entry.pack()
browse_button.pack()
file_path_label.pack()
submit_button.pack()

# Run the main loop of the GUI window
window.mainloop()
