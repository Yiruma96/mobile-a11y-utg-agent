# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:16:38
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.bypressfo`（静态标签：`malicious` / `Exobot` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.bypressfo/com.bypressfo.p050e` | hooks=`[]` | overlays=`0` | texts=`Permission required / Enable permission for BAWAG PSK Security to continue / Continue`
- **Back 后 +5.5s**：`com.bypressfo/com.bypressfo.p050e` | hooks=`[]` | overlays=`0` | texts=`Permission required / Enable permission for BAWAG PSK Security to continue / Continue`
- **Back 后 +10.5s**：`com.bypressfo/com.bypressfo.p050e` | hooks=`[]` | overlays=`0` | texts=`Permission required / Enable permission for BAWAG PSK Security to continue / Continue`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `RequestIgnoreBatteryOptimizations` | `-` | 4 | 192 / 否 | `click` → [4] Button text="Allow" id=button1 (click) center=(887, | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.bypressfo` / `p050e` | `-` | 3 | 79 / 否 | `click` → [3] Button text="Continue" id=button1 (click) center=(5 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 217 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/RequestIgnoreBatteryOptimizations`)**: `Let app always run in background?` | `Allowing BAWAG PSK Security to always run in the backgr` | `Deny` | `Allow`
- **Step 2 (`com.bypressfo/p050e`)**: `Permission required` | `Enable permission for BAWAG PSK Security to continue` | `Continue`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `BAWAG PSK Security` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用伪装成 BAWAG PSK Security，先诱导允许后台常驻，再以应用内“需要权限”弹窗和通知反复引导开启无障碍服务；进入系统无障碍设置后探针捕获钩子，用户拒绝时仍重拉同一权限诱导框形成循环。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Let app always run in background? -> 让应用始终在后台运行？（Step 1 系统电池优化弹窗）
- Allowing BAWAG PSK Security to always run in the background may reduce battery life. You can change this later from Settings > Apps & notifications. -> 允许 BAWAG PSK Security 始终后台运行可能缩短续航，可稍后在设置中更改（Step 1 系统电池优化弹窗）
- Permission required -> 需要权限（Step 2、拒权弹窗）
- Enable permission for BAWAG PSK Security to continue -> 请为 BAWAG PSK Security 启用权限以继续（Step 2、拒权弹窗）
- Continue -> 继续（Step 2、拒权弹窗）
- Use BAWAG PSK Security -> 使用 BAWAG PSK Security（服务详情页）
- Service must be enabled. -> 必须启用服务（服务详情页）
- String (Enable service) -> 启用服务（通知标题）
- String (BAWAG PSK Security) -> BAWAG PSK Security（通知正文）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: RequestIgnoreBatteryOptimi** | 系统电池优化弹窗：提示允许 BAWAG PSK Security 后台常驻可能耗电，仍诱导点 Allow；无遮罩。 | `step_01_action.png` |
| 2 | **Step 2: p050e** | 应用内伪造“需要权限”弹窗，称须为 BAWAG PSK Security 启用权限才能继续；本步点 Continue，顶部有启用服务通知横幅。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 系统无障碍列表页，BAWAG PSK Security 显示为 Off；启用服务通知仍在，探针捕获无障碍设置钩子后自动终止。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转后 0.8 秒探针，仍停留系统无障碍设置页；未见遮罩，通知横幅继续显示启用服务诱导。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后 2.0 秒探针，页面仍为系统无障碍设置且无遮罩；启用服务通知持续展示，强化授权诱导。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | 无障碍服务详情页，开关为 Use BAWAG PSK Security，并提示 Service must be enabled；通知仍在，本步仅查看。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 应用内“需要权限”弹窗再次出现，仍以须启用权限才能继续诱导；本步仅检查，无遮罩且无通知，只有 Continue。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 拒绝返回 2 秒后，应用重新拉起同一“需要权限”弹窗并要求 Continue，形成拒权后循环诱导。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒绝返回 10.5 秒后，仍再次弹出“需要权限”诱导框，Continue 文案不变，说明拒权后持续重试拉起。 | `step_03_refusal_10500ms_screen.png` |
