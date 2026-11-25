# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:21:13
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.kieronquinn.app.taptap`（静态标签：`benign` / `按键映射与手势导航` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `7` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.kieronquinn.app.taptap` / `MainActivity` | `-` | 3 | 40 / 否 | `click` → [2] Button text="Get started" id=setup_landing_get_star | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.kieronquinn.app.taptap` / `MainActivity` | `-` | 8 | 871 / 否 | `click` → [8] Button text="Next" id=setup_info_next (click) cente | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.kieronquinn.app.taptap` / `MainActivity` | `-` | 5 | 176 / 否 | `click` → [4] Button text="Allow while Tap, Tap is open" id=dialo | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.kieronquinn.app.taptap` / `MainActivity` | `-` | 6 | 135 / 否 | `click` → [5] ImageButton (click) center=(77,2038) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.kieronquinn.app.taptap` / `MainActivity` | `-` | 12 | 576 / 否 | `swipe` → [540, 1900] | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.kieronquinn.app.taptap` / `MainActivity` | `-` | 12 | 554 / 否 | `click` → [2] ImageButton (click) center=(77,160) | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.kieronquinn.app.taptap` / `MainActivity` | `-` | 6 | 113 / 否 | `click` → [5] ImageButton (click) center=(77,2038) | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.kieronquinn.app.taptap` / `MainActivity` | `-` | 12 | 576 / 否 | `click` → [2] ImageButton (click) center=(77,160) | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.kieronquinn.app.taptap/MainActivity`)**: `Welcome to Tap, Tap` | `Get started` | `Skip setup`
- **Step 2 (`com.kieronquinn.app.taptap/MainActivity`)**: `Tap, Tap is free and open source` | `Tap, Tap is and always will be free, building off open ` | `Only install Tap, Tap from one of the official sources ` | `If you like the Tap, Tap app and wish to make a donatio` | `Next`
- **Step 3 (`com.kieronquinn.app.taptap/MainActivity`)**: `Allow Internet Access?` | `This will only be used to retrieve device specification` | `Allow Always` | `Allow while Tap, Tap is open` | `Deny`
- **Step 4 (`com.kieronquinn.app.taptap/MainActivity`)**: `Double tap the back of your device to activate the gest` | `Gesture Configuration`
- **Step 5 (`com.kieronquinn.app.taptap/MainActivity`)**: `Gesture Configuration` | `Device Size` | `Select the best model size for your device. Currently s` | `Sensitivity` | `Change the sensitivity of the gesture by adjusting how ` | `Value, High` | `Double tap the back of your device to activate the gest`
- **Step 6 (`com.kieronquinn.app.taptap/MainActivity`)**: `Gesture Configuration` | `Device Size` | `Select the best model size for your device. Currently s` | `Sensitivity` | `Change the sensitivity of the gesture by adjusting how ` | `Value, High` | `Not working? Try changing the device size and sensitivi`
- **Step 7 (`com.kieronquinn.app.taptap/MainActivity`)**: `Not working? Try changing the device size and sensitivi` | `Gesture Configuration`
- **Step 8 (`com.kieronquinn.app.taptap/MainActivity`)**: `Gesture Configuration` | `Device Size` | `Select the best model size for your device. Currently s` | `Sensitivity` | `Change the sensitivity of the gesture by adjusting how ` | `Value, High` | `Double tap the back of your device to activate the gest`

## 中文逐页引导链路解读

> **全链路总结**：从欢迎页点“开始”，经开源说明页、选择“仅打开时允许”联网，进入双击背部手势引导；随后反复展开/关闭手势配置面板仅调尺寸与灵敏度，未触发后续授权或拒权，通知栏持续显示服务运行。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “欢迎使用Tap, Tap”“开始”“跳过设置”（Step1欢迎页）
- 英文 -> “Tap, Tap免费且开源，源码可在GitHub查看，官方下载仅限XDA、GitHub、APKMirror”（Step2开源说明页）
- 英文 -> “仅从上述官方来源安装，否则建议卸载重装”（Step2开源说明页）
- 英文 -> “允许联网？仅用于获取设备规格并定期后台检查更新”（Step3联网弹窗）
- 英文 -> “双击设备背面激活手势，用食指指腹用力敲”（Step4/5/8手势引导）
- 英文 -> “不生效？尝试在手势配置面板调整设备尺寸和灵敏度”（Step6/7）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 欢迎页：欢迎使用Tap, Tap，提供开始与跳过设置；本步点“Get started”进入设置向导，无通知与遮罩。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 开源说明页：称应用免费开源，仅建议从XDA、GitHub、APKMirror安装；本步点“Next”继续，无通知与遮罩。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 联网授权弹窗：称仅用于读取设备规格和后台检查更新；含始终允许、仅打开时允许、拒绝，本步选“仅打开时允许”。 | `step_03_action.png` |
| 4 | **Step 4: MainActivity** | 手势引导页：提示双击背部触发，用食指指腹用力敲；本步点箭头展开手势配置，通知栏显示服务运行。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | 手势配置面板：可调设备尺寸与灵敏度，当前153.9mm中号、灵敏度高；本步下滑以寻找触发控制，通知栏显示服务运行。 | `step_05_action.png` |
| 6 | **Step 6: MainActivity** | 配置面板底部：提示不生效可调尺寸和灵敏度；本步点X关闭面板回到手势设置页，通知栏仍显示服务运行。 | `step_06_action.png` |
| 7 | **Step 7: MainActivity** | 手势设置页：保留“不生效可调配置”提示与手势配置入口；本步再次点箭头展开面板寻找触发控制，通知栏显示服务运行。 | `step_07_action.png` |
| 8 | **Step 8: MainActivity** | 手势配置面板：仍为尺寸/灵敏度调节，当前中号与高灵敏度；本步点X关闭面板，未执行触发探针，通知栏显示服务运行。 | `step_08_action.png` |
