# RatOn & NGate & SuperCard X：TOAD 电话诱导 + 无障碍/NFC 碰一碰隔空盗刷

- **案例编号**：`INTEL_GL_11` ｜ **地区与活跃期**：欧洲（捷克/波兰/意大利）及中文背景 MaaS 全球扩散（2024–2025）
- **诱导隐蔽度分级**：`L4 · 带外通话社工 + 伪会议/远控协同型`
- **为何首次动态运行容易遗漏**：电话带外指挥「把银行卡贴靠手机背面 NFC」+ 部分融合无障碍自动化盗刷

## 一、伪装形式与接触通道
- **伪装外衣**：伪装银行卡安全核验 App（如 *Verica Carta*、*KingCard NFC*、假 NFC 认证工具、RatOn 多功能木马）
- **带外接触通道**：TOAD 电话/短信冒充银行风控称卡片存在盗刷风险，要求下载核验 App 并贴卡验证
- **应用内界面特征**：表面极简（仅要求输入卡 PIN 并展示「请将银行卡贴靠手机背面」动画），部分家族（如 `RatOn`）进一步结合无障碍权限屏蔽拦截与自动操作支付界面；底层基于开源 `NFCGate` / HCE 将实体芯片卡加密报文实时中继至远端黑产手机在 ATM/POS 机隔空取现

## 二、典型诱骗话术
- 「为解除卡片风险锁定，请下载「卡片安全认证」App，输入 PIN 码并将实体银行卡贴靠在手机背面 NFC 感应区」
- 「RatOn 同时结合无障碍权限执行覆盖页套密、ATS 自动转账与 NFC 中继盗刷」

## 三、攻击步骤与技术链路
- 1. 电话/短信冒充银行引导侧载安装假 NFC 卡片验证 App（或 PWA）
- 2. 诱骗输入银行卡 PIN 码（及在 RatOn 等变种中开启无障碍辅助权限）
- 3. 引导受害人把实体银行卡贴靠手机背面，通过 NFC + HCE 实时中继至攻击者终端在 ATM 机取现

## 四、端侧可观测信号与鸿蒙防御映射
- 侧载非银行官方应用在通话态下出现「NFC 贴卡 / 输入 PIN 码 / 卡片验证」界面并与无障碍/覆盖窗联动
- 代表 2025 移动金融诈骗从「纯无障碍控屏」向「无障碍 + NFC 物理中继」演进的新趋势
- **鸿蒙端侧防御要点**：通话并发态下对非官方金融应用的 NFC 读卡/HCE 中继与无障碍权限联动触发强反诈阻断

## 五、原文链接（公开报道 / 官方公告 / 安全实验室博客）
- [ESET Research 首发原文：NGate Android Malware Relays NFC Traffic to Steal Victims' Cash from ATMs](https://www.eset.com/us/about/newsroom/research/eset-research-discovers-ngate-android-malware-which-relays-nfc-traffic-to-steal-victims-cash-from-atms-1/)
- [ESET Research 追踪：NGate Hides in NFC Payment App Possibly Built with AI](https://www.eset.com/us/about/newsroom/research/eset-research-ngate-hides-nfc-payment-app-ai/)
- [Cleafy Labs 首发原文：SuperCard X — Exposing a Chinese-Speaking MaaS for NFC Relay Fraud](https://www.cleafy.com/cleafy-labs/supercardx-exposing-chinese-speaker-maas-for-nfc-relay-fraud-operation)
- [Malwarebytes：Android Malware Turns Phones into Malicious Tap-to-Pay Machines](https://www.malwarebytes.com/blog/news/2025/04/android-malware-turns-phones-into-malicious-tap-to-pay-machines)
