# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:50:55
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`coyzin.lasterm.malanko`（静态标签：`malicious` / `basbanke` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`coyzin.lasterm.malanko/coyzin.lasterm.malanko.main` | hooks=`[]` | overlays=`0` | texts=`CleanDroid

VOCÊ PRECISA ATIVAR O RECURSO PARA UTILIZAR O CLEAN DROID

Ative a permissão a seguir!.

Caso você esteja com dificuldades pode procurar nosso suporte para auxiliar.

Configurações >  Acessibilidade > CleanDroid / OK`
- **Back 后 +5.5s**：`coyzin.lasterm.malanko/coyzin.lasterm.malanko.main` | hooks=`[]` | overlays=`0` | texts=`CleanDroid

VOCÊ PRECISA ATIVAR O RECURSO PARA UTILIZAR O CLEAN DROID

Ative a permissão a seguir!.

Caso você esteja com dificuldades pode procurar nosso suporte para auxiliar.

Configurações >  Acessibilidade > CleanDroid / OK`
- **Back 后 +10.5s**：`coyzin.lasterm.malanko/coyzin.lasterm.malanko.main` | hooks=`[]` | overlays=`0` | texts=`CleanDroid

VOCÊ PRECISA ATIVAR O RECURSO PARA UTILIZAR O CLEAN DROID

Ative a permissão a seguir!.

Caso você esteja com dificuldades pode procurar nosso suporte para auxiliar.

Configurações >  Acessibilidade > CleanDroid / OK`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `coyzin.lasterm.malanko` / `main` | `-` | 2 | 6 / 是 | `click` → [2] TextView text="ATIVAR" (click) center=(538,1868) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `coyzin.lasterm.malanko` / `main` | `-` | 2 | 225 / 否 | `click` → [2] Button text="OK" id=button1 (click) center=(887,148 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 209 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`coyzin.lasterm.malanko/main`)**: `ATIVAR`
- **Step 2 (`coyzin.lasterm.malanko/main`)**: `CleanDroid  VOCÊ PRECISA ATIVAR O RECURSO PARA UTILIZAR` | `OK`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `CleanDroid` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：主页面以“ATIVAR”按钮诱导进入教程弹窗，声称必须开启CleanDroid无障碍服务并跳转系统设置；在服务详情页与系统高危警告中继续施压，用户拒绝后应用反复重启同一诱导弹窗。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 葡萄牙语“ATIVAR” -> “激活”按钮，作为入口诱导点击（主页面）
- 葡萄牙语“VOCÊ PRECISA ATIVAR O RECURSO PARA UTILIZAR O CLEAN DROID...” -> “您必须激活该功能才能使用CleanDroid；请激活以下权限；如遇困难可联系支持；设置>无障碍>CleanDroid”（教程弹窗）
- 葡萄牙语“Ativando o recurso você tem ativação do seu recurso...” -> “激活此功能即可启用；如有疑问联系支持；官方网络应用；需要权限才能运行”（服务详情页）
- 英语“Allow CleanDroid to have full control of your device?” -> “允许CleanDroid完全控制您的设备？”（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: main** | 主页面仅见葡萄牙语“ATIVAR”（激活）按钮，作为入口诱导点击；无通知/遮罩，点击后触发无障碍授权引导。 | `step_01_action.png` |
| 2 | **Step 2: main** | 教程弹窗称必须激活CleanDroid功能，否则无法使用，并指引到设置>无障碍>CleanDroid；点“OK”跳系统无障碍页。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 系统无障碍列表显示CleanDroid为Off，页面有下载应用等项；探针在此捕获无障碍钩子后自动终止，无通知/遮罩。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍停留系统无障碍设置页，无通知横幅、无遮罩，未出现额外诱导界面。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后2.0秒探针：系统无障碍页保持静止，遮罩数0、通知为空，未见自动点击或浮层。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | 服务详情页显示“Use CleanDroid”开关与快捷键选项；葡语说明称激活后可用、需权限运行，属官方应用，并引导开启。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 系统高危警告要求允许CleanDroid完全控制设备，可读屏、显示悬浮层并代操作；含Allow/Deny，点Deny拒权。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 拒权返回2秒后，应用重新弹出同一葡语教程弹窗，反复要求激活无障碍权限；无通知/遮罩，属拒权后重试诱导。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权返回10.5秒后教程弹窗仍持续存在，重复“必须激活”话术并仅给OK，形成循环施压，未新增通知/遮罩。 | `step_03_refusal_10500ms_screen.png` |
