#!/usr/bin/env python3
"""
OpenClaw API 适配器
自动检测并适配不同版本的 OpenClaw API
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional


class OpenClawAPIAdapter:
    """OpenClaw API 适配器"""
    
    # 支持的 API 版本
    SUPPORTED_VERSIONS = ["1.0", "2.0", "current"]
    
    def __init__(self):
        self.local_mem0_dir = Path.home() / ".openclaw" / "workspace" / "infinite_memory"
        self.config_path = Path.home() / ".openclaw" / "config.yaml"
        self.api_version = None
        self.adapter_config = {}
    
    def detect_api_version(self) -> str:
        """检测 OpenClaw API 版本"""
        print("🔍 检测 OpenClaw API 版本...")
        
        # 尝试多种方式检测版本
        
        # 1. 检查 openclaw 命令
        try:
            import subprocess
            result = subprocess.run(
                ["openclaw", "--version"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                version_str = result.stdout.strip()
                print(f"   检测到 OpenClaw: {version_str}")
                
                # 解析版本号
                if "v" in version_str:
                    version = version_str.split("v")[-1].split(".")[0]
                    self.api_version = f"{version}.0"
                    return self.api_version
        except:
            pass
        
        # 2. 检查配置文件
        if self.config_path.exists():
            print(f"   发现配置文件: {self.config_path}")
            self.api_version = "current"
            return self.api_version
        
        # 3. 默认假设为当前版本
        print(f"   无法检测版本，假设为 current")
        self.api_version = "current"
        return self.api_version
    
    def get_adapter_for_version(self, version: str) -> Dict[str, Any]:
        """获取指定版本的适配器配置"""
        
        adapters = {
            "1.0": {
                "memory_hook": "custom-memory",
                "import_path": "scripts.memory_store",
                "save_function": "save_memory",
                "search_function": "search_memory",
                "integration_method": "import_override"
            },
            "2.0": {
                "memory_hook": "memory",
                "import_path": "openclaw.memory",
                "save_function": "remember",
                "search_function": "recall",
                "integration_method": "plugin"
            },
            "current": {
                "memory_hook": "custom-memory",
                "import_path": "skills.custom_memory.scripts.memory_store",
                "save_function": "save_memory",
                "search_function": "search_memory",
                "integration_method": "bootstrap"
            }
        }
        
        return adapters.get(version, adapters["current"])
    
    def generate_bootstrap_code(self, version: str) -> str:
        """生成启动代码"""
        adapter = self.get_adapter_for_version(version)
        
        code = f'''#!/usr/bin/env python3
"""
LOCAL-MEM0 Bootstrap for OpenClaw API {version}
自动生成的启动脚本
"""

import sys
from pathlib import Path

# 添加 LOCAL-MEM0 到路径
LOCAL_MEM0_DIR = Path.home() / ".openclaw" / "workspace" / "infinite_memory"
sys.path.insert(0, str(LOCAL_MEM0_DIR / "src"))

# 导入适配器
try:
    from openclaw_adapter import (
        get_memory_adapter,
        save_memory,
        search_memory,
        remember,
        recall
    )
    
    # 初始化适配器
    _adapter = get_memory_adapter()
    
    # 尝试覆盖原生记忆函数
    try:
        import {adapter['import_path']} as native_memory
        native_memory.{adapter['save_function']} = save_memory
        native_memory.{adapter['search_function']} = search_memory
        print("✅ LOCAL-MEM0 已成功集成")
    except ImportError:
        pass
        
except Exception as e:
    print(f"⚠️  LOCAL-MEM0 集成警告: {{e}}")


# 导出便捷函数
def get_context(query: str, max_results: int = 5) -> str:
    """获取相关上下文"""
    if '_adapter' in globals():
        return _adapter.get_context_for_query(query, max_results)
    return ""
'''
        return code
    
    def update_bootstrap_script(self):
        """更新启动脚本"""
        print("📝 更新启动脚本...")
        
        # 检测版本
        version = self.detect_api_version()
        
        # 生成代码
        code = self.generate_bootstrap_code(version)
        
        # 保存到 LOCAL-MEM0
        bootstrap_path = self.local_mem0_dir / "src" / "openclaw_bootstrap.py"
        
        with open(bootstrap_path, 'w') as f:
            f.write(code)
        
        print(f"   ✅ 启动脚本已更新: {bootstrap_path}")
        
        # 同时创建一个版本标记文件
        version_file = self.local_mem0_dir / ".api_version"
        with open(version_file, 'w') as f:
            f.write(version)
        
        return True
    
    def verify_adapter(self) -> bool:
        """验证适配器是否正常工作"""
        print("🔍 验证适配器...")
        
        try:
            sys.path.insert(0, str(self.local_mem0_dir / "src"))
            from openclaw_adapter import get_memory_adapter
            
            adapter = get_memory_adapter()
            
            # 测试基本功能
            print("   测试搜索功能...")
            results = adapter.recall("test", limit=1)
            
            print("   ✅ 适配器工作正常")
            return True
            
        except Exception as e:
            print(f"   ❌ 适配器验证失败: {e}")
            return False
    
    def adapt(self) -> bool:
        """执行适配"""
        print("🔄 开始 API 适配...")
        
        # 1. 检测版本
        version = self.detect_api_version()
        print(f"   目标 API 版本: {version}")
        
        # 2. 更新启动脚本
        self.update_bootstrap_script()
        
        # 3. 验证适配器
        if self.verify_adapter():
            print(f"\n✅ API 适配成功")
            print(f"   版本: {version}")
            return True
        else:
            print(f"\n⚠️  适配器验证失败，但脚本已更新")
            return False


def main():
    """主函数"""
    adapter = OpenClawAPIAdapter()
    success = adapter.adapt()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
