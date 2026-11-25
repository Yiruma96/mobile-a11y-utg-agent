# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:47:48
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.estrongs.android.pop`（静态标签：`malicious` / `Unattributed` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 4 步，UTG 唯一节点 `7` 个，有向边 `8` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 4 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_04_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.estrongs.android.pop/com.seguranca.protecao.SetupWizardActivity` | hooks=`[]` | overlays=`0` | texts=`1 de 5 / Etapa 1: Serviço de Proteção / O Serviço de Proteção precisa ser ativado para:

• Detectar aplicativos maliciosos
• Bloquear ameaças automaticamente
• Proteger seus dados em tempo real

Toque em ATIVAR para habilitar o serviço. / ATIVAR SERVIÇO / Configurando serviço de proteção...`
- **Back 后 +5.5s**：`com.estrongs.android.pop/com.seguranca.protecao.SetupWizardActivity` | hooks=`[]` | overlays=`0` | texts=`1 de 5 / Etapa 1: Serviço de Proteção / O Serviço de Proteção precisa ser ativado para:

• Detectar aplicativos maliciosos
• Bloquear ameaças automaticamente
• Proteger seus dados em tempo real

Toque em ATIVAR para habilitar o serviço. / ATIVAR SERVIÇO / Configurando serviço de proteção...`
- **Back 后 +10.5s**：`com.estrongs.android.pop/com.seguranca.protecao.SetupWizardActivity` | hooks=`[]` | overlays=`0` | texts=`1 de 5 / Etapa 1: Serviço de Proteção / O Serviço de Proteção precisa ser ativado para:

• Detectar aplicativos maliciosos
• Bloquear ameaças automaticamente
• Proteger seus dados em tempo real

Toque em ATIVAR para habilitar o serviço. / ATIVAR SERVIÇO / Configurando serviço de proteção...`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `RequestIgnoreBatteryOptimizations` | `-` | 4 | 181 / 否 | `click` → [4] Button text="Allow" id=button1 (click) center=(887, | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.estrongs.android.pop` / `SetupWizardActivity` | `-` | 4 | 251 / 否 | `click` → [4] Button text="AVANÇAR" id=btnNext (click) center=(54 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.estrongs.android.pop` / `SetupWizardActivity` | `-` | 4 | 244 / 否 | `click` → [4] Button text="ATIVAR SERVIÇO" id=btnNext (click) cen | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 31 | 292 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_04_layout.xml` + `step_04_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/RequestIgnoreBatteryOptimizations`)**: `Let app always run in background?` | `Allowing Privacy to always run in the background may re` | `Deny` | `Allow`
- **Step 2 (`com.estrongs.android.pop/SetupWizardActivity`)**: `0 de 5` | `Bem-vindo ao Sistema de Proteção` | `Este assistente irá configurar a proteção do seu dispos` | `AVANÇAR`
- **Step 3 (`com.estrongs.android.pop/SetupWizardActivity`)**: `1 de 5` | `Etapa 1: Serviço de Proteção` | `O Serviço de Proteção precisa ser ativado para:  • Dete` | `ATIVAR SERVIÇO`
- **Step 4 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Privacy` | `Off / Serviço de otimização de renderização e acessibil` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用先请求电池优化白名单并以伪系统通知常驻，随后用葡语“保护系统”五步向导诱导启用无障碍服务“Privacy”；进入系统无障碍详情与高风险完全控制警告，拒绝授权后仍卡在“正在配置保护服务”的诱导页，形成 TRAPPED_ON_LURE_SCREEN。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 允许应用始终在后台运行？（电池优化弹窗）
- 英文 -> 允许 Privacy 始终后台运行可能缩短续航，可稍后在设置中更改（电池优化弹窗）
- 葡萄牙语 -> 欢迎来到保护系统；本向导将用几步配置设备保护，需要授予权限，点击 AVANÇAR 继续（设置向导第0/5页）
- 葡萄牙语 -> 保护服务需激活以检测恶意应用、自动拦截威胁并实时保护数据，点击 ATIVAR SERVIÇO（设置向导第1/5页）
- 葡萄牙语 -> 企业界面渲染优化与无障碍服务（系统无障碍列表/详情描述）
- 英文 -> 允许 Privacy 完全控制设备？完全控制适合无障碍需求应用，不适用于多数应用；可查看控制屏幕、读取所有屏幕内容并叠加显示、跟踪交互并代为操作（系统警告弹窗）
- 葡萄牙语 -> 正在配置保护服务……请稍候（拒权返回向导页）
- 葡萄牙语/英文 -> “系统服务”/“正在优化能耗……”（常驻通知，伪装系统优化）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: RequestIgnoreBatteryOptimi** | 系统电池优化弹窗，英文诱导允许Privacy始终后台运行并称可能耗电；点Allow授权，通知栏伪装系统优化。 | `step_01_action.png` |
| 2 | **Step 2: SetupWizardActivity** | 设置向导第0/5页，葡语欢迎来到保护系统，称需授予权限配置防护；点AVANÇAR进入下一步，通知栏仍有伪装。 | `step_02_action.png` |
| 3 | **Step 3: SetupWizardActivity** | 向导第1/5页，葡语称保护服务需激活以检测恶意应用、拦截威胁并实时护数据；点ATIVAR SERVIÇO跳转无障碍。 | `step_03_action.png` |
| 4 | **Step 4: [无障碍列表页]** | 跳至系统无障碍列表，已下载应用Privacy显示关闭，描述为企业界面渲染优化与无障碍服务；采集钩子后终止。 | `step_04_screen.png` |
| 5 | **跳后探针 +0.8s** | 跳转后0.8秒探针，仍在无障碍列表且无可见文本；遮罩数为0，仅见伪装系统优化通知，等待观察。 | `step_04_probe_800ms_screen.png` |
| 6 | **跳后探针 +2.0s** | 跳转后2.0秒探针，无障碍列表无新增文本、无遮罩；伪装系统服务通知持续，页面未自动跳转。 | `step_04_probe_2000ms_screen.png` |
| 7 | **服务详情页** | Privacy服务详情页，显示Use Privacy开关关闭及Privacy shortcut选项；描述仍为企业渲染优化与无障碍，供检查。 | `step_04_service_detail_screen.png` |
| 8 | **系统警告弹窗(点Deny)** | 系统高风险警告：允许Privacy完全控制设备？称可读取屏幕、叠加显示并代操作；含Allow/Deny，本步检查未点。 | `step_04_system_warning_screen.png` |
| 9 | **拒权返回 +2.0s** | 点Deny/返回后2秒回到向导第1/5页，仍显示激活服务与“正在配置，请稍候”；无法退出，判定困在诱导页。 | `step_04_refusal_2000ms_screen.png` |
| 10 | **拒权返回 +10.5s** | 拒权后10.5秒仍停在向导第1/5页，激活按钮与“正在配置保护服务，请稍候”不变；持续困在诱导页。 | `step_04_refusal_10500ms_screen.png` |
