# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:33:02
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`kovvkynlzyyy.dfpn.iablbixbxg`（静态标签：`malicious` / `Anubis` / 静态可见性：`partial_dynamic_or_remote`）
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

> **全链路总结**：应用先打开系统无障碍设置并暴露“Flash Player Service”，进入服务详情诱导开启完全控制；拒绝后转跳到电池优化白名单弹窗继续请求后台常驻，拒绝仅优雅停留/降级，未强退。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English -> 使用 Flash Player 服务（服务详情页）
- English -> 允许 Flash Player 服务完全控制您的设备？（系统无障碍警告弹窗）
- English -> 完全控制适用于辅助无障碍需求的应用，但不适用于大多数应用（系统无障碍警告弹窗）
- English -> 可读取屏幕上的所有内容并显示在其他应用之上（系统无障碍警告弹窗）
- English -> 可跟踪您与应用或硬件传感器的交互，并代表您与应用交互（系统无障碍警告弹窗）
- English -> 允许应用始终在后台运行？（电池优化弹窗）
- English -> 允许 Flash Player 始终后台运行可能缩短电池寿命，可稍后在设置中更改（电池优化弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 无障碍设置列表页：可见“Flash Player Service”处于关闭；本步触发无障碍设置Hook与探针后自动终止，无通知横幅、遮罩0。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳后0.8秒探针：仍停在无障碍设置页，文本为空；无通知横幅、遮罩0，仅等待观察。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳后2.0秒探针：页面仍为无障碍设置且无文本变化；无通知横幅、遮罩0，继续等待。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 服务详情页：展示“Flash Player Service”，有启用开关、音量键快捷方式及“未提供描述”；本步仅查看详情，无通知、遮罩0。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统无障碍授权弹窗：询问是否允许 Flash Player 服务完全控制设备，列明读屏、悬浮显示与代操作风险；本步查看警告，遮罩0。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒权后2.0秒跳至电池优化页：弹窗请求“允许应用始终后台运行”，含拒绝/允许；本步返回拒绝，结果优雅停留或降级。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权后10.5秒：仍停在电池优化后台运行请求弹窗，重复说明耗电影响；本步再次返回拒绝，未强退，遮罩0。 | `step_01_refusal_10500ms_screen.png` |
