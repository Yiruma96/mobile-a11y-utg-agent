# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:16:33
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`abywinv.yoamhjbrsdsxshkt.zxenmspvja`（静态标签：`malicious` / `BankBot` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`hook_captured`（共执行 1 步，UTG 唯一节点 `4` 个，有向边 `5` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 1 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_01_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing Flash Player to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`
- **Back 后 +5.5s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing Flash Player to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`
- **Back 后 +10.5s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing Flash Player to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 219 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Flash Player Service` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用以「Flash Player Service」伪装名称将自身植入系统无障碍服务列表，随后进入服务详情页并弹出要求「完全控制设备」的无障碍授权警告；研究员点 Deny 拒绝后，样本未崩溃而是转向「后台常驻运行」的电池优化豁免弹窗继续索取权限，全程无遮罩、仅伴随系统备份提醒通知，属渐进式诱导授权链路，被拒不崩（GRACEFUL_STAY_OR_DEGRADE）。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English -> 「Flash Player Service」（无障碍服务列表/详情页）——冒充知名播放器组件名，掩盖其为第三方可疑应用的身份
- English -> 「Use Flash Player Service」（服务详情页）——以播放器功能为名引导开启无障碍服务
- English -> 「No description provided.」（服务详情页）——刻意留空服务说明，规避用户识别风险
- English -> 「Allow Flash Player Service to have full control of your device?」（系统警告弹窗）——直接索要设备完全控制权
- English -> 「View and control screen / It can read all content on the screen and display content over other apps.」（系统警告弹窗）——即捕获屏幕与悬浮窗覆盖能力，正是银行木马所需
- English -> 「View and perform actions / It can track your interactions with an app or a hardware sensor, and interact with apps on your behalf.」（系统警告弹窗）——即代用户点击与监听，可用于自动转账
- English -> 「Let app always run in background? / Allowing Flash Player to always run in the background may reduce battery life.」（电池优化豁免弹窗）——拒权后改索后台常驻，维持远控存活

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 系统无障碍设置页，列表出现可疑项「Flash Player Service」且状态为 Off；页面仅有返回与搜索，无取消或退出入口，采集到无障碍 Hook 与探针后自动终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳转后 0.8 秒探针，仍停留在无障碍设置页但界面文本已抓取为空，遮罩数为 0，无新增弹窗，说明页面处于短暂重载/空白过渡态。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳转后 2.0 秒探针，页面与文本依旧为空、遮罩为 0，确认应用未在此期间弹出任何诱导浮层，仍等待用户手动点击列表项。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 「Flash Player Service」服务详情页，含「Use Flash Player Service」开关与快捷键选项，说明栏写「No description provided.」刻意留空，引导用户开启无障碍服务。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统无障碍授权警告弹窗，明示将获得「完全控制设备」、读取屏幕全部内容并可覆盖显示、代用户执行操作；仅 Allow/Deny 两键，本步选择 Deny 拒绝。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒绝无障碍后 2 秒，弹出电池优化豁免页「Let app always run in background?」，以降低续航为提示索要后台常驻；选择 Deny 后样本未崩溃而降级停留。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒绝 10.5 秒后同一电池优化豁免弹窗仍在，界面文本未变化、无遮罩覆盖，表明应用在二次拒权后保持静默等待而非退出，属平稳降级行为。 | `step_01_refusal_10500ms_screen.png` |
