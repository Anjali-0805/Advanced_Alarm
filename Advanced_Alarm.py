import tkinter as tk
import time
import math
import random
from tkinter import messagebox
import threading
import pygame
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime

# Initialize Pygame for sound
pygame.mixer.init()

def is_24_hour_format():
    time_str = time.strftime("%H:%M")  
    return time.strftime("%p") == ""  

# Create the main window
root = tk.Tk()
root.title("Advanced Alarm Clock")
root.configure(bg="black")
 
# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}+0+0")

main_frame = tk.Frame(root, bg="black")
main_frame.pack(fill="both", expand=True, pady=(0, 20))

clock_frame = tk.Frame(main_frame, bg="black")
clock_frame.pack(side="top", fill="both", expand=True, pady=(0, 5))
# Calculate responsive sizes based on screen dimensions
font_size = max(14, min(16, screen_width // 45))  # Dynamic font size
padding_size = max(5, screen_height // 100)       # Dynamic padding
button_height = max(30, screen_height // 25)      # Dynamic button height

# Control Box with responsive settings
control_box = tk.Frame(
    main_frame,
    bg="black",
    padx=screen_width//50,          # Responsive horizontal padding
    pady=screen_height//100         # Responsive vertical padding
)
control_box.pack(
    side=tk.BOTTOM,
    fill=tk.X,
    expand=False,  # Don't let it expand vertically
    pady=(0, 10)   # Reduced bottom padding (top, bottom)
)

# Set clock size
clock_size =int(min(screen_width, screen_height) // 2.3)

# Create clock canvas
canvas = tk.Canvas(
    clock_frame, 
    width=clock_size, 
    height=clock_size, 
    bg="black", 
    highlightthickness=0
)
canvas.pack(pady=5, expand=True)

# Clock drawing parameters
center_x = clock_size // 2
center_y = clock_size // 2
radius = clock_size // 2 - 10

# Draw clock ticks
for i in range(60):
    angle = math.radians(i * 6)
    inner_radius = radius - 23
    outer_radius = radius - 5
    
    x1 = center_x + inner_radius * math.cos(angle)
    y1 = center_y + inner_radius * math.sin(angle)
    x2 = center_x + outer_radius * math.cos(angle)
    y2 = center_y + outer_radius * math.sin(angle)

    if i % 5 == 0:  # Hour ticks
        canvas.create_line(x1, y1, x2, y2, width=4, fill="white")
    else:  # Minute ticks
        canvas.create_line(x1, y1, x2, y2, width=2, fill="gray")

# Draw clock numbers
for i in range(1, 13):
    angle = math.radians(i * 30 - 90)
    num_radius = radius - 40
    x = center_x + num_radius * math.cos(angle)
    y = center_y + num_radius * math.sin(angle)
    canvas.create_text(
        x, y, 
        text=str(i), 
        font=("Courier New", max(14, clock_size//20), "bold"),
        fill="white"
    )

# Create clock hands
hour_hand_length = radius * 0.5
minute_hand_length = radius * 0.7
second_hand_length = radius * 0.8

hour_hand = canvas.create_line(
    center_x, center_y, 
    center_x, center_y - hour_hand_length, 
    width=max(4, clock_size//50),
    fill="white", 
    capstyle=tk.ROUND
)
minute_hand = canvas.create_line(
    center_x, center_y, 
    center_x, center_y - minute_hand_length, 
    width=max(3, clock_size//70),
    fill="white", 
    capstyle=tk.ROUND
)
second_hand = canvas.create_line(
    center_x, center_y, 
    center_x, center_y - second_hand_length, 
    width=2,
    fill="red", 
    capstyle=tk.ROUND
)

# Center circle
canvas.create_oval(
    center_x - 5, center_y - 5,
    center_x + 5, center_y + 5,
    fill="red", 
    outline="red"
)

# Digital time display in control box
time_label = tk.Label(
    control_box,
    text="", 
    font=("Digital Numbers", max(24, min(48, screen_width//300)), "bold"),
    fg="orange", 
    bg="black"
)
time_label.pack(pady=screen_height//200)

# Date display
date_label = tk.Label(
    control_box,
    text="", 
    font=("Courier New", max(6, min(14, screen_width//50))), 
    fg="Orange", 
    bg="black"
)
date_label.pack()

alarm_frame = tk.Frame(
    control_box, 
    bg="black",
    padx=screen_width//100,
    pady=screen_height//200
)
alarm_frame.pack(pady=screen_height//100)

# Date selection frame
date_selection_frame = tk.Frame(alarm_frame, bg="black")
date_selection_frame.grid(row=0, column=0, columnspan=4, pady=(0, 10))

tk.Label(date_selection_frame, text="Set Alarm Date:", font=("Tw Cen MT", 14, "bold"), fg="orange", bg="black").grid(row=0, column=0, padx=5)

# Date variables
day_var = tk.StringVar()
month_var = tk.StringVar()
year_var = tk.StringVar()

# Get current date
now = datetime.now()
current_year = now.year
current_month = now.month
current_day = now.day

# Day picker
day_picker = ttk.Combobox(
    date_selection_frame,
    values=[str(i).zfill(2) for i in range(1, 32)],
    textvariable=day_var,
    width=3,
    state="readonly",
    justify="center",
    font=("Arial", 12)
)
day_picker.grid(row=0, column=1, padx=5)
day_picker.set(str(current_day).zfill(2))

# Month picker
month_picker = ttk.Combobox(
    date_selection_frame,
    values=[str(i).zfill(2) for i in range(1, 13)],
    textvariable=month_var,
    width=3,
    state="readonly",
    justify="center",
    font=("Arial", 12)
)
month_picker.grid(row=0, column=2, padx=5)
month_picker.set(str(current_month).zfill(2))

# Year picker
year_picker = ttk.Combobox(
    date_selection_frame,
    values=[str(i) for i in range(current_year, current_year + 11)],
    textvariable=year_var,
    width=5,
    state="readonly",
    justify="center",
    font=("Arial", 12)
)
year_picker.grid(row=0, column=3, padx=5)
year_picker.set(str(current_year))

# Time selection frame
time_selection_frame = tk.Frame(alarm_frame, bg="black")
time_selection_frame.grid(row=1, column=0, columnspan=4, pady=(10, 0))

tk.Label(time_selection_frame, text="Set Alarm Time:", font=("Tw Cen MT", 14, "bold"), fg="orange", bg="black").grid(row=0, column=0, padx=5)

# Time pickers
hour_var = tk.StringVar()
minute_var = tk.StringVar()
am_pm_var = tk.StringVar()

hour_picker = ttk.Combobox(
    time_selection_frame,
    values=[str(i).zfill(2) for i in range(1, 13)],
    textvariable=hour_var,
    width=5,
    state="readonly",
    justify="center",
    font=("Arial", 12)
)
hour_picker.grid(row=0, column=1, padx=5)
hour_picker.current(0)

minute_picker = ttk.Combobox(
    time_selection_frame,
    values=[str(i).zfill(2) for i in range(0, 60)],
    textvariable=minute_var,
    width=5,
    state="readonly",
    justify="center",
    font=("Arial", 12)
)
minute_picker.grid(row=0, column=2, padx=5)
minute_picker.current(0)

am_pm_picker = ttk.Combobox(
    time_selection_frame,
    values=["AM", "PM"],
    textvariable=am_pm_var,
    width=5,
    state="readonly",
    justify="center",
    font=("Arial", 12)
)
am_pm_picker.grid(row=0, column=3, padx=5)
am_pm_picker.current(0)

# Ringtone selection
ringtones = {
    "Loud Alarm": "loud_alarm_sound.mp3",
    "Alert Buzzer": "alert_buzzer.mp3",
    "Ultimate Wake Up": "ultimate_wake_up.mp3",
    "Persistent Alarm": "persistent_alarm_clock.mp3",
    "Intense Alarm": "alarm-beeps.mp3",
    "Alarm 1":"Classic-2.mp3",
    "Alarm 2":"Alarm_2.mp3",
    "Alarm 3":"Alarm_Classic.mp3"

}

selected_ringtone = tk.StringVar()
selected_ringtone.set("Loud Alarm")

tk.Label(alarm_frame, text="Ringtone:", font=("Tw Cen MT", 14, "bold"), 
         fg="orange", bg="black").grid(row=2, column=0, padx=5, pady=(10, 0))
ringtone_picker = ttk.Combobox(
    alarm_frame,
    values=list(ringtones.keys()),
    textvariable=selected_ringtone,
    width=15,
    state="readonly",
    justify="center",
    font=("Arial", 12)
)
ringtone_picker.grid(row=2, column=1, columnspan=3, pady=(10, 0))
ringtone_picker.current(0)

button_canvas = tk.Canvas(
    control_box,
    width=max(150, screen_width//8),
    height=max(40, screen_height//20),
    bg="black",
    highlightthickness=0
)
button_canvas.pack(pady=screen_height//100)

def draw_rounded_rect(canvas, x1, y1, x2, y2, radius, color):
    canvas.create_arc(x1, y1, x1 + 2*radius, y1 + 2*radius, start=90, extent=90, 
                     outline=color, width=2, style="arc")
    canvas.create_arc(x2 - 2*radius, y1, x2, y1 + 2*radius, start=0, extent=90, 
                     outline=color, width=2, style="arc")
    canvas.create_arc(x1, y2 - 2*radius, x1 + 2*radius, y2, start=180, extent=90, 
                     outline=color, width=2, style="arc")
    canvas.create_arc(x2 - 2*radius, y2 - 2*radius, x2, y2, start=270, extent=90, 
                     outline=color, width=2, style="arc")
    canvas.create_line(x1 + radius, y1, x2 - radius, y1, fill=color, width=2)
    canvas.create_line(x1 + radius, y2, x2 - radius, y2, fill=color, width=2)
    canvas.create_line(x1, y1 + radius, x1, y2 - radius, fill=color, width=2)
    canvas.create_line(x2, y1 + radius, x2, y2 - radius, fill=color, width=2)

draw_rounded_rect(button_canvas, 10, 10, 170, 40, 15, "#FFA500")
draw_rounded_rect(button_canvas, 12, 12, 168, 38, 13, "#FFD700")
button_canvas.create_text(85, 25, text="SET ALARM", font=("Helvetica", 10, "bold"), fill="white")
button_canvas.create_text(145, 25, text="⏰", font=("Arial", 8, "bold"), fill="white")

alarm_status = tk.Label(
    control_box,
    text="⏰ No Alarm Set",
    font=("Tw Cen MT", 16),
    fg="red",
    bg="black",
    padx=screen_width//100,
    pady=screen_height//200
)
alarm_status.pack(pady=(0, screen_height//50))

# Alarm functionality
alarm_datetime = None
puzzle_open = False

def set_alarm():
    global alarm_datetime
    try:
        day = int(day_var.get())
        month = int(month_var.get())
        year = int(year_var.get())
        hour = int(hour_var.get())
        minute = int(minute_var.get())
        am_pm = am_pm_var.get()
        
        # Convert to 24-hour format
        if am_pm == "PM" and hour != 12:
            hour += 12
        elif am_pm == "AM" and hour == 12:
            hour = 0
            
        # Validate date
        try:
            alarm_date = datetime(year, month, day, hour, minute)
            current_date = datetime.now()
            
            if alarm_date < current_date:
                messagebox.showerror("Error", "Cannot set alarm for past date/time!")
                return
                
            alarm_datetime = alarm_date
            formatted_time = alarm_date.strftime("%d-%m-%Y - %I:%M %p")
            alarm_status.config(
                text=f" Alarm Set for {formatted_time}",
                fg="#bbf90f",
                bg="black",
                font=("Tw Cen MT", font_size, "bold")
            )
            pygame.mixer.music.stop()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid date: {e}")
            
    except Exception as e:
        messagebox.showerror("Error", f"Error setting alarm: {e}")

button_canvas.bind("<Button-1>", lambda e: set_alarm())

def check_alarm():
    global alarm_datetime, puzzle_open
    while True:
        if alarm_datetime and not puzzle_open:
            current_datetime = datetime.now()
            if current_datetime >= alarm_datetime:
                trigger_alarm()
                alarm_datetime = None  # Reset after triggering
                time.sleep(1)
        time.sleep(1)

def trigger_alarm():
    global puzzle_open
    if puzzle_open:
        return

    ringtone_file = ringtones[selected_ringtone.get()]
    pygame.mixer.music.load(ringtone_file)
    pygame.mixer.music.play(loops=-1)
    show_puzzle_window()

def show_puzzle_window():
    global puzzle_open, puzzle_window, answer_var, correct_answer, answer_entry, error_label, result_label, gif_label, gif_frames, current_frame

    if puzzle_open:
        return  

    puzzle_open = True  
    puzzle_window = tk.Toplevel(root)
    puzzle_window.title("Solve the Puzzle!")

    screen_width = puzzle_window.winfo_screenwidth()
    screen_height = puzzle_window.winfo_screenheight()
    window_width = min(800, screen_width - 100)
    window_height = min(600, screen_height - 100)
    
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    puzzle_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    puzzle_window.configure(bg="#181818")
    puzzle_window.protocol("WM_DELETE_WINDOW", lambda: None)
    puzzle_window.grab_set()  

    title_font_size = max(24, min(36, window_width // 20))
    question_font_size = max(20, min(32, window_width // 50))
    button_font_size = max(10, min(28, window_width // 50))
    entry_font_size = max(14, min(28, window_width // 50))
    message_font_size = max(10, min(20, window_width // 40))

    current_frame = 0
    gif_frames = []

    gif_path = "Alarm_ringing.gif"
    
    try:
        gif_image = Image.open(gif_path)
        gif_width = min(window_width - 80, 800)
        
        for i in range(gif_image.n_frames):
            gif_image.seek(i)
            frame = gif_image.copy()
            aspect_ratio = frame.width / frame.height
            new_height = int(gif_width / aspect_ratio)
            frame = frame.resize((gif_width, new_height), Image.LANCZOS)
            gif_frames.append(ImageTk.PhotoImage(frame))
        
    except Exception as e:
        print(f"Error loading GIF: {e}")
        gif_frames = [tk.PhotoImage()]

    gif_label = tk.Label(puzzle_window, bg="#181818")
    gif_label.pack(pady=20)

    def animate_gif():
        global current_frame
        if gif_frames:
            gif_label.config(image=gif_frames[current_frame])
            current_frame = (current_frame + 1) % len(gif_frames)
            puzzle_window.after(100, animate_gif)

    animate_gif()

    puzzle_type = random.choice(["multiplication", "bodmas", "logic"])
    if puzzle_type == "multiplication":  
        num1, num2 = random.randint(1000, 1565), random.randint(1240, 1435)  
        correct_answer = num1 + num2
        question = f"Solve: {num1} + {num2} = ?"  
    elif puzzle_type == "bodmas":  
        a, b = random.randint(1, 15), random.randint(1, 15)
        c = random.randint(1, 5)  
        correct_answer = (a + b) - c  
        question = f"Solve: ({a} + {b}) - {c} = ?"  
    elif puzzle_type == "logic":
        num1, num2 = random.randint(1, 50), random.randint(1, 50)
        num3 = random.randint(1, 20)
        correct_answer = (num1 + num2) - num3
        question = f"If a + b = {num1 + num2} and c = {num3}, what is (a + b) - c?"

    puzzle_label = tk.Label(
        puzzle_window, 
        text=question, 
        font=("Cambria", question_font_size, "bold"), 
        fg="yellow", 
        bg="#181818", 
        wraplength=window_width - 100
    )
    puzzle_label.pack(pady=30)

    answer_var = tk.StringVar()
    answer_entry = tk.Entry(
        puzzle_window, 
        textvariable=answer_var, 
        font=("Arial", entry_font_size), 
        justify="center", 
        fg="black", 
        bg="lightyellow", 
        relief="ridge", 
        borderwidth=4,
        width=15
    )
    answer_entry.pack(pady=20)
    submit_button = tk.Button(
        puzzle_window, 
        text="SUBMIT",
        font=("Tw Cen MT", button_font_size,"bold"),
        command=check_answer, 
        bg="#007BFF", 
        fg="white",
        activebackground="#0056b3", 
        activeforeground="white",
        width=15,           # Horizontal padding (increases width)
               # Vertical padding (increases height)
        relief="flat", 
        borderwidth=0
    )
    submit_button.pack(pady=20)

    result_frame = tk.Frame(puzzle_window, bg="#181818")
    result_frame.pack(pady=20)

    result_label = tk.Label(
        result_frame, 
        text="", 
        font=("Tw Cen MT", message_font_size,"bold"), 
        fg="green",
        bg="#181818"
    )
    result_label.grid(row=0, column=0, padx=10)

    error_label = tk.Label(
        result_frame, 
        text="", 
        font=("Tw Cen MT", message_font_size), 
        fg="red", 
        bg="#181818"
    )
    error_label.grid(row=0, column=1, padx=10)


    answer_entry.focus_set()


def check_answer():
    global puzzle_open, alarm_datetime, result_label
    if answer_var.get().isdigit() and int(answer_var.get()) == correct_answer:
        pygame.mixer.music.stop()
        alarm_datetime = None
        alarm_status.config(text="⏰ No Alarm Set", fg="red")
        puzzle_open = False
        
        error_label.config(text="")
        result_label.config(text="  ✅ Correct Answer!")
        
        puzzle_window.after(1000, puzzle_window.destroy)
    else:
        result_label.config(text="")
        error_label.config(text="  ❌ Wrong Answer! Try again.")
        answer_entry.delete(0, tk.END)



def update_clock():
    current_time = time.localtime()
    hours = current_time.tm_hour % 12 if not is_24_hour_format() else current_time.tm_hour
    minutes = current_time.tm_min
    seconds = current_time.tm_sec

    hour_angle = math.radians((hours + minutes / 60) * 30 - 90)
    minute_angle = math.radians((minutes + seconds / 60) * 6 - 90)
    second_angle = math.radians((seconds * 6) - 90)

    hour_x = center_x + hour_hand_length * 0.6 * math.cos(hour_angle)
    hour_y = center_y + hour_hand_length * 0.6 * math.sin(hour_angle)
    minute_x = center_x + minute_hand_length * 0.8 * math.cos(minute_angle)
    minute_y = center_y + minute_hand_length * 0.8 * math.sin(minute_angle)
    second_x = center_x + second_hand_length * 0.9 * math.cos(second_angle)
    second_y = center_y + second_hand_length * 0.9 * math.sin(second_angle)

    canvas.coords(hour_hand, center_x, center_y, hour_x, hour_y)
    canvas.coords(minute_hand, center_x, center_y, minute_x, minute_y)
    canvas.coords(second_hand, center_x, center_y, second_x, second_y)

    if is_24_hour_format():
        time_label.config(text=time.strftime("%H:%M:%S"))
    else:
        time_label.config(text=time.strftime("%I:%M:%S %p"))
    
    # Update date display
    date_label.config(text=time.strftime("%A, %B %d, %Y"))

    root.after(40, update_clock)

# Start threads
alarm_thread = threading.Thread(target=check_alarm, daemon=True)
alarm_thread.start()

update_clock()
root.mainloop()