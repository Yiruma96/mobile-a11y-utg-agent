# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:00:29
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.agomi.applocker`（静态标签：`malicious` / `TOASTAMIGO` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `4` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.agomi.applocker/com.goami.applocker.AppLocker.ApplicationListActivity` | hooks=`[]` | overlays=`0` | texts=`Attention / This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it. / Cancel / Confirm`
- **Back 后 +5.5s**：`com.agomi.applocker/com.goami.applocker.AppLocker.ApplicationListActivity` | hooks=`[]` | overlays=`0` | texts=`Attention / This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it. / Cancel / Confirm`
- **Back 后 +10.5s**：`com.agomi.applocker/com.goami.applocker.AppLocker.ApplicationListActivity` | hooks=`[]` | overlays=`0` | texts=`Attention / This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it. / Cancel / Confirm`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.agomi.applocker` / `ApplicationListActivity` | `-` | 4 | 130 / 否 | `click` → [4] TextView text="Confirm" id=btn_ok (click) center=(8 | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 214 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.agomi.applocker/ApplicationListActivity`)**: `Attention` | `This device version is above Android 4.0.3 .Please Go S` | `Cancel` | `Confirm`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Smart AppLocker` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用入口即用Attention弹窗以Android版本为由诱导用户前往系统无障碍开启Smart AppLocker；跳转设置并暴露服务详情后，若用户点Deny拒权，应用返回列表页立即重启同一诱导弹窗，并配合常驻“服务运行中”通知反复施压授权。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “设备版本高于Android 4.0.3，请前往设置→无障碍→App Locker并开启”，以系统兼容性为由诱导开启无障碍（应用内Attention弹窗）
- 英文 -> 通知横幅“AppLocker/服务运行中”，以常驻通知强化服务已启用（各页通知栏）
- 英文 -> “Smart AppLocker/使用Smart AppLocker/用于Android 4.0.3以上轻松锁应用的服务”，以应用锁功能包装无障碍服务（服务详情页）
- 英文 -> 系统警告“允许Smart AppLocker完全控制设备？”，并说明可读屏、覆盖显示、追踪交互并代操作，诱导点Allow（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ApplicationListActivity** | 应用列表页弹出英文Attention弹窗，称设备高于Android 4.0.3，要求去设置→无障碍→App Locker开启；点击Confirm跳转系统设置，通知持续显示服务运行中。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 系统无障碍列表页，DOWNLOADED APPS下Smart AppLocker显示Off；本步采集无障碍Hook与探针后自动终止，通知仍显示AppLocker服务运行中。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳转后0.8秒探针停在无障碍设置页，界面文本为空、无遮罩；通知横幅仍为AppLocker/服务运行中，未见新增弹窗。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳转后2.0秒仍停在无障碍设置页，界面文本为空、无遮罩；通知持续显示AppLocker服务运行中，未出现新弹窗或覆盖层。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | Smart AppLocker服务详情页：显示Use Smart AppLocker开关、快捷键与音量键选项，说明称用于Android 4.0.3以上轻松锁应用；本步仅查看未授权。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统权限警告弹窗：英文询问是否允许Smart AppLocker完全控制设备，列明可读屏、覆盖显示、追踪交互并代操作；有Allow/Deny，本步未授权。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒权返回2秒后，应用重回列表页并再次弹出同一Attention弹窗，要求去设置开启无障碍；通知横幅仍显示服务运行中，无遮罩。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒权返回10.5秒后仍停列表页且同一Attention诱导弹窗被重启，持续要求开启无障碍；通知显示服务运行中，无遮罩。 | `step_02_refusal_10500ms_screen.png` |
