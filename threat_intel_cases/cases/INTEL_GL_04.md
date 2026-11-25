# INTEL_GL_04 · Brokewell：假 Chrome 紧急更新页 + 定制 Dropper 绕受限设置 + 全事件远控

- **来源类型**：`[Source C · 公开威胁情报 / 警方通报 / 安全实验室博客]`
- **地区与活跃期**：欧洲及全球（2024–2025）
- **隐蔽度分级**：`Level 2 · 高仿系统/品牌分步图文引导型`
- **为何首启/离线动态易遗漏**：定制 Dropper 绕受限设置 + 浏览器更新语义伪装
- **关联新扩充行为模式编号**：`EVADE_07`

## 1. 伪装外衣与带外接触通道
- **伪装形态**：伪装 Google Chrome 浏览器紧急更新页、奥地利数字身份认证 App（ID Austria）等
- **带外接触通道**：被劫持网站弹出高仿 Chrome 更新提示，诱骗下载 Dropper APK
- **应用内界面特征**：内置定制化 Dropper 绕过 Android 13+ 受限设置；取得无障碍后记录全部触控、文本输入、打开应用事件，并支持 WebView Cookie 窃取与实时录屏远控

## 2. 真实诱骗话术与剧本摘录
- 「您的 Google Chrome 版本过旧存在安全漏洞，请立即下载并安装最新更新」
- 「请按照屏幕提示完成受限设置解除与辅助服务启用以完成浏览器升级」

## 3. 完整攻击杀伤链
- 1. 网页伪造 Chrome 紧急更新下载定制 Dropper
- 2. Dropper 绕过 Android 13+ 受限设置并诱导授权无障碍
- 3. 利用无障碍捕获 WebView Cookie、注入假登录遮罩并开启实时 VNC 远控

## 4. 端侧 UTG 与跨信道可观测特征
- 声称浏览器/系统更新却请求无障碍权限（典型「功能-权限语义强背离」）
- 浏览器更新页 → 安装器 → 无障碍设置页的跨页跳转序列

## 5. 鸿蒙端侧防御与检测映射
- 语义一致性检测（声称“更新/升级”却请求无障碍权限直接高危拦截）

## 6. 权威公开来源
- ThreatFabric (April 2024): Brokewell Android Banking Malware & Dropper Analysis (threatfabric.com)
- The Hacker News / CyberInsider 2024 技术报道
