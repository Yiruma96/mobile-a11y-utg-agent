# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:30:04
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.props.rescue.girl`（静态标签：`malicious` / `HiddenAd` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `3` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.props.rescue.girl` / `UnityPlayerActivity` | `-` | 3 | 21 / 否 | `wait` | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.props.rescue.girl` / `UnityPlayerActivity` | `-` | 1 | 9 / 否 | `click` → [1] View desc="Game view" center=(540,1074) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.props.rescue.girl` / `UnityPlayerActivity` | `-` | 1 | 9 / 否 | `swipe` → [210, 893] | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.props.rescue.girl` / `UnityPlayerActivity` | `-` | 1 | 9 / 否 | `static_activity_jump` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.props.rescue.girl` / `UnityPlayerActivity` | `-` | 1 | 9 / 否 | `swipe` → [190, 1024] | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.props.rescue.girl` / `UnityPlayerActivity` | `-` | 1 | 9 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.props.rescue.girl` / `UnityPlayerActivity` | `-` | 1 | 9 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.props.rescue.girl` / `CustomTabActivity` | `-` | 1 | 12 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.props.rescue.girl/UnityPlayerActivity`)**: `Game view` | `Props Rescue`
- **Step 2 (`com.props.rescue.girl/UnityPlayerActivity`)**: `Game view`
- **Step 3 (`com.props.rescue.girl/UnityPlayerActivity`)**: `Game view`
- **Step 4 (`com.props.rescue.girl/UnityPlayerActivity`)**: `Game view`
- **Step 5 (`com.props.rescue.girl/UnityPlayerActivity`)**: `Game view`
- **Step 6 (`com.props.rescue.girl/UnityPlayerActivity`)**: `Game view`
- **Step 7 (`com.props.rescue.girl/UnityPlayerActivity`)**: `Game view`
- **Step 8 (`com.props.rescue.girl/CustomTabActivity`)**: `Props Rescue`

## 中文逐页引导链路解读

> **全链路总结**：应用以Unity游戏“Props Rescue”为入口，前台仅显示游戏视图，未出现可见广告或授权弹窗；随后由静态引导连续跳转Facebook接收器、CustomTab及com.rescue.machine.UnityPlayerActivity，呈现隐藏广告链特征，授权结果未测试。

![全流程中文标注连环画](./utg_storyboard.png)

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: UnityPlayerActivity** | Unity游戏启动页，显示“Game view/Props Rescue”（游戏视图/道具救援）；等待加载，未见通知横幅、遮罩或广告弹窗。 | `step_01_action.png` |
| 2 | **Step 2: UnityPlayerActivity** | 仍在Unity游戏视图，仅有“Game view”（游戏视图）；点击屏幕中心尝试交互，未触发广告、通知或权限弹窗。 | `step_02_action.png` |
| 3 | **Step 3: UnityPlayerActivity** | Unity游戏视图无新文案；执行向上滑动，界面仍无广告层、通知横幅或遮罩，静态分析指向后台广告注入。 | `step_03_action.png` |
| 4 | **Step 4: UnityPlayerActivity** | 界面仍为Unity游戏视图，无新增提示；静态探针跳转至Facebook令牌过期广播接收器，未见可见页面或广告弹窗。 | `step_04_screen.png` |
| 5 | **Step 5: UnityPlayerActivity** | Unity游戏视图无新文案；再次滑动尝试拖动黄球入洞，但未出现广告、通知或遮罩，交互仍停留在游戏画面。 | `step_05_action.png` |
| 6 | **Step 6: UnityPlayerActivity** | 仍停留在Unity游戏视图，无新增外文提示；静态探针跳转至com.fully.AActivity，界面未显示广告或授权弹窗。 | `step_06_screen.png` |
| 7 | **Step 7: UnityPlayerActivity** | Unity游戏画面无变化，仅有“Game view”（游戏视图）；静态探针跳转至Facebook CustomTabActivity，仍未出现可见广告。 | `step_07_screen.png` |
| 8 | **Step 8: CustomTabActivity** | 进入Facebook CustomTab容器，仅见“Props Rescue”（道具救援）游戏名；静态跳转指向com.rescue.machine.UnityPlayerActivity，无通知/遮罩。 | `step_08_screen.png` |
