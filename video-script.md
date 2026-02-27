# OpenClaw部署与培养完全指南
# 视频脚本与演示材料

---

## 📋 视频章节脚本

### 1. 开场成果展示 (1-2分钟)

**画面**: 黑屏 → 代码滚动 → 飞书消息弹窗

**台词**:
"这是我部署的AI助手，24小时自动运行。每小时自动学习新技能，每天早上自动汇报数据。"

**展示内容**:
- 定时任务列表: `openclaw cron list`
- 技能学习记录: `skills-learning-log.json`
- 飞书收到的日报消息
- Git自动备份日志

**数据亮点**:
- 已学习技能: 40+
- 运行天数: 3天
- 自动化任务: 5个

---

### 2. 部署方法 (3-5分钟)

#### 2.1 安装OpenClaw

**命令**:
```bash
# Linux/macOS
curl -fsSL https://openclaw.dev/install.sh | bash

# 验证安装
openclaw --version
```

**关键配置目录**:
```
~/.openclaw/
├── config/           # 配置文件
│   └── config.yaml   # 主配置
├── skills/           # 技能目录
├── workspace/        # 工作目录
└── logs/            # 日志
```

#### 2.2 初始化工作区

```bash
# 创建工作区
mkdir -p ~/my-assistant
cd ~/my-assistant

# 初始化OpenClaw
openclaw init

# 生成基础配置文件
```

**生成的文件**:
- `SOUL.md` - AI性格定义
- `USER.md` - 用户信息
- `HEARTBEAT.md` - 定时任务
- `MEMORY.md` - 长期记忆

---

### 3. API选择分析 (5-8分钟)

#### 3.1 白嫖方案对比

| 提供商 | 模型 | 免费额度 | 特点 |
|--------|------|----------|------|
| Google | Gemini 1.5 Pro | 1500请求/天 | 中文好，速度快 |
| Groq | Llama 3 70B | 200k tokens/天 | 极快，代码强 |
| Cerebras | Llama 3.1 70B | 150k tokens/天 | 最快，数学好 |
| Together | 多种开源 | 1000请求/月 | 模型多 |

**推荐组合**: Gemini(日常) + Groq(代码)

#### 3.2 付费方案对比

| 提供商 | 模型 | 价格 | 特点 |
|--------|------|------|------|
| Anthropic | Claude 3.5 Sonnet | $3/$15 per 1M | 最聪明，推理强 |
| OpenAI | GPT-4o | $5/$15 per 1M | 全能，生态好 |
| Moonshot | Kimi k2.5 | ¥12/1M | 中文最强 |
| DeepSeek | V3 | ¥2/1M | 性价比最高 |

**性价比之王**: Claude Sonnet + Kimi组合

#### 3.3 配置文件示例

```yaml
# ~/.openclaw/config/config.yaml
llm:
  default: claude-3-5-sonnet-20241022
  fallback: gemini-1.5-pro
  
  providers:
    anthropic:
      apiKey: ${ANTHROPIC_API_KEY}
      model: claude-3-5-sonnet-20241022
    
    google:
      apiKey: ${GOOGLE_API_KEY}
      model: gemini-1.5-pro
    
    groq:
      apiKey: ${GROQ_API_KEY}
      model: llama-3.1-70b-versatile
```

---

### 4. 飞书连接配置 (3分钟)

#### 4.1 创建飞书机器人

