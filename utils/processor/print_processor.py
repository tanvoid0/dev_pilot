import os
import sys
import threading
import time

RESET_TEXT = "\033[0m"  # Reset text color to default
BLACK_TEXT = "\033[0;30m"
BBLACK_TEXT = "\033[1;30m"
RED_TEXT = "\033[0;31m"
BRED_TEXT = "\033[1;31m"
GREEN_TEXT = "\033[0;32m"
BGREEN_TEXT = "\033[1;32m"
YELLOW_TEXT = "\033[0;33m"
BYELLOW_TEXT = "\033[1;33m"
BLUE_TEXT = "\033[0;34m"
BBLUE_TEXT = "\033[1;34m"
PURPLE_TEXT = "\033[0;35m"
BPURPLE_TEXT = "\033[1;35m"
CYAN_TEXT = "\033[0;36m"
BCYAN_TEXT = "\033[1;36m"
WHITE_TEXT = "\033[0;37m"
BWHITE_TEXT = "\033[1;37m"

# Bold Colors
BOLD_BLACK_TEXT = "\033[1;30m"
BOLD_RED_TEXT = "\033[1;31m"
BOLD_GREEN_TEXT = "\033[1;32m"
BOLD_YELLOW_TEXT = "\033[1;33m"
BOLD_BLUE_TEXT = "\033[1;34m"
BOLD_PURPLE_TEXT = "\033[1;35m"
BOLD_CYAN_TEXT = "\033[1;36m"
BOLD_WHITE_TEXT = "\033[1;37m"

# Underlined Colors
UNDERLINED_BLACK_TEXT = "\033[4;30m"
UNDERLINED_RED_TEXT = "\033[4;31m"
UNDERLINED_GREEN_TEXT = "\033[4;32m"
UNDERLINED_YELLOW_TEXT = "\033[4;33m"
UNDERLINED_BLUE_TEXT = "\033[4;34m"
UNDERLINED_PURPLE_TEXT = "\033[4;35m"
UNDERLINED_CYAN_TEXT = "\033[4;36m"
UNDERLINED_WHITE_TEXT = "\033[4;37m"

# Background Colors
BACKGROUND_BLACK = "\033[40m"
BACKGROUND_RED = "\033[41m"
BACKGROUND_GREEN = "\033[42m"
BACKGROUND_YELLOW = "\033[43m"
BACKGROUND_BLUE = "\033[44m"
BACKGROUND_PURPLE = "\033[45m"
BACKGROUND_CYAN = "\033[46m"
BACKGROUND_WHITE = "\033[47m"

# High Intensity Colors
HIGH_INTENSITY_BLACK_TEXT = "\033[0;90m"
HIGH_INTENSITY_RED_TEXT = "\033[0;91m"
HIGH_INTENSITY_GREEN_TEXT = "\033[0;92m"
HIGH_INTENSITY_YELLOW_TEXT = "\033[0;93m"
HIGH_INTENSITY_BLUE_TEXT = "\033[0;94m"
HIGH_INTENSITY_PURPLE_TEXT = "\033[0;95m"
HIGH_INTENSITY_CYAN_TEXT = "\033[0;96m"
HIGH_INTENSITY_WHITE_TEXT = "\033[0;97m"

# Bold High Intensity Colors
BOLD_HIGH_INTENSITY_BLACK_TEXT = "\033[1;90m"
BOLD_HIGH_INTENSITY_RED_TEXT = "\033[1;91m"
BOLD_HIGH_INTENSITY_GREEN_TEXT = "\033[1;92m"
BOLD_HIGH_INTENSITY_YELLOW_TEXT = "\033[1;93m"
BOLD_HIGH_INTENSITY_BLUE_TEXT = "\033[1;94m"
BOLD_HIGH_INTENSITY_PURPLE_TEXT = "\033[1;95m"
BOLD_HIGH_INTENSITY_CYAN_TEXT = "\033[1;96m"
BOLD_HIGH_INTENSITY_WHITE_TEXT = "\033[1;97m"

# High Intensity Background Colors
HIGH_INTENSITY_BACKGROUND_BLACK = "\033[0;100m"
HIGH_INTENSITY_BACKGROUND_RED = "\033[0;101m"
HIGH_INTENSITY_BACKGROUND_GREEN = "\033[0;102m"
HIGH_INTENSITY_BACKGROUND_YELLOW = "\033[0;103m"
HIGH_INTENSITY_BACKGROUND_BLUE = "\033[0;104m"
HIGH_INTENSITY_BACKGROUND_PURPLE = "\033[0;105m"
HIGH_INTENSITY_BACKGROUND_CYAN = "\033[0;106m"
HIGH_INTENSITY_BACKGROUND_WHITE = "\033[0;107m"


def color_text(color, text):
    colorize = os.getenv('COLOR')
    if colorize:
        return color + str(text) + RESET_TEXT
    return text


# FIXME: bug. creates buffer with no stop
def countdown_timer(text, seconds):
    timer = threading.Thread(target=lambda: timer_thread(text, seconds))
    timer.daemon = True  # This makes the thread exit when the main program exits.
    timer.start()

    # Simulate some work being done
    time.sleep(seconds)  # Change this to the desired processing time
    print("")


def timer_thread(text, seconds):
    while True:
        seconds -= 1
        sys.stdout.write("\r{}: {} seconds".format(text, seconds))
        sys.stdout.flush()
        time.sleep(1)


# FIX ME: Not working
def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


def press_enter_to_continue():
    input(f"\nPress {color_text(RED_TEXT, 'Enter(*)')} to continue...")
