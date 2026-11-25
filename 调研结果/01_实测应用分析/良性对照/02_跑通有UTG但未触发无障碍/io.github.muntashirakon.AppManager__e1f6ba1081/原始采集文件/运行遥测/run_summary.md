# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:08:15
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`io.github.muntashirakon.AppManager`（静态标签：`benign` / `系统清理与省电冻结` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `3` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `io.github.muntashirakon.AppManager` / `KeyStoreActivity` | `-` | 5 | 240 / 否 | `click` → [5] Button text="Close" id=button2 (click) center=(832, | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `io.github.muntashirakon.AppManager` / `SplashActivity` | `-` | 3 | 47 / 否 | `wait` | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `io.github.muntashirakon.AppManager` / `SplashActivity` | `-` | 3 | 47 / 否 | `wait` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `io.github.muntashirakon.AppManager` / `SplashActivity` | `-` | 3 | 47 / 否 | `wait` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `io.github.muntashirakon.AppManager` / `SplashActivity` | `-` | 3 | 47 / 否 | `system_button` → Back | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `open` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `io.github.muntashirakon.AppManager` / `SplashActivity` | `-` | 3 | 47 / 否 | `wait` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `io.github.muntashirakon.AppManager` / `SplashActivity` | `-` | 3 | 47 / 否 | `wait` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`io.github.muntashirakon.AppManager/KeyStoreActivity`)**: `KeyStore` | `The following is the App Manager KeyStore password. Ple` | `zCSrQefOH3skRYUhSLcSEhy7KyRF8I` | `Show password` | `Close`
- **Step 2 (`io.github.muntashirakon.AppManager/SplashActivity`)**: `App Manager` | `Determining working mode…` | `4.1.1 (451)`
- **Step 3 (`io.github.muntashirakon.AppManager/SplashActivity`)**: `App Manager` | `Determining working mode…` | `4.1.1 (451)`
- **Step 4 (`io.github.muntashirakon.AppManager/SplashActivity`)**: `App Manager` | `Determining working mode…` | `4.1.1 (451)`
- **Step 5 (`io.github.muntashirakon.AppManager/SplashActivity`)**: `App Manager` | `Determining working mode…` | `4.1.1 (451)`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 7 (`io.github.muntashirakon.AppManager/SplashActivity`)**: `App Manager` | `Determining working mode…` | `4.1.1 (451)`
- **Step 8 (`io.github.muntashirakon.AppManager/SplashActivity`)**: `App Manager` | `Determining working mode…` | `4.1.1 (451)`

## 中文逐页引导链路解读

> **全链路总结**：应用启动后先弹出 KeyStore 密码提示并明文展示密码，关闭后进入 Splash 启动页持续显示“Determining working mode…”，多次等待仍卡住，返回桌面重启后依旧停留在启动页；全程无通知横幅、无遮罩，未进入主界面，也未出现授权或拒权诱导。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English -> “以下为 App Manager KeyStore 密码，请存放在安全处以便备份/恢复；此消息不会再次显示”（KeyStoreActivity 页面，属安全提示而非诱导）
- English -> “正在确定工作模式…”（SplashActivity 页面，属初始化状态提示）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: KeyStoreActivity** | KeyStoreActivity 弹出密码提示，英文说明密码用于备份/恢复且仅显示一次，并明文展示 zCSr…；本步点击 Close 关闭，无通知横幅与遮罩。 | `step_01_action.png` |
| 2 | **Step 2: SplashActivity** | SplashActivity 启动页显示 App Manager、版本 4.1.1 与英文“Determining working mode…（正在确定工作模式）”；本步等待加载，无通知与遮罩。 | `step_02_action.png` |
| 3 | **Step 3: SplashActivity** | 仍停留 Splash 启动页，继续显示“正在确定工作模式…”及版本 4.1.1；本步再次等待初始化，页面无通知横幅、无遮罩。 | `step_03_action.png` |
| 4 | **Step 4: SplashActivity** | Splash 启动页第三次保持“正在确定工作模式…”，未出现新内容；本步继续等待，页面无通知、无遮罩，也未进入主界面。 | `step_04_action.png` |
| 5 | **Step 5: SplashActivity** | Splash 启动页仍卡在“正在确定工作模式”，等待无进展后本步按系统 Back 退出应用；页面无通知横幅、无遮罩，也无取消/跳过键。 | `step_05_action.png` |
| 6 | **Step 6: NexusLauncherActivity** | 退出至系统桌面 NexusLauncher，显示 Apps list、周三 11月25日、-1°C 多云及 Messages/Chrome/Search 等；本步准备重新打开应用，无通知/遮罩。 | `step_06_action.png` |
| 7 | **Step 7: SplashActivity** | 重新启动后仍回到 SplashActivity，显示“正在确定工作模式…”与版本 4.1.1；本步继续等待，页面无通知横幅与遮罩。 | `step_07_action.png` |
| 8 | **Step 8: SplashActivity** | Splash 启动页第二次仍卡在“正在确定工作模式…”，长时间等待无变化；页面无通知、无遮罩，也未进入主界面或授权流程。 | `step_08_action.png` |
