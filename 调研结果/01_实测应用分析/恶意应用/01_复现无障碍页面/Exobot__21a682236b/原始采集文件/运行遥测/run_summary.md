# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:44:15
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.darklittler`（静态标签：`malicious` / `Exobot` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.darklittler/com.darklittler.p089t` | hooks=`[]` | overlays=`0` | texts=`Permission required / Enable permission for BAWAG PSK Security to continue / Continue`
- **Back 后 +5.5s**：`com.darklittler/com.darklittler.p089t` | hooks=`[]` | overlays=`0` | texts=`Permission required / Enable permission for BAWAG PSK Security to continue / Continue`
- **Back 后 +10.5s**：`com.darklittler/com.darklittler.p089t` | hooks=`[]` | overlays=`0` | texts=`Permission required / Enable permission for BAWAG PSK Security to continue / Continue`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `RequestIgnoreBatteryOptimizations` | `-` | 4 | 192 / 否 | `click` → [4] Button text="Allow" id=button1 (click) center=(887, | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.darklittler` / `p089t` | `-` | 3 | 79 / 否 | `click` → [3] Button text="Continue" id=button1 (click) center=(5 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 217 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/RequestIgnoreBatteryOptimizations`)**: `Let app always run in background?` | `Allowing BAWAG PSK Security to always run in the backgr` | `Deny` | `Allow`
- **Step 2 (`com.darklittler/p089t`)**: `Permission required` | `Enable permission for BAWAG PSK Security to continue` | `Continue`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `BAWAG PSK Security` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用伪装为 BAWAG PSK Security，先诱导允许后台常驻，再以“需要权限”弹窗连至无障碍设置并尝试启用服务；拒权后反复重弹同一诱导弹窗（RELAUNCHED_LURE_DIALOG），呈 Exobot 权限滥用链。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文“Let app always run in background?” -> 中文意译：让应用始终在后台运行？（Step 1 电池优化请求页）
- 英文“Allowing BAWAG PSK Security to always run in the background may reduce battery life. You can change this later from Settings > Apps & notifications.” -> 中文意译：允许 BAWAG PSK Security 始终后台运行可能降低续航，之后可在设置>应用与通知中更改。（Step 1）
- 英文“Permission required” -> 中文意译：需要权限（Step 2、服务详情及拒权重弹页）
- 英文“Enable permission for BAWAG PSK Security to continue” -> 中文意译：请为 BAWAG PSK Security 启用权限以继续（Step 2、服务详情及拒权重弹页）
- 英文“Continue” -> 中文意译：继续（Step 2 及拒权重弹页）
- 英文“Use BAWAG PSK Security” -> 中文意译：使用 BAWAG PSK Security（无障碍服务详情页）
- 英文“Service must be enabled.” -> 中文意译：必须启用服务（无障碍服务详情页）
- 英文通知“String (Enable service)”/“String (BAWAG PSK Security)” -> 中文意译：占位字符串（启用服务）/（BAWAG PSK Security）（服务详情页通知横幅）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: RequestIgnoreBatteryOptimi** | 系统电池优化请求页，英文提示让应用始终后台运行并称可稍后更改；点击“Allow/允许”推进引导。 | `step_01_action.png` |
| 2 | **Step 2: p089t** | 应用内“需要权限”弹窗，英文要求为 BAWAG PSK Security 启用权限以继续；点击“Continue/继续”前往无障碍提示。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 系统无障碍设置页，列表显示 BAWAG PSK Security 为“Off/关闭”；触发无障碍设置钩子与探针后自动终止。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转后0.8秒探针仍停留在无障碍设置页，界面文本为空、无通知与遮罩，仅等待观察。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后2.0秒探针仍在无障碍设置页，无界面文本、通知或悬浮遮罩，等待无新增动作。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | 无障碍服务详情页，显示“使用该服务”及“必须启用服务”，通知横幅含占位字符串“Enable service”；仅作检查。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 应用内“需要权限”弹窗，要求为 BAWAG PSK Security 启用权限以继续；仅检查，遮罩为0。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 拒权返回2秒后仍弹“需要权限”诱导页，显示“Continue/继续”，记录 RELAUNCHED_LURE_DIALOG 重复诱导。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权返回10.5秒后同一诱导弹窗再现，仍要求继续授权，状态 RELAUNCHED_LURE_DIALOG，无遮罩通知。 | `step_03_refusal_10500ms_screen.png` |
