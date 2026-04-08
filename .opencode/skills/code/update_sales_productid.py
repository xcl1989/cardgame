import mysql.connector
import json
from decimal import Decimal
from datetime import datetime, date, time
import random

# 定义一个函数将 Decimal 转换为 float
def convert_to_serializable(obj):
    if isinstance(obj, Decimal):
        return float(obj)  # 将 Decimal 转换为 float
    elif isinstance(obj, (datetime, date, time)):
        return obj.isoformat()  # 将日期时间对象转换为ISO格式字符串
    elif isinstance(obj, bytes):
        return obj.decode('utf-8')  # 将字节对象解码为UTF-8字符串
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def sqlexecute(sqltext):
    # 连接数据库
    conn = mysql.connector.connect(
        host="127.0.0.1",       # 主机地址
        user="root",            # 用户名
        password="12345678",  # 密码
        database="Test"   # 数据库名称
    )
    # 创建游标
    cursor = conn.cursor()

    # 执行查询 SQL
    sql_query = sqltext
    cursor.execute(sql_query)

    # 获取查询结果
    results = cursor.fetchall()
    column_names = cursor.column_names
    rows = []
    for row in results:
        rows.append(row)

    # 转换整个数据结构
    json_data = json.dumps(rows, default=convert_to_serializable, ensure_ascii=False)
    column_names = json.dumps(column_names, ensure_ascii=False)
    #json_data = json_data.replace('"', "'")
    # 关闭游标和连接
    cursor.close()
    conn.close()
    print(column_names)
    print(json_data)
    return json.dumps(
        {
            "column_names": column_names,
            "data": json_data
        }
    )


def update_sales_productid():
    """为sales表的productid字段随机赋值1，2，3，4，5"""
    # 连接数据库
    conn = mysql.connector.connect(
        host="127.0.0.1",       # 主机地址
        user="root",            # 用户名
        password="12345678",  # 密码
        database="Test"   # 数据库名称
    )
    # 创建游标
    cursor = conn.cursor()

    # 为每个记录随机分配productid值（1到5之间）
    sql_query = """
    UPDATE sales 
    SET productid = FLOOR(1 + RAND() * 5)
    """
    
    try:
        cursor.execute(sql_query)
        conn.commit()
        print(f"成功更新了 {cursor.rowcount} 条记录的productid字段")
    except Exception as e:
        print(f"更新失败: {e}")
        conn.rollback()
    finally:
        # 关闭游标和连接
        cursor.close()
        conn.close()


if __name__ == "__main__":
    # 先执行随机更新
    update_sales_productid()
    
    # 可以再执行查询来验证更新结果
    # sqlexecute("SELECT * FROM sales LIMIT 10;")