# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:11:56
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`coy.newring.fcb`（静态标签：`malicious` / `basbanke` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`coy.newring.fcb/coy.newring.fcb.main` | hooks=`[]` | overlays=`0` | texts=`FACEBOOK ATIVAÇÃO

VOCÊ PRECISA ATIVAR O RECURSO PARA VER VISITANTES NO SEU PERFIL

Ative a permissão a seguir, para o funcionamento do sistema.

Caso você tenha dificuldades, basta procurar o nome do aplicativo na proxima janela

Configurações >  Acessibilidade > Quem viu teu perfil / OK`
- **Back 后 +5.5s**：`coy.newring.fcb/coy.newring.fcb.main` | hooks=`[]` | overlays=`0` | texts=`FACEBOOK ATIVAÇÃO

VOCÊ PRECISA ATIVAR O RECURSO PARA VER VISITANTES NO SEU PERFIL

Ative a permissão a seguir, para o funcionamento do sistema.

Caso você tenha dificuldades, basta procurar o nome do aplicativo na proxima janela

Configurações >  Acessibilidade > Quem viu teu perfil / OK`
- **Back 后 +10.5s**：`coy.newring.fcb/coy.newring.fcb.main` | hooks=`[]` | overlays=`0` | texts=`FACEBOOK ATIVAÇÃO

VOCÊ PRECISA ATIVAR O RECURSO PARA VER VISITANTES NO SEU PERFIL

Ative a permissão a seguir, para o funcionamento do sistema.

Caso você tenha dificuldades, basta procurar o nome do aplicativo na proxima janela

Configurações >  Acessibilidade > Quem viu teu perfil / OK`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `coy.newring.fcb` / `main` | `-` | 3 | 102 / 否 | `click` → [3] ImageView (click) center=(540,1899) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `coy.newring.fcb` / `main` | `-` | 2 | 286 / 否 | `click` → [2] Button text="OK" id=button1 (click) center=(887,150 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 218 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`coy.newring.fcb/main`)**: `QUEM TE VISITOU` | `Seja bem vindo !!
 
 Descubra quem visitou seu perfil c`
- **Step 2 (`coy.newring.fcb/main`)**: `FACEBOOK ATIVAÇÃO  VOCÊ PRECISA ATIVAR O RECURSO PARA V` | `OK`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Quem viu teu perfil` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用以“谁访问了你”为诱饵，先展示欢迎页并引导点击仿Facebook入口，再弹出“Facebook激活”要求到系统无障碍中开启“Quem viu teu perfil”；拒权后仍反复重弹同一诱导弹窗。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 葡萄牙语「QUEM TE VISITOU / Seja bem vindo !! Descubra quem visitou seu perfil com nosso algoritimo inteligente.」 -> 欢迎，用智能算法发现谁访问了你的主页（Step1主页面）
- 葡萄牙语「FACEBOOK ATIVAÇÃO / VOCÊ PRECISA ATIVAR O RECURSO PARA VER VISITANTES NO SEU PERFIL / Ative a permissão a seguir...」 -> Facebook激活：必须开启该功能才能查看访客，请开启以下权限（Step2及拒权后弹窗）
- 葡萄牙语「Caso você tenha dificuldades, basta procurar o nome do aplicativo na proxima janela / Configurações > Acessibilidade > Quem viu teu perfil」 -> 若找不到，就在下个窗口搜索应用名并进入设置>无障碍>Quem viu teu perfil（Step2假Facebook弹窗）
- 葡萄牙语「Ativando o recurso você tem ativação do componente. * Veja quem visitou seu perfil * Aplicativo oficial da rede * Precisamos da permissão para localizar os visitantes」 -> 开启即可查看访客、关注新访客、自称官方应用，并称需要权限定位访客（服务详情页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: main** | 主页面以“谁访问了你”为诱饵，称用智能算法发现访客；点击底部图片按钮，疑似进入仿Facebook登录入口。 | `step_01_action.png` |
| 2 | **Step 2: main** | 仿Facebook激活弹窗称必须开启权限才能查看访客，并引导到设置无障碍中搜索本应用；点击OK继续。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 跳到系统无障碍列表，已见本应用“Quem viu teu perfil”处于Off；探针捕获无障碍设置Hook后自动终止。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍停留在系统无障碍设置页，界面文本为空，无通知横幅、无遮罩覆盖。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后2.0秒探针：仍在无障碍设置页，overlays=0，无通知或弹窗，说明页面保持等待用户开启。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | 无障碍服务详情页，展示“使用Quem viu teu perfil”开关及快捷方式选项；说明文字以查看访客、官方应用、需权限为由诱导开启。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | Android高危授权弹窗，询问是否允许该应用完全控制设备，列明可读屏、可代操作；提供Allow与Deny，审核步点Deny。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 从系统授权页返回并拒绝后2秒，应用立即重弹同一仿Facebook激活弹窗，继续要求开启无障碍权限。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒绝后10.5秒，仿Facebook激活弹窗仍再次出现，形成反复施压；无通知、无遮罩，仅OK按钮引导继续。 | `step_03_refusal_10500ms_screen.png` |
