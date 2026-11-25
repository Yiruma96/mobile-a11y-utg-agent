# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:50:02
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`kind.collect.action`（静态标签：`malicious` / `Hydra` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `4` 个，有向边 `4` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_A11Y_SETTINGS`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | hooks=`['HOOK_A11Y_SETTINGS']` | overlays=`0` | texts=`Back / Accessibility / Search settings / DOWNLOADED APPS / HD Video Player`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `kind.collect.action` / `PermissionsActivity` | `-` | 6 | 223 / 否 | `click` → [6] Button text="GO TO SETTINGS" id=bt_goto_settings (c | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 214 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`kind.collect.action/PermissionsActivity`)**: `Activate accessibility services for the correct applica` | `Step 1. - Go to Settings` | `Step 2. - Open "Downloaded Services" menu` | `Step 3. - Activate services for the HD Video Player` | `Enjoy your new opportunities` | `GO TO SETTINGS`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `HD Video Player` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用入口以“HD Video Player”名义诱导用户前往系统设置启用无障碍服务，随后进入无障碍列表、服务详情与高权限系统警告弹窗；用户拒绝返回后应用重新拉起无障碍设置，呈现反复引导与持久化诱导特征。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Activate accessibility services for the correct application work: -> 为让应用正常工作，请启用无障碍服务（Step 1 权限页）
- Step 1. - Go to Settings -> 第一步：前往设置（Step 1 权限页）
- Step 2. - Open "Downloaded Services" menu -> 第二步：打开“已下载的服务”菜单（Step 1 权限页）
- Step 3. - Activate services for the HD Video Player -> 第三步：为HD Video Player启用服务（Step 1 权限页）
- Enjoy your new opportunities -> 享受你的新机会/新功能（Step 1 权限页）
- GO TO SETTINGS -> 前往设置（Step 1 权限页）
- Allow HD Video Player to have full control of your device? -> 允许HD Video Player完全控制你的设备？（系统警告弹窗）
- Full control is appropriate for apps that help you with accessibility needs, but not for most apps. -> 完全控制适用于辅助无障碍需求的应用，但不适合大多数应用（系统警告弹窗）
- View and control screen -> 可查看并控制屏幕：读取屏幕所有内容并覆盖显示在其他应用上（系统警告弹窗）
- View and perform actions -> 可查看并执行操作：跟踪与应用的交互或硬件传感器，并代你操作应用（系统警告弹窗）
- Allow -> 允许（系统警告弹窗）
- Deny -> 拒绝（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: PermissionsActivity** | 入口权限页：英文诱导为应用启用无障碍，按三步前往设置并开启“HD Video Player”；点击“GO TO SETTINGS”跳转系统设置。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 系统无障碍列表：显示“已下载应用”下HD Video Player为Off；应用跳转后在此停留并被终止抓取钩子，尚未开启服务。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍处系统无障碍列表，无可见文本、无通知横幅、遮罩数为0，未发生额外弹窗。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳转后2.0秒探针：页面仍为系统无障碍列表，无可见文本与通知，遮罩数为0，未出现诱导覆盖层。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 服务详情页：系统显示“HD Video Player”及“Use HD Video Player”开关、快捷键与音量键选项；说明为未提供描述，属待授权入口。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统高权限警告：英文询问是否允许HD Video Player完全控制设备，列明可读屏、悬浮显示、跟踪交互并代操作；提供Allow/Deny。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒权返回后2.0秒：回到无障碍列表，HD Video Player仍为Off；动作显示Back_refuse后应用重新拉起无障碍设置，呈反复引导。 | `step_02_refusal_2000ms_screen.png` |
