# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:59:43
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.snaperfect.inframe1`（静态标签：`malicious` / `GodFather` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `4` 个，有向边 `5` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_A11Y_SETTINGS`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.snaperfect.inframe1/com.snaperfect.inframe1.Activitys.calamaroidblennometritis` | hooks=`[]` | overlays=`0` | texts=``
- **Back 后 +5.5s**：`com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | hooks=`['HOOK_A11Y_SETTINGS']` | overlays=`0` | texts=`Back / Accessibility / Search settings / DOWNLOADED APPS / MYT Müzik`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.snaperfect.inframe1` / `calamaroidblennometritis` | `-` | 0 | 0 / 否 | `wait` | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 208 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.snaperfect.inframe1/calamaroidblennometritis`)**: (空文本)
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `MYT Müzik` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用以异名启动页冷启动并投放“MYT Müzik/请激活以保持更新生效”通知，随后跳转系统无障碍列表与 MYT Müzik 服务详情，展示全权控制警告；拒绝后未收敛，2秒内退回启动页并再次拉起无障碍设置，呈现冒充音乐应用、借更新名义诱导开启无障碍全权控制及拒权循环重拉特征。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> 请激活以保持更新生效（无障碍列表通知横幅）
- 英语 -> 允许 MYT Müzik 完全控制您的设备？（系统全权控制警告弹窗）
- 英语 -> 完全控制适用于帮助无障碍需求的应用，但不适用于大多数应用（系统全权控制警告弹窗）
- 英语 -> 查看并控制屏幕（系统全权控制警告弹窗）
- 英语 -> 可读取屏幕全部内容并覆盖显示在其他应用上（系统全权控制警告弹窗）
- 英语 -> 查看并执行操作（系统全权控制警告弹窗）
- 英语 -> 可跟踪您与应用或硬件传感器的交互，并代表您与应用程序交互（系统全权控制警告弹窗）
- 英语 -> 使用 MYT Müzik（服务详情页开关）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: calamaroidblennometritis** | 应用冷启动进入异名启动页 calamaroidblennometritis，无可见文案；仅有本应用空通知“String ( )”，遮罩0，等待后触发无障碍设置跳转。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 系统无障碍列表页，显示“DOWNLOADED APPS/MYT Müzik Off”；通知横幅称“请激活以保持更新生效”，遮罩0，采集钩子后自动终止。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳转后0.8秒探针仍停在系统无障碍列表，页面文案未捕获，遮罩0；仅剩本应用空通知，无新增弹窗。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳转后2.0秒探针仍在无障碍列表，文案为空，遮罩0；本应用空通知持续，无新增诱导界面，等待结束。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 进入“MYT Müzik”服务详情，见“使用 MYT Müzik”开关和快捷方式设置，说明为“未提供说明”；遮罩0，本步查看详情。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 弹出系统全权控制警告：是否允许 MYT Müzik 完全控制设备，并称可读屏、覆盖显示及代操作；有 Allow/Deny，本步检查警告。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒绝后约2秒回到异名启动页，界面无文案；本应用空通知仍在，遮罩0，拒绝后直接重拉无障碍设置（RELAUNCHED_A11Y_SETTINGS）。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +5.5s** | 拒绝后5.5秒再次出现无障碍列表，MYT Müzik 仍为 Off，通知“请激活以保持更新生效”复现；遮罩0，显示拒权循环重拉。 | `step_02_refusal_5500ms_screen.png` |
