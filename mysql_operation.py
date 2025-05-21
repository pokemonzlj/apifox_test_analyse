import pymysql
import datetime

def create_connection():
    return pymysql.connect(
        host='xxxxxxx.sql.tencentcdb.com',
        port=10086,
        user='test',
        password='xxxxxxxxxxxx',
        database='xxxxxx',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=20  # 增加连接超时设置
    )

def insert_fail_case(fail_case_name, occurrence_time, fail_case_parent, fail_comment, fail_path, fail_reason, is_online):
    """单条插入数据"""
    try:
        with connection.cursor() as cursor:
            # 定义插入数据的SQL语句
            sql = "INSERT INTO apifox_fail_case " \
                  "(fail_case_name, occurrence_time, fail_case_parent, fail_comment,  fail_path, fail_reason, is_online)" \
                  " VALUES (%s, %s, %s, %s, %s, %s, %s)"
            # 执行插入操作
            cursor.execute(sql, (fail_case_name, occurrence_time, fail_case_parent, fail_comment, fail_path, fail_reason, is_online))
            # 提交事务
            connection.commit()
            print("数据插入成功")
    except Exception as e:
        print(f"操作失败: {e}")
        # 回滚事务
        connection.rollback()
    finally:
        if connection:
            connection.close()  # 关闭连接

def batch_insert_fail_cases(fail_case_dict):
    """批量插入数据"""
    if not fail_case_dict:
        print("提示：报错接口用例数据集为空，跳过插入操作")
        return
    try:
        with create_connection() as connection:
            with connection.cursor() as cursor:
                # 构建动态VALUES占位符
                values_placeholder = ', '.join(['(%s, %s, %s, %s, %s, %s, %s)'] * len(fail_case_dict))
                sql = f"""
                    INSERT INTO apifox_fail_case 
                    (fail_case_name, occurrence_time, fail_case_parent, fail_comment, fail_path, fail_reason, is_online) 
                    VALUES {values_placeholder}
                """
                # 扁平化参数列表
                params = []
                for fail_case_name, case in fail_case_dict.items():
                    params.extend([
                        fail_case_name,
                        case.get('执行时间'),
                        case.get('测试用例集'),
                        case.get('断言内容'),
                        case.get('接口地址'),
                        case.get('错误内容'),
                        case.get('是否线上')
                    ])

                cursor.execute(sql, params)
                connection.commit()
                print(f"成功插入 {len(fail_case_dict)} 条数据")
    except Exception as e:
        print(f"操作失败: {e}")
        connection.rollback()
    finally:
        if connection:
            connection.close()


def batch_insert_fail_cases1(fail_case_dict):
    if not fail_case_dict:
        print("提示：报错接口用例数据集为空，跳过插入操作")
        return
    try:
        with create_connection() as conn:  # 每次创建新连接
            with conn.cursor() as cursor:
                # 分批次写入（每批200条）
                batch_size = 200
                cases = list(fail_case_dict.items())

                for i in range(0, len(cases), batch_size):
                    batch = cases[i:i + batch_size]
                    _execute_batch(conn, cursor, batch)

    except pymysql.Error as e:
        print(f"数据库错误: {e}")

def _execute_batch(conn, cursor, batch):
    placeholders = ', '.join(['(%s, %s, %s, %s, %s, %s, %s)'] * len(batch))
    sql = f"""INSERT INTO apifox_fail_case 
        (fail_case_name, occurrence_time, fail_case_parent, 
         fail_comment, fail_path, fail_reason, is_online)
        VALUES {placeholders}"""
    params = []
    for name, case in batch:
        params.extend([
            name,
            case.get(' 执行时间') or datetime.datetime.now(),  # 空值处理
            case.get(' 测试用例集'),
            case.get(' 断言内容'),
            case.get(' 接口地址'),
            case.get(' 错误内容')[:255],  # 防溢出
            case.get(' 是否线上', 0)
        ])
    try:
        cursor.execute(sql, params)
        conn.commit()
        print(f"成功写入 {len(batch)} 条")
    except pymysql.OperationalError as e:
        print(e)


if __name__ == "__main__":
    pass