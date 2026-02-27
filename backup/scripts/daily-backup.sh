#!/bin/bash
# 本地备份系统 - 每日执行
# 由 cron 定时调用: 0 2 * * *

BACKUP_DIR="/home/zzyuzhangxing/.openclaw/workspace/backup"
WORKSPACE="/home/zzyuzhangxing/.openclaw/workspace"
DATE=$(date +%Y-%m-%d)
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)

echo "[$(date)] 开始每日备份..."

# 1. 创建每日目录
mkdir -p "$BACKUP_DIR/daily/$DATE"

# 2. 备份系统配置
echo "  → 备份系统配置..."
mkdir -p "$BACKUP_DIR/system/config/$DATE"
cp ~/.openclaw/openclaw.json "$BACKUP_DIR/system/config/$DATE/" 2>/dev/null
crontab -l > "$BACKUP_DIR/system/config/$DATE/crontab.txt" 2>/dev/null

# 3. 汇总昨日聊天记录
echo "  → 汇总聊天记录..."
if [ -f "$WORKSPACE/memory/$YESTERDAY.md" ]; then
  cp "$WORKSPACE/memory/$YESTERDAY.md" "$BACKUP_DIR/chat/$YESTERDAY.md"
fi

# 4. 备份技能学习汇总
echo "  → 备份技能汇总..."
if [ -d "$BACKUP_DIR/skills" ]; then
  tar -czf "$BACKUP_DIR/daily/$DATE/skills-backup.tar.gz" -C "$BACKUP_DIR" skills/
fi

# 5. 生成每日摘要
echo "  → 生成每日摘要..."
cat > "$BACKUP_DIR/daily/$DATE/system-status.md" << EOF
# 系统状态 - $DATE

**备份时间**: $(date)

## 磁盘使用
$(df -h $WORKSPACE)

## 内存使用
$(free -h)

## 定时任务状态
$(crontab -l 2>/dev/null | grep -v "^#" | head -10)

## 最近技能学习
$(tail -5 "$WORKSPACE/skills-learning-log.json" 2>/dev/null | jq -r '.[] | "- \(.hour):00 \(.skillLearned.name // "N/A")"' 2>/dev/null || echo "暂无数据")
EOF

echo "[$(date)] 每日备份完成: $BACKUP_DIR/daily/$DATE/"
