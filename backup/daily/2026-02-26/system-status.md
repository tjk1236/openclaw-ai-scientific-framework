# 系统状态 - 2026-02-26

**备份时间**: Thu Feb 26 02:00:01 CST 2026

## 磁盘使用
Filesystem      Size  Used Avail Use% Mounted on
/dev/sdd       1007G  6.2G  950G   1% /

## 内存使用
               total        used        free      shared  buff/cache   available
Mem:            15Gi       1.4Gi        14Gi       3.6Mi       259Mi        14Gi
Swap:          4.0Gi          0B       4.0Gi

## 定时任务状态
0 * * * * cd /home/zzyuzhangxing/.openclaw/workspace && /usr/bin/node learn-skill.js >> /home/zzyuzhangxing/.openclaw/workspace/learn-cron.log 2>&1
0 * * * * /home/zzyuzhangxing/.openclaw/workspace/backup/scripts/hourly-backup.sh >> /home/zzyuzhangxing/.openclaw/workspace/backup/system/logs/hourly.log 2>&1
0 2 * * * /home/zzyuzhangxing/.openclaw/workspace/backup/scripts/daily-backup.sh >> /home/zzyuzhangxing/.openclaw/workspace/backup/system/logs/daily.log 2>&1
0 9 * * * cd /home/zzyuzhangxing/.openclaw/workspace && /usr/bin/python3 scripts/bilibili-account-fetch.py >> /home/zzyuzhangxing/.openclaw/workspace/backup/system/logs/bilibili-account.log 2>&1
30 9 * * * cd /home/zzyuzhangxing/.openclaw/workspace && /usr/bin/python3 scripts/generate-daily-report.py >> /home/zzyuzhangxing/.openclaw/workspace/backup/system/logs/daily-report.log 2>&1

## 最近技能学习
暂无数据
