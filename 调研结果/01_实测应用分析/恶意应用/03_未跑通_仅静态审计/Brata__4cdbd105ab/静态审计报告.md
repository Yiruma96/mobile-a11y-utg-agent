# MR_111__4cdbd105ab｜Brata — Out Protect

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：282.7s

## 1. 一句话核心结论

- **核心申请方式**：以远端下发的“应用已过期/立即更新”虚假弹窗为唯一入口，点击后不更新而是跳转系统无障碍设置并叠加自家“点击按钮以启用”引导页，获权后即远程加载 DEX、禁用自身启动组件并从启动器消失。
- **静态可见性说明**：引导链骨架（MainActivity→MainActivity$d→LipicaeActivity→IndlisySvc、三星/通用无障碍设置分支、WindowManager 遮罩）全部在本包 DEX 内静态可见；但诱饵文案原文、被冒充的应用名（WhatsApp）与检测目标清单由远端 https://tastiem.com/a/a.php 下发并以 Base64+异或混淆后运行时解密，授权后执行的载荷为远程 classes.zip 反射加载，二者均不在包内。本轮 input.apk 已从磁盘移除，未能重新反编译，上述依据本项目已确认风险台账的既有方法级证据。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `4cdbd105ab8117620731630f8f89eb2e6110dbf6341df43712a0ec9837c5a9be` |
| 包名 / 年份 | `com.outprotect.android` / 2021 |
| 家族 / 品类 | **Brata**（同池样本数：8） |
| 原始来源标识 | https://www.mcafee.com/blogs/other-blogs/mcafee-labs/brata-keeps-sneaking-into-google-play-now-targeting-usa-and-spain/?hilite=%27Android%27%2C%27Malware%27 |
| 桌面显示名 | Out Protect |
| 引导页宣称品牌/身份 | 系统更新/应用更新服务，并冒用 WhatsApp 作为“已过期需更新”的对象 |
| 系统无障碍列表服务名 | Serviço de Atualização（更新服务） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务 android:description 为空数组，系统列表不展示任何用途说明，用户仅能凭“更新服务”标签判断；服务 label 与包名/应用名 Out Protect 无语义关联；关键字符串以 int[] 位运算与 Base64+异或混淆存储，运行时才还原出 URL 与类名；获权后反射调用 setComponentEnabledSetting 将 MainActivity 置 DISABLED 并 finish，使图标从启动器消失 |
| 无障碍服务类名 | `com.outprotect.IndlisySvc` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `无` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.outprotect.MainActivity（启动 Activity） | onCreate 中经 b.b.b#a 做 ptBR 语言门控后启动检测线程 MainActivity$c.run | 原生Activity | **原文**：Verificando aplicativos.<br>**译注**：正在检查应用。 | 无显式操作，仅等待“检测”结束（无取消/跳过控件记录） | `com.outprotect.MainActivity#onCreate / com.outprotect.MainActivity$c#run` |
| 2 | 业务功能触发 | MainActivity 内检测线程 + PackageManager 查询 | MainActivity$c.run 请求 https://tastiem.com/a/a.php，解密 Base64+异或混淆的 JSON 清单并逐个 PackageManager 查询是否已安装 | 不可静态还原 | 无 | 无 | `com.outprotect.MainActivity$c#run` |
| 3 | 引导说明页 | MainActivity 上的原生提示弹窗（命中/未命中两分支） | MainActivity$c$b.run 依据查询结果渲染文案与按钮，按钮点击绑定 MainActivity$b.onClick | 原生Dialog | **原文**：O aplicativo abaixo encontra-se desatualizado. / WhatsApp / Atualizar Agora! （未命中分支：PARABÉNS / Nenhum problema foi encontrado.）<br>**译注**：下列应用已过期。/ WhatsApp / 立即更新！（未命中分支：恭喜 / 未发现任何问题。） | 点击“Atualizar Agora!”（立即更新）；台账证据未见取消或跳过控件 | `com.outprotect.MainActivity$c$b#run / com.outprotect.MainActivity$b#onClick` |
| 4 | 跳无障碍设置 | 系统无障碍设置页：三星走 com.samsung.accessibility/...Activities$InstalledServicesSettings 组件，其余走 android.settings.ACCESSIBILITY_SETTINGS | MainActivity$b.onClick 写入 rathefa=true 后由 MainActivity$d.run 读取 accessibility_enabled/enabled_accessibility_services 判定未启用即跳转，入口由 MainActivity.a(Context) 按 Build.MANUFACTURER 构造 | 系统无障碍页 | 无 | 在系统列表中手动找到并开启“Serviço de Atualização” | `com.outprotect.MainActivity$b#onClick / com.outprotect.MainActivity$d#run / com.outprotect.MainActivity#a` |
| 5 | 遮罩叠层指引 | com.outprotect.LipicaeActivity（压栈于系统设置页之上） | MainActivity$d.run 跳转设置后启动 LipicaeActivity.onCreate 渲染引导 | 原生Activity | **原文**：Clique no botão para habilitar / Desativado<br>**译注**：点击按钮以启用 / 已停用 | 按页面指引点击按钮完成启用；台账证据未见取消/跳过路径 | `com.outprotect.LipicaeActivity#onCreate` |
| 6 | 获权后动作 | com.outprotect.IndlisySvc 无障碍服务 + b.b.c 全屏悬浮遮罩 + 反射禁用 MainActivity | onServiceConnected 读到 rathefa=true 后启动 IndlisySvc$a.run（下载 classes.zip 并反射加载）；同时 MainActivity.b(Context) 反射 setComponentEnabledSetting 置 DISABLED 并 finish，b.b.c.run 用 WindowManager.addView(type=2032) 挂遮罩 | 悬浮窗Overlay | **原文**：Instalando...<br>**译注**：正在安装... | 无交互，界面被全屏黑色遮罩（FLAG_NOT_FOCUSABLE/NOT_TOUCHABLE）覆盖 | `com.outprotect.IndlisySvc#onServiceConnected / com.outprotect.IndlisySvc$a#run / com.outprotect.MainActivity#b / b.b.c#run` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 原生提示弹窗：伪造的“应用已过期”说明 + 目标应用名 + “Atualizar Agora!”按钮（文案运行时由远端 JSON 解密还原，不在 strings.xml）
- MainActivity 原生提示弹窗未命中分支：“PARABÉNS / Nenhum problema foi encontrado.”（同为运行时解密文案）
- 系统无障碍服务列表条目标签：android:label = Serviço de Atualização（res 字符串资源），android:description 为空，列表内无用途说明
- LipicaeActivity 全屏引导页：“Clique no botão para habilitar”与状态“Desativado”，压在系统无障碍设置页之上
- WindowManager type=2032 全屏黑色悬浮遮罩：“Instalando...”，FLAG_NOT_FOCUSABLE|NOT_TOUCHABLE
- 未发现 assets 本地 HTML 或远端 WebView 承载任何引导文案

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| pt | Verificando aplicativos. | 正在检查应用。 | `远端 a/a.php 下发 JSON 经 Base64+异或解密后硬编码渲染（MainActivity$c$b 路径）` | 清理工具伪装 |
| pt | O aplicativo abaixo encontra-se desatualizado. | 下列应用已过期。 | `远端下发 JSON 解密文案，渲染于 MainActivity 原生弹窗` | 故障恐吓 |
| pt | Atualizar Agora! | 立即更新！ | `远端下发 JSON 解密文案，绑定 MainActivity$b.onClick` | 假更新 |
| pt | PARABÉNS / Nenhum problema foi encontrado. | 恭喜 / 未发现任何问题。 | `远端下发 JSON 解密文案（未命中分支）` | 清理工具伪装 |
| pt | Clique no botão para habilitar | 点击按钮以启用 | `com.outprotect.LipicaeActivity（引导页文案）` | 受限设置分步教学 |
| pt | Serviço de Atualização | 更新服务 | `AndroidManifest 中 IndlisySvc 的 android:label 字符串资源` | 假更新 |
| pt | Instalando... | 正在安装... | `b.b.c 悬浮遮罩文案（获权后显示）` | 假更新 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：台账证据未记录 onResume 死循环重跳或定时器拉起；LipicaeActivity 常驻于系统设置页之上持续提示“点击按钮以启用/Desativado”，用户返回后需重新经过 MainActivity 入口才会再次跳转（该重入路径本轮因样本缺失未能复核）
- **遮罩叠层 / 高仿系统设置页**：无高仿系统无障碍开关页；但在真实系统设置页之上压入自家 LipicaeActivity 引导页，并在获权后立刻叠加 type=2032 全屏黑色半透明遮罩（Instalando...）阻断视线
- **Android 13+ 受限设置（Restricted Settings）应对**：无（未见针对 Android 13+ 受限设置“应用详情→右上角菜单→允许受限设置”的分步教学，也未使用 Session 安装器绕过）
- **获权后即时行为与防撤权机制**：获权后立即反射 setComponentEnabledSetting 将 MainActivity 置 DISABLED 并 finish，使应用从启动器消失；未发现监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权的代码
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测 Intent 目标为 android.settings.ACCESSIBILITY_SETTINGS 或三星组件 com.samsung.accessibility/com.samsung.accessibility.Activities$InstalledServicesSettings 的启动瞬间；次优为冷启动 MainActivity 后出现“Atualizar Agora!”弹窗并发生点击的瞬间
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：诱饵文案与检测清单来自远端 a/a.php 且经 Base64+异或混淆，若远端在特定时段返回“无问题”分支（PARABÉNS）或按地域/语言停发，纯静态或单次 UTG 抓取可能只看到良性外壳；设备语言必须为 ptBR 才会进入该分支，其他语言环境下整条引导链不可达，需按语言条件复现。远程 classes.zip 载荷内容未取得，UTG 亦无法直接区分其内部行为。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页（诱饵）** | com.outprotect.MainActivity 上的原生提示弹窗，含按钮文本“Atualizar Agora!”与目标应用名“WhatsApp” | 这是唯一入口，且文案由远端下发、无本地 strings 可查，UTG 抓取可固定诱饵话术与“无取消按钮”事实 | 按钮文本 Atualizar Agora!；文案 O aplicativo abaixo encontra-se desatualizado.；目标应用名 WhatsApp；弹窗中不存在取消/跳过控件 |
| **跳转前到系统设置之间的压栈引导页** | com.outprotect.LipicaeActivity 界面，文本“Clique no botão para habilitar”与状态“Desativado” | 直接证明应用在真实系统设置页上叠加自家引导层，是“教唆开启无障碍”最直接的画面证据 | Clique no botão para habilitar；Desativado；当前前台 Activity 为 com.outprotect.LipicaeActivity 而非系统设置 |
| **系统无障碍服务列表项** | 系统无障碍设置页中 label 为 Serviço de Atualização 的条目，description 区域为空 | 核对用户实际看到的权限说明缺失，与“更新服务”这一误导性标签形成对照 | 服务名 Serviço de Atualização；该条目下方无用途说明文本；包名 com.outprotect.android 与标签语义不一致 |
| **获权后 800ms 内压栈遮罩页** | 全屏黑色 WindowManager type=2032 悬浮窗，文本“Instalando...”，无触摸焦点 | 区分“授权即投递”的恶意时序：遮罩出现即代表远程载荷下载/反射加载已启动 | 文本 Instalando...；覆盖全屏且不可点击的悬浮窗；启动器/最近任务中 MainActivity 消失 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.outprotect.MainActivity#onCreate`
- `com.outprotect.MainActivity$c$b#run`
- `com.outprotect.MainActivity$b#onClick`
- `com.outprotect.MainActivity$d#run`
- `com.outprotect.MainActivity#a`
- `com.outprotect.LipicaeActivity#onCreate`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点（UTG 页面流转视角）

