# Vultur（2024 升级版）：短信诱回拨（TOAD）+ 伪装 McAfee Security 无障碍接管

- **案例编号**：`INTEL_GL_03` ｜ **地区与活跃期**：欧洲（英国/荷兰/意大利等）（2024）
- **诱导隐蔽度分级**：`L4 · 带外通话社工 + 伪会议/远控协同型`
- **为何首次动态运行容易遗漏**：短信+人工来电混合驱动 + Brunhilda 多阶段 Dropper 延迟解密

## 一、伪装形式与接触通道
- **伪装外衣**：伪装 McAfee Security 与 Android Accessibility Suite（内置 Brunhilda Dropper）
- **带外接触通道**：先发银行大额未授权交易预警短信 → 诱导受害人主动回拨假客服电话 → 电话发送下载链接
- **应用内界面特征**：界面高仿 McAfee 安全扫描界面；获取无障碍后具备远控点击/滑动、关闭锁屏密码（Disable Keyguard）、静音与阻止指定安全软件运行等完整 DTO 能力

## 二、典型诱骗话术
- 「检测到您的银行账户发生未授权大额转账，请立即致电客服核实（短信诱饵）」
- 「请安装我们发来的 McAfee Security 安全版本并开启辅助保护以拦截盗刷」

## 三、攻击步骤与技术链路
- 1. 短信钓鱼诱导受害人主动呼出电话（TOAD），建立极高心理信任
- 2. 电话引导安装伪装 McAfee 的 Dropper 解密释放 Vultur 载荷
- 3. 诱导授予无障碍权限后远程执行点击、滑动、解密锁屏并实施设备端欺诈（ODF）

## 四、端侧可观测信号与鸿蒙防御映射
- 高仿知名安全品牌（McAfee / Google Play Protect）UI + 非官方签名
- 无障碍详情页或启动链路中冒用系统无障碍套件名称（Android Accessibility Suite）
- **鸿蒙端侧防御要点**：品牌图标/服务名与包签名一致性核验 + 电话并发无障碍高危授权阻断

## 五、原文链接（公开报道 / 官方公告 / 安全实验室博客）
- [Fox-IT 官方技术报告：Android Malware Vultur Expands Its Wingspan (2024)](https://blog.fox-it.com/2024/03/28/android-malware-vultur-expands-its-wingspan/)
