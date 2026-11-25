# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:06:09
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`p1a1fa04c.pae25061e.p658c02c8`（静态标签：`malicious` / `BingoMod` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`p1a1fa04c.pae25061e.p658c02c8/p1a1fa04c.pae25061e.p658c02c8.p055ff792` | hooks=`[]` | overlays=`0` | texts=`AnroidRAA / Image 2 / Per abilitare correttamente l'app è necessario consentire tutti i permessi. Clicca sul pulsante "Prosegui" in basso per continuare. / Prosegui`
- **Back 后 +5.5s**：`p1a1fa04c.pae25061e.p658c02c8/p1a1fa04c.pae25061e.p658c02c8.p055ff792` | hooks=`[]` | overlays=`0` | texts=`AnroidRAA / Image 2 / Per abilitare correttamente l'app è necessario consentire tutti i permessi. Clicca sul pulsante "Prosegui" in basso per continuare. / Prosegui`
- **Back 后 +10.5s**：`p1a1fa04c.pae25061e.p658c02c8/p1a1fa04c.pae25061e.p658c02c8.p055ff792` | hooks=`[]` | overlays=`0` | texts=`AnroidRAA / Image 2 / Per abilitare correttamente l'app è necessario consentire tutti i permessi. Clicca sul pulsante "Prosegui" in basso per continuare. / Prosegui`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `p1a1fa04c.pae25061e.p658c02c8` / `p055ff792` | `-` | 1 | 0 / 是 | `click` → [540, 1747] | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `p1a1fa04c.pae25061e.p658c02c8` / `p055ff792` | `-` | 4 | 155 / 否 | `click` → [4] Button text="Prosegui" (click) center=(540,2018) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 208 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`p1a1fa04c.pae25061e.p658c02c8/p055ff792`)**: (空文本)
- **Step 2 (`p1a1fa04c.pae25061e.p658c02c8/p055ff792`)**: `AnroidRAA` | `Image 2` | `Per abilitare correttamente l'app è necessario consenti` | `Prosegui`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Scudo App` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用从全屏WebView意大利语盾牌权限诱导页起步，以“须授予全部权限”话术引导点击Prosegui，并跳转系统无障碍设置为Scudo App开启服务；在系统高风险警告点Deny返回后，应用仍反复停留在原诱导页，无取消/退出，最终TRAPPED_ON_LURE_SCREEN。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 意大利语 -> “为正确启用应用，必须授予所有权限；点击下方‘Prosegui（继续）’按钮以继续。”（step_02 与拒权返回+2.0s/+10.5s 诱导页）
- 英语 -> “允许Scudo App完全控制你的设备？完全控制适合有辅助无障碍需求的App，但不适合大多数App；可查看并控制屏幕、查看并执行操作。”（系统警告弹窗，点Deny）
- 英语 -> “使用Scudo App”启用无障碍服务，且“未提供描述”。（Scudo App 服务详情页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: p055ff792** | 应用启动即进入全屏WebView，展示意大利语盾牌权限诱导页；本步点击(540,1747)，无文字、通知或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: p055ff792** | 权限诱导页显示意大利语：须授予全部权限并点“Prosegui”（继续）；本步点击底部按钮中心(540,2018)。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 跳转系统无障碍设置，列表显示“Scudo App”为Off；截获HOOK_A11Y_SETTINGS后自动终止，无通知/遮罩。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转后0.8秒探针，仍停在无障碍设置页；无可见文字、通知或遮罩，仅等待观察页面稳定性。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后2.0秒探针，仍为无障碍设置页；无文字、通知与遮罩，等待未触发额外页面或提示。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | 进入Scudo App服务详情页，含“Use Scudo App”启用项与快捷键；描述为No description provided，未见警告。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 系统高风险授权弹窗：询问是否允许Scudo App完全控制设备，列明读屏、覆盖显示与代操作；本步检查后点Deny。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 拒权返回2秒后仍被扣在意大利语权限诱导页，要求授予全部权限并点“Prosegui”；无取消/退出，形成诱骗闭环。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权返回10.5秒仍停留同一意大利语诱骗页，持续要求全部权限并点“Prosegui”；无退出路径，判定困于诱导屏。 | `step_03_refusal_10500ms_screen.png` |
