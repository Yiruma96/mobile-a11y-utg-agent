# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:20:10
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.sarangem.zenwell`（静态标签：`benign` / `专注自律与防沉迷管控` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `4` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.sarangem.zenwell/com.sarangem.zenwell.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Let’s unlock your focus goals! Zenwell needs Accessibility permission to see which apps are open so it can keep your screen time in check. / Grant permission / Create schedules to lock distracting apps. Tap '+' to begin. / Zenwell / Home`
- **Back 后 +5.5s**：`com.sarangem.zenwell/com.sarangem.zenwell.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Let’s unlock your focus goals! Zenwell needs Accessibility permission to see which apps are open so it can keep your screen time in check. / Grant permission / Create schedules to lock distracting apps. Tap '+' to begin. / Zenwell / Home`
- **Back 后 +10.5s**：`com.sarangem.zenwell/com.sarangem.zenwell.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Let’s unlock your focus goals! Zenwell needs Accessibility permission to see which apps are open so it can keep your screen time in check. / Grant permission / Create schedules to lock distracting apps. Tap '+' to begin. / Zenwell / Home`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.sarangem.zenwell` / `MainActivity` | `-` | 15 | 287 / 否 | `click` → [3] TextView text="Grant permission" center=(885,468) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 206 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.sarangem.zenwell/MainActivity`)**: `Let’s unlock your focus goals! Zenwell needs Accessibil` | `Grant permission` | `Create schedules to lock distracting apps. Tap '+' to b` | `Zenwell` | `Home` | `Stats` | `Settings` | `Skip guide` | `Enable permissions to unlock your focus`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Zenwell` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用入口主界面以“解锁专注目标”为由请求无障碍权限，点击后跳转系统无障碍列表与 Zenwell 服务详情，最终弹出系统全权控制警告；拒绝授权后返回主界面仍保持原页并可降级使用，未出现强制遮挡或通知骚扰。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Let’s unlock your focus goals! Zenwell needs Accessibility permission to see which apps are open so it can keep your screen time in check. -> 让我们解锁你的专注目标！Zenwell 需要无障碍权限查看哪些应用正在打开，以便管控屏幕时间。（主界面）
- Enable permissions to unlock your focus -> 启用权限以解锁你的专注（主界面底部提示）
- Grant permission -> 授予权限（主界面按钮）
- Zenwell uses this service to know which app you are using and locks that app to cure your addiction. -> Zenwell 使用此服务了解你正在使用哪个应用，并锁定该应用来戒除你的成瘾。（服务详情页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 主界面以“解锁专注目标”为由请求无障碍权限，说明可查看已开应用以管控屏幕时间；点击“Grant permission”，无通知、无遮罩。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 跳至系统无障碍列表，DOWNLOADED APPS 下 Zenwell 显示“Off”；采集到无障碍设置钩子与探针后自动终止，尚未授权。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 授权跳转后 0.8 秒探针：仍停留在系统无障碍设置页，界面文本为空，无通知横幅、无悬浮遮罩（overlays=0），状态未变。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳转后 2.0 秒二次探针：系统无障碍设置页保持原样，无弹窗、无通知、无遮罩（overlays=0），未发生授权操作。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 进入 Zenwell 服务详情页，有“Use Zenwell”开关与“Off”状态；说明称用该服务识别当前应用并锁定以戒瘾，属权限用途说明。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统弹出全权控制警告：允许 Zenwell 完全控制设备？列出可查看屏幕内容、代操作等能力；提供“Allow/Deny”，本步未点允许。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 在系统警告中点“Deny”拒权后 2 秒返回主界面；仍显示授权引导与“Grant permission”，无通知、无遮罩，应用保持原页降级。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒权返回 10.5 秒后主界面未变，继续展示“启用权限以解锁专注”等引导；无通知横幅、无悬浮遮罩，未强制跳转或锁屏。 | `step_02_refusal_10500ms_screen.png` |
