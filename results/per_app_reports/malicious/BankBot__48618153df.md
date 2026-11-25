# MB_108__48618153df｜BankBot — Atualização WA [4ed5]

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：131.3s

## 1. 一句话核心结论

- **核心申请方式**：冷启动即在子线程检测自身无障碍服务未启用后弹出不可取消 AlertDialog，以"更新 WA"为名教用户到系统 Serviços 中开启 AccService 并直跳 ACCESSIBILITY_SETTINGS，同时15秒隐藏桌面图标、45秒未获权自杀，获权后弹"更新成功"完成伪装闭环。
- **静态可见性说明**：未加壳、无加密载荷、无远端 HTML；引导链路（MainActivity.onCreate→b→MainActivity$a.b→MainActivity$a$1.onClick）、全部弹窗文案硬编码于 DEX、无障碍 description 明文存于 resources.arsc，均已静态完整还原。仅 res/xml/accessibility_service_config.xml 与 strings 为二进制资源格式，内容已由 strings -e l 提取确认。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `48618153df1b2b5be3f83e6e1fa6aa5f517b173b10f3f6e925d1598a22b459e1` |
| 包名 / 年份 | `com.gelini` / 2025 |
| 家族 / 品类 | **BankBot**（同池样本数：8） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Atualização WA [4ed5] |
| 引导页宣称品牌/身份 | WhatsApp（WA）官方更新/升级包 |
| 系统无障碍列表服务名 | 无独立 label（Manifest 未声明 android:label，系统无障碍列表显示为空或继承应用名） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名 com.gelini 与代码包 com.irifix 不一致（套壳拼接）；显示名注入随机十六进制标记 [4ed5] 用于批量变体区分；无障碍服务不设 label 使系统列表项显示空白；15秒后 setComponentEnabledSetting 禁用 MainActivity 使桌面图标消失以规避事后追查；全部引导文案以硬编码 Html.fromHtml 拼接，不含 strings 资源 key。 |
| 无障碍服务类名 | `com.irifix.AccService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `REQUEST_INSTALL_PACKAGES` |
| 系统设置项说明 (`android:description`) | Para continuar a atualização [4ed5] você deve Habilitar esse serviço. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.irifix.MainActivity | onCreate 中 new Thread(new MainActivity$1(this)).start()，子线程回调 MainActivity.b() | 原生Activity | 无 | 无需操作，冷启动自动进入下一步 | `com.irifix.MainActivity#onCreate / com.irifix.MainActivity#b` |
| 2 | 业务功能触发 | Settings.Secure 无障碍服务启用状态查询 | MainActivity.b() 调用 g.a(getApplicationContext(), getPackageName()) | 不可静态还原 | 无 | 无（静默判定） | `com.irifix.g#a` |
| 3 | 引导说明页 | AlertDialog（MainActivity$a 静态弹窗实例，setCancelable(false)） | 未启用分支 → c.post(new MainActivity$4(this)) 与 c.postDelayed(new MainActivity$5(this), 15000L)，主线程经 MainActivity$3.run → MainActivity$a.b(context) 弹窗 | 原生Dialog | **原文**：Atenção / Para atualizar você precisa ativar o serviço de acessiblidade em <b>Serviços > {服务名}</b> na proxima tela. / Continuar<br>**译注**：注意 / 要完成更新，你需要在下一屏的「服务 > {服务名}」中启用该无障碍服务。 / 继续 | 只能点击唯一按钮「Continuar」；无取消、无跳过、无返回键退出（setCancelable(false)，仅 setNeutralButton 一个按钮） | `com.irifix.MainActivity$a#b` |
| 4 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表页） | MainActivity$a$1.onClick(DialogInterface,int) 中 startActivity(Intent("android.settings.ACCESSIBILITY_SETTINGS")) | 系统无障碍页 | 无 | 要求用户在系统列表中手动找到并开启本应用的无障碍服务（应用侧无高亮、无遮罩、无引导指示） | `com.irifix.MainActivity$a$1#onClick` |
| 5 | 拒权反馈循环 | MainActivity 组件禁用 + Timer 自杀 | MainActivity$5.run（15秒后 setComponentEnabledSetting(MainActivity, 2, 1)）与 MainActivity$c.run（Timer 45000ms 后复检） | 不可静态还原 | 无 | 无显式请求；通过图标消失与应用退出施加压力，不提供放弃/降级选项 | `com.irifix.MainActivity$5#run / com.irifix.MainActivity$c#run / com.irifix.MainActivity#a` |
| 6 | 获权后动作 | AlertDialog（MainActivity$b 静态弹窗）+ com.irifix.AccService 启动 | g.a() 判定已启用 → j.c() 写 SharedPreferences 标记 → c.post(new MainActivity$3(this)) → 弹窗；同时 AccService.onServiceConnected 注册 USER_PRESENT 广播 | 原生Dialog | **原文**：Atenção / Atualização aplicada com sucesso. / Continuar<br>**译注**：注意 / 更新已成功应用。 / 继续 | 点击「Continuar」后 MainActivity.finish()；同样 setCancelable(false)，无取消按钮 | `com.irifix.MainActivity$b#b / com.irifix.MainActivity$b$1#onClick / com.irifix.AccService#onServiceConnected` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 不可取消 AlertDialog（标题 Atenção，正文 Html.fromHtml 硬编码，按钮 Continuar）——引导开启无障碍的主载体，位于 com.irifix.MainActivity$a#b
- MainActivity 不可取消 AlertDialog（标题 Atenção，正文 Atualização aplicada com sucesso.，按钮 Continuar）——获权后的假成功提示，位于 com.irifix.MainActivity$b#b
- 系统无障碍服务列表 android:description：Para continuar a atualização [4ed5] você deve Habilitar esse serviço.（存于 resources.arsc，由 Manifest service 的 meta-data android.accessibilityservice=@7F0E0000 指向 res/xml/accessibility_service_config.xml）
- 桌面启动器图标名称：Atualização WA [4ed5]（application android:label=@7F0B0028）
- MainActivity 布局 activity_main.xml 中的 Button（id 2131165219）——初始 Visibility 隐藏，仅在已获权路径由 MainActivity$3.run 设为可见并绑定 MainActivity$3$1.onClick
- 无 WebView、无 assets 内 HTML、无悬浮窗 Overlay、无高仿系统设置页；全部引导文字仅存在于上述两个原生 AlertDialog 与无障碍 description

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| pt | Atenção | 注意 | `硬编码于 com.irifix.MainActivity$a#b 与 com.irifix.MainActivity$b#b（AlertDialog.setTitle）` | 假更新 |
| pt | Para atualizar você precisa ativar o serviço de acessiblidade em Serviços > {服务名} na proxima tela. | 要完成更新，你需要在下一屏的「服务 > {服务名}」中启用该无障碍服务。 | `硬编码于 com.irifix.MainActivity$a#b（Html.fromHtml 拼接 context.getString(2131427368)）` | 假更新 |
| pt | Continuar | 继续 | `硬编码于 com.irifix.MainActivity$a#b / com.irifix.MainActivity$b#b（setNeutralButton）` | 受限设置分步教学 |
| pt | Atualização aplicada com sucesso. | 更新已成功应用。 | `硬编码于 com.irifix.MainActivity$b#b（Html.fromHtml）` | 假更新 |
| pt | Para continuar a atualização [4ed5] você deve Habilitar esse serviço. | 要继续更新 [4ed5]，你必须启用此服务。 | `resources.arsc → res/xml/accessibility_service_config.xml 的 android:description（Manifest meta-data @7F0E0000）` | 假更新 |
| pt | Atualização WA [4ed5] | WA 更新 [4ed5]（WA 指 WhatsApp） | `resources.arsc → application android:label=@7F0B0028` | 假更新 |
| pt | Atualizando... / Atualização concluida! | 正在更新... / 更新完成！ | `硬编码于 com.irifix.f#a 与 com.irifix.f$2#run（进度按钮文案）` | 假更新 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不做 onResume 死循环重跳：15 秒后 setComponentEnabledSetting(MainActivity, COMPONENT_ENABLED_STATE_DISABLED=2, DONT_KILL_APP=1) 隐藏桌面启动图标；Timer 45000ms 后 MainActivity$c.run 复检，仍未获权则 MainActivity.a() 调 finish() 自杀退出。用户返回桌面时应用图标已消失，通过"应用自动消失"施压，需重新从安装源或通知栏才能再次进入引导。
- **遮罩叠层 / 高仿系统设置页**：无。不使用半透明引导遮罩、不使用全屏悬浮窗、不做高仿系统无障碍开关页；仅靠不可取消原生 AlertDialog 的口头文案 + 直跳真实系统 ACCESSIBILITY_SETTINGS 页。
- **Android 13+ 受限设置（Restricted Settings）应对**：无针对 Android 13+ 受限设置的右上角菜单教学；但存在相邻的受限设置引导：Permissions$RequestActivity.onCreate 在 SDK_INT>=26 且 !canRequestPackageInstalls() 时以 Intent("android.settings.MANAGE_UNKNOWN_APP_SOURCES", "package:<包名>") 跳转未知来源安装授权页，并以 startActivityForResult + Object.wait(10000) 同步等待结果。
- **获权后即时行为与防撤权机制**：获权后不主动自点确认，也不在设置页发 GLOBAL_ACTION_BACK/HOME 阻止撤权；但 DEX 含 PERFORM_GLOBAL_ACTION 能力与 AccService.onAccessibilityEvent 对 TYPE_WINDOW_STATE_CHANGED 的节点遍历动作链（a/e/b/c/d 六个处理器），具备运行期自动操作与干扰用户操作的能力。
- **良性降级 / 替代方案**：无。未获权时既无手动模式、也无仅观看模式或功能降级，唯一路径是隐藏图标并退出。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 Activity 启动 Intent action == android.settings.ACCESSIBILITY_SETTINGS（或 component 为 com.android.settings/.Settings$AccessibilitySettingsActivity），在其前一个前台窗口为 com.irifix.MainActivity 时立即抓取；亦可在冷启动 MainActivity 后 1~3 秒（子线程 post 弹窗完成时）直接抓屏，此时必为 Atenção 弹窗。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：全部引导文案为文本型原生 AlertDialog，UTG 可直接读取文本与控件树。需注意两点：(1) 无障碍服务未声明 label，系统列表项为空白，若检测逻辑依赖服务名关键词匹配会漏判，应改以包名 + description 文本为锚点；(2) 应用在 15 秒内即禁用启动组件，UTG 若在冷启动后延迟超过 15 秒才抓取，可能因图标消失而误判为"应用未安装/无界面"，应在启动后 1~3 秒内完成首屏抓取。本样本无加壳、无远端 HTML、无图空文本诱导。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页（唯一文案载体）** | 前台窗口 com.irifix.MainActivity + 不可取消 AlertDialog，标题文本 Atenção，正文含 Para atualizar / acessiblidade / Serviços，唯一按钮 Continuar | 整个诱导的全部说辞都在此一处；可同时取证"假更新名义""无取消按钮""教用户去 Serviços 开启"三要素，是判定诱导而非良性说明的决定性页面 | 弹窗仅存在一个可点击按钮（Continuar），无取消/跳过/关闭控件；正文包含 acessiblidade + Serviços + proxima tela 组合文案；标题为泛化警示词 Atenção 而非功能名；点击返回键或弹窗外区域后弹窗仍驻留（不可取消验证） |
| **跳转后系统无障碍服务列表项** | 系统设置无障碍页中本应用条目（package com.gelini），条目文本为空/仅显示图标，description 提示为 Para continuar a atualização [4ed5] você deve Habilitar esse serviço. | 验证应用未在系统层提供任何真实功能标签，且 description 仍以"更新"为名，与桌面名 Atualização WA [4ed5] 构成同一伪装叙事，可确认身份伪装而非真实辅助功能服务 | 无障碍列表项 label 为空白或仅显示应用名，无功能描述；description 文本含 atualização 关键词而非无障碍功能说明；列表页为真实系统设置（非应用自绘高仿页），排除假设置页手法 |
| **拒权返回后桌面状态页（图标消失）** | 冷启动后约 15 秒返回桌面，com.gelini 启动图标从 Launcher 消失；约 45 秒后应用进程 MainActivity 已 finish 退出 | 区分"强制引导"与"良性授权请求"的关键运行期行为：良性应用拒权后留在原页或降级，本应用则隐藏入口并退出，是规避追查的强信号 | 15 秒节点后 Launcher 中 com.gelini 图标消失；45 秒节点后前台窗口不再为 com.irifix.MainActivity，且无任务栈残留；全程无任何降级/跳过 UI 出现 |
| **获权后假成功弹窗页** | 无障碍开启后回到前台，AlertDialog 标题 Atenção、正文 Atualização aplicada com sucesso.、按钮 Continuar | 确认授权被包装为"更新安装成功"，完成诱导闭环，证明授权本身就是目的而非功能前置条件 | 弹窗文本 Atualização aplicada com sucesso. 与实际发生的无障碍授权行为不符；同样仅有一个 Continuar 按钮、不可取消 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.irifix.MainActivity#onCreate`
- `com.irifix.MainActivity#b`
- `com.irifix.MainActivity$a#b`
- `com.irifix.MainActivity$a$1#onClick`
- `com.irifix.MainActivity$c#run`
- `res/xml/accessibility_service_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（运行期 UTG 视角）

**核心机制：冷启动 0 步强制引导，无业务功能伪装**

1. **入口即引导**：[MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.irifix.MainActivity#onCreate>) 只 `setContentView` 后立即起子线程，UI 线程不含任何业务逻辑；子线程回到 [MainActivity.b()](<resource-unit:#1.dex1 code:com.irifix.MainActivity#b>) 用 [g.a(Context,String)](<resource-unit:#1.dex1 code:com.irifix.g#a>) 读 `Settings.Secure.enabled_accessibility_services` 判断自身服务是否已启用。
2. **不可取消教学弹窗**：[MainActivity$a.b(Context)](<resource-unit:#1.dex1 code:com.irifix.MainActivity$a#b>) 构造 `AlertDialog`（标题 `Atenção`），正文硬编码 `"Para atualizar você precisa ativar o serviço de acessiblidade em <b>Serviços > <服务名></b> na proxima tela."`，`setCancelable(false)` + 单一 `Continuar` 按钮——无取消、无跳过、无降级路径。
3. **直跳系统无障碍页**：[MainActivity$a$1.onClick()](<resource-unit:#1.dex1 code:com.irifix.MainActivity$a$1#onClick>) 以 `Intent("android.settings.ACCESSIBILITY_SETTINGS")` 加 `NEW_TASK|0x8000|0x800000` 拉起系统列表页；不叠加悬浮窗遮罩、不做高仿设置页，纯"文案教学+系统页"路线。
4. **拒权反馈不是重跳，而是"消失"**：同分支 15 秒后 [MainActivity$5.run()](<resource-unit:#1.dex1 code:com.irifix.MainActivity$5#run>) 将启动器组件 `COMPONENT_ENABLED_STATE_DISABLED` 隐藏桌面图标；45 秒定时器 [MainActivity$c.run()](<resource-unit:#1.dex1 code:com.irifix.MainActivity$c#run>) 复检，仍未获权则 [MainActivity.a()](<resource-unit:#1.dex1 code:com.irifix.MainActivity#a>) `finish()` 自杀退出。
5. **假完成闭环**：获权后弹 [MainActivity$b.b(Context)](<resource-unit:#1.dex1 code:com.irifix.MainActivity$b#b>) `Atualização aplicada com sucesso.`（同样不可取消），把无障碍授权包装成"更新安装成功"。
6. **身份伪装**：显示名 `Atualização WA [4ed5]`（宣称 WhatsApp 更新器），包名 `com.gelini` 与代码包 `com.irifix` 不一致；无障碍 `android:description` = `Para continuar a atualização [4ed5] você deve Habilitar esse serviço.`；服务无独立 label（系统列表显示空白/继承应用名）。
7. **静态可见性**：未加壳，引导链路、文案、跳转全部明文可读；仅无障碍配置 xml 与 strings 为二进制资源（已由 `strings -e l` 直接取回原文）。

**UTG 关键抓取点**：`ACCESSIBILITY_SETTINGS` 跳转前的不可取消弹窗（唯一文案载体）+ 跳转后系统列表项（空白 label 是强判别信号）+ 15 秒后桌面图标消失现象。

```json
{
  "static_visibility": "clear",
  "visibility_note": "未加壳、无加密载荷、无远端 HTML；引导链路（MainActivity.onCreate→b→MainActivity$a.b→MainActivity$a$1.onClick）、全部弹窗文案硬编码于 DEX、无障碍 description 明文存于 resources.arsc，均已静态完整还原。仅 res/xml/accessibility_service_config.xml 与 strings 为二进制资源格式，内容已由 strings -e l 提取确认。",
  "summary_one_liner": "冷启动即在子线程检测自身无障碍服务未启用后弹出不可取消 AlertDialog，以\"更新 WA\"为名教用户到系统 Serviços 中开启 AccService 并直跳 ACCESSIBILITY_SETTINGS，同时15秒隐藏桌面图标、45秒未获权自杀，获权后弹\"更新成功\"完成伪装闭环。",
  "disguise_identity": {
    "app_display_name": "Atualização WA [4ed5]",
    "claimed_brand_or_persona": "WhatsApp（WA）官方更新/升级包",
    "a11y_service_label": "无独立 label（Manifest 未声明 android:label，系统无障碍列表显示为空或继承应用名）",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名 com.gelini 与代码包 com.irifix 不一致（套壳拼接）；显示名注入随机十六进制标记 [4ed5] 用于批量变体区分；无障碍服务不设 label 使系统列表项显示空白；15秒后 setComponentEnabledSetting 禁用 MainActivity 使桌面图标消失以规避事后追查；全部引导文案以硬编码 Html.fromHtml 拼接，不含 strings 资源 key。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.irifix.MainActivity",
      "trigger_event": "onCreate 中 new Thread(new MainActivity$1(this)).start()，子线程回调 MainActivity.b()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "空白启动页（layout activity_main，仅含一个默认隐藏的 Button），无任何可见文案",
      "user_action_requested": "无需操作，冷启动自动进入下一步",
      "code_anchor": "com.irifix.MainActivity#onCreate / com.irifix.MainActivity#b"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "Settings.Secure 无障碍服务启用状态查询",
      "trigger_event": "MainActivity.b() 调用 g.a(getApplicationContext(), getPackageName())",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "读取 accessibility_enabled 与 enabled_accessibility_services，逐个 ComponentName 比对本包是否已启用",
      "user_action_requested": "无（静默判定）",
      "code_anchor": "com.irifix.g#a"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "AlertDialog（MainActivity$a 静态弹窗实例，setCancelable(false)）",
      "trigger_event": "未启用分支 → c.post(new MainActivity$4(this)) 与 c.postDelayed(new MainActivity$5(this), 15000L)，主线程经 MainActivity$3.run → MainActivity$a.b(context) 弹窗",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Atenção / Para atualizar você precisa ativar o serviço de acessiblidade em <b>Serviços > {服务名}</b> na proxima tela. / Continuar",
      "shown_text_zh": "注意 / 要完成更新，你需要在下一屏的「服务 > {服务名}」中启用该无障碍服务。 / 继续",
      "user_action_requested": "只能点击唯一按钮「Continuar」；无取消、无跳过、无返回键退出（setCancelable(false)，仅 setNeutralButton 一个按钮）",
      "code_anchor": "com.irifix.MainActivity$a#b"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表页）",
      "trigger_event": "MainActivity$a$1.onClick(DialogInterface,int) 中 startActivity(Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "系统原生无障碍服务列表，其中本应用条目因未声明 label 而显示空白/仅图标",
      "user_action_requested": "要求用户在系统列表中手动找到并开启本应用的无障碍服务（应用侧无高亮、无遮罩、无引导指示）",
      "code_anchor": "com.irifix.MainActivity$a$1#onClick"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity 组件禁用 + Timer 自杀",
      "trigger_event": "MainActivity$5.run（15秒后 setComponentEnabledSetting(MainActivity, 2, 1)）与 MainActivity$c.run（Timer 45000ms 后复检）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "15 秒后桌面启动图标被禁用消失；45 秒后若仍未获权则 MainActivity.finish() 退出，用户返回时无应用可寻",
      "user_action_requested": "无显式请求；通过图标消失与应用退出施加压力，不提供放弃/降级选项",
      "code_anchor": "com.irifix.MainActivity$5#run / com.irifix.MainActivity$c#run / com.irifix.MainActivity#a"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "AlertDialog（MainActivity$b 静态弹窗）+ com.irifix.AccService 启动",
      "trigger_event": "g.a() 判定已启用 → j.c() 写 SharedPreferences 标记 → c.post(new MainActivity$3(this)) → 弹窗；同时 AccService.onServiceConnected 注册 USER_PRESENT 广播",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Atenção / Atualização aplicada com sucesso. / Continuar",
      "shown_text_zh": "注意 / 更新已成功应用。 / 继续",
      "user_action_requested": "点击「Continuar」后 MainActivity.finish()；同样 setCancelable(false)，无取消按钮",
      "code_anchor": "com.irifix.MainActivity$b#b / com.irifix.MainActivity$b$1#onClick / com.irifix.AccService#onServiceConnected"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 不可取消 AlertDialog（标题 Atenção，正文 Html.fromHtml 硬编码，按钮 Continuar）——引导开启无障碍的主载体，位于 com.irifix.MainActivity$a#b",
    "MainActivity 不可取消 AlertDialog（标题 Atenção，正文 Atualização aplicada com sucesso.，按钮 Continuar）——获权后的假成功提示，位于 com.irifix.MainActivity$b#b",
    "系统无障碍服务列表 android:description：Para continuar a atualização [4ed5] você deve Habilitar esse serviço.（存于 resources.arsc，由 Manifest service 的 meta-data android.accessibilityservice=@7F0E0000 指向 res/xml/accessibility_service_config.xml）",
    "桌面启动器图标名称：Atualização WA [4ed5]（application android:label=@7F0B0028）",
    "MainActivity 布局 activity_main.xml 中的 Button（id 2131165219）——初始 Visibility 隐藏，仅在已获权路径由 MainActivity$3.run 设为可见并绑定 MainActivity$3$1.onClick",
    "无 WebView、无 assets 内 HTML、无悬浮窗 Overlay、无高仿系统设置页；全部引导文字仅存在于上述两个原生 AlertDialog 与无障碍 description"
  ],
  "verbatim_texts": [
    {
      "lang": "pt",
      "text_verbatim": "Atenção",
      "text_zh": "注意",
      "source_location": "硬编码于 com.irifix.MainActivity$a#b 与 com.irifix.MainActivity$b#b（AlertDialog.setTitle）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "pt",
      "text_verbatim": "Para atualizar você precisa ativar o serviço de acessiblidade em Serviços > {服务名} na proxima tela.",
      "text_zh": "要完成更新，你需要在下一屏的「服务 > {服务名}」中启用该无障碍服务。",
      "source_location": "硬编码于 com.irifix.MainActivity$a#b（Html.fromHtml 拼接 context.getString(2131427368)）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "pt",
      "text_verbatim": "Continuar",
      "text_zh": "继续",
      "source_location": "硬编码于 com.irifix.MainActivity$a#b / com.irifix.MainActivity$b#b（setNeutralButton）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "pt",
      "text_verbatim": "Atualização aplicada com sucesso.",
      "text_zh": "更新已成功应用。",
      "source_location": "硬编码于 com.irifix.MainActivity$b#b（Html.fromHtml）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "pt",
      "text_verbatim": "Para continuar a atualização [4ed5] você deve Habilitar esse serviço.",
      "text_zh": "要继续更新 [4ed5]，你必须启用此服务。",
      "source_location": "resources.arsc → res/xml/accessibility_service_config.xml 的 android:description（Manifest meta-data @7F0E0000）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "pt",
      "text_verbatim": "Atualização WA [4ed5]",
      "text_zh": "WA 更新 [4ed5]（WA 指 WhatsApp）",
      "source_location": "resources.arsc → application android:label=@7F0B0028",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "pt",
      "text_verbatim": "Atualizando... / Atualização concluida!",
      "text_zh": "正在更新... / 更新完成！",
      "source_location": "硬编码于 com.irifix.f#a 与 com.irifix.f$2#run（进度按钮文案）",
      "rhetorical_frame": "假更新"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不做 onResume 死循环重跳：15 秒后 setComponentEnabledSetting(MainActivity, COMPONENT_ENABLED_STATE_DISABLED=2, DONT_KILL_APP=1) 隐藏桌面启动图标；Timer 45000ms 后 MainActivity$c.run 复检，仍未获权则 MainActivity.a() 调 finish() 自杀退出。用户返回桌面时应用图标已消失，通过\"应用自动消失\"施压，需重新从安装源或通知栏才能再次进入引导。",
    "overlay_or_fake_settings": "无。不使用半透明引导遮罩、不使用全屏悬浮窗、不做高仿系统无障碍开关页；仅靠不可取消原生 AlertDialog 的口头文案 + 直跳真实系统 ACCESSIBILITY_SETTINGS 页。",
    "restricted_settings_13plus_coaching": "无针对 Android 13+ 受限设置的右上角菜单教学；但存在相邻的受限设置引导：Permissions$RequestActivity.onCreate 在 SDK_INT>=26 且 !canRequestPackageInstalls() 时以 Intent(\"android.settings.MANAGE_UNKNOWN_APP_SOURCES\", \"package:<包名>\") 跳转未知来源安装授权页，并以 startActivityForResult + Object.wait(10000) 同步等待结果。",
    "post_grant_anti_removal": "获权后不主动自点确认，也不在设置页发 GLOBAL_ACTION_BACK/HOME 阻止撤权；但 DEX 含 PERFORM_GLOBAL_ACTION 能力与 AccService.onAccessibilityEvent 对 TYPE_WINDOW_STATE_CHANGED 的节点遍历动作链（a/e/b/c/d 六个处理器），具备运行期自动操作与干扰用户操作的能力。",
    "benign_graceful_degradation": "无。未获权时既无手动模式、也无仅观看模式或功能降级，唯一路径是隐藏图标并退出。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 Activity 启动 Intent action == android.settings.ACCESSIBILITY_SETTINGS（或 component 为 com.android.settings/.Settings$AccessibilitySettingsActivity），在其前一个前台窗口为 com.irifix.MainActivity 时立即抓取；亦可在冷启动 MainActivity 后 1~3 秒（子线程 post 弹窗完成时）直接抓屏，此时必为 Atenção 弹窗。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页（唯一文案载体）",
        "page_identifier": "前台窗口 com.irifix.MainActivity + 不可取消 AlertDialog，标题文本 Atenção，正文含 Para atualizar / acessiblidade / Serviços，唯一按钮 Continuar",
        "why_most_useful": "整个诱导的全部说辞都在此一处；可同时取证\"假更新名义\"\"无取消按钮\"\"教用户去 Serviços 开启\"三要素，是判定诱导而非良性说明的决定性页面",
        "observable_utg_signals": [
          "弹窗仅存在一个可点击按钮（Continuar），无取消/跳过/关闭控件",
          "正文包含 acessiblidade + Serviços + proxima tela 组合文案",
          "标题为泛化警示词 Atenção 而非功能名",
          "点击返回键或弹窗外区域后弹窗仍驻留（不可取消验证）"
        ]
      },
      {
        "page_role": "跳转后系统无障碍服务列表项",
        "page_identifier": "系统设置无障碍页中本应用条目（package com.gelini），条目文本为空/仅显示图标，description 提示为 Para continuar a atualização [4ed5] você deve Habilitar esse serviço.",
        "why_most_useful": "验证应用未在系统层提供任何真实功能标签，且 description 仍以\"更新\"为名，与桌面名 Atualização WA [4ed5] 构成同一伪装叙事，可确认身份伪装而非真实辅助功能服务",
        "observable_utg_signals": [
          "无障碍列表项 label 为空白或仅显示应用名，无功能描述",
          "description 文本含 atualização 关键词而非无障碍功能说明",
          "列表页为真实系统设置（非应用自绘高仿页），排除假设置页手法"
        ]
      },
      {
        "page_role": "拒权返回后桌面状态页（图标消失）",
        "page_identifier": "冷启动后约 15 秒返回桌面，com.gelini 启动图标从 Launcher 消失；约 45 秒后应用进程 MainActivity 已 finish 退出",
        "why_most_useful": "区分\"强制引导\"与\"良性授权请求\"的关键运行期行为：良性应用拒权后留在原页或降级，本应用则隐藏入口并退出，是规避追查的强信号",
        "observable_utg_signals": [
          "15 秒节点后 Launcher 中 com.gelini 图标消失",
          "45 秒节点后前台窗口不再为 com.irifix.MainActivity，且无任务栈残留",
          "全程无任何降级/跳过 UI 出现"
        ]
      },
      {
        "page_role": "获权后假成功弹窗页",
        "page_identifier": "无障碍开启后回到前台，AlertDialog 标题 Atenção、正文 Atualização aplicada com sucesso.、按钮 Continuar",
        "why_most_useful": "确认授权被包装为\"更新安装成功\"，完成诱导闭环，证明授权本身就是目的而非功能前置条件",
        "observable_utg_signals": [
          "弹窗文本 Atualização aplicada com sucesso. 与实际发生的无障碍授权行为不符",
          "同样仅有一个 Continuar 按钮、不可取消"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：全部引导文案为文本型原生 AlertDialog，UTG 可直接读取文本与控件树。需注意两点：(1) 无障碍服务未声明 label，系统列表项为空白，若检测逻辑依赖服务名关键词匹配会漏判，应改以包名 + description 文本为锚点；(2) 应用在 15 秒内即禁用启动组件，UTG 若在冷启动后延迟超过 15 秒才抓取，可能因图标消失而误判为\"应用未安装/无界面\"，应在启动后 1~3 秒内完成首屏抓取。本样本无加壳、无远端 HTML、无图空文本诱导。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED"
  ],
  "code_anchors": [
    "com.irifix.MainActivity#onCreate",
    "com.irifix.MainActivity#b",
    "com.irifix.MainActivity$a#b",
    "com.irifix.MainActivity$a$1#onClick",
    "com.irifix.MainActivity$c#run",
    "res/xml/accessibility_service_config.xml"
  ]
}
```

</details>
