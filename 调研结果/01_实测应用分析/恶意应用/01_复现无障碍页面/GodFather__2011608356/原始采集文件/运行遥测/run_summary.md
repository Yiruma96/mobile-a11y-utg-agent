# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T16:01:20
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.melting.mantaught`（静态标签：`malicious` / `GodFather` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `4` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.melting.mantaught/com.melting.mantaught.arcuses` | hooks=`[]` | overlays=`0` | texts=`e / Please grant the permission shown above for the application to run. / ALLOW`
- **Back 后 +5.5s**：`com.melting.mantaught/com.melting.mantaught.arcuses` | hooks=`[]` | overlays=`0` | texts=`e / Please grant the permission shown above for the application to run. / ALLOW`
- **Back 后 +10.5s**：`com.melting.mantaught/com.melting.mantaught.arcuses` | hooks=`[]` | overlays=`0` | texts=`e / Please grant the permission shown above for the application to run. / ALLOW`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.melting.mantaught` / `arcuses` | `-` | 3 | 73 / 否 | `click` → [3] Button text="ALLOW" id=button (click) center=(540,2 | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 205 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.melting.mantaught/arcuses`)**: `e` | `Please grant the permission shown above for the applica` | `ALLOW`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Chrome` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用以伪装成 Play Store/Chrome 的权限引导页诱导用户授予无障碍权限；点击 ALLOW 后跳转系统无障碍设置，若用户拒绝则返回原诱导页并反复重新拉起同一弹窗与通知催促。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Please grant the permission shown above for the application to run. -> 请授予上方所示权限以便应用运行（入口 arcuses 诱导页）
- ALLOW -> 允许（入口诱导按钮）
- Please grant accessibility permission to use the application. -> 请授予无障碍权限以使用应用（拒权返回后的 Chrome 通知）
- Allow Chrome to have full control of your device? -> 允许 Chrome 完全控制你的设备？（系统授权警告页）
- Full control is appropriate for apps that help you with accessibility needs, but not for most apps. -> 完全控制适合辅助无障碍需求的应用，但多数应用不适合（系统授权警告页）
- View and control screen; It can read all content on the screen and display content over other apps. -> 查看并控制屏幕：可读取屏幕全部内容并覆盖显示在其他应用上（系统授权警告页）
- View and perform actions; It can track your interactions with an app or a hardware sensor, and interact with apps on your behalf. -> 查看并执行操作：可跟踪交互并代表你操作应用（系统授权警告页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: arcuses** | 入口 arcuses 伪装 Play Store 引导页：提示请授予上方权限以便运行，点击 ALLOW 触发无障碍设置；通知横幅为 Play Store，遮罩 0。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 系统无障碍设置列表：显示 Chrome Off 等应用项；命中 A11Y 设置钩子与探针后自动终止，尚未授权，Play Store 通知仍在，遮罩 0。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳转后 0.8 秒探针：仍停留在无障碍设置列表，无可读文本；未检测到悬浮遮罩，Play Store 通知横幅仍显示，仅等待。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳转后 2.0 秒探针：页面仍为无障碍设置列表且无文本，悬浮遮罩为 0；Play Store 通知继续存在，仅等待，无交互。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | Chrome 无障碍服务详情页：显示“Use Chrome”、快捷键关闭、“未提供描述”；本步仅检查详情，未授权，遮罩 0。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统高危警告弹窗：询问是否允许 Chrome 完全控制设备，说明可读屏、覆盖与代操作；含允许/拒绝，本步仅检查未授权，遮罩 0。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒权返回 arcuses 诱导页并重拉同一弹窗；Chrome 通知催促“请授予无障碍权限以使用应用”，Play Store 通知仍在，遮罩 0。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒权返回+10.5 秒仍停 arcuses 诱导页并再次拉起弹窗；Chrome 催促通知已消失，仅剩 Play Store 空通知，遮罩 0。 | `step_02_refusal_10500ms_screen.png` |
