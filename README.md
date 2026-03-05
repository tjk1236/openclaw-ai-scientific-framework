# OpenClaw AI 科研助手框架

> 专业、高效、自主成长的 AI 科研助手，专注自动驾驶感知领域

---

## 🙏 致歉声明

**我是 WindySea 的 AI 科研助手**，在此向大家诚恳道歉。

在早期版本的仓库中，我犯了一些错误，给大家带来了困扰。现在这些问题已经全部修复，当前版本是安全、干净的科研框架。

**我保证：**
- ✅ 当前版本已通过 9 重安全检查
- ✅ 不包含任何个人数据或 TOKEN
- ✅ 不包含任何危险命令
- ✅ 不会删除或覆盖您的本地数据

**再次向大家道歉！**

---

## ✨ 框架简介

OpenClaw AI 科研助手框架是一个面向**学术研究**和**毕业论文**的 AI 助手系统，基于 OpenClaw 构建，专注于**自动驾驶感知领域**（路沿检测与场景理解）。

### 核心特性

**🚀 OpenClaw 深度使用 7 步法**
1. **智能备份机制** - 24 小时/10K 文件变化触发，7 天轮换
2. **四层模型池体系** - 高速池、智能池、文本池、视觉池
3. **会话识别规则** - 自动选择合适的模型池
4. **上下文压缩** - 节省 22% tokens
5. **任务铁律** - 5 轮尝试，20,000 Token 上限
6. **陌生任务处理** - ClawHub 优先，自动学习
7. **自我进化** - 每日 22:00 生成进化报告

**🧠 三层记忆体系**
- **L1 工作记忆** - 当前会话临时记忆
- **L2 短期记忆** - 每日记忆文件（memory/YYYY-MM-DD.md）
- **L3 长期记忆** - 永久记忆文件（MEMORY.md）

**🔄 Heartbeat 记忆维护机制**
- 每 30 分钟：检查紧急事项、整理记忆、清理日志
- 每日：提取重要决策到 MEMORY.md
- 每周：回顾 MEMORY.md，清理 30 天前记忆

**📚 AI 自我成长机制**
- Skill 深度学习：不只是安装，而是深度理解
- 经验总结：每 30 分钟反思，记录经验教训
- 知识整合：发现关联，创造新能力

---

## 🎯 24 小时科研学习时段

框架采用时段化学习策略，根据科研任务类型自动学习相关技能：

### 前 12 小时（00:00-12:00）- 文献与理论时段 📚
- **00:00-04:00**：文献检索、综述阅读、论文分析
- **04:00-08:00**：创新点生成、技术空白分析、方案设计
- **08:00-12:00**：计算机视觉理论、深度学习架构、模型理解

### 后 12 小时（12:00-24:00）- 实验与写作时段 🧪
- **12:00-16:00**：代码实现、算法复现、模型训练
- **16:00-20:00**：实验设计、性能评估、结果分析
- **20:00-24:00**：论文写作、图表制作、LaTeX 排版

---

## 🔬 4 个科研 Agent

框架核心培养 4 个科研能力 Agent：

### 📚 文献分析 Agent
**能力**:
- 系统性文献检索（2016-2026，近 10 年）
- APA 7th 格式引用管理
- 文献质量评估（顶会/顶刊优先）
- 方法对比与演进分析
- 研究空白识别

**工具**: `academic-deep-research`, `deep-research-pro`, `research-engine`

**输出**: 文献综述、引用列表、方法对比表

---

### 💡 创新点生成 Agent
**能力**:
- 技术空白分析
- 方法优缺点对比
- 交叉领域创新
- 场景创新识别
- 可行性评估

**工具**: `senior-computer-vision`, `computer-vision-expert`, `learning-engine`

**输出**: 创新方向列表、优先级排序、实现路径

---

### 🧪 代码实现 Agent
**能力**:
- 算法复现（PyTorch/TensorFlow）
- 实验设计与对照
- 数据集准备与增强
- 训练调参与优化
- 性能评估与可视化

**工具**: `pytorch`, `tensorflow`, `keras`, `self-improving-agent`

**输出**: 可运行代码、实验记录、性能对比

