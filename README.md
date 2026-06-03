# 三股复盘分析平台

纯静态网站，用于展示三只A股（新凤鸣、华工科技、中兴通讯）的每日复盘数据和趋势分析。

## 技术栈

- 纯 HTML/CSS/JS，零构建工具，零后端
- Chart.js v4（CDN 加载）
- 响应式设计：桌面端双列布局，移动端单列 + 底部导航

## 项目结构

```
stock-dashboard/
├── index.html                  # 首页仪表盘
├── pages/
│   ├── xinfengming.html        # 新凤鸣(sh603225) 个股详情
│   ├── huagongkeji.html        # 华工科技(sz000988) 个股详情
│   └── zhongxing.html          # 中兴通讯(sz000063) 个股详情
├── css/
│   └── style.css               # 统一样式
├── js/
│   ├── charts.js               # Chart.js 图表封装
│   ├── data-loader.js          # 数据加载与图表更新
│   ├── stock-detail.js         # 个股页面逻辑
│   └── main.js                 # 首页逻辑
├── data/
│   ├── xinfengming/
│   │   └── index.json          # 新凤鸣复盘数据
│   ├── huagongkeji/
│   │   └── index.json          # 华工科技复盘数据
│   └── zhongxing/
│       └── index.json          # 中兴通讯复盘数据
├── .gitignore
└── README.md
```

## 使用方法

1. 直接打开 `index.html` 即可浏览首页仪表盘
2. 点击任意股票卡片跳转到个股详情页
3. 或使用任意静态文件服务器（如 `python -m http.server`）在项目根目录启动

## 数据更新

编辑对应股票目录下的 `data/<stock>/index.json` 文件，按格式添加新的 session 数据即可。复盘卡片截图放在 `data/<stock>/cards/` 目录下，命名格式为 `<date>-<session>.png`。

## 颜色体系

| 用途 | 颜色 | 色值 |
|------|------|------|
| 涨（红） | 红色 | `#d85a30` |
| 跌（绿） | 绿色 | `#1d9e75` |
| 支撑位 | 蓝色 | `#378add` |
| 压力位 | 橙色 | `#e8923f` |
