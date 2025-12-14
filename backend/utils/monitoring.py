"""
监控和日志工具
提供系统监控、性能追踪和日志记录功能
"""
import time
import logging
import functools
from typing import Dict, Any, Optional
from datetime import datetime


class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        self.metrics: Dict[str, Any] = {}
        self.logger = logging.getLogger('parking_performance')
    
    def record_metric(self, name: str, value: float, tags: Optional[Dict] = None):
        """记录性能指标"""
        metric = {
            'timestamp': datetime.now().isoformat(),
            'value': value,
            'tags': tags or {}
        }
        
        if name not in self.metrics:
            self.metrics[name] = []
        
        self.metrics[name].append(metric)
        
        # 记录到日志
        self.logger.info(f"Metric {name}: {value} {tags}")
    
    def time_function(self, func):
        """函数执行时间装饰器"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                self.record_metric(f"{func.__name__}_duration", duration)
                return result
            except Exception as e:
                duration = time.time() - start_time
                self.record_metric(f"{func.__name__}_error_duration", duration)
                raise
        return wrapper
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """获取指标摘要"""
        summary = {}
        for name, values in self.metrics.items():
            if values:
                values_list = [v['value'] for v in values]
                summary[name] = {
                    'count': len(values_list),
                    'min': min(values_list),
                    'max': max(values_list),
                    'avg': sum(values_list) / len(values_list),
                    'latest': values_list[-1] if values_list else None
                }
        return summary


class RequestLogger:
    """请求日志记录器"""
    
    def __init__(self):
        self.logger = logging.getLogger('parking_requests')
    
    def log_request(self, method: str, url: str, status_code: int, duration: float, user_id: Optional[int] = None):
        """记录请求日志"""
        log_data = {
            'method': method,
            'url': url,
            'status_code': status_code,
            'duration': f"{duration:.3f}s",
            'user_id': user_id,
            'timestamp': datetime.now().isoformat()
        }
        
        if status_code >= 400:
            self.logger.warning(f"HTTP {status_code}: {method} {url} - {duration:.3f}s")
        else:
            self.logger.info(f"HTTP {status_code}: {method} {url} - {duration:.3f}s")


# 全局监控实例
performance_monitor = PerformanceMonitor()
request_logger = RequestLogger()


def monitor_performance(func):
    """性能监控装饰器"""
    return performance_monitor.time_function(func)


def setup_logging():
    """设置日志配置"""
    # 创建日志目录
    import os
    os.makedirs('logs', exist_ok=True)
    
    # 配置日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 文件处理器
    file_handler = logging.FileHandler('logs/parking_system.log')
    file_handler.setFormatter(formatter)
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # 配置根日志器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # 配置性能监控日志器
    perf_logger = logging.getLogger('parking_performance')
    perf_logger.setLevel(logging.INFO)
    
    # 配置请求日志器
    req_logger = logging.getLogger('parking_requests')
    req_logger.setLevel(logging.INFO)
