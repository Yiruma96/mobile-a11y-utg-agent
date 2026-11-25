# Anatsa (TeaBot) 官方商店潜伏壳：地理围栏 + 多日延迟热更新后才暴露无障碍

- **案例编号**：`INTEL_GL_07` ｜ **地区与活跃期**：全球（美/英/德/西等官方商店）（2024–2025）
- **诱导隐蔽度分级**：`L3 · 跨页隐蔽协同与感知劫持型`
- **为何首次动态运行容易遗漏**：最典型的「首次运行完全不暴露」：审核期 100% 干净，延迟数日 + 地理围栏 + 多次重启后才下发恶意 Add-On

## 一、伪装形式与接触通道
- **伪装外衣**：官方 Google Play 上架的 PDF 阅读器、文件清理器、二维码扫描器（含本数据集 `TeaBot MB_121` 动态脱壳样张）
- **带外接触通道**：正规官方应用商店自然搜索下载（前期完全无恶意代码！）
- **应用内界面特征**：阶段一通过 SIM 国家码/IP 地理围栏与时间延迟规避自动化沙箱；数日后向目标国家用户下发二阶段 Add-On 才动态脱壳呈现高仿 Samsung One UI / Android 无障碍设置页

## 二、典型诱骗话术
- 「应用正常使用数天后弹出「下载核心功能附加组件（Add-On / Update）」」
- 「附加组件伪造系统无障碍设置界面（如本数据集动态实测捕获的 `QR-Code Scanner: Add-On`），引导在已下载服务中开启开关」

## 三、攻击步骤与技术链路
- 1. 干净工具壳通过应用商店审核，建立官方背书与高下载量
- 2. 检查 SIM/地区地理围栏并延迟数日/多次重启后，向目标地区推送恶意 Add-On 更新
- 3. 二阶段载荷动态脱壳后呈现高仿系统无障碍设置页诱导授权并执行银行盗刷

## 四、端侧可观测信号与鸿蒙防御映射
- 完美解释为何单次冷启动动态检测对延迟壳有天然盲区
- 一旦进入二阶段脱壳运行（如本数据集 `TeaBot MB_121` 动态实拍），UTG 立即暴露「高仿系统无障碍列表页 → 真实系统无障碍页」的双重设置页镜像特征
- **鸿蒙端侧防御要点**：应用热更新/子包安装后的首次无障碍请求重新纳入高危 UTG 实时检测，不能因阶段一历史清白而永久白名单

## 五、原文链接（公开报道 / 官方公告 / 安全实验室博客）
- [ThreatFabric 原文：Anatsa Targets North America Using Proven Mobile Campaign Process](https://www.threatfabric.com/blogs/anatsa-targets-north-america-uses-proven-mobile-campaign-process)
- [ThreatFabric 原文：Anatsa Trojan Returns Targeting Europe and Expanding Its Reach](https://www.threatfabric.com/blogs/anatsa-trojan-returns-targeting-europe-and-expanding-its-reach)
- [Cleafy Labs：TeaBot (Anatsa) Technical Analysis](https://www.cleafy.com/cleafy-labs/teabot)
