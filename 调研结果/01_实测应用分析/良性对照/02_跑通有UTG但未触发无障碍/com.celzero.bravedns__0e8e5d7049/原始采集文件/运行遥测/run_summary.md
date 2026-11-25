# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:12:40
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.celzero.bravedns`（静态标签：`benign` / `隐私指示与安全防护工具` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `7` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.celzero.bravedns` / `WelcomeActivity` | `-` | 7 | 147 / 否 | `click` → [6] Button text="Skip" id=btn_skip (click) center=(143, | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.celzero.bravedns` / `HomeScreenActivity` | `-` | 34 | 367 / 否 | `click` → [33] TextView text="Skip Tour" id=tour_skip_btn (click) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.celzero.bravedns` / `HomeScreenActivity` | `-` | 28 | 168 / 否 | `click` → [13] CardView id=fhs_card_apps_cv (click) center=(540,8 | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.celzero.bravedns` / `AppListActivity` | `-` | 71 | 240 / 否 | `system_button` → Back | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.celzero.bravedns` / `HomeScreenActivity` | `-` | 28 | 168 / 否 | `click` → [25] FrameLayout desc="Configure" id=configureFragment  | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.celzero.bravedns` / `HomeScreenActivity` | `-` | 35 | 405 / 否 | `click` → [10] CardView id=fs_firewall_card (click) center=(540,9 | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.celzero.bravedns` / `FirewallActivity` | `-` | 12 | 315 / 否 | `click` → [3] RelativeLayout id=universal_firewall_rl (click) cen | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.celzero.bravedns` / `UniversalFirewallSettingsActivity` | `-` | 35 | 415 / 否 | `click` → [9] Switch id=firewall_background_mode_check (click,unc | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.celzero.bravedns/WelcomeActivity`)**: `Rethink` | `Welcome` | `Rethink is the easiest way to monitor network activity,` | `Skip` | `Next`
- **Step 2 (`com.celzero.bravedns/HomeScreenActivity`)**: `NOT PROTECTED` | `DNS · off` | `Inactive` | `Swipe to see universal firewall, IP, and domain rules` | `0` | `Universal firewall rules` | `Proxy Inactive` | `Firewall · off` | `›` | `START`
- **Step 3 (`com.celzero.bravedns/HomeScreenActivity`)**: `NOT PROTECTED` | `DNS · off` | `Inactive` | `Swipe to see universal firewall, IP, and domain rules` | `0` | `Universal firewall rules` | `Proxy Inactive` | `Firewall · off` | `›` | `START`
- **Step 4 (`com.celzero.bravedns/AppListActivity`)**: `Search apps by uid, name` | `All` | `Allowed` | `Blocked` | `Blocked: Unmetered (WiFi)` | `Showing all apps` | `Application Icon` | `2 Button Navigation Bar` | `allowed` | `0 B 🔺 / 0 B 🔻`
- **Step 5 (`com.celzero.bravedns/HomeScreenActivity`)**: `NOT PROTECTED` | `DNS · off` | `Inactive` | `Swipe to see universal firewall, IP, and domain rules` | `0` | `Universal firewall rules` | `Proxy Inactive` | `Firewall · off` | `›` | `START`
- **Step 6 (`com.celzero.bravedns/HomeScreenActivity`)**: `RETHINK` | `A highly customizable DNS and Firewall` | `Apps` | `Per-app firewall rules and network policy` | `DNS` | `Monitor, block, and encrypt DNS requests.` | `Firewall` | `Monitor network activity and firewall any app or IP add` | `Proxy` | `WireGuard, SOCKS5, and HTTP proxy routing`
- **Step 7 (`com.celzero.bravedns/FirewallActivity`)**: `Universal` | `Universal firewall rules` | `Apply firewall rules on all applications based on devic` | `IP & Port rules` | `Modify blocked or trusted Domain, IP / Port rules.` | `Per App` | `Per app IP / Domain rules` | `Modify per app IP / Domain rules.`
- **Step 8 (`com.celzero.bravedns/UniversalFirewallSettingsActivity`)**: `Universal` | `Apply firewall rules on all applications based on devic` | `Block all apps when device is locked` | `0` | `Block any app not in use` | `Block when source app is unknown` | `Block UDP except DNS and NTP` | `Block when DNS is bypassed` | `Block newly installed apps by default` | `Block on metered (mobile) network`

## 中文逐页引导链路解读

> **全链路总结**：应用从欢迎引导页经跳过导览进入“未保护”主页，再经配置页进入防火墙与通用规则设置页；全程为安全工具的功能说明与设置引导，未观察到强制授权、恐吓或付费诱导。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “监控网络活动、绕过互联网审查并为应用设置防火墙的最简单方式”（欢迎页）
- 英文 -> “高度可定制的 DNS 与防火墙”（配置页）
- 英文 -> “监控网络活动并对任意应用或 IP 地址设防火墙”（配置页）
- 英文 -> “基于设备事件对所有应用应用防火墙规则，例如锁屏或应用未使用时启用”（通用防火墙页）
- 英文 -> “默认阻止新安装应用、阻止绕过 DNS、阻止计量网络”等安全功能说明（通用防火墙设置页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: WelcomeActivity** | 欢迎引导页：Welcome/Next/Skip 即欢迎、下一步、跳过；介绍可监控网络、绕过审查、应用防火墙。本步点 Skip 跳过引导。 | `step_01_action.png` |
| 2 | **Step 2: HomeScreenActivity** | 主页显示 NOT PROTECTED、DNS·off、Firewall·off 与 START；出现功能导览，点击 Skip Tour 跳过；无通知/遮罩。 | `step_02_action.png` |
| 3 | **Step 3: HomeScreenActivity** | 仍在主页，状态为未保护且 DNS/防火墙关闭；点击应用卡片进入应用列表，并非通用防火墙设置页；无通知/遮罩。 | `step_03_action.png` |
| 4 | **Step 4: AppListActivity** | 应用列表页：搜索框、All/Allowed/Blocked 筛选及 Android Auto 等应用；因进入错误页面点系统返回；无通知/遮罩。 | `step_04_action.png` |
| 5 | **Step 5: HomeScreenActivity** | 返回主页，仍显示 NOT PROTECTED、DNS·off、Firewall·off；点击底部 Configure 进入配置页寻找通用防火墙；无通知/遮罩。 | `step_05_action.png` |
| 6 | **Step 6: HomeScreenActivity** | 配置页：RETHINK 及 Apps/DNS/Firewall/Proxy/Network/Settings 入口；点 Firewall 卡片；无通知/遮罩。 | `step_06_action.png` |
| 7 | **Step 7: FirewallActivity** | 防火墙页：Universal 即通用、IP & Port rules、Per App；点通用防火墙规则卡进入设置页；无通知/遮罩。 | `step_07_action.png` |
| 8 | **Step 8: UniversalFirewallSettingsA** | 通用防火墙设置页列出多项拦截开关；本步点击未选中的“阻止任何未使用应用”开关；无通知/遮罩。 | `step_08_action.png` |
