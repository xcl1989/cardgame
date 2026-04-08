"""
从数据库获取图片数据并调用 API
支持 MySQL 数据库查询 conversation_images 表
Token 从 Redis 获取
"""

import pymysql
import redis
import json
import requests
import sys
import logging
import base64
from typing import Optional, Dict, Any
from dataclasses import dataclass

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


@dataclass
class DBConfig:
    """数据库配置"""

    host: str = "127.0.0.1"
    port: int = 3306
    user: str = "root"
    password: str = "12345678"
    database: str = "ANALYSE"
    charset: str = "utf8mb4"


@dataclass
class RedisConfig:
    """Redis 配置"""

    host: str = "localhost"
    port: int = 6379
    token_key: str = "user:admin:tokens"


class DatabaseImageProcessor:
    """数据库图片数据处理器"""

    def __init__(
        self,
        db_config: Optional[DBConfig] = None,
        redis_config: Optional[RedisConfig] = None,
        api_base_url: str = "http://127.0.0.1:8000",
        timeout: int = 30,
    ):
        """初始化处理器"""
        self.db_config = db_config or DBConfig()
        self.redis_config = redis_config or RedisConfig()
        self.api_base_url = api_base_url
        self.timeout = timeout
        self._token: Optional[str] = None

    def get_latest_image_from_db(self) -> Dict[str, Any]:
        """从数据库获取最新一条图片数据"""
        conn = None
        try:
            conn = pymysql.connect(
                host=self.db_config.host,
                port=self.db_config.port,
                user=self.db_config.user,
                password=self.db_config.password,
                database=self.db_config.database,
                charset=self.db_config.charset,
                cursorclass=pymysql.cursors.DictCursor,
            )

            with conn.cursor() as cursor:
                sql = """
                    SELECT id, message_id, filename, mime_type, base64_data, size, created_at
                    FROM conversation_images
                    ORDER BY created_at DESC
                    LIMIT 1
                """
                cursor.execute(sql)
                result = cursor.fetchone()

                if not result:
                    raise RuntimeError("未找到图片数据")

                logger.info(f"成功获取图片：{result['filename']}")
                return result

        except pymysql.Error as e:
            logger.error(f"数据库连接失败：{e}")
            raise
        finally:
            if conn:
                conn.close()

    def get_token_from_redis(self) -> str:
        """从 Redis 获取 Token"""
        if self._token:
            return self._token

        try:
            redis_client = redis.Redis(
                host=self.redis_config.host,
                port=self.redis_config.port,
                decode_responses=True,
                socket_connect_timeout=5,
            )

            token_data = redis_client.smembers(self.redis_config.token_key)
            if not token_data:
                raise RuntimeError(
                    f"Redis 中未找到 Token: {self.redis_config.token_key}"
                )

            token = token_data.pop()
            try:
                data = json.loads(token)
                if isinstance(data, dict):
                    token = data.get("token") or data.get("access_token") or token
            except json.JSONDecodeError:
                pass

            self._token = token
            logger.info("成功获取 Token")
            return token

        except redis.RedisError as e:
            logger.error(f"Redis 连接失败：{e}")
            raise
        except Exception as e:
            logger.error(f"获取 Token 失败：{e}")
            raise

    def call_person_api(
        self, person_data: Dict[str, Any], image_base64: str, image_filename: str
    ) -> Dict[str, Any]:
        """调用用户信息 API"""
        url = f"{self.api_base_url}/api/person"
        token = self.get_token_from_redis()

        payload = {
            "name": person_data.get("name", ""),
            "birth_date": person_data.get("birth_date", ""),
            "gender": person_data.get("gender", ""),
            "address": person_data.get("address", ""),
            "id_card": person_data.get("id_card", ""),
            "photo_base64": image_base64,
            "photo_filename": image_filename,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

        logger.info(f"调用用户信息 API: {url}")
        response = requests.post(
            url, json=payload, headers=headers, timeout=self.timeout
        )
        response.raise_for_status()

        return {
            "success": True,
            "status_code": response.status_code,
            "data": response.json() if response.text else {},
        }

    def call_contract_api(
        self, contract_data: Dict[str, Any], image_base64: str, image_filename: str
    ) -> Dict[str, Any]:
        """调用合同信息 API"""
        url = f"{self.api_base_url}/api/contract"
        token = self.get_token_from_redis()

        payload = {
            "contract_name": contract_data.get("contract_name", ""),
            "party_a": contract_data.get("party_a", ""),
            "party_b": contract_data.get("party_b", ""),
            "amount": contract_data.get("amount", 0),
            "remarks": contract_data.get("remarks", ""),
            "photo_base64": image_base64,
            "photo_filename": image_filename,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

        logger.info(f"调用合同信息 API: {url}")
        response = requests.post(
            url, json=payload, headers=headers, timeout=self.timeout
        )
        response.raise_for_status()

        return {
            "success": True,
            "status_code": response.status_code,
            "data": response.json() if response.text else {},
        }

    def process_id_card(self, person_info: Dict[str, Any]) -> Dict[str, Any]:
        """处理身份证件"""
        image_data = self.get_latest_image_from_db()

        result = self.call_person_api(
            person_data=person_info,
            image_base64=image_data["base64_data"],
            image_filename=image_data["filename"],
        )

        logger.info("身份证件处理完成")
        return result

    def process_contract(self, contract_info: Dict[str, Any]) -> Dict[str, Any]:
        """处理合同文档"""
        image_data = self.get_latest_image_from_db()

        result = self.call_contract_api(
            contract_data=contract_info,
            image_base64=image_data["base64_data"],
            image_filename=image_data["filename"],
        )

        logger.info("合同文档处理完成")
        return result


def main(extracted_data: Optional[Dict[str, Any]] = None):
    """
    主函数

    Args:
        extracted_data: 提取的数据（姓名、身份证号等）
    """
    processor = DatabaseImageProcessor()

    try:
        image_data = processor.get_latest_image_from_db()
        logger.info(f"获取到图片：{image_data['filename']}")

        if not extracted_data:
            extracted_data = {
                "name": "韦小宝",
                "birth_date": "1654-12-20",
                "gender": "男",
                "address": "北京市东城区景山前街 4 号紫禁城敬事房",
                "id_card": "11204416541220243X",
            }

        logger.info("正在调用 API...")

        if (
            "contract_name" in extracted_data
            or "party_a" in extracted_data
            or "party_b" in extracted_data
        ):
            result = processor.call_contract_api(
                contract_data=extracted_data,
                image_base64=image_data["base64_data"],
                image_filename=image_data["filename"],
            )
        else:
            result = processor.call_person_api(
                person_data=extracted_data,
                image_base64=image_data["base64_data"],
                image_filename=image_data["filename"],
            )

        print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        logger.error(f"处理失败：{e}")
        sys.exit(1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="从数据库获取图片数据并调用 API")
    parser.add_argument("--data", type=str, help="提取的数据（JSON 格式）")

    args = parser.parse_args()

    extracted_data = None
    if args.data:
        extracted_data = json.loads(args.data)

    main(extracted_data=extracted_data)
