"""
日志管理工具 - 数据分析助手

为每次查询创建独立的日志文件夹，保存：
- API 调用参数
- 生成的 DSL
- 查询结果数据
"""

import json
import time
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime


class QueryLogger:
    """查询日志记录器"""

    SESSION_MARKER = ".current_session"

    def __init__(self, log_base_dir: Optional[str] = None):
        """
        初始化日志记录器

        Args:
            log_base_dir: 日志基础目录，默认为项目根目录下的 logs 文件夹
        """
        if log_base_dir is None:
            self.log_base_dir = (
                Path(__file__).parent.parent.parent.parent.parent / "logs"
            )
        else:
            self.log_base_dir = Path(log_base_dir)

        self.session_dir: Optional[Path] = None
        self.session_id: Optional[str] = None

    def create_session(self, reuse_existing: bool = True) -> str:
        """
        创建新的查询会话，或复用现有会话

        Args:
            reuse_existing: 是否尝试复用现有会话

        Returns:
            会话 ID（时间戳）
        """
        if reuse_existing:
            existing_session = self._load_current_session()
            if existing_session:
                self.session_id = existing_session
                self.session_dir = self.log_base_dir / existing_session
                return self.session_id

        timestamp = int(time.time())
        date_str = datetime.fromtimestamp(timestamp).strftime("%Y%m%d_%H%M%S")

        self.session_id = f"{date_str}"
        self.session_dir = self.log_base_dir / self.session_id

        if not self.log_base_dir.exists():
            self.log_base_dir.mkdir(parents=True, exist_ok=True)

        self.session_dir.mkdir(parents=True, exist_ok=True)
        self._save_current_session_marker()

        session_info = {
            "session_id": self.session_id,
            "start_time": datetime.fromtimestamp(timestamp).isoformat(),
            "timestamp": timestamp,
        }

        self._save_json("session_info.json", session_info)
        return self.session_id

    def load_session(self, session_id: str) -> bool:
        """
        加载指定的会话

        Args:
            session_id: 会话 ID

        Returns:
            是否成功加载
        """
        session_dir = self.log_base_dir / session_id
        if not session_dir.exists():
            return False

        self.session_id = session_id
        self.session_dir = session_dir
        self._save_current_session_marker()
        return True

    def _save_current_session_marker(self):
        """保存当前会话标记"""
        if not self.session_id:
            return
        marker_file = self.log_base_dir / self.SESSION_MARKER
        with open(marker_file, "w", encoding="utf-8") as f:
            f.write(self.session_id)

    def _load_current_session(self) -> Optional[str]:
        """加载当前会话标记"""
        marker_file = self.log_base_dir / self.SESSION_MARKER
        if not marker_file.exists():
            return None

        try:
            with open(marker_file, "r", encoding="utf-8") as f:
                session_id = f.read().strip()
                session_dir = self.log_base_dir / session_id
                if session_dir.exists():
                    return session_id
        except Exception:
            pass

        return None

    def _get_timestamp_str(self) -> str:
        """获取当前时间戳字符串"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def _format_filename(self, step: str, description: str, suffix: str = "") -> str:
        """
        Format filename: step{step}-{description}{suffix}.json

        Args:
            step: Step number (e.g., "1", "2", "3a", "4-1")
            description: Step description (in English, concise)
            suffix: Optional suffix (e.g., "_raw", "_data")

        Returns:
            Formatted filename
        """
        if suffix:
            return f"step{step}-{description}{suffix}.json"
        return f"step{step}-{description}.json"

    def log_api_call(
        self,
        step: str,
        description: str,
        api_type: str,
        question: str,
        models: Optional[List[Dict[str, Any]]] = None,
        last_question: Optional[str] = None,
        last_result: Optional[Dict[str, Any]] = None,
        dsl: Optional[Dict[str, Any]] = None,
        additional_params: Optional[Dict[str, Any]] = None,
        call_index: int = 0,
    ):
        """
        Record API call parameters

        Args:
            step: Step number
            description: Step description
            api_type: API type
            question: Current question
            models: Model list
            last_question: Previous question
            last_result: Previous result
            dsl: DSL object
            additional_params: Additional parameters
            call_index: Call index to distinguish multiple calls
        """
        log_data: Dict[str, Any] = {
            "step": step,
            "description": description,
            "api_type": api_type,
            "question": question,
            "logged_at": datetime.now().isoformat(),
        }

        if models:
            log_data["models"] = models

        if last_question:
            log_data["last_question"] = last_question

        if last_result:
            log_data["last_result"] = last_result

        if dsl:
            log_data["dsl"] = dsl

        if additional_params:
            log_data.update(additional_params)

        step_suffix = f"-{call_index + 1}" if call_index > 0 else ""
        filename = self._format_filename(step, f"{description}-api-params", step_suffix)
        self._save_json(filename, log_data)

    def log_dsl(
        self,
        step: str,
        description: str,
        dsl: Dict[str, Any],
        question: str,
        call_index: int = 0,
    ):
        """
        Record generated DSL

        Args:
            step: Step number
            description: Step description
            dsl: DSL object
            question: Current question
            call_index: Call index to distinguish multiple calls
        """
        log_data = {
            "step": step,
            "description": description,
            "question": question,
            "dsl": dsl,
            "generated_at": datetime.now().isoformat(),
        }

        step_suffix = f"-{call_index + 1}" if call_index > 0 else ""
        filename = self._format_filename(step, f"{description}-dsl", step_suffix)
        self._save_json(filename, log_data)

    def log_query_result(
        self,
        step: str,
        description: str,
        result: Dict[str, Any],
        question: str,
        call_index: int = 0,
    ):
        """
        Record query result

        Args:
            step: Step number
            description: Step description
            result: Query result
            question: Current question
            call_index: Call index to distinguish multiple calls
        """
        log_data = {
            "step": step,
            "description": description,
            "question": question,
            "result": result,
            "received_at": datetime.now().isoformat(),
        }

        step_suffix = f"-{call_index + 1}" if call_index > 0 else ""
        filename = self._format_filename(step, f"{description}-result", step_suffix)
        self._save_json(filename, log_data)

    def log_api_response(
        self,
        step: str,
        description: str,
        api_type: str,
        response_data: Dict[str, Any],
        status: str = "success",
        error: Optional[str] = None,
        call_index: int = 0,
    ):
        """
        Record API response

        Args:
            step: Step number
            description: Step description
            api_type: API type
            response_data: Response data
            status: Status
            error: Error message
            call_index: Call index to distinguish multiple calls
        """
        log_data = {
            "step": step,
            "description": description,
            "api_type": api_type,
            "status": status,
            "response": response_data,
            "received_at": datetime.now().isoformat(),
        }

        if error:
            log_data["error"] = error

        step_suffix = f"-{call_index + 1}" if call_index > 0 else ""
        filename = self._format_filename(
            step, f"{description}-api-response", step_suffix
        )
        self._save_json(filename, log_data)

    def log_models_info(
        self, step: str, description: str, models: list, call_index: int = 0
    ):
        """
        Record data model information

        Args:
            step: Step number
            description: Step description
            models: Model list
            call_index: Call index to distinguish multiple calls
        """
        log_data = {
            "step": step,
            "description": description,
            "models": models,
            "count": len(models),
            "logged_at": datetime.now().isoformat(),
        }

        step_suffix = f"-{call_index + 1}" if call_index > 0 else ""
        filename = self._format_filename(step, f"{description}-models", step_suffix)
        self._save_json(filename, log_data)

    def log_dsl_only(self, step: str, description: str, dsl: dict, call_index: int = 0):
        """
        Record DSL only (simplified version, without extra wrapper)

        Args:
            step: Step number
            description: Step description
            dsl: DSL object
            call_index: Call index to distinguish multiple calls
        """
        step_suffix = f"-{call_index + 1}" if call_index > 0 else ""
        filename = self._format_filename(
            step, f"{description}-dsl", f"{step_suffix}_raw"
        )
        self._save_json(filename, dsl)

    def log_query_data_only(
        self, step: str, description: str, data: dict, call_index: int = 0
    ):
        """
        Record query data only (simplified version, without extra wrapper)

        Args:
            step: Step number
            description: Step description
            data: Query result data
            call_index: Call index to distinguish multiple calls
        """
        step_suffix = f"-{call_index + 1}" if call_index > 0 else ""
        filename = self._format_filename(
            step, f"{description}-data", f"{step_suffix}_raw"
        )
        self._save_json(filename, data)

    def _save_json(self, filename: str, data: Dict[str, Any]):
        """
        保存 JSON 文件

        Args:
            filename: 文件名
            data: 要保存的数据
        """
        if not self.session_dir:
            raise RuntimeError("未创建会话，请先调用 create_session()")

        filepath = self.session_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_session_dir(self) -> Optional[Path]:
        """
        获取当前会话目录

        Returns:
            会话目录路径
        """
        return self.session_dir

    def get_session_id(self) -> Optional[str]:
        """
        获取当前会话 ID

        Returns:
            会话 ID
        """
        return self.session_id


def create_logger(
    log_base_dir: Optional[str] = None, reuse_session: bool = True
) -> QueryLogger:
    """
    创建并初始化日志记录器

    Args:
        log_base_dir: 日志基础目录
        reuse_session: 是否复用现有会话

    Returns:
        QueryLogger 实例
    """
    logger = QueryLogger(log_base_dir)
    logger.create_session(reuse_existing=reuse_session)
    return logger
