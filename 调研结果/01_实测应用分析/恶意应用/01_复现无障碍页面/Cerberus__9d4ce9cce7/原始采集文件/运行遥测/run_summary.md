# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:09:31
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`tail.curious.matrix`（静态标签：`malicious` / `Cerberus` / 静态可见性：`packed_or_encrypted`）
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

> **全链路总结**：应用通过伪装成意大利语“系统更新”的无障碍服务诱导用户授予全控制权限；用户在系统警告页选择Deny后返回无障碍列表，服务保持Off，但应用随即重新拉起无障碍设置，呈现拒权后反复诱导/重试特征。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Aggiornamento del sistema -> “系统更新”（无障碍列表页/服务详情页：作为无障碍服务名称，伪装成系统更新）
- Use Aggiornamento del sistema -> “使用系统更新”（服务详情页：启用入口）
- Aggiornamento del sistema shortcut -> “系统更新快捷方式”（服务详情页：快捷方式设置项）
- Allow Aggiornamento del sistema to have full control of your device? -> “允许系统更新完全控制你的设备？”（系统全控制警告弹窗）
- View and control screen / View and perform actions -> “查看并控制屏幕”/“查看并执行操作”（系统警告弹窗权限说明）
- Your data isn’t backed up / Add a backup account now -> “你的数据未备份”/“现在添加备份账户”（全局Google通知横幅，非应用弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 无障碍列表页，下载应用区见意大利语“系统更新”服务且状态Off；顶部有未备份通知，无遮罩，采到钩子后终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳转后0.8秒探针，仍停留无障碍列表页，UI文本为空；顶部仍有Google未备份通知，无悬浮遮罩，等待0.8秒。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳转后2.0秒探针，仍在无障碍列表页且无可见文本；顶部保留未备份通知，遮罩数为0，等待2秒未出现新界面。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 服务详情页：意大利语“系统更新”服务含使用、快捷方式项且无描述；顶部有未备份通知，无遮罩，本步查看详情。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 全控制警告：英文称“系统更新”可读屏、覆盖显示并代操作；有Allow/Deny，本步点Deny，无遮罩，顶部有未备份通知。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒权后2秒回无障碍列表，服务仍Off；顶部未备份通知持续，无遮罩，动作标记RELAUNCHED_A11Y_SETTINGS。 | `step_01_refusal_2000ms_screen.png` |
