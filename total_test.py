from apifox import apifox_auto_test
import schedule
import time
import datetime
import subprocess


# 设置日志记录
# logging.basicConfig(filename='scheduler.log', level=logging.INFO, format='%(asctime)s - %(message)s')


def total_test(online=False):
    # 在这里调用 apifox.py 文件中的 total_test 函数
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
    if online:
        print('{}:Running total_test with online parameter: True'.format(date_time))
    else:
        print('{}:Running total_test with online parameter: False'.format(date_time))
    test = apifox_auto_test()
    test.total_test(online)


# 定义定时任务
def schedule_jobs(online=False):
    start_time = "09:00"
    end_time = "20:00"
    interval_hours = 3

    current_time = datetime.datetime.strptime(start_time, "%H:%M")
    end_time = datetime.datetime.strptime(end_time, "%H:%M")

    while current_time <= end_time:
        formatted_time = current_time.strftime("%H:%M")
        schedule.every().day.at(formatted_time).do(total_test, online)
        current_time += datetime.timedelta(hours=interval_hours)


# 执行定时任务
if __name__ == "__main__":
    schedule_jobs(True)
    while True:
        schedule.run_pending()  # 调用以检查是否有定时任务需要执行
        time.sleep(5)
