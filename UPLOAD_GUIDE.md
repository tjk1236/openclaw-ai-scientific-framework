# 📤 框架上传指南

## ✅ 本地修改已完成

**已修改文件** (6 个):
- `README.md` - 科研版框架说明
- `config/skill-learning-schedule.json` - 科研学习计划
- `config/self-evolution.md` - 科研自我进化机制
- `docs/literature-review-guide.md` - 文献调研指南（新增）
- `docs/innovation-mining.md` - 创新点挖掘（新增）
- `docs/experiment-design.md` - 实验设计规范（新增）

**提交信息**:
```
feat: 科研版框架 - 面向自动驾驶感知研究

- 修改 README 为科研方向（路沿检测与场景理解）
- 添加 4 个科研 Agent 能力培养方案
- 修改 24 小时学习计划为科研时段
- 添加科研专用文档（文献调研/创新点挖掘/实验设计）
- 更新自我进化机制为科研导向
- 配置毕业里程碑管理
```

---

## 🔧 上传步骤

### 方法 1: 使用 GitHub Desktop（推荐）

1. **下载 GitHub Desktop**: https://desktop.github.com/
2. **克隆仓库**:
   - File → Clone Repository
   - 选择 `framework-backup` 文件夹
3. **切换到新仓库**:
   - Repository → Repository Settings
   - 修改 Remote URL: `https://github.com/tjk1236/openclaw-ai-scientific-framework.git`
4. **提交更改**:
   - 看到 6 个文件修改
   - 填写提交信息（已在上文提供）
   - Commit to main
5. **推送**:
   - Push origin

---

### 方法 2: 使用命令行 + Token

1. **创建 GitHub Token**:
   - 访问：https://github.com/settings/tokens
   - Generate new token (classic)
   - 勾选：`repo` (完全控制)
   - 生成后复制 token（只显示一次）

2. **配置 Git**:
   ```bash
   cd /home/tjk/.openclaw/workspace/framework-backup
   
   # 配置用户信息
   git config user.name "tjk1236"
   git config user.email "你的 GitHub 邮箱"
   
   # 修改 remote 到新仓库
   git remote set-url origin https://tjk1236:YOUR_TOKEN@github.com/tjk1236/openclaw-ai-scientific-framework.git
   
   # 推送
   git push -u origin main
   ```

---

### 方法 3: 手动创建仓库 + 上传

1. **在 GitHub 创建新仓库**:
   - 访问：https://github.com/new
   - 仓库名：`openclaw-ai-scientific-framework`
   - 公开/私有：自选
   - **不要** 勾选"Add README"

2. **复制上传命令**（GitHub 会提供）:
   ```bash
   git remote add origin https://github.com/tjk1236/openclaw-ai-scientific-framework.git
   git branch -M main
   git push -u origin main
   ```

3. **在 framework-backup 目录运行**:
   ```bash
   cd /home/tjk/.openclaw/workspace/framework-backup
   git remote set-url origin https://github.com/tjk1236/openclaw-ai-scientific-framework.git
   git push -u origin main
   ```

---

## ✅ 上传后检查

### 1. 访问仓库确认

打开：https://github.com/tjk1236/openclaw-ai-scientific-framework

**检查项**:
- [ ] README.md 显示科研版内容
- [ ] 文件数量正确（36+ 个）
- [ ] 最新提交是"feat: 科研版框架"

---

### 2. 检查要求满足情况

| 要求 | 检查项 | 状态 |
|:---|:---|:---|
| **自媒体→科研** | README 方向修改 | ✅ |
| **4 个 Agent** | 文献/创新/代码/写作 | ✅ |
| **保留机制** | 备份/记忆/进化等 | ✅ |
| **科研文档** | 文献/创新/实验指南 | ✅ |
| **毕业里程碑** | 时间节点配置 | ✅ |

---

## 📋 框架内容清单

### 核心文件

```
openclaw-ai-scientific-framework/
├── README.md                        # 科研版说明 ⭐
├── BOOTSTRAP.md                     # 启动指南
├── install.sh                       # 安装脚本
├── config/
│   ├── model-pools.json            # 模型池配置
│   ├── skill-learning-schedule.json # 科研学习计划 ⭐
│   ├── self-evolution.md           # 科研自我进化 ⭐
│   └── ...
├── docs/
│   ├── literature-review-guide.md  # 文献调研指南 ⭐
│   ├── innovation-mining.md        # 创新点挖掘 ⭐
│   ├── experiment-design.md        # 实验设计规范 ⭐
│   └── ...
└── scripts/
    ├── daily-evolution.py          # 每日进化报告
    └── ...
```

---

## 🎯 4 个科研 Agent 能力

### 📚 文献分析 Agent
- 系统性文献检索（2016-2026）
- APA 7th 格式引用管理
- 顶会/顶刊质量评估
- 方法对比与演进分析
- 研究空白识别

### 💡 创新点生成 Agent
- 技术空白分析
- 方法优缺点对比
- 交叉领域创新
- 场景创新识别
- 可行性评估

### 🧪 代码实现 Agent
- 算法复现（PyTorch/TensorFlow）
- 实验设计与对照
- 数据集准备与增强
- 训练调参与优化
- 性能评估与可视化

### 📝 论文写作 Agent
- 论文结构规划
- 章节撰写
- 图表制作与优化
- LaTeX 排版
- 审稿意见回复

---

## 📅 毕业里程碑配置

| 里程碑 | 目标日期 | 交付物 |
|:---|:---|:---|
| 文献综述 | 2026-03-31 | 40-50 篇核心文献 |
| 创新点确定 | 2026-04-15 | 技术方案 + 创新点 |
| 实验完成 | 2026-05-15 | 完整实验 + 对比 |
| 论文初稿 | 2026-05-31 | 完整论文稿 |
| 毕业答辩 | 2026-06-15 | 答辩 PPT+ 演示 |

---

## 🚀 下一步

上传成功后：

1. **配置本地 OpenClaw**:
   ```bash
   # 将框架配置应用到你的 workspace
   cp config/model-pools.json ~/.openclaw/workspace/config/
   cp config/skill-learning-schedule.json ~/.openclaw/workspace/config/
   ```

2. **开始科研任务**:
   - 文献调研：`/research curb detection 2016-2026`
   - 创新点分析：使用 `innovation-mining.md` 指南
   - 实验设计：参考 `experiment-design.md`

3. **每日进化**:
   - 22:00 自动生成进化报告
   - 检查毕业里程碑进度

---

## 📞 问题排查

### 问题 1: 推送失败

**错误**: `could not read Username`

**解决**: 使用方法 3（手动创建仓库）

---

### 问题 2: 权限不足

**错误**: `Permission denied (publickey)`

**解决**:
```bash
# 配置 SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"
# 复制 ~/.ssh/id_ed25519.pub 到 GitHub Settings → SSH and GPG keys
```

---

### 问题 3: 仓库已存在

**错误**: `repository already exists`

**解决**: 使用不同的仓库名，或删除现有仓库

---

**准备就绪！请选择一种方法上传。** 🚀
