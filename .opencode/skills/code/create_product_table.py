import mysql.connector
import json
from decimal import Decimal
from datetime import datetime, date, time

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


def create_product_table():
    """创建Product表"""
    # 连接数据库
    conn = mysql.connector.connect(
        host="127.0.0.1",       # 主机地址
        user="root",            # 用户名
        password="12345678",  # 密码
        database="Test"   # 数据库名称
    )
    # 创建游标
    cursor = conn.cursor()

    # 删除已存在的表（如果存在）
    drop_table_sql = "DROP TABLE IF EXISTS Product;"
    
    # 创建Product表的SQL语句
    create_table_sql = """
    CREATE TABLE Product (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        price DECIMAL(10, 2),
        category VARCHAR(100),
        brand VARCHAR(100),
        stock_quantity INT DEFAULT 0,
        created_date DATE,
        updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
    """
    
    try:
        # 删除旧表
        cursor.execute(drop_table_sql)
        print("已删除可能存在的旧Product表")
        
        # 创建新表
        cursor.execute(create_table_sql)
        conn.commit()
        print("Product表创建成功！")
        
    except Exception as e:
        print(f"创建表失败: {e}")
        conn.rollback()
    finally:
        # 关闭游标和连接
        cursor.close()
        conn.close()


def insert_sample_products():
    """向Product表插入示例数据"""
    # 连接数据库
    conn = mysql.connector.connect(
        host="127.0.0.1",       # 主机地址
        user="root",            # 用户名
        password="12345678",  # 密码
        database="Test"   # 数据库名称
    )
    # 创建游标
    cursor = conn.cursor()

    # 插入示例产品的SQL语句
    insert_sql = """
    INSERT INTO Product (name, description, price, category, brand, stock_quantity, created_date) VALUES
    ('智能手机A', '高性能智能手机，配备先进摄像头系统', 2999.99, '电子产品', 'TechBrand', 150, '2023-01-15'),
    ('笔记本电脑B', '轻薄便携办公笔记本，适合商务人士', 5999.00, '电子产品', 'OfficePro', 80, '2023-02-20'),
    ('运动鞋C', '舒适透气跑步鞋，适合日常锻炼', 599.50, '服装鞋帽', 'SportMax', 300, '2023-03-10'),
    ('咖啡机D', '全自动家用咖啡机，一键制作美味咖啡', 1299.00, '家用电器', 'HomeLife', 60, '2023-04-05'),
    ('蓝牙耳机E', '无线降噪蓝牙耳机，音质出色', 799.99, '电子产品', 'AudioTech', 200, '2023-05-12');
    """
    
    try:
        cursor.execute(insert_sql)
        conn.commit()
        print(f"成功插入了 {cursor.rowcount} 条产品记录")
    except Exception as e:
        print(f"插入数据失败: {e}")
        conn.rollback()
    finally:
        # 关闭游标和连接
        cursor.close()
        conn.close()


if __name__ == "__main__":
    # 创建Product表
    create_product_table()
    
    # 插入示例数据
    insert_sample_products()
    
    # 查询验证
    print("\nProduct表内容：")
    sqlexecute("SELECT * FROM Product;")