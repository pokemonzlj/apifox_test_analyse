用于APIFOX的接口自动化测试用例执行后，统计所有用例的执行情况  
并输出执行结果和失败的用例详情
![image](https://github.com/user-attachments/assets/0fbead47-c4d2-40d3-ba8b-9f4fc9404385)  
  
接口测试用例正常在APIFOX上写，然后生成CLI  
![image](https://github.com/user-attachments/assets/2aa61d3e-5354-4f50-98b1-a900ac73b8ab)  
然后将地址写入excel中apifox_url.xlsx：  
![image](https://github.com/user-attachments/assets/a504c2ae-f6f9-469f-8def-2a135819e720)  
然后运行total_test.py既可  

更新一版内容，APIFOX返回的执行结果json日志的结构做了更新，做了适配  
![image](https://github.com/user-attachments/assets/08b154ae-1a07-4a34-b9ba-7de83755f417)  
