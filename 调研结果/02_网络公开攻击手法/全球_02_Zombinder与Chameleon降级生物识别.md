# Zombinder + Chameleon：捆绑合法应用绕过审计 + 无障碍强制降级生物识别锁

- **案例编号**：`INTEL_GL_02` ｜ **地区与活跃期**：欧洲（英国/意大利/波兰等）（2023–2024）
- **诱导隐蔽度分级**：`L3 · 跨页隐蔽协同与感知劫持型`
- **为何首次动态运行容易遗漏**：Zombinder 捆绑正常功能外壳 + 延迟按条件触发无障碍与锁屏劫持

## 一、伪装形式与接触通道
- **伪装外衣**：伪装 Google Chrome、政府服务或流行工具（含本数据集 `Chameleon` 登录门控样本）
- **带外接触通道**：钓鱼网页与 Zombinder 恶意捆绑分发平台
- **应用内界面特征**：外层具备完整合法应用功能（Zombinder 捆绑），内嵌针对不同 Android 版本动态切换的 HTML 诱导页（Android 13+ 自动切换受限设置教学）；拿到无障碍后强制干扰 `KeyguardManager` 禁用指纹/人脸解锁，逼迫用户输入 PIN 码并实时窃取

## 二、典型诱骗话术
- 「Chameleon 展示高仿 HTML 受限设置引导页（针对 Android 13+），引导用户手动授予无障碍」
- 「生物识别暂不可用，请输入 PIN 码/图案锁解锁设备（由无障碍主动禁用生物识别并窃取锁屏 PIN）」

## 三、攻击步骤与技术链路
- 1. Zombinder 通过 Session API 投放并捆绑合法应用外壳降低戒心
- 2. 按系统版本自适应弹出标准无障碍诱导或 Android 13+ 受限设置教学 HTML
- 3. 获得无障碍后禁用生物识别锁屏，强迫回退至 PIN 码并截获，随后在息屏期自主解锁盗刷

## 四、端侧可观测信号与鸿蒙防御映射
- 捆绑正常功能导致首启可能停在登录/业务页（与本课题动态实测中 `Chameleon` 停在登录表单完全一致！）
- 按 OS 版本动态分支的本地/远程 HTML 受限设置引导页
- **鸿蒙端侧防御要点**：静态提取条件分支 HTML 模板 + 禁止第三方无障碍服务干预锁屏认证方式降级

## 五、原文链接（公开报道 / 官方公告 / 安全实验室博客）
- [ThreatFabric 原文：Android Banking Trojan Chameleon Can Now Bypass Any Biometric Authentication](https://www.threatfabric.com/blogs/android-banking-trojan-chameleon-can-now-bypass-any-biometric-authentication)
- [ThreatFabric 原文：Android Banking Trojan Chameleon Is Back in Action (Zombinder)](https://www.threatfabric.com/blogs/android-banking-trojan-chameleon-is-back-in-action)
- [ThreatFabric 原文：Chameleon Targeting Employees Masquerading as a CRM App](https://www.threatfabric.com/blogs/chameleon-is-now-targeting-employees-masquerading-as-a-crm-app)
