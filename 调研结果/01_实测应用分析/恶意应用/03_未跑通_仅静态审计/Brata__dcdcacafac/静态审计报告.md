# MR_071__dcdcacafac｜Brata — Vivo Internet Gratis

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：157.1s

## 1. 一句话核心结论

- **核心申请方式**：冷启动延时5秒读取 accessibility_enabled，未开启即弹出仅有“Continuar”按钮的不可取消原生弹窗，以“提升兼容性”话术跳转系统无障碍设置，拒绝后秒级轮询并强制回桌面循环施压，获权后再以伪系统卸载提示误导并隐藏桌面图标。
- **静态可见性说明**：引导链全部静态可见：MainActivity.onCreate/n 的延时与门控、MainActivity$a 的不可取消弹窗、MainActivity$a$1 的 ACCESSIBILITY_SETTINGS 跳转、MainActivity$c 的秒级轮询与 HOME 强制、MainActivity$3 的图标禁用均在 DEX 明文中；提示文字来自 res/values/strings.xml 与硬编码字符串；无加壳、无 AES 密文、无远端 HTML 引导页。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `dcdcacafacb1f8a9474ff714dd418e0104e854b87ad07220ce5e4564568ce997` |
| 包名 / 年份 | `com.vivointernetgratis` / 2019 |
| 家族 / 品类 | **Brata**（同池样本数：8） |
| 原始来源标识 | https://gbhackers.com/brata-android-rat/ |
| 桌面显示名 | Vivo Internet Gratis |
| 引导页宣称品牌/身份 | Vivo（借 Vivo 品牌的“免费上网/网络福利”工具） |
| 系统无障碍列表服务名 | 未设置 android:label，系统无障碍列表项回退显示应用名 Vivo Internet Gratis；描述为“* Para melhorar a compatibilidade você deve ATIVAR.” |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务无独立 label，列表项直接沿用应用名以免暴露服务性质；无障碍描述与应用内弹窗复用同一句“兼容性”话术，把全窗口读取权限包装成兼容性修复；获权后 setComponentEnabledSetting 禁用 MainActivity 隐藏桌面图标；未使用空白/换行挤出、同形字、activity-alias 或伪造 isAccessibilityTool。 |
| 无障碍服务类名 | `com.vivointernetgratis.AccService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | * Para melhorar a compatibilidade você deve ATIVAR. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.vivointernetgratis.MainActivity（LAUNCHER，excludeFromRecents=true） | onCreate → new Thread(new MainActivity$1(this, 5000)).start()，首次启动固定 sleep 5000ms | 原生Activity | 无 | 无，用户无需操作 | `com.vivointernetgratis.MainActivity.onCreate / MainActivity$1.run` |
| 2 | 业务功能触发 | MainActivity.n() 权限状态门控 | 延时结束后调用 n()，读取 Settings.Secure.getInt("accessibility_enabled") 判定 | 不可静态还原（无界面，纯状态判定） | 无 | 无 | `com.vivointernetgratis.MainActivity.n / com.vivointernetgratis.f.e(Context)` |
| 3 | 引导说明页 | android.support.v7.app.AlertDialog（由 MainActivity$a.b(Context) 构造，setCancelable(false)） | 未获权分支 p.post(new MainActivity$4(this)) → MainActivity$a.b(n) | 原生Dialog | **原文**：Alerta / Para maior compatibilidade do App você deve ativar o serviço de acessiblidade em Serviços > Vivo Internet Gratis / Continuar<br>**译注**：警告 / 为了更好的应用兼容性，你必须在“服务 > Vivo Internet Gratis”中激活无障碍服务 / 继续 | 只能点击“Continuar”；setCancelable(false)，无取消、跳过或“以后再说”按钮，返回键亦被屏蔽 | `com.vivointernetgratis.MainActivity$a.b(Context)` |
| 4 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS（Intent 带 FLAG_ACTIVITY_NEW_TASK 等 268435456/32768/8388608） | 点击“Continuar” → MainActivity$a$1.onClick | 系统无障碍页 | **原文**：Alerta / * Para melhorar a compatibilidade você deve ATIVAR.<br>**译注**：警告 / * 为了提升兼容性你必须启用。 | 要求在系统无障碍列表中找到并手动开启“Vivo Internet Gratis”服务开关；应用侧无 APPLICATION_DETAILS_SETTINGS 跳转，也无“允许受限设置”教学 | `com.vivointernetgratis.MainActivity$a$1.onClick / res/xml/accessibility_service_config.xml / res/values/strings.xml accessibility_description` |
| 5 | 拒权反馈循环 | MainActivity$c（Timer 周期 0ms/1000ms）+ ACTION_MAIN/CATEGORY_HOME 启动器 | 诱导分支同时 r.schedule(new MainActivity$c(ctx), 0, 1000)；每次 tick 检查 accessibility_enabled，仍未开启且 elapsed>=45000ms 则 MainActivity.k() 关闭引导页；一旦为 1 立即 startActivity(HOME) | 系统无障碍页 / 桌面 | 无 | 无明确要求，用户返回桌面即被视为拒绝；重新打开应用会再次进入第 3 步弹窗 | `com.vivointernetgratis.MainActivity$c.run / MainActivity.k` |
| 6 | 获权后动作 | 第二条 AlertDialog（MainActivity$b.b，setCancelable(false)）+ MainActivity$3 隐藏图标 + GeneralService | accessibility_enabled==1 时 p.post(new MainActivity$2(this)) 立即弹窗；p.postDelayed(new MainActivity$3(this, ctx), 15000) 在 15 秒后执行 | 原生Dialog + 后台Service | **原文**：Alerta / O App é incompatível com este dispositivo e será desinstalado. / OK<br>**译注**：警告 / 本应用与设备不兼容，将被卸载。 / 确定 | 只能点“OK”，点击仅调用 finish() 关闭应用；同时在后台 GeneralService.a(ctx) 拉起常驻服务并 setComponentEnabledSetting(MainActivity, DISABLED, DONT_KILL_APP) 禁用桌面图标 | `com.vivointernetgratis.MainActivity$2.run / MainActivity$b.b / MainActivity$3.run / GeneralService.a(Context)` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 内不可取消 AlertDialog（标题 Alerta，正文“Para maior compatibilidade do App você deve ativar o serviço de acessiblidade em Serviços > Vivo Internet Gratis”，按钮 Continuar）——由 MainActivity$a.b 构造，setCancelable(false)
- 系统无障碍服务列表项的描述文本：res/xml/accessibility_service_config.xml 的 android:description → res/values/strings.xml 的 accessibility_description（* Para melhorar a compatibilidade você deve ATIVAR.）
- 获权后第二条不可取消 AlertDialog：标题 Alerta，正文“O App é incompatível com este dispositivo e será desinstalado.”，按钮 OK（MainActivity$b.b）
- 跳转系统设置页后应用侧无叠加遮罩/悬浮引导窗；引导话术完全依赖上述两条弹窗与系统无障碍描述，未使用 WebView/HTML 教学页

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| pt | Para maior compatibilidade do App você deve ativar o serviço de acessiblidade em Serviços > | 为了更好的应用兼容性，你必须在“服务 > （应用名）”中激活无障碍服务 | `com.vivointernetgratis.MainActivity$a.b 硬编码字符串（Html.fromHtml），拼接 context.getString(2131427358)=app_name` | 受限设置分步教学 |
| pt | Alerta | 警告 | `com.vivointernetgratis.MainActivity$a.b / MainActivity$b.b 硬编码 setTitle` | 故障恐吓 |
| pt | Continuar | 继续 | `com.vivointernetgratis.MainActivity$a.b 硬编码按钮文案` | 受限设置分步教学 |
| pt | * Para melhorar a compatibilidade você deve ATIVAR. | * 为了提升兼容性你必须启用。 | `res/values/strings.xml → accessibility_description（被 accessibility_service_config.xml 的 android:description 引用）` | 受限设置分步教学 |
| pt | O App é incompatível com este dispositivo e será desinstalado. | 本应用与设备不兼容，将被卸载。 | `com.vivointernetgratis.MainActivity$b.b 硬编码字符串` | 故障恐吓 |
| pt | OK | 确定 | `com.vivointernetgratis.MainActivity$b.b 硬编码按钮文案` | 故障恐吓 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：拒绝（返回/退到桌面）后应用侧每 1000ms 轮询 accessibility_enabled；45 秒仍未开启则调用 MainActivity.k() 关闭引导 Activity，用户下次启动或重新回到应用会再次执行 onCreate→5 秒延时→重弹同一不可取消弹窗；一旦检测到开关为 1 立即以 ACTION_MAIN/CATEGORY_HOME 强制把用户送回桌面，并在 100ms 后继续后续隐藏动作
- **遮罩叠层 / 高仿系统设置页**：无半透明引导遮罩、无全屏悬浮窗、无高仿系统无障碍开关页；仅使用原生 AlertDialog + 系统真实无障碍设置页。已申请 SYSTEM_ALERT_WINDOW 且 Permissions$RequestActivity 会跳 MANAGE_OVERLAY_PERMISSION，但本引导链未叠加遮罩
- **Android 13+ 受限设置（Restricted Settings）应对**：无。应用内未出现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转，也无“进入应用详情→右上角菜单→允许受限设置”或 Session 安装器绕过教学（targetSdk=27，本身不受 13+ 受限设置约束）
- **获权后即时行为与防撤权机制**：未监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权（AccService 中虽有 PERFORM_GLOBAL_ACTION 相关实现，但本次未确认用于撤权对抗）；已确认的对抗手段为获权后 15 秒调用 setComponentEnabledSetting(MainActivity, COMPONENT_ENABLED_STATE_DISABLED, DONT_KILL_APP) 禁用桌面图标，使用户找不到入口关闭无障碍或卸载，并以“设备不兼容将被卸载”伪系统提示误导用户
- **良性降级 / 替代方案**：无。未获权分支没有手动模式、只读模式、ADB 指引或功能降级路径，只有轮询施压与关闭引导页

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动后第 5 秒出现的不可取消 AlertDialog（标题“Alerta”、按钮仅“Continuar”）即为最佳抓取瞬间；同时监听 startActivity 到 android.settings.ACCESSIBILITY_SETTINGS 的跳转事件作为第二触发点，以及 accessibility_enabled 由 0 变 1 后 5 秒出现的“将被卸载”弹窗作为获权侧触发点
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：引导链为纯明文原生弹窗与系统设置页，无纯图空文本、无 WebView 外壳、无加壳。需注意两点：(1) 首次冷启动固定延时 5 秒，UTG 需等待 ≥6 秒再采样，否则会漏采弹窗；(2) 弹窗依赖 accessibility_enabled != 1 的前置状态，若测试机已开启任意无障碍服务将走“伪卸载”分支而不再出现引导弹窗，须先关闭全部无障碍服务。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页** | Dialog 标题“Alerta”，正文含“compatibilidade”“serviço de acessiblidade”，唯一按钮“Continuar”，无取消按钮且返回键无效 | 这是整个诱导链唯一的入口，可直接证明“仅单一继续按钮 + 兼容性话术”的强迫式引导性质，且与系统无障碍描述同源，最能区分诱导与良性说明 | 弹窗节点数量与可点击按钮列表仅 1 项（Continuar）；正文包含 compatibilidade/acessiblidade 关键词；无 dismiss/close 可访问节点，isCancelable=false |
| **系统无障碍服务列表项** | 设置→无障碍→已下载/已安装的服务中名为“Vivo Internet Gratis”的条目，摘要为“* Para melhorar a compatibilidade você deve ATIVAR.” | 证明应用把全窗口读取权限包装成“兼容性”修复，且服务无独立 label、直接冒用应用名，是身份伪装的直接证据 | 服务条目文本 = 应用名而非无障碍服务名；描述文本与 strings.xml accessibility_description 完全一致；开关状态节点可用于判定 accessibility_enabled |
| **设置页后返回/拒绝时的强制回桌面** | 系统无障碍页 → 1 秒内被 ACTION_MAIN/CATEGORY_HOME 顶替为桌面 | 验证秒级轮询与 HOME 强制行为，区分“良性跳转后停留在本页”与“检测到未开启即弹回桌面”的对抗式循环 | 前台包名在 1 秒内由 settings 切换为 launcher；每秒一次的窗口事件节拍；45 秒后应用引导 Activity 消失 |
| **获权后伪系统卸载弹窗页** | 标题“Alerta”，正文“O App é incompatível com este dispositivo e será desinstalado.”，按钮“OK” | 证明获权后立即用伪造的系统卸载提示误导用户并掩护后台隐藏图标动作 | 弹窗文本包含 incompatível/desinstalado；点击 OK 后应用进程仍存活并启动 Service；15 秒后桌面图标消失（component 被禁用） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.vivointernetgratis.MainActivity.onCreate`
- `com.vivointernetgratis.MainActivity.n`
- `com.vivointernetgratis.MainActivity$a.b(Context)`
- `com.vivointernetgratis.MainActivity$a$1.onClick`
- `com.vivointernetgratis.MainActivity$b.b(Context)`
- `res/values/strings.xml (accessibility_description) / res/xml/accessibility_service_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，纯运行期 UTG 视角）

- **触发时机**：冷启动即触发，无用户操作。`MainActivity.onCreate` 起线程 `sleep(5000)` → `n()`，先读 `Settings.Secure.accessibility_enabled` 判定分支，属 `cold_start_0_step`。
- **引导载体**：原生不可取消 AlertDialog（`setCancelable(false)`），标题 `"Alerta"`，正文葡萄牙语"为了更好的应用兼容性，你必须在 服务 > Vivo Internet Gratis 中激活无障碍服务"。唯一按钮 `Continuar`，**无取消/跳过**。
- **跳转点**：`MainActivity$a$1.onClick` 以 NEW_TASK 拉起 `android.settings.ACCESSIBILITY_SETTINGS`。**未发现** `ACTION_APPLICATION_DETAILS_SETTINGS`，也**无** 13+ 受限设置（"允许受限设置"）分步教学。
- **文字双背书**：同一话术同时写在系统无障碍列表描述 `res/values/strings.xml` 的 `accessibility_description`（`* Para melhorar a compatibilidade você deve ATIVAR.`）和运行期弹窗正文，形成"系统描述 + 应用弹窗"互相印证。
- **拒绝反馈循环**：未获权分支还起 `Timer`，每 1000ms 轮询 `accessibility_enabled`；一旦变为 1 立刻发 `ACTION_MAIN/CATEGORY_HOME` 强制回桌面；45 秒超时调 `k()` 关掉引导页，下次启动重弹。
- **获权后动作**：5 秒弹第二条不可取消弹窗"本应用与设备不兼容，将被卸载"（伪系统提示），仅 `OK`；15 秒后 `GeneralService.a()` 拉起常驻服务并 `setComponentEnabledSetting(MainActivity, DISABLED, DONT_KILL_APP)` **隐藏桌面图标**，使无障碍开关难以手动关闭。
- **身份**：桌面名 `Vivo Internet Gratis` 借用 Vivo 品牌，实为"免费上网"型诱导外壳；无障碍配置声明 `typeAllMask`、`flagRetrieveInteractiveWindows`、`canRetrieveWindowContent=true`，权限范围远超"兼容性"说法。
- **静态可见性**：`clear`——引导链全部为明文 Java 与资源，无加壳/加密/远端 HTML。

```json
{
  "static_visibility": "clear",
  "visibility_note": "引导链全部静态可见：MainActivity.onCreate/n 的延时与门控、MainActivity$a 的不可取消弹窗、MainActivity$a$1 的 ACCESSIBILITY_SETTINGS 跳转、MainActivity$c 的秒级轮询与 HOME 强制、MainActivity$3 的图标禁用均在 DEX 明文中；提示文字来自 res/values/strings.xml 与硬编码字符串；无加壳、无 AES 密文、无远端 HTML 引导页。",
  "summary_one_liner": "冷启动延时5秒读取 accessibility_enabled，未开启即弹出仅有“Continuar”按钮的不可取消原生弹窗，以“提升兼容性”话术跳转系统无障碍设置，拒绝后秒级轮询并强制回桌面循环施压，获权后再以伪系统卸载提示误导并隐藏桌面图标。",
  "disguise_identity": {
    "app_display_name": "Vivo Internet Gratis",
    "claimed_brand_or_persona": "Vivo（借 Vivo 品牌的“免费上网/网络福利”工具）",
    "a11y_service_label": "未设置 android:label，系统无障碍列表项回退显示应用名 Vivo Internet Gratis；描述为“* Para melhorar a compatibilidade você deve ATIVAR.”",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务无独立 label，列表项直接沿用应用名以免暴露服务性质；无障碍描述与应用内弹窗复用同一句“兼容性”话术，把全窗口读取权限包装成兼容性修复；获权后 setComponentEnabledSetting 禁用 MainActivity 隐藏桌面图标；未使用空白/换行挤出、同形字、activity-alias 或伪造 isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.vivointernetgratis.MainActivity（LAUNCHER，excludeFromRecents=true）",
      "trigger_event": "onCreate → new Thread(new MainActivity$1(this, 5000)).start()，首次启动固定 sleep 5000ms",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无（静默延时，界面为空白引导页布局）",
      "user_action_requested": "无，用户无需操作",
      "code_anchor": "com.vivointernetgratis.MainActivity.onCreate / MainActivity$1.run"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "MainActivity.n() 权限状态门控",
      "trigger_event": "延时结束后调用 n()，读取 Settings.Secure.getInt(\"accessibility_enabled\") 判定",
      "ui_carrier": "不可静态还原（无界面，纯状态判定）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无（==1 走已获权分支，否则走诱导分支）",
      "user_action_requested": "无",
      "code_anchor": "com.vivointernetgratis.MainActivity.n / com.vivointernetgratis.f.e(Context)"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "android.support.v7.app.AlertDialog（由 MainActivity$a.b(Context) 构造，setCancelable(false)）",
      "trigger_event": "未获权分支 p.post(new MainActivity$4(this)) → MainActivity$a.b(n)",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Alerta / Para maior compatibilidade do App você deve ativar o serviço de acessiblidade em Serviços > Vivo Internet Gratis / Continuar",
      "shown_text_zh": "警告 / 为了更好的应用兼容性，你必须在“服务 > Vivo Internet Gratis”中激活无障碍服务 / 继续",
      "user_action_requested": "只能点击“Continuar”；setCancelable(false)，无取消、跳过或“以后再说”按钮，返回键亦被屏蔽",
      "code_anchor": "com.vivointernetgratis.MainActivity$a.b(Context)"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS（Intent 带 FLAG_ACTIVITY_NEW_TASK 等 268435456/32768/8388608）",
      "trigger_event": "点击“Continuar” → MainActivity$a$1.onClick",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Alerta / * Para melhorar a compatibilidade você deve ATIVAR.",
      "shown_text_zh": "警告 / * 为了提升兼容性你必须启用。",
      "user_action_requested": "要求在系统无障碍列表中找到并手动开启“Vivo Internet Gratis”服务开关；应用侧无 APPLICATION_DETAILS_SETTINGS 跳转，也无“允许受限设置”教学",
      "code_anchor": "com.vivointernetgratis.MainActivity$a$1.onClick / res/xml/accessibility_service_config.xml / res/values/strings.xml accessibility_description"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity$c（Timer 周期 0ms/1000ms）+ ACTION_MAIN/CATEGORY_HOME 启动器",
      "trigger_event": "诱导分支同时 r.schedule(new MainActivity$c(ctx), 0, 1000)；每次 tick 检查 accessibility_enabled，仍未开启且 elapsed>=45000ms 则 MainActivity.k() 关闭引导页；一旦为 1 立即 startActivity(HOME)",
      "ui_carrier": "系统无障碍页 / 桌面",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无（拒绝后不提示，仅每秒轮询并在超时后关闭引导页，下次启动重新弹窗）",
      "user_action_requested": "无明确要求，用户返回桌面即被视为拒绝；重新打开应用会再次进入第 3 步弹窗",
      "code_anchor": "com.vivointernetgratis.MainActivity$c.run / MainActivity.k"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "第二条 AlertDialog（MainActivity$b.b，setCancelable(false)）+ MainActivity$3 隐藏图标 + GeneralService",
      "trigger_event": "accessibility_enabled==1 时 p.post(new MainActivity$2(this)) 立即弹窗；p.postDelayed(new MainActivity$3(this, ctx), 15000) 在 15 秒后执行",
      "ui_carrier": "原生Dialog + 后台Service",
      "shown_text_verbatim": "Alerta / O App é incompatível com este dispositivo e será desinstalado. / OK",
      "shown_text_zh": "警告 / 本应用与设备不兼容，将被卸载。 / 确定",
      "user_action_requested": "只能点“OK”，点击仅调用 finish() 关闭应用；同时在后台 GeneralService.a(ctx) 拉起常驻服务并 setComponentEnabledSetting(MainActivity, DISABLED, DONT_KILL_APP) 禁用桌面图标",
      "code_anchor": "com.vivointernetgratis.MainActivity$2.run / MainActivity$b.b / MainActivity$3.run / GeneralService.a(Context)"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 内不可取消 AlertDialog（标题 Alerta，正文“Para maior compatibilidade do App você deve ativar o serviço de acessiblidade em Serviços > Vivo Internet Gratis”，按钮 Continuar）——由 MainActivity$a.b 构造，setCancelable(false)",
    "系统无障碍服务列表项的描述文本：res/xml/accessibility_service_config.xml 的 android:description → res/values/strings.xml 的 accessibility_description（* Para melhorar a compatibilidade você deve ATIVAR.）",
    "获权后第二条不可取消 AlertDialog：标题 Alerta，正文“O App é incompatível com este dispositivo e será desinstalado.”，按钮 OK（MainActivity$b.b）",
    "跳转系统设置页后应用侧无叠加遮罩/悬浮引导窗；引导话术完全依赖上述两条弹窗与系统无障碍描述，未使用 WebView/HTML 教学页"
  ],
  "verbatim_texts": [
    {
      "lang": "pt",
      "text_verbatim": "Para maior compatibilidade do App você deve ativar o serviço de acessiblidade em Serviços > ",
      "text_zh": "为了更好的应用兼容性，你必须在“服务 > （应用名）”中激活无障碍服务",
      "source_location": "com.vivointernetgratis.MainActivity$a.b 硬编码字符串（Html.fromHtml），拼接 context.getString(2131427358)=app_name",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "pt",
      "text_verbatim": "Alerta",
      "text_zh": "警告",
      "source_location": "com.vivointernetgratis.MainActivity$a.b / MainActivity$b.b 硬编码 setTitle",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "pt",
      "text_verbatim": "Continuar",
      "text_zh": "继续",
      "source_location": "com.vivointernetgratis.MainActivity$a.b 硬编码按钮文案",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "pt",
      "text_verbatim": "* Para melhorar a compatibilidade você deve ATIVAR.",
      "text_zh": "* 为了提升兼容性你必须启用。",
      "source_location": "res/values/strings.xml → accessibility_description（被 accessibility_service_config.xml 的 android:description 引用）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "pt",
      "text_verbatim": "O App é incompatível com este dispositivo e será desinstalado.",
      "text_zh": "本应用与设备不兼容，将被卸载。",
      "source_location": "com.vivointernetgratis.MainActivity$b.b 硬编码字符串",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "pt",
      "text_verbatim": "OK",
      "text_zh": "确定",
      "source_location": "com.vivointernetgratis.MainActivity$b.b 硬编码按钮文案",
      "rhetorical_frame": "故障恐吓"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "拒绝（返回/退到桌面）后应用侧每 1000ms 轮询 accessibility_enabled；45 秒仍未开启则调用 MainActivity.k() 关闭引导 Activity，用户下次启动或重新回到应用会再次执行 onCreate→5 秒延时→重弹同一不可取消弹窗；一旦检测到开关为 1 立即以 ACTION_MAIN/CATEGORY_HOME 强制把用户送回桌面，并在 100ms 后继续后续隐藏动作",
    "overlay_or_fake_settings": "无半透明引导遮罩、无全屏悬浮窗、无高仿系统无障碍开关页；仅使用原生 AlertDialog + 系统真实无障碍设置页。已申请 SYSTEM_ALERT_WINDOW 且 Permissions$RequestActivity 会跳 MANAGE_OVERLAY_PERMISSION，但本引导链未叠加遮罩",
    "restricted_settings_13plus_coaching": "无。应用内未出现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转，也无“进入应用详情→右上角菜单→允许受限设置”或 Session 安装器绕过教学（targetSdk=27，本身不受 13+ 受限设置约束）",
    "post_grant_anti_removal": "未监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权（AccService 中虽有 PERFORM_GLOBAL_ACTION 相关实现，但本次未确认用于撤权对抗）；已确认的对抗手段为获权后 15 秒调用 setComponentEnabledSetting(MainActivity, COMPONENT_ENABLED_STATE_DISABLED, DONT_KILL_APP) 禁用桌面图标，使用户找不到入口关闭无障碍或卸载，并以“设备不兼容将被卸载”伪系统提示误导用户",
    "benign_graceful_degradation": "无。未获权分支没有手动模式、只读模式、ADB 指引或功能降级路径，只有轮询施压与关闭引导页"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动后第 5 秒出现的不可取消 AlertDialog（标题“Alerta”、按钮仅“Continuar”）即为最佳抓取瞬间；同时监听 startActivity 到 android.settings.ACCESSIBILITY_SETTINGS 的跳转事件作为第二触发点，以及 accessibility_enabled 由 0 变 1 后 5 秒出现的“将被卸载”弹窗作为获权侧触发点",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页",
        "page_identifier": "Dialog 标题“Alerta”，正文含“compatibilidade”“serviço de acessiblidade”，唯一按钮“Continuar”，无取消按钮且返回键无效",
        "why_most_useful": "这是整个诱导链唯一的入口，可直接证明“仅单一继续按钮 + 兼容性话术”的强迫式引导性质，且与系统无障碍描述同源，最能区分诱导与良性说明",
        "observable_utg_signals": ["弹窗节点数量与可点击按钮列表仅 1 项（Continuar）", "正文包含 compatibilidade/acessiblidade 关键词", "无 dismiss/close 可访问节点，isCancelable=false"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置→无障碍→已下载/已安装的服务中名为“Vivo Internet Gratis”的条目，摘要为“* Para melhorar a compatibilidade você deve ATIVAR.”",
        "why_most_useful": "证明应用把全窗口读取权限包装成“兼容性”修复，且服务无独立 label、直接冒用应用名，是身份伪装的直接证据",
        "observable_utg_signals": ["服务条目文本 = 应用名而非无障碍服务名", "描述文本与 strings.xml accessibility_description 完全一致", "开关状态节点可用于判定 accessibility_enabled"]
      },
      {
        "page_role": "设置页后返回/拒绝时的强制回桌面",
        "page_identifier": "系统无障碍页 → 1 秒内被 ACTION_MAIN/CATEGORY_HOME 顶替为桌面",
        "why_most_useful": "验证秒级轮询与 HOME 强制行为，区分“良性跳转后停留在本页”与“检测到未开启即弹回桌面”的对抗式循环",
        "observable_utg_signals": ["前台包名在 1 秒内由 settings 切换为 launcher", "每秒一次的窗口事件节拍", "45 秒后应用引导 Activity 消失"]
      },
      {
        "page_role": "获权后伪系统卸载弹窗页",
        "page_identifier": "标题“Alerta”，正文“O App é incompatível com este dispositivo e será desinstalado.”，按钮“OK”",
        "why_most_useful": "证明获权后立即用伪造的系统卸载提示误导用户并掩护后台隐藏图标动作",
        "observable_utg_signals": ["弹窗文本包含 incompatível/desinstalado", "点击 OK 后应用进程仍存活并启动 Service", "15 秒后桌面图标消失（component 被禁用）"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：引导链为纯明文原生弹窗与系统设置页，无纯图空文本、无 WebView 外壳、无加壳。需注意两点：(1) 首次冷启动固定延时 5 秒，UTG 需等待 ≥6 秒再采样，否则会漏采弹窗；(2) 弹窗依赖 accessibility_enabled != 1 的前置状态，若测试机已开启任意无障碍服务将走“伪卸载”分支而不再出现引导弹窗，须先关闭全部无障碍服务。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.vivointernetgratis.MainActivity.onCreate",
    "com.vivointernetgratis.MainActivity.n",
    "com.vivointernetgratis.MainActivity$a.b(Context)",
    "com.vivointernetgratis.MainActivity$a$1.onClick",
    "com.vivointernetgratis.MainActivity$b.b(Context)",
    "res/values/strings.xml (accessibility_description) / res/xml/accessibility_service_config.xml"
  ]
}
```

</details>
