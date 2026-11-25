# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:01:51
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`nusku.ermacv2.apk`（静态标签：`malicious` / `Ermac` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `4` 个，有向边 `4` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_A11Y_SETTINGS`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | hooks=`['HOOK_A11Y_SETTINGS']` | overlays=`0` | texts=`Back / Accessibility / Search settings / DOWNLOADED APPS / Ermac-V2 Apk`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `nusku.ermacv2.apk` / `zafewo` | `-` | 13 | 125 / 否 | `click` → [13] Button text="Open Settings" (click) center=(534,15 | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 211 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`nusku.ermacv2.apk/zafewo`)**: `..Accesname..` | `MH1LDiZuzhiYqAAAAAElFTkSuQmCC` | `Accessibility Service` | `DOWNLOADED SERVICES` | `Switch Access` | `OFF` | `TalkBack` | `svg%3E` | `Open Settings`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Ermac-V2 Apk` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用先展示伪造的无障碍服务入口，以“Open Settings”引导进入真系统无障碍设置，并借通知横幅探针监测Enable tag；进入Ermac-V2 Apk服务详情与完全控制警告后，测试选择Deny，应用拒权后仍重新拉起无障碍设置。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Accessibility Service -> 无障碍服务（伪造入口页 step_01）
- Open Settings -> 打开设置（伪造入口页 step_01）
- String (Enable tag) -> 字符串（启用标签）（通知横幅）
- Use Ermac-V2 Apk -> 使用 Ermac-V2 Apk（服务详情页）
- No description provided. -> 未提供描述（服务详情页）
- Allow Ermac-V2 Apk to have full control of your device? -> 允许 Ermac-V2 Apk 完全控制你的设备？（系统警告弹窗）
- Full control is appropriate for apps that help you with accessibility needs, but not for most apps. -> 完全控制适用于辅助无障碍需求的应用，不适用于大多数应用（系统警告弹窗）
- View and control screen -> 查看并控制屏幕（系统警告弹窗）
- It can read all content on the screen and display content over other apps. -> 它可读取屏幕全部内容并覆盖显示在其他应用上（系统警告弹窗）
- View and perform actions -> 查看并执行操作（系统警告弹窗）
- It can track your interactions with an app or a hardware sensor, and interact with apps on your behalf. -> 它可跟踪你与应用或硬件传感器的交互，并代表你操作其他应用（系统警告弹窗）
- Allow -> 允许（系统警告弹窗）
- Deny -> 拒绝（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: zafewo** | 伪造无障碍入口页，按钮“Open Settings”意为“打开设置”；点击后跳转真系统设置，通知为占位字符串。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 真系统无障碍设置页，下载列表出现Ermac-V2 Apk且为Off；通知横幅含Enable tag探针，采集hook后终止。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳后0.8秒探针，仍为真无障碍设置页，无可见文本；Ermac-V2 Apk为Off，Enable tag通知仍在，遮罩0。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳后2.0秒探针，页面仍为真无障碍设置，无可见文本；Ermac-V2 Apk保持Off，Enable tag通知未消失，遮罩0。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | Ermac-V2 Apk服务详情页，英文“Use Ermac-V2 Apk”意为“使用该应用”，快捷方式开关Off且无描述，疑诱导开启。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统警告弹窗，询问是否允许Ermac-V2 Apk完全控制设备，并说明可读屏、覆盖与代操作；含Allow/Deny，选拒绝。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 点Deny拒权后返回无障碍列表，Ermac-V2 Apk仍为Off；应用随即RELAUNCHED_A11Y_SETTINGS，重新拉起无障碍设置。 | `step_02_refusal_2000ms_screen.png` |
