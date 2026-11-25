# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:07:39
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`net.blumia.pineapple.lockscreen.oss`（静态标签：`benign` / `按键映射与手势导航` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `4` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`net.blumia.pineapple.lockscreen.oss/net.blumia.pineapple.lockscreen.MainActivityAliasGreenLock` | hooks=`[]` | overlays=`0` | texts=`This application require to enable its accessibility service in order to work.
You can use the following button to enable or disable the service conveniently. / Accessibility Settings / You can create a shortcut icon on your launcher to perform the lock action. / Create Shortcut Icon / This application also provide a quick settings tile to turn the screen off. You can add the tile by edit the quick settings area and drag the Lock Screen tile to where you want.`
- **Back 后 +5.5s**：`net.blumia.pineapple.lockscreen.oss/net.blumia.pineapple.lockscreen.MainActivityAliasGreenLock` | hooks=`[]` | overlays=`0` | texts=`This application require to enable its accessibility service in order to work.
You can use the following button to enable or disable the service conveniently. / Accessibility Settings / You can create a shortcut icon on your launcher to perform the lock action. / Create Shortcut Icon / This application also provide a quick settings tile to turn the screen off. You can add the tile by edit the quick settings area and drag the Lock Screen tile to where you want.`
- **Back 后 +10.5s**：`net.blumia.pineapple.lockscreen.oss/net.blumia.pineapple.lockscreen.MainActivityAliasGreenLock` | hooks=`[]` | overlays=`0` | texts=`This application require to enable its accessibility service in order to work.
You can use the following button to enable or disable the service conveniently. / Accessibility Settings / You can create a shortcut icon on your launcher to perform the lock action. / Create Shortcut Icon / This application also provide a quick settings tile to turn the screen off. You can add the tile by edit the quick settings area and drag the Lock Screen tile to where you want.`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `net.blumia.pineapple.lockscreen.oss` / `MainActivityAliasGreenLock` | `-` | 13 | 496 / 否 | `click` → [3] TextView text="Accessibility Settings" center=(279, | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 31 | 244 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`net.blumia.pineapple.lockscreen.oss/MainActivityAliasGreenLock`)**: `This application require to enable its accessibility se` | `Accessibility Settings` | `You can create a shortcut icon on your launcher to perf` | `Create Shortcut Icon` | `This application also provide a quick settings tile to ` | `Open Quick Settings` | `Pineapple Lock Screen` | `Menu`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Pineapple Lock Screen - Accessibility Service` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用入口主界面以英文强调必须启用无障碍服务，引导跳转系统无障碍列表并进入服务详情/系统警告；用户点 Deny 后应用反复回到同一主界面，形成 TRAPPED_ON_LURE_SCREEN，未见可继续使用的功能路径。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “本应用需要启用无障碍服务才能工作，可用下方按钮方便地启用或禁用该服务”（主界面 step_01/拒权返回页）
- 英文 -> “可创建启动器快捷图标执行锁屏动作”“提供快速设置磁贴关闭屏幕，可拖动 Lock Screen 磁贴到所需位置”（主界面）
- 英文 -> “该无障碍服务用于提供锁屏能力，否则应用无法工作；点右上角开关并在下一屏点 Allow；无需启用第二个快捷方式开关”（服务详情页）
- 英文 -> 注意事项：强制停止主应用后可能需重新启用服务；服务已启用但应用不正常时可尝试禁用再启用（服务详情页）
- 英文 -> 系统警告：允许 Pineapple Lock Screen - Accessibility Service 完全控制设备？可查看控制屏幕、查看并执行操作；有 Allow/Deny（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivityAliasGreenLock** | 应用主界面：英文称必须启用无障碍服务才能工作，本步点“Accessibility Settings”跳转系统设置；有 Google 备份通知，无遮罩。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 系统无障碍列表：显示“Pineapple Lock Screen - Accessibility Service”为 Off；探针在此截获设置 Hook 后自动终止，有 Google 备份通知，无遮罩。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳后0.8秒探针：仍停留系统无障碍列表，页面文本为空；通知新增 Gboard 更新提示，无弹窗/遮罩，未发生点击。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳后2.0秒探针：仍在系统无障碍列表，无页面文本变化；Google 备份与 Gboard 通知并存，无遮罩，仍等待。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 服务详情页：英文称无障碍服务用于锁屏能力，否则应用无法工作；指导点右上角开关并下一屏点 Allow，无需开第二开关。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统警告弹窗：询问是否允许该服务完全控制设备，列明可查看控制屏幕、查看并执行操作；提供 Allow/Deny，本步仅检查，无遮罩。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒权后2秒回到应用主界面：仍以英文要求启用无障碍服务，停留同一诱导页，未进入功能；有 Google 备份通知，无遮罩。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒权后10.5秒仍困在主界面：同一英文启用无障碍服务提示与按钮未消失，无替代使用路径；有备份通知，无遮罩。 | `step_02_refusal_10500ms_screen.png` |
