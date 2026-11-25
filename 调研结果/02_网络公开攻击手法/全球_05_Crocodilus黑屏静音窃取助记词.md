# Crocodilus：加壳载荷 + 假助记词告警 + 黑屏静音窃取 OTP 与加密钱包

- **案例编号**：`INTEL_GL_05` ｜ **地区与活跃期**：欧洲（西班牙/波兰）、土耳其、拉美、亚洲（2025）
- **诱导隐蔽度分级**：`L3 · 跨页隐蔽协同与感知劫持型`
- **为何首次动态运行容易遗漏**：强加壳 + 联网 C2 下发动态 HTML 诱饵（离线首启不暴露完整诱饵）

## 一、伪装形式与接触通道
- **伪装外衣**：伪装浏览器更新、金融服务、购物/奖励应用（含本数据集 `Crocodilus` 加壳样本）
- **带外接触通道**：钓鱼广告（Meta/社媒广告）与定制 Dropper 分发
- **应用内界面特征**：使用高度混淆/加壳外衣（与本课题离线动态首启未触达无障碍的现象高度吻合）；获得无障碍后通过黑屏遮罩 + 静音隐藏后台操作，专门爬取 Google Authenticator 验证码与加密钱包助记词

## 二、典型诱骗话术
- 「请在 12 小时内备份您的钱包助记词，否则将失去账户访问权限（无障碍配合动态 HTML 假提示）」
- 「正在同步安全配置，请勿关闭屏幕（黑屏遮罩配合静音后台操作）」

## 三、攻击步骤与技术链路
- 1. 社媒广告投放 Dropper 绕过受限设置并释放加壳主体
- 2. 诱导开启无障碍后监控金融与加密钱包前台切换
- 3. 叠加动态 HTML 假警告与纯黑屏遮罩，静音后台完成设备端盗刷与助记词收割

## 四、端侧可观测信号与鸿蒙防御映射
- 强加壳主体首启不暴露动态 HTML 诱饵，需静态加壳标注 + 威胁情报联合刻画
- 无障碍授权后伴随全屏纯黑遮罩 + 音频静音 + 读取认证器/钱包节点
- **鸿蒙端侧防御要点**：监测无障碍启用后的全屏低亮度/纯黑遮罩与异常静音组合行为

## 五、原文链接（公开报道 / 官方公告 / 安全实验室博客）
- [ThreatFabric 首发原文：Exposing Crocodilus — New Device Takeover Malware Targeting Android](https://www.threatfabric.com/blogs/exposing-crocodilus-new-device-takeover-malware-targeting-android-devices)
- [ThreatFabric 演进追踪：Crocodilus Mobile Malware Evolving Fast, Going Global](https://www.threatfabric.com/blogs/crocodilus-mobile-malware-evolving-fast-going-global)
- [Zimperium 分析：Pragmatic Crocodilus — A New Variant in the Horizon](https://zimperium.com/blog/pragmatic-crocodilus-a-new-variant-in-the-horizon)
- [The Hacker News：Android Trojan Crocodilus Active in Europe & South America](https://thehackernews.com/2025/06/android-trojan-crocodilus-now-active-in.html)
