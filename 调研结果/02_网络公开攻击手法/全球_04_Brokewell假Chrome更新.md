# Brokewell：假 Chrome 紧急更新页 + 定制 Dropper 绕受限设置 + 全事件远控

- **案例编号**：`INTEL_GL_04` ｜ **地区与活跃期**：欧洲及全球（2024–2025）
- **诱导隐蔽度分级**：`L2 · 高仿系统/品牌分步引导型`
- **为何首次动态运行容易遗漏**：定制 Dropper 绕受限设置 + 浏览器更新语义伪装

## 一、伪装形式与接触通道
- **伪装外衣**：伪装 Google Chrome 浏览器紧急更新页、奥地利数字身份认证 App（ID Austria）等
- **带外接触通道**：被劫持网站弹出高仿 Chrome 更新提示，诱骗下载 Dropper APK
- **应用内界面特征**：内置定制化 Dropper 绕过 Android 13+ 受限设置；取得无障碍后记录全部触控、文本输入、打开应用事件，并支持 WebView Cookie 窃取与实时录屏远控

## 二、典型诱骗话术
- 「您的 Google Chrome 版本过旧存在安全漏洞，请立即下载并安装最新更新」
- 「请按照屏幕提示完成受限设置解除与辅助服务启用以完成浏览器升级」

## 三、攻击步骤与技术链路
- 1. 网页伪造 Chrome 紧急更新下载定制 Dropper
- 2. Dropper 绕过 Android 13+ 受限设置并诱导授权无障碍
- 3. 利用无障碍捕获 WebView Cookie、注入假登录遮罩并开启实时 VNC 远控

## 四、端侧可观测信号与鸿蒙防御映射
- 声称浏览器/系统更新却请求无障碍权限（典型「功能-权限语义强背离」）
- 浏览器更新页 → 安装器 → 无障碍设置页的跨页跳转序列
- **鸿蒙端侧防御要点**：语义一致性检测（声称“更新/升级”却请求无障碍权限直接高危拦截）

## 五、原文链接（公开报道 / 官方公告 / 安全实验室博客）
- [ThreatFabric 官方技术报告：Brokewell — Do Not Go Broke from New Banking Malware](https://www.threatfabric.com/blogs/brokewell-do-not-go-broke-from-new-banking-malware)
