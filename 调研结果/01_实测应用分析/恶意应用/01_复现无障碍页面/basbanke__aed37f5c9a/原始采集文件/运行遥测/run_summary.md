# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:27:18
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`pine.coyzinhu.infee`（静态标签：`malicious` / `basbanke` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`pine.coyzinhu.infee/pine.coyzinhu.infee.main` | hooks=`[]` | overlays=`0` | texts=`MAX CUPONS

VOCÊ PRECISA ATIVAR O RECURSO PARA VALIDAR SEU TICKET

Ative a permissão a seguir, para evitar compartilhamento do seu ticket.

Caso você esteja em um estabelecimento você pode procurar um de nossos funcionários para auxiliar.

Configurações >  Acessibilidade > Max Cupons / OK`
- **Back 后 +5.5s**：`pine.coyzinhu.infee/pine.coyzinhu.infee.main` | hooks=`[]` | overlays=`0` | texts=`MAX CUPONS

VOCÊ PRECISA ATIVAR O RECURSO PARA VALIDAR SEU TICKET

Ative a permissão a seguir, para evitar compartilhamento do seu ticket.

Caso você esteja em um estabelecimento você pode procurar um de nossos funcionários para auxiliar.

Configurações >  Acessibilidade > Max Cupons / OK`
- **Back 后 +10.5s**：`pine.coyzinhu.infee/pine.coyzinhu.infee.main` | hooks=`[]` | overlays=`0` | texts=`MAX CUPONS

VOCÊ PRECISA ATIVAR O RECURSO PARA VALIDAR SEU TICKET

Ative a permissão a seguir, para evitar compartilhamento do seu ticket.

Caso você esteja em um estabelecimento você pode procurar um de nossos funcionários para auxiliar.

Configurações >  Acessibilidade > Max Cupons / OK`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `pine.coyzinhu.infee` / `main` | `-` | 7 | 169 / 否 | `click` → [7] TextView text="Ativar Cupom!!" (click) center=(539, | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `pine.coyzinhu.infee` / `main` | `-` | 2 | 286 / 否 | `click` → [2] Button text="OK" id=button1 (click) center=(887,153 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 209 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`pine.coyzinhu.infee/main`)**: `Max Cupons!!` | `Webpage not available` | `x+AAAAAElFTkSuQmCC` | `The webpage at http://80.82.67.246/MaxCupons/ could not` | `net::ERR_INTERNET_DISCONNECTED` | `Ativar Cupom!!`
- **Step 2 (`pine.coyzinhu.infee/main`)**: `MAX CUPONS  VOCÊ PRECISA ATIVAR O RECURSO PARA VALIDAR ` | `OK`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Max Cupons` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用以“Max Cupons”优惠券/门票为名，先显示远程IP网页加载失败，再以激活门票、防止门票被共享为由，用葡语弹窗引导用户前往系统无障碍设置；用户拒权后仍反复重弹同一诱导框，核心目的是骗取无障碍完全控制权限。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 葡萄牙语/英语 -> “Max Cupons!! / Ativar Cupom!!”：最大优惠券！/ 激活优惠券！！（Step 1 主页面）
- 葡萄牙语 -> “VOCÊ PRECISA ATIVAR O RECURSO PARA VALIDAR SEU TICKET... Configurações > Acessibilidade > Max Cupons”：您需要激活该功能以验证门票；请开启以下权限，以免您的门票被共享；在店内可找员工协助；设置>无障碍>Max Cupons（Step 2 原生弹窗）
- 葡萄牙语 -> “Ativando o recurso você tem ativação do seu ticket... Precisamos da permissão para evitar que seu ticket seja usado por outros clientes”：开启功能即可激活门票；每周多张门票；20至190雷亚尔折扣；有问题找支持；官方应用；需要权限防止门票被他人使用（服务详情页）
- 英语/系统文案 -> “Allow Max Cupons to have full control of your device? ... View and control screen ... View and perform actions ... Allow / Deny”：允许Max Cupons完全控制设备？可查看并控制屏幕、查看并执行操作；允许/拒绝（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: main** | 主页以Max Cupons优惠券为入口，网页报断网无法加载远程IP，仍留“Ativar Cupom!!”按钮；点击触发无障碍授权提示。 | `step_01_action.png` |
| 2 | **Step 2: main** | 原生葡语弹窗称必须激活无障碍功能以验证门票并防止门票被共享，指引前往设置>无障碍>Max Cupons；点击OK继续。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 跳转至系统无障碍列表，已下载应用中出现Max Cupons且状态为Off；探针捕获无障碍设置钩子后自动终止，无通知与遮罩。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍停留系统无障碍列表页，无新增UI文本，通知为空、overlays=0，未见遮罩。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后2.0秒探针：仍停留系统无障碍列表页，无新增UI文本，通知为空、overlays=0，未见遮罩。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | 服务详情页显示“Use Max Cupons”及快捷选项；葡语说明以多张门票、20至190雷亚尔折扣、防他人使用为由诱导开启无障碍。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 系统警告称将授予Max Cupons完全控制设备，可读取屏幕、覆盖应用并代操作，含Allow/Deny；本步仅检视未确认。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 拒权返回2秒后，应用重弹同一葡语诱导框，称需激活无障碍以验证门票并防共享，再次给出OK；overlays=0。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权返回10.5秒后仍反复重弹同一葡语诱导框，持续要求开启无障碍验证门票；overlays=0，未提供取消退出。 | `step_03_refusal_10500ms_screen.png` |
