# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:36:17
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.cave.series`（静态标签：`malicious` / `Cerberus` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `5` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.cave.series/com.qyqnmuqtrwcsxf.nnjuaiupnwe.yjebjvqra.ndkdfujotsm` | hooks=`[]` | overlays=`0` | texts=`Accessibility / android-flat / Android Güncelleme / Bir sonraki ekranda erişilebilirlik izni vermeniz gerekmektedir.
1. Devam Et Tıklayınız
2. Yüklü servisler menüsünde veya Android Güncelleme'ye tıklayanız. / white-tick-png-8`
- **Back 后 +5.5s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing  to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`
- **Back 后 +10.5s**：`com.cave.series/com.qyqnmuqtrwcsxf.nnjuaiupnwe.yjebjvqra.ndkdfujotsm` | hooks=`[]` | overlays=`0` | texts=`Accessibility / android-flat / Android Güncelleme / Bir sonraki ekranda erişilebilirlik izni vermeniz gerekmektedir.
1. Devam Et Tıklayınız
2. Yüklü servisler menüsünde veya Android Güncelleme'ye tıklayanız. / white-tick-png-8`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.cave.series` / `ndkdfujotsm` | `-` | 7 | 222 / 否 | `click` → [5] View id=btn (click) center=(540,1503) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 217 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.cave.series/ndkdfujotsm`)**: `Accessibility` | `android-flat` | `Android Güncelleme` | `Bir sonraki ekranda erişilebilirlik izni vermeniz gerek` | `white-tick-png-8` | `Devam Et`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `ANDROID GUNCELLEME` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用以伪装成“Android 更新”的土耳其语页面诱导用户开启无障碍服务，并跳转系统无障碍列表、服务详情和高风险授权警告；用户拒绝后反复重弹诱导页，并穿插请求忽略电池优化以维持后台运行。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 土耳其语 -> “Android 更新”：伪装成系统更新组件（step_01/refusal_2.0s/refusal_10.5s）
- 土耳其语 -> “下一屏需授予无障碍权限：1.点击继续 2.在已安装服务中点击 Android 更新”：借更新名义诱导开启无障碍（step_01/refusal_2.0s/refusal_10.5s）
- 土耳其语 -> “继续”：诱导进入授权流程的按钮（step_01/refusal_2.0s/refusal_10.5s）
- 英语 -> “使用 ANDROID GUNCELLEME”：系统无障碍服务启用项（detail_1_service_detail_page）
- 英语 -> “允许 ANDROID GUNCELLEME 完全控制你的设备？”：高风险无障碍授权警告（detail_2_system_warning_dialog）
- 英语 -> “让应用始终在后台运行？”：请求忽略电池优化以保活（refusal_5.5s）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ndkdfujotsm** | 应用内土耳其语诱导页，伪装“Android 更新”，要求下一屏开启无障碍并点“继续”；本步点击该按钮。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 跳转系统无障碍列表，下载应用区见“ANDROID GUNCELLEME”状态关闭；命中无障碍设置钩子后终止，无通知/遮罩。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳转后0.8秒探针，仍停留系统无障碍列表页，无可见文本、无通知横幅、无遮罩，仅等待观察。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳转后2.0秒探针，页面仍为系统无障碍设置，无可见文本、无通知与遮罩，未发生进一步跳转。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 进入服务详情页，标题为“ANDROID GUNCELLEME”，含启用开关与快捷方式设置，说明为“未提供描述”；仅检查未授权。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统无障碍高风险警告弹窗，询问是否允许“ANDROID GUNCELLEME”完全控制设备，列出读屏与代操作能力；本步未点允许。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒绝后2秒被拉回应用同一土耳其语诱导页，仍要求开启无障碍并点“继续”，形成拒权后循环重弹。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +5.5s** | 拒绝后5.5秒弹出系统电池优化页，询问是否让应用始终后台运行，含“拒绝/允许”；随后又被拉回诱导页。 | `step_02_refusal_5500ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒绝后10.5秒再次回到应用土耳其语无障碍诱导页，继续催促点“继续”，显示拒权后反复重试诱导。 | `step_02_refusal_10500ms_screen.png` |
