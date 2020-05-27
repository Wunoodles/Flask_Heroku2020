import schedule
import time

def job():
    print("I'm working...")

second_5_j = schedule.every(5).seconds.do(job)


# 無窮迴圈
while True: 
    schedule.run_pending()
    time.sleep(1)


#