import Tkinter as tk
import time       # https://docs.python.org/3/library/time.html
from PIL import Image, ImageTk    # sudo apt-get install python-imaging-tk
from Adafruit_BMP085 import BMP085
from gpiozero import Servo  # for servo control
from time import sleep      # for servo timer


bmp = BMP085(0x77)
temp = bmp.readTemperature()
pressure = bmp.readPressure()
press = int(pressure)

root = tk.Tk()
root.title("PROPELL FACTORY CONTROL")
root.geometry("1200x800")
root.resizable(False, False)

target_press = tk.IntVar()
trigger_press = tk.IntVar()

itarget = 0
itrigger = 0

valve_servo = 12
power_servo = 16

RUN = False

interval = 0
start = 0
end = 0

s1 = Servo(valve_servo)
s2 = Servo(power_servo)


# Boolean variable to help control state of time
running = False

# Time varibles initially set to 0
days, hours, minutes, seconds = 0, 0, 0, 0


# logo
logo = Image.open('propell200.jpg')
logo = ImageTk.PhotoImage(logo)


# definition adjust
def adjust(textbox1, textbox2):
    global itarget, itrigger

    button_text.set("adjusting")

    itarget = target_press.get()
    itrigger = trigger_press.get()

    vacuum_label.config(text="target pressure = " + str(textbox1) + ", trigger pressure = " + str(textbox2))
    print(itarget, itrigger)

# writing function
def write():

    month = time.strftime("%B")
    date = time.strftime("%d")
    day = time.strftime("%A")
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    second = time.strftime("%S")
    time_zone = time.strftime("%Z")

    write_label.config(text="VACUUM STARTED AT : " + month + " / " + date + "   time : " + hour + " : " + minute + " : " + second + " / " + time_zone + " / " + day)

# timer function
def timer_start():
    global running
    if not running:
        t_update()
        running = True


def t_update():
    # update seconds with (additional) compound assigned operator
    global days, hours, minutes, seconds
    seconds += 1
    if seconds == 60:
        minutes += 1
        seconds = 0
    if minutes == 60:
        hours += 1
        minutes = 0
    if hours == 24:
        days += 1
        hours = 0

    # update timer label after 1000ms (1 second)
    stopwatch_label.config(text="ELAPSED TIME IS : " + str(days) + " days  " + str(hours) + ' : ' + str(minutes) + ' : ' + str(seconds))
     # after each second (1000 milliseconds), call update function
    # use update_time variable to cancel or pause the time using after_cancel
    global update_time
    update_time = stopwatch_label.after(1000, t_update)


# clock function
def clock():
    month = time.strftime("%B")
    date = time.strftime("%d")
    day = time.strftime("%A")
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    second = time.strftime("%S")
    time_zone = time.strftime("%Z")

    cl_label.config(text=month + " / " + date + "   time : " + hour + ":" + minute + ":" + second + " / " + time_zone + " / " + day)
    cl_label.after(1000, clock)



# Read values from the sensors at regular interval
def read():
    global temp, pressure, press

    temp = bmp.readTemperature()
    pressure = bmp.readPressure()
    press = int(pressure)

    temp_label.configure(text=str(temp))
    pressure_label.configure(text=str(pressure))

    print(press)

def read_every_1():

    read()

    root.after(1000, read_every_1)


# Servo functions
def valve_open():
    s1.max()
    print("valve_open")

def valve_close():
    s1.min()
    print("valve_close")

def power_on():
    s2.min()
    print("power_on")

def power_off():
    s2.max()
    print("power_off")

# conducting vacuum operations


def operations():
    global press, itarget, itrigger, RUN, s_cnt, interval, start, end

    if RUN == True:
        if press < itarget:
            print("reached target")
            valve_close()
            power_off()
            start = time.time()

        if press >= itrigger:
            valve_open()
            power_on()
            print("repeating")
            end = time.time()
            interval = end - start
            interval_label.config(text="interval :" + str(interval))

    else:
        if press >= itarget:
            valve_open()
            power_on()
            RUN = True
            print("operations commencing")

    root.after(1000, operations)


#quit
def stop():
    valve_close()
    power_off()

    root.destroy()



canvas = tk.Canvas(root, height=400, width=800)
canvas.pack()

# **********  FRAMES  **********

# upper frame
frame1 = tk.Frame(root, bg='white')
frame1.place(relx=0.5, rely=0.06, relwidth=0.9, relheight=0.2, anchor='n')


# lower frame
frame2 = tk.Frame(root, bg='gray')
frame2.place(relx=0.5, rely=0.25, relwidth=0.9, relheight=0.6, anchor='n')

# ROOM temperature
frame3 = tk.Frame(frame2, bg='white')
frame3.place(relx=0.7, rely=0.05, relwidth=0.2, relheight=0.08)

# Current pressure
frame4 = tk.Frame(frame2, bg='white')
frame4.place(relx=0.7, rely=0.16, relwidth=0.2, relheight=0.08)


