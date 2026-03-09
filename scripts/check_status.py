#!/usr/bin/env python3
"""
LOCAL-MEM0 状态检查脚本
快速诊断系统状态
"""

import os
import sys
import subprocess
from pathlib import Path


class LocalMem0Checker:
    """状态检查器"""
    
    def __init__(self):
        self.results = {}
        self.errors = []
        
    def check_all(self):
        """运行所有检查"""
        print("=" * 60)
        print("   🔍 LOCAL-MEM0 状态检查")
        print("=" * 60)
        
        checks = [
            ("安装完整性", self.check_installation),
            ("文件系统", self.check_filesystem),
            ("数据库", self.check_database),
            ("LaunchAgent", self.check_launchd),
            ("CLI工具", self.check_cli),
            ("集成状态", self.check_integration),
        ]
        
        for name, check_func in checks:
            print(f"\n📋 {name}")
            try:
                result = check_func()
                self.results[name] = result
            except Exception as e:
                print(f"   ❌ 检查失败: {e}")
                self.results[name] = False
                self.errors.append(f"{name}: {e}")
        
        # 输出总结
        self.print_summary()
    
    def check_installation(self):
        """检查安装"""
        paths = {
            "项目目录": Path.home() / ".openclaw" / "workspace" / "infinite_memory",
            "记忆存储": Path.home() / "Documents" / "claw_memory",
            "索引目录": Path.home() / ".claw_memory_index",
        }
        
        all_ok = True
        for name, path in paths.items():
            exists = path.exists()
            status = "✅" if exists else "❌"
            print(f"   {status} {name}: {path}")
            if not exists:
                all_ok = False
        
        return all_ok
    
    def check_filesystem(self):
        """检查文件系统"""
        memory_dir = Path.home() / "Documents" / "claw_memory"
        
        if not memory_dir.exists():
            print(f"   ❌ 记忆目录不存在")
            return False
        
        # 统计文件
        categories = ["daily", "core", "bank", "archive", "cold", "summaries"]
        total_files = 0
        
        for cat in categories:
            cat_dir = memory_dir / cat
            if cat_dir.exists():
                count = len(list(cat_dir.glob("*.md")))
                if count > 0:
                    print(f"   ✅ {cat}/: {count} 篇文档")
                    total_files += count
        
        print(f"   📊 总计: {total_files} 篇文档")
        return total_files >= 0
    
    def check_database(self):
        """检查数据库"""
        db_path = Path.home() / ".claw_memory_index" / "main.db"
        
        if not db_path.exists():
            print(f"   ❌ 数据库不存在: {db_path}")
            return False
        
        print(f"   ✅ 数据库存在: {db_path}")
        
        # 尝试查询
        try:
            import sqlite3
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM documents WHERE is_deleted = 0")
            count = cursor.fetchone()[0]
            
            print(f"   📊 索引文档数: {count}")
            
            conn.close()
            return True
            
        except Exception as e:
            print(f"   ⚠️  数据库查询失败: {e}")
            return False
    
    def check_launchd(self):
        """检查 LaunchAgent"""
        services = [
            "com.claw.memory.monitor",
            "com.claw.memory.daily-review",
            "com.claw.memory.email-sender"
        ]
        
        result = subprocess.run(
            ["launchctl", "list"],
            capture_output=True,
            text=True
        )
        
        for service in services:
            if service in result.stdout:
                for line in result.stdout.split('\n'):
                    if service in line:
                        pid = line.split()[0]
                        if pid != "-":
                            print(f"   ✅ {service}: 运行中 (PID: {pid})")
                        else:
                            print(f"   ⏸️  {service}: 已加载")
                        break
            else:
                print(f"   ❌ {service}: 未加载")
        
        return True
    
    def check_cli(self):
        """检查 CLI"""
        cli_path = Path.home() / ".local" / "bin" / "claw"
        
        if not cli_path.exists():
            print(f"   ❌ CLI 不存在: {cli_path}")
            return False
        
        print(f"   ✅ CLI 存在: {cli_path}")
        
        # 尝试运行
        try:
            result = subprocess.run(
                [str(cli_path), "stats"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print(f"   ✅ CLI 可正常执行")
                return True
            else:
                print(f"   ⚠️  CLI 执行异常")
                return False
                
        except Exception as e:
            print(f"   ⚠️  CLI 测试失败: {e}")
            return False
    
    def check_integration(self):
        """检查集成"""
        try:
            sys.path.insert(0, str(
                Path.home() / ".openclaw" / "workspace" / "infinite_memory" / "src"
            ))
            from openclaw_adapter import get_memory_adapter
            
            adapter = get_memory_adapter()
            print(f"   ✅ 适配器可导入")
            
            # 测试搜索
            results = adapter.recall("test", limit=1)
            print(f"   ✅ 搜索功能正常")
            
            return True
            
        except Exception as e:
            print(f"   ❌ 集成检查失败: {e}")
            return False
    
    def print_summary(self):
        """输出总结"""
        print("\n" + "=" * 60)
        print("   📊 检查总结")
        print("=" * 60)
        
        passed = sum(1 for v in self.results.values() if v)
        total = len(self.results)
        
        print(f"\n通过: {passed}/{total}")
        
        if self.errors:
            print(f"\n❌ 发现 {len(self.errors)} 个错误:")
            for error in self.errors:
                print(f"   - {error}")
        else:
            print(f"\n✅ 系统状态良好")
        
        print("\n" + "=" * 60)


def main():
    """主函数"""
    checker = LocalMem0Checker()
    checker.check_all()


if __name__ == "__main__":
    main()
