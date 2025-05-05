# Rainbow 模拟投资


## 简介

Rainbow 模拟投资是一款基于命令行的金融模拟游戏，玩家可以体验股票、债券等金融产品的投资交易，学习投资策略和市场分析。游戏具有以下特点：

- 真实的市场波动模拟
- 丰富的金融产品（股票、债券等）
- 完整的存档系统
- 直观的数据可视化
- 季节系统影响市场

## 系统要求

- Python 3.8+
- 支持ANSI颜色的终端
- 推荐终端宽度≥100字符

## 安装指南

1. 克隆仓库：
   ```bash
   git clone https://github.com/CExnlh/Rainbow.git
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 运行游戏：
   ```bash
   python main.py
   ```

## 游戏玩法

### 基本操作

- **股票交易**
- **债券市场**
- **查看持仓**
- **进入下一天**
- **查看交易历史**
- **查看资产价格走势图**
- **自动筛选好投资**
- **存档管理**
- **保存并退出**


### 核心机制

- **季节系统**：春夏秋冬四季影响市场波动
- **价格保护**：防止资产价格暴跌
- **做空机制**：可以做空高估股票
- **历史记录**：完整记录所有交易和价格变化

## 存档系统

游戏支持多存档管理：
- 创建新存档
- 加载存档
- 删除存档
- 自动保存

存档位置：`./saves/` 目录

## 开发指南

### 项目结构

Rainbow/
├── main.py # 主程序
├── README.md # 说明文档
├── requirements.txt # 依赖
├── LICENSE # Apache 2.0 License
└── saves/ # 存档目录

### 扩展建议

1. 添加更多金融产品（基金、期货等）
2. 实现多人竞争模式
3. 添加新闻事件系统
4. 开发图形界面

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

Apache 2.0 License

Copyright (c) 2025 CExnlh

## 联系方式

作者：Robo Siya
邮箱：robosiya@cexnlh.dpdns.org
Session ID:05ebbe601eba90618689e9aba924eaa55025f5e32c5eb172086492cc56a51b432d
项目地址：https://github.com/CExnlh/Rainbow
