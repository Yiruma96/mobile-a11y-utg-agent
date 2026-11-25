# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:43:39
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`camilo.whienal.coyzim`（静态标签：`malicious` / `basbanke` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`camilo.whienal.coyzim/camilo.whienal.coyzim.main` | hooks=`[]` | overlays=`0` | texts=`Férias Decolar

VOCÊ PRECISA ATIVAR O RECURSO PARA UTILIZAR O PLUGIN

Ative a permissão a seguir!.

Caso você esteja com dificuldades pode procurar nosso suporte para auxiliar.

Configurações >  Acessibilidade > Férias Decolar / OK`
- **Back 后 +5.5s**：`camilo.whienal.coyzim/camilo.whienal.coyzim.main` | hooks=`[]` | overlays=`0` | texts=`Férias Decolar

VOCÊ PRECISA ATIVAR O RECURSO PARA UTILIZAR O PLUGIN

Ative a permissão a seguir!.

Caso você esteja com dificuldades pode procurar nosso suporte para auxiliar.

Configurações >  Acessibilidade > Férias Decolar / OK`
- **Back 后 +10.5s**：`camilo.whienal.coyzim/camilo.whienal.coyzim.main` | hooks=`[]` | overlays=`0` | texts=`Férias Decolar

VOCÊ PRECISA ATIVAR O RECURSO PARA UTILIZAR O PLUGIN

Ative a permissão a seguir!.

Caso você esteja com dificuldades pode procurar nosso suporte para auxiliar.

Configurações >  Acessibilidade > Férias Decolar / OK`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `camilo.whienal.coyzim` / `main` | `-` | 2 | 6 / 是 | `click` → [2] TextView text="ATIVAR" (click) center=(538,1868) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `camilo.whienal.coyzim` / `main` | `-` | 2 | 228 / 否 | `click` → [2] Button text="OK" id=button1 (click) center=(887,148 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 213 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`camilo.whienal.coyzim/main`)**: `ATIVAR`
- **Step 2 (`camilo.whienal.coyzim/main`)**: `Férias Decolar  VOCÊ PRECISA ATIVAR O RECURSO PARA UTIL` | `OK`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Férias Decolar` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用以“Férias Decolar”插件入口点击 ATIVAR 启动流程，用葡萄牙语弹窗反复引导用户前往系统无障碍设置开启完全控制权限；详情页借 Outback 票券福利强化授权动机，用户点 Deny 拒权后应用仍重弹同一诱导弹窗。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- ATIVAR（葡萄牙语）-> 激活（主界面入口按钮）
- VOCÊ PRECISA ATIVAR O RECURSO PARA UTILIZAR O PLUGIN / Ative a permissão a seguir! / Configurações > Acessibilidade > Férias Decolar（葡萄牙语）-> 您需要激活该资源才能使用插件；请激活以下权限！设置>无障碍>Férias Decolar（授权说明弹窗）
- Use Férias Decolar（葡萄牙语/产品名）-> 使用 Férias Decolar（无障碍服务详情页开关说明）
- Ticket Outback: Ativando o recurso você tem ativação do seu ticket / Varios ticket por semana / Descontos de 20R$ até 190R$ / Precisamos da permissão para evitar que seu ticket seja usado por outros clientes（葡萄牙语）-> 激活资源即可激活票券；每周多张票券；20至190雷亚尔折扣；需要权限防止票券被他人使用（服务详情页）
- Allow Férias Decolar to have full control of your device? / View and control screen / View and perform actions / Allow / Deny（英语）-> 允许 Férias Decolar 完全控制您的设备吗？可查看并控制屏幕、查看并执行操作/代为交互；允许/拒绝（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: main** | 主界面仅见葡萄牙语按钮“ATIVAR”；点击后启动诱导流程，无通知横幅、无遮罩，下一步将弹出授权说明弹窗。 | `step_01_action.png` |
| 2 | **Step 2: main** | 主界面弹出说明弹窗，标题“Férias Decolar”，称必须激活资源/权限，并指引前往设置>无障碍>Férias Decolar；点击 OK 关闭继续。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 系统无障碍列表页，DOWNLOADED APPS 下可见“Férias Decolar”开关为 Off；应用在此触发无障碍设置钩子后自动终止，未授权。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍停留在系统无障碍设置页，界面文本为空，overlays=0，无通知横幅或悬浮遮罩，等待未见变化。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后2.0秒探针：系统无障碍设置页保持无文本、无通知、无遮罩（overlays=0），未出现二次跳转或弹窗。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | 无障碍服务详情页：显示“Use Férias Decolar”及选项；下方用“Ticket Outback”票券福利和防他人使用话术，诱使开启完全控制权限。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 系统授权警告弹窗：英文询问是否允许“Férias Decolar”完全控制设备，列明可读屏、覆盖显示、代操作等风险，含 Allow/Deny；本步点 Deny。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 拒绝授权返回后2秒，应用再次弹出同一葡萄牙语诱导弹窗，坚称必须激活权限并给设置路径，仅 OK 按钮，形成反复施压。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒绝后10.5秒仍停留在同一诱导弹窗，未进入功能页；说明应用在拒权后持续重弹，逼迫用户前往无障碍设置授权。 | `step_03_refusal_10500ms_screen.png` |
