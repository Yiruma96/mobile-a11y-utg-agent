# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:06:33
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.stone.observe`（静态标签：`malicious` / `TeaBot` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `5` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / Messages / Chrome / Search`
- **Back 后 +5.5s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / Messages / Chrome / Search`
- **Back 后 +10.5s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / Messages / Chrome / Search`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.stone.observe` / `InioawndOIADNwaiond` | `-` | 12 | 562 / 否 | `click` → [9] View text="Installed services5 services" id=this ce | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 222 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.stone.observe/InioawndOIADNwaiond`)**: `QR-Code Scanner: Add-On` | `Accessibility` | `Screen readerGet spoken audio guidance and special cont` | `Visibility enhancementsChange size, contrast, and colou` | `Hearing enhancementsAdjust the audio to help your heari` | `Interaction and dexterityEnhance or replace touch inter` | `Advanced settingsManage Direct access and other advance` | `Installed services5 services` | `About Accessibility` | `Contact Us`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `QR-Code Scanner: Add-On` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：TeaBot 样本以“QR-Code Scanner: Add-On”伪装无障碍插件，先展示仿系统无障碍引导并提示需启用，再跳转系统设置诱导授予全权无障碍。拒绝后回到桌面且无异常遮罩，表现为优雅停留或降级。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 二维码扫描器：附加组件（步骤1伪装应用名、步骤2已下载应用列表）
- 英文 -> 你需要启用无障碍（步骤1提示气泡）
- 英文 -> 已安装服务 5 项（步骤1引导点击的入口）
- 英文 -> 使用二维码扫描器：附加组件（服务详情页启用文案）
- 英文 -> 按住音量键（服务详情页快捷方式说明）
- 英文 -> 未提供描述（服务详情页说明缺失）
- 英文 -> 允许“QR-Code Scanner: Add-On”完全控制你的设备？（系统警告弹窗）
- 英文 -> 完全控制适合帮助无障碍需求的应用，但不适合大多数应用（系统警告弹窗）
- 英文 -> 可查看并控制屏幕，读取屏幕上所有内容并覆盖显示在其他应用上（系统警告弹窗）
- 英文 -> 可查看并执行操作，跟踪与应用或硬件传感器的交互，并代表你操作应用（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: InioawndOIADNwaiond** | 仿系统无障碍引导页，英文提示“需启用无障碍”并列出已安装服务；本步点击“Installed services 5 services”入口。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 系统无障碍设置页，“DOWNLOADED APPS”下显示“QR-Code Scanner: Add-On”为关闭；探针捕获设置钩子后自动终止。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳后0.8秒仍停留在无障碍设置页，界面无新增文本、无通知横幅、遮罩数为0，仅等待观察。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳后2.0秒继续停留于无障碍设置页，仍未出现弹窗或覆盖层，遮罩数为0，探针等待结束。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 服务详情页展示“Use QR-Code Scanner: Add-On”启用说明及“Hold volume keys”快捷项，底部称未提供描述；本步仅检查详情。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统全权控制警告弹窗：英文询问是否允许该附加组件完全控制设备，并说明可读屏、覆盖及代操作；本步检查后拒权。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒绝授权后2秒返回桌面启动器，显示应用列表、搜索等常规图标，无通知或遮罩，表现为优雅停留或降级。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒权后10.5秒仍在桌面启动器，仅见应用列表与搜索入口，无再次诱导弹窗、通知或覆盖层，状态保持降级。 | `step_02_refusal_10500ms_screen.png` |
