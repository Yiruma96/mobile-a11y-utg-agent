# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:22:36
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.fire.the.desert.in`（静态标签：`malicious` / `HiddenAd` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `2` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.fire.the.desert.in` / `UnityPlayerActivity` | `-` | 1 | 9 / 否 | `wait` | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.fire.the.desert.in` / `UnityPlayerActivity` | `-` | 1 | 9 / 否 | `click` → [1] View desc="Game view" center=(540,1074) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.fire.the.desert.in` / `UnityPlayerActivity` | `-` | 1 | 9 / 否 | `static_activity_jump` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.fire.the.desert.in` / `UnityPlayerActivity` | `-` | 1 | 9 / 否 | `click` → [540, 1755] | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.fire.the.desert.in` / `UnityPlayerActivity` | `-` | 1 | 9 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.fire.the.desert.in` / `UnityPlayerActivity` | `-` | 1 | 9 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.fire.the.desert.in` / `UnityPlayerActivity` | `-` | 1 | 9 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.fire.the.desert.in/UnityPlayerActivity`)**: `Game view`
- **Step 2 (`com.fire.the.desert.in/UnityPlayerActivity`)**: `Game view`
- **Step 3 (`com.fire.the.desert.in/UnityPlayerActivity`)**: `Game view`
- **Step 4 (`com.fire.the.desert.in/UnityPlayerActivity`)**: `Game view`
- **Step 5 (`com.fire.the.desert.in/UnityPlayerActivity`)**: `Game view`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 7 (`com.fire.the.desert.in/UnityPlayerActivity`)**: `Game view`
- **Step 8 (`com.fire.the.desert.in/UnityPlayerActivity`)**: `Game view`

## 中文逐页引导链路解读

> **全链路总结**：应用入口为 UnityPlayerActivity，先显示黑屏“Game view”并引导点击或“TAP TO PLAY”，随后多次静态跳转至 StartActivity、Unity 内购页、系统桌面、Tenjin 与 GMS 安装来源接收器；全程未见通知横幅、悬浮遮罩或授权/拒权弹窗，拒权结果未测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English -> “点击开始”（UnityPlayerActivity 第4步 Unity 菜单按钮）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: UnityPlayerActivity** | UnityPlayerActivity 显示“Game view（游戏视图）”，为黑色加载画面；本步仅等待，未发现通知横幅或悬浮遮罩。 | `step_01_action.png` |
| 2 | **Step 2: UnityPlayerActivity** | 仍为 Unity 游戏视图黑色画面；点击屏幕中心“Game view（游戏视图）”试图跳过启动页继续流程，无通知或遮罩。 | `step_02_action.png` |
| 3 | **Step 3: UnityPlayerActivity** | 同一 Unity 游戏视图无新增可见文案；未点击，通过静态引导跳转到 com.firedesert.StartActivity，无通知与遮罩。 | `step_03_screen.png` |
| 4 | **Step 4: UnityPlayerActivity** | Unity 菜单画面，层级未暴露“TAP TO PLAY（点击开始）”按钮；按坐标点击该按钮继续，无通知横幅或悬浮遮罩。 | `step_04_action.png` |
| 5 | **Step 5: UnityPlayerActivity** | Unity 游戏视图；未点击，静态跳转至 VRPurchaseActivity（Unity 内购相关页），无通知横幅或悬浮遮罩。 | `step_05_screen.png` |
| 6 | **Step 6: NexusLauncherActivity** | 系统桌面应用列表，显示日期、-1°C 天气及 Messages、Chrome 等；无诱导话术，无通知横幅或遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: UnityPlayerActivity** | Unity 游戏视图无新增可见文案；未点击，静态跳转至 TenjinReferrerReceiver（归因接收器），无通知横幅或悬浮遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: UnityPlayerActivity** | Unity 游戏视图；未点击，静态跳转至 AppMeasurementInstallReferrer（安装来源测量接收器），无通知横幅或悬浮遮罩。 | `step_08_screen.png` |
