# AgroImageryTimeline
A query (SQL + Python) based analytics project to analyze agricultural imagery timeline for maize crop monitoring

[![GitHub license](https://img.shields.io/github/license/Ocholar/AgroImageryTimeline)](https://github.com/Ocholar/AgroImageryTimeline/blob/main/LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/Ocholar/AgroImageryTimeline)](https://github.com/Ocholar/AgroImageryTimeline/commits/main)
[![Open Issues](https://img.shields.io/github/issues/Ocholar/AgroImageryTimeline)](https://github.com/Ocholar/AgroImageryTimeline/issues)

## Overview
AgroImageryTimeline is a project designed to visualize agricultural imagery over time, leveraging data to track changes in crop health, growth stages, and environmental conditions. This repo aims to provide a timeline-based analysis tool for farmers, researchers, and agritech enthusiasts.

## Features
- **Time-Series Visualization**: Interactive timeline of imagery data.
- **Data Integration**: Supports prepared dataset for real-time updates.
- **Customizable**: Easily extendable for new imagery sources or analytics.

## 🌦️ Seasonal Brief: AgroImagery Timeline Insights

Analyzed **73,921 satellite images** tagged with four crop seasons using their capture dates.

### 📊 Seasonal Cycles & Imagery Distribution

| Season Label       | Months            | Description                        | Image Count |
|--------------------|-------------------|------------------------------------|-------------|
| Long Rains         | March–May         | Peak planting and early growth 🌱 | 0           |
| Cold/Dry Spell     | June–August       | Dormant or low vegetation ❄️       | 73,921      |
| Short Rains        | September–November| Secondary planting season 🌧️      | 0           |
| Hot/Dry Spell      | December–February | Drought or prep season 🔥          | 0           |

🧠 Note: All imagery currently falls within **Cold/Dry Spell (June–August)**, suggesting seasonal concentration or availability bias in captured data. Timeline can be expanded by integrating imagery from additional seasons or sources.

Each image is now tagged with a `season`, helping to analyze crop phases, plan field visits, and track seasonal patterns from space 🛰️✨
