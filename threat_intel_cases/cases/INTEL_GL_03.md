# INTEL_GL_03 · Vultur（2024 升级版）：短信诱回拨（TOAD）+ 伪装 McAfee Security 无障碍接管

- **来源类型**：`[Source C · 公开威胁情报 / 警方通报 / 安全实验室博客]`
- **地区与活跃期**：欧洲（英国/荷兰/意大利等）（2024）
- **隐蔽度分级**：`Level 4 · 带外通话社工 + 伪会议/远控协同型`
- **为何首启/离线动态易遗漏**：短信+人工来电混合驱动 + Brunhilda 多阶段 Dropper 延迟解密
- **关联新扩充行为模式编号**：`EVADE_05`, `EVADE_08`

## 1. 伪装外衣与带外接触通道
- **伪装形态**：伪装 McAfee Security 与 Android Accessibility Suite（内置 Brunhilda Dropper）
- **带外接触通道**：先发银行大额未授权交易预警短信 → 诱导受害人主动回拨假客服电话 → 电话发送下载链接
- **应用内界面特征**：界面高仿 McAfee 安全扫描界面；获取无障碍后具备远控点击/滑动、关闭锁屏密码（Disable Keyguard）、静音与阻止指定安全软件运行等完整 DTO 能力

## 2. 真实诱骗话术与剧本摘录
- 「检测到您的银行账户发生未授权大额转账，请立即致电客服核实（短信诱饵）」
- 「请安装我们发来的 McAfee Security 安全版本并开启辅助保护以拦截盗刷」

## 3. 完整攻击杀伤链
- 1. 短信钓鱼诱导受害人主动呼出电话（TOAD），建立极高心理信任
- 2. 电话引导安装伪装 McAfee 的 Dropper 解密释放 Vultur 载荷
- 3. 诱导授予无障碍权限后远程执行点击、滑动、解密锁屏并实施设备端欺诈（ODF）

## 4. 端侧 UTG 与跨信道可观测特征
- 高仿知名安全品牌（McAfee / Google Play Protect）UI + 非官方签名
- 无障碍详情页或启动链路中冒用系统无障碍套件名称（Android Accessibility Suite）

## 5. 鸿蒙端侧防御与检测映射
- 品牌图标/服务名与包签名一致性核验 + 电话并发无障碍高危授权阻断

## 6. 权威公开来源
- Fox-IT (March 2024): Vultur Android Banking Trojan Upgraded with Remote Control & McAfee Disguise (fox-it.com)
