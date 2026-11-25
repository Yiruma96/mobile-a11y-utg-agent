# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:35:20
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.odiousapps.mx3buttonmapper`（静态标签：`benign` / `远程协助与跨设备互联` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.odiousapps.mx3buttonmapper/com.odiousapps.mx3buttonmapper.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Grant Shizuku permission, then enable this service under Accessibility / OPEN ACCESSIBILITY SETTINGS / Shizuku start/stop intent auth token (paste the full ‘auth: XXXX’ line from Shizuku’s View intents screen) / auth: XXXX / PASTE`
- **Back 后 +5.5s**：`com.odiousapps.mx3buttonmapper/com.odiousapps.mx3buttonmapper.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Grant Shizuku permission, then enable this service under Accessibility / OPEN ACCESSIBILITY SETTINGS / Shizuku start/stop intent auth token (paste the full ‘auth: XXXX’ line from Shizuku’s View intents screen) / auth: XXXX / PASTE`
- **Back 后 +10.5s**：`com.odiousapps.mx3buttonmapper/com.odiousapps.mx3buttonmapper.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Grant Shizuku permission, then enable this service under Accessibility / OPEN ACCESSIBILITY SETTINGS / Shizuku start/stop intent auth token (paste the full ‘auth: XXXX’ line from Shizuku’s View intents screen) / auth: XXXX / PASTE`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `android` / `ResolverActivity` | `-` | 6 | 77 / 否 | `click` → [6] TextView text="MX3 Button Mapper" id=text1 center=( | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.odiousapps.mx3buttonmapper` / `MainActivity` | `-` | 12 | 401 / 否 | `click` → [2] Button text="OPEN ACCESSIBILITY SETTINGS" id=openAc | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 216 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`android/ResolverActivity`)**: `Use Pixel Launcher as Home` | `Just once` | `Always` | `Use a different app` | `MX3 Button Mapper`
- **Step 2 (`com.odiousapps.mx3buttonmapper/MainActivity`)**: `Grant Shizuku permission, then enable this service unde` | `OPEN ACCESSIBILITY SETTINGS` | `Shizuku start/stop intent auth token (paste the full ‘a` | `auth: XXXX` | `PASTE` | `SAVE` | `TV brand (affects the MX3 Air Mouse TV button specifica` | `TCL` | `Blaupunkt` | `Log every key press (for troubleshooting only)`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `MX3 Button Mapper` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用由系统主页选择器启动后，主界面以“授予 Shizuku/开启无障碍”为核心诱导，引导进入系统无障碍列表、服务详情并弹出完全控制高危授权警告；点 Deny 后仍反复回到同一诱导主界面，最终被判定为 TRAPPED_ON_LURE_SCREEN。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Use Pixel Launcher as Home / Just once / Always / Use a different app -> 将 Pixel 启动器设为主页/仅一次/始终/使用其他应用（系统主页选择器）
- Grant Shizuku permission, then enable this service under Accessibility -> 授予 Shizuku 权限，然后在无障碍中启用此服务（应用主界面）
- OPEN ACCESSIBILITY SETTINGS -> 打开无障碍设置（应用主界面）
- Shizuku start/stop intent auth token (paste the full ‘auth: XXXX’ line from Shizuku’s View intents screen) -> 粘贴 Shizuku 完整 auth: XXXX 行作为启停令牌（应用主界面）
- Use MX3 Button Mapper -> 使用 MX3 按键映射器（服务详情页）
- Listens for specific hardware button presses ... Key presses are never stored or sent anywhere. -> 声称监听遥控硬件按键并重映射、记录前台应用以区分场景，按键不存储不外发（服务详情页）
- Allow MX3 Button Mapper to have full control of your device? -> 允许 MX3 Button Mapper 完全控制你的设备？（系统警告弹窗）
- View and control screen / It can read all content on the screen and display content over other apps. -> 查看并控制屏幕/可读取屏幕全部内容并悬浮显示在其他应用上（系统警告弹窗）
- View and perform actions / It can track your interactions with an app or a hardware sensor, and interact with apps on your behalf. -> 查看并执行操作/可跟踪你与应用或硬件传感器的交互，并代你操作应用（系统警告弹窗）
- Allow / Deny -> 允许/拒绝（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ResolverActivity** | 系统主页选择器：列表含“Use Pixel Launcher as Home/Just once/Always/Use a different app”；本步点选 MX3 Button Mapper 启动目标应用。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 应用主界面：提示授予 Shizuku 并在无障碍启用，含 auth 粘贴与 TV 品牌选项；本步点“OPEN ACCESSIBILITY SETTINGS”跳系统设置。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 系统无障碍列表：下载应用下 MX3 Button Mapper 显示 Off；探针捕获无障碍设置钩子后自动终止，无通知无遮罩。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转后 0.8 秒探针：仍停留在系统无障碍列表页，界面文本为空，overlays=0，无通知横幅。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后 2.0 秒探针：仍停留在系统无障碍列表页，界面文本为空，overlays=0，无通知横幅。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | 服务详情页：显示“Use MX3 Button Mapper”及快捷方式；说明称监听遥控按键并重映射、记录前台应用，不存储不外发。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 系统高危警告：询问是否允许完全控制设备，列明可读屏、悬浮显示、跟踪交互并代操作；有 Allow/Deny，overlays=0。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 拒权后返回主界面：仍显示授予 Shizuku、开启无障碍及 auth 粘贴诱导，无其他入口；判定 TRAPPED_ON_LURE_SCREEN。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权 10.5 秒后仍停留在同一主界面：继续展示 Shizuku/无障碍及 auth 粘贴诱导，无通知无遮罩，判定被困于诱导页。 | `step_03_refusal_10500ms_screen.png` |
