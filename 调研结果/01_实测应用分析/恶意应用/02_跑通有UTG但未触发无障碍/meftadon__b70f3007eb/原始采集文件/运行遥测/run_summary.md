# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:14:09
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.puredevlab.powermanager`（静态标签：`malicious` / `meftadon` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.puredevlab.powermanager` / `ViewActivity` | `-` | 6 | 42 / 否 | `click` → [6] ImageButton id=imageButton (click) center=(540,1968 | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.puredevlab.powermanager` / `ViewActivity` | `-` | 3 | 44 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,125 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.puredevlab.powermanager` / `ViewActivity` | `-` | 6 | 41 / 否 | `click` → [6] ImageButton id=imageButton (click) center=(540,1968 | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.puredevlab.powermanager` / `ViewActivity` | `-` | 3 | 44 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,125 | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.puredevlab.powermanager` / `ViewActivity` | `-` | 6 | 41 / 否 | `system_button` → Back | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.puredevlab.powermanager/ViewActivity`)**: `Power Manager` | `100 %` | `25.0 °C` | `Time left:` | `51h 12m`
- **Step 2 (`com.puredevlab.powermanager/ViewActivity`)**: `Success` | `Your device settings are optimized!` | `OK`
- **Step 3 (`com.puredevlab.powermanager/ViewActivity`)**: `Power Manager` | `100 %` | `25.0 °C` | `Time left:` | `64h 2m`
- **Step 4 (`com.puredevlab.powermanager/ViewActivity`)**: `Success` | `Your device settings are optimized!` | `OK`
- **Step 5 (`com.puredevlab.powermanager/ViewActivity`)**: `Power Manager` | `100 %` | `25.0 °C` | `Time left:` | `64h 2m`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 8 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`

## 中文逐页引导链路解读

> **全链路总结**：入口为伪造电量、温度和剩余时间的主界面，点击图片按钮后反复弹出“Success/设备设置已优化”的虚假成功框，关闭后回到主界面；系统返回后落回桌面，静态引导尝试跳转SrvAccessibility、ViewActivity及内部类均未进入应用授权页。整体仅见伪造优化成功话术，未观察到真实系统设置变更，授权或拒权结果未测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Power Manager -> 电量管理器（Step1/3/5主界面标题）
- Time left: 51h 12m / 64h 2m -> 剩余时间：51小时12分 / 64小时2分（Step1/3/5主界面）
- Success -> 成功（Step2/4成功弹窗标题）
- Your device settings are optimized! -> 您的设备设置已优化！（Step2/4成功弹窗正文）
- OK -> 确定（Step2/4仅有关闭按钮）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ViewActivity** | 主界面显示电量100%、温度25.0°C、剩余51h12m；点击底部无文字图片按钮“优化”，无通知或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: ViewActivity** | 弹出“Success/您的设备设置已优化！”对话框，仅有“OK”按钮；点击OK关闭，未出现权限或系统设置页。 | `step_02_action.png` |
| 3 | **Step 3: ViewActivity** | 回到主界面，电量100%、温度25.0°C、剩余时间变为64h2m；再次点击底部图片优化按钮，无遮罩。 | `step_03_action.png` |
| 4 | **Step 4: ViewActivity** | 再次弹出相同“Success/设备设置已优化”虚假成功框，仅有OK；点击关闭，仍无权限请求或跳转。 | `step_04_action.png` |
| 5 | **Step 5: ViewActivity** | 主界面仍显示100%、25.0°C、剩余64h2m；按系统返回键尝试回主Activity，未见隐藏菜单或权限入口。 | `step_05_action.png` |
| 6 | **Step 6: NexusLauncherActivity** | 桌面应用列表页，显示日期及Messages/Chrome/搜索；静态引导跳转SrvAccessibility未进入应用界面。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 仍在桌面应用列表，未显示应用界面；静态引导跳转com.puredevlab.powermanager.ViewActivity失败并停留桌面。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 仍在桌面应用列表，未显示应用界面；静态引导跳转ViewActivity$2内部类失败，无授权或权限提示。 | `step_08_screen.png` |
