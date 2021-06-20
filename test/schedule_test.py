from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
import ohlcv
import time
import datetime as dt
import schedule
import bybit
import mkdntjr12_bybit1


client = bybit.bybit(test=False, api_key=mkdntjr12_bybit1.api_key, api_secret=mkdntjr12_bybit1.secret_key)
info = client.Market.Market_symbolInfo(symbol="BTCUSD").result() # 마켓에서 거래되는 모든 거래쌍에 대한 현재 정보를 가져오는 것 keys 에 info 를 넣고 for i 문을 통해 안에 뭐가 들어있는지 확인이 가능함

sched_2 = BackgroundScheduler() #background scheduler 를 sched 로 다시 define
# sched.start()                 #backgorund scheduler start - 먼저 시작 후 
# sched.add_job(job, "cron", hour = "0-23", minute = "*/10" , second="*/1", id="rsi")


# sched = BlockingScheduler()

# 매일 12시 30분에 실행
# @sched.scheduled_job('interval', seconds=1, id='test_1')
# def job1():
#     print(f'job1 : {time.strftime("%H:%M:%S")}')

#     sched.shutdown

# 매일 12시 30분에 실행
# @sched.scheduled_job('cron', hour='12', minute='30', id='test_2')
# def job2():
#     print(f'job2 : {time.strftime("%H:%M:%S")}')

# 이런식으로 추가도 가능. 매분에 실행
# sched.add_job(job2, 'cron', second='0', id="test_3")


# print('sched before~')
# sched.start()
# print('sched after~') # 여긴 실행 안됨. Blocking 이기 때문에.

count = 0

def job_function():
    print("job executing")
    global count, scheduler

    # Execute the job till the count of 5 
    count = count + 1
    if count == 5:
        scheduler.remove_job('my_job_id')


scheduler = BlockingScheduler()
scheduler.add_job(job_function, 'interval', seconds=1, id='my_job_id')
scheduler.start()


print("end")

# while True:
#     print("Working .....")
#     time.sleep(1)