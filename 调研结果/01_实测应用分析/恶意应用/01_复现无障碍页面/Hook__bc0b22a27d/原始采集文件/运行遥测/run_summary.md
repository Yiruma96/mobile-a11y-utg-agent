# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:48:12
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.fisececitinoje.lalole`（静态标签：`malicious` / `Hook` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`hook_captured`（共执行 1 步，UTG 唯一节点 `3` 个，有向边 `3` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_A11Y_SETTINGS`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 1 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_01_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | hooks=`['HOOK_A11Y_SETTINGS']` | overlays=`0` | texts=`Back / Accessibility / Search settings / DOWNLOADED APPS / BBVA4`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 204 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `BBVA4` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用以「BBVA4」无障碍服务名义，通过持续通知引导用户进入系统无障碍设置并打开服务详情，展示授权说明与系统全权控制警告；用户拒绝后应用会重新拉起无障碍设置页，呈现反复诱导授权特征。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Enable BBVA4（通知横幅） -> 启用 BBVA4（无障碍列表页及跳后探针）
- Use BBVA4（服务详情页） -> 使用 BBVA4（服务详情页）
- If accessibility permission has been on, please turn off then turn on.（服务详情页） -> 若无障碍权限曾开启，请先关闭再开启（服务详情页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 无障碍列表页：下载应用区BBVA4显示关闭，通知横幅提示Enable BBVA4（启用）；捕获设置Hook与探针后终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳后0.8秒探针：仍停留在无障碍列表页，界面文本为空，遮罩为0；通知横幅持续显示启用BBVA4诱导文案。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳后2.0秒探针：无障碍列表页无可见文本、无遮罩，应用通知仍提示Enable BBVA4（启用BBVA4），未发生跳转。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 服务详情页：展示BBVA4、Use BBVA4（使用）及快捷键选项；提示若权限曾开启需先关再开，通知横幅仍在。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统授权警告：询问是否允许BBVA4完全控制设备，列明可查看屏幕、执行操作；提供Allow/Deny，本步查看未授权。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒权返回：点Deny后回到无障碍列表，BBVA4仍为Off（关闭）；应用随即重新拉起无障碍设置页，呈现反复诱导。 | `step_01_refusal_2000ms_screen.png` |
