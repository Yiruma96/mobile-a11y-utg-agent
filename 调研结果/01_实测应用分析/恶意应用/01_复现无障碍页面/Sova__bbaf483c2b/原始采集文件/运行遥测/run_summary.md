# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:59:49
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.crop.horse`（静态标签：`malicious` / `Sova` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `4` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.crop.horse/by.onliner.catalog.ui.AccessibilityGuideActivity` | hooks=`[]` | overlays=`0` | texts=`Wygl+xJEYdDFjVZQcA70jRRwdWBz9NJ1pUHxOBqyjUsO53LDR6xr7sNeSjeamf3Wuo+UjgTjTGmM0Y2l4SJFHiV6GnElFMs0oOsSTEyMD3FuDnSlUHibn6aTbOh8Ab4FknEMy+MYB+o0j5pkSsgHsch+FOLTmUz024wy8pbezzegpxqcSiep3CGLlNf2 / Welcome to Chrome / Browser updated successfully / To use this application, click the "Continue" button and then enable Chrome services. / 1Open settings`
- **Back 后 +5.5s**：`com.crop.horse/by.onliner.catalog.ui.AccessibilityGuideActivity` | hooks=`[]` | overlays=`0` | texts=`Wygl+xJEYdDFjVZQcA70jRRwdWBz9NJ1pUHxOBqyjUsO53LDR6xr7sNeSjeamf3Wuo+UjgTjTGmM0Y2l4SJFHiV6GnElFMs0oOsSTEyMD3FuDnSlUHibn6aTbOh8Ab4FknEMy+MYB+o0j5pkSsgHsch+FOLTmUz024wy8pbezzegpxqcSiep3CGLlNf2 / Welcome to Chrome / Browser updated successfully / To use this application, click the "Continue" button and then enable Chrome services. / 1Open settings`
- **Back 后 +10.5s**：`com.crop.horse/by.onliner.catalog.ui.AccessibilityGuideActivity` | hooks=`[]` | overlays=`0` | texts=`Wygl+xJEYdDFjVZQcA70jRRwdWBz9NJ1pUHxOBqyjUsO53LDR6xr7sNeSjeamf3Wuo+UjgTjTGmM0Y2l4SJFHiV6GnElFMs0oOsSTEyMD3FuDnSlUHibn6aTbOh8Ab4FknEMy+MYB+o0j5pkSsgHsch+FOLTmUz024wy8pbezzegpxqcSiep3CGLlNf2 / Welcome to Chrome / Browser updated successfully / To use this application, click the "Continue" button and then enable Chrome services. / 1Open settings`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.crop.horse` / `AccessibilityGuideActivity` | `-` | 1 | 0 / 是 | `click` → [540, 1747] | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 205 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.crop.horse/AccessibilityGuideActivity`)**: (空文本)
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Chrome` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用以伪装“Chrome更新成功”的WebView欢迎页诱导点击CONTINUE，跳转系统无障碍并将Chrome显示为Off；触发无障碍设置钩子/探针后返回仍被锁在诱导页，拒权无法脱离且通知持续要求为Chrome启用访问。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 更新应用访问权限/为“Chrome”启用访问（通知横幅，全程持续）
- 英文 -> 欢迎使用Chrome/浏览器已成功更新（诱导页及拒权返回页）
- 英文 -> 要使用本应用，请点击“继续”按钮并启用Chrome服务（诱导页）
- 英文 -> 1打开设置 2选择无障碍 3滑动开关启用（诱导页三步指引）
- 英文 -> 继续（诱导页CONTINUE按钮）
- 英文 -> 使用Chrome/Chrome快捷方式关闭/服务允许Android无障碍扫描设备无障碍问题（服务详情页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: AccessibilityGuideActivity** | 入口为伪装“Chrome更新成功”的WebView欢迎页，含CONTINUE按钮；通知横幅提示“为Chrome启用访问”，点击后跳系统无障碍。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 系统无障碍列表页显示Chrome为Off；应用触发无障碍设置钩子与探针后自动终止，通知仍提示为Chrome启用访问。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳转后0.8s仍停在无障碍设置页，无可见文案与遮罩；通知持续显示“更新应用访问/为Chrome启用访问”。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳转后2.0s仍停在无障碍设置页，无文案、无遮罩；通知横幅继续要求为Chrome启用访问，页面无进一步动作。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 进入Chrome无障碍服务详情页，显示Use Chrome、Chrome快捷方式Off及无障碍扫描说明；执行检查详情/警告，未见授权。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 自称系统警告但实际仍为com.crop.horse诱导页，含加密串、Chrome更新成功、三步开启指引与CONTINUE；遮罩为0。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒权返回后2s仍被困在伪装Chrome更新成功页，三步指引与CONTINUE仍在，通知持续；无退出路径。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒权返回后10.5s仍锁定同一诱导页，Chrome更新成功与CONTINUE话术未变，通知持续要求启用访问。 | `step_02_refusal_10500ms_screen.png` |
