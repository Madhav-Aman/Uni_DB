import os
import time
import mysql.connector
from tkinter import *
from tkinter import messagebox
from pyfingerprint.pyfingerprint import PyFingerprint
from PIL import ImageTk, Image

# Function to initialize the fingerprint sensor


def init_sensor():
    try:
        f = PyFingerprint('COM5', 57600, 0xFFFFFFFF, 0x00000000)
        if (f.verifyPassword() == False):
            raise ValueError('The given fingerprint sensor password is wrong!')
    except Exception as e:
        messagebox.showerror(
            "Error", "The fingerprint sensor could not be initialized!")
        exit(1)
    return f


# initialize the fingerprint sensor
fingerprint_sensor = init_sensor()


image_path = None


# Function to read the fingerprint image and save it to file
def scan_fingerprint():
    global image_path
    time.sleep(1)
    while (fingerprint_sensor.readImage() == False):
        pass
    filename = time.strftime("%Y-%m-%d_%H-%M-%S") + ".bmp"
    directory = "e:/24-03-2023/DEMO1"
    if not os.path.exists(directory):
        os.makedirs(directory)
    imageDestination = os.path.join(directory, filename)
    fingerprint_sensor.downloadImage(imageDestination)
    # store the image path in the global variable
    image_path = imageDestination
    return imageDestination


# To delete the stored fingerprint image before scanning the new one,
def rescan_fingerprint():
    global image_path
    try:
        directory = "e:/24-03-2023/DEMO1"
        filelist = [f for f in os.listdir(directory) if f.endswith(".bmp")]
        if filelist:
            # sort the list of files by creation time in descending order
            filelist.sort(key=lambda x: os.path.getctime(
                os.path.join(directory, x)), reverse=True)
            os.remove(os.path.join(directory, filelist[0]))

        image_path=scan_fingerprint()
        if image_path:
            show_image(image_path)
    except Exception as e:
        messagebox.showerror("Error", "Failed to rescan fingerprint!")


def show_image(image_path):
    # try:
        image = Image.open(image_path)
        image = image.resize((200, 200), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        image_label = Label(root, image=photo)
        image_label.image = photo
        image_label.grid(row=5, column=1)
    # except Exception as e:
    #     messagebox.showerror("Error", "Failed to display image!")


def on_scan_button_click():
    global image_path 
    image_path= scan_fingerprint()
    if image_path:
        show_image(image_path)


# Function to insert data into database and delete image file

# Function to insert data into database and delete image file
def submit_data():
    global image_path
    uidai = uidai_entry.get()
    name = name_entry.get()
    phone_no = phone_entry.get()
    if not uidai.isdigit() or len(uidai) != 12:
        messagebox.showerror(
            "Error", "Enter a valid UIDAI number (12 digits)!")
        return
    if not phone_no.isdigit() or len(phone_no) != 10:
        messagebox.showerror(
            "Error", "Enter a valid phone number (10 digits)!")
        return
    if not name:
        messagebox.showerror("Error", "Enter a name!")
        return
    # read the image data from the stored image path
    with open(image_path, 'rb') as f:
        image_data = f.read()
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="uni_db"
        )
        cursor = mydb.cursor()
        sql = "INSERT INTO registration (UIDAI, name, phone_no, fingerprint) VALUES (%s, %s, %s, %s)"
        val = (uidai, name, phone_no, image_data)
        cursor.execute(sql, val)
        
        mydb.commit()
        # delete the stored image file
        os.remove(image_path)
        # reset the global image path variable
        
        image_path= None
        messagebox.showinfo("uploaded", "Data is uploaded to UNI_DB")
    except Exception as e:
        messagebox.showerror(
            "Error", "Failed to insert data into database!")
    finally:
        clear_fields()
        cursor.close()
        mydb.close()

# create the tkinter window
root = Tk()
root.title("Unified Database Registration")
root.geometry("400x550")
root.resizable(False, False)

# create labels and entries for UIDAI, Name and Phone No.
uidai_label = Label(root, text="UIDAI Number:")
uidai_label.grid(row=0, column=0, padx=10, pady=10)
uidai_entry = Entry(root, width=30)
uidai_entry.grid(row=0, column=1)

name_label = Label(root, text="Name:")
name_label.grid(row=1, column=0, padx=10, pady=10)
name_entry = Entry(root, width=30)
name_entry.grid(row=1, column=1)

phone_label = Label(root, text="Phone Number:")
phone_label.grid(row=2, column=0, padx=10, pady=10)
phone_entry = Entry(root, width=30)
phone_entry.grid(row=2, column=1)

# Function to clear the text in UIDAI, Name and Phone No. entries


def clear_fields():
    global image_path
    directory = "e:/24-03-2023/DEMO1"
    filelist = [f for f in os.listdir(directory) if f.endswith(".bmp")]
    if filelist:
        for file in filelist:
            os.remove(os.path.join(directory, file))
        
    uidai_entry.delete(0, END)
    name_entry.delete(0, END)
    phone_entry.delete(0, END)
    image_path=None
    show_image("E:/30-03-2023/UNI_DB 1.0/src/1.png")
    
    

# Function to exit the application


def exit_application():
    root.destroy()


# Create the scan button
scan_button = Button(root, text="Scan Fingerprint",
                     command=on_scan_button_click)
scan_button.grid(row=3, column=0 , padx=10,pady=10)

# Create the rescan button
rescan_button = Button(root, text="Rescan Fingerprint",
                       command=rescan_fingerprint)
rescan_button.grid(row=3, column=1,padx=10)


# create buttons for submitting and clearing data
submit_button = Button(root, text="Submit", command=submit_data)
submit_button.grid(row=4, column=1, padx=10, pady=10)





clear_button = Button(root, text="Clear", command=clear_fields)
clear_button.grid(row=4, column=0, padx=10, pady=10)

exit_button = Button(root, text="Exit", command=exit_application)
exit_button.grid(row=4, column=2, padx=10, pady=10)

# run the tkinter event loop
root.mainloop()
