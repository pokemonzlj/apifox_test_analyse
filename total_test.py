from apifox import apifox_auto_test
import schedule
import time
import datetime
import subprocess
from typing import Optional, List


# 设置日志记录
# logging.basicConfig(filename='scheduler.log', level=logging.INFO, format='%(asctime)s - %(message)s')


def total_test(send_online_message: bool = False, run_online_case_only: bool = False, 
               project_keywords: Optional[List[str]] = None):
    """执行测试用例
    
    Args:
        send_online_message: 是否发送线上消息
        run_online_case_only: 是否只执行线上用例
        project_keywords: 项目关键词列表，用于过滤特定项目的用例
    """
    # 在这里调用 apifox.py 文件中的 total_test 函数
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
    
    # 显示执行参数信息
    if send_online_message:
        print('{}:Running total_test with online parameter: True'.format(date_time))
    else:
        print('{}:Running total_test with online parameter: False'.format(date_time))
        
    if run_online_case_only:
        print('{}:Running online cases only'.format(date_time))
    else:
        print('{}:Running all cases with multi-threading'.format(date_time))
        
    if project_keywords:
        print('{}:Project filtering: {}'.format(date_time, project_keywords))
    
    test = apifox_auto_test()
    test.total_test(send_online_message, run_online_case_only, project_keywords)


# 定义定时任务，9点开始每3个小时执行一次
def schedule_jobs(send_online_message: bool = False, run_online_case_only: bool = False,
                  project_keywords: Optional[List[str]] = None):
    """设置定时任务
    
    Args:
        send_online_message: 是否发送线上消息
        run_online_case_only: 是否只执行线上用例
        project_keywords: 项目关键词列表，用于过滤特定项目的用例
    """
    start_time = "09:00"
    end_time = "20:00"
    interval_hours = 3
    current_time = datetime.datetime.strptime(start_time, "%H:%M")
    end_time = datetime.datetime.strptime(end_time, "%H:%M")

    while current_time <= end_time:
        formatted_time = current_time.strftime("%H:%M")
        schedule.every().day.at(formatted_time).do(
            total_test, 
            send_online_message, 
            run_online_case_only,
            project_keywords
        )
        current_time += datetime.timedelta(hours=interval_hours)
    
    print(f"定时任务已设置: 从 {start_time} 到 {end_time.strftime('%H:%M')}，每 {interval_hours} 小时执行一次")


# 执行定时任务
if __name__ == "__main__":
    # 示例：执行所有用例，发送线上消息
    schedule_jobs(True, False)
    
    # 示例：只执行线上用例
    # schedule_jobs(True, True)
    
    # 示例：执行特定项目的用例
    # schedule_jobs(True, False, ["用户管理", "订单系统"])
    
    # 示例：执行特定项目的线上用例
    # schedule_jobs(True, True, ["支付系统"])
    
    while True:
        # total_test(True)
        schedule.run_pending()  # 调用以检查是否有定时任务需要执行
        time.sleep(5)
