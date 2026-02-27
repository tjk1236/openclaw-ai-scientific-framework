#!/bin/bash
# 本地备份系统 - 每小时执行
# 由 cron 定时调用: 0 * * * *

BACKUP_DIR="/home/zzyuzhangxing/.openclaw/workspace/backup"
WORKSPACE="/home/zzyuzhangxing/.openclaw/workspace"
DATE=$(date +%Y-%m-%d)
HOUR=$(date +%H:%M)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "[$(date)] 开始本地备份..."

# 1. 创建小时目录
mkdir -p "$BACKUP_DIR/hourly/$DATE"

# 2. 系统状态快照
echo "  → 保存系统状态..."
cat > "$BACKUP_DIR/hourly/$DATE/${TIMESTAMP}-system.json" << EOF
{
  "timestamp": "$(date -Iseconds)",
  "hour": "$HOUR",
  "hostname": "$(hostname)",
  "uptime": "$(uptime | awk '{print $3,$4}' | sed 's/,//')",
  "disk_usage": "$(df -h $WORKSPACE | tail -1 | awk '{print $5}')",
  "memory": "$(free -h | grep Mem | awk '{print $3"/"$2}')"
}
EOF

# 3. 备份学习日志
if [ -f "$WORKSPACE/skills-learning-log.json" ]; then
  echo "  → 备份学习日志..."
  cp "$WORKSPACE/skills-learning-log.json" "$BACKUP_DIR/hourly/$DATE/${TIMESTAMP}-skills.json"
fi

# 4. 同步到Git (如果配置了)
if [ -d "$WORKSPACE/.git" ]; then
  echo "  → Git备份..."
  cd "$WORKSPACE"
  git add -A 2>/dev/null
  git commit -m "Auto backup: $TIMESTAMP" 2>/dev/null || true
fi

echo "[$(date)] 备份完成: $BACKUP_DIR/hourly/$DATE/"
