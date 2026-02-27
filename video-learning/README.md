# 🎬 Video Learning System

> 视频管家学习进化系统  
> 目标: 从错误中学习，从优秀中提取模式，持续优化分镜质量

---

## 📁 目录结构

```
video-learning/
├── README.md           # 本文件
├── errors/            # 错误案例库 (评分<70)
│   ├── template.json  # 错误案例模板
│   └── YYYY-MM/       # 按月归档
├── patterns/          # 优秀模式库 (评分≥90)
│   └── YYYY-MM/       # 按月归档
├── rules/             # 审查规则版本
│   ├── v1.0-rules.md  # 初始规则
│   └── v1.1-rules.md  # 迭代规则
└── insights/          # 洞察分析报告
    └── weekly-YYYY-MM-DD.md
```

---

## 🔄 学习流程

### 实时流程 (自动执行)

```
生成分镜
    ↓
强制审查评分
    ├─ ≥90分 → 存入 patterns/
    ├─ 70-89分 → 常规输出
    └─ <70分 → 存入 errors/
```

### 每周流程 (周日20:00执行)

```
1. 统计本周数据
   - 生成总数
   - 平均评分
   - 错误类型分布

2. 分析 errors/ 目录
   - 识别高频错误模式
   - 提取新的审查规则

3. 分析 patterns/ 目录
   - 提取优秀模式
   - 总结成功因素

4. 更新审查规则
   - 发布新版本规则
   - 更新评分权重

5. 输出洞察报告
   - 写入 insights/weekly-YYYYMMDD.md
```

---

## 📊 关键指标

| 指标 | 目标 | 当前 |
|------|------|------|
| 平均审查评分 | >85 | - |
| 优秀率 (≥90) | >30% | - |
| 不及格率 (<70) | <10% | - |
| 规则迭代频率 | 每周 | - |

---

## 🎯 学习优先级

### P0 (立即学习)
- prompt-engineering (提示词工程)
- storytelling (叙事结构)

### P1 (本周学习)
- film-making (电影镜头语言)
- video-editing (剪辑连贯性)
- continuity-checking (逻辑连贯性审查)

### P2 (本月学习)
- screenplay (剧本结构)
- directing (导演视角)

---

*系统版本: v1.0*  
*创建时间: 2026-02-25*  
*负责人: 视频管家 (Video Manager)*
