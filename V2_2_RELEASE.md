# LOCAL-MEM0 v2.2 发布说明

**版本**: v2.2  
**日期**: 2026-03-14  
**代号**: Advanced (真实嵌入模型)

---

## 🎯 新增功能

### 1. 真实嵌入模型 (Real Embedding)

**使用 sentence-transformers 替代简化版哈希向量**

- **模型**: all-MiniLM-L6-v2 (384维)
- **优势**: 真实的语义理解，而非简单的词频统计
- **GPU 加速**: MPS (Metal Performance Shaders) 支持
- **缓存优化**: LRU 缓存避免重复编码

**性能对比**:

| 指标 | 简化版 | 真实模型 | 提升 |
|------|--------|---------|------|
| 语义理解 | ❌ 词频统计 | ✅ 深度学习 | 质的飞跃 |
| 编码速度 | 0.6ms | 30ms (单条) | 功能换速度 |
| 批处理 | 0.6ms | 1.65ms/条 (100条) | 可接受 |
| 缓存命中 | - | 0.01ms | 39259x |

**使用方式**:
```python
from real_embedding import RealEmbeddingModel

model = RealEmbeddingModel(use_gpu=True)
embedding = model.encode_single("这是一段测试文本")
```

### 2. 流式服务常驻

**LaunchAgent 配置**

- **服务名**: com.claw.memory.streaming
- **启动时机**: 开机自动启动
- **日志位置**: ~/.claw_memory_index/streaming.log

**管理命令**:
```bash
# 启动
launchctl load ~/Library/LaunchAgents/com.claw.memory.streaming.plist

# 停止
launchctl unload ~/Library/LaunchAgents/com.claw.memory.streaming.plist

# 查看状态
launchctl list | grep com.claw.memory.streaming
```

### 3. LOCAL-MEM0 Advanced

**整合所有高级功能**

```python
from local_mem0_advanced import LocalMem0Advanced

mem0 = LocalMem0Advanced(use_gpu=True, use_cache=True)

# 语义搜索（真实嵌入）
result = mem0.semantic_search("银行安全", top_k=10)
```

---

## 📁 新增文件

```
infinite_memory/
├── src/
│   ├── real_embedding.py         # 真实嵌入模型 ⭐
│   ├── streaming_indexer.py      # 流式索引 (已有)
│   ├── mps_accelerator.py        # GPU 加速 (已有)
│   ├── vector_index.py           # HNSW 索引 (已有)
│   └── local_mem0_advanced.py    # 高级整合 ⭐
├── scripts/
│   └── start_streaming.sh        # 流式服务启动
└── docs/
    └── V2_2_RELEASE.md           # 本文档

LaunchAgents/
└── com.claw.memory.streaming.plist  # 开机启动配置
```

---

## 🚀 快速开始

### 1. 验证安装

```bash
# 测试真实嵌入模型
python3 ~/.openclaw/workspace/infinite_memory/src/real_embedding.py benchmark

# 测试高级版
python3 ~/.openclaw/workspace/infinite_memory/src/local_mem0_advanced.py
```

### 2. 启动流式服务

```bash
# 方法1: LaunchAgent (推荐，开机自动)
launchctl load ~/Library/LaunchAgents/com.claw.memory.streaming.plist

# 方法2: 手动启动
~/.openclaw/workspace/infinite_memory/scripts/start_streaming.sh
```

### 3. 在代码中使用

```python
from real_embedding import RealEmbeddingModel

# 创建模型 (自动使用 GPU)
model = RealEmbeddingModel(use_gpu=True)

# 编码文本
embedding = model.encode_single("要编码的文本")

# 计算相似度
sim = model.similarity("文本1", "文本2")
print(f"相似度: {sim:.4f}")
```

---

## 📊 性能基准

### 真实嵌入模型 (MPS GPU)

```
Single Text Encoding:
  Length  21: 889ms (首次编译)
  Length  89:  91ms
  Length 171:  36ms

Batch Encoding:
  Batch  10: 30.27ms/text
  Batch  50:  3.99ms/text
  Batch 100:  1.65ms/text  ⭐

Cached Encoding:
  First call:  224.64ms
  Second call:   0.01ms
  Speedup: 39259x  🚀
```

