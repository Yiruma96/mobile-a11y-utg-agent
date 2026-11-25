# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:15:25
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.help.marine`（静态标签：`malicious` / `Sova` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `4` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.help.marine/com.tapston.burgerking.ui.AccessibilityGuideActivity` | hooks=`[]` | overlays=`0` | texts=`Wygl+xJEYdDFjVZQcA70jRRwdWBz9NJ1pUHxOBqyjUsO53LDR6xr7sNeSjeamf3Wuo+UjgTjTGmM0Y2l4SJFHiV6GnElFMs0oOsSTEyMD3FuDnSlUHibn6aTbOh8Ab4FknEMy+MYB+o0j5pkSsgHsch+FOLTmUz024wy8pbezzegpxqcSiep3CGLlNf2 / Welcome to Chrome / Browser updated successfully / To use this application, click the "Continue" button and then enable Chrome services. / 1Open settings`
- **Back 后 +5.5s**：`com.help.marine/com.tapston.burgerking.ui.AccessibilityGuideActivity` | hooks=`[]` | overlays=`0` | texts=`Wygl+xJEYdDFjVZQcA70jRRwdWBz9NJ1pUHxOBqyjUsO53LDR6xr7sNeSjeamf3Wuo+UjgTjTGmM0Y2l4SJFHiV6GnElFMs0oOsSTEyMD3FuDnSlUHibn6aTbOh8Ab4FknEMy+MYB+o0j5pkSsgHsch+FOLTmUz024wy8pbezzegpxqcSiep3CGLlNf2 / Welcome to Chrome / Browser updated successfully / To use this application, click the "Continue" button and then enable Chrome services. / 1Open settings`
- **Back 后 +10.5s**：`com.help.marine/com.tapston.burgerking.ui.AccessibilityGuideActivity` | hooks=`[]` | overlays=`0` | texts=`Wygl+xJEYdDFjVZQcA70jRRwdWBz9NJ1pUHxOBqyjUsO53LDR6xr7sNeSjeamf3Wuo+UjgTjTGmM0Y2l4SJFHiV6GnElFMs0oOsSTEyMD3FuDnSlUHibn6aTbOh8Ab4FknEMy+MYB+o0j5pkSsgHsch+FOLTmUz024wy8pbezzegpxqcSiep3CGLlNf2 / Welcome to Chrome / Browser updated successfully / To use this application, click the "Continue" button and then enable Chrome services. / 1Open settings`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.help.marine` / `AccessibilityGuideActivity` | `-` | 1 | 0 / 是 | `click` → [540, 1638] | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 205 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.help.marine/AccessibilityGuideActivity`)**: (空文本)
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Chrome` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用从伪造 Chrome 更新/欢迎页入口，以假“继续”按钮和持续通知诱导用户进入系统无障碍设置并为 Chrome 开启服务；采集到设置钩子后，用户拒权返回仍被困在同一诱导页（TRAPPED_ON_LURE_SCREEN），全程无遮罩。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Update app accesses / Enable access for Chrome -> 更新应用访问权限、为“Chrome”启用访问（通知横幅，贯穿各页）
- Welcome to Chrome -> 欢迎使用 Chrome（假 Chrome 警告页/拒权返回页）
- Browser updated successfully -> 浏览器已成功更新（假 Chrome 警告页/拒权返回页）
- To use this application, click the CONTINUE button and then enable Chrome services. -> 要使用此应用，请点击“继续”并随后启用 Chrome 服务（假 Chrome 警告页/拒权返回页）
- 1 Open settings / 2 Select Accessibility / 3 Slide the switch to enable -> 1 打开设置、2 选择无障碍、3 滑动开关启用（假 Chrome 警告页/拒权返回页）
- CONTINUE -> 继续（假 Chrome 引导页/警告页/拒权返回页）
- Use Chrome / Service allows Accessibility for Android to scan your device for accessibility issues. -> 使用 Chrome；该服务允许 Android 无障碍扫描设备以检查无障碍问题（服务详情页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: AccessibilityGuideActivity** | 假 Chrome 引导页，点击伪造“继续”按钮推进；通知横幅称“更新应用访问/为 Chrome 启用访问”，无遮罩。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 进入系统无障碍列表，Chrome 显示“关闭”；采集到设置钩子与探针后自动终止，通知仍提示为 Chrome 启用访问。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳转后 0.8 秒探针，仍在无障碍设置页且无遮罩；通知横幅继续提示“为 Chrome 启用访问”，界面文本为空。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳转后 2.0 秒探针，仍为无障碍设置页、无遮罩；原应用通知变为空标题/空内容，未见进一步页面变化。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | Chrome 无障碍服务详情页，显示“使用 Chrome”，说明称可扫描无障碍问题；无遮罩，通知仍提示启用访问。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 假 Chrome 警告/引导页，称“浏览器更新成功”，引导打开设置、无障碍并滑动开启后点“继续”；含混淆串，无遮罩。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒权返回 2 秒后仍被困在假 Chrome 诱导页，提示点“继续”并启用 Chrome 服务，附三步开启说明；无遮罩，通知仍在。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒权返回 10.5 秒仍停留同一假 Chrome 诱导页，三步说明和“继续”未消失，呈 TRAPPED_ON_LURE_SCREEN；无遮罩。 | `step_02_refusal_10500ms_screen.png` |
