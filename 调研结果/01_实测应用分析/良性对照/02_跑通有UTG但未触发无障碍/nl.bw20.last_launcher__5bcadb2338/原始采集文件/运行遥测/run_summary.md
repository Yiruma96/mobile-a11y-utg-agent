# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:42:45
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`nl.bw20.last_launcher`（静态标签：`benign` / `极简桌面与双击锁屏` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `3` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `nl.bw20.last_launcher` / `MainActivity` | `-` | 1 | 41 / 否 | `long_press` → [1] View desc="Swipe up for apps
Long press for setting | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `nl.bw20.last_launcher` / `MainActivity` | `-` | 14 | 271 / 否 | `click` → [6] Button desc="Home" (click) center=(540,776) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `nl.bw20.last_launcher` / `MainActivity` | `-` | 7 | 193 / 否 | `click` → [4] Switch desc="Double tap to sleep
Requires accessibi | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `nl.bw20.last_launcher` / `MainActivity` | `-` | 7 | 193 / 否 | `click` → [4] Switch desc="Double tap to sleep
Requires accessibi | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `nl.bw20.last_launcher` / `MainActivity` | `-` | 7 | 193 / 否 | `click` → [1] Button desc="Back" (click) center=(77,160) | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `nl.bw20.last_launcher` / `MainActivity` | `-` | 14 | 271 / 否 | `click` → [6] Button desc="Home" (click) center=(540,776) | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `nl.bw20.last_launcher` / `MainActivity` | `-` | 7 | 193 / 否 | `click` → [4] Switch desc="Double tap to sleep
Requires accessibi | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `nl.bw20.last_launcher` / `MainActivity` | `-` | 7 | 193 / 否 | `click` → [4] Switch desc="Double tap to sleep
Requires accessibi | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`nl.bw20.last_launcher/MainActivity`)**: `Swipe up for apps Long press for settings`
- **Step 2 (`nl.bw20.last_launcher/MainActivity`)**: `Back` | `Settings` | `Set as default home app Open the system picker` | `Appearance Standard · System` | `Home` | `App drawer None` | `Backup & restore` | `Support` | `Donate Support the development of Last Launcher` | `Send feedback Email the developer`
- **Step 3 (`nl.bw20.last_launcher/MainActivity`)**: `Back` | `Home` | `Lock layout Disable pinning and long press on the home ` | `Double tap to sleep Requires accessibility service enab` | `Alignment Left` | `Left module None` | `Right module None`
- **Step 4 (`nl.bw20.last_launcher/MainActivity`)**: `Back` | `Home` | `Lock layout Disable pinning and long press on the home ` | `Double tap to sleep Requires accessibility service enab` | `Alignment Left` | `Left module None` | `Right module None`
- **Step 5 (`nl.bw20.last_launcher/MainActivity`)**: `Back` | `Home` | `Lock layout Disable pinning and long press on the home ` | `Double tap to sleep Requires accessibility service enab` | `Alignment Left` | `Left module None` | `Right module None`
- **Step 6 (`nl.bw20.last_launcher/MainActivity`)**: `Back` | `Settings` | `Set as default home app Open the system picker` | `Appearance Standard · System` | `Home` | `App drawer None` | `Backup & restore` | `Support` | `Donate Support the development of Last Launcher` | `Send feedback Email the developer`
- **Step 7 (`nl.bw20.last_launcher/MainActivity`)**: `Back` | `Home` | `Lock layout Disable pinning and long press on the home ` | `Double tap to sleep Requires accessibility service enab` | `Alignment Left` | `Left module None` | `Right module None`
- **Step 8 (`nl.bw20.last_launcher/MainActivity`)**: `Back` | `Home` | `Lock layout Disable pinning and long press on the home ` | `Double tap to sleep Requires accessibility service enab` | `Alignment Left` | `Left module None` | `Right module None`

## 中文逐页引导链路解读

> **全链路总结**：应用从桌面长按进入设置，再进入 Home 子页反复切换“双击息屏”开关，但始终未拉起系统无障碍授权。整体为极简桌面/双击锁屏的正常配置引导，无通知横幅或遮罩，拒权结果未测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Swipe up for apps / Long press for settings -> 上滑查看应用，长按进入设置（首页引导）
- Set as default home app / Open the system picker -> 设为默认桌面应用，打开系统选择器（设置主菜单）
- Double tap to sleep / Requires accessibility service enabled in system settings -> 双击息屏，需在系统设置中启用无障碍服务（Home 设置页）
- Donate / Support the development of Last Launcher -> 捐赠以支持 Last Launcher 开发（设置主菜单支持区）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 桌面首页，提示“上滑看应用、长按进设置”；长按提示区域进入设置，无通知横幅或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 设置主菜单，含默认桌面、外观、应用抽屉、备份与支持等入口；点击“Home”进入主页设置，无通知或遮罩。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 主页设置页，见锁定布局、双击息屏需无障碍、对齐与左右模块；点击“双击息屏”开关后为选中，未弹系统授权。 | `step_03_action.png` |
| 4 | **Step 4: MainActivity** | 仍为主页设置页；再次点击“双击息屏”开关，状态变为未选中，仍无系统无障碍授权弹窗，也无通知遮罩。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | 主页设置页；因开关未触发系统授权，点击左上“Back”返回设置主菜单，当前无通知横幅或悬浮遮罩。 | `step_05_action.png` |
| 6 | **Step 6: MainActivity** | 返回设置主菜单，含默认桌面、外观、应用抽屉、备份与支持；再次点击“Home”重试双击息屏设置，无通知或遮罩。 | `step_06_action.png` |
| 7 | **Step 7: MainActivity** | 再次进入主页设置，点击“双击息屏”开关使其选中；文案称需系统无障碍服务，但页面未出现系统授权弹窗或遮罩。 | `step_07_action.png` |
| 8 | **Step 8: MainActivity** | 主页设置页；点击“双击息屏”开关使其取消选中，仍未触发系统无障碍设置页，也无通知横幅或悬浮遮罩。 | `step_08_action.png` |
