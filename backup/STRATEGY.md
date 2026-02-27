# 备份策略总览 - 完全本地版

**文档版本**: v1.0  
**创建时间**: 2026-02-24 20:00  
**存储位置**: `~/.openclaw/workspace/backup/STRATEGY.md`  
**更新方式**: 手动编辑 + 自动追加

---

## 一、备份目标

确保以下数据在任何情况下（包括飞书API不可用、网络中断）都能从本地恢复：

1. ✅ 聊天记录与决策
2. ✅ 技能学习进度
3. ✅ 系统配置与定时任务
4. ✅ 视频提示词库
5. ✅ 用户偏好与记忆

---

## 二、备份分层架构

### Layer 1: 实时层 (内存/运行中)
- 当前会话上下文
- 技能执行状态
- 临时计算结果

### Layer 2: 工作层 (本地文件)
- `MEMORY.md` - 长期记忆
- `USER.md` - 用户画像
- `IDENTITY.md` - 助手身份
- `skills-learning-plan.md` - 技能计划
- `backup/` - 备份系统
- `prompts/` - 提示词库

### Layer 3: 归档层 (本地备份)
- `backup/daily/` - 每日快照
- `backup/hourly/` - 每小时快照
- `backup/chat/` - 聊天记录归档
- `backup/system/` - 系统配置归档

### Layer 4: 镜像层 (飞书/可选)
- 飞书Wiki - 知识库镜像
- 飞书文档 - 日报镜像
- **性质**: 只读镜像，非必需

---

## 三、定时备份任务 (10个)

### 高频率 (每小时)
| 任务ID | 执行时间 | 内容 | 本地路径 | 飞书镜像 |
|--------|----------|------|----------|----------|
| skillsmp-learner | 0 * * * * | 学习新技能 | backup/hourly/YYYY-MM-DD/ | 可选 |
| auto-skill-installer | 0 * * * * | 安装技能依赖 | 工作区skills/目录 | 否 |
| local-hourly-backup | 0 * * * * | 系统状态快照 | backup/hourly/YYYY-MM-DD/ | 否 |

### 中频率 (每日多次)
| 任务ID | 执行时间 | 内容 | 本地路径 | 飞书镜像 |
|--------|----------|------|----------|----------|
| bilibili-tech-fetch | 10:00/22:00 | B站科技区数据 | workspace/data/bilibili/ | 可选 |
| bilibili-short-drama-fetch | 11:00/23:00 | B站短剧区数据 | workspace/data/bilibili/ | 可选 |
| short-drama-daily-report | 21:00 | 短剧日报生成 | backup/daily/YYYY-MM-DD/ | 可选 |

### 低频率 (每日一次)
| 任务ID | 执行时间 | 内容 | 本地路径 | 飞书镜像 |
|--------|----------|------|----------|----------|
| system-ops-daily-report-merged | 09:00 | 系统运维日报 | backup/daily/YYYY-MM-DD/ | 可选 |
| daily-chat-backup | 02:00 | 对话记录归档 | backup/chat/YYYY-MM-DD.md | 可选 |
| auto-git-backup | */30 * * * * | Git自动提交 | .git/ | 否 |
| local-daily-backup | 02:00 | 每日完整备份 | backup/daily/YYYY-MM-DD/ | 否 |

---

## 四、文件映射表

### 核心记忆文件
| 文件 | 本地路径 | 备份频率 | 飞书镜像 |
|------|----------|----------|----------|
| MEMORY.md | workspace/ | 实时 | 可选 |
| USER.md | workspace/ | 实时 | 可选 |
| IDENTITY.md | workspace/ | 实时 | 可选 |
| skills-learning-plan.md | workspace/ | 每小时 | 可选 |
| learn-skill.js | workspace/ | Git版本控制 | 否 |

### 技能文件
| 目录 | 本地路径 | 内容 |
|------|----------|------|
| 已安装技能 | `~/.openclaw/workspace/skills/` | SKILL.md + 脚本 |
| 技能记录 | `backup/skills/*/` | 分类详细记录 |
| 学习日志 | `skills-learning-log.json` | 时间线记录 |

### 提示词库
| 类型 | 本地路径 | 文件数 |
|------|----------|--------|
| 视频提示词 | `prompts/video/` | 15个 |
| 清单 | `prompts/video/manifest.json` | 1个 |

---

## 五、恢复流程

### 场景1: 飞书API不可用
**影响**: 无法同步到飞书  
**本地状态**: ✅ 完全可用  
**操作**: 继续正常运行，等待API恢复后补同步

### 场景2: 工作区文件损坏
**恢复步骤**:
1. 从 `backup/daily/` 恢复最新快照
2. 从Git历史恢复修改过的文件
3. 重新安装技能依赖 (clawhub install)

### 场景3: 完全重建
**恢复步骤**:
1. 克隆Git仓库恢复代码
2. 复制 `backup/` 目录恢复数据
3. 执行 `clawhub sync` 恢复技能
4. 恢复crontab定时任务

---

## 六、依赖清单

### 必需依赖 (本地)
- Node.js + npm
- Git
- Cron
- Bash
- Python 3 (技能用)

### 可选依赖 (云端)
- 飞书API (只用于镜像)
- B站API (用于数据爬取)
- SkillsMP.com (用于技能学习)

**设计原则**: 核心功能不依赖任何外部API

---

## 七、监控与告警

### 本地监控
```bash
# 检查备份完整性
check_backup.sh

# 检查技能状态
check_skills.sh

# 检查定时任务
crontab -l
```

### 告警阈值
- 磁盘使用 > 80%
- 备份文件缺失 > 3个
- 技能安装失败连续 > 3次

---

## 八、更新日志

| 时间 | 版本 | 变更 |
|------|------|------|
| 2026-02-24 | v1.0 | 初始版本，完全本地化 |

---

**注意**: 本文档是自给自足的，不依赖任何外部链接或服务。
_最后更新: 2026-02-24_
