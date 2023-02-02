import requests
import speedtest
import time as t
from datetime import datetime, time
import csv
import schedule
import threading
from rich.console import Console
import random
import os
#from alive_progress import alive_bar
#from alive_progress.styles import showtime
#from halo import Halo

console = Console()

# Insert path to data files here
#datapath = r""
#text_file = rf'{datapath}\no_internet.txt'
#speed_file = rf'{datapath}\speed.csv'
mainpath = os.getcwd()
text_file = os.path.join(mainpath, 'no_internet.txt')
speed_file = os.path.join(mainpath, 'speed.csv')

print(f"Data files: \n{text_file} \n{speed_file}")

# Initialize data files
with open(text_file, "a") as myfile:
    pass
with open(speed_file, 'a', newline='') as f:
    pass

internet = True

def internet_on():
    try:
        response = requests.get("http://google.com")
        if response.ok:
            return True
        else:
            return True
    except:
        current_time = datetime.now()
        #with open(text_file, "a") as myfile:
        #    myfile.write(f"No internet @ {current_time}\n")
        return False

def constant_check():
    global internet
    line = "-"*45
    current_time = datetime.now()
    current_status = internet_on()
    if internet == current_status:
        return
    elif (internet is False) & (current_status is True):
        print(f"\n{line}")
        #print(f"Internet: {internet}", flush=True)
        internet = True
        console.print(f"Internet Returns @ {current_time}", style="green")
        #print(f"Internet: {internet}")
        print(f"{line}", flush=True)

        with open(text_file, "a") as myfile:
            myfile.write(f"Internet Returns @ {current_time}\n")


    elif (internet is True) & (current_status is False):
        print(f"\n{line}")
        #print(f"Internet: {internet}", flush=True)
        internet = False
        console.print(f"No internet @ {current_time}", style="red")
        #print(f"Internet: {internet}")
        print(f"{line}", flush=True)

        with open(text_file, "a") as myfile:
            myfile.write(f"No internet @ {current_time}\n")

# TODO: add try/except if speedcheck fails
def speed_check():
    current_time = datetime.now()
    line = "-"*45
    try:
        if internet_on():
            start = t.time()
            st = speedtest.Speedtest()
            st.get_best_server()
            download = st.download()/1000000
            upload = st.upload()/1000000
            end = t.time()
            speed_dur = end - start

            start = t.time()
            fields = [current_time,download,upload]
            with open(speed_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
            end = t.time()
            write_dur = end - start


            print(f"\n{line}")
            console.print(current_time)
            console.print(f"[cyan]Download: {download}[/]\n[magenta]Upload: {upload}[/]")
            print(f"Speedtest Duration: {speed_dur}")
            print(f"Write Duration: {write_dur}")
            print(f"{line}")
        else:
            print(f"\n{line}")
            console.print(current_time)
            console.print(f"Speedtest unavailable \nNo Internet", style="red")
            print(f"{line}")
    except Exception as e:
        print(f"\n{line}")
        console.print(current_time)
        console.print(f"Speedtest unavailable \n{repr(e)}", style="red")
        print(f"{line}")

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


# TODO add randomized timing
hours = [
    '00:', '01:', '02:', '03:', '04:', '05:', 
    '06:', '07:', '08:', '09:', '10:', '11:', 
    '12:', '13:', '14:', '15:', '16:', '17:', 
    '18:', '19:', '20:', '21:', '22:', '23:'
]

def random_hours(hours):
    hour_min = hours
    for i, val in enumerate(hour_min):
        minute = random.randint(1, 59)
        while (minute % 5) == 0:
            minute = random.randint(1, 59)
        hr = val.split(":")
        hour_min[i] = f"{hr[0]}:{minute:02d}"
    return hour_min

def schedule_test(delay, offset, hours):

    hour_min = random_hours(hours)
    #print(hour_min)

    i = offset
    while i < len(hour_min):
        #print(i)
        #print(hour_min[i])
        schedule.every().day.at(hour_min[i]).do(run_threaded, speed_check).tag("speed")
        i += delay

def job_print():
    print("Jobs:")
    for i in schedule.get_jobs():
        print(f"    {repr(i).split(')')[0]})")

def reset():
    schedule.clear("speed")
    schedule_test(delay, offset, hours)
    job_print()

def test():
    #with open("test.txt", "a") as myfile:
    #    myfile.write(f"Testing")
    print("\nhello")

#schedule.every(15).seconds.do(run_threaded, internet_on)
schedule.every(5).seconds.do(run_threaded, constant_check)
schedule.every().day.at("00:00").do(run_threaded, reset)

delay = int(input("Time between tests: "))
offset = int(input("Offset: "))
schedule_test(delay, offset, hours)
#reset(delay, offset)

job_print()

#showtime()
console.print("Start time: ", datetime.now(), style="yellow")
#status()

#random_hours(hours)

#@Halo(text='Running', spinner={"interval": 80,	"frames": ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]})
def main():
    with console.status("Running") as status:
        while True:
            schedule.run_pending()
            t.sleep(1)



if __name__ == "__main__":
    main()