# ***********LABELS***********

# logo label
logo_label = tk.Label(frame1, image=logo)
logo_label.image = logo
logo_label.place(x=0, y=25)

# clock label
cl_label = tk.Label(frame1, text="", font=("Helvetica", 25), fg='yellow', bg='black')
cl_label.place(x=370, y=100)


label = tk.Label(frame1, text="Temperature and Pressure Control", font="Raleway, 30", bg='white')
label.place(x=250, y=30)

s_label = tk.Label(frame1, text="PROPELL CHANG-MI FACTORY", font="Raleway, 15", bg='white', fg='brown')
s_label.place(x=780, y=0)

# grid options : must be -column, -columnspan, -in, -ipadx, -ipady, -padx, -pady, -row, -rowspan, or -sticky

label2 = tk.Label(frame2, text="ROOM Temperature", font="Raleway, 20", bg='black', fg='blue')
label2.place(x=10, y=30)

label3 = tk.Label(frame2, text="Current Pressure", font="Raleway, 20", bg='black', fg='blue')
label3.place(x=10, y=80)

label4 = tk.Label(frame2, text="TARGET Pressure", font="Raleway, 20", bg='black', fg='red')
label4.place(x=10, y=130)

trg_label = tk.Label(frame2, text="TRIGGER Pressure", font="Raleway, 20", bg='black', fg='red')
trg_label.place(x=10, y=180)

vacuum_label = tk.Label(frame2, text="====================waiting====================", font="Raleway, 20", bg='white', fg='red')
vacuum_label.place(x=10, y=300)

write_label = tk.Label(frame2, text="====================wating====================", font="Raleway, 18", bg='black', fg='red')
write_label.place(x=10, y=370)

# label to display timer
stopwatch_label = tk.Label(frame2, text="====================waiting====================", font=('Arial', 20), bg='black', fg='yellow')
stopwatch_label.place(x=10, y=420)

# label to display ROOM temperature
temp_label = tk.Label(frame3, text=temp, font="Raleway, 20", bg='white', fg='blue')
temp_label.place(x=0, y=0)

# label to display current pressure
pressure_label = tk.Label(frame4, text=pressure, font="Raleway, 20", bg='white', fg='blue')
pressure_label.place(x=0, y=0)

# label interval
interval_label = tk.Label(frame2, text="interval : " + str(interval) + " sec", font="Raleway, 15", bg='gray', fg='white')
interval_label.place(relx=0.8, rely=0.94)


# ********** ENTRIES **********

textbox1 = tk.Entry(frame2, textvariable=target_press, bg='white', fg='blue', font=('Raleway', 15))
textbox1.place(relx=0.7, rely=0.27, relwidth=0.15, relheight=0.08)

textbox2 = tk.Entry(frame2, textvariable=trigger_press, bg='white', fg='blue', font=('Raleway', 15))
textbox2.place(relx=0.7, rely=0.38, relwidth=0.15, relheight=0.08)


# ********** BUTTONS **********
button_text = tk.StringVar()
button1 = tk.Button(frame2, textvariable=button_text, command=lambda: adjust(textbox1.get(), textbox2.get()), font='Raleway, 18',  bg='yellow', text='adjust')
button_text.set("Change")
button1.place(relx=0.88, rely=0.27, relwidth=0.1, relheight=0.19)

button2 = tk.Button(frame2, command=lambda: (write(), timer_start(), operations()), text='VACUUM STARTS', fg='red', font='Raleway, 25')
button2.place(relx=0, rely=0.5, relwidth=1, relheight=0.1)

button3 = tk.Button(frame2, command=lambda: valve_open(), text='V_open', fg='green', bg='gray', font='Raleway, 15')
button3.place(x=380, y=30, relwidth=0.1, relheight=0.15)

button4 = tk.Button(frame2, command=lambda: valve_close(), text='V_close', fg='green', bg='gray', font='Raleway, 15')
button4.place(x=380, y=140, relwidth=0.1, relheight=0.15)

button5 = tk.Button(frame2, command=lambda: power_on(), text='P_on', fg='green', bg='gray', font='Raleway, 15')
button5.place(x=500, y=30, relwidth=0.1, relheight=0.15)

button6 = tk.Button(frame2, command=lambda: power_off(), text='P-off', fg='green', bg='gray', font='Raleway, 15')
button6.place(x=500, y=140, relwidth=0.1, relheight=0.15)

button7 =  tk.Button(frame2, command=lambda: stop(), text='STOP', fg='red', bg='white', font='Raleway, 18')
button7.place(x=620, y=80, relwidth=0.1, relheight=0.15)

# button = tk.Button(frame, text="Adjust", fg="black")
# button.place(relx=0, rely=0, relwidth=0.25, relheight=0.25)



clock()

read_every_1()

valve_close()
power_off()

root.mainloop()

