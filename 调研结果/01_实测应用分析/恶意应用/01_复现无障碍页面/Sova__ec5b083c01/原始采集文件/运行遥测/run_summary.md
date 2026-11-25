# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:32:32
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.royal.bottom`（静态标签：`malicious` / `Sova` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `4` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.royal.bottom/com.tapston.burgerking.ui.AccessibilityGuideActivity` | hooks=`[]` | overlays=`0` | texts=`Wygl+xJEYdDFjVZQcA70jRRwdWBz9NJ1pUHxOBqyjUsO53LDR6xr7sNeSjeamf3Wuo+UjgTjTGmM0Y2l4SJFHiV6GnElFMs0oOsSTEyMD3FuDnSlUHibn6aTbOh8Ab4FknEMy+MYB+o0j5pkSsgHsch+FOLTmUz024wy8pbezzegpxqcSiep3CGLlNf2 / Welcome to Chrome / Browser updated successfully / To use this application, click the "Continue" button and then enable Chrome services. / 1Open settings`
- **Back 后 +5.5s**：`com.royal.bottom/com.tapston.burgerking.ui.AccessibilityGuideActivity` | hooks=`[]` | overlays=`0` | texts=`Wygl+xJEYdDFjVZQcA70jRRwdWBz9NJ1pUHxOBqyjUsO53LDR6xr7sNeSjeamf3Wuo+UjgTjTGmM0Y2l4SJFHiV6GnElFMs0oOsSTEyMD3FuDnSlUHibn6aTbOh8Ab4FknEMy+MYB+o0j5pkSsgHsch+FOLTmUz024wy8pbezzegpxqcSiep3CGLlNf2 / Welcome to Chrome / Browser updated successfully / To use this application, click the "Continue" button and then enable Chrome services. / 1Open settings`
- **Back 后 +10.5s**：`com.royal.bottom/com.tapston.burgerking.ui.AccessibilityGuideActivity` | hooks=`[]` | overlays=`0` | texts=`Wygl+xJEYdDFjVZQcA70jRRwdWBz9NJ1pUHxOBqyjUsO53LDR6xr7sNeSjeamf3Wuo+UjgTjTGmM0Y2l4SJFHiV6GnElFMs0oOsSTEyMD3FuDnSlUHibn6aTbOh8Ab4FknEMy+MYB+o0j5pkSsgHsch+FOLTmUz024wy8pbezzegpxqcSiep3CGLlNf2 / Welcome to Chrome / Browser updated successfully / To use this application, click the "Continue" button and then enable Chrome services. / 1Open settings`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.royal.bottom` / `AccessibilityGuideActivity` | `-` | 1 | 0 / 是 | `click` → [551, 1719] | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 214 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.royal.bottom/AccessibilityGuideActivity`)**: (空文本)
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Tinder Platinum` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用 com.royal.bottom 先展示伪装 Chrome 更新的无障碍引导页，并以「Tinder Platinum」通知催促开启服务；跳转系统无障碍列表/详情页后若拒绝授权，会反复回到同一诱导页并卡死（TRAPPED_ON_LURE_SCREEN），全程无明显取消出口。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> “欢迎使用 Chrome”（AccessibilityGuideActivity 伪装引导页）
- 英语 -> “浏览器更新成功”（AccessibilityGuideActivity 伪装引导页）
- 英语 -> “要使用本应用，请点击 Continue 按钮，然后启用 Chrome 服务”（AccessibilityGuideActivity 伪装引导页）
- 英语 -> “1 打开设置；2 选择无障碍；3 滑动开关以启用”（AccessibilityGuideActivity 三步诱导说明）
- 英语 -> “继续 / CONTINUE”（AccessibilityGuideActivity 按钮）
- 英语 -> “更新应用访问权限 / 为 Tinder Platinum 启用访问”（通知横幅，催促授权）
- 英语 -> “使用 Tinder Platinum / 服务允许 Accessibility for Android 扫描设备无障碍问题”（服务详情页，弱化权限风险）
- 英语 -> “Tinder Platinum 快捷方式 关闭”（服务详情页选项，显示服务已注册）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: AccessibilityGuideActivity** | 伪装 Chrome 引导页首次出现，含 CONTINUE 按钮；通知横幅显示“更新应用访问权限/为 Tinder Platinum 启用访问”，本步点击 CONTINUE，尚无遮罩。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 跳至系统无障碍列表页，DOWNLOADED APPS 下可见 Tinder Platinum 为 Off；通知仍催促启用，本步因捕获无障碍设置钩子自动终止。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳后 0.8 秒仍停系统无障碍列表，界面文本为空，Tinder Platinum 通知横幅持续；探针显示 overlays=0，未出现遮罩。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳后 2.0 秒仍停无障碍列表，页面无文本，通知横幅持续显示启用 Tinder Platinum；探针 overlays=0，无遮罩或弹窗。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 进入 Tinder Platinum 服务详情页，含“使用 Tinder Platinum”、快捷方式 Off 与扫描无障碍问题说明；本步仅检查详情/警告，未授权。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 标题标注系统警告弹窗(点Deny)，实际显示伪装 Chrome 页：欢迎使用、更新成功、三步开启与 CONTINUE；检查详情，overlays=0，无真实系统警告文案。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒绝授权返回 2 秒后仍被锁在同一伪装 Chrome 页，通知横幅继续要求为 Tinder Platinum 开启访问；无取消键，结果为 TRAPPED_ON_LURE_SCREEN。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒绝授权返回 10.5 秒后页面无变化，仍显示 Chrome 更新成功、三步开启与 CONTINUE，通知横幅持续；仍卡死在诱导页，无退出路径。 | `step_02_refusal_10500ms_screen.png` |
