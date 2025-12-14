"""
缓存工具
提供简单的内存缓存机制
"""
import time
from typing import Any, Optional, Dict


class MemoryCache:
    """简单的内存缓存"""
    
    def __init__(self, default_ttl: int = 300):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        if key not in self.cache:
            return None
        
        item = self.cache[key]
        
        # 检查是否过期
        if item['expires_at'] < time.time():
            del self.cache[key]
            return None
        
        return item['value']
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """设置缓存值"""
        if ttl is None:
            ttl = self.default_ttl
        
        self.cache[key] = {
            'value': value,
            'expires_at': time.time() + ttl
        }
    
    def delete(self, key: str) -> bool:
        """删除缓存值"""
        if key in self.cache:
            del self.cache[key]
            return True
        return False
    
    def clear(self) -> None:
        """清空所有缓存"""
        self.cache.clear()
    
    def exists(self, key: str) -> bool:
        """检查缓存是否存在且未过期"""
        if key not in self.cache:
            return False
        
        if self.cache[key]['expires_at'] < time.time():
            del self.cache[key]
            return False
        
        return True
    
    def get_or_set(self, key: str, factory: callable, ttl: Optional[int] = None) -> Any:
        """获取缓存值，如果不存在则设置"""
        value = self.get(key)
        if value is None:
            value = factory()
            self.set(key, value, ttl)
        return value


# 全局缓存实例
cache = MemoryCache()
