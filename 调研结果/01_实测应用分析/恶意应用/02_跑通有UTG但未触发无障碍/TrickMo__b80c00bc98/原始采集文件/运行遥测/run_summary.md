# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:18:32
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`orkei.ti981.pay`（静态标签：`malicious` / `TrickMo` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `2` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `orkei.ti981.pay` / `q9ZvOL4rBmC` | `-` | 0 | 0 / 否 | `wait` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `orkei.ti981.pay` / `q9ZvOL4rBmC` | `-` | 0 | 0 / 否 | `wait` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `orkei.ti981.pay` / `q9ZvOL4rBmC` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `orkei.ti981.pay` / `q9ZvOL4rBmC` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `orkei.ti981.pay` / `q9ZvOL4rBmC` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`orkei.ti981.pay/q9ZvOL4rBmC`)**: (空文本)
- **Step 5 (`orkei.ti981.pay/q9ZvOL4rBmC`)**: (空文本)
- **Step 6 (`orkei.ti981.pay/q9ZvOL4rBmC`)**: (空文本)
- **Step 7 (`orkei.ti981.pay/q9ZvOL4rBmC`)**: (空文本)
- **Step 8 (`orkei.ti981.pay/q9ZvOL4rBmC`)**: (空文本)

## 中文逐页引导链路解读

> **全链路总结**：该应用无启动图标，代理多次按包名启动均无界面后，改用静态Activity跳转进入orkei.ti981.pay的q9ZvOL4rBmC，WebView长期空白，随后连续静态跳转至多个组件（含WorkManager系统代理）均未呈现业务界面；全程仅见Google Play服务“数据未备份”英文通知，未出现授权/拒权测试或明确诱导话术。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “你的数据未备份”（Step1-Step8顶部系统通知横幅；来自com.google.android.gms，非目标应用话术）
- 英文 -> “立即添加备份帐户”（Step1-Step8顶部系统通知横幅；来自com.google.android.gms，非目标应用话术）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面应用列表页；目标应用无启动图标，代理按包名直接启动，未出现目标界面；顶部谷歌服务“数据未备份”通知。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍为桌面列表；代理重试按包名打开，目标应用无界面响应，未触发WebView；谷歌“数据未备份”通知仍显示。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 桌面页；直接启动无界面，代理改静态Activity跳转进入目标包q9ZvOL4rBmC；谷歌未备份通知仍在。 | `step_03_screen.png` |
| 4 | **Step 4: q9ZvOL4rBmC** | 目标q9ZvOL4rBmC空白页；WebView载荷渲染中，无可见文案或按钮，无遮罩，代理等待，谷歌未备份通知仍在。 | `step_04_action.png` |
| 5 | **Step 5: q9ZvOL4rBmC** | q9ZvOL4rBmC仍空白；无UI元素，代理继续等待WebView完成；仅见谷歌“数据未备份”通知。 | `step_05_action.png` |
| 6 | **Step 6: q9ZvOL4rBmC** | q9ZvOL4rBmC无内容；代理静态跳转至Bl4P9CM5U0NphInSk，未渲染成功；谷歌未备份通知仍在。 | `step_06_screen.png` |
| 7 | **Step 7: q9ZvOL4rBmC** | q9ZvOL4rBmC空白；再静态跳转VA1Q3FvY_3YtXoCRqlfm，仍无界面或话术；谷歌未备份通知仍在。 | `step_07_screen.png` |
| 8 | **Step 8: q9ZvOL4rBmC** | q9ZvOL4rBmC空白；静态跳转至ConstraintProxy$Batter系统组件，非业务页，无诱导文案；谷歌未备份通知仍在。 | `step_08_screen.png` |
