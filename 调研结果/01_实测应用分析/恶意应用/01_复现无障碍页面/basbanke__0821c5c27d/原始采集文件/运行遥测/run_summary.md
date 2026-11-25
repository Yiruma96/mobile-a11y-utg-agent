# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:05:56
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`igr.manobom.inla`（静态标签：`malicious` / `basbanke` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`igr.manobom.inla/igr.manobom.inla.main` | hooks=`[]` | overlays=`0` | texts=`INSTAGRAM ATIVAÇÃO RECURSO

VOCÊ PRECISA ATIVAR O RECURSO PARA ATIVAR A FUNÇÃO

Ative a permissão a seguir, para evitar erros no instagram.

Caso você tenha dificuldades pode procurar nosso suporte oficial para auxiliar

Configurações >  Acessibilidade > Quem te visitou / OK`
- **Back 后 +5.5s**：`igr.manobom.inla/igr.manobom.inla.main` | hooks=`[]` | overlays=`0` | texts=`INSTAGRAM ATIVAÇÃO RECURSO

VOCÊ PRECISA ATIVAR O RECURSO PARA ATIVAR A FUNÇÃO

Ative a permissão a seguir, para evitar erros no instagram.

Caso você tenha dificuldades pode procurar nosso suporte oficial para auxiliar

Configurações >  Acessibilidade > Quem te visitou / OK`
- **Back 后 +10.5s**：`igr.manobom.inla/igr.manobom.inla.main` | hooks=`[]` | overlays=`0` | texts=`INSTAGRAM ATIVAÇÃO RECURSO

VOCÊ PRECISA ATIVAR O RECURSO PARA ATIVAR A FUNÇÃO

Ative a permissão a seguir, para evitar erros no instagram.

Caso você tenha dificuldades pode procurar nosso suporte oficial para auxiliar

Configurações >  Acessibilidade > Quem te visitou / OK`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `igr.manobom.inla` / `main` | `-` | 1 | 14 / 是 | `click` → [1] TextView text="ATIVAR RECURSO" (click) center=(533, | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `igr.manobom.inla` / `main` | `-` | 2 | 272 / 否 | `click` → [2] Button text="OK" id=button1 (click) center=(887,150 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 214 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`igr.manobom.inla/main`)**: `ATIVAR RECURSO`
- **Step 2 (`igr.manobom.inla/main`)**: `INSTAGRAM ATIVAÇÃO RECURSO  VOCÊ PRECISA ATIVAR O RECUR` | `OK`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Quem te visitou` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用以葡萄牙语伪称激活 Instagram“谁访问了你”功能，先弹说明再跳转系统无障碍设置，诱导开启“Quem te visitou”服务；用户拒绝后仍反复重弹同一诱导弹窗（RELAUNCHED_LURE_DIALOG）。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- ATIVAR RECURSO -> 激活功能（step_01 主启动页）
- INSTAGRAM ATIVAÇÃO RECURSO... Configurações > Acessibilidade > Quem te visitou -> Instagram 功能激活：必须激活该功能，开启以下权限以避免 Instagram 错误，困难可找官方支持，路径为设置>无障碍>谁访问了你（step_02 主界面弹窗）
- Ativando o recurso você tem ativação do componente... -> 启用功能即激活组件，全网络可用，有疑问联系支持，系官方应用，需权限以运行算法（服务详情页）
- Allow Quem te visitou to have full control of your device? -> 允许“谁访问了你”完全控制你的设备？可查看控制屏幕、读取全部屏幕内容并悬浮显示、跟踪交互并代你操作（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: main** | 主启动页仅显示“ATIVAR RECURSO/激活功能”按钮，代理点击进入权限引导；无通知横幅、无遮罩。 | `step_01_action.png` |
| 2 | **Step 2: main** | 主界面弹出葡萄牙语“Instagram 功能激活”说明，要求去无障碍开启“Quem te visitou”，点击 OK 继续；无遮罩/通知。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 系统无障碍列表显示已下载应用“Quem te visitou/谁访问了你”且关闭；探针命中后自动终止，无遮罩。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转后 0.8 秒探针仍停留在无障碍设置页，界面文本为空、遮罩数为 0，未见弹窗或通知横幅。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后 2.0 秒探针仍在无障碍设置页，未捕获界面文本、遮罩为 0，未出现新弹窗或通知。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | 进入“Quem te visitou”服务详情，葡萄牙语称启用组件、全网络可用、官方应用并需权限运行算法；诱导开启无障碍服务。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 系统警告询问是否允许“Quem te visitou”完全控制设备，列明读屏、悬浮、跟踪并代操作，提供 Allow/Deny；本步仅检查。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 点拒绝返回应用后 2 秒，主页再次弹出同一“激活 Instagram 功能”诱导弹窗，出现 RELAUNCHED_LURE_DIALOG，未降级为普通页。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权后 10.5 秒应用仍反复重弹同一葡萄牙语激活/无障碍引导弹窗，标记 RELAUNCHED_LURE_DIALOG，持续施压用户授权。 | `step_03_refusal_10500ms_screen.png` |
