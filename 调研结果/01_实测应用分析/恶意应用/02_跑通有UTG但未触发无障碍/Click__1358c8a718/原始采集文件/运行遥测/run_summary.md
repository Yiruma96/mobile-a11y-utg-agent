# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:29:49
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.qiblafinder.prayertime.hijricalendar`（静态标签：`malicious` / `Click` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `2` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 7 | 192 / 否 | `click` → [5] Button text="While using the app" id=permission_all | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.qiblafinder.prayertime.hijricalendar` / `ActivityLocation` | `-` | 5 | 82 / 否 | `click` → [4] Button text="AUTOMATIC" id=automatic (click) center | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.qiblafinder.prayertime.hijricalendar` / `ActivityLocation` | `-` | 5 | 82 / 否 | `click` → [5] Button text="MANUAL" id=manual (click) center=(540, | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.qiblafinder.prayertime.hijricalendar` / `ActivityLocation` | `-` | 5 | 82 / 否 | `static_activity_jump` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.qiblafinder.prayertime.hijricalendar` / `ActivityLocation` | `-` | 5 | 82 / 否 | `swipe` → [540, 1600] | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.qiblafinder.prayertime.hijricalendar` / `ActivityLocation` | `-` | 5 | 82 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.qiblafinder.prayertime.hijricalendar` / `ActivityLocation` | `-` | 5 | 82 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.qiblafinder.prayertime.hijricalendar` / `ActivityLocation` | `-` | 5 | 82 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Qibla to access this device’s location?` | `This app may want to access your location all the time,` | `While using the app` | `Only this time` | `Deny`
- **Step 2 (`com.qiblafinder.prayertime.hijricalendar/ActivityLocation`)**: `Navigate up` | `Qibla` | `Please, choose the method of detection of your city` | `AUTOMATIC` | `MANUAL`
- **Step 3 (`com.qiblafinder.prayertime.hijricalendar/ActivityLocation`)**: `Navigate up` | `Qibla` | `Please, choose the method of detection of your city` | `AUTOMATIC` | `MANUAL`
- **Step 4 (`com.qiblafinder.prayertime.hijricalendar/ActivityLocation`)**: `Navigate up` | `Qibla` | `Please, choose the method of detection of your city` | `AUTOMATIC` | `MANUAL`
- **Step 5 (`com.qiblafinder.prayertime.hijricalendar/ActivityLocation`)**: `Navigate up` | `Qibla` | `Please, choose the method of detection of your city` | `AUTOMATIC` | `MANUAL`
- **Step 6 (`com.qiblafinder.prayertime.hijricalendar/ActivityLocation`)**: `Navigate up` | `Qibla` | `Please, choose the method of detection of your city` | `AUTOMATIC` | `MANUAL`
- **Step 7 (`com.qiblafinder.prayertime.hijricalendar/ActivityLocation`)**: `Navigate up` | `Qibla` | `Please, choose the method of detection of your city` | `AUTOMATIC` | `MANUAL`
- **Step 8 (`com.qiblafinder.prayertime.hijricalendar/ActivityLocation`)**: `Navigate up` | `Qibla` | `Please, choose the method of detection of your city` | `AUTOMATIC` | `MANUAL`

## 中文逐页引导链路解读

> **全链路总结**：该应用先请求系统定位授权，用户选择“使用应用时”后进入Qibla城市检测方式页；自动/手动选择均未带来可见页面变化，后续轨迹被静态探针连续跳转至指南针回调、启动页、包安装接收器与电池状态接收器，未见通知或遮罩。整体诱导话术较弱，风险集中在定位索取及安装包/系统状态监听线索。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “允许Qibla访问此设备的位置？”（Step 1 系统定位授权页）
- 英文 -> “该应用可能希望始终访问你的位置，即使你未使用应用；可在设置中允许。”（Step 1 系统定位授权页）
- 英文 -> “请选择检测你所在城市的方式”（Step 2-8 定位方式页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: GrantPermissionsActivity** | 系统定位授权页：请求允许Qibla访问位置，并称可能始终访问；本步点“使用应用时”授权前台定位，无通知或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: ActivityLocation** | 应用城市检测页：提示选择城市检测方式，提供自动/手动；本步点击AUTOMATIC，未见跳转、通知横幅或遮罩。 | `step_02_action.png` |
| 3 | **Step 3: ActivityLocation** | 同一城市检测页：仍显示自动/手动选项；本步改点MANUAL，后续观察无明显效果，无通知或遮罩。 | `step_03_action.png` |
| 4 | **Step 4: ActivityLocation** | 界面仍为城市检测页且无可见变化；轨迹以静态跳转探针指向Qibla指南针Activity回调，无通知或遮罩。 | `step_04_screen.png` |
| 5 | **Step 5: ActivityLocation** | 城市检测页未变；向上滑动查找搜索框或下一步，仍未出现新控件或跳转，无通知横幅与遮罩。 | `step_05_action.png` |
| 6 | **Step 6: ActivityLocation** | 页面仍停在城市检测页；探针静态跳转至应用启动页SplashActivity，无用户可见新界面、通知或遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: ActivityLocation** | 界面仍为城市检测页；轨迹探针跳转至包安装接收器PackageInstallReceiver，反映安装包事件监听线索，无可见UI或遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: ActivityLocation** | 界面仍为城市检测页；探针跳转至BatteryOkayReceiver电池状态接收器，反映系统状态监听线索，无可见UI或通知。 | `step_08_screen.png` |
