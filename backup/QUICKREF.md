# 快速参考表 - Quick Reference

**本文档包含所有关键信息，可独立使用**

---

## 核心文件位置

| 文件 | 路径 | 用途 |
|------|------|------|
| 长期记忆 | `workspace/MEMORY.md` | 老鱼画像、决策记录 |
| 用户档案 | `workspace/USER.md` | 工作风格、技术栈 |
| 助手身份 | `workspace/IDENTITY.md` | 我的使命、任务 |
| 技能计划 | `workspace/skills-learning-plan.md` | 学习进度、已掌握技能 |
| 学习脚本 | `workspace/learn-skill.js` | 自动学习核心脚本 |
| 备份策略 | `workspace/backup/STRATEGY.md` | 完整备份规则 |
| 定时任务 | `workspace/backup/system/crontab/config.txt` | crontab配置 |
| 恢复脚本 | `workspace/backup/scripts/restore.sh` | 系统恢复工具 |

---

## 定时任务速查 (10个)

| 时间 | 任务 | 本地路径 |
|------|------|----------|
| 每小时:00 | 学习新技能 | `learn-skill.js` |
| 每小时:00 | 安装技能依赖 | `clawhub sync` |
| 每小时:00 | 本地备份 | `backup/scripts/hourly-backup.sh` |
| 10:00/22:00 | B站科技区爬取 | `scripts/bilibili-tech-fetch.py` |
| 11:00/23:00 | B站短剧区爬取 | `scripts/bilibili-short-drama-fetch.py` |
| 21:00 | 短剧日报 | `scripts/short-drama-daily-report.py` |
| 09:00 | 系统运维日报 | `scripts/system-ops-daily-report.sh` |
| 02:00 | 本地每日备份 | `backup/scripts/daily-backup.sh` |
| 02:00 | 对话归档 | `scripts/daily-chat-backup.sh` |
| */30分钟 | Git自动备份 | `git commit + push` |

---

## 关键技能清单 (12个已安装)

### 飞书生态 (5个)
- feishu-doc - 文档操作
- feishu-drive - 云存储
- feishu-perm - 权限管理
- feishu-wiki - 知识库
- feishu-task - 任务管理

### 内容创作 (3个)
- writer - AI写作陷阱修复
- summarize - 内容摘要
- tweet-writer - 推文撰写

### 数据分析 (2个)
- github - GitHub操作
- gh-issues - Issues管理

### 多媒体 (2个)
- image - 图片分析
- googlephotos-automation - 相册管理

---

## 用户关键信息

**老鱼**
- 身份: AI自媒体博主，粉丝近5万
- 方向: ComfyUI、Seedence、泛AI内容
- 风格: 系统化思维、数据驱动、成本敏感、风控优先
- 技术栈: Python、飞书、OpenClaw、ComfyUI

**我的任务**
- 每小时学习1个新技能 (24个/天)
- 12个视频/图片类 + 12个其他类别
- 成为最忠心、最得力的助手

---

## 常用命令

```bash
# 查看定时任务
crontab -l

# 手动执行学习脚本
cd ~/.openclaw/workspace && node learn-skill.js

# 恢复系统
bash ~/.openclaw/workspace/backup/scripts/restore.sh 2026-02-24

# 查看系统状态
openclaw status

# 同步技能
npx clawhub sync

# 查看技能列表
openclaw skills list
```

---

## 故障排除

### 场景: 飞书API不可用
**症状**: 无法同步到飞书  
**解决**: 无需处理，本地完全可用，等待API恢复后自动同步

### 场景: 技能学习失败
**症状**: 每小时学习脚本报错  
**解决**: 检查 `learn-skill.js`、检查网络、查看日志

### 场景: 定时任务未执行
**症状**: 到点没有新学习记录  
**解决**: `crontab -l` 检查任务是否存在、检查cron服务状态

### 场景: 需要完全重建
**解决**: 执行 `restore.sh` 脚本恢复所有配置

---

## 备份验证

```bash
# 检查备份完整性
ls ~/.openclaw/workspace/backup/daily/

# 检查技能记录
ls ~/.openclaw/workspace/backup/skills/

# 检查提示词库
ls ~/.openclaw/workspace/prompts/video/
```

---

**本文档是自给自足的，不依赖任何外部链接。**
_版本: v1.0 | 2026-02-24_
