# 升级指南

## v2.0 升级说明 (2026-03-14)

### 概述

LOCAL-MEM0 v2.0 带来了重大性能提升和新功能。本指南帮助用户从 v1.x 升级到 v2.0。

---

## 升级步骤

### 1. 备份现有数据

```bash
# 创建完整备份
tar czf ~/claw_memory_backup_v1_$(date +%Y%m%d).tar.gz \
  ~/Documents/claw_memory \
  ~/.claw_memory_index
```

### 2. 更新代码

```bash
# 进入技能目录
cd ~/.openclaw/workspace/skills/load-local-mem0

# 拉取最新代码
git pull origin main

# 或者手动更新
# 下载最新版本并替换
```

### 3. 重新加载 LOCAL-MEM0

```bash
# 运行恢复脚本
python3 ~/.openclaw/workspace/skills/load-local-mem0/scripts/restore.py
```

### 4. 应用 M5 Pro 优化

```bash
# 运行优化脚本
python3 ~/.openclaw/workspace/infinite_memory/scripts/optimize_m5.py
```

### 5. 安装加速依赖

```bash
# 安装 NumPy 和 FAISS
python3 -m pip install numpy faiss-cpu --user --break-system-packages

# 可选：安装 sentence-transformers
# python3 -m pip install sentence-transformers --user --break-system-packages
```

### 6. 重建索引

```bash
# 重建所有索引
claw reindex

# 或使用并行索引器（更快）
python3 ~/.openclaw/workspace/infinite_memory/src/parallel_indexer.py
```

### 7. 验证升级

```bash
# 检查统计
claw stats

# 测试搜索
claw search "测试"

# 检查性能
python3 -c "
import sys
sys.path.insert(0, '/Users/agents/.openclaw/workspace/infinite_memory/src')
from vector_index import HNSWVectorIndex
print('HNSW 索引模块正常')
"
```

---

## 新特性

### 1. HNSW 向量搜索

**v1.x**: 仅支持关键词搜索  
**v2.0**: 新增 HNSW 向量语义搜索

```python
# 使用向量搜索
python3 ~/.openclaw/workspace/infinite_memory/src/vector_index.py
```

**性能**: 100万向量 ~2ms 响应

### 2. M5 Pro 优化

**v1.x**: 默认 SQLite 配置  
**v2.0**: 针对 M5 + 32GB 优化

| 配置 | v1.x | v2.0 |
|------|------|------|
| SQLite Cache | 2MB | 512MB |
| MMap | 0 | 2GB |
| 并行索引 | 单线程 | 8 线程 |

### 3. 新分类体系

**v2.0 新增分类**:
- `daily/work` - 工作相关日常
- `daily/personal` - 个人日常
- `decisions` - 关键决策（永久保留）
- `learnings` - 经验总结（永久保留）
- `people` - 人员信息
- `projects` - 项目相关
- `ideas` - 想法/灵感

### 4. 增强搜索

**v2.0 新增**:
- 搜索别名（"银行项目" → "bank", "BANK-AI"）
- 时间线视图
- 相似文档查找

### 5. 自动化功能

**v2.0 新增**:
- 自动摘要生成
- 智能标签建议
- 每日自动报告（23:30）
- iCloud 同步脚本

---

## 破坏性变更

### 配置文件变更

v2.0 扩展了 `~/.claw_memory_index/config.json`：

```json
{
  // v1.x 已有
  "version": "1.0.0",
  "embedding_model": "all-MiniLM-L6-v2",
  
  // v2.0 新增
  "categories": { ... },
  "tag_aliases": { ... },
  "storage_layers": { ... },
  "auto_tiering": { ... }
}
```

### API 变更

`store.py` 接口保持不变，新增模块：
- `vector_index.py` - HNSW 向量索引
- `search_enhanced.py` - 增强搜索
- `auto_summary.py` - 自动摘要
- `parallel_indexer.py` - 并行索引

---

## 故障排除

### 问题 1: 恢复脚本失败

**症状**: `restore.py` 报错  
**解决**:
```bash
# 检查安装
ls ~/Documents/claw_memory
ls ~/.claw_memory_index/main.db

# 手动重新安装
cd ~/.openclaw/workspace/infinite_memory
python3 scripts/setup.py
```

### 问题 2: 模块导入失败

**症状**: `ImportError: No module named 'faiss'`  
**解决**:
```bash
python3 -m pip install faiss-cpu --user --break-system-packages
```

### 问题 3: 性能没有提升

**症状**: 索引速度没有变化  
**解决**:
```bash
# 检查优化是否应用
python3 -c "
import sqlite3
from pathlib import Path
conn = sqlite3.connect(str(Path.home() / '.claw_memory_index' / 'main.db'))
cursor = conn.cursor()
cursor.execute('PRAGMA cache_size')
print(f'Cache: {cursor.fetchone()[0]}')
conn.close()
"
# 应该显示 -524288 (512MB)
```

### 问题 4: 向量搜索报错

**症状**: `FAISS not available`  
**解决**:
```bash
# 检查 FAISS 安装
python3 -c "import faiss; print(faiss.__version__)"

# 重新安装
python3 -m pip uninstall faiss-cpu -y
python3 -m pip install faiss-cpu --user --break-system-packages
```

---

## 回滚方案

如果升级后需要回滚到 v1.x：

```bash
# 恢复备份
tar xzf ~/claw_memory_backup_v1_YYYYMMDD.tar.gz -C ~/

# 恢复 store.py
cp ~/.openclaw/workspace/infinite_memory/src/store.py.backup \
   ~/.openclaw/workspace/infinite_memory/src/store.py

# 重新加载
python3 ~/.openclaw/workspace/skills/load-local-mem0/scripts/restore.py
```

---

## 性能对比

| 指标 | v1.x | v2.0 | 提升 |
|------|------|------|------|
| 索引速度 | ~500 docs/sec | **2,833 docs/sec** | 5.6x |
| 关键词搜索 | ~2ms | **<1ms** | 2x |
| 向量搜索 (100万) | N/A | **~2ms** | 新功能 |
| 最大支持文档 | 100万 | **1000万+** | 10x |

---

## 后续计划

### v2.1 (计划)
- [ ] Metal GPU 加速
- [ ] 自动模型下载
- [ ] 多设备同步

### v3.0 (远期)
- [ ] 分布式存储
- [ ] 实时协作
- [ ] 高级 NLP 分析

---

## 反馈

遇到问题请提交 Issue：
https://github.com/zwybirth/load-local-mem0/issues

---

**升级日期**: 2026-03-14  
**版本**: v2.0  
**作者**: zwybirth
