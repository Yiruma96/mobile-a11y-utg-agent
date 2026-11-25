# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:04:20
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.xhqlob.doscby`（静态标签：`malicious` / `Hqwar` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 1 步，UTG 唯一节点 `4` 个，有向边 `5` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 1 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_01_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing Servis Güncellemesi to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`
- **Back 后 +5.5s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing Servis Güncellemesi to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`
- **Back 后 +10.5s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing Servis Güncellemesi to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 218 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Servis Güncellemesi` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用以“Servis Güncellemesi/服务更新”命名伪装，先引导开启无障碍全权控制，遭拒后转而请求电池优化后台常驻，最终表现为优雅停留/降级，全程无通知横幅与悬浮遮罩。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 土耳其语「Servis Güncellemesi」 -> 中文意译“服务更新”（无障碍列表/服务详情/授权弹窗/电池优化），以正常服务更新名义伪装应用。
- 英语「Use Servis Güncellemesi」 -> 中文意译“使用服务更新”（服务详情页），引导启用该无障碍服务。
- 英语「Allow Servis Güncellemesi to have full control of your device?」 -> 中文意译“允许服务更新完全控制你的设备？”（系统警告弹窗），索取无障碍全权控制。
- 英语「View and control screen / View and perform actions」 -> 中文意译“查看并控制屏幕/查看并执行操作”（系统警告弹窗），说明可读屏、悬浮覆盖和代操作。
- 英语「Let app always run in background?」 -> 中文意译“让应用始终在后台运行？”（电池优化弹窗），拒权后继续索取后台常驻。
- 英语「No description provided.」 -> 中文意译“未提供描述”（服务详情页），无障碍服务缺少用途说明，增加伪装性。

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 无障碍列表页：显示“Servis Güncellemesi（服务更新）”开关为关闭；抓取无障碍设置钩子与探针后自动终止，无通知横幅与遮罩。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳后0.8秒探针：界面仍为无障碍设置页且无可读文本；等待0.8秒，遮罩数0，无通知横幅，未见诱导浮层。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳后2.0秒探针：仍停留在无障碍设置页，界面文本为空；等待2.0秒，遮罩数0且无通知，未出现覆盖层。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 服务详情页：显示“Servis Güncellemesi（服务更新）”启用项、快捷方式与音量键选项，并称未提供描述；本步仅查看详情，无遮罩。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统警告弹窗：询问是否允许“服务更新”完全控制设备，说明可读屏、悬浮覆盖并代操作；提供Allow/Deny，本步检查警告准备拒绝。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒权返回后2秒：转至电池优化弹窗，询问是否让“服务更新”始终后台运行；拒绝后结果为优雅停留/降级，无通知与遮罩。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权返回后10.5秒：仍停在电池优化后台常驻弹窗，含Deny/Allow；拒绝后保持优雅停留/降级，无通知横幅与遮罩。 | `step_01_refusal_10500ms_screen.png` |
