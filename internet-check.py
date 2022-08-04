import requests
import speedtest
import time as t
from datetime import datetime, time
import csv
import schedule
import threading
#from alive_progress import alive_bar
#from alive_progress.styles import showtime
from halo import Halo

# Insert path to data files here
datapath = r""
text_file = rf'{datapath}\no_internet.txt'
speed_file = rf'{datapath}\speed.csv'

print(text_file)
print(speed_file)

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
        
        return False

def constant_check():
    global internet
    current_time = datetime.now()
    current_status = internet_on()
    if (current_status != internet) & internet_on():
        print("\n", "-"*40)
        print(f"Internet Returns @ {current_time}")
        print("-"*40)
        internet = True

        with open(text_file, "a") as myfile:
            myfile.write(f"Internet Returns @ {current_time}\n")


    elif (current_status != internet) & (not internet_on()):
        print("\n", "-"*40)
        print(f"No internet @ {current_time}")
        print("-"*40)
        internet = False

        with open(text_file, "a") as myfile:
            myfile.write(f"No internet @ {current_time}\n")

def speed_check():
    current_time = datetime.now()
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

hours = ['00:05', '01:05', '02:05', '03:05', '04:05', '05:05', '06:05', '07:05', '08:05', '09:05', '10:05', '11:05', '12:05', '13:05', '14:05', '15:05', '16:05', '17:05', '18:05', '19:05', '20:05', '21:05', '22:05', '23:05']

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

#schedule.every(30).seconds.do(run_threaded, internet_on)
schedule.every(5).seconds.do(run_threaded, constant_check)

#schedule.every().day.at("00:00").do(run_threaded, status)
#schedule.every(3).seconds.do(run_threaded, status)

#time = ['08:56']
#schedule.every().day.at(time[0]).do(run_threaded, speed_check)

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


# TODO: make internet check func run every 5 sec and only record when state flips
# TODO: add path input and store data outside git folder
