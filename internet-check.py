import requests
import speedtest
import time as t
from datetime import datetime, time
import csv
import schedule
import threading
from rich.console import Console
#from alive_progress import alive_bar
#from alive_progress.styles import showtime
#from halo import Halo

console = Console()

# Insert path to data files here
datapath = r""
text_file = rf'{datapath}\no_internet.txt'
speed_file = rf'{datapath}\speed.csv'

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

        line = "-"*45

        print(f"\n{line}")
        console.print(current_time)
        console.print(f"[cyan]Download: {download}[/]\n[magenta]Upload: {upload}[/]")
        print(f"Speedtest Duration: {speed_dur}")
        print(f"Write Duration: {write_dur}")
        print(f"{line}")
    else:
        print(f"\n{line}")
        print(f"No internet @ {current_time}")
        print(f"{line}")

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


# TODO add option to choose minute offset
hours = [
    '00:15', '01:15', '02:15', '03:15', '04:15', '05:15', 
    '06:15', '07:15', '08:15', '09:15', '10:15', '11:15', 
    '12:15', '13:15', '14:15', '15:15', '16:15', '17:15', 
    '18:15', '19:15', '20:15', '21:15', '22:15', '23:15'
]

def schedule_test():
    delay = int(input("Time between tests: "))
    offset = int(input("Offset: "))

    i = offset
    while i < len(hours):
        schedule.every().day.at(hours[i]).do(run_threaded, speed_check)
        i += delay

#def status():
#    now = datetime.now()
#    current_time = now.strftime("%H:%M:%S")
#    spinner = Halo(text='Running', spinner={"interval": 80,	"frames": ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]})
#    spinner.start()

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

#schedule.every(15).seconds.do(run_threaded, internet_on)
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
console.print("Start time: ", datetime.now(), style="yellow")
#status()

#@Halo(text='Running', spinner={"interval": 80,	"frames": ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]})
def main():
    with console.status("Running") as status:
        while True:
            schedule.run_pending()
            t.sleep(1)



if __name__ == "__main__":
    main()

