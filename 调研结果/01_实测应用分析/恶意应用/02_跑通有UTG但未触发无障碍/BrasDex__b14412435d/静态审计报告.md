# MB_022__b14412435d｜BrasDex — Google Docs

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：75.2s

## 1. 一句话核心结论

- **核心申请方式**：冷启动即弹单句葡语原生 AlertDialog，两个按钮（Continuar/Cancelar）共用同一监听强制跳转系统无障碍设置，且服务描述留空、桌面名伪装 Google Docs。
- **静态可见性说明**：无障碍引导流程（mainActivity 冷启动 -> activityToast 原生 AlertDialog -> ACTION_ACCESSIBILITY_SETTINGS）全部以明文代码与明文常量呈现，弹窗文案仅做 Base64 解码（f.a），无加壳、无 AES、无远端 HTML/WebView。仅获权后由 C2（http://brasdex.com:3000）下发的指令内容属运行期数据，静态不可见，但不影响引导链路判定。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `b14412435de7ebe13c434eef79a5c24dc2c48e5483d9db2aef30b569738f4b32` |
| 包名 / 年份 | `com.mydocs.documents` / 2023 |
| 家族 / 品类 | **BrasDex**（同池样本数：2） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Google Docs |
| 引导页宣称品牌/身份 | Google Docs（Google 文档，冒充 Google 官方产品） |
| 系统无障碍列表服务名 | Ativar Google Docs |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名 com.mydocs.documents 与 Google 无关；无障碍服务 android:description 完全留空（系统列表不显示用途）；引导 Activity activityToast 的 android:label="" 为空标签并叠加 Theme.Translucent.NoTitleBar 透明无标题主题；弹窗文案以 Base64 常量存储（com.mydocs.documents.a#R 经 f.a 解码）；应用 targetSdkVersion=29，无需受限设置教学即可直接跳转无障碍页。 |
| 无障碍服务类名 | `com.mydocs.documents.Services.serviceMagic` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `READ_CONTACTS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.mydocs.documents.mainActivity（LAUNCHER Activity，带 android.app.role.SMS category） | onCreate：先做 Build.DEVICE/FINGERPRINT/MODEL/BOARD/MANUFACTURER/HOST/BRAND/HARDWARE/PRODUCT 环境指纹校验，命中则直接 return；否则 startService(serviceConnect/serviceUpdate)、startForegroundService(serviceLoop)，随后 startActivity(activityToast) 并 finish() | 无界面（透明跳板 Activity，随即 finish） | 无 | 无需操作，用户仅看到弹窗出现 | `com.mydocs.documents.mainActivity#onCreate` |
| 2 | 引导说明页 | com.mydocs.documents.Acts.activityToast（透明无标题 Activity）+ 原生 AlertDialog | activityToast.onCreate 中 new AlertDialog.Builder(this).setMessage(a.R).setPositiveButton("Continuar", d).setNegativeButton("Cancelar", d).show() | 原生Dialog | **原文**：É necessário ativar a acessibilidade para habilitar o Google Docs.<br>**译注**：需要启用无障碍功能才能启用 Google Docs。 | 点击 Continuar（继续）或 Cancelar（取消）——两个按钮都会跳转无障碍设置，实为不可取消 | `com.mydocs.documents.Acts.activityToast#onCreate / com.mydocs.documents.a#R` |
| 3 | 跳无障碍设置 | 系统无障碍设置页 android.settings.ACCESSIBILITY_SETTINGS（服务项 Ativar Google Docs） | activityToast$1.onClick（DialogInterface.OnClickListener）无论 i 为 BUTTON_POSITIVE 还是 BUTTON_NEGATIVE，均执行 startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS")) | 系统无障碍页 | **原文**：Ativar Google Docs<br>**译注**：启用 Google Docs（系统无障碍服务列表中显示的服务名，且无用途描述） | 在系统列表中手动找到 Ativar Google Docs 并打开开关；无应用侧取消或跳过入口 | `com.mydocs.documents.Acts.activityToast$1#onClick` |
| 4 | 获权后动作 | com.mydocs.documents.Services.serviceMagic（无障碍服务，持有 WindowManager 悬浮窗 RelativeLayout/TextView/ProgressBar） | onServiceConnected / onAccessibilityEvent（typeWindowContentChanged、typeViewClicked 等）驱动节点检索与点击 | 悬浮窗Overlay | **原文**：无（静态未见面向用户的引导文案，仅见节点定位串 com.android.settings.SubSettings、com.android.settings:id/action_button、android:id/button1、com.android.packageinstaller:id/permission_allow_button、com.android.vending:id/play_protect_settings）<br>**译注**：获权后不再展示说明，转而以窗口内容读取和自动点击操作设置页、安装器与 Play 保护设置 | 无（由服务自动执行点击，包括关闭安全扫描相关开关） | `com.mydocs.documents.Services.serviceMagic#onServiceConnected / com.mydocs.documents.a#aB` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- com.mydocs.documents.Acts.activityToast 的原生 AlertDialog 消息体（a.R 解码后）：“É necessário ativar a acessibilidade para habilitar o Google Docs.”
- 同一 AlertDialog 的两个按钮文案：“Continuar”（positive）与“Cancelar”（negative），二者绑定同一个监听器
- 系统无障碍服务列表项名称：AndroidManifest 中 serviceMagic 的 android:label="Ativar Google Docs"
- 系统无障碍服务详情/描述：res/xml/serviceconfig.xml 未声明 android:description，列表与详情页无任何用途说明文本
- 桌面图标名称：application android:label="Google Docs"
- 引导 Activity activityToast：android:label=""（空标签）+ Theme.Translucent.NoTitleBar，不呈现任何可见标题文本
- 未发现本地 HTML/WebView 引导页、悬浮遮罩引导文案或图片教程资源

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| pt | É necessário ativar a acessibilidade para habilitar o Google Docs. | 需要启用无障碍功能才能启用 Google Docs。 | `com.mydocs.documents.a#R（Base64 常量 w4kgbmVjZXNzw6FyaW8gYXRpdmFyIGEgYWNlc3NpYmlsaWRhZGUgcGFyYSBhIGhhYmlsaXRhciBvIEdvb2dsZSBEb2NzLg== 经 f.a 解码）` | 假更新 |
| pt | Continuar | 继续 | `com.mydocs.documents.Acts.activityToast#onCreate（setPositiveButton 硬编码）` | 受限设置分步教学 |
| pt | Cancelar | 取消 | `com.mydocs.documents.Acts.activityToast#onCreate（setNegativeButton 硬编码，与“继续”共用同一跳转监听）` | 未知 |
| pt | Ativar Google Docs | 启用 Google Docs | `AndroidManifest.xml serviceMagic android:label / strings 资源` | 假更新 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：弹窗层面即无拒绝分支：Cancelar 与 Continuar 复用同一个 activityToast$1.onClick，均 startActivity(ACCESSIBILITY_SETTINGS)；activityToast.onStop 仅置 c=false 并写入 accVisible 标记，服务端可通过 accs/cmds 通道再次拉起（远端重跳逻辑静态不可见）；mainActivity 每次冷启动都会无条件重新拉起 activityToast
- **遮罩叠层 / 高仿系统设置页**：引导阶段无遮罩/高仿设置页；仅获权后 serviceMagic 内持有 WindowManager + RelativeLayout/TextView/ProgressBar 悬浮窗对象，用于叠层显示与自动点击（非高仿无障碍开关页）
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=29，直接 startActivity(ACCESSIBILITY_SETTINGS) 即可跳转，无需受限设置教学；未见 Session 安装器绕过逻辑）
- **获权后即时行为与防撤权机制**：获权后通过无障碍节点定位串 com.android.settings.SubSettings、com.android.settings:id/action_button、com.android.settings:id/left_button、android:id/button1、com.android.packageinstaller:id/permission_allow_button 自动点击确认；并以 com.android.vending:id/play_protect_settings、com.google.android.gms.security.settings.verifyappssettingsactivity 关闭 Play 保护；配置声明 WATCH_SETTINGS/WATCH_PKG_INSTALLER/PERFORM_GLOBAL_ACTION 与 BOOT_COMPLETED/PACKAGE_ADDED 自启接收器，形成撤权对抗
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以“监测到应用进程启动后 0–2 秒内出现 windowStateChanged 且当前焦点窗口为 com.mydocs.documents.Acts.activityToast”为第一捕获点；第二捕获点为“应用内发起 startActivity 目标 action=android.settings.ACCESSIBILITY_SETTINGS”的瞬间
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无图片型诱导，全部为文本控件，纯 UTG 可提取；盲区在于：1）远端 C2（http://brasdex.com:3000 的 cmds/accs 通道）可能下发新的引导文案或重新拉起弹窗，静态不可见；2）mainActivity 的模拟器/分析环境指纹校验命中时静默 return，真机与沙箱表现可能不同，需注意在真实设备环境复现；3）应用无静态加壳，运行期界面不受影响。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页** | 包名 com.mydocs.documents，透明无标题窗口，含两个按钮文案 Continuar / Cancelar 的 AlertDialog | 这是唯一直接向用户索取无障碍权限的说明界面，且能证明“取消即跳设置”的无拒绝设计 | 弹窗消息全文“É necessário ativar a acessibilidade para habilitar o Google Docs.”；两个按钮文案同时存在（Continuar、Cancelar）；点击 Cancelar 后仍跳转 ACCESSIBILITY_SETTINGS 的行为轨迹 |
| **系统无障碍服务列表项** | 系统设置“无障碍 → 已安装的服务”中出现 Ativar Google Docs，且描述区为空 | 证明服务标签冒充 Google 品牌且刻意不留用途说明，是身份伪装与告知缺失的直接证据 | 服务名文本 Ativar Google Docs；描述文本为空/缺失；包名 com.mydocs.documents 与服务名不一致 |
| **获权后悬浮窗/自动点击页** | 设置页或安装器页面之上叠加的 WindowManager 悬浮窗（serviceMagic 内 RelativeLayout+ProgressBar） | 可验证获权后的真实目的（自动点击授权、关闭 Play 保护），补全从诱导到滥用的完整链条 | 非应用包名的悬浮窗层级出现；设置页/安装器按钮被非用户输入点击；com.android.vending 保护设置页被自动进入并关闭 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.mydocs.documents.mainActivity#onCreate`
- `com.mydocs.documents.Acts.activityToast#onCreate`
- `com.mydocs.documents.Acts.activityToast$1#onClick`
- `com.mydocs.documents.a#R`
- `com.mydocs.documents.Services.serviceMagic#onServiceConnected`
- `res/xml/serviceconfig.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验）

**无障碍权限的诱导申请完全在运行期完成，相关逻辑均可静态还原；未发现远端 HTML 或密文加载。**

1. **冷启动后直接弹出引导，且没有真正的“取消”**：`mainActivity.onCreate` 先对模拟器或分析环境做指纹校验（`Build.DEVICE`、`FINGERPRINT`、`MODEL`、`BOARD`、`MANUFACTURER`、`HOST`、`BRAND`、`HARDWARE`、`PRODUCT`，命中即静默 `return`），随后注册、拉起 `serviceConnect`、`serviceUpdate`、`serviceLoop`（前台服务），并 `startActivity(activityToast)`，最后立即 `finish()`。
2. **引导弹窗只有一句葡萄牙语，两个按钮都跳转到系统无障碍设置**：`activityToast.onCreate` 使用 `AlertDialog`，消息为 `a.R`（经 `f.a` 做 Base64 解码），原文 `É necessário ativar a acessibilidade para habilitar o Google Docs.`（“需要启用无障碍才能启用 Google Docs”）。`Continuar` 与 `Cancelar` 绑定的是**同一个** `activityToast$1.onClick`，二者都执行 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`，因此不存在拒绝或跳过的路径。
3. **系统无障碍列表刻意留空描述**：`res/xml/serviceconfig.xml` 只声明 `canRetrieveWindowContent="true"`、`flagIncludeNotImportantViews`、`flagReportViewIds` 和 `typeWindowContentChanged`，**没有 `android:description`**，因此用户在系统设置中看不到用途说明；服务标签为葡萄牙语 `Ativar Google Docs`，冒充 Google 品牌。
4. **身份伪装**：桌面名为 `Google Docs`，包名 `com.mydocs.documents`，主题为 `Theme.Translucent.NoTitleBar`；`activityToast` 的 `android:label=""` 为空标签，配合透明主题使弹窗外观与来源更不易辨识。
5. **获权后与后续行为（旁证）**：`serviceMagic` 持有 `WindowManager`、`RelativeLayout`、`TextView`、`ProgressBar` 等悬浮窗字段，并含 `com.android.settings.SubSettings`、`android:id/button1`、`permission_allow_button`、`com.android.vending:id/play_protect_settings` 等节点定位串，表明获权后可自动点击授权或关闭安全设置；C2 为 `http://brasdex.com:3000`（`/mobile`、`/accs`、`cmds`、`activation_hash`），属于远端指令控制（与本次 UTG 页面流转不冲突，可另行深挖）。
6. **预筛中的 Google Play services 英文串**来自内置 GMS 库资源，不是引导文案，不能作为诱导证据。

