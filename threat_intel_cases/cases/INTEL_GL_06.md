# INTEL_GL_06 · ToxicPanda & PlayPraetor：中文背景 MaaS 规模化 ODF 与高仿 Google Play 商店页

- **来源类型**：`[Source C · 公开威胁情报 / 警方通报 / 安全实验室博客]`
- **地区与活跃期**：欧洲（意/西/法/葡）与拉美（数万台设备感染）（2024–2025）
- **隐蔽度分级**：`Level 3 · 跨页隐蔽协同与感知劫持型`
- **为何首启/离线动态易遗漏**：C2 远程动态下发近 200 家银行覆盖页（离线沙箱呈空白 WebView）
- **关联新扩充行为模式编号**：`COERCE_07`

## 1. 伪装外衣与带外接触通道
- **伪装形态**：伪装 Google Chrome、主流银行 App、高仿 Google Play 商店下载页
- **带外接触通道**：大规模钓鱼落地页、短信与虚假社媒广告（PlayPraetor 2025 感染超万台设备）
- **应用内界面特征**：采用极简 WebView 高仿商店页与动态覆盖层，利用无障碍服务在受害者真实设备会话中直接发起转账（On-Device Fraud），绕过传统银行基于设备指纹/IP 的异常检测

## 2. 真实诱骗话术与剧本摘录
- 「高仿 Google Play 商店安装页诱骗侧载 APK，随后弹出「需开启辅助服务以完成安装/安全验证」」
- 「面向近 200 家银行/加密应用动态下发高仿覆盖页，配合无障碍远控在受害人本机直接发起转账绕过风控」

## 3. 完整攻击杀伤链
- 1. 钓鱼页面伪装 Google Play 诱导侧载安装
- 2. 诱导授予无障碍权限获取全屏幕结构树读取与手势注入能力
- 3. 通过 C2 实时下发近 200 家目标银行的覆盖页并远程代操作转账

## 4. 端侧 UTG 与跨信道可观测特征
- 高仿应用商店 WebView 诱导 + 远程 C2 下发模板（离线沙箱中易呈空白 WebView）
- 无障碍授权后跨多款金融 App 频繁触发覆盖窗与自动手势注入

## 5. 鸿蒙端侧防御与检测映射
- 金融应用受保护窗口禁止非认证无障碍读取节点与手势注入（对齐 `accessibilityDataSensitive` 机制）

## 6. 权威公开来源
- Cleafy Threat Intelligence (Nov 2024): ToxicPanda Android Banking Trojan (cleafy.com)
- Cleafy Threat Intelligence (2025): PlayPraetor Large-Scale Android RAT MaaS (cleafy.com / securityaffairs.com)
