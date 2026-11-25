# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:15:38
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`scissors.boss.wide`（静态标签：`malicious` / `Cerberus` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 1 步，UTG 唯一节点 `3` 个，有向边 `3` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_A11Y_SETTINGS`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 1 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_01_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | hooks=`['HOOK_A11Y_SETTINGS']` | overlays=`0` | texts=`Back / Accessibility / Search settings / DOWNLOADED APPS / Aggiornamento del sistema`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 224 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Aggiornamento del sistema` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用以意大利语“Aggiornamento del sistema（系统更新）”伪装成系统组件，在无障碍列表引导开启服务，进入详情后触发“完全控制设备”的授权警告；代理点Deny拒权后出现重新拉起无障碍设置的行为，具明显诱导授权特征。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 意大利语「Aggiornamento del sistema」 -> 中文意译“系统更新”（无障碍列表/服务详情页），冒充系统更新组件诱导开启无障碍服务。
- 英语「Use Aggiornamento del sistema」 -> 中文意译“使用系统更新”（服务详情页），以系统更新名义引导启用。
- 英语「Allow Aggiornamento del sistema to have full control of your device?」 -> 中文意译“允许‘系统更新’完全控制您的设备？”（系统警告弹窗），实质索取无障碍完全控制权限。
- 英语「Full control is appropriate for apps that help you with accessibility needs, but not for most apps.」 -> 中文意译“完全控制适用于辅助无障碍需求的应用，不适用于大多数应用。”（系统警告弹窗），提示高风险授权。
- 英语「View and control screen / It can read all content on the screen and display content over other apps.」 -> 中文意译“查看并控制屏幕/可读取屏幕全部内容并叠加显示。”（系统警告弹窗），说明可监控与覆盖界面。
- 英语「View and perform actions / It can track your interactions with an app or a hardware sensor, and interact with apps on your behalf.」 -> 中文意译“查看并执行操作/可追踪交互并代你操作应用。”（系统警告弹窗），表明可代操作。
- 英语「No description provided.」 -> 中文意译“未提供描述”（服务详情页），服务说明缺失。

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 无障碍列表页：下载应用列出“Aggiornamento del sistema（系统更新）”且为Off；顶部备份未开启通知；无遮罩；捕获无障碍挂钩后终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳后0.8s：仍在无障碍设置页，暂无可见文本；无遮罩；等待0.8s探针，顶部Google备份未开启通知仍在。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳后2.0s：同一无障碍设置页仍无可捕获文本；无遮罩；等待2.0s探针，顶部备份未开启通知持续显示。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 服务详情页：显示“Aggiornamento del sistema（系统更新）”与“Use…（使用系统更新）”，含快捷键选项；顶部备份通知在，无遮罩，执行查看详情。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统警告弹窗：询问是否允许“系统更新”完全控制设备，列明可读屏、覆盖显示与代操作；顶部备份通知在；本步点Deny。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒权后2.0s：返回无障碍列表，“系统更新”仍为Off；顶部备份通知在，无遮罩；随后动作显示重新拉起无障碍设置。 | `step_01_refusal_2000ms_screen.png` |
