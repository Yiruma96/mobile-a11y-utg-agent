# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:09:12
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.appativesh.masterclean`（静态标签：`malicious` / `Xavier` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `7` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 19 | 217 / 否 | `click` → [19] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.appativesh.masterclean` / `PIPCleanerMainActivity` | `-` | 3 | 146 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.appativesh.masterclean` / `PIPCleanerMainActivity` | `-` | 21 | 104 / 否 | `click` → [10] RelativeLayout id=rl_to_boost (click) center=(268, | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.appativesh.masterclean` / `ProcessManagerActivity` | `-` | 21 | 250 / 否 | `click` → [21] Button text="Scanning...." id=btJunk (click) cente | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.appativesh.masterclean` / `JunkCleanActivity` | `-` | 23 | 121 / 否 | `click` → [23] Button text="Tap to Clean" id=btn_junk_clean (clic | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.appativesh.masterclean` / `JunkCleanActivity` | `-` | 17 | 235 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.appativesh.masterclean` / `JunkCleanActivity` | `-` | 18 | 263 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.appativesh.masterclean` / `JunkCleanActivity` | `-` | 18 | 263 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Master Cleanner to access` | `Files and media` | `access photos, media, and files on your device` | `Contacts` | `access your contacts` | `Phone` | `make and manage phone calls` | `Camera` | `take pictures and record video` | `Cancel`
- **Step 2 (`com.appativesh.masterclean/PIPCleanerMainActivity`)**: `Master Cleanner` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.appativesh.masterclean/PIPCleanerMainActivity`)**: `Master Cleanner` | `11.48 GB/12.46 GB` | `Memory` | `40.0℃` | `CPU temperature` | `Phone Boost` | `Junk Clean` | `App Lock` | `Clean` | `Tools`
- **Step 4 (`com.appativesh.masterclean/ProcessManagerActivity`)**: `Phone Boost` | `Your phone was boosted` | `0` | `M` | `-450 MB/1.16 GB` | `Apps with privacy issues` | `Turn on AppLock to protect your privacy` | `Go now` | `Notification Toggle` | `Turn on notification, more convenient to manage your ph`
- **Step 5 (`com.appativesh.masterclean/JunkCleanActivity`)**: `Junk Clean` | `1.59` | `Cleanable` | `M` | `Scan completed` | `Cache` | `87.00B` | `Thumbnail` | `108.00B` | `Residue cache`
- **Step 6 (`com.appativesh.masterclean/JunkCleanActivity`)**: `Junk Clean` | `Cleaned 1.59M junk` | `Speed up your phone` | `Apps with privacy issues` | `Turn on AppLock to protect your privacy` | `Go now` | `Notification Toggle` | `Turn on notification, more convenient to manage your ph` | `Home` | `Boost`
- **Step 7 (`com.appativesh.masterclean/JunkCleanActivity`)**: `Junk Clean` | `Cleaned 1.59M junk` | `Speed up your phone` | `Apps with privacy issues` | `Turn on AppLock to protect your privacy` | `Go now` | `Notification Toggle` | `Turn on notification, more convenient to manage your ph` | `Home` | `Boost`
- **Step 8 (`com.appativesh.masterclean/JunkCleanActivity`)**: `Junk Clean` | `Cleaned 1.59M junk` | `Speed up your phone` | `Apps with privacy issues` | `Turn on AppLock to protect your privacy` | `Go now` | `Notification Toggle` | `Turn on notification, more convenient to manage your ph` | `Home` | `Boost`

## 中文逐页引导链路解读

> **全链路总结**：链路从系统权限审查页请求文件媒体、联系人、电话、相机并点“继续”放行，进入清理主界面后以手机加速、垃圾清理、隐私风险和通知便捷话术连续引流。清理完成页再静默跳转至 AccessTip、进程管理及广告接收器组件，本轨迹未测试拒权结果。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “选择允许 Master Cleanner 访问什么”，并列文件媒体、联系人、电话、相机权限（Step 1 权限审查页，含取消/继续）
- 英文 -> “此应用为旧版 Android 构建，可能无法正常运行，请检查更新或联系开发者”（Step 2 兼容性警告，仅 OK）
- 英文 -> “你的手机已加速”“0 M”“-450 MB/1.16 GB”（Step 4 加速结果页，制造已优化/释放空间效果）
- 英文 -> “存在隐私问题的应用”“开启 AppLock 保护隐私”“立即前往”（Step 4、Step 6-8 隐私风险引流）
- 英文 -> “开启通知，更方便管理手机”（Step 4、Step 6-8 通知开关诱导）
- 英文 -> “扫描中…”“点击清理”（Step 4-5 按钮诱导，推动进入清理流程）
- 英文 -> “已清理 1.59M 垃圾”“加速你的手机”（Step 6-8 清理完成页，夸大清理效果）
- 英文 -> “手机加速”“垃圾清理”“应用锁”“清理”等功能入口（Step 3 首页，以工具名义吸引点击）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限审查页，英文要求选择允许 Master Cleanner 访问文件媒体、联系人、电话和相机；本步点“继续”放行，页面有取消键。 | `step_01_action.png` |
| 2 | **Step 2: PIPCleanerMainActivity** | 应用弹出旧版 Android 兼容警告，英文称可能无法正常运行、建议检查更新；本步点“OK”关闭警告以进入主界面，仅有确认键。 | `step_02_action.png` |
| 3 | **Step 3: PIPCleanerMainActivity** | 清理应用首页，展示内存、CPU温度及 Phone Boost、Junk Clean、App Lock 等入口；本步点击“手机加速”进入进程管理页。 | `step_03_action.png` |
| 4 | **Step 4: ProcessManagerActivity** | 手机加速结果页，英文称“你的手机已加速”并显示释放空间、隐私风险与通知开关诱导；本步点击“扫描中…”加速按钮。 | `step_04_action.png` |
| 5 | **Step 5: JunkCleanActivity** | 垃圾清理结果页，英文显示扫描完成、可清理 1.59M 及缓存/缩略图/APK 分类；本步点“点击清理”触发后续组件跳转。 | `step_05_action.png` |
| 6 | **Step 6: JunkCleanActivity** | 清理完成页，英文称“已清理1.59M垃圾/加速手机”，并含隐私、通知引流；本步静态回退跳转 AccessTipActivity。 | `step_06_screen.png` |
| 7 | **Step 7: JunkCleanActivity** | 仍为清理完成页，重复“已清理1.59M垃圾/加速手机”及隐私、通知引流；本步静态回退跳转 ProcessManagerActivity。 | `step_07_screen.png` |
| 8 | **Step 8: JunkCleanActivity** | 仍为清理完成页，重复清理/加速话术及隐私、通知引流；本步静态回退跳转广告接收器 PackageAddReceiver。 | `step_08_screen.png` |
