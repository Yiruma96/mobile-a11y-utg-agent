# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:51:47
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.cable.liar`（静态标签：`malicious` / `Cerberus` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `7` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / -1°C / Cloudy, -1°C / Messages`
- **Back 后 +5.5s**：`com.cable.liar/com.ujirteg.qlowvkvdwx.vjziz.dsxujce` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing Android Güncelleme to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`
- **Back 后 +10.5s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing Android Güncelleme to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.cable.liar` / `dsxujce` | `-` | 1 | 0 / 是 | `click` → [540, 634] | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 217 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.cable.liar/dsxujce`)**: (空文本)
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Android Güncelleme` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用先以 WebView 假“Erişilebilirlik Hizmeti/无障碍服务”教程诱导开启无障碍，随后伪装成“Android Güncelleme/Android 更新”出现在无障碍列表并请求完全控制；用户拒绝后返回桌面，应用又反复弹出后台常驻与电池优化豁免诱导，呈现典型 Cerberus 式权限钓鱼链路。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 土耳其语：Erişilebilirlik Hizmeti -> 中文意译：无障碍服务（Step 1 假指导页）
- 土耳其语：Android Güncelleme -> 中文意译：Android 更新（无障碍列表/服务详情/授权弹窗中的伪装应用名）
- 英语：Use Android Güncelleme -> 中文意译：使用 Android 更新（服务详情页开关/快捷方式）
- 英语：Allow Android Güncelleme to have full control of your device? -> 中文意译：允许 Android 更新完全控制你的设备吗？（系统无障碍授权警告）
- 英语：Full control is appropriate for apps that help you with accessibility needs, but not for most apps. -> 中文意译：完全控制适合辅助无障碍需求的 App，但不适合大多数 App（授权警告说明）
- 英语：View and control screen / It can read all content on the screen and display content over other apps. -> 中文意译：查看并控制屏幕/可读取屏幕全部内容并覆盖显示在其他 App 上（授权权限说明）
- 英语：View and perform actions / It can track your interactions with an app or a hardware sensor, and interact with apps on your behalf. -> 中文意译：查看并执行操作/可追踪与 App 或硬件传感器的交互并代你操作 App（授权权限说明）
- 英语：Let app always run in background? -> 中文意译：允许 App 始终在后台运行吗？（后台常驻诱导弹窗）
- 英语：Allowing Android Güncelleme to always run in the background may reduce battery life. You can change this later from Settings > Apps & notifications. -> 中文意译：允许 Android 更新始终后台运行可能缩短电池续航，可稍后在设置中更改（后台常驻说明）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: dsxujce** | WebView 假“Erişilebilirlik Hizmeti（无障碍服务）”指导页，点击[540,634]继续；无通知横幅与遮罩。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 系统无障碍列表页，伪装项“Android Güncelleme（Android 更新）”显示 Off；检测到设置钩子后终止，探针无通知、无遮罩。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 拒权跳转后 0.8 秒探针，仍停留在系统无障碍列表；无 UI 文本、无通知横幅、遮罩数为 0，仅等待观察。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 拒权跳转后 2.0 秒探针，界面仍为系统无障碍列表；无 UI 文本、无通知横幅、遮罩数为 0，未发生新诱导。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 服务详情页，伪装名“Android Güncelleme（Android 更新）”，含“Use Android Güncelleme（使用 Android 更新）”，快捷方式 Off、无描述；仅检查详情。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统无障碍授权警告，问是否允许“Android Güncelleme（Android 更新）完全控制设备”，列出读屏、代操作等权限，按钮 Allow/Deny；本步仅检查弹窗。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 点 Deny/拒绝后返回桌面启动器，显示应用列表、天气与搜索等；无通知横幅与遮罩，但记录为拒权后重新拉起诱导弹窗。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +5.5s** | 拒权后回到应用假页并弹后台常驻诱导：“Let app always run in background?（允许始终后台运行？）”，称可能耗电，有 Deny/Allow；无遮罩。 | `step_02_refusal_5500ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 再次拒权后跳至系统电池优化豁免页，复用同一后台常驻弹窗：“Let app always run in background?”；有 Deny/Allow，无通知与遮罩。 | `step_02_refusal_10500ms_screen.png` |