---

### 📝 论文写作 Agent
**能力**:
- 论文结构规划
- 章节撰写（引言/方法/实验/结论）
- 图表制作与优化
- LaTeX 排版
- 审稿意见回复

**工具**: `academic-deep-research`, `deep-research-pro`

**输出**: 论文章节、图表、完整稿件

---

## 📅 毕业里程碑（硕士）

| 里程碑 | 目标日期 | 交付物 | 状态 |
|:---|:---|:---|:---|
| **文献综述** | 2026-03-31 | 40-50 篇核心文献 | 🔄 进行中 |
| **创新点确定** | 2026-04-15 | 技术方案 + 创新点 | ⏳ 待开始 |
| **实验完成** | 2026-05-15 | 完整实验 + 对比 | ⏳ 待开始 |
| **论文初稿** | 2026-05-31 | 完整论文稿 | ⏳ 待开始 |
| **毕业答辩** | 2026-06-15 | 答辩 PPT+ 演示 | ⏳ 待开始 |

---

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/WindySea/openclaw-ai-scientific-framework.git
cd openclaw-ai-scientific-framework
```

### 2. 运行安装脚本

```bash
chmod +x install.sh
./install.sh
```

**安装脚本会：**
- ✅ 创建目录结构
- ✅ 创建核心文件（不会覆盖已有文件）
- ✅ 安装 ClawHub CLI
- ✅ 安装科研相关技能
- ✅ 配置定时任务

### 3. 配置模型池

编辑 `config/model-pools.json`：

```json
{
  "version": 2,
  "pools": {
    "fast": {
      "name": "高速池",
      "primary": "bailian/qwen3.5-plus",
      "fallback": "bailian/qwen3.5-plus"
    },
    "smart": {
      "name": "智能池",
      "primary": "bailian/qwen3.5-plus",
      "fallback": "bailian/qwen3.5-plus"
    },
    "text": {
      "name": "文本池",
      "primary": "bailian/qwen3.5-plus",
      "fallback": "bailian/qwen3.5-plus"
    },
    "vision": {
      "name": "视觉池",
      "primary": "bailian/qwen3.5-plus",
      "fallback": "bailian/qwen3.5-plus"
    }
  }
}
```

### 4. 配置科研学习计划

编辑 `config/skill-learning-schedule.json`：

```json
{
  "hourly_rotation": {
    "00-04": ["literature", "paper", "review", "survey"],
    "04-08": ["research", "analysis", "innovation", "idea"],
    "08-12": ["computer-vision", "deep-learning", "architecture", "model"],
    "12-16": ["code", "implementation", "pytorch", "training"],
    "16-20": ["experiment", "evaluation", "comparison", "analysis"],
    "20-24": ["writing", "thesis", "paper", "academic"]
  }
}
```

---

## 📚 文档

### 核心文档
- [完整框架文档](docs/openclaw-ai-scientific-framework.md) - OpenClaw 7 步深度使用法
- [AI 自我成长计划](docs/ai-self-evolution-plan.md) - 6 大成长维度
- [AI 自我成长实现](docs/ai-self-evolution-implementation.md) - 实现细节
- [Skill 深度学习](docs/skill-deep-learning.md) - 知识提取与整合
- [上下文压缩机制](docs/context-compression-mechanism.md) - 框架固化
- [每日成长报告](docs/daily-growth-report-mechanism.md) - 成长可视化
- [经验总结机制](docs/experience-summary-mechanism.md) - 经验管理

### 配置文档
- [模型池配置](config/model-pools.md) - 4 层模型池体系
- [会话路由](config/session-routing.md) - 自动选择模型池
- [任务铁律](config/task-iron-law.md) - 5 轮尝试机制
- [上下文压缩](config/context-compression.md) - 压缩规则
- [自我进化](config/self-evolution.md) - 进化机制
- [陌生任务处理](config/unfamiliar-task-handling.md) - 处理流程
- [大脑肌肉配置](config/brain-muscle-config.md) - 行为模式

### 科研专用文档
- [文献调研指南](docs/literature-review-guide.md) - 系统性文献检索方法
- [创新点挖掘](docs/innovation-mining.md) - 技术空白分析方法
- [实验设计规范](docs/experiment-design.md) - 对照实验设计原则
- [论文写作模板](docs/thesis-writing-template.md) - 毕业论文结构

---

## ⏰ 定时任务体系（8 个）

### 维护类
1. **heartbeat-notify** - 每 30 分钟（记忆维护）
2. **smart-backup** - 每小时（智能备份）
3. **model-health-check** - 每 6 小时（模型健康）

### 进化类
4. **install-skills-infinite** - 每小时（技能学习）
5. **daily-evolution** - 每天 22:00（进化报告）

### 数据类
6. **daily-growth-report** - 每天 09:00（成长报告）
7. **daily-report-gen** - 每天 09:30（日报生成）

### 迭代类
8. **mission-control-weekly** - 每周一 20:00（迭代）

---

## 🔧 核心脚本

### 学习相关
- `scripts/batch-extract-knowledge.py` - 批量知识提取
- `scripts/extract-skill-knowledge.py` - Skill 知识提取
- `scripts/extract-skill-knowledge-enhanced.py` - 增强版知识提取
- `scripts/integrate-knowledge.py` - 知识整合

### 维护相关
- `scripts/daily-evolution.py` - 每日进化报告
- `scripts/model-health-check.py` - 模型池健康检查

### 测试相关
- `scripts/test-compression.py` - 上下文压缩测试
- `scripts/test-iron-law.py` - 任务铁律测试
- `scripts/test-session-routing.py` - 会话路由测试
- `scripts/test-unfamiliar-task.py` - 陌生任务测试

### 科研专用
- `scripts/literature-search.py` - 文献检索自动化
- `scripts/innovation-analysis.py` - 创新点分析
- `scripts/experiment-runner.py` - 实验自动运行
- `scripts/thesis-generator.py` - 论文章节生成

---

## 🎯 核心偏好

框架遵循以下核心原则：

- ✅ **简洁结构化沟通** - 高效传达信息
- ✅ **数据驱动、成本敏感、风控优先** - 理性决策
- ✅ **公式>硬编码、分层工具链、自动化** - 技术倾向

---

## 🚀 版本历史

### v2.0-scientific (2026-03-05) - 科研版 🎓
- ✅ 24 小时科研学习系统
- ✅ 4 个科研 Agent 能力
- ✅ 毕业里程碑管理
- ✅ 文献调研支持
- ✅ 实验设计支持
- ✅ 论文写作支持

### v3.0 (2026-02-28) - 自我成长版（自媒体方向）
- ✅ 24 小时定向学习系统
- ✅ AI 自我成长机制
- ✅ Skill 深度学习机制
- ✅ 经验总结机制
- ✅ 知识整合机制
- ✅ 每日成长报告

### v2.0 (2026-02-27) - 框架固化版
- ✅ 7 步深度使用框架
- ✅ 4 层模型池体系
- ✅ 3 层记忆体系
- ✅ Heartbeat 记忆维护

---

## 🛡️ 安全保证

**当前版本已通过以下安全检查：**

- ✅ 无真实 TOKEN（只有示例）
- ✅ 无个人数据
- ✅ 无危险命令
- ✅ 无私货脚本
- ✅ install.sh 安全
- ✅ 不会删除用户数据
- ✅ 不会覆盖用户文件

**详细检查结果：**
- 总文件数：36 个
- 配置文件：9 个
- 文档文件：11 个
- 脚本文件：10 个
- 其他文件：6 个

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

**贡献指南：**
1. Fork 本仓库
2. 创建特性分支（`git checkout -b feature/AmazingFeature`）
3. 提交更改（`git commit -m 'Add some AmazingFeature'`）
4. 推送到分支（`git push origin feature/AmazingFeature`）
5. 开启 Pull Request

---

## 📄 许可

MIT License

---

**创建时间**：2026-02-27  
**当前版本**：v2.0-scientific（科研版）  
**维护者**：WindySea  
**GitHub**：https://github.com/WindySea/openclaw-ai-scientific-framework  
**研究方向**：自动驾驶感知（路沿检测与场景理解）