### 系统整体性能

| 功能 | 延迟 | 说明 |
|------|------|------|
| 关键词搜索 | <1ms | FTS5 |
| 语义搜索 (缓存) | <1ms | HNSW + 缓存 |
| 语义搜索 (首次) | 30-100ms | 真实嵌入 |
| 文档索引 | 2秒 | 流式服务 |

---

## ⚠️ 注意事项

### 1. 首次加载较慢
- **模型下载**: 首次使用需下载 all-MiniLM-L6-v2 (~80MB)
- **MPS 编译**: 首次 GPU 运行有编译开销 (~800ms)
- **解决**: 后续调用会快很多，缓存命中率是关键

### 2. 内存占用
- **PyTorch + 模型**: ~500MB
- **HNSW 索引**: 100万向量 ~400MB
- **总计**: 建议 8GB+ 内存

### 3. GPU 使用条件
- **小批量 (< 50K)**: CPU 更快 (避免传输开销)
- **大批量 (> 50K)**: GPU 有优势
- **缓存命中**: 直接内存返回，不经过 GPU

---

## 🔄 升级指南 (v2.1 → v2.2)

### 1. 安装依赖

```bash
python3 -m pip install sentence-transformers --user --break-system-packages
```

### 2. 配置开机启动

```bash
launchctl load ~/Library/LaunchAgents/com.claw.memory.streaming.plist
```

### 3. 测试

```bash
python3 ~/.openclaw/workspace/infinite_memory/src/real_embedding.py benchmark
```

### 4. 重建向量索引 (可选)

如需使用真实嵌入重建所有索引：

```python
from local_mem0_advanced import LocalMem0Advanced

mem0 = LocalMem0Advanced()
mem0.index_all_documents()
```

---

## 🎯 使用建议

### 场景 1: 实时笔记
- **流式服务**: ✅ 启用
- **嵌入模型**: 使用缓存版本
- **预期延迟**: <2秒

### 场景 2: 批量导入
- **批处理大小**: 50-100 条
- **嵌入模型**: GPU 加速
- **预期速度**: 2-4秒/100条

### 场景 3: 语义搜索
- **缓存策略**: 常用查询缓存
- **HNSW 索引**: 预先构建
- **预期延迟**: <10ms (缓存) / <100ms (首次)

---

## 📈 后续规划

### v2.3 (计划)
- [ ] 量化模型 (int8) 减少内存
- [ ] 多模型支持 (切换不同嵌入模型)
- [ ] 分布式索引 (多台设备同步)

### v3.0 (远期)
- [ ] 本地 LLM 集成 (Llama.cpp)
- [ ] 多模态支持 (图片/音频嵌入)
- [ ] 自动标签与分类 (LLM-based)

---

## 🐛 故障排除

### 问题 1: 模型下载失败

**症状**: `ConnectionError` 或下载卡住

**解决**:
```bash
# 设置镜像
export HF_ENDPOINT=https://hf-mirror.com

# 手动下载
huggingface-cli download sentence-transformers/all-MiniLM-L6-v2
```

### 问题 2: MPS 不可用

**症状**: `MPS not available`

**解决**:
```python
# 强制使用 CPU
model = RealEmbeddingModel(use_gpu=False)
```

### 问题 3: 流式服务未启动

**症状**: 文件变化未触发索引

**解决**:
```bash
# 检查状态
launchctl list | grep com.claw.memory.streaming

# 查看日志
tail -f ~/.claw_memory_index/streaming.log

# 重启
launchctl unload ~/Library/LaunchAgents/com.claw.memory.streaming.plist
launchctl load ~/Library/LaunchAgents/com.claw.memory.streaming.plist
```

---

## 📞 支持

GitHub Issues: https://github.com/zwybirth/load-local-mem0/issues

---

**感谢使用 LOCAL-MEM0!** 🧠
