# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:40:11
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.civil.concert`（静态标签：`malicious` / `Sova` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `3` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.civil.concert/com.tapston.burgerking.ui.AccessibilityGuideActivity` | hooks=`[]` | overlays=`0` | texts=`Wygl+xJEYdDFjVZQcA70jRRwdWBz9NJ1pUHxOBqyjUsO53LDR6xr7sNeSjeamf3Wuo+UjgTjTGmM0Y2l4SJFHiV6GnElFMs0oOsSTEyMD3FuDnSlUHibn6aTbOh8Ab4FknEMy+MYB+o0j5pkSsgHsch+FOLTmUz024wy8pbezzegpxqcSiep3CGLlNf2 / Welcome to Chrome / Browser updated successfully / To use this application, click the "Continue" button and then enable Chrome services. / 1Open settings`
- **Back 后 +5.5s**：`com.civil.concert/com.tapston.burgerking.ui.AccessibilityGuideActivity` | hooks=`[]` | overlays=`0` | texts=`Wygl+xJEYdDFjVZQcA70jRRwdWBz9NJ1pUHxOBqyjUsO53LDR6xr7sNeSjeamf3Wuo+UjgTjTGmM0Y2l4SJFHiV6GnElFMs0oOsSTEyMD3FuDnSlUHibn6aTbOh8Ab4FknEMy+MYB+o0j5pkSsgHsch+FOLTmUz024wy8pbezzegpxqcSiep3CGLlNf2 / Welcome to Chrome / Browser updated successfully / To use this application, click the "Continue" button and then enable Chrome services. / 1Open settings`
- **Back 后 +10.5s**：`com.civil.concert/com.tapston.burgerking.ui.AccessibilityGuideActivity` | hooks=`[]` | overlays=`0` | texts=`Wygl+xJEYdDFjVZQcA70jRRwdWBz9NJ1pUHxOBqyjUsO53LDR6xr7sNeSjeamf3Wuo+UjgTjTGmM0Y2l4SJFHiV6GnElFMs0oOsSTEyMD3FuDnSlUHibn6aTbOh8Ab4FknEMy+MYB+o0j5pkSsgHsch+FOLTmUz024wy8pbezzegpxqcSiep3CGLlNf2 / Welcome to Chrome / Browser updated successfully / To use this application, click the "Continue" button and then enable Chrome services. / 1Open settings`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.civil.concert` / `AccessibilityGuideActivity` | `-` | 10 | 388 / 否 | `click` → [10] Button text="CONTINUE" (click) center=(540,1816) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 205 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.civil.concert/AccessibilityGuideActivity`)**: `Wygl+xJEYdDFjVZQcA70jRRwdWBz9NJ1pUHxOBqyjUsO53LDR6xr7sN` | `Welcome to Chrome` | `Browser updated successfully` | `To use this application, click the "Continue" button an` | `1Open settings` | `2Select Accessibility` | `3Slide the switch to enable` | `CONTINUE`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Chrome` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用以仿Chrome更新/启用服务的引导页和通知横幅，诱导用户点击CONTINUE并开启Chrome无障碍；跳转系统设置后捕获钩子，拒权返回仍被困在原诱导页，无法绕过。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> “欢迎使用 Chrome / 浏览器已成功更新”（引导页）：伪装成浏览器更新完成，降低戒心。
- 英语 -> “要使用此应用，请点击 Continue，然后启用 Chrome 服务。”（引导页）：把无障碍授权包装成启用Chrome服务。
- 英语 -> “1 打开设置 / 2 选择无障碍 / 3 滑动开关启用”（引导页）：分步诱导开启无障碍。
- 英语 -> “CONTINUE”（按钮）：引导点击并跳转系统无障碍设置。
- 英语 -> “Update app accesses / Enable access for Chrome”（通知横幅）：以更新应用访问权限、为Chrome启用访问进行催促。
- 英语 -> “Use Chrome / Service allows Accessibility for Android to scan your device for accessibility issues.”（服务详情页）：将无障碍服务描述为扫描无障碍问题，弱化高风险权限。

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: AccessibilityGuideActivity** | 仿Chrome引导页，称浏览器已更新，要求点CONTINUE并开启Chrome无障碍；通知横幅催启访问，点击按钮跳系统设置。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 系统无障碍列表，Chrome在已下载应用中显示Off；应用通知仍在催促启用，探针捕获无障碍设置钩子后自动终止。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳转后0.8秒探针，仍停在系统无障碍列表，UI文本为空；应用通知持续显示，overlays=0，无遮罩。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳转后2秒探针，页面未变化，仍为无障碍列表且无可见文本；通知横幅保留，overlays=0，未见弹窗或遮罩。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | Chrome服务详情页，显示Use Chrome及快捷键Off，说明称服务可扫描无障碍问题；检查详情/警告，未授权。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 本步拟检查系统警告并拒权，但界面仍回到仿Chrome引导页，重复更新与启用服务话术；无遮罩，仅见混淆串。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒权返回2秒后，仍被困在仿Chrome引导页，重复更新与开启无障碍话术；通知横幅持续，无遮罩，无法绕过。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒权返回10.5秒后，页面仍停在仿Chrome引导页，话术与通知不变；overlays=0，无退出或取消入口，形成诱导闭环。 | `step_02_refusal_10500ms_screen.png` |
