# OpenClaw API 版本对照表

本文件记录不同版本 OpenClaw 的 API 差异，用于 LOCAL-MEM0 适配器参考。

## 版本兼容性

| OpenClaw 版本 | API 版本 | 记忆模块路径 | 集成方式 | 状态 |
|--------------|----------|--------------|----------|------|
| 1.x          | 1.0      | scripts.memory_store | 直接导入 | 支持 |
| 2.x          | 2.0      | openclaw.memory      | 插件系统 | 支持 |
| current      | current  | skills.custom_memory.scripts.memory_store | Bootstrap | 支持 |

## API 差异

### 保存记忆

**API 1.0:**
```python
from scripts.memory_store import save_memory
save_memory(content, category="general", tags=[], source="conversation")
```

**API 2.0:**
```python
from openclaw.memory import remember
remember(content, **kwargs)
```

**API current:**
```python
from skills.custom_memory.scripts.memory_store import save_memory
save_memory(content, category="general", tags=[], source="conversation")
```

### 搜索记忆

**API 1.0:**
```python
from scripts.memory_store import search_memory
results = search_memory(query, top_k=5)
```

**API 2.0:**
```python
from openclaw.memory import recall
results = recall(query, **kwargs)
```

**API current:**
```python
from skills.custom_memory.scripts.memory_store import search_memory
results = search_memory(query, top_k=5)
```

## 适配策略

### 通用适配器模式

LOCAL-MEM0 使用适配器模式统一不同版本的 API：

```python
class OpenClawMemoryAdapter:
    def remember(self, content, **kwargs):
        # 统一接口，内部适配到不同版本
        return save_document(content, **kwargs)
    
    def recall(self, query, **kwargs):
        # 统一接口，内部适配到不同版本
        return self.store.search_keywords(query, **kwargs)
```

### 版本检测方法

1. **检查命令版本**: `openclaw --version`
2. **检查配置文件**: `~/.openclaw/config.yaml`
3. **尝试导入模块**: 尝试导入不同路径的记忆模块
4. **默认回退**: 如果无法检测，使用 current 配置

## 升级注意事项

### OpenClaw 升级时

1. **数据安全**: LOCAL-MEM0 数据与 OpenClaw 版本无关
2. **集成配置**: 可能需要重新运行 setup
3. **环境变量**: 检查是否保留
4. **LaunchAgent**: 通常无需重新配置

### 升级后检查清单

- [ ] 运行 `claw stats` 确认系统正常
- [ ] 检查环境变量 `$CLAW_SENDER_PASSWORD`
- [ ] 测试保存一篇新文档
- [ ] 测试搜索功能
- [ ] 确认定时任务: `launchctl list | grep claw`

## 故障排除

### 导入错误

**问题**: `ImportError: No module named 'scripts.memory_store'`

**解决**: 运行 `python3 ~/.openclaw/workspace/skills/load-local-mem0/scripts/restore.py`

### API 不匹配

**问题**: 函数签名不匹配导致保存失败

**解决**: 更新适配器脚本 `api_adapter.py` 会自动检测并适配

### 配置丢失

**问题**: 升级后环境变量丢失

**解决**: 重新设置环境变量或添加到 `~/.zshenv`
