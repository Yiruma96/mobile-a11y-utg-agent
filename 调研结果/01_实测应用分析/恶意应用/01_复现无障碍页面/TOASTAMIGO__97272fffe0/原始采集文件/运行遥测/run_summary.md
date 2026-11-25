# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:05:23
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.goami.applocker`（静态标签：`malicious` / `TOASTAMIGO` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `4` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.goami.applocker/com.goami.applocker.AppLocker.ApplicationListActivity` | hooks=`[]` | overlays=`0` | texts=`Attention / This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it. / Cancel / Confirm`
- **Back 后 +5.5s**：`com.goami.applocker/com.goami.applocker.AppLocker.ApplicationListActivity` | hooks=`[]` | overlays=`0` | texts=`Attention / This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it. / Cancel / Confirm`
- **Back 后 +10.5s**：`com.goami.applocker/com.goami.applocker.AppLocker.ApplicationListActivity` | hooks=`[]` | overlays=`0` | texts=`Attention / This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it. / Cancel / Confirm`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.goami.applocker` / `ApplicationListActivity` | `-` | 4 | 130 / 否 | `click` → [4] TextView text="Confirm" id=btn_ok (click) center=(8 | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 214 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.goami.applocker/ApplicationListActivity`)**: `Attention` | `This device version is above Android 4.0.3 .Please Go S` | `Cancel` | `Confirm`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Smart AppLocker` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：AppLocker入口页以“Android 4.0.3以上需开启无障碍服务”为由弹窗，引导用户进入系统无障碍并开启Smart AppLocker；在系统高危授权警告处拒绝后，应用返回列表页并持续重复同一诱导弹窗（RELAUNCHED_LURE_DIALOG）。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English -> 注意：本设备版本高于Android 4.0.3，请前往设置→无障碍→App Locker并开启它（Step 1/拒权返回弹窗）
- English -> 使用Smart AppLocker；Smart AppLocker快捷方式；长按音量键；快捷方式设置（服务详情页）
- English -> 该服务用于在Android 4.0.3及以上轻松锁定应用（服务详情页说明）
- English -> 允许Smart AppLocker完全控制你的设备？完全控制适用于帮助无障碍需求的应用，但不适合大多数应用；可查看并控制屏幕、读取屏幕全部内容并覆盖其他应用、跟踪交互并代为操作（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ApplicationListActivity** | 应用列表页弹出Attention提示，称设备高于Android 4.0.3需去设置无障碍开启App Locker；点击Confirm，通知栏显示AppLocker服务运行。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 进入系统无障碍列表，DOWNLOADED APPS下Smart AppLocker显示Off；采集无障碍设置钩子后自动终止，通知栏仍显示服务运行。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳转后0.8秒探针停在无障碍设置页，UI文本为空、无遮罩；仅见AppLocker服务运行通知，未发生点击。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳转后2.0秒仍在无障碍设置页，无新增界面文本与遮罩；探针等待结束，通知栏AppLocker服务继续运行。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 服务详情页显示Smart AppLocker及Use Smart AppLocker开关，含快捷方式、音量键选项和适配Android 4.0.3说明；本步仅检查详情。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统高危授权警告：允许Smart AppLocker完全控制设备，可查看屏幕、读取内容并代操作；含Allow/Deny，本步查看警告未授权。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒权返回2秒后，应用列表页再次弹出同一Attention引导弹窗，Cancel/Confirm仍在，触发重复诱导RELAUNCHED_LURE_DIALOG。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒权返回10.5秒后仍停留应用列表页，Attention弹窗持续重复出现，Cancel/Confirm可操作，诱导未停止。 | `step_02_refusal_10500ms_screen.png` |
