# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:56:49
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.gotbutcv`（静态标签：`malicious` / `Exobot` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.gotbutcv/com.gotbutcv.p037p` | hooks=`[]` | overlays=`0` | texts=`Permission required / Enable permission for BAWAG PSK Security to continue / Continue`
- **Back 后 +5.5s**：`com.gotbutcv/com.gotbutcv.p037p` | hooks=`[]` | overlays=`0` | texts=`Permission required / Enable permission for BAWAG PSK Security to continue / Continue`
- **Back 后 +10.5s**：`com.gotbutcv/com.gotbutcv.p037p` | hooks=`[]` | overlays=`0` | texts=`Permission required / Enable permission for BAWAG PSK Security to continue / Continue`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `RequestIgnoreBatteryOptimizations` | `-` | 4 | 192 / 否 | `click` → [4] Button text="Allow" id=button1 (click) center=(887, | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.gotbutcv` / `p037p` | `-` | 3 | 79 / 否 | `click` → [3] Button text="Continue" id=button1 (click) center=(5 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 217 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/RequestIgnoreBatteryOptimizations`)**: `Let app always run in background?` | `Allowing BAWAG PSK Security to always run in the backgr` | `Deny` | `Allow`
- **Step 2 (`com.gotbutcv/p037p`)**: `Permission required` | `Enable permission for BAWAG PSK Security to continue` | `Continue`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `BAWAG PSK Security` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用伪装为 BAWAG PSK Security，先诱导允许后台常驻并请求权限，再跳转安卓无障碍设置以开启服务；拒权或返回后会反复拉起同一权限诱导弹窗，呈现 Exobot 典型无障碍滥用与循环诱导特征。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 是否允许应用始终在后台运行？（电池优化授权页）
- 英文 -> 允许 BAWAG PSK Security 始终后台运行可能降低续航，可稍后在设置中更改（电池优化授权页）
- 英文 -> 需要权限（应用内权限弹窗）
- 英文 -> 请为 BAWAG PSK Security 启用权限以继续（应用内权限弹窗）
- 英文 -> 继续（应用内权限弹窗按钮）
- 英文 -> 使用 BAWAG PSK Security（无障碍服务详情页）
- 英文 -> 必须启用服务（无障碍服务详情页）
- 英文 -> 字符串（启用服务）/ 字符串（BAWAG PSK Security）（应用通知横幅，疑似占位或本地化缺失）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: RequestIgnoreBatteryOptimi** | 安卓电池优化授权页，以 BAWAG PSK Security 名义请求后台常驻，称允许可能耗电；本步点击 Allow。无通知/遮罩。 | `step_01_action.png` |
| 2 | **Step 2: p037p** | 应用内权限诱导页：英文称需要权限，要求为 BAWAG PSK Security 启用权限后继续；本步点击 Continue，推进至无障碍授权。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 安卓无障碍设置列表，下载应用中 BAWAG PSK Security 显示 Off；采集到无障碍设置 Hook 与探针后自动终止，未继续点开。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转后 0.8 秒探针：仍停留在无障碍设置页，无可见文本、无活动通知、遮罩数为 0，未见额外诱导。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后 2.0 秒探针：无障碍设置页无新增文本与通知，遮罩仍为 0，页面保持静止等待。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | 无障碍服务详情页：显示 Use BAWAG PSK Security 与 Service must be enabled，并有应用通知横幅提示启用服务；本步仅检查详情/警告。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 系统警告/权限弹窗检查页：实际回到应用 p037p 的 Permission required/Continue 诱导弹窗，要求启用权限继续；遮罩为 0。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 拒权/返回后 2 秒：应用再次拉起同一需要权限诱导弹窗（RELAUNCHED_LURE_DIALOG），仅见 Continue，继续要求启用权限。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权/返回后 10.5 秒：仍反复拉起同一权限诱导弹窗，仅见 Continue，无取消/拒绝入口，体现循环骚扰。 | `step_03_refusal_10500ms_screen.png` |
