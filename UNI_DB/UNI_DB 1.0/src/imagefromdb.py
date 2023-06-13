import mysql.connector
from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO

# Connect to the database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="uni_db"
)

# Create a cursor object to execute queries
cursor = mydb.cursor()

# Get UIDAI number from user
uidai = input("Enter UIDAI number: ")

# Retrieve fingerprint image from database
sql = "SELECT fingerprint FROM registration WHERE UIDAI = %s"
val = (uidai,)
cursor.execute(sql, val)
result = cursor.fetchone()

# Check if image was found
if result is None:
    print("No image found for UIDAI number", uidai)
    exit(1)

# Convert binary data to PIL image
img_data = result[0]
img_io = BytesIO(img_data)
img = Image.open(img_io)

# Create Tkinter window and display image
root = Tk()
photo = ImageTk.PhotoImage(img)
label = Label(root, image=photo)
label.pack()
root.mainloop()
