# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:24:28
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.sidalistudio.developer.app`（静态标签：`malicious` / `SharkBot` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `6` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.sidalistudio.developer.app` / `MainActivity` | `-` | 27 | 116 / 否 | `click` → [26] FrameLayout desc="Personal" id=navigation_persiona | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.sidalistudio.developer.app` / `MainActivity` | `-` | 22 | 146 / 否 | `click` → [5] LinearLayout id=ll_settings (click) center=(540,100 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.sidalistudio.developer.app` / `SettingActivity` | `-` | 32 | 395 / 否 | `swipe` → [540, 1900] | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.sidalistudio.developer.app` / `SettingActivity` | `-` | 31 | 392 / 否 | `click` → [1] ImageView id=im_back_toolbar (click) center=(71,159 | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.sidalistudio.developer.app` / `MainActivity` | `-` | 20 | 144 / 否 | `click` → [15] FrameLayout desc="Home" id=navigation_home (click) | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.sidalistudio.developer.app` / `MainActivity` | `-` | 32 | 220 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.sidalistudio.developer.app` / `MainActivity` | `-` | 32 | 220 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.sidalistudio.developer.app` / `MainActivity` | `-` | 32 | 220 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.sidalistudio.developer.app/MainActivity`)**: `HOME` | `44` | `%` | `Memory used` | `5` | `Storage used` | `Junk files` | `CPU Cooler` | `Phone boost` | `Antivirus`
- **Step 2 (`com.sidalistudio.developer.app/MainActivity`)**: `Phone AID, Cleaner, Booster has protected your phone 1 ` | `AD` | `Settings` | `Feedback` | `Upgrade` | `Other application` | `Share` | `Like us on Facebook` | `Home` | `Toolbox`
- **Step 3 (`com.sidalistudio.developer.app/SettingActivity`)**: `SETTINGS` | `General Settings` | `Notification Toggle` | `Create shortcut` | `Create home screen shortcut` | `Application protected` | `Do not dissturb` | `22:00 - 08:00` | `Notification Settings` | `Junk Reminder Frequency`
- **Step 4 (`com.sidalistudio.developer.app/SettingActivity`)**: `SETTINGS` | `Do not dissturb` | `22:00 - 08:00` | `Notification Settings` | `Junk Reminder Frequency` | `Every day` | `Phone Boost Reminder` | `Remind when memory overusing` | `CPU Cooler Reminder` | `Remind me when CPU overheating`
- **Step 5 (`com.sidalistudio.developer.app/MainActivity`)**: `Phone AID, Cleaner, Booster has protected your phone 1 ` | `Settings` | `Feedback` | `Upgrade` | `Other application` | `Share` | `Like us on Facebook` | `Home` | `Toolbox` | `Personal`
- **Step 6 (`com.sidalistudio.developer.app/MainActivity`)**: `HOME` | `53` | `%` | `Memory used` | `5` | `Storage used` | `Junk files` | `CPU Cooler` | `Phone boost` | `Antivirus`
- **Step 7 (`com.sidalistudio.developer.app/MainActivity`)**: `HOME` | `53` | `%` | `Memory used` | `5` | `Storage used` | `Junk files` | `CPU Cooler` | `Phone boost` | `Antivirus`
- **Step 8 (`com.sidalistudio.developer.app/MainActivity`)**: `HOME` | `53` | `%` | `Memory used` | `5` | `Storage used` | `Junk files` | `CPU Cooler` | `Phone boost` | `Antivirus`

## 中文逐页引导链路解读

> **全链路总结**：该SharkBot样本伪装成清理加速/App Lock工具，从首页经Personal进入设置未发现“高级保护”，随后多次静态跳转App Lock权限引导与启动页均未成功；全程零遮罩、无系统授权/拒权弹窗，拒权结果未测试，仅见谷歌备份系统通知。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- EN: “Phone AID, Cleaner, Booster has protected your phone 1 day(s)” -> “手机助手、清理器、加速器已保护您的手机1天”（Personal页）
- EN: “App Lock / Protect the privacy data and the property” -> “应用锁/保护隐私数据与财产”（首页）
- EN: “Antivirus / Phone boost / CPU Cooler / Power Saving / Game Booster” -> “杀毒/手机加速/CPU降温/省电/游戏加速”（首页功能承诺）
- EN: “Application protected” -> “应用已受保护”（设置页状态提示）
- EN: “Delete the APK file after app installed” -> “安装后删除APK文件”（设置页安装选项）
- EN: “Upgrade” -> “升级”（个人页推广入口）
- EN: “Your data isn’t backed up / Add a backup account now” -> “你的数据未备份/立即添加备份账户”（谷歌系统通知，非应用文案）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 首页清理加速仪表盘，显示内存/存储/垃圾/杀毒/省电/游戏加速与AD；点击Personal进入个人页，无遮罩，仅谷歌备份通知。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 个人页称已保护手机1天，列设置、反馈、升级、分享及Facebook点赞；点击Settings进入设置，无遮罩，通知同前。 | `step_02_action.png` |
| 3 | **Step 3: SettingActivity** | 设置页含通知开关、快捷方式、应用保护、免打扰22:00-08:00及垃圾/加速/降温提醒；下滑寻高级保护未果，无遮罩。 | `step_03_action.png` |
| 4 | **Step 4: SettingActivity** | 设置页下部含免打扰、通知与垃圾/加速/降温/省电提醒及安装后删APK；未见高级保护，点返回，无遮罩。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | 返回个人页仍为设置/反馈/升级/分享等入口；点击底部Home回首页，通知横幅未变，无遮罩。 | `step_05_action.png` |
| 6 | **Step 6: MainActivity** | 首页新增App Lock，称保护隐私数据与财产；静态探针跳转applock权限引导页失败，仍留首页，无授权弹窗。 | `step_06_screen.png` |
| 7 | **Step 7: MainActivity** | 首页仍显示App Lock隐私财产保护话术；再次静态跳转自身权限引导Activity未生效，界面未变，无授权弹窗。 | `step_07_screen.png` |
| 8 | **Step 8: MainActivity** | 首页不变；静态探针尝试跳转SplashActivity仍停留原页，未见权限/拒权流程，仅谷歌备份通知常驻。 | `step_08_screen.png` |
