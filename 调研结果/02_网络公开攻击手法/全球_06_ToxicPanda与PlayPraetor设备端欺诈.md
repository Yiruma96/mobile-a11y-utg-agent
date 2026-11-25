# ToxicPanda & PlayPraetor：中文背景 MaaS 规模化 ODF 与高仿 Google Play 商店页

- **案例编号**：`INTEL_GL_06` ｜ **地区与活跃期**：欧洲（意/西/法/葡）与拉美（数万台设备感染）（2024–2025）
- **诱导隐蔽度分级**：`L3 · 跨页隐蔽协同与感知劫持型`
- **为何首次动态运行容易遗漏**：C2 远程动态下发近 200 家银行覆盖页（离线沙箱呈空白 WebView）

## 一、伪装形式与接触通道
- **伪装外衣**：伪装 Google Chrome、主流银行 App、高仿 Google Play 商店下载页
- **带外接触通道**：大规模钓鱼落地页、短信与虚假社媒广告（PlayPraetor 2025 感染超万台设备）
- **应用内界面特征**：采用极简 WebView 高仿商店页与动态覆盖层，利用无障碍服务在受害者真实设备会话中直接发起转账（On-Device Fraud），绕过传统银行基于设备指纹/IP 的异常检测

## 二、典型诱骗话术
- 「高仿 Google Play 商店安装页诱骗侧载 APK，随后弹出「需开启辅助服务以完成安装/安全验证」」
- 「面向近 200 家银行/加密应用动态下发高仿覆盖页，配合无障碍远控在受害人本机直接发起转账绕过风控」

## 三、攻击步骤与技术链路
- 1. 钓鱼页面伪装 Google Play 诱导侧载安装
- 2. 诱导授予无障碍权限获取全屏幕结构树读取与手势注入能力
- 3. 通过 C2 实时下发近 200 家目标银行的覆盖页并远程代操作转账

## 四、端侧可观测信号与鸿蒙防御映射
- 高仿应用商店 WebView 诱导 + 远程 C2 下发模板（离线沙箱中易呈空白 WebView）
- 无障碍授权后跨多款金融 App 频繁触发覆盖窗与自动手势注入
- **鸿蒙端侧防御要点**：金融应用受保护窗口禁止非认证无障碍读取节点与手势注入（对齐 `accessibilityDataSensitive` 机制）

## 五、原文链接（公开报道 / 官方公告 / 安全实验室博客）
- [Cleafy Labs 原文：ToxicPanda — A New Banking Trojan from Asia Hit Europe and LATAM](https://www.cleafy.com/cleafy-labs/toxicpanda-a-new-banking-trojan-from-asia-hit-europe-and-latam)
- [Cleafy Labs 原文：PlayPraetor's Evolving Threat — Scaling an Android RAT Globally](https://www.cleafy.com/cleafy-labs/playpraetors-evolving-threat-how-chinese-speaking-actors-globally-scale-an-android-rat)
- [Promon：PlayPraetor Malware — Why Banking Apps Need Protection from the Inside Out](https://promon.io/security-news/playpraetor-malware-why-banking-apps-need-protection-from-the-inside-out)
- [SecurityAffairs：PlayPraetor Android RAT Expands Rapidly](https://securityaffairs.com/180760/malware/playpraetor-android-rat-expands-rapidly-across-spanish-and-french-speaking-regions.html)
