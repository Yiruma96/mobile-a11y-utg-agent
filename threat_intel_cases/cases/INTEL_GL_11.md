# INTEL_GL_11 · RatOn & NGate & SuperCard X：TOAD 电话诱导 + 无障碍/NFC 碰一碰隔空盗刷

- **来源类型**：`[Source C · 公开威胁情报 / 警方通报 / 安全实验室博客]`
- **地区与活跃期**：欧洲（捷克/波兰/意大利）及中文背景 MaaS 全球扩散（2024–2025）
- **隐蔽度分级**：`Level 4 · 带外通话社工 + 伪会议/远控协同型`
- **为何首启/离线动态易遗漏**：电话带外指挥「把银行卡贴靠手机背面 NFC」+ 部分融合无障碍自动化盗刷
- **关联新扩充行为模式编号**：`EVADE_09`, `EVADE_05`

## 1. 伪装外衣与带外接触通道
- **伪装形态**：伪装银行卡安全核验 App（如 *Verica Carta*、*KingCard NFC*、假 NFC 认证工具、RatOn 多功能木马）
- **带外接触通道**：TOAD 电话/短信冒充银行风控称卡片存在盗刷风险，要求下载核验 App 并贴卡验证
- **应用内界面特征**：表面极简（仅要求输入卡 PIN 并展示「请将银行卡贴靠手机背面」动画），部分家族（如 `RatOn`）进一步结合无障碍权限屏蔽拦截与自动操作支付界面；底层基于开源 `NFCGate` / HCE 将实体芯片卡加密报文实时中继至远端黑产手机在 ATM/POS 机隔空取现

## 2. 真实诱骗话术与剧本摘录
- 「为解除卡片风险锁定，请下载「卡片安全认证」App，输入 PIN 码并将实体银行卡贴靠在手机背面 NFC 感应区」
- 「RatOn 同时结合无障碍权限执行覆盖页套密、ATS 自动转账与 NFC 中继盗刷」

## 3. 完整攻击杀伤链
- 1. 电话/短信冒充银行引导侧载安装假 NFC 卡片验证 App（或 PWA）
- 2. 诱骗输入银行卡 PIN 码（及在 RatOn 等变种中开启无障碍辅助权限）
- 3. 引导受害人把实体银行卡贴靠手机背面，通过 NFC + HCE 实时中继至攻击者终端在 ATM 机取现

## 4. 端侧 UTG 与跨信道可观测特征
- 侧载非银行官方应用在通话态下出现「NFC 贴卡 / 输入 PIN 码 / 卡片验证」界面并与无障碍/覆盖窗联动
- 代表 2025 移动金融诈骗从「纯无障碍控屏」向「无障碍 + NFC 物理中继」演进的新趋势

## 5. 鸿蒙端侧防御与检测映射
- 通话并发态下对非官方金融应用的 NFC 读卡/HCE 中继与无障碍权限联动触发强反诈阻断

## 6. 权威公开来源
- ESET Research (Aug 2024): NGate — First Android Malware Relaying NFC Traffic (eset.com)
- Cleafy Threat Intelligence (Apr 2025): SuperCard X Chinese-Speaking NFC Relay MaaS (cleafy.com)
- ThreatFabric / Kaspersky (2025): RatOn RAT + ATS + NFC Relay Analysis
