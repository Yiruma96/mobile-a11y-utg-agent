# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:47:04
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.helicopter.shoot.city.explore.peace`（静态标签：`malicious` / `HiddenAd` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `3` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.helicopter.shoot.city.explore.peace` / `UnityPlayerActivity` | `-` | 1 | 9 / 否 | `wait` | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.helicopter.shoot.city.explore.peace` / `UnityPlayerActivity` | `-` | 1 | 9 / 否 | `click` → [1] View desc="Game view" center=(540,1074) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.helicopter.shoot.city.explore.peace` / `UnityPlayerActivity` | `-` | 1 | 9 / 否 | `static_activity_jump` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.helicopter.shoot.city.explore.peace` / `UnityPlayerActivity` | `-` | 1 | 9 / 否 | `click` → [540, 937] | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.helicopter.shoot.city.explore.peace` / `UnityPlayerActivity` | `-` | 1 | 9 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.helicopter.shoot.city.explore.peace` / `UnityPlayerActivity` | `-` | 1 | 9 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.helicopter.shoot.city.explore.peace` / `b` | `-` | 1 | 9 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.helicopter.shoot.city.explore.peace/UnityPlayerActivity`)**: `Game view`
- **Step 2 (`com.helicopter.shoot.city.explore.peace/UnityPlayerActivity`)**: `Game view`
- **Step 3 (`com.helicopter.shoot.city.explore.peace/UnityPlayerActivity`)**: `Game view`
- **Step 4 (`com.helicopter.shoot.city.explore.peace/UnityPlayerActivity`)**: `Game view`
- **Step 5 (`com.helicopter.shoot.city.explore.peace/UnityPlayerActivity`)**: `Game view`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 7 (`com.helicopter.shoot.city.explore.peace/UnityPlayerActivity`)**: `Game view`
- **Step 8 (`com.helicopter.shoot.city.explore.peace/b`)**: `Game view`

## 中文逐页引导链路解读

> **全链路总结**：应用以 UnityPlayerActivity 的 Game view 黑屏游戏视图为入口，穿插 GDPR 同意弹窗点击与多次静态引导跳转，依次经过 Facebook 接收器、com.helicopt.ga、系统桌面及可疑短组件 b，最终指向 com.saypromo.SPAdActivity 广告页。核心特征是游戏界面掩护下的授权诱导与隐藏广告跳转。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 I Accept -> 中文“我接受”（Step 4：Unity 游戏视图内 GDPR 同意弹窗，选项已勾选，诱导用户直接同意）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: UnityPlayerActivity** | UnityPlayerActivity 游戏视图，仅显示英文 Game view（游戏视图），无通知与遮罩；代理先等待观察，界面仍停留在黑屏启动状态。 | `step_01_action.png` |
| 2 | **Step 2: UnityPlayerActivity** | 仍为 Unity 游戏视图 Game view（游戏视图），无通知、无遮罩；代理点击屏幕中心（540,1074）试图推进，仍未见可交互内容。 | `step_02_action.png` |
| 3 | **Step 3: UnityPlayerActivity** | 仍为 Unity 游戏视图 Game view（游戏视图），无通知与遮罩；本步为静态引导跳转探针，目标指向 Facebook 令牌过期广播接收器。 | `step_03_screen.png` |
| 4 | **Step 4: UnityPlayerActivity** | 仍显示 Game view（游戏视图），代理记录出现 GDPR 同意弹窗且 I Accept（我接受）已勾选；本步点击坐标推进，无通知与遮罩。 | `step_04_action.png` |
| 5 | **Step 5: UnityPlayerActivity** | Unity 游戏视图 Game view（游戏视图），无通知与遮罩；静态引导探针再次跳转，目标为可疑短包名 com.helicopt.ga 组件。 | `step_05_screen.png` |
| 6 | **Step 6: NexusLauncherActivity** | 跳至系统 NexusLauncherActivity 桌面，显示 Apps list（应用列表）、Messages（信息）、Chrome、Search（搜索）等；无通知与遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: UnityPlayerActivity** | 回到 Unity 游戏视图 Game view（游戏视图），无通知与遮罩；静态引导探针跳向同包可疑短组件 com.helicopt.b。 | `step_07_screen.png` |
| 8 | **Step 8: b** | 进入同包 activity b，界面仍为 Game view（游戏视图），无通知与遮罩；静态引导探针继续跳向 com.saypromo.SPAdActivity 广告页。 | `step_08_screen.png` |
