# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:02:03
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.iron.clothes.smooth.perfect`（静态标签：`malicious` / `HiddenAd` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `1` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.iron.clothes.smooth.perfect` / `UnityPlayerActivity` | `-` | 1 | 9 / 否 | `wait` | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.iron.clothes.smooth.perfect` / `UnityPlayerActivity` | `-` | 1 | 9 / 否 | `swipe` → [200, 700] | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.iron.clothes.smooth.perfect` / `UnityPlayerActivity` | `-` | 1 | 9 / 否 | `static_activity_jump` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.iron.clothes.smooth.perfect` / `UnityPlayerActivity` | `-` | 1 | 9 / 否 | `swipe` → [300, 1300] | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.iron.clothes.smooth.perfect` / `UnityPlayerActivity` | `-` | 1 | 9 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.iron.clothes.smooth.perfect` / `UnityPlayerActivity` | `-` | 1 | 9 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.iron.clothes.smooth.perfect` / `UnityPlayerActivity` | `-` | 1 | 9 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.iron.clothes.smooth.perfect` / `UnityPlayerActivity` | `-` | 1 | 9 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.iron.clothes.smooth.perfect/UnityPlayerActivity`)**: `Game view`
- **Step 2 (`com.iron.clothes.smooth.perfect/UnityPlayerActivity`)**: `Game view`
- **Step 3 (`com.iron.clothes.smooth.perfect/UnityPlayerActivity`)**: `Game view`
- **Step 4 (`com.iron.clothes.smooth.perfect/UnityPlayerActivity`)**: `Game view`
- **Step 5 (`com.iron.clothes.smooth.perfect/UnityPlayerActivity`)**: `Game view`
- **Step 6 (`com.iron.clothes.smooth.perfect/UnityPlayerActivity`)**: `Game view`
- **Step 7 (`com.iron.clothes.smooth.perfect/UnityPlayerActivity`)**: `Game view`
- **Step 8 (`com.iron.clothes.smooth.perfect/UnityPlayerActivity`)**: `Game view`

## 中文逐页引导链路解读

> **全链路总结**：该应用以 Unity 游戏外壳为入口，8 步前台始终停留在 UnityPlayerActivity，界面只呈现英文「Game view」，全程未出现任何可见的授权弹窗、通知横幅或悬浮遮罩，也没有拒绝授权的路径。探针以静态引导跳转的方式，串起 ironit 自定义 Activity、Tapjoy、AppsFlyer、字节海外 SDK 安装回执与独立进程下载器，呈现出隐藏广告注入，以及广告归因和下载分发链路。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 「游戏画面」（Step 1-8 同一 Unity 渲染视图），界面实际无可交互控件，仅作为伪装成正常游戏的空壳入口

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: UnityPlayerActivity** | 启动即进入 Unity 渲染视图，仅显示英文「Game view」（游戏画面）；本步静置等待加载，无通知横幅、无悬浮遮罩，也未弹出任何授权或诱导按钮。 | `step_01_action.png` |
| 2 | **Step 2: UnityPlayerActivity** | 仍是同一 Unity 游戏壳，仅有「Game view」文字；在坐标 [200,700] 上滑尝试唤醒游戏或隐藏面板，界面毫无变化，无点击响应、无弹窗。 | `step_02_action.png` |
| 3 | **Step 3: UnityPlayerActivity** | 前台依旧为游戏画面「Game view」；本步静态引导跳转探针指向 com.ironit.StartActivity，界面未切换，说明该 Activity 未真正暴露为可交互页面。 | `step_03_screen.png` |
| 4 | **Step 4: UnityPlayerActivity** | 界面仍只有「Game view」，属无 UI 元素的游戏渲染层；在 [300,1300] 上滑后无任何变化，未触发广告展示，也无通知条与遮罩层。 | `step_04_action.png` |
| 5 | **Step 5: UnityPlayerActivity** | 仍停留在 Unity 游戏壳「Game view」；静态跳转探针指向 Tapjoy 归因接收器 com.tapjoy.InstallReferrerReceiver，系统未展示对应界面，无可见提示。 | `step_05_screen.png` |
| 6 | **Step 6: UnityPlayerActivity** | 前台未变，仅显示「Game view」；探针尝试拉起 AppsFlyer 安装广播接收器 com.appsflyer.MultipleInstallBroadcastReceiver，无界面呈现，也没有授权或拒绝入口。 | `step_06_screen.png` |
| 7 | **Step 7: UnityPlayerActivity** | 仍为 Unity 游戏画面；静态引导跳向字节海外 SDK 的 GooglePlayInstallReceiver（安装回执接收器），界面无变化、无弹窗、无通知。 | `step_07_screen.png` |
| 8 | **Step 8: UnityPlayerActivity** | 页面仍只有「Game view」渲染视图；探针指向字节系 Downloader 独立进程组件，未弹出下载确认、安装引导或任何权限请求。 | `step_08_screen.png` |
