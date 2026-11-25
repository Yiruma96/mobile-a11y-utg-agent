# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:34:37
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.example.autoclicker`（静态标签：`malicious` / `AbereBot` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 1 步，UTG 唯一节点 `4` 个，有向边 `5` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 1 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_01_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.example.autoclicker/com.example.autoclicker.MainActivity` | hooks=`[]` | overlays=`0` | texts=``
- **Back 后 +5.5s**：`com.example.autoclicker/com.example.autoclicker.MainActivity` | hooks=`[]` | overlays=`0` | texts=``
- **Back 后 +10.5s**：`com.example.autoclicker/com.example.autoclicker.MainActivity` | hooks=`[]` | overlays=`0` | texts=``

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 211 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Flash Player` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用伪装为“Flash Player”，引导用户在系统无障碍设置中开启完全控制权限；检测到无障碍设置Hook后终止，若用户拒绝授权则返回主界面并平稳停留/降级。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English: “Please allow the app to make it working right.” -> 请允许该应用以便其正常运行（服务详情页）
- English: “Allow Flash Player to have full control of your device?” -> 允许 Flash Player 完全控制您的设备？（系统警告弹窗）
- English: “Full control is appropriate for apps that help you with accessibility needs, but not for most apps.” -> 完全控制适用于辅助无障碍需求的应用，但不适用于大多数应用（系统警告弹窗）
- English: “View and control screen” -> 查看并控制屏幕（系统警告弹窗）
- English: “It can read all content on the screen and display content over other apps.” -> 可读取屏幕全部内容并叠加显示在其他应用上（系统警告弹窗）
- English: “View and perform actions” -> 查看并执行操作（系统警告弹窗）
- English: “It can track your interactions with an app or a hardware sensor, and interact with apps on your behalf.” -> 可跟踪与应用的交互或硬件传感器，并代表您操作应用（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 系统无障碍列表页，已下载应用“Flash Player”显示关闭，无通知与遮罩；捕获无障碍设置Hook后自动终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳转后0.8秒探针仍停在无障碍设置页，界面文本暂未读取，无通知横幅与遮罩，执行等待。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳转后2.0秒探针继续等待无障碍设置页，界面文本暂未读取，无通知横幅与遮罩，遮罩计数为0。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 服务详情页展示“Flash Player”开关与快捷方式设置，并提示“请允许应用以使其正常运行”，诱导开启无障碍服务。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统无障碍授权警告弹窗，称可查看控制屏幕并代操作，提供Allow/Deny；本步点“Deny”拒绝。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒绝授权后返回主界面约2秒，MainActivity无文本、无通知与遮罩，应用平稳停留或降级未崩溃。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒绝授权后约10.5秒仍在主界面，MainActivity无文本、无通知与遮罩，维持平稳停留或降级状态。 | `step_01_refusal_10500ms_screen.png` |