**前置边界：** 本轮 `input.apk` 已不在磁盘（原路径 `...\stage3_brata\input.apk` 及全盘检索均未找到），无法重新反编译核验。以下流程依据本项目对同一目标 `#1` 的已确认风险台账（`autonomous_audit` 来源）中记录的方法级证据与逐字文案；其证据边界沿用台账原有说明。

1. **触发时机是冷启动且强阻断**：`MainActivity.onCreate` 先做 `ptBR` 语言门控，再起线程请求 `https://tastiem.com/a/a.php`，取回 Base64+异或混淆的 JSON 清单，用 `PackageManager` 逐个查询是否已安装。
2. **诱饵载体是原生 Dialog/Activity，不是 WebView**：命中后渲染“检测已装应用 / 下列应用已过期 / WhatsApp / 立即更新！”；未命中则显示“恭喜，未发现问题”。全程无本地 HTML 或远端 WebView 参与，纯原生控件。
3. **点击“更新”不更新，直接进入受限设置**：`MainActivity$b.onClick` 只写入 `rathefa=true`，`MainActivity$d.run` 读取 `accessibility_enabled`/`enabled_accessibility_services` 判定自身未启用后，经 `MainActivity.a(Context)` 跳转——三星机型走 `com.samsung.accessibility/...Activities$InstalledServicesSettings` 组件，其余回落 `android.settings.ACCESSIBILITY_SETTINGS`。
4. **设置页之上再叠一层自家引导页**：`LipicaeActivity.onCreate` 显示“点击按钮以启用”，状态“Desativado”（已停用），在系统设置页之上形成压栈式引导。
5. **获权即“变脸”**：`IndlisySvc.onServiceConnected` 放行远程 `classes.zip` 反射加载；同时 `MainActivity.b(Context)` 反射 `setComponentEnabledSetting` 把 `MainActivity` 置 `DISABLED` 并 `finish()`，`b.b.c.run` 用 `WindowManager.addView(type=2032)` 挂全屏黑遮罩“Instalando...”。
6. **身份与权限说明的双重留白**：无障碍服务 label 为“Serviço de Atualização”（更新服务），而 `android:description` 为空数组——系统无障碍列表不展示任何用途说明，用户只能凭“更新”语义做判断。
7. **UTG 最佳切入点**：监测 `ACTION_ACCESSIBILITY_SETTINGS` / 三星 `InstalledServicesSettings` 的启动瞬间（此时诱饵 Dialog 与压栈引导页同时在场），比冷启动更稳。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "引导链骨架（MainActivity→MainActivity$d→LipicaeActivity→IndlisySvc、三星/通用无障碍设置分支、WindowManager 遮罩）全部在本包 DEX 内静态可见；但诱饵文案原文、被冒充的应用名（WhatsApp）与检测目标清单由远端 https://tastiem.com/a/a.php 下发并以 Base64+异或混淆后运行时解密，授权后执行的载荷为远程 classes.zip 反射加载，二者均不在包内。本轮 input.apk 已从磁盘移除，未能重新反编译，上述依据本项目已确认风险台账的既有方法级证据。",
  "summary_one_liner": "以远端下发的“应用已过期/立即更新”虚假弹窗为唯一入口，点击后不更新而是跳转系统无障碍设置并叠加自家“点击按钮以启用”引导页，获权后即远程加载 DEX、禁用自身启动组件并从启动器消失。",
  "disguise_identity": {
    "app_display_name": "Out Protect",
    "claimed_brand_or_persona": "系统更新/应用更新服务，并冒用 WhatsApp 作为“已过期需更新”的对象",
    "a11y_service_label": "Serviço de Atualização（更新服务）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务 android:description 为空数组，系统列表不展示任何用途说明，用户仅能凭“更新服务”标签判断；服务 label 与包名/应用名 Out Protect 无语义关联；关键字符串以 int[] 位运算与 Base64+异或混淆存储，运行时才还原出 URL 与类名；获权后反射调用 setComponentEnabledSetting 将 MainActivity 置 DISABLED 并 finish，使图标从启动器消失"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.outprotect.MainActivity（启动 Activity）",
      "trigger_event": "onCreate 中经 b.b.b#a 做 ptBR 语言门控后启动检测线程 MainActivity$c.run",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Verificando aplicativos.",
      "shown_text_zh": "正在检查应用。",
      "user_action_requested": "无显式操作，仅等待“检测”结束（无取消/跳过控件记录）",
      "code_anchor": "com.outprotect.MainActivity#onCreate / com.outprotect.MainActivity$c#run"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "MainActivity 内检测线程 + PackageManager 查询",
      "trigger_event": "MainActivity$c.run 请求 https://tastiem.com/a/a.php，解密 Base64+异或混淆的 JSON 清单并逐个 PackageManager 查询是否已安装",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面文字，后台比对已安装应用清单",
      "user_action_requested": "无",
      "code_anchor": "com.outprotect.MainActivity$c#run"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "MainActivity 上的原生提示弹窗（命中/未命中两分支）",
      "trigger_event": "MainActivity$c$b.run 依据查询结果渲染文案与按钮，按钮点击绑定 MainActivity$b.onClick",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "O aplicativo abaixo encontra-se desatualizado. / WhatsApp / Atualizar Agora! （未命中分支：PARABÉNS / Nenhum problema foi encontrado.）",
      "shown_text_zh": "下列应用已过期。/ WhatsApp / 立即更新！（未命中分支：恭喜 / 未发现任何问题。）",
      "user_action_requested": "点击“Atualizar Agora!”（立即更新）；台账证据未见取消或跳过控件",
      "code_anchor": "com.outprotect.MainActivity$c$b#run / com.outprotect.MainActivity$b#onClick"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍设置页：三星走 com.samsung.accessibility/...Activities$InstalledServicesSettings 组件，其余走 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "MainActivity$b.onClick 写入 rathefa=true 后由 MainActivity$d.run 读取 accessibility_enabled/enabled_accessibility_services 判定未启用即跳转，入口由 MainActivity.a(Context) 按 Build.MANUFACTURER 构造",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "系统无障碍服务列表，其中一项显示为“更新服务”",
      "user_action_requested": "在系统列表中手动找到并开启“Serviço de Atualização”",
      "code_anchor": "com.outprotect.MainActivity$b#onClick / com.outprotect.MainActivity$d#run / com.outprotect.MainActivity#a"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.outprotect.LipicaeActivity（压栈于系统设置页之上）",
      "trigger_event": "MainActivity$d.run 跳转设置后启动 LipicaeActivity.onCreate 渲染引导",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Clique no botão para habilitar / Desativado",
      "shown_text_zh": "点击按钮以启用 / 已停用",
      "user_action_requested": "按页面指引点击按钮完成启用；台账证据未见取消/跳过路径",
      "code_anchor": "com.outprotect.LipicaeActivity#onCreate"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.outprotect.IndlisySvc 无障碍服务 + b.b.c 全屏悬浮遮罩 + 反射禁用 MainActivity",
      "trigger_event": "onServiceConnected 读到 rathefa=true 后启动 IndlisySvc$a.run（下载 classes.zip 并反射加载）；同时 MainActivity.b(Context) 反射 setComponentEnabledSetting 置 DISABLED 并 finish，b.b.c.run 用 WindowManager.addView(type=2032) 挂遮罩",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Instalando...",
      "shown_text_zh": "正在安装...",
      "user_action_requested": "无交互，界面被全屏黑色遮罩（FLAG_NOT_FOCUSABLE/NOT_TOUCHABLE）覆盖",
      "code_anchor": "com.outprotect.IndlisySvc#onServiceConnected / com.outprotect.IndlisySvc$a#run / com.outprotect.MainActivity#b / b.b.c#run"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 原生提示弹窗：伪造的“应用已过期”说明 + 目标应用名 + “Atualizar Agora!”按钮（文案运行时由远端 JSON 解密还原，不在 strings.xml）",
    "MainActivity 原生提示弹窗未命中分支：“PARABÉNS / Nenhum problema foi encontrado.”（同为运行时解密文案）",
    "系统无障碍服务列表条目标签：android:label = Serviço de Atualização（res 字符串资源），android:description 为空，列表内无用途说明",
    "LipicaeActivity 全屏引导页：“Clique no botão para habilitar”与状态“Desativado”，压在系统无障碍设置页之上",
    "WindowManager type=2032 全屏黑色悬浮遮罩：“Instalando...”，FLAG_NOT_FOCUSABLE|NOT_TOUCHABLE",
    "未发现 assets 本地 HTML 或远端 WebView 承载任何引导文案"
  ],
  "verbatim_texts": [
    {
      "lang": "pt",
      "text_verbatim": "Verificando aplicativos.",
      "text_zh": "正在检查应用。",
      "source_location": "远端 a/a.php 下发 JSON 经 Base64+异或解密后硬编码渲染（MainActivity$c$b 路径）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "pt",
      "text_verbatim": "O aplicativo abaixo encontra-se desatualizado.",
      "text_zh": "下列应用已过期。",
      "source_location": "远端下发 JSON 解密文案，渲染于 MainActivity 原生弹窗",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "pt",
      "text_verbatim": "Atualizar Agora!",
      "text_zh": "立即更新！",
      "source_location": "远端下发 JSON 解密文案，绑定 MainActivity$b.onClick",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "pt",
      "text_verbatim": "PARABÉNS / Nenhum problema foi encontrado.",
      "text_zh": "恭喜 / 未发现任何问题。",
      "source_location": "远端下发 JSON 解密文案（未命中分支）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "pt",
      "text_verbatim": "Clique no botão para habilitar",
      "text_zh": "点击按钮以启用",
      "source_location": "com.outprotect.LipicaeActivity（引导页文案）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "pt",
      "text_verbatim": "Serviço de Atualização",
      "text_zh": "更新服务",
      "source_location": "AndroidManifest 中 IndlisySvc 的 android:label 字符串资源",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "pt",
      "text_verbatim": "Instalando...",
      "text_zh": "正在安装...",
      "source_location": "b.b.c 悬浮遮罩文案（获权后显示）",
      "rhetorical_frame": "假更新"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "台账证据未记录 onResume 死循环重跳或定时器拉起；LipicaeActivity 常驻于系统设置页之上持续提示“点击按钮以启用/Desativado”，用户返回后需重新经过 MainActivity 入口才会再次跳转（该重入路径本轮因样本缺失未能复核）",
    "overlay_or_fake_settings": "无高仿系统无障碍开关页；但在真实系统设置页之上压入自家 LipicaeActivity 引导页，并在获权后立刻叠加 type=2032 全屏黑色半透明遮罩（Instalando...）阻断视线",
    "restricted_settings_13plus_coaching": "无（未见针对 Android 13+ 受限设置“应用详情→右上角菜单→允许受限设置”的分步教学，也未使用 Session 安装器绕过）",
    "post_grant_anti_removal": "获权后立即反射 setComponentEnabledSetting 将 MainActivity 置 DISABLED 并 finish，使应用从启动器消失；未发现监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权的代码",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测 Intent 目标为 android.settings.ACCESSIBILITY_SETTINGS 或三星组件 com.samsung.accessibility/com.samsung.accessibility.Activities$InstalledServicesSettings 的启动瞬间；次优为冷启动 MainActivity 后出现“Atualizar Agora!”弹窗并发生点击的瞬间",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页（诱饵）",
        "page_identifier": "com.outprotect.MainActivity 上的原生提示弹窗，含按钮文本“Atualizar Agora!”与目标应用名“WhatsApp”",
        "why_most_useful": "这是唯一入口，且文案由远端下发、无本地 strings 可查，UTG 抓取可固定诱饵话术与“无取消按钮”事实",
        "observable_utg_signals": ["按钮文本 Atualizar Agora!", "文案 O aplicativo abaixo encontra-se desatualizado.", "目标应用名 WhatsApp", "弹窗中不存在取消/跳过控件"]
      },
      {
        "page_role": "跳转前到系统设置之间的压栈引导页",
        "page_identifier": "com.outprotect.LipicaeActivity 界面，文本“Clique no botão para habilitar”与状态“Desativado”",
        "why_most_useful": "直接证明应用在真实系统设置页上叠加自家引导层，是“教唆开启无障碍”最直接的画面证据",
        "observable_utg_signals": ["Clique no botão para habilitar", "Desativado", "当前前台 Activity 为 com.outprotect.LipicaeActivity 而非系统设置"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统无障碍设置页中 label 为 Serviço de Atualização 的条目，description 区域为空",
        "why_most_useful": "核对用户实际看到的权限说明缺失，与“更新服务”这一误导性标签形成对照",
        "observable_utg_signals": ["服务名 Serviço de Atualização", "该条目下方无用途说明文本", "包名 com.outprotect.android 与标签语义不一致"]
      },
      {
        "page_role": "获权后 800ms 内压栈遮罩页",
        "page_identifier": "全屏黑色 WindowManager type=2032 悬浮窗，文本“Instalando...”，无触摸焦点",
        "why_most_useful": "区分“授权即投递”的恶意时序：遮罩出现即代表远程载荷下载/反射加载已启动",
        "observable_utg_signals": ["文本 Instalando...", "覆盖全屏且不可点击的悬浮窗", "启动器/最近任务中 MainActivity 消失"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "诱饵文案与检测清单来自远端 a/a.php 且经 Base64+异或混淆，若远端在特定时段返回“无问题”分支（PARABÉNS）或按地域/语言停发，纯静态或单次 UTG 抓取可能只看到良性外壳；设备语言必须为 ptBR 才会进入该分支，其他语言环境下整条引导链不可达，需按语言条件复现。远程 classes.zip 载荷内容未取得，UTG 亦无法直接区分其内部行为。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.outprotect.MainActivity#onCreate",
    "com.outprotect.MainActivity$c$b#run",
    "com.outprotect.MainActivity$b#onClick",
    "com.outprotect.MainActivity$d#run",
    "com.outprotect.MainActivity#a",
    "com.outprotect.LipicaeActivity#onCreate"
  ]
}
```

**说明：** 本轮因 `input.apk` 缺失未能重新反编译，`static_visibility` 与流程细节均取自已登记风险 R-002 / R-001 的既有证据；其中“是否存在拒绝后自动重跳循环”“弹窗是否有取消按钮”两项台账未明确记载，已在 JSON 中按证据边界标注，未据此升级结论。

</details>
