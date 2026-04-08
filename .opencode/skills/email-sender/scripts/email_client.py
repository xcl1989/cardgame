#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SMTP Email Client
使用标准 SMTP 协议发送邮件，支持主流邮箱服务
"""

import smtplib
import json
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional, List, Dict, Any, Union
from datetime import datetime


class EmailClient:
    """SMTP 邮件客户端"""

    DEFAULT_RECIPIENT = "49781545@qq.com"

    def __init__(
        self, config_path: Optional[str] = None, skip_config_check: bool = False
    ):
        """
        初始化客户端

        Args:
            config_path: 配置文件路径，默认为 assets/config.json
            skip_config_check: 是否跳过配置文件存在检查，默认为 False
        """
        if config_path is None:
            config_path = str(Path(__file__).parent.parent / "assets" / "config.json")

        self.config_path = Path(config_path)
        self.config = self._load_config(skip_check=skip_config_check)

        self.smtp_server = self.config.get("smtpServer", "smtp.qq.com")
        self.smtp_port = self.config.get("smtpPort", 465)
        self.email = self.config.get("email", "")
        self.password = self.config.get("password", "")
        self.sender_name = self.config.get("senderName", "Email Sender")

    def _load_config(self, skip_check: bool = False) -> Dict[str, Any]:
        """
        加载配置文件

        Args:
            skip_check: 是否跳过文件存在检查，默认为 False
        """
        if not skip_check and not self.config_path.exists():
            raise FileNotFoundError(f"配置文件不存在：{self.config_path}")

        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def send_email(
        self,
        to: Union[str, List[str]],
        subject: str,
        content: Optional[str] = None,
        html: Optional[str] = None,
        attachments: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        发送邮件

        Args:
            to: 收件人邮箱（单个或列表）
            subject: 邮件主题
            content: 邮件正文（纯文本）
            html: 邮件正文（HTML）
            attachments: 附件文件路径列表

        Returns:
            发送结果
        """
        recipients = [to] if isinstance(to, str) else to

        if not recipients:
            recipients = [self.DEFAULT_RECIPIENT]

        if not content and not html:
            return {
                "success": False,
                "errorCode": "InvalidParameterValue",
                "message": "邮件内容不能为空（content 或 html 至少提供一个）",
            }

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{self.sender_name} <{self.email}>"
        msg["To"] = ", ".join(recipients)

        if content:
            msg.attach(MIMEText(content, "plain", "utf-8"))
        if html:
            msg.attach(MIMEText(html, "html", "utf-8"))

        if attachments:
            for file_path in attachments:
                if Path(file_path).exists():
                    msg = self._add_attachment(msg, file_path)
                else:
                    return {
                        "success": False,
                        "errorCode": "FileNotFound",
                        "message": f"附件文件不存在：{file_path}",
                    }

        server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
        server.login(self.email, self.password)
        server.sendmail(self.email, recipients, msg.as_string())
        server.quit()

        return {
            "success": True,
            "recipient": recipients if len(recipients) > 1 else recipients[0],
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": "sent",
        }

    def _add_attachment(self, msg: MIMEMultipart, file_path: str) -> MIMEMultipart:
        """添加附件"""
        path = Path(file_path)

        with open(path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())

        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f'attachment; filename="{path.name}"')

        msg.attach(part)
        return msg

    def send_batch_email(
        self,
        to_list: List[str],
        subject: str,
        content: Optional[str] = None,
        html: Optional[str] = None,
        attachments: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        群发邮件

        Args:
            to_list: 收件人列表
            subject: 邮件主题
            content: 邮件正文（纯文本）
            html: 邮件正文（HTML）
            attachments: 附件文件路径列表

        Returns:
            发送统计结果
        """
        success_count = 0
        failed_count = 0
        failed_recipients = []

        for recipient in to_list:
            result = self.send_email(
                to=recipient,
                subject=subject,
                content=content,
                html=html,
                attachments=attachments,
            )

            if result.get("success"):
                success_count += 1
            else:
                failed_count += 1
                failed_recipients.append(recipient)

        return {
            "success": failed_count == 0,
            "total": len(to_list),
            "success_count": success_count,
            "failed_count": failed_count,
            "failed_recipients": failed_recipients,
        }

    def test_connection(self) -> Dict[str, Any]:
        """
        测试连接

        Returns:
            测试结果
        """
        try:
            server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            server.login(self.email, self.password)
            server.quit()

            return {
                "success": True,
                "message": "连接成功",
                "smtp_server": self.smtp_server,
                "email": self.email,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }

        except smtplib.SMTPAuthenticationError:
            return {"success": False, "message": "邮箱账号或授权码错误"}
        except Exception as e:
            return {"success": False, "message": str(e)}


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description="SMTP 邮件发送 - 发送邮件")
    parser.add_argument("--to", type=str, help="收件人邮箱")
    parser.add_argument("--to-list", type=str, help="收件人列表文件路径")
    parser.add_argument("--subject", type=str, required=True, help="邮件主题")
    parser.add_argument("--content", type=str, help="邮件正文（纯文本）")
    parser.add_argument("--html", type=str, help="邮件正文（HTML）")
    parser.add_argument(
        "--attachments", type=str, help="附件文件路径（多个用逗号分隔）"
    )
    parser.add_argument("--config", type=str, help="配置文件路径")
    parser.add_argument("--test", action="store_true", help="测试连接")

    args = parser.parse_args()

    # 测试连接
    if args.test:
        client = EmailClient(args.config)
        result = client.test_connection()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # 验证参数
    if not args.to and not args.to_list:
        print("ERROR: 请指定收件人 (--to 或 --to-list)")
        return

    # 初始化客户端
    try:
        client = EmailClient(args.config)
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        return

    # 解析附件
    attachment_list = None
    if args.attachments:
        attachment_list = [p.strip() for p in args.attachments.split(",")]

    # 群发模式
    if args.to_list:
        to_list_path = Path(args.to_list)
        if not to_list_path.exists():
            print(f"ERROR: 收件人列表文件不存在：{to_list_path}")
            return

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

    # 单发模式
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
