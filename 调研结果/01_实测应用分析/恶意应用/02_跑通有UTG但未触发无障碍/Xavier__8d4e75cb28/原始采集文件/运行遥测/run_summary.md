# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:41:30
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.helpdesk.slauncher`（静态标签：`malicious` / `Xavier` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 27 | 280 / 否 | `click` → [27] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `android` / `ResolverActivity` | `-` | 3 | 142 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `android` / `ResolverActivity` | `-` | 6 | 71 / 否 | `click` → [6] TextView text="S6 Launcher" id=text1 center=(297,20 | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.helpdesk.slauncher` / `Launcher` | `-` | 1 | 64 / 否 | `click` → [240, 940] | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.helpdesk.slauncher` / `Launcher` | `-` | 1 | 64 / 否 | `click` → [300, 940] | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.helpdesk.slauncher` / `Launcher` | `-` | 1 | 64 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.helpdesk.slauncher` / `Launcher` | `-` | 1 | 64 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.helpdesk.slauncher` / `Launcher` | `-` | 1 | 64 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow S6 Launcher to access` | `Phone` | `make and manage phone calls` | `Contacts` | `access your contacts` | `Files and media` | `access photos, media, and files on your device` | `SMS` | `send and view SMS messages` | `Call logs`
- **Step 2 (`android/ResolverActivity`)**: `S6 Launcher` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`android/ResolverActivity`)**: `Use Pixel Launcher as Home` | `Just once` | `Always` | `Use a different app` | `S6 Launcher`
- **Step 4 (`com.helpdesk.slauncher/Launcher`)**: `By continuing you accept our Terms of Service and Priva`
- **Step 5 (`com.helpdesk.slauncher/Launcher`)**: `By continuing you accept our Terms of Service and Priva`
- **Step 6 (`com.helpdesk.slauncher/Launcher`)**: `By continuing you accept our Terms of Service and Priva`
- **Step 7 (`com.helpdesk.slauncher/Launcher`)**: `By continuing you accept our Terms of Service and Priva`
- **Step 8 (`com.helpdesk.slauncher/Launcher`)**: `By continuing you accept our Terms of Service and Priva`

## 中文逐页引导链路解读

> **全链路总结**：应用以S6 Launcher为名，先诱导一次性授予电话、联系人、文件媒体、短信、通话记录和相机等权限，再经旧版Android警告与主屏幕选择进入启动器；首屏以继续即接受条款隐私政策并需点GO，后续无界面变化但静态跳转至设置/壁纸裁剪。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “选择允许S6 Launcher访问的内容”（Step1权限授权页）
- 英文 -> “继续即表示接受我们的服务条款和隐私政策”（Step4-8启动器首页）
- 英文 -> “此应用为旧版Android构建，可能无法正常运行，请检查更新或联系开发者”（Step2旧版警告页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 英文系统权限总览页，列电话、联系人、文件媒体、短信、通话记录、相机；本步点Continue继续授权，虽有Cancel但未取消。 | `step_01_action.png` |
| 2 | **Step 2: ResolverActivity** | 旧版Android警告弹窗，称S6 Launcher可能无法正常运行，建议检查更新或联系开发者；本步点OK忽略，通知栏显示其运行中。 | `step_02_action.png` |
| 3 | **Step 3: ResolverActivity** | 主屏幕选择页，提示用Pixel Launcher作Home，列出Just once、Always、其他应用及S6 Launcher；本步点选S6 Launcher作桌面。 | `step_03_action.png` |
| 4 | **Step 4: Launcher** | 启动器首页仅见“继续即接受服务条款和隐私政策”，下方GO按钮；本步点屏幕中部尝试进入，通知栏仍显示S6 Launcher运行中。 | `step_04_action.png` |
| 5 | **Step 5: Launcher** | 同一启动器首页，条款隐私文案和GO按钮仍在；本步再次点击GO中心，仍未跳转，仅通知栏保留S6 Launcher运行提示。 | `step_05_action.png` |
| 6 | **Step 6: Launcher** | 界面仍为启动器条款页且无可见变化；本步为静态引导跳转至LauncherSetting.onActivityResult，通知栏仍显示S6 Launcher运行中。 | `step_06_screen.png` |
| 7 | **Step 7: Launcher** | 界面仍是条款与GO的启动器页，无用户可见变化；本步静态跳转到WallpaperCropActivity，通知栏保留S6 Launcher运行提示。 | `step_07_screen.png` |
| 8 | **Step 8: Launcher** | 仍显示条款与GO的启动器首页，无可见交互结果；本步静态跳转回LauncherSetting，通知栏持续显示S6 Launcher正在运行。 | `step_08_screen.png` |
