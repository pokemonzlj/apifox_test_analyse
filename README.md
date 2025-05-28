# 引言
适合于只需要对接口做基础测试的测试团队的接口测试框架！测试人员只需要会用apifox写接口测试用例，就可以完整生成整套测试代码！  
大大降低了入门学习的门槛，提升整个团队的效率！  
## 介绍
APIFOX的CLI命令只能单条执行，无法批量执行并统计完整执行结果。
脚本用于批量执行APIFOX的CLI命令，待接口自动化测试用例执行后，统计所有用例的执行情况。  
并输出执行结果和失败的用例详情，发送通知到指定的企微、飞书等工具：  
![image](https://github.com/user-attachments/assets/0fbead47-c4d2-40d3-ba8b-9f4fc9404385)  
# 使用介绍  
接口测试用例只需要正常在APIFOX上写，然后生成CLI，支持新老版本CLI  
![image](https://github.com/user-attachments/assets/2aa61d3e-5354-4f50-98b1-a900ac73b8ab)  
![image](https://github.com/user-attachments/assets/1bf744d3-78ae-422b-a0a7-715135ec3167)  
然后将CLI地址复制出来，写入excel文件apifox_url.xlsx中既可：  
![image](https://github.com/user-attachments/assets/a504c2ae-f6f9-469f-8def-2a135819e720)  
然后运行total_test.py既可  
## 更新记录
更新一版内容，APIFOX返回的执行结果json日志的结构做了更新，做了适配  
![image](https://github.com/user-attachments/assets/08b154ae-1a07-4a34-b9ba-7de83755f417)  
