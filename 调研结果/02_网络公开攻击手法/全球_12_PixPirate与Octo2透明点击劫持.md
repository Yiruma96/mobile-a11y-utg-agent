# PixPirate & Octo2 & ClayRat & BTMOB：透明点击劫持（`TYPE_ACCESSIBILITY_OVERLAY`）与无图标 ATS

- **案例编号**：`INTEL_GL_12` ｜ **地区与活跃期**：拉美（巴西）、欧洲及全球（2024–2025）
- **诱导隐蔽度分级**：`L3 · 跨页隐蔽协同与感知劫持型`
- **为何首次动态运行容易遗漏**：安装后无桌面图标潜伏 + 收到特定推送/打开银行才触发 + `TYPE_ACCESSIBILITY_OVERLAY` 免悬浮窗授权透明遮罩

## 一、伪装形式与接触通道
- **伪装外衣**：伪装 Google Chrome、NordVPN、实用工具或二阶段无图标载荷（`PixPirate`、`Octo2`、`ClayRat`、`BTMOB`）
- **带外接触通道**：WhatsApp/短信钓鱼链接与恶意广告分发
- **应用内界面特征**：针对巴西 Pix 等即时支付系统与欧洲网银：部分变种采用双应用协同（Dropper 启动后卸载自身，留下无桌面图标的恶意主体潜伏）；拿到无障碍后直接用 `TYPE_ACCESSIBILITY_OVERLAY` 绕过 `SYSTEM_ALERT_WINDOW` 审计，实施透明点击劫持（Tapjacking）、黑屏自动转账与设置页防卸载秒退

## 二、典型诱骗话术
- 「表面展示加载转圈或安全校验按钮，底层通过透明层引导手指点击完成受限设置解锁与无障碍授权」
- 「授权后无需申请 `SYSTEM_ALERT_WINDOW`，直接利用 `TYPE_ACCESSIBILITY_OVERLAY` 绘制高透明/黑屏遮罩执行即时转账（ATS）并阻止卸载」

## 三、攻击步骤与技术链路
- 1. 伪装 NordVPN/Chrome 等安装并隐藏桌面图标进入后台潜伏
- 2. 通过透明引导层或分步覆盖诱导授予无障碍权限
- 3. 利用 `TYPE_ACCESSIBILITY_OVERLAY` 绕过常规悬浮窗申请，黑屏静默完成即时转账（ATS）并在用户进入设置页时自动点击返回防卸载

## 四、端侧可观测信号与鸿蒙防御映射
- 无桌面图标潜伏导致常规单次启动入口遍历易落空（需静态查 Receiver/无 Launcher 组件与动态通知触发）
- 监控无障碍启用后的 `TYPE_ACCESSIBILITY_OVERLAY` 窗口创建及设置页高频 `GLOBAL_ACTION_BACK/HOME` 调用
- **鸿蒙端侧防御要点**：无桌面图标侧载组件重点标记 + 严格限制 `AccessibilityExtensionAbility` 绘制全屏覆盖窗与回退系统设置页

## 五、原文链接（公开报道 / 官方公告 / 安全实验室博客）
- [ThreatFabric 原文：Octo2 — European Banks Already Under Attack by New Malware Variant](https://www.threatfabric.com/blogs/octo2-european-banks-already-under-attack-by-new-malware-variant)
- [腾讯云开发者社区：安卓无障碍远控木马与控屏机制剖析](https://cloud.tencent.com/developer/article/2651462)
- [腾讯云开发者社区：移动端屏幕共享与无障碍权限滥用分析](https://developer.cloud.tencent.com/article/2675698)
