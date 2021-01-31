import os
import sys
import datetime
import time
import gspread
from selenium import webdriver
import pyautogui as pyg

os.system('cls')
file = open(r'C:\Users\ica\Coding Projects\Python\zoomBot\log.txt', "a+")
testlink = "https://zoom.us/j/5826131212?pwd=N1NKSU90bDdKby9LQ1FMbkpTUFp0Zz09"

gc = gspread.service_account(
    filename=r'C:\Users\ica\Coding Projects\Python\zoomBot\creds.json')
sh = gc.open_by_key('1WA5qHhe-pUtsYrjXgY0jBYKVizzGY8t18A23tOrAP7s')
ws = sh.sheet1


def open_link(link):
    driver = webdriver.Chrome(executable_path="C:\\SeleniumDrivers\\chromedriver.exe")
    driver.get(link)
    time.sleep(1)
    button_coords = pyg.locateOnScreen(r'C:\Users\ica\Coding Projects\Python\zoomBot\open_meetings_button.png')
    position = pyg.position()
    pyg.click(button_coords)
    pyg.moveTo(position)
    time.sleep(2)
    driver.close()


def open_meeting(link, subject, date):
    file.write(f"Joined {subject} class: {date}\n")
    print(f"Joined {subject} class: {date}\n")
    open_link(link)


def end_program():
    file.write(f"Ended program: {date}\n\n")
    file.close()
    sys.exit()


date = datetime.datetime.now()
weekday = int(date.strftime("%w"))-1  # 0-monday, 6-sunday
file.write(f"Started program: {date}\n")

if weekday == -1:
    weekday = 6

if weekday != 5 and weekday != 6:
    loop = True
else:
    print("it is a weekend")
    loop = False
    end_program()

print(True)
range_o = weekday*5+2
range_s = ('').join(['B', str(weekday*5+2)])
range_e = ('').join(['B', str(weekday*5+5)])
range_a = (':').join([range_s, range_e])
time_column = ws.get(range_a)
print(range_a)

print("Today's meetings:")
for cell in time_column:
    try:
        meeting_time = cell[0]
        current_index = range_o + time_column.index(cell)
        subject = (ws.get(('').join(["A", str(current_index)]))[
                0][0]).lower()
        link = ws.get(('').join(["C", str(current_index)]))[0][0]
        print(f"row: {current_index}\nsubject: {subject}\ntime: {meeting_time}\nlink: {link}\n")
    except Exception as e:
        # print(f"{e}\n")
        pass

while loop == True:
    date = datetime.datetime.now()
    real_time = date.time()
    hour = real_time.hour
    minute = real_time.minute
    real_time = (':').join([str(hour), str(minute)])

    for cell in time_column:
        try:
            meeting_time = cell[0]
            current_index = range_o + time_column.index(cell)
            subject = (ws.get(('').join(["A", str(current_index)]))[
                       0][0]).lower()
            link = ws.get(('').join(["C", str(current_index)]))[0][0]
            # print(f"row: {current_index}\nsubject: {subject}\ntime: {meeting_time}\nlink: {link}")
            if meeting_time == real_time:
                open_meeting(link, subject, date)
            # else:
            #     print("False\n")

        except Exception as e:
            print(f"{e}\n")
            pass

    if real_time == "16:00":
        end_program()

    time.sleep(50)

# open_test_meeting(testlink)
end_program()