1. 打开 [飞书开发者平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 添加机器人能力
4. 获取 **App ID** 和 **App Secret**

#### 4.2 OpenClaw配置

```yaml
# config.yaml 添加channels配置
channels:
  feishu:
    appId: ${FEISHU_APP_ID}
    appSecret: ${FEISHU_APP_SECRET}
    encryptKey: ${FEISHU_ENCRYPT_KEY}
    verificationToken: ${FEISHU_VERIFICATION_TOKEN}
```

#### 4.3 测试消息发送

```bash
# 发送测试消息
openclaw message send \
  --channel feishu \
  --target "your-chat-id" \
  --message "Hello from OpenClaw! 🤖"
```

**效果展示**: 飞书收到机器人消息

---

### 5. 如何培养AI助手 (5分钟) ⭐核心内容

#### 5.1 SOUL.md - 定义性格

```markdown
# SOUL.md - AI性格定义

## 核心特质
- **身份**: 专业自媒体助手
- **性格**: 高效、严谨、主动
- **沟通风格**: 简洁直接，数据驱动

## 行为准则
1. 优先用行动回答，而非长篇解释
2. 定时汇报，不打扰
3. 主动发现问题并解决

## 记忆系统
- 每日更新 `memory/YYYY-MM-DD.md`
- 重要决策记录到 `MEMORY.md`
- 技能学习追踪到 `skills-learning-log.json`
```

#### 5.2 USER.md - 告诉AI你是谁

```markdown
# USER.md - 用户信息

## 基本信息
- **称呼**: 老鱼
- **身份**: AI自媒体博主
- **粉丝**: ~5万
- **方向**: ComfyUI、Seedence、泛AI

## 工作风格
- 系统化思维，注重记录
- 数据驱动决策
- 成本敏感，风控优先

## 当前项目
- B站数据爬取分析
- 每小时技能学习系统
- 自动化内容运营

## 沟通偏好
- 简洁结构化
- 公式>硬编码
- 任何配置更改需询问许可
```

#### 5.3 HEARTBEAT.md - 定时任务

```markdown
# HEARTBEAT.md

## 定时任务

### skill_learning
**时间**: 每小时整点
**操作**: 
```bash
python3 learn-skill-official.py
```
**说明**: 从官方库学习新技能

### daily_report
**时间**: 每天09:30
**操作**: 生成统一日报
**包含**: B站数据 + AI情报 + 技能学习

## 汇报规则
- 异常时立即通知
- 正常时静默执行
- 每天早上09:30统一汇报
```

#### 5.4 技能学习系统演示

**展示**:
1. 技能库文件: `openclaw-skills-library.md`
2. 学习脚本: `learn-skill-official.py`
3. 定时任务: `crontab -l`
4. 学习记录: `skills-learning-log.json`

**运行演示**:
```bash
# 手动运行一次
python3 learn-skill-official.py

# 查看结果
tail -20 skills-learning-log.json
```

---

### 6. 实战演示 (3分钟)

#### 6.1 现场添加定时任务

```bash
# 添加每小时任务
openclaw cron create \
  --name "hourly-skill" \
  --cron "0 * * * *" \
  --message "学习新技能"

# 查看任务列表
openclaw cron list
```

#### 6.2 等待执行并展示结果

**画面**: 等待1分钟，显示任务执行
**结果**: 飞书收到技能学习完成通知

---

## 📊 演示数据准备

### 截图清单

1. **openclaw cron list** 输出
2. **skills-learning-log.json** 内容
3. 飞书消息通知界面
4. **SOUL.md / USER.md** 内容
5. **HEARTBEAT.md** 配置
6. 定时任务运行日志

### 录屏准备

1. 初始化工作区过程
2. 添加定时任务过程
3. 手动运行技能学习脚本
4. 飞书收到通知

### 对比素材

| 任务 | 人工耗时 | AI耗时 |
|------|---------|--------|
| 每小时查看数据 | 10分钟/次 | 0秒 |
| 整理日报 | 30分钟/天 | 0秒 |
| 学习新工具 | 2小时/个 | 自动 |
| Git备份 | 5分钟/次 | 自动 |

---

## 🎯 结尾金句

"OpenClaw不是工具，而是你的数字员工。给它明确的指令，它会7×24小时为你工作。"

---

## 📎 资源链接

- 官方文档: https://docs.openclaw.ai
- 技能库: https://clawhub.com
- GitHub: https://github.com/openclaw/openclaw
- 本视频配套代码: [GitHub链接]

---

## 💡 进阶提示

### 如果想让AI更智能

1. **添加更多记忆文件**
   - `PROJECTS.md` - 追踪项目进度
   - `DECISIONS.md` - 记录重要决策
   - `TOOLS.md` - 工具使用偏好

2. **自定义技能**
   ```bash
   # 创建自定义技能
   mkdir -p ~/.openclaw/skills/my-custom-skill
   # 编写SKILL.md
   # 实现index.js
   ```

3. **多Agent协作**
   - 学习Agent: 每小时学习
   - 数据Agent: 负责分析
   - 内容Agent: 负责创作
   - 协调Agent: 分配任务

---

*脚本完成，祝录制顺利！🎬*
