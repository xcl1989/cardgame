#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试邮箱连接
"""

import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from email_client import EmailClient


def main():
    """测试连接"""
    print("正在测试邮箱连接...")

    try:
        client = EmailClient()
        result = client.test_connection()

        if result.get("success"):
            print("✅ 连接成功！")
            print(f"邮箱：{result.get('email')}")
            print(f"SMTP: {result.get('smtp_server')}")
            print(f"时间：{result.get('timestamp')}")
        else:
            print("❌ 连接失败")
            print(f"错误：{result.get('message')}")

    except FileNotFoundError as e:
        print("❌ 配置文件不存在")
        print(f"请创建配置文件：{e}")
        print("\n配置文件格式：")
        print("""
{
  "smtpServer": "smtp.qq.com",
  "smtpPort": 465,
  "email": "your-email@qq.com",
  "password": "your-auth-code",
  "senderName": "Your Name"
}
        """)
    except Exception as e:
        print(f"❌ 错误：{e}")


if __name__ == "__main__":
    main()
