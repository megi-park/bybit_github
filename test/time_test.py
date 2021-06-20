from apscheduler.schedulers.background import BackgroundScheduler
import ohlcv
import time
import datetime as dt

sched = BackgroundScheduler() #background scheduler 를 sched 로 다시 define
sched.start()                 #backgorund scheduler start - 먼저 시작 후 
# sched.add_job(ohlcv.ohlcv,'cron', hour='0-23', minute='*/5')

# cron 으로 하는 경우는 다음과 같이 파라미터를 상황에 따라 여러개 넣어도 됩니다.
# 	매시간 10분마다 1초에 실행한다는 의미.
sched.add_job(ohlcv.ohlcv, "cron", hour = "0-23", minute = "*/10" , second="1", id="rsi")

while True:
    now = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("Running main process...............{0}".format(now))
    time.sleep(1)