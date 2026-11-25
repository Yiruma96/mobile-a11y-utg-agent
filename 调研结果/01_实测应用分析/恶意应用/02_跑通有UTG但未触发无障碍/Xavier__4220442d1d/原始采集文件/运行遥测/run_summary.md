# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:03:31
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.coramobile.powerbattery.batterysaver`（静态标签：`malicious` / `Xavier` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `7` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 15 | 179 / 否 | `click` → [15] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.coramobile.powerbattery.batterysaver` / `SplashActivity` | `-` | 3 | 144 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.coramobile.powerbattery.batterysaver` / `SplashActivity` | `-` | 4 | 79 / 否 | `click` → [3] Button text="START" id=btn_start (click) center=(54 | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.coramobile.powerbattery.batterysaver` / `UserTipActivity` | `-` | 4 | 77 / 否 | `click` → [4] TextView text="Skip" id=skip (click) center=(80,195 | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.coramobile.powerbattery.batterysaver` / `MainActivity` | `-` | 23 | 105 / 否 | `click` → [7] Button text="OPTIMIZE" id=apply_screen (click) cent | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.coramobile.powerbattery.batterysaver` / `NewOptimizeActivity` | `-` | 7 | 60 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.coramobile.powerbattery.batterysaver` / `NewOptimizeActivity` | `-` | 14 | 330 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.coramobile.powerbattery.batterysaver` / `NewOptimizeActivity` | `-` | 14 | 330 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Battery Saver to access` | `Files and media` | `access photos, media, and files on your device` | `Contacts` | `access your contacts` | `Phone` | `make and manage phone calls` | `Cancel` | `Continue`
- **Step 2 (`com.coramobile.powerbattery.batterysaver/SplashActivity`)**: `Battery Saver` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.coramobile.powerbattery.batterysaver/SplashActivity`)**: `BATTERY SAVER` | `Power, Just Faster` | `START` | `By proceeding you agree with Privacy Policy`
- **Step 4 (`com.coramobile.powerbattery.batterysaver/UserTipActivity`)**: `Thank you for choosing Battery Saver` | `Swipe left or right to see more tips.` | `Skip`
- **Step 5 (`com.coramobile.powerbattery.batterysaver/MainActivity`)**: `BATTERY SAVER` | `Charging time` | `100%` | `Completed` | `OPTIMIZE` | `Mode` | `Monitor` | `Cooler` | `Temperature` | `25`
- **Step 6 (`com.coramobile.powerbattery.batterysaver/NewOptimizeActivity`)**: `Navigate up` | `Optimize` | `Time left` | `H` | `M` | `0 Running apps consuming power`
- **Step 7 (`com.coramobile.powerbattery.batterysaver/NewOptimizeActivity`)**: `Navigate up` | `Optimize` | `Time left` | `26h14m` | `Rate our App` | `If you love our app, please take a moment to rate it on` | `SUPPORT 5 STAR` | `Adjust Brightness` | `Turning down the brightness to extends battery lifes.` | `Adjust`
- **Step 8 (`com.coramobile.powerbattery.batterysaver/NewOptimizeActivity`)**: `Navigate up` | `Optimize` | `Time left` | `26h14m` | `Rate our App` | `If you love our app, please take a moment to rate it on` | `SUPPORT 5 STAR` | `Adjust Brightness` | `Turning down the brightness to extends battery lifes.` | `Adjust`

## 中文逐页引导链路解读

> **全链路总结**：应用先经系统权限页请求文件媒体、联系人、电话等宽泛权限，再以旧版兼容提示、品牌启动页和“优化/降温/五星支持”等话术连续引导点击，最终进入优化页并静态跳转至强制清理/加速流程，呈典型工具类过度授权与诱导交互特征。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Choose what to allow Battery Saver to access / Files and media / Contacts / Phone -> 选择允许电池助手访问文件与媒体、联系人、电话（系统权限页 step_01）
- This app was built for an older version of Android and may not work properly... -> 此应用为旧版Android构建，可能无法正常运行（启动页 step_02）
- Power, Just Faster -> 电力，只是更快（启动页 step_03）
- By proceeding you agree with Privacy Policy -> 继续即表示同意隐私政策（启动页 step_03）
- Thank you for choosing Battery Saver / Swipe left or right to see more tips. -> 感谢选择电池助手；左右滑动查看更多提示（提示页 step_04）
- Charging time 100% Completed / OPTIMIZE -> 充电时间100%完成/优化（主页 step_05）
- 0 Running apps consuming power / Time left 26h14m -> 0个运行应用耗电/剩余26小时14分（优化页 step_06、step_07）
- Rate our App / If you love our app, please take a moment to rate it on Google Play store / SUPPORT 5 STAR -> 评价应用；若喜欢请花点时间在Google Play评分；支持五星（优化页 step_07、step_08）
- Adjust Brightness / Turning down the brightness to extends battery lifes. -> 调节亮度；降低亮度可延长电池寿命（优化页 step_07、step_08）
- Cooler Master / High CPU temperature can affect the health of mobilephone, click to test the current temperature / Cooling now! -> 降温大师；CPU高温影响手机健康，点击测试当前温度；正在降温！（优化页 step_07、step_08）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限总览页，要求为“电池助手”勾选文件与媒体、联系人、电话权限；本步点击“继续”放行，属过度授权入口。 | `step_01_action.png` |
| 2 | **Step 2: SplashActivity** | 旧版Android兼容警告启动页，提示应用可能无法正常运行，仅有“确定”可点；本步点确定关闭警告，通知栏有空白通知。 | `step_02_action.png` |
| 3 | **Step 3: SplashActivity** | 品牌启动页展示“电池助手/电力更快”和“开始”，并称继续即同意隐私政策；本步点开始进入主界面，通知栏空通知仍在。 | `step_03_action.png` |
| 4 | **Step 4: UserTipActivity** | 使用提示页称“感谢选择电池助手”，提示左右滑动查看更多；本步点“跳过”绕过提示轮播，通知栏空通知仍在。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | 主界面展示充电时间100%完成、温度25℃、电压5.00V及“优化”按钮；本步点优化进入加速流程，属伪电池监控面板。 | `step_05_action.png` |
| 6 | **Step 6: NewOptimizeActivity** | 优化页显示剩余时间和0个运行耗电应用；本步静态跳回启动页，未执行真实清理，通知栏空通知。 | `step_06_screen.png` |
| 7 | **Step 7: NewOptimizeActivity** | 优化页出现五星好评、亮度调节和“正在降温”卡片，宣称高温影响健康；本步静态跳转至强制清理页，诱导互动。 | `step_07_screen.png` |
| 8 | **Step 8: NewOptimizeActivity** | 同一优化页重复展示五星支持、亮度调节与降温话术；本步再次静态跳转至强制清理活动，页面未变化。 | `step_08_screen.png` |
