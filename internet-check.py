import requests
import speedtest
import time as t
from datetime import datetime, time
import csv
import schedule
import threading
from alive_progress import alive_bar
from alive_progress.styles import showtime
from halo import Halo


def internet_on():
    try:
        response = requests.get("http://google.com")

        if response.ok:
            return True
        else:
            return True
    except:
        current_time = datetime.now()
        with open("no_internet.txt", "a") as myfile:
            myfile.write(f"No internet @ {current_time}\n")
        print("\n", "-"*40)
        print(f"No internet @ {current_time}")
        print("-"*40)
        return False

def speed_check():
    current_time = datetime.now()
    if internet_on():
        start = t.time()
        st = speedtest.Speedtest()
        end = t.time()
        speed_dur = end - start

        start = t.time()
        fields = [current_time,st.download()/1000000,st.upload()/1000000]
        with open(r'speed.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
        end = t.time()
        write_dur = end - start

        download = st.download()/1000000
        upload = st.upload()/1000000

        print("\n", "-"*40)
        print(current_time)
        print(f"Download: {download}\nUpload: {upload}")
        print(f"Speedtest Duration: {speed_dur}")
        print(f"Write Duration: {write_dur}")
        print("-"*40)
    else:
        print("\n", "-"*40)
        print(f"No internet @ {current_time}")
        print("-"*40)

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

hours = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']

def schedule_test():
    delay = int(input("Time between tests: "))
    offset = int(input("Offset: "))

    i = offset
    while i < len(hours):
        schedule.every().day.at(hours[i]).do(run_threaded, speed_check)
        i += delay

def status():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    spinner = Halo(text='Running', spinner={"interval": 80,	"frames": ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]})
    spinner.start()

    #for i in range(5):
    #    print("Running", "."*i, end="\r")
    #    t.sleep(0.5)
    #with alive_bar(title="Running", unknown='dots_waves2', stats=False, monitor=False) as bar:
    #    while datetime.now().time() < time(23, 59, 55):
    #        bar()
    #        now = datetime.now()
    #        current_time = now.strftime("%H:%M:%S")

def test():
    #with open("test.txt", "a") as myfile:
    #    myfile.write(f"Testing")
    print("\nhello")

schedule.every(30).seconds.do(run_threaded, internet_on)
#schedule.every().day.at("00:00").do(run_threaded, status)
#schedule.every(3).seconds.do(run_threaded, status)

#schedule.every().day.at("19:45").do(run_threaded, speed_check)

#schedule.every().day.at("00:00").do(run_threaded, speed_check)
#schedule.every().day.at("03:00").do(run_threaded, speed_check)
#schedule.every().day.at("06:00").do(run_threaded, speed_check)
#schedule.every().day.at("09:00").do(run_threaded, speed_check)
#schedule.every().day.at("12:00").do(run_threaded, speed_check)
#schedule.every().day.at("15:00").do(run_threaded, speed_check)
#schedule.every().day.at("18:00").do(run_threaded, speed_check)
#schedule.every().day.at("21:00").do(run_threaded, speed_check)

schedule_test()

print("Jobs:", schedule.get_jobs())
#showtime()
print("Start time: ", datetime.now())
#status()

@Halo(text='Running', spinner={"interval": 80,	"frames": ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]})
def run():
    while True:
        schedule.run_pending()
        t.sleep(1)

run()
