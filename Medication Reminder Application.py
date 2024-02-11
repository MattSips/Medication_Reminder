# import modules
import time
import datetime
import http.client, urllib
from pushoverSecrets1 import token, user

# create reminder function
def reminder():
    # Create dictionary on drug and waiting time between doses, ask about drug and when it was taken
    print("What medicine is it that you want to be reminded about?")
    drug = str(input())
    drug_dict = {"Codeine": 360, "Paracetamol": 240, "Ibuprofen": 240, "Movicol": 720}
    tries = 0
    while drug not in drug_dict:
        tries += 1
        if tries == 2:
            print("This is your last try\n")
        if tries == 3:
            print("Please Start Again")
            return
        print("Did you enter the correct drug?, Try Again!")
        drug = str(input())


    print("What time did you take the medicine? (In Army time i.e. 15:30)")
    take_time = str(input()).split()
    time_of_take=take_time

    for time_1 in take_time:
        hour, min = [int(i) for i in time_1.split(":")]
        min_digit = min
        if min < 10:
            min_digit = "0{}".format(min)
            # print("you took {} at {}:{}".format(drug, hour, min_digit))

    # for loop to go through list of drugs and wait times

    for key in drug_dict:
        val = int(hour) * 60 + int(min)
        current_time = val
        if drug == key:
            next_take_total = drug_dict[key] + current_time
            wait_time = drug_dict[key] * 60
            if next_take_total > 1440:
                next_take_total = next_take_total - 1440
            n_time_h = next_take_total // 60
            n_time_m = next_take_total % 60
            reminder_time = str(n_time_h) + ":" + str(n_time_m)
            drug=drug
            if min < 10:
                reminder_time = str(n_time_h) + ":0{}".format(min)
                min = "0{}".format(min)
                print("Since you took {} at {}:{}, you can take the next dose at {}".format(drug, hour, min, reminder_time))
                break
            print("Since you took", drug, " at", hour, ":", min, "you can take the next dose at", reminder_time)
            return

    # create a time buff and then send a notification using pushover notification application

    time.sleep(wait_time) # wait time till reminder kicks off
    print("It has been {} minutes, and it is now time to take your next dose of {}".format(int(wait_time/60), drug))
    # create connection
    conn = http.client.HTTPSConnection("api.pushover.net:443")

    # make POST request to send message
    conn.request("POST", "/1/messages.json",
                 urllib.parse.urlencode({
                     "token": token,
                     "user": user,
                     "title": "Medication Reminder",
                     "message": "It has been {} minutes, and it is now time to take your next dose of {}".format(int(wait_time/60), drug),
                     "url": "",
                     "priority": "0"
                 }), {"Content-type": "application/x-www-form-urlencoded"})
    conn.getresponse()
# run function
reminder()
