# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:00:53
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`generating.purpose.nightlife`（静态标签：`malicious` / `Unattributed` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `4` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`generating.purpose.nightlife/generating.purpose.hqbifjnoaezametghmhuyxjhggtblhbjzsjaywebuweoloxrxk2.vwdzizsvjbkqdhgbswunkhoypfelwermymjyzztkwiqupmficv20` | hooks=`[]` | overlays=`0` | texts=`Itau Empresas Suporte / 1- Instale o Aplicativo Itau Empresas Suporte

2- Permitir o aplicativo

3- Depois de Ativar Aguarde o final do Procedimento. / Ativar`
- **Back 后 +5.5s**：`generating.purpose.nightlife/generating.purpose.hqbifjnoaezametghmhuyxjhggtblhbjzsjaywebuweoloxrxk2.vwdzizsvjbkqdhgbswunkhoypfelwermymjyzztkwiqupmficv20` | hooks=`[]` | overlays=`0` | texts=`Itau Empresas Suporte / 1- Instale o Aplicativo Itau Empresas Suporte

2- Permitir o aplicativo

3- Depois de Ativar Aguarde o final do Procedimento. / Ativar`
- **Back 后 +10.5s**：`generating.purpose.nightlife/generating.purpose.hqbifjnoaezametghmhuyxjhggtblhbjzsjaywebuweoloxrxk2.vwdzizsvjbkqdhgbswunkhoypfelwermymjyzztkwiqupmficv20` | hooks=`[]` | overlays=`0` | texts=`Itau Empresas Suporte / 1- Instale o Aplicativo Itau Empresas Suporte

2- Permitir o aplicativo

3- Depois de Ativar Aguarde o final do Procedimento. / Ativar`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `generating.purpose.nightlife` / `vwdzizsvjbkqdhgbswunkhoypfelwermymjyzztkwiqupmficv20` | `-` | 7 | 152 / 否 | `click` → [7] Button text="Ativar" id=okbtn (click) center=(540,1 | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 220 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`generating.purpose.nightlife/vwdzizsvjbkqdhgbswunkhoypfelwermymjyzztkwiqupmficv20`)**: `Itau Empresas Suporte` | `1- Instale o Aplicativo Itau Empresas Suporte  2- Permi` | `Ativar`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Itau Empresas Suporte` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用以葡萄牙语伪装“Itau Empresas Suporte”银行支持，分步引导安装、允许并激活无障碍服务；点击“Ativar”后跳至系统无障碍列表、服务详情和高风险授权弹窗，拒权后反复回到同一诱导页，形成无法绕出的陷阱。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 葡萄牙语 -> “Itaú 企业支持”：第1步安装该应用；第2步允许该应用；第3步激活后等待流程结束（入口诱导页）
- 葡萄牙语 -> “激活”按钮，催促用户开启后续系统授权（入口诱导页）
- 英语 -> 允许“Itau Empresas Suporte”完全控制你的设备？该权限可查看/控制屏幕、读取屏幕内容、覆盖其他应用并代替你操作（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: vwdzizsvjbkqdhgbswunkhoypf** | 葡语“Itau Empresas Suporte”假支持页：引导安装、允许并激活后等待；本步点Ativar，无遮罩，通知栏有应用空通知及Google备份提醒。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 跳至系统无障碍列表：下载应用中“Itau Empresas Suporte”显示Off；本步终止并记录HOOK_A11Y_SETTINGS探针，无遮罩。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳后0.8秒仍停留无障碍设置页，UI文本为空；等待探针显示overlays=0，无遮罩、无新弹窗。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳后2.0秒仍为无障碍设置页，未出现新界面；等待探针overlays=0，通知横幅仍在，无遮罩。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 进入无障碍服务详情：显示“Use Itau Empresas Suporte”，含快捷方式与按住音量键选项；本步仅检查详情，未授权。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统高风险授权弹窗：英文称可完全控制设备、读取屏幕并代为操作；提供Allow/Deny，本步仅检查未授权。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒绝后2秒被带回同一葡语诱导页：仍要求安装、允许、激活；仅见“Ativar”，无退出/取消，判定TRAPPED_ON_LURE_SCREEN。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒绝后10.5秒仍困在同一葡语诱导页：重复安装/允许/激活话术与“Ativar”，无退出或取消，维持TRAPPED_ON_LURE_SCREEN。 | `step_02_refusal_10500ms_screen.png` |
