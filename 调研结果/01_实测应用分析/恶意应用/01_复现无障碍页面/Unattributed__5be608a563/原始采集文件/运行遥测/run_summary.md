# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T16:16:02
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.arlosoft.macrodroid`（静态标签：`malicious` / `Unattributed` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 4 步，UTG 唯一节点 `7` 个，有向边 `8` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 4 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_04_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.arlosoft.macrodroid/com.seguranca.protecao.SetupWizardActivity` | hooks=`[]` | overlays=`0` | texts=`1 de 5 / Etapa 1: Serviço de Proteção / O Serviço de Proteção precisa ser ativado para:

• Detectar aplicativos maliciosos
• Bloquear ameaças automaticamente
• Proteger seus dados em tempo real

Toque em ATIVAR para habilitar o serviço. / ATIVAR SERVIÇO / Configurando serviço de proteção...`
- **Back 后 +5.5s**：`com.arlosoft.macrodroid/com.seguranca.protecao.SetupWizardActivity` | hooks=`[]` | overlays=`0` | texts=`1 de 5 / Etapa 1: Serviço de Proteção / O Serviço de Proteção precisa ser ativado para:

• Detectar aplicativos maliciosos
• Bloquear ameaças automaticamente
• Proteger seus dados em tempo real

Toque em ATIVAR para habilitar o serviço. / ATIVAR SERVIÇO / Configurando serviço de proteção...`
- **Back 后 +10.5s**：`com.arlosoft.macrodroid/com.seguranca.protecao.SetupWizardActivity` | hooks=`[]` | overlays=`0` | texts=`1 de 5 / Etapa 1: Serviço de Proteção / O Serviço de Proteção precisa ser ativado para:

• Detectar aplicativos maliciosos
• Bloquear ameaças automaticamente
• Proteger seus dados em tempo real

Toque em ATIVAR para habilitar o serviço. / ATIVAR SERVIÇO / Configurando serviço de proteção...`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `RequestIgnoreBatteryOptimizations` | `-` | 4 | 188 / 否 | `click` → [4] Button text="Allow" id=button1 (click) center=(887, | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.arlosoft.macrodroid` / `SetupWizardActivity` | `-` | 4 | 251 / 否 | `click` → [4] Button text="AVANÇAR" id=btnNext (click) center=(54 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.arlosoft.macrodroid` / `SetupWizardActivity` | `-` | 4 | 244 / 否 | `click` → [4] Button text="ATIVAR SERVIÇO" id=btnNext (click) cen | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 31 | 274 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_04_layout.xml` + `step_04_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/RequestIgnoreBatteryOptimizations`)**: `Let app always run in background?` | `Allowing Rei dos Canais to always run in the background` | `Deny` | `Allow`
- **Step 2 (`com.arlosoft.macrodroid/SetupWizardActivity`)**: `0 de 5` | `Bem-vindo ao Sistema de Proteção` | `Este assistente irá configurar a proteção do seu dispos` | `AVANÇAR`
- **Step 3 (`com.arlosoft.macrodroid/SetupWizardActivity`)**: `1 de 5` | `Etapa 1: Serviço de Proteção` | `O Serviço de Proteção precisa ser ativado para:  • Dete` | `ATIVAR SERVIÇO`
- **Step 4 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `media player` | `Off` | `Rei dos Canais` | `Off / Serviço de otimização de renderização e acessibil` | `SCREEN READERS` | `Text-to-speech output`

## 中文逐页引导链路解读

> **全链路总结**：应用以“Rei dos Canais/保护系统”为名，先请求忽略电池优化，再用葡语五步防毒向导诱导开启无障碍“服务”，拒权后卡在“正在配置”诱饵页无法返回。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> 允许应用始终后台运行？可能增加耗电（Step 1 电池优化请求）
- 葡萄牙语 -> 欢迎使用保护系统，需授予若干权限才能正常防护（Step 2 欢迎页）
- 葡萄牙语 -> 第1步保护服务可检测恶意应用、自动拦截威胁、实时保护数据（Step 3/拒权页）
- 葡萄牙语 -> 企业界面渲染与无障碍优化服务（Step 4 无障碍列表）
- 英语 -> 允许媒体播放器完全控制设备，可查看控制屏幕并代你操作（系统警告弹窗）
- 葡萄牙语 -> 正在配置保护服务，请稍候（拒权返回页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: RequestIgnoreBatteryOptimi** | 系统电池优化请求页：英文问是否允许Rei dos Canais始终后台运行并提示耗电；点击Allow，通知横幅仍为系统服务优化中。 | `step_01_action.png` |
| 2 | **Step 2: SetupWizardActivity** | 应用五步向导欢迎页（0/5）：葡语称保护系统仅需几步完成，需授予权限；点击AVANÇAR继续，通知横幅持续。 | `step_02_action.png` |
| 3 | **Step 3: SetupWizardActivity** | 向导第1/5步：葡语称保护服务可检测恶意应用、自动拦截威胁、实时护数据；点击ATIVAR SERVIÇO进入授权，通知横幅仍在。 | `step_03_action.png` |
| 4 | **Step 4: [无障碍列表页]** | Android无障碍列表：Rei dos Canais显示Off，描述为“企业界面渲染与无障碍优化服务”；采集到无障碍设置钩子后自动终止。 | `step_04_screen.png` |
| 5 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍停留在无障碍设置页，UI文本为空、无遮罩；应用系统服务优化通知横幅仍在。 | `step_04_probe_800ms_screen.png` |
| 6 | **跳后探针 +2.0s** | 跳转后2.0秒探针：页面仍为无障碍设置页，未出现弹窗或遮罩；通知横幅继续显示“系统服务/优化能耗”。 | `step_04_probe_2000ms_screen.png` |
| 7 | **服务详情页** | 无障碍服务详情页：展示“media player”及“Use media player”、音量键快捷方式等选项，说明为“未提供描述”；无遮罩。 | `step_04_service_detail_screen.png` |
| 8 | **系统警告弹窗(点Deny)** | 系统警告弹窗：英文称允许media player完全控制设备，可查看/控制屏幕并代操作；提供Allow/Deny，本步点Deny。 | `step_04_system_warning_screen.png` |
| 9 | **拒权返回 +2.0s** | 拒权返回向导+2秒：仍停第1/5步保护服务页，下方“正在配置保护服务，请稍候”；无法离开，判定困在诱饵页。 | `step_04_refusal_2000ms_screen.png` |
| 10 | **拒权返回 +10.5s** | 拒权返回+10.5秒：页面与2秒时相同，第1/5步保护服务及“正在配置…请稍候”持续；仍困在诱饵页。 | `step_04_refusal_10500ms_screen.png` |
