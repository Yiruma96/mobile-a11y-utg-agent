# SecuriDropper & BugDrop：滥用 Session 安装 API 绕过 Android 13–15「受限设置」

- **案例编号**：`INTEL_GL_01` ｜ **地区与活跃期**：全球（欧洲/拉美为主）（2023–2025）
- **诱导隐蔽度分级**：`L2 · 高仿系统/品牌分步引导型`
- **为何首次动态运行容易遗漏**：多阶段 Dropper（阶段一完全不声明无障碍权限，安装二阶段载荷才暴露）

## 一、伪装形式与接触通道
- **伪装外衣**：Dropper-as-a-Service（伪装 Google Chrome / 实用工具 / 杀毒应用，投放 SpyNote、Ermac、Anatsa、Chameleon）
- **带外接触通道**：钓鱼网站、短信链接或第三方商店侧载
- **应用内界面特征**：阶段一壳程序本身**完全不声明 `BIND_ACCESSIBILITY_SERVICE`**，仅申请 `REQUEST_INSTALL_PACKAGES` 并通过 `PackageInstaller.Session` + Multi-Split APK 模仿官方应用商店安装流程；二阶段载荷被 OS 误判为商店安装从而绕过「受限设置」直接弹出无障碍请求

## 二、典型诱骗话术
- 「点击「Reinstall / Update」以完成组件安装（实则调用 Session-based PackageInstaller 安装二阶段木马）」
- 「为继续使用安全保护，请启用已安装服务中的无障碍开关」

## 三、攻击步骤与技术链路
- 1. 阶段一 Dropper 伪装轻量更新器/工具，静态与首启均不触发无障碍规则
- 2. 调用 `PackageInstaller.Session` 会话安装接口投放加密内嵌的二阶段木马 APK
- 3. 二阶段载荷绕过 Restricted Settings 灰显拦截，直接拉起无障碍设置并接管设备

## 四、端侧可观测信号与鸿蒙防御映射
- 单阶段静态扫描容易漏检阶段一 Dropper；端侧 UTG 需追踪「应用内拉起系统安装器（PackageInstaller）→ 新安装子应用首次启动即跳无障碍」的跨包因果链
- **鸿蒙端侧防御要点**：追踪跨应用安装来源链（Installer Provenance），杜绝非官方商店会话安装器获得免受限豁免

## 五、原文链接（公开报道 / 官方公告 / 安全实验室博客）
- [ThreatFabric 原文：Bypassing Android 13 Restrictions with SecuriDropper](https://www.threatfabric.com/blogs/bypassing-android-13-restrictions-with-securidropper)
- [BleepingComputer：Cybercrime Service Bypasses Android Security to Install Malware](https://www.bleepingcomputer.com/news/security/cybercrime-service-bypasses-android-security-to-install-malware/)
- [SecurityWeek：Dropper Service Bypassing Android Security Restrictions](https://www.securityweek.com/dropper-service-bypassing-android-security-restrictions-to-install-malware/)
- [The Hacker News：Cybercriminals Developing BugDrop](https://thehackernews.com/2022/08/cybercriminals-developing-bugdrop.html)
