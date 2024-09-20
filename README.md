用于APIFOX的接口自动化测试用例执行后，统计所有用例的执行情况  
并输出执行结果和失败的用例详情
![1708927889150](https://github.com/pokemonzlj/apifox_test_analyse/assets/35096840/b63ca42a-f52e-4c42-8e49-d045a4104db6)  
接口测试用例正常在APIFOX上写，然后生成CLI  
![image](https://github.com/user-attachments/assets/2aa61d3e-5354-4f50-98b1-a900ac73b8ab)  
然后将地址写入excel中apifox_url.xlsx：  
![image](https://github.com/user-attachments/assets/a504c2ae-f6f9-469f-8def-2a135819e720)  
然后运行total_test.py既可  

更新一版内容，APIFOX返回的执行结果json日志的结构做了更新，做了适配  
![image](https://github.com/user-attachments/assets/08b154ae-1a07-4a34-b9ba-7de83755f417)  
