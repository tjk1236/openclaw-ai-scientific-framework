#!/bin/bash
# OpenClaw视频演示脚本
# 按顺序执行，每步有停顿

echo "========================================"
echo "🎬 OpenClaw演示脚本"
echo "========================================"
echo ""

# 1. 展示版本
echo "📌 Step 1: 检查OpenClaw版本"
openclaw --version
echo ""
sleep 2

# 2. 展示工作区
echo "📌 Step 2: 工作区结构"
ls -la ~/.openclaw/workspace/
echo ""
sleep 2

# 3. 展示核心配置文件
echo "📌 Step 3: 核心配置文件"
echo "--- SOUL.md (AI性格) ---"
head -20 ~/.openclaw/workspace/SOUL.md
echo ""
sleep 3

# 4. 展示定时任务
echo "📌 Step 4: 定时任务列表"
openclaw cron list
echo ""
sleep 3

# 5. 展示技能学习记录
echo "📌 Step 5: 技能学习记录"
echo "今日已学技能:"
cat ~/.openclaw/workspace/skills-learning-log.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
today = '2026-02-26'
for d in data[-5:]:
    if today in d['timestamp']:
        skill = d.get('skillLearned', {})
        print(f\"  {d['hour']:02d}:00 - {skill.get('name', 'N/A')}\")
"
echo ""
sleep 3

# 6. 手动运行一次技能学习
echo "📌 Step 6: 手动运行技能学习"
echo "正在学习新技能..."
python3 ~/.openclaw/workspace/learn-skill-official.py
echo ""
sleep 3

# 7. 展示结果
echo "📌 Step 7: 查看最新学习记录"
tail -30 ~/.openclaw/workspace/skills-learning-log.json | head -20
echo ""

echo "========================================"
echo "✅ 演示完成！"
echo "========================================"