**覆盖边界**：`Cancelar` 是否在特定分支被拦截、以及远端 `cmds` 下发的二次文案无法静态确证（取决于服务端）；引导流程本身的界面载体、按钮绑定与跳转目标已完全静态闭合。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导流程（mainActivity 冷启动 -> activityToast 原生 AlertDialog -> ACTION_ACCESSIBILITY_SETTINGS）全部以明文代码与明文常量呈现，弹窗文案仅做 Base64 解码（f.a），无加壳、无 AES、无远端 HTML/WebView。仅获权后由 C2（http://brasdex.com:3000）下发的指令内容属运行期数据，静态不可见，但不影响引导链路判定。",
  "summary_one_liner": "冷启动即弹单句葡语原生 AlertDialog，两个按钮（Continuar/Cancelar）共用同一监听强制跳转系统无障碍设置，且服务描述留空、桌面名伪装 Google Docs。",
  "disguise_identity": {
    "app_display_name": "Google Docs",
    "claimed_brand_or_persona": "Google Docs（Google 文档，冒充 Google 官方产品）",
    "a11y_service_label": "Ativar Google Docs",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名 com.mydocs.documents 与 Google 无关；无障碍服务 android:description 完全留空（系统列表不显示用途）；引导 Activity activityToast 的 android:label=\"\" 为空标签并叠加 Theme.Translucent.NoTitleBar 透明无标题主题；弹窗文案以 Base64 常量存储（com.mydocs.documents.a#R 经 f.a 解码）；应用 targetSdkVersion=29，无需受限设置教学即可直接跳转无障碍页。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.mydocs.documents.mainActivity（LAUNCHER Activity，带 android.app.role.SMS category）",
      "trigger_event": "onCreate：先做 Build.DEVICE/FINGERPRINT/MODEL/BOARD/MANUFACTURER/HOST/BRAND/HARDWARE/PRODUCT 环境指纹校验，命中则直接 return；否则 startService(serviceConnect/serviceUpdate)、startForegroundService(serviceLoop)，随后 startActivity(activityToast) 并 finish()",
      "ui_carrier": "无界面（透明跳板 Activity，随即 finish）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "启动瞬间不展示任何界面，直接转入引导弹窗 Activity",
      "user_action_requested": "无需操作，用户仅看到弹窗出现",
      "code_anchor": "com.mydocs.documents.mainActivity#onCreate"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "com.mydocs.documents.Acts.activityToast（透明无标题 Activity）+ 原生 AlertDialog",
      "trigger_event": "activityToast.onCreate 中 new AlertDialog.Builder(this).setMessage(a.R).setPositiveButton(\"Continuar\", d).setNegativeButton(\"Cancelar\", d).show()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "É necessário ativar a acessibilidade para habilitar o Google Docs.",
      "shown_text_zh": "需要启用无障碍功能才能启用 Google Docs。",
      "user_action_requested": "点击 Continuar（继续）或 Cancelar（取消）——两个按钮都会跳转无障碍设置，实为不可取消",
      "code_anchor": "com.mydocs.documents.Acts.activityToast#onCreate / com.mydocs.documents.a#R"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍设置页 android.settings.ACCESSIBILITY_SETTINGS（服务项 Ativar Google Docs）",
      "trigger_event": "activityToast$1.onClick（DialogInterface.OnClickListener）无论 i 为 BUTTON_POSITIVE 还是 BUTTON_NEGATIVE，均执行 startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Ativar Google Docs",
      "shown_text_zh": "启用 Google Docs（系统无障碍服务列表中显示的服务名，且无用途描述）",
      "user_action_requested": "在系统列表中手动找到 Ativar Google Docs 并打开开关；无应用侧取消或跳过入口",
      "code_anchor": "com.mydocs.documents.Acts.activityToast$1#onClick"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "com.mydocs.documents.Services.serviceMagic（无障碍服务，持有 WindowManager 悬浮窗 RelativeLayout/TextView/ProgressBar）",
      "trigger_event": "onServiceConnected / onAccessibilityEvent（typeWindowContentChanged、typeViewClicked 等）驱动节点检索与点击",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无（静态未见面向用户的引导文案，仅见节点定位串 com.android.settings.SubSettings、com.android.settings:id/action_button、android:id/button1、com.android.packageinstaller:id/permission_allow_button、com.android.vending:id/play_protect_settings）",
      "shown_text_zh": "获权后不再展示说明，转而以窗口内容读取和自动点击操作设置页、安装器与 Play 保护设置",
      "user_action_requested": "无（由服务自动执行点击，包括关闭安全扫描相关开关）",
      "code_anchor": "com.mydocs.documents.Services.serviceMagic#onServiceConnected / com.mydocs.documents.a#aB"
    }
  ],
  "text_presentation_locations": [
    "com.mydocs.documents.Acts.activityToast 的原生 AlertDialog 消息体（a.R 解码后）：“É necessário ativar a acessibilidade para habilitar o Google Docs.”",
    "同一 AlertDialog 的两个按钮文案：“Continuar”（positive）与“Cancelar”（negative），二者绑定同一个监听器",
    "系统无障碍服务列表项名称：AndroidManifest 中 serviceMagic 的 android:label=\"Ativar Google Docs\"",
    "系统无障碍服务详情/描述：res/xml/serviceconfig.xml 未声明 android:description，列表与详情页无任何用途说明文本",
    "桌面图标名称：application android:label=\"Google Docs\"",
    "引导 Activity activityToast：android:label=\"\"（空标签）+ Theme.Translucent.NoTitleBar，不呈现任何可见标题文本",
    "未发现本地 HTML/WebView 引导页、悬浮遮罩引导文案或图片教程资源"
  ],
  "verbatim_texts": [
    {
      "lang": "pt",
      "text_verbatim": "É necessário ativar a acessibilidade para habilitar o Google Docs.",
      "text_zh": "需要启用无障碍功能才能启用 Google Docs。",
      "source_location": "com.mydocs.documents.a#R（Base64 常量 w4kgbmVjZXNzw6FyaW8gYXRpdmFyIGEgYWNlc3NpYmlsaWRhZGUgcGFyYSBhIGhhYmlsaXRhciBvIEdvb2dsZSBEb2NzLg== 经 f.a 解码）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "pt",
      "text_verbatim": "Continuar",
      "text_zh": "继续",
      "source_location": "com.mydocs.documents.Acts.activityToast#onCreate（setPositiveButton 硬编码）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "pt",
      "text_verbatim": "Cancelar",
      "text_zh": "取消",
      "source_location": "com.mydocs.documents.Acts.activityToast#onCreate（setNegativeButton 硬编码，与“继续”共用同一跳转监听）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "pt",
      "text_verbatim": "Ativar Google Docs",
      "text_zh": "启用 Google Docs",
      "source_location": "AndroidManifest.xml serviceMagic android:label / strings 资源",
      "rhetorical_frame": "假更新"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "弹窗层面即无拒绝分支：Cancelar 与 Continuar 复用同一个 activityToast$1.onClick，均 startActivity(ACCESSIBILITY_SETTINGS)；activityToast.onStop 仅置 c=false 并写入 accVisible 标记，服务端可通过 accs/cmds 通道再次拉起（远端重跳逻辑静态不可见）；mainActivity 每次冷启动都会无条件重新拉起 activityToast",
    "overlay_or_fake_settings": "引导阶段无遮罩/高仿设置页；仅获权后 serviceMagic 内持有 WindowManager + RelativeLayout/TextView/ProgressBar 悬浮窗对象，用于叠层显示与自动点击（非高仿无障碍开关页）",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=29，直接 startActivity(ACCESSIBILITY_SETTINGS) 即可跳转，无需受限设置教学；未见 Session 安装器绕过逻辑）",
    "post_grant_anti_removal": "获权后通过无障碍节点定位串 com.android.settings.SubSettings、com.android.settings:id/action_button、com.android.settings:id/left_button、android:id/button1、com.android.packageinstaller:id/permission_allow_button 自动点击确认；并以 com.android.vending:id/play_protect_settings、com.google.android.gms.security.settings.verifyappssettingsactivity 关闭 Play 保护；配置声明 WATCH_SETTINGS/WATCH_PKG_INSTALLER/PERFORM_GLOBAL_ACTION 与 BOOT_COMPLETED/PACKAGE_ADDED 自启接收器，形成撤权对抗",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以“监测到应用进程启动后 0–2 秒内出现 windowStateChanged 且当前焦点窗口为 com.mydocs.documents.Acts.activityToast”为第一捕获点；第二捕获点为“应用内发起 startActivity 目标 action=android.settings.ACCESSIBILITY_SETTINGS”的瞬间",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页",
        "page_identifier": "包名 com.mydocs.documents，透明无标题窗口，含两个按钮文案 Continuar / Cancelar 的 AlertDialog",
        "why_most_useful": "这是唯一直接向用户索取无障碍权限的说明界面，且能证明“取消即跳设置”的无拒绝设计",
        "observable_utg_signals": ["弹窗消息全文“É necessário ativar a acessibilidade para habilitar o Google Docs.”", "两个按钮文案同时存在（Continuar、Cancelar）", "点击 Cancelar 后仍跳转 ACCESSIBILITY_SETTINGS 的行为轨迹"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统设置“无障碍 → 已安装的服务”中出现 Ativar Google Docs，且描述区为空",
        "why_most_useful": "证明服务标签冒充 Google 品牌且刻意不留用途说明，是身份伪装与告知缺失的直接证据",
        "observable_utg_signals": ["服务名文本 Ativar Google Docs", "描述文本为空/缺失", "包名 com.mydocs.documents 与服务名不一致"]
      },
      {
        "page_role": "获权后悬浮窗/自动点击页",
        "page_identifier": "设置页或安装器页面之上叠加的 WindowManager 悬浮窗（serviceMagic 内 RelativeLayout+ProgressBar）",
        "why_most_useful": "可验证获权后的真实目的（自动点击授权、关闭 Play 保护），补全从诱导到滥用的完整链条",
        "observable_utg_signals": ["非应用包名的悬浮窗层级出现", "设置页/安装器按钮被非用户输入点击", "com.android.vending 保护设置页被自动进入并关闭"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无图片型诱导，全部为文本控件，纯 UTG 可提取；盲区在于：1）远端 C2（http://brasdex.com:3000 的 cmds/accs 通道）可能下发新的引导文案或重新拉起弹窗，静态不可见；2）mainActivity 的模拟器/分析环境指纹校验命中时静默 return，真机与沙箱表现可能不同，需注意在真实设备环境复现；3）应用无静态加壳，运行期界面不受影响。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH"
  ],
  "code_anchors": [
    "com.mydocs.documents.mainActivity#onCreate",
    "com.mydocs.documents.Acts.activityToast#onCreate",
    "com.mydocs.documents.Acts.activityToast$1#onClick",
    "com.mydocs.documents.a#R",
    "com.mydocs.documents.Services.serviceMagic#onServiceConnected",
    "res/xml/serviceconfig.xml"
  ]
}
```

</details>
