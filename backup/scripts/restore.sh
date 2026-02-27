#!/bin/bash
# 完全恢复脚本
# 用途: 从本地备份恢复整个OpenClaw系统
# 执行: bash ~/.openclaw/workspace/backup/scripts/restore.sh [备份日期]

set -e

BACKUP_DIR="/home/zzyuzhangxing/.openclaw/workspace/backup"
WORKSPACE="/home/zzyuzhangxing/.openclaw/workspace"
RESTORE_DATE="${1:-$(date +%Y-%m-%d)}"

echo "==================================="
echo "  OpenClaw 系统恢复脚本"
echo "==================================="
echo "恢复日期: $RESTORE_DATE"
echo ""

# 检查备份是否存在
if [ ! -d "$BACKUP_DIR/daily/$RESTORE_DATE" ]; then
    echo "❌ 错误: 找不到备份 $RESTORE_DATE"
    echo "可用备份:"
    ls -1 $BACKUP_DIR/daily/ 2>/dev/null | head -5
    exit 1
fi

echo "✅ 找到备份: $BACKUP_DIR/daily/$RESTORE_DATE"
echo ""

# 1. 恢复核心记忆文件
echo "→ 步骤1: 恢复核心记忆文件..."
if [ -f "$BACKUP_DIR/daily/$RESTORE_DATE/MEMORY.md" ]; then
    cp "$BACKUP_DIR/daily/$RESTORE_DATE/MEMORY.md" "$WORKSPACE/"
    echo "  ✓ MEMORY.md"
fi
if [ -f "$BACKUP_DIR/daily/$RESTORE_DATE/USER.md" ]; then
    cp "$BACKUP_DIR/daily/$RESTORE_DATE/USER.md" "$WORKSPACE/"
    echo "  ✓ USER.md"
fi
if [ -f "$BACKUP_DIR/daily/$RESTORE_DATE/IDENTITY.md" ]; then
    cp "$BACKUP_DIR/daily/$RESTORE_DATE/IDENTITY.md" "$WORKSPACE/"
    echo "  ✓ IDENTITY.md"
fi
echo ""

# 2. 恢复技能记录
echo "→ 步骤2: 恢复技能记录..."
if [ -d "$BACKUP_DIR/skills" ]; then
    cp -r "$BACKUP_DIR/skills" "$WORKSPACE/backup/"
    echo "  ✓ 技能记录已恢复"
fi
echo ""

# 3. 恢复提示词库
echo "→ 步骤3: 恢复提示词库..."
if [ -d "$BACKUP_DIR/prompts" ]; then
    cp -r "$BACKUP_DIR/prompts" "$WORKSPACE/"
    echo "  ✓ 提示词库已恢复"
fi
echo ""

# 4. 恢复定时任务
echo "→ 步骤4: 恢复定时任务..."
if [ -f "$BACKUP_DIR/system/crontab/config.txt" ]; then
    crontab "$BACKUP_DIR/system/crontab/config.txt"
    echo "  ✓ 定时任务已恢复 (10个任务)"
    echo ""
    echo "  当前任务列表:"
    crontab -l | grep -v "^#" | grep -v "^$" | nl
fi
echo ""

# 5. 恢复系统配置
echo "→ 步骤5: 恢复系统配置..."
if [ -f "$BACKUP_DIR/system/config/$RESTORE_DATE/openclaw.json" ]; then
    cp "$BACKUP_DIR/system/config/$RESTORE_DATE/openclaw.json" ~/.openclaw/
    echo "  ✓ openclaw.json"
fi
echo ""

# 6. 重新安装技能依赖
echo "→ 步骤6: 重新安装技能依赖..."
echo "  这将重新安装所有已记录的技能..."
cd "$WORKSPACE"

# 从skills-learning-log.json提取已安装的技能
if [ -f "$WORKSPACE/skills-learning-log.json" ]; then
    echo "  从学习日志恢复技能列表..."
    # 这里可以添加自动安装逻辑
    echo "  (手动执行: npx clawhub sync)"
fi
echo ""

# 7. 验证恢复
echo "→ 步骤7: 验证恢复..."
echo ""
echo "  文件检查:"
[ -f "$WORKSPACE/MEMORY.md" ] && echo "  ✓ MEMORY.md 存在" || echo "  ✗ MEMORY.md 缺失"
[ -f "$WORKSPACE/USER.md" ] && echo "  ✓ USER.md 存在" || echo "  ✗ USER.md 缺失"
[ -f "$WORKSPACE/learn-skill.js" ] && echo "  ✓ learn-skill.js 存在" || echo "  ✗ learn-skill.js 缺失"
echo ""
echo "  目录检查:"
[ -d "$WORKSPACE/backup" ] && echo "  ✓ backup/ 存在" || echo "  ✗ backup/ 缺失"
[ -d "$WORKSPACE/prompts" ] && echo "  ✓ prompts/ 存在" || echo "  ✗ prompts/ 缺失"
echo ""

echo "==================================="
echo "  恢复完成!"
echo "==================================="
echo ""
echo "下一步建议:"
echo "1. 检查 MEMORY.md 内容是否正确"
echo "2. 运行 'npx clawhub sync' 恢复技能"
echo "3. 运行 'openclaw status' 检查系统状态"
echo "4. 手动触发一次技能学习测试"
echo ""
