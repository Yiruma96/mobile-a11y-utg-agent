# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T16:17:38
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.coramobile.powerbattery.batterysaver`（静态标签：`malicious` / `Xavier` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 15 | 179 / 否 | `click` → [15] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.coramobile.powerbattery.batterysaver` / `SplashActivity` | `-` | 3 | 144 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.coramobile.powerbattery.batterysaver` / `SplashActivity` | `-` | 2 | 48 / 否 | `click` → [1] Button text="START" id=btn_start (click) center=(54 | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.coramobile.powerbattery.batterysaver` / `UserTipActivity` | `-` | 4 | 77 / 否 | `click` → [4] TextView text="Skip" id=skip (click) center=(80,195 | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.coramobile.powerbattery.batterysaver` / `MainActivity` | `-` | 4 | 77 / 否 | `click` → [4] TextView text="Skip" id=skip (click) center=(80,195 | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.coramobile.powerbattery.batterysaver` / `MainActivity` | `-` | 4 | 77 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.coramobile.powerbattery.batterysaver` / `MainActivity` | `-` | 4 | 77 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.coramobile.powerbattery.batterysaver` / `MainActivity` | `-` | 4 | 77 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Battery Saver to access` | `Files and media` | `access photos, media, and files on your device` | `Contacts` | `access your contacts` | `Phone` | `make and manage phone calls` | `Cancel` | `Continue`
- **Step 2 (`com.coramobile.powerbattery.batterysaver/SplashActivity`)**: `Battery Saver` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.coramobile.powerbattery.batterysaver/SplashActivity`)**: `START` | `By proceeding you agree with Privacy Policy`
- **Step 4 (`com.coramobile.powerbattery.batterysaver/UserTipActivity`)**: `Thank you for choosing Battery Saver` | `Swipe left or right to see more tips.` | `Skip`
- **Step 5 (`com.coramobile.powerbattery.batterysaver/MainActivity`)**: `Thank you for choosing Battery Saver` | `Swipe left or right to see more tips.` | `Skip`
- **Step 6 (`com.coramobile.powerbattery.batterysaver/MainActivity`)**: `Thank you for choosing Battery Saver` | `Swipe left or right to see more tips.` | `Skip`
- **Step 7 (`com.coramobile.powerbattery.batterysaver/MainActivity`)**: `Thank you for choosing Battery Saver` | `Swipe left or right to see more tips.` | `Skip`
- **Step 8 (`com.coramobile.powerbattery.batterysaver/MainActivity`)**: `Thank you for choosing Battery Saver` | `Swipe left or right to see more tips.` | `Skip`

## 中文逐页引导链路解读

> **全链路总结**：该应用先通过系统权限聚合页索取文件/媒体、联系人与电话权限并点Continue，再经旧版兼容警告、START同意隐私政策、Skip提示轮播进入MainActivity；提示层反复残留，后以静态回退连续跳转ForceActivity、SplashActivity与ShortcutActivity。核心特征是借“电池优化”名义聚拢高敏感权限，界面仅推进不提供拒权/退出，并伴随空通知占位。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文：“Choose what to allow Battery Saver to access” -> “选择允许 Battery Saver 访问的内容”（Step_01 系统权限页）
- 英文：“Files and media — access photos, media, and files on your device” -> “文件与媒体：访问设备上的照片、媒体和文件”（Step_01 权限说明）
- 英文：“Contacts — access your contacts” -> “联系人：访问你的联系人”（Step_01 权限说明）
- 英文：“Phone — make and manage phone calls” -> “电话：拨打和管理电话”（Step_01 权限说明）
- 英文：“This app was built for an older version of Android and may not work properly” -> “该应用为旧版Android构建，可能无法正常运行”（Step_02 兼容警告）
- 英文：“By proceeding you agree with Privacy Policy” -> “继续即表示你同意隐私政策”（Step_03 启动页）
- 英文：“Thank you for choosing Battery Saver”与“Swipe left or right to see more tips.” -> “感谢选择 Battery Saver”并引导左右滑动查看更多提示（Step_04至Step_08 提示轮播）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限聚合页，列文件媒体、联系人、电话三项访问，含Cancel与Continue；本步点Continue同意运行时权限，无遮罩通知。 | `step_01_action.png` |
| 2 | **Step 2: SplashActivity** | SplashActivity兼容警告页，提示该应用为旧版Android构建可能异常，仅有OK；本步点OK关闭警告，无遮罩与应用通知。 | `step_02_action.png` |
| 3 | **Step 3: SplashActivity** | 启动页仅见START与“继续即同意隐私政策”，无拒绝或退出选项；本步点START进入主流程，未触发遮罩或通知。 | `step_03_action.png` |
| 4 | **Step 4: UserTipActivity** | UserTipActivity提示轮播页，称感谢选择Battery Saver并可左右滑动看更多提示，含Skip；本步点Skip跳过，无遮罩通知。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | MainActivity仍残留提示轮播层，称感谢选择并可左右滑动看提示，含Skip；再点Skip尝试关闭，应用通知标题/正文均为空。 | `step_05_action.png` |
| 6 | **Step 6: MainActivity** | 界面仍为提示轮播层，含感谢选择、左右滑动与Skip；本步非点击，静态回退跳转至force.ForceActivity，通知为空。 | `step_06_screen.png` |
| 7 | **Step 7: MainActivity** | 界面仍为提示轮播层，含感谢选择、左右滑动与Skip；本步静态回退跳转至.activity.SplashActivity，通知为空无遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: MainActivity** | 界面仍为提示轮播层，含感谢选择、左右滑动与Skip；静态回退跳转至ShortcutActivity，通知为空、无遮罩。 | `step_08_screen.png` |
