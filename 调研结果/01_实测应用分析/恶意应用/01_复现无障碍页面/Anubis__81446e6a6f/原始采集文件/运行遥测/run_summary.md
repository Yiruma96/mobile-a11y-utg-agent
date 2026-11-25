# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:49:47
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`anubis.bot.myapplication`（静态标签：`malicious` / `Anubis` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `5` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing TikTok to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`
- **Back 后 +5.5s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing TikTok to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`
- **Back 后 +10.5s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing TikTok to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `anubis.bot.myapplication` / `MainActivity` | `-` | 1 | 0 / 是 | `click` → [540, 2100] | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 205 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`anubis.bot.myapplication/MainActivity`)**: (空文本)
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `TikTok` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用先以伪造的 TikTok 页面诱导点击俄语“继续”，再跳转系统无障碍设置引导为 TikTok 开启服务，并出现“完全控制设备”警告；拒权后继续请求后台运行豁免，整体表现为优雅停留或降级。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 俄语 -> “继续”（第1步伪造TikTok页底部蓝色按钮）
- 英语 -> “允许TikTok完全控制你的设备？”并说明可查看和控制屏幕、代你执行操作（系统无障碍授权警告弹窗）
- 英语 -> “让应用始终在后台运行？”并称可能降低续航、稍后可在设置中更改（电池优化豁免请求页）
- 英语 -> “你的数据未备份/立即添加备份账户”（贯穿各页的Google Play服务通知横幅）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 伪造TikTok主页，界面无可见文字；点击底部蓝色俄语“Продолжить（继续）”，顶部有数据未备份通知横幅，无遮罩。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 跳转系统无障碍设置，列表显示已下载应用TikTok为“关闭”；采集到无障碍设置Hook后自动终止，顶部保留备份通知。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳转后0.8秒探针仍停留在无障碍设置页，界面无新增文字、无遮罩，仅见数据未备份通知横幅。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳转后2.0秒探针仍为无障碍设置页，无新增可见文本与遮罩，备份账户通知横幅持续显示。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 进入TikTok无障碍服务详情页，显示“Use TikTok/使用TikTok”及快捷键等选项，说明为“未提供描述”；本步仅检查详情。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统弹窗警告允许TikTok完全控制设备，称可读取屏幕内容、代你操作应用；提供允许/拒绝，本步仅检查未点选。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒权后返回，弹出后台运行请求：允许TikTok始终后台运行可能耗电，可选拒绝/允许；状态为优雅停留或降级。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒权后10.5秒仍停在后台运行请求页，话术称可能降低续航、稍后可改；拒绝/允许按钮仍在，未进一步跳转。 | `step_02_refusal_10500ms_screen.png` |
