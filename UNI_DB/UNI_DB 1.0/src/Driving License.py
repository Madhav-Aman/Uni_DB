import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import io
import webbrowser
from demo import fingerprint_matching_score
import base64

def open_pdf_in_browser(data, filename):
    # Function to open PDF file in Google Chrome
    try:
        with open(filename, 'wb') as f:
            f.write(data)
        webbrowser.open(filename)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while opening the file: {str(e)}")

# Rest of the code...

def submit_form():
    uidai = uidai_entry.get()
    print("UIDAI:", uidai)
    if aadhar_var.get() == 0 and pan_var.get() == 0:
        messagebox.showwarning("No Documents Selected", "Please select at least one document.")
        return

    score = fingerprint_matching_score(uidai)
    if score < 3:
        messagebox.showwarning("Fingerprint Does Not Matched", "The fingerprint matching score is less than 3.")
        return

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="uni_db"
        )
        cursor = conn.cursor()

        

        if aadhar_var.get() == 1:
            cursor.execute("SELECT Aadhar_card FROM aadharkendra WHERE UIDAI=%s", (uidai,))
            row = cursor.fetchone()
            # print("Aadhar Card Row:", row)  # Debug statement

            if row is not None:
                aadhar_card_data = row[0]
                open_pdf_in_browser(aadhar_card_data, "aadhar_card.pdf")
            else:
                messagebox.showwarning("Aadhar Card Not Found", "Aadhar Card not found in the database.")

        if pan_var.get() == 1:
            cursor.execute("SELECT pan_card FROM pancard WHERE UIDAI=%s", (uidai,))
            row = cursor.fetchone()
            # print("Pan Card Row:", row)  # Debug statement

            if row is not None:
                pan_card_data = row[0]
                open_pdf_in_browser(pan_card_data, "pan_card.pdf")
            else:
                messagebox.showwarning("Pan Card Not Found", "Pan Card not found in the database.")

        conn.close()
    except Error as e:
        messagebox.showerror("Database Error", f"An error occurred while accessing the database: {str(e)}")


# Create main window
root = tk.Tk()
root.title("Document Download")
root.geometry("400x200")

# Create UIDAI entry field
uidai_label = tk.Label(root, text="Enter UIDAI Number:")
uidai_label.pack()
uidai_entry = tk.Entry(root)
uidai_entry.pack()

# Create Aadhar Card checkbox
aadhar_var = tk.IntVar()
aadhar_checkbox = tk.Checkbutton(root, text="Aadhar Card", variable=aadhar_var)
aadhar_checkbox.pack()

# Create Pan Card checkbox
pan_var = tk.IntVar()
pan_checkbox = tk.Checkbutton(root, text="Pan Card", variable=pan_var)
pan_checkbox.pack()

# Create Submit button
submit_button = tk.Button(root, text="Submit", command=submit_form)
submit_button.pack()

root.mainloop()
