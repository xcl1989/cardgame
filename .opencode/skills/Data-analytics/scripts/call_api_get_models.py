#!/usr/bin/env python3
"""
API 配置加载模块
"""

import os
import json
from pathlib import Path


def get_config_path() -> Path:
    """获取配置文件路径（技能根目录下的 api_config.json）"""
    skill_dir = Path(__file__).parent.parent
    return skill_dir / "api_config.json"


def get_api_key_from_config() -> str:
    """从配置文件读取 API 密钥"""
    config_path = get_config_path()
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                return config.get("hecomapiKey", "")
        except (json.JSONDecodeError, IOError):
            return ""
    return ""


def save_api_key_to_config(api_key: str) -> bool:
    """保存 API 密钥到配置文件"""
    config_path = get_config_path()
    try:
        config = {}
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        config["hecomapiKey"] = api_key
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except (IOError, json.JSONDecodeError) as e:
        print(f"WARNING: 保存配置失败: {e}")
        return False


def get_api_key() -> str:
    """
    获取 API 密钥（优先级：环境变量 > 配置文件）

    Returns:
        API 密钥字符串

    Raises:
        ValueError: 当未设置 API 密钥时
    """
    api_key = os.environ.get("hecomapiKey", "")
    if not api_key:
        api_key = get_api_key_from_config()
    if not api_key:
        raise ValueError(
            f"API 密钥未设置。\n"
            f"请在技能根目录的 api_config.json 文件中添加配置:\n"
            f'{{"hecomapiKey": "your-api-key-here"}}'
        )
    return api_key
