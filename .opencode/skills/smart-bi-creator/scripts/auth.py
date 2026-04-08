#!/usr/bin/env python3
"""共享认证模块 - 统一加载 header.json 中的认证信息"""

import json
import time
import requests
from pathlib import Path
from typing import Dict, Optional, Callable
from functools import wraps


def load_headers(
    header_file: Optional[str] = None,
    extra_headers: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    """从 header.json 加载认证信息并构建请求头

    Args:
        header_file: header.json 路径，默认使用脚本同目录下的文件
        extra_headers: 额外要添加的请求头

    Returns:
        完整的请求头字典
    """
    if header_file is None:
        header_file = str(Path(__file__).parent / "header.json")

    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json",
        "clientTag": "web",
        "app": "biapp",
        "user-locale": "zh-CN",
    }

    path = Path(header_file)
    if path.exists():
        with open(path, "r") as f:
            header_data = json.load(f)
        headers.update({k: v for k, v in header_data.items() if k != "Content-Type"})
    else:
        print(f"警告：未找到 header.json 文件 ({path})")

    if extra_headers:
        headers.update(extra_headers)

    return headers


def get_base_url(env: str = "dev") -> str:
    """获取 API 基础 URL

    Args:
        env: 环境标识 (dev/test/prod)

    Returns:
        API 基础 URL
    """
    urls = {
        "dev": "https://dev.cloud.hecom.cn",
        "test": "https://test.cloud.hecom.cn",
        "prod": "https://cloud.hecom.cn",
    }
    return urls.get(env, urls["dev"])


def get_preview_url(screen_id: int, base_url: Optional[str] = None) -> str:
    """获取大屏预览 URL

    Args:
        screen_id: 大屏 ID
        base_url: 基础 URL（自动去除 /biserver 后缀）

    Returns:
        预览 URL
    """
    if base_url is None:
        base_url = get_base_url()
    clean_url = base_url.split("/biserver")[0] if "/biserver" in base_url else base_url
    return f"{clean_url}/largescreenpreview?id={screen_id}"


def with_retry(
    func: Callable,
    max_retries: int = 3,
    initial_delay: float = 0.5,
    backoff_factor: float = 2.0,
) -> Callable:
    """为 requests 请求添加重试装饰器

    Args:
        func: 要包装的函数（通常是 requests.get/post）
        max_retries: 最大重试次数
        initial_delay: 初始重试延迟（秒）
        backoff_factor: 退避因子（每次重试延迟翻倍）

    Returns:
        包装后的函数
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        last_exception = None
        delay = initial_delay
        for attempt in range(max_retries + 1):
            try:
                response = func(*args, **kwargs)
                # 2xx 成功
                if response.status_code < 300:
                    return response
                # 429/5xx 重试
                if response.status_code in (429, 500, 502, 503, 504):
                    if attempt < max_retries:
                        time.sleep(delay)
                        delay *= backoff_factor
                        continue
                return response
            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.RequestException,
            ) as e:
                last_exception = e
                if attempt < max_retries:
                    time.sleep(delay)
                    delay *= backoff_factor
                else:
                    break
        raise last_exception or requests.exceptions.RequestException(
            f"请求失败，已重试 {max_retries} 次"
        )

    return wrapper


# ============== 请求封装（自动 raise_for_status） ==============


class ApiError(Exception):
    """API 请求错误"""

    def __init__(self, url: str, status_code: int, body: str):
        self.url = url
        self.status_code = status_code
        self.body = body
        super().__init__(f"API 错误 {status_code}: {url}")


def _request_with_raise(
    func: Callable, url: str, max_retries: int = 3, **kwargs
) -> requests.Response:
    """发起请求，自动调用 raise_for_status()，4xx/5xx 直接抛异常不重试

    Args:
        func: requests.get 或 requests.post
        url: 请求 URL
        max_retries: 最大重试次数（仅对网络错误和 5xx 生效）
        **kwargs: 透传给 requests

    Returns:
        Response 对象（已通过 raise_for_status 检查）

    Raises:
        ApiError: HTTP 4xx/5xx 响应
    """
    last_exception = None
    delay = 0.5
    for attempt in range(max_retries + 1):
        try:
            response = func(url, **kwargs)
            if response.status_code < 400:
                return response
            if attempt < max_retries and response.status_code >= 500:
                time.sleep(delay)
                delay *= 2
                continue
            response.raise_for_status()
            return response
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.RequestException,
        ) as e:
            last_exception = e
            if attempt < max_retries:
                time.sleep(delay)
                delay *= 2
            else:
                break
    raise last_exception or ApiError(url, 0, "请求失败")


def get(url: str, **kwargs) -> requests.Response:
    """GET 请求，自动 raise_for_status，网络错误自动重试"""
    return _request_with_raise(requests.get, url, **kwargs)


def post(url: str, **kwargs) -> requests.Response:
    """POST 请求，自动 raise_for_status，网络错误自动重试"""
    return _request_with_raise(requests.post, url, **kwargs)


# 重试版本的 requests（保留，向后兼容）
get_retry = lambda url, **kw: _request_with_raise(requests.get, url, **kw)
post_retry = lambda url, **kw: _request_with_raise(requests.post, url, **kw)


# ============== 大屏配置缓存 ==============

_CACHE_DIR = Path(__file__).parent / ".cache"
_SCREEN_CACHE_TTL = 300  # 5分钟 TTL


def _get_screen_cache_path(screen_id: int) -> Path:
    path = _CACHE_DIR / "screens"
    path.mkdir(parents=True, exist_ok=True)
    return path / f"{screen_id}.json"


def screen_cache_get(
    screen_id: int, max_age: int = _SCREEN_CACHE_TTL
) -> Optional[Dict]:
    """从本地缓存获取大屏配置（TTL 内有效）

    Args:
        screen_id: 大屏 ID
        max_age: 缓存最大有效期（秒），默认 5 分钟

    Returns:
        缓存数据 dict 或 None（缓存不存在或已过期）
    """
    cache_file = _get_screen_cache_path(screen_id)
    if not cache_file.exists():
        return None
    try:
        age = time.time() - cache_file.stat().st_mtime
        if age > max_age:
            return None
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def screen_cache_set(screen_id: int, data: Dict) -> None:
    """将大屏配置写入本地缓存"""
    cache_file = _get_screen_cache_path(screen_id)
    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    except OSError:
        pass  # 缓存写入失败不影响主流程
