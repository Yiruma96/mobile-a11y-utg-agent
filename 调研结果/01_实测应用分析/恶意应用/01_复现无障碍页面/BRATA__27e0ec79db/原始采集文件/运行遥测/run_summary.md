# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:38:12
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.xd.craft.school`（静态标签：`malicious` / `BRATA` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `4` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.xd.craft.school/com.xd.craft.school.permission_activity_a11y` | hooks=`[]` | overlays=`0` | texts=`Nuestra App requiere tu autorización operativa para mantenerla completamente segura.
	Haga clic en el botón "Proceder" a continuación para autorizar que nuestro sistema de seguridad funcione en su dispositivo.


	Más descargas -> Accesibilidad -> Módulo de Seguridad Bancaria / Proceder`
- **Back 后 +5.5s**：`com.xd.craft.school/com.xd.craft.school.permission_activity_a11y` | hooks=`[]` | overlays=`0` | texts=`Nuestra App requiere tu autorización operativa para mantenerla completamente segura.
	Haga clic en el botón "Proceder" a continuación para autorizar que nuestro sistema de seguridad funcione en su dispositivo.


	Más descargas -> Accesibilidad -> Módulo de Seguridad Bancaria / Proceder`
- **Back 后 +10.5s**：`com.xd.craft.school/com.xd.craft.school.permission_activity_a11y` | hooks=`[]` | overlays=`0` | texts=`Nuestra App requiere tu autorización operativa para mantenerla completamente segura.
	Haga clic en el botón "Proceder" a continuación para autorizar que nuestro sistema de seguridad funcione en su dispositivo.


	Más descargas -> Accesibilidad -> Módulo de Seguridad Bancaria / Proceder`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.xd.craft.school` / `permission_activity_a11y` | `-` | 3 | 283 / 否 | `click` → [3] TextView text="Proceder" (click) center=(540,1672) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 227 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.xd.craft.school/permission_activity_a11y`)**: `Nuestra App requiere tu autorización operativa para man` | `Proceder`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Módulo de Seguridad Bancaria` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用先以西班牙语“安全授权”页诱导点击Proceder，跳转安卓无障碍开启“银行安全模块”，再以全控制警告索权；拒绝后通知催促并困回诱导页，体现BRATA式无障碍滥用与拒权锁定。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 西班牙语 -> “我们的应用需要你的操作授权以保持完全安全；请点击‘继续’授权安全系统运行；更多下载->无障碍->银行安全模块”（授权诱导页 step_01/refusal）
- 西班牙语 -> 按钮“Proceder”意为“继续/前往”（授权诱导页）
- 意大利语 -> 通知“Attenzione / Tu dispositivo está seguro”意为“注意/你的设备安全”（全流程通知横幅）
- 西班牙语/英语混合 -> 无障碍服务名“Módulo de Seguridad Bancaria”意为“银行安全模块”（无障碍列表/详情）
- 英语 -> “Our app use this service for make your device safety”意为“本应用使用此服务保障设备安全”（服务详情页）
- 西班牙语 -> 通知“Para continuar, habilite la opción de accesibilidad.”意为“要继续，请启用无障碍选项”（拒权返回后）
- 英语 -> 系统弹窗“Allow ... full control...”意为“允许银行安全模块完全控制设备？可读屏、覆盖应用并代为操作”（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: permission_activity_a11y** | 西语授权诱导页：称需授权保安全，指引无障碍开启“银行安全模块”；点“Proceder”，通知称设备安全，无遮罩。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 安卓无障碍列表显示“银行安全模块”关闭；捕获HOOK_A11Y_SETTINGS后终止，通知仍称设备安全，无遮罩。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳后0.8秒探针仍在无障碍列表，界面文本为空；通知横幅称注意/设备安全，遮罩0，无新增交互。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳后2.0秒探针仍停留无障碍列表，无界面文本；通知横幅持续称注意/设备安全，遮罩0，无操作。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 服务详情页：显示“使用银行安全模块”、音量键快捷方式及英文说明“保障设备安全”；无遮罩，通知称设备安全。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统全控制警告弹窗：提示可读屏、覆盖其他应用并代为操作；含允许/拒绝，本步仅检查，通知称设备安全。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 点拒绝返回后仍回西语授权诱导页；新增西语通知“要继续请启用无障碍”，下方通知称设备安全，陷于诱导页。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 10.5秒后仍困在西语授权诱导页，仅“Proceder”；西语通知催启用无障碍，另一通知称设备安全，无退出路径。 | `step_02_refusal_10500ms_screen.png` |
