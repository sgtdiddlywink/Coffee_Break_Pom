# --------------------------------------------------Import Modules-----------------------------------------------------#
import tkinter as tk
from os import startfile
import math
import ctypes

# --------------------------------------------------CONSTANTS----------------------------------------------------------#
WINDOW_BG_COLOR = "#F26052"

TITLE_FONT_NAME = "Arial"
TITLE_FONT_HEIGHT = 36
TITLE_FONT_TYPE = "bold"
TITLE_FONT_COLOR = "#F2DEDC"

TEXT_FONT_NAME = "Arial"
TEXT_FONT_HEIGHT = 20
TEXT_FONT_TYPE = "normal"
TEXT_FONT_COLOR = "#F2DEDC"

TK_WINDOW_TITLE = "Coffee Break"  # Set title of Tk Window

SHORT_BREAK_TIME = 5  # Timer in minutes
LONG_BREAK_TIME = 15  # Timer in minutes
WORK_TIME = 25  # Timer in minutes
BREAK_INTERVALS = 0  # This sets how many short breaks before a long break
TIMER = None  # Need a variable to set the after_cancel method, or it won't work
PAUSE = False
GLOBAL_TIME = 0

# Screen size based on your monitor - This is for a 2560x1440 Monitor and will place window in the upper right corner
WINDOW_WIDTH = 450  # pixels wide
WINDOW_HEIGHT = 900  # pixels high


# --------------------------------------------Functions----------------------------------------------------------------#
# Function for counting down. Takes a variable input for the amount of time to start with
def count_down(time):
	global GLOBAL_TIME
	GLOBAL_TIME = time
	if time > 0:  # If statement to start the countdown
		minutes = math.floor(time / 60)
		if time < 60:
			seconds = time
			minutes = 0
		else:
			seconds = time % 60
		timer_label.configure(text=f"{str(minutes)}min : {str(seconds)}sec")  # Change the label to the new time
		global TIMER  # Bring Constant in and set the window after to it.
		# Set TIMER equal to window after will loop through the function with the new time
		TIMER = window.after(1000, count_down, time - 1)
	else:
		start()  # Will call the start function after time == 0


def start():
	global BREAK_INTERVALS  # Bring this in globally to adjust it within the function
	# Bring these in as a single variables that will be overridden every time the functions are called
	long = LONG_BREAK_TIME
	short = SHORT_BREAK_TIME
	work = WORK_TIME
	BREAK_INTERVALS += 1  # This will set the break interval variable to an odd number to initiate work
	if BREAK_INTERVALS == 8:  # Since there are 4 work periods and 4 rest periods this will be 8
		count_down(long * 60)  # Call countdown function
		title_label.config(text="LONG\nBREAK")  # Adjust label
		BREAK_INTERVALS = 0  # Revert Constant back to 0
		startfile("15_break.mp4")  # Call a mp4 file of your choice
	elif BREAK_INTERVALS % 2 == 0:  # Every even period of the Constant break_intervals a break period will be called
		count_down(short * 60)  # Call function
		title_label.config(text="SHORT\nBREAK")  # Change title
		startfile("5_break.mp4")  # Start mp4 file of your choice
	else:
		count_down(work * 60)  # Call for every odd period of the work_interval
		title_label.config(text="WORK")  # Change label


def pause_resume():
	global PAUSE, GLOBAL_TIME  # Bring in Constants to manipulate and keep track between functions
	if not PAUSE:
		window.after_cancel(TIMER)  # Cancel the timer function
		PAUSE = True  # This will detect whether it should stay paused or resume
		pause_button.config(text="RESUME")
	else:
		count_down(GLOBAL_TIME)
		PAUSE = False
		pause_button.config(text="PAUSE")


def reset():
	global PAUSE, BREAK_INTERVALS, GLOBAL_TIME  # Bring Constant in to change it back to zero
	if not PAUSE:
		BREAK_INTERVALS = 0  # Reset the Constant
		window.after_cancel(TIMER)  # Needs to be set to a Constant outside of the functions to stop the action
		timer_label.config(text="")  # Reset the label
	else:
		window.after_cancel(TIMER)  # Needs to be set to a Constant outside of the functions to stop the action
		GLOBAL_TIME = 0
		BREAK_INTERVALS = 0  # Reset the Constant
		timer_label.config(text="")  # Reset the label
		pause_button.config(text="PAUSE")


# --------------------------------------------Tk Window Box------------------------------------------------------------#
window = tk.Tk()  # Create a window for the GUI

# Determine existing windows condition and if multiple monitors are present
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(78)  # Determines monitor pixel width
screen_height = user32.GetSystemMetrics(79)  # Determine monitor pixel height
# If multiple monitors are present, this will center the tk window in the far left
# This assumes that windows are horizontally aligned and not vertical
window_x = math.floor(((screen_width/4) - (WINDOW_WIDTH/2)))  # pixel buffer from right side of screen
window_y = math.floor(((screen_height/2) - (WINDOW_HEIGHT/2)))  # pixel buffer from top of screen
screen_geometry = f"{str(WINDOW_WIDTH)}x{str(WINDOW_HEIGHT)}+{str(window_x)}+{str(window_y)}"  # Placed in geometry

window.title(TK_WINDOW_TITLE)  # Set the title for the GUI
window.geometry(screen_geometry)  # Set the window geometry for the GUI
window.configure(pady=5, padx=5, bg=WINDOW_BG_COLOR)

# Create image at top of screen and icon
pic = tk.PhotoImage(file="coffee.png")
window.iconphoto(False, pic)  # Override default image with custom image
image = tk.Label(
	master=window,
	image=pic,
	anchor="center",
	bg=WINDOW_BG_COLOR,
)
image.grid(column=0, row=0)

# Create title label which will change depending on if it is in work or break phase
title_label = tk.Label(
	master=window,
	anchor="center",
	text="WORK",
	fg=TITLE_FONT_COLOR,
	bg="black",
	font=(TITLE_FONT_NAME, TITLE_FONT_HEIGHT, TITLE_FONT_TYPE),
)
title_label.grid(column=0, row=0)

# Create padding label
padding_label = tk.Label(master=window, text="", bg=WINDOW_BG_COLOR)
padding_label.grid(column=0, row=1)

# Start button
start_button = tk.Button(
	text="START",
	highlightthickness=0,
	command=start,
	font=(TEXT_FONT_NAME, TEXT_FONT_HEIGHT, TEXT_FONT_TYPE)
)
start_button.grid(column=0, row=2)

# Create padding label
padding_label = tk.Label(master=window, text="", bg=WINDOW_BG_COLOR)
padding_label.grid(column=0, row=3)

# Pause button
pause_button = tk.Button(
	text="PAUSE",
	highlightthickness=0,
	command=pause_resume,
	font=(TEXT_FONT_NAME, TEXT_FONT_HEIGHT, TEXT_FONT_TYPE)
)
pause_button.grid(column=0, row=4)

# Create padding label
padding_label = tk.Label(master=window, text="", bg=WINDOW_BG_COLOR)
padding_label.grid(column=0, row=5)

# Reset button
reset_button = tk.Button(
	text="RESET",
	highlightthickness=0,
	command=reset,
	font=(TEXT_FONT_NAME, TEXT_FONT_HEIGHT, TEXT_FONT_TYPE)
)
reset_button.grid(column=0, row=6)

# Create padding label
padding_label = tk.Label(master=window, text="", bg=WINDOW_BG_COLOR)
padding_label.grid(column=0, row=7)

# Create timer label
timer_label = tk.Label(
	master=window,
	anchor="center",
	text="",
	fg=TITLE_FONT_COLOR,
	bg=WINDOW_BG_COLOR,
	font=(TITLE_FONT_NAME, TITLE_FONT_HEIGHT, TITLE_FONT_TYPE),
)
timer_label.grid(column=0, row=8)

# Keep window looping and open
window.mainloop()
