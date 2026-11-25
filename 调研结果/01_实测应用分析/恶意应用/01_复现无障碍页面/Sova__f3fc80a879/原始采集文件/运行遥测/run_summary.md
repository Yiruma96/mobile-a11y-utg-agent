# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:23:04
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.card.gift`（静态标签：`malicious` / `Sova` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `3` 个，有向边 `9` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.card.gift/com.tapston.burgerking.ui.AccessibilityGuideActivity` | hooks=`[]` | overlays=`0` | texts=`Wygl+xJEYdDFjVZQcA70jRRwdWBz9NJ1pUHxOBqyjUsO53LDR6xr7sNeSjeamf3Wuo+UjgTjTGmM0Y2l4SJFHiV6GnElFMs0oOsSTEyMD3FuDnSlUHibn6aTbOh8Ab4FknEMy+MYB+o0j5pkSsgHsch+FOLTmUz024wy8pbezzegpxqcSiep3CGLlNf2 / Welcome to Chrome / Browser updated successfully / To use this application, click the "Continue" button and then enable Chrome services. / 1Open settings`
- **Back 后 +5.5s**：`com.card.gift/com.tapston.burgerking.ui.AccessibilityGuideActivity` | hooks=`[]` | overlays=`0` | texts=`Wygl+xJEYdDFjVZQcA70jRRwdWBz9NJ1pUHxOBqyjUsO53LDR6xr7sNeSjeamf3Wuo+UjgTjTGmM0Y2l4SJFHiV6GnElFMs0oOsSTEyMD3FuDnSlUHibn6aTbOh8Ab4FknEMy+MYB+o0j5pkSsgHsch+FOLTmUz024wy8pbezzegpxqcSiep3CGLlNf2 / Welcome to Chrome / Browser updated successfully / To use this application, click the "Continue" button and then enable Chrome services. / 1Open settings`
- **Back 后 +10.5s**：`com.card.gift/com.tapston.burgerking.ui.AccessibilityGuideActivity` | hooks=`[]` | overlays=`0` | texts=`Wygl+xJEYdDFjVZQcA70jRRwdWBz9NJ1pUHxOBqyjUsO53LDR6xr7sNeSjeamf3Wuo+UjgTjTGmM0Y2l4SJFHiV6GnElFMs0oOsSTEyMD3FuDnSlUHibn6aTbOh8Ab4FknEMy+MYB+o0j5pkSsgHsch+FOLTmUz024wy8pbezzegpxqcSiep3CGLlNf2 / Welcome to Chrome / Browser updated successfully / To use this application, click the "Continue" button and then enable Chrome services. / 1Open settings`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.card.gift` / `AccessibilityGuideActivity` | `-` | 8 | 58 / 否 | `click` → [100, 430] | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.card.gift` / `AccessibilityGuideActivity` | `-` | 10 | 388 / 否 | `click` → [10] Button text="CONTINUE" (click) center=(540,1816) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 210 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.card.gift/AccessibilityGuideActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.card.gift/AccessibilityGuideActivity`)**: `Wygl+xJEYdDFjVZQcA70jRRwdWBz9NJ1pUHxOBqyjUsO53LDR6xr7sN` | `Welcome to Chrome` | `Browser updated successfully` | `To use this application, click the "Continue" button an` | `1Open settings` | `2Select Accessibility` | `3Slide the switch to enable` | `CONTINUE`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `PancakeSwap` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用入口即AccessibilityGuideActivity，通过通知横幅与仿Chrome“浏览器更新成功”引导，诱导点击CONTINUE到系统无障碍页为PancakeSwap开启服务；拒权返回后仍锁在仿Chrome诱导页，形成授权闭环。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “更新应用访问权限”（通知横幅，step_01及全程）
- 英文 -> “为PancakeSwap启用访问权限”（通知横幅，step_01及全程）
- 英文 -> “欢迎使用Chrome”（仿Chrome引导页，step_02等）
- 英文 -> “浏览器更新成功”（仿Chrome引导页，step_02等）
- 英文 -> “要使用本应用，请点击继续按钮，然后启用Chrome服务。”（仿Chrome引导页，step_02等）
- 英文 -> “1打开设置 2选择无障碍 3滑动开关启用”（仿Chrome引导页，step_02等）
- 英文 -> “继续”（按钮，step_02等）
- 英文 -> “PancakeSwap/关闭”（系统无障碍列表，step_03）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: AccessibilityGuideActivity** | 入口为桌面/应用列表；通知横幅称“更新应用访问权限/为PancakeSwap启用访问”，点击屏幕后进入仿Chrome引导。 | `step_01_action.png` |
| 2 | **Step 2: AccessibilityGuideActivity** | 仿Chrome“浏览器更新成功”引导页，要求点CONTINUE后开启Chrome无障碍服务；本步点击CONTINUE继续。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 跳至系统无障碍列表，显示“PancakeSwap 关闭”诱导开启；探针捕获HOOK_A11Y_SETTINGS后终止。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳后0.8秒探针：仍停在仿Chrome引导页，无可见文本与遮罩，通知横幅持续诱导为PancakeSwap开权限。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳后2.0秒探针：页面未变且无遮罩，仿Chrome引导与PancakeSwap授权通知仍持续显示。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | 服务详情页仍是仿Chrome引导，含“浏览器更新成功”和三步开启无障碍说明；仅检出乱码令牌，未见遮罩。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 系统警告弹窗(点Deny)探测：界面仍为仿Chrome引导，未捕获弹窗正文；授权通知持续诱导。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 拒权返回2秒后：仍被锁在仿Chrome引导页，CONTINUE与三步无障碍说明持续展示，无法退出，形成诱导闭环。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权返回10.5秒后：仍困在仿Chrome引导页，CONTINUE和三步无障碍说明未消失，持续施压开启权限。 | `step_03_refusal_10500ms_screen.png` |
