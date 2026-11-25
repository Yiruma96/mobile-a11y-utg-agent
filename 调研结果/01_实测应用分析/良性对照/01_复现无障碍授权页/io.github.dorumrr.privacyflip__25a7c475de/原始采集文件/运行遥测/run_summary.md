# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:28:32
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`io.github.dorumrr.privacyflip`（静态标签：`benign` / `隐私指示与安全防护工具` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 7 步，UTG 唯一节点 `9` 个，有向边 `11` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 7 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_07_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`io.github.dorumrr.privacyflip/io.github.dorumrr.privacyflip.MainActivity` | hooks=`[]` | overlays=`0` | texts=`⚙️ Manage App Exemptions / Delays / Configure timing for privacy actions / Delay after Lock (sec) / 10s`
- **Back 后 +5.5s**：`io.github.dorumrr.privacyflip/io.github.dorumrr.privacyflip.MainActivity` | hooks=`[]` | overlays=`0` | texts=`⚙️ Manage App Exemptions / Delays / Configure timing for privacy actions / Delay after Lock (sec) / 10s`
- **Back 后 +10.5s**：`io.github.dorumrr.privacyflip/io.github.dorumrr.privacyflip.MainActivity` | hooks=`[]` | overlays=`0` | texts=`⚙️ Manage App Exemptions / Delays / Configure timing for privacy actions / Delay after Lock (sec) / 10s`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `io.github.dorumrr.privacyflip` / `MainActivity` | `-` | 28 | 787 / 否 | `swipe` → [540, 1800] | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `io.github.dorumrr.privacyflip` / `MainActivity` | `-` | 41 | 322 / 否 | `swipe` → [540, 1900] | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `io.github.dorumrr.privacyflip` / `MainActivity` | `-` | 37 | 429 / 否 | `swipe` → [540, 1900] | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `io.github.dorumrr.privacyflip` / `MainActivity` | `-` | 26 | 382 / 否 | `swipe` → [540, 1900] | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `io.github.dorumrr.privacyflip` / `MainActivity` | `-` | 21 | 626 / 否 | `click` → [18] Switch id=accessibilityServiceSwitch (click,unchec | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `io.github.dorumrr.privacyflip` / `MainActivity` | `-` | 21 | 592 / 否 | `click` → [20] Button text="OPEN ACCESSIBILITY SETTINGS" id=openA | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 235 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_07_layout.xml` + `step_07_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`io.github.dorumrr.privacyflip/MainActivity`)**: `System Requirements` | `Required for privacy control functionality` | `Privileged Access` | `Root Available` | `Privacy Flip could not confirm root access. Open Magisk` | `CHECK AGAIN` | `Battery Optimization` | `Optimization enabled` | `Disable battery optimization for reliable background op` | `OPEN BATTERY SETTINGS`
- **Step 2 (`io.github.dorumrr.privacyflip/MainActivity`)**: `Wi-Fi` | `Disable on lock` | `Only if not connected` | `Enable on unlock` | `Only if not already enabled` | `Bluetooth` | `Mobile Data` | `Only if no media is playing` | `Location (experimental)` | `Only if not in use`
- **Step 3 (`io.github.dorumrr.privacyflip/MainActivity`)**: `Enable on unlock` | `NFC Auto-Retry` | `If NFC turns itself back on right after this app turns ` | `Camera` | `Disable on lock` | `Needs Android 12 or newer. Your Android version has no ` | `Microphone` | `Only if not in use` | `Extras` | `Additional protection`
- **Step 4 (`io.github.dorumrr.privacyflip/MainActivity`)**: `Disable on unlock` | `Battery Saver` | `Enable on lock` | `⚙️ Manage App Exemptions` | `Delays` | `Configure timing for privacy actions` | `Delay after Lock (sec)` | `10s` | `Delay after Unlock (sec)` | `1s`
- **Step 5 (`io.github.dorumrr.privacyflip/MainActivity`)**: `⚙️ Manage App Exemptions` | `Delays` | `Configure timing for privacy actions` | `Delay after Lock (sec)` | `10s` | `Delay after Unlock (sec)` | `1s` | `Debug Notifications` | `Show notifications for privacy actions` | `Debug Logs`
- **Step 6 (`io.github.dorumrr.privacyflip/MainActivity`)**: `⚙️ Manage App Exemptions` | `Delays` | `Configure timing for privacy actions` | `Delay after Lock (sec)` | `10s` | `Delay after Unlock (sec)` | `1s` | `Debug Notifications` | `Show notifications for privacy actions` | `Debug Logs`
- **Step 7 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Privacy Flip - Lock Screen Detection` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用入口为主界面，先以系统要求、Root授权和电池优化提示铺垫，再滚动展示锁屏/解锁隐私开关，最终用“锁屏检测（实验）”引导开启无障碍服务并弹出系统“完全控制”警告；选择拒绝后返回主界面且无退出或降级路径，轨迹判定为困在诱导页。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “系统要求：隐私控制功能所需；特权访问；Root可用”，但提示无法确认Root，需打开Magisk允许后点“再次检查”（Step 1主界面）
- 英文 -> “Privacy Flip无法执行：Root已配置但未获授权，锁屏/解锁动作被跳过，打开应用授权”（Step 1-6通知横幅）
- 英文 -> “禁用电池优化以保证后台可靠运行”（Step 1主界面）
- 英文 -> “锁屏检测（实验）：启用无障碍服务作为额外锁屏/解锁信号”（Step 5-6主界面卡片）
- 英文 -> “本服务不读取屏幕内容或密码”，仅感知锁屏出现/消失（服务详情页）
- 英文 -> “允许Privacy Flip获得完全控制？可查看并控制屏幕、读取所有内容、覆盖其他应用、跟踪交互并代操作”（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 主界面系统要求页：提示Root可用但未授权，需打开Magisk后重查；电池优化已开启；顶部两条无法执行通知常驻，本次下滑寻找锁屏检测。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 主界面隐私开关页：列出Wi-Fi、蓝牙、移动数据、定位、NFC及锁屏关闭/解锁开启选项；两条无法执行通知仍在，继续下滑。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 主界面继续下滑：显示相机/麦克风及飞行模式、省电等扩展锁屏开关；提示Android版本不支持摄像头/麦克风切换，通知仍常驻。 | `step_03_action.png` |
| 4 | **Step 4: MainActivity** | 主界面延时与调试页：显示应用豁免、锁屏后10秒/解锁后1秒延时、调试通知与日志开关；两条无法执行通知仍在，下滑露出无障碍状态。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | 主界面锁屏检测（实验）卡片：说明用无障碍服务作额外锁屏/解锁信号；点击未勾选开关以触发无障碍流程，通知仍常驻。 | `step_05_action.png` |
| 6 | **Step 6: MainActivity** | 同一卡片：开关已开启，状态提示需在系统无障碍设置中启用；点击“打开无障碍设置”跳转系统页，两条无法执行通知仍常驻。 | `step_06_action.png` |
| 7 | **Step 7: [无障碍列表页]** | 系统无障碍列表页：显示“Privacy Flip - Lock Screen Detection”为关闭；采集到无障碍设置钩子与探针后自动终止，应用通知仍在。 | `step_07_screen.png` |
| 8 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍停留在系统无障碍列表页，无弹窗或遮罩，应用两条无法执行通知继续显示。 | `step_07_probe_800ms_screen.png` |
| 9 | **跳后探针 +2.0s** | 跳转后2.0秒探针：页面未变化，无遮罩或新弹窗，通知栏仍挂两条Privacy Flip无法执行提示。 | `step_07_probe_2000ms_screen.png` |
| 10 | **服务详情页** | 服务详情页：说明无障碍仅感知锁屏出现/消失作额外信号，不读取屏幕内容或密码；服务当前关闭，需点“使用”进入系统授权。 | `step_07_service_detail_screen.png` |
| 11 | **系统警告弹窗(点Deny)** | 系统授权警告弹窗：称该服务将获得完全控制，可查看屏幕内容、覆盖其他应用并代操作；底部允许/拒绝，本步选择拒绝。 | `step_07_system_warning_screen.png` |
| 12 | **拒权返回 +2.0s** | 拒权后2秒返回主界面：仍停在延时/调试区域，无退出或降级路径；两条无法执行通知仍常驻，轨迹标记为困在诱导页。 | `step_07_refusal_2000ms_screen.png` |
| 13 | **拒权返回 +10.5s** | 拒权后10.5秒：主界面未变化，仍显示延时/调试项且通知常驻；无取消或关闭诱导卡片路径，继续处于困在诱导页状态。 | `step_07_refusal_10500ms_screen.png` |
