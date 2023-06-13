import mysql.connector
from tkinter import *
from tkinter import messagebox
import tempfile
import os
from demo import fingerprint_matching_score

# Connect to the MySQL database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="uni_db"
)

# Create a cursor object to execute SQL queries
mycursor = mydb.cursor()

# Create a function to handle the button click event
# Create a function to handle the button click event
def show_records(uidai):
    # Call the fingerprint_matching_score function to get the score
    score = fingerprint_matching_score(uidai)
    
    # Check if the score is greater than 3
    if score > 3:
        # Execute the SQL query to select the records for the given UIDAI number
        mycursor.execute("SELECT Daterec, Filename, UIDAI FROM medicaldoc WHERE UIDAI = %s", (uidai,))
        records = mycursor.fetchall()

        # Create a new window to display the records in a table
        table_window = Tk()

        # Set the window title and dimensions
        table_window.title("Medical Records for UIDAI: " + uidai)
        table_window.geometry("500x500")

        # Create a table header
        header = ["Date", "Treatment", "Option"]
        for i in range(len(header)):
            Label(table_window, text=header[i], relief="solid", width=15).grid(row=0, column=i)

        # Loop through the records and display them in the table
        for i in range(len(records)):
            # Add a new row to the table
            row = i + 1

            # Add the date to the table
            date_label = Label(table_window, text=records[i][0], relief="solid", width=15)
            date_label.grid(row=row, column=0)

            # Add the treatment to the table
            treatment_label = Label(table_window, text=records[i][1], relief="solid", width=15)
            treatment_label.grid(row=row, column=1)

            # Add a button to fetch the records for this row
            def fetch_records(uidai=uidai, daterec=records[i][0], filename=records[i][1]):
                # Execute the SQL query to select the records for the given UIDAI, date and treatment
                mycursor.execute("SELECT Records FROM medicaldoc WHERE UIDAI = %s AND Daterec = %s AND Filename = %s", (uidai, daterec, filename))
                result = mycursor.fetchone()

                # Create a temporary file to write the BLOB data
                with tempfile.TemporaryFile(suffix='.pdf', delete=False) as temp_file:
                    # Write the BLOB data to the temporary file
                    temp_file.write(result[0])

                    # Open the PDF file in the default PDF viewer
                    os.startfile(temp_file.name)

            fetch_button = Button(table_window, text="Fetch", command=lambda uidai=uidai, daterec=records[i][0], filename=records[i][1]: fetch_records(uidai, daterec, filename), relief="solid", width=15)
            fetch_button.grid(row=row, column=2)

        # Start the event loop for the new window
        table_window.mainloop()
    else:
        messagebox.showwarning("Invalid UIDAI", "The UIDAI number is not valid.")


# Create a new window to prompt the user for their UIDAI number
uidai_window = Tk()

# Set the window title and dimensions
uidai_window.title("Medical Records.")
uidai_window.geometry("250x100")

# Create a label and entry field for the UIDAI number
Label(uidai_window, text="UIDAI Number:").grid(row=0, column=0)
uidai_entry = Entry(uidai_window, width=20)
uidai_entry.grid(row=0, column=1)

# Create a button to submit the UIDAI number and show the records
submit_button = Button(uidai_window, text="Submit", command=lambda: show_records(uidai_entry.get()))
submit_button.grid(row=1, column=0, columnspan=2)

uidai_window.mainloop()

mydb.close()
