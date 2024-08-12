# -*- coding: UTF-8 -*-
import os
from datetime import datetime
import subprocess
import requests
import json  # 标准库 json 主要用于 JSON 数据的读取和写入，而不提供直接的 JSONPath 功能
from jsonpath_ng import jsonpath, parse  # 专门的 JSONPath 解析库
import configparser
import openpyxl
import re


class apifox_auto_test():
    def __init__(self):
        self.total_case = 0
        self.total_fail_case = 0
        self.total_online_fail_case = 0
        self.jsonfile_list = []
        self.total_fail_case_info = {}
        # self.config = configparser.ConfigParser()
        # self.config.read("apifox_url.ini", encoding="utf-8")
        # # self.config.read("apifox_url_online.ini", encoding="utf-8")
        # # self.apifox_url_list = list(self.config['URL'].values())
        # self.apifox_url_list = [line.split(' ')[2] for line in self.config['URL'].values()]
        workbook = openpyxl.load_workbook('apifox_url.xlsx')
        worksheet = workbook.active
        values = [cell.value for cell in worksheet['H'] if cell.value is not None]
        self.apifox_url_list = [value.split(' ')[2] for value in values]
        workbook.close()
        # print(self.apifox_url_list)

    def run_command(self,
                    command="https://api.apifox.cn/api/v1/projects/2875535/api-test/ci-config/375963/detail?token=x4"):
        """执行apifox CLI的命令"""
        # apifox_cli_path = "C:/Users/hozest/AppData/Roaming/npm/node_modules/apifox-cli/bin/apifox"
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = "apifox-report-" + f"{date_time}"
        apifox_cli_path = "D:/Nodejs/node.exe C:/Users/hozest/AppData/Roaming/npm/node_modules/apifox-cli/bin/cli.js"
        apifox_command = apifox_cli_path + " run " + command + " -r json" + " --out-file {}".format(filename)
        # 输出到脚本目录下\apifox-reports文件夹
        # 使用subprocess运行命令
        try:
            result = subprocess.check_output(apifox_command, shell=True, stderr=subprocess.STDOUT,
                                             universal_newlines=False)
            #  将subprocess.check_output中的universal_newlines=True参数更改为False，这将返回未解码的字节字符串，而不是尝试将其解码为文本
            print("{}:命令执行成功:".format(date_time))
            print(result.decode("utf-8"))
            self.jsonfile_list.append(filename)
        except subprocess.CalledProcessError as e:
            print("{}:命令执行完成:".format(date_time))
            print(e.output.decode("utf-8"))
            self.jsonfile_list.append(filename)
        except Exception as e:
            print("{}:发生错误:".format(date_time))
            print(str(e))

    def deal_with_fail_reason(self, fail_reason):
        """针对返回的结果，做一层处理后输出"""
        pattern = re.compile(r'expected (\d+) to be below (\d+)')
        # 查找匹配项
        match = pattern.search(fail_reason)
        if match:
            first_number = int(match.group(1))
            second_number = int(match.group(2))
            first_number = first_number / 1000
            first_number = round(first_number, 2)
            second_number = second_number / 1000
            second_number = round(second_number, 2)
            fail_reason = "接口执行耗时{}秒，标准需要小于{}秒,要优化.".format(first_number, second_number)
            return fail_reason
        pattern = re.compile(r'expected (.+) to deeply equal (.+)')
        # 查找匹配项
        match = pattern.search(fail_reason)
        if match:
            first_number = int(match.group(1))
            second_number = int(match.group(2))
            fail_reason = "接口返回预期：{}，实际：{},存在偏差请检查.".format(second_number, first_number)
            return fail_reason
        pattern = re.compile(r'expected (.+) to not deeply equal (.+)')
        # 查找匹配项
        match = pattern.search(fail_reason)
        if match:
            first_number = int(match.group(1))
            second_number = int(match.group(2))
            fail_reason = "接口返回预期非：{}，实际：{},存在偏差请检查.".format(second_number, first_number)
            return fail_reason
        return fail_reason

    def json_analyse(self, filename="apifox-report-2023-09-12-17-20-08-602-0.json"):
        """分析输出的json报告"""
        path = "apifox-reports/"
        is_online_case = False
        file_path = path + filename
        if ".json" not in file_path:
            file_path += ".json"
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    # 使用 json.load() 解析 JSON 文件内容为 Python 数据结构
                    data = json.load(json_file)
                # 现在，'data' 变量包含了 JSON 文件中的数据，可以像访问字典一样访问其中的内容
                total_count = data['result']['stats']['requests']['total']
                fail_count = data['result']['stats']['requests']['failed']
                result_dict = {}
                jsonpath_expr = parse("$.collection.name")  # 取外部的整个测试用例集的名字
                # 使用 JSONPath 表达式提取数据
                matches_fail_case_parent = [match.value if match.value else 'None' for match in
                                            jsonpath_expr.find(data)]
                if matches_fail_case_parent:
                    matches_fail_case_parent = matches_fail_case_parent[0]
                if "(线上)" in matches_fail_case_parent:
                    is_online_case = True
                # 定义 JSONPath 表达式
                if fail_count > 0:
                    jsonpath_expr = parse("$.result.steps[*].id")
                    case_id = [match.value for match in jsonpath_expr.find(data)]
                    jsonpath_expr = parse("$.result.steps[*].name")
                    case_name = [match.value for match in jsonpath_expr.find(data)]
                    jsonpath_expr = parse("$.result.steps[*].metaInfo.httpApiPath")
                    case_url = [match.value for match in jsonpath_expr.find(data)]
                    # 先把整个用例的数据取出来，用来做下面报错数据的映射
                    cases_dict = {id_: (name, url) for id_, name, url in zip(case_id, case_name, case_url)}
                    # 把数据生成一个字典用来做下面的匹对
                    # print(cases_dict)
                    jsonpath_expr = parse("$.result.failures[*].error.message")
                    matches_fail_reason = [match.value for match in jsonpath_expr.find(data)]
                    jsonpath_expr = parse("$.result.failures[*].cursor.ref")
                    matches_fail_case_id = [match.value for match in jsonpath_expr.find(data)]
                    # print(matches_fail_case_id)
                    matches_fail_case = []
                    # 遍历失败ID列表
                    j = 0
                    for fail_id in matches_fail_case_id:
                        # 检查fail_id是否在cases_dict中
                        if fail_id in cases_dict:
                            # 从字典中获取case_name和case_url
                            case_name, case_url = cases_dict[fail_id]
                            # 创建一个包含所需信息的字典或元组，并将其添加到列表中
                            # 这里使用字典作为示例
                            matches_fail_case.append({
                                'case_name': case_name,
                                'case_url': case_url,
                                'fail_reason': matches_fail_reason[j]  # 获取对应的失败原因
                            })
                        j += 1
                            # jsonpath_expr = parse("$.result.failures[*].source.request.url.path")
                    # matches_fail_case_path_list = [match.value for match in jsonpath_expr.find(data)]
                    # # print(matches_fail_case_path_list)
                    # matches_fail_case_path_lists = []
                    # for l in matches_fail_case_path_list:
                    #     matches_fail_case_path = '/'.join(l)
                    #     matches_fail_case_path_lists.append(matches_fail_case_path)
                    # jsonpath_expr = parse("$.result.failures[*].source.request.url.host")
                    # matches_fail_case_host_list = [match.value for match in jsonpath_expr.find(data)]
                    # # print(matches_fail_case_host_list)
                    # matches_fail_case_host_lists = []
                    # for l in matches_fail_case_host_list:
                    #     matches_fail_case_host = '.'.join(l)
                    #     matches_fail_case_host_lists.append(matches_fail_case_host)
                    # print(matches_fail_reason)
                    # print(matches_fail_case)
                    # print(len(matches_fail_case))
                    for i in range(len(matches_fail_case)):
                        fail_case = matches_fail_case[i]
                        fail_case_name = fail_case['case_name']
                        fail_reason = fail_case['fail_reason']
                        fail_reason = self.deal_with_fail_reason(fail_reason)
                        fail_case_parent = matches_fail_case_parent
                        fail_path = fail_case['case_url']
                        result_dict[fail_case_name] = {
                            "错误内容": fail_reason,
                            "测试用例集": fail_case_parent,
                            "接口地址": fail_path,
                        }
                return total_count, fail_count, result_dict, is_online_case
            except json.decoder.JSONDecodeError as e:
                print(f"JSON解析错误：{str(e)}")
                return False
            except Exception as e:
                print(e)
                return False

    def send_message(self, message="", online=False):
        """通过webhook发送消息，online是false就发通知给测试群"""
        # message_json = json.dumps(message)
        data = {"msg_type": "text", "content": {"text": "{}".format(message)}}
        data = json.dumps(data)
        webhook_url_test = "https://open.feishu.cn/open-apis/bot/v2/hook/d"
        webhook_url_online = "https://open.feishu.cn/open-apis/bot/v2/hook/f"
        if online:
            response = requests.post(webhook_url_online, data=data, headers={'Content-Type': 'application/json'})
        else:
            response = requests.post(webhook_url_test, data=data, headers={'Content-Type': 'application/json'})
        # 检查响应结果
        if response.status_code == 200:
            print("Message sent successfully.")
        else:
            print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")

    def total_test(self, online=False):
        apifox_url_list = self.apifox_url_list
        for url in apifox_url_list:
            self.run_command(url)
        for file in self.jsonfile_list:
            if file:
                result = self.json_analyse(file)
                if not result:
                    continue
                total_count, fail_count, result_dict, is_online_case = result
                self.total_case += total_count
                self.total_fail_case += fail_count
                self.total_fail_case_info.update(result_dict)
                if is_online_case:
                    self.total_online_fail_case += fail_count
        message = "共测试接口用例{}条，失败{}条，其中线上{}条".format(self.total_case, self.total_fail_case, self.total_online_fail_case)
        message2 = "共测试接口用例{}条，失败{}条，失败的线下用例如下:\n".format(self.total_case, self.total_fail_case)
        if self.total_fail_case != 0:
            i = 1
            j = 1
            if self.total_online_fail_case == 0:
                message += "，线上没有出问题也不错！再接再厉！"
                for key, value in self.total_fail_case_info.items():
                    message2 += "{}.{}: {}\n".format(j, key, value)
                    j += 1
            else:
                message += "，失败的线上用例如下:\n"
                # 遍历字典的键值对并逐行输出
                for key, value in self.total_fail_case_info.items():
                    if "(线上)" in value['测试用例集'] or "（线上）" in value['测试用例集']:
                        message += "{}.{}: {}\n".format(i, key, value)
                        i += 1
                    else:
                        message2 += "{}.{}: {}\n".format(j, key, value)
                        j += 1
        else:
            message += "，震惊，再接再厉！"
        self.send_message(message, online)
        self.send_message(message2, False)


if __name__ == "__main__":
    apifox_test = apifox_auto_test()
    apifox_test.total_test(False)
    # apifox_test.json_analyse()
