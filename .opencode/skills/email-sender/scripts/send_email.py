#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发送邮件 - 命令行工具
"""

import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from email_client import EmailClient
import argparse
import json


def main():
    parser = argparse.ArgumentParser(description="SMTP 邮件发送")
    parser.add_argument("--to", type=str, help="收件人邮箱")
    parser.add_argument("--to-list", type=str, help="收件人列表文件路径")
    parser.add_argument("--subject", type=str, required=True, help="邮件主题")
    parser.add_argument("--content", type=str, help="邮件正文（纯文本）")
    parser.add_argument("--html", type=str, help="邮件正文（HTML）")
    parser.add_argument(
        "--attachments", type=str, help="附件文件路径（多个用逗号分隔）"
    )
    parser.add_argument("--config", type=str, help="配置文件路径")

    args = parser.parse_args()

    # 配置文件一定存在，跳过检查
    client = EmailClient(config_path=args.config, skip_config_check=True)

    if not args.to and not args.to_list:
        args.to = client.DEFAULT_RECIPIENT

    attachment_list = None
    if args.attachments:
        attachment_list = [p.strip() for p in args.attachments.split(",")]

    if args.to_list:
        to_list_path = Path(args.to_list)
        with open(to_list_path, "r", encoding="utf-8") as f:
            recipients = [line.strip() for line in f if line.strip()]

        result = client.send_batch_email(
            to_list=recipients,
            subject=args.subject,
            content=args.content,
            html=args.html,
            attachments=attachment_list,
        )

        print(f"发送完成:")
        print(f"  总计：{result['total']}")
        print(f"  成功：{result['success_count']}")
        print(f"  失败：{result['failed_count']}")

    else:
        result = client.send_email(
            to=args.to,
            subject=args.subject,
            content=args.content,
            html=args.html,
            attachments=attachment_list,
        )

        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
