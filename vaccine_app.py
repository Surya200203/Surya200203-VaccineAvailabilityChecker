# IMPORTING NECCESSARY MODULES

from tkinter import *  # importing every function present in tkinter module
from tkinter import messagebox
from datetime import datetime
import pytz  # TIMEZONE MODULE
import requests


# SETTING TIME ZONE

IST = pytz.timezone('Asia/Kolkata')  # variable for timezone

# CREATING WINDOW

window = Tk()  # object of TK class



# Window Geometry and components for app
''' All code related to GUI resides between window = Tk()  & window.mainloop()'''
window.geometry("1200x750+0+0")
window.title("Vaccine Availability Checker")
window.iconbitmap("vaccine_icon.ico")
window.resizable(True, True)
window.config(background="#009B77")

# ADD FRAME
# ( window is parent container , bg= background color, bd=borderdepth)
# relif options = FLAT,RAISED,SUNKEN,GROOVE,RIDGE

frame1 = Frame(window, height=120, width=180, bg="#D2386C", bd=10, relief=RIDGE)  # created frame not placed on window
frame1.place(x=0, y=0)  # we placed frame1 on window with place() function at (0,0)

frame2 = Frame(window, height=120, width=1300, bg="#926AA6", bd=10, relief=RIDGE)  # created frame not placed on window
frame2.place(x=180, y=0)  # we placed frame2 on window with place() function at (180,0)

frame3 = Frame(window, height=38, width=1480, bg="#009B77", bd=5, relief=RIDGE)  # created frame not placed on window
frame3.place(x=0, y=121)  # we placed frame2 on window with place() function at (180,0)



# ENTRY BOX/Widget
# (window is parent conatiner , bg= background color , fg= foreground color(textcolor), textvariable allows us to read and write the value entered in text box.

pincode_text_var = StringVar()  # To initilize variable in tkinter.
pincode_text = Entry(window, width=20, bg="white", fg="black",bd=5, font="Times 11  bold", textvariable=pincode_text_var)
pincode_text.place(x=300, y=50)
pincode_text['textvariable'] = pincode_text_var

date_text_var = StringVar()  # To initilize variable in tkinter.
date_text = Entry(window, width=20, bg="white", fg="black", bd=5,font="Times 11  bold", textvariable=date_text_var)
date_text.place(x=600, y=50)
date_text['textvariable'] = date_text_var

# LABEL

label_date = Label(text = "", bg="#D2386C", font="verdana 12 bold")
label_date.place(x=20, y=50)

label_time = Label(text="", bg="#D2386C", font="Helvetica 12 ")
label_time.place(x=20, y=70)

label_pincode = Label(text="PINCODE", bg="#926AA6", font="verdana 11 bold ")
label_pincode.place(x=300, y=20)

label_searchbox_date = Label(text="DATE", bg="#926AA6", font="verdana 11 bold")
label_searchbox_date.place(x=600, y=20)

label_searchbox_date_format = Label(text="[dd-mm-yyyy]", bg="#926AA6", font="verdana 7  bold")
label_searchbox_date_format.place(x=650, y=23)

label_frame3 = Label(text="********** VACCINE AVAILABILITY CHECKER **********",bg="#009B77",font="Koulen 13 bold italic")
label_frame3.place(x=450,y=127)




# RESULT BOX

# result_box = Text(window, height=650, width=900, bg="#939597", fg="black", relief=FLAT, font="verdana 10 bold",bd=5)
# result_box.place(x=0, y=150)
result_box = Text(window, height=100, width=160, bg="#939597", fg="black", relief=FLAT, font="verdana 10 bold",borderwidth=5)
result_box.place(x=0, y=160)




# defination for fletching current date
def insert_date_checkbox():
    raw_TS= datetime.now(IST)
    formatted_TS = raw_TS.strftime("%d-%m-%Y")
    date_text_var.set(formatted_TS)


# defination for fletching current location pincode

url = 'https://ipinfo.io/postal'

def get_postal_ip_service(url):
    response_pincode = requests.get(url).text
    return response_pincode

def insert_date_radio():
    curr_pincode = get_postal_ip_service(url)
    pincode_text_var.set(curr_pincode)

# label for checkbox

checkbox_var_date = IntVar()
check_box_date = Checkbutton(window, text="Today", bg="#926AA6", variable=checkbox_var_date, onvalue=1, offvalue=1, command=insert_date_checkbox())
check_box_date.place(x=600, y=80)

# label for radio button for pincode

current_loc = StringVar()
radio_button_pincode = Radiobutton(window, text="Current Location", bg="#926AA6", variable=current_loc,value=current_loc, command=insert_date_radio())
radio_button_pincode.place(x=300, y=80)


#FUNCTIONS
# to update clock with current timing
def update_clock():
    raw_TS = datetime.now(IST)
    current_date = raw_TS.strftime("%d %b %Y")
    current_time = raw_TS.strftime("%H:%M:%S %p")
    label_date.config(text = current_date)
    label_time.config(text = current_time)
    label_time.after(1000, update_clock)

update_clock()      #calling function in gui

def clear_result_box():
    result_box.delete('1.0', END)


def refresh_api_call(PINCODE,DATE):
    header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/83.0.4103.116 Safari/537.36'}
    request_link = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={PINCODE}&date={DATE}"
    response = requests.get(request_link, headers=header)
    raw_JSON = response.json()
    return raw_JSON

def search_vaccine_avability():
    clear_result_box()
    PINCODE = pincode_text_var.get().strip()
    DATE = date_text_var.get()
    raw_JSON = refresh_api_call(PINCODE,DATE)

    try:
        Number_Of_Centers = len(raw_JSON['centers'])
        if (Number_Of_Centers == 0):
            messagebox.showinfo("INFO","Their are no centers in your Area...Re-check pincode again..")
        else:
            for i in range(Number_Of_Centers):
                result_box.insert(END,"\n")
                fee = raw_JSON['centers'][i]["fee_type"]
                result_box.insert(END,
                f"Center {i + 1} || Name:{raw_JSON['centers'][i]['name']} || Address :{raw_JSON['centers'][i]['address']},{raw_JSON['centers'][i]['district_name']},{raw_JSON['centers'][i]['state_name']}\n")
                result_box.insert(END,
                "---------------------------------------------------------------------------------------------------------------------------\n")
                result_box.insert(END,
                "     Date\t        Vaccine Type       FeeType        Minimum Age      Available Slots(dose 1)     Available Slots(dose 2)\n")
                result_box.insert(END,
                "   -----------     -------------     -----------      -------------        -----------------------          ------------------------\n")
                session_list = raw_JSON['centers'][i]["sessions"]

                for j in range(len(session_list)):
                    result_box.insert(END,"{0:^12} {1:^17} {2:^13} {3:^25} {4:^45} {5:^60}\n".format(
                    session_list[j]["date"], session_list[j]["vaccine"], fee, session_list[j]["min_age_limit"],
                    session_list[j]["available_capacity_dose1"], session_list[j]["available_capacity_dose2"]))
    except KeyError as KE:
        messagebox.showerror("ERROR", "No Available centers for the given Pincode and Date")

# Buttons
# search_vaccine_image = PhotoImage(file='search_Image.png')
search_vaccine_btn = Button(window, bg="#867ae9", command=search_vaccine_avability,relief=RAISED,text="Search \nAvailable Vaccine",bd=8,fg="black")
search_vaccine_btn.place(x=900, y=25)







window.mainloop()
























