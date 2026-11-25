# MB_035__b27e363d23｜AbereBot — Flash Player

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：126.3s

## 1. 一句话核心结论

- **核心申请方式**：伪装成 Flash Player 的 AbereBot 银行木马，冷启动检测无障碍未开启即直接跳系统无障碍设置并反复 Toast 提示，零说明零取消，获权后自动点 ALLOW、读联系人短信、下载远端注入页覆盖银行 App 并阻止卸载。
- **静态可见性说明**：无障碍申请/跳转路径（MainActivity.onCreate 判定 + ACTION_ACCESSIBILITY_SETTINGS 跳转 + Toast + 无障碍服务全量监听与 ALLOW 自动点击）全部静态可见、无加壳无密文；仅下游银行注入 HTML（GitHub aerebot123/564 下发的 <locale>.zip 解到 .injections/）与 Telegram Bot 控制通道为远端资产，静态包内不可见。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_WEBVIEW_REMOTE_URL`（远端下发HTML/WebView动态引导页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `b27e363d2365ea2cc02ce83fd92f62d0035b676b1a5b6d0a4ae91b07840fc4f9` |
| 包名 / 年份 | `com.example.autoclicker` / 2022 |
| 家族 / 品类 | **AbereBot**（同池样本数：1） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Flash Player |
| 引导页宣称品牌/身份 | Adobe Flash Player（伪造品牌，实际为银行钓鱼木马；包名 com.example.autoclicker 亦为无关占位名） |
| 系统无障碍列表服务名 | Flash Player（系统无障碍列表沿用应用 label @string/app_name，说明为 Please allow the app to make it working right.） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍说明文案极度模糊（Please allow the app to make it working right.）不披露真实用途；accessibility_service_config.xml 的 android:settingsActivity 指向不存在的 com.example.android.accessibility.ServiceSettingsActivity；包名 com.example.autoclicker 与显示名 Flash Player 完全不符；onCreate 检测 http.proxyHost/http.proxyPort，发现代理立即 finishAndRemoveTask() 反分析退出；真实功能文案（ALLOW/uninstall）以混淆资源 id 引用而非可读文本。 |
| 无障碍服务类名 | `com.example.autoclicker.AccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `READ_CONTACTS, RECEIVE_SMS` |
| 系统设置项说明 (`android:description`) | Please allow the app to make it working right. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.example.autoclicker.MainActivity（LAUNCHER 入口，无布局内容） | onCreate：读取 System.getProperty(http.proxyHost/http.proxyPort) 做反分析判定 | 不可静态还原 | 无 | 无 | `com.example.autoclicker.MainActivity.onCreate` |
| 2 | 跳无障碍设置 | MainActivity.onCreate → Settings.Secure 读取 enabled_accessibility_services 比对 ComponentName(MainActivity, AccessibilityService) | onCreate 中未在已启用列表找到自身无障碍服务组件 | 系统无障碍页 | **原文**：无（直接 startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))）<br>**译注**：未做任何说明，直接把用户甩到系统「无障碍」设置总列表页 | 要求用户自行在系统无障碍列表中找到 Flash Player 并打开开关；无取消、无跳过、无解释 | `com.example.autoclicker.MainActivity.onCreate` |
| 3 | 引导说明页 | 系统 Toast（连续弹出两次） | 跳转 ACCESSIBILITY_SETTINGS 后立即执行 | 通知栏 | **原文**：Please enable Flash Player!（"Please enable " + getString(0x7f0e001c) + "!"，0x7f0e001c = @string/app_name = Flash Player）<br>**译注**：请启用 Flash Player！ | 仅催促开启，无按钮、无关闭选项（Toast 自动消失） | `com.example.autoclicker.MainActivity.onCreate` |
| 4 | 系统无障碍列表项 | 系统 设置 → 无障碍 → 已下载/已安装的服务 中的 com.example.autoclicker.AccessibilityService | 用户进入无障碍设置页 | 系统无障碍页 | **原文**：Flash Player / Please allow the app to make it working right.<br>**译注**：Flash Player ／ 请允许该应用以使其正常工作。 | 要求用户点击该条目并开启开关（说明文字未披露会读取屏幕内容、点击按钮、读短信与联系人） | `res/xml/accessibility_service_config.xml + res/values/strings.xml#L30-L31` |
| 5 | 拒权反馈循环 | MainActivity 再次 onCreate / AccessibilityService.onServiceConnected 反向拉起 MainActivity / AlarmReceiver 每小时 onReceive | 用户从设置页返回但未开启服务；或应用被杀后再次冷启动；或 onServiceConnected 成功后 startActivity(MainActivity, BOTID) | 系统无障碍页 | **原文**：Please enable Flash Player!<br>**译注**：再次跳转无障碍设置并重复 Toast 催促 | 无退出路径：每次进入应用都会被重新跳到设置页，不提供降级/手动模式 | `com.example.autoclicker.MainActivity.onCreate / com.example.autoclicker.AccessibilityService.onServiceConnected / com.example.autoclicker.AlarmReceiver.onReceive` |
| 6 | 获权后动作 | AccessibilityService.onServiceConnected + MainActivity.onCreate 已启用分支 | 无障碍服务被系统连接（onServiceConnected），随后 onCreate 走 enabled 分支 | 原生Activity | **原文**：Please wait...<br>**译注**：请稍候……（同时静默申请 RECEIVE_SMS / READ_CONTACTS、下载注入包、向 Telegram 上报 BOT ID 与已装银行列表） | 无操作提示，用户仅看到 Please wait...；系统随后弹出短信/联系人权限框 | `com.example.autoclicker.AccessibilityService.onServiceConnected / com.example.autoclicker.MainActivity.onCreate` |
| 7 | 获权后动作 | AccessibilityService.a(AccessibilityNodeInfo) 监听 packageinstaller / permissioncontroller 窗口 | onAccessibilityEvent 收到包名为 packageinstaller 或 permissioncontroller 的事件 | 不可静态还原 | **原文**：ALLOW（@string/permission，id 0x7f0e0067）<br>**译注**：自动查找文本为 ALLOW 的节点并 performAction(CLICK)，代用户点「允许」，绕过权限弹窗确认 | 用户无需操作，权限确认被代点 | `com.example.autoclicker.AccessibilityService.a` |
| 8 | 获权后动作 | AccessibilityService.onAccessibilityEvent 检测 settings 页面文本 | 事件包名包含 settings 且界面出现文本 uninstall（0x7f0e006b） | 系统无障碍页 | **原文**：uninstall<br>**译注**：在系统设置（含卸载入口）页面看到「卸载」字样即发送 ACTION_MAIN/CATEGORY_HOME 跳回桌面，阻断卸载 | 用户被强制踢回桌面，无法完成卸载 | `com.example.autoclicker.AccessibilityService.onAccessibilityEvent` |
| 9 | 业务功能触发 | Bank Activity（WebView）加载 file://<externalFilesDir>/download/.injections/<bank>.html | 目标银行包（或 com.google.android.gm）触发 TYPE_WINDOW_STATE_CHANGED(2048)，注入文件存在且网络连通，Thread.sleep(4500) 后 startActivity(Bank) | 本地HTML WebView | **原文**：远端下发 HTML 内容，静态包内不可见<br>**译注**：覆盖真实银行界面，展示伪造登录页窃取凭证/验证码 | 用户在伪造页面输入账号密码与短信验证码 | `com.example.autoclicker.AccessibilityService.onAccessibilityEvent / com.example.autoclicker.Bank.onCreate` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统 Toast：MainActivity.onCreate 未启用分支连续两次 Toast "Please enable Flash Player!"（无任何自定义弹窗/Activity 承载）
- 系统无障碍列表条目：应用名 Flash Player + android:description "Please allow the app to make it working right."（res/values/strings.xml#L30-L31）
- 系统权限弹窗：由 AccessibilityService.a() 通过 findAccessibilityNodeInfosByText("ALLOW") 代点，文本来自 @string/permission=ALLOW
- 获权后 Toast："Please wait..."（MainActivity.onCreate enabled 分支）
- 远端 WebView 注入页：Bank.onCreate 加载 .injections/*.html，页面文案不在包内
- 不存在任何 assets 本地 HTML 教学页、悬浮窗遮罩或高仿无障碍开关页

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Please enable Flash Player! | 请启用 Flash Player！ | `com.example.autoclicker.MainActivity.onCreate 硬编码 + @string/app_name` | 假更新 |
| en | Please allow the app to make it working right. | 请允许该应用以使其正常工作。 | `strings.xml key accessibility_service_description（系统无障碍列表说明）` | 良性透明说明 |
| en | Flash Player | Flash Player（伪冒 Adobe 品牌） | `strings.xml key app_name / AndroidManifest android:label` | 假更新 |
| en | Please wait... | 请稍候…… | `com.example.autoclicker.MainActivity.onCreate 硬编码` | 未知 |
| en | ALLOW | 允许 | `strings.xml key permission（AccessibilityService.a 用于自动点击）` | 教唆忽视警告 |
| en | uninstall | 卸载 | `strings.xml key uninstall（onAccessibilityEvent 命中后跳桌面）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：无独立循环定时器：每次冷启动 onCreate 重新判定 enabled_accessibility_services，未启用即再次 startActivity(ACCESSIBILITY_SETTINGS)；此外 onServiceConnected 与 AlarmReceiver（1 小时 inexactRepeating）都会再次拉起 MainActivity 触发同一判定，用户返回设置页未开启后重进应用必被重跳，且无降级路径。
- **遮罩叠层 / 高仿系统设置页**：无遮罩、无悬浮窗、无高仿无障碍开关页；仅原生 Toast 催促 + 直接跳真实系统无障碍列表
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion 30，未做 Android 13 受限设置分步教学，也无 Session 安装器绕过）
- **获权后即时行为与防撤权机制**：有：onAccessibilityEvent 监听 settings 页面文本 "uninstall"（0x7f0e006b）命中即发 ACTION_MAIN/CATEGORY_HOME 跳桌面阻断卸载；另在 packageinstaller/permissioncontroller 自动点 ALLOW 代授权
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动 MainActivity 后监测到 Intent action=android.settings.ACCESSIBILITY_SETTINGS 的 startActivity 瞬间（或窗口切到 com.android.settings 无障碍页时）立即截图/取 UI 树，此时 Toast "Please enable Flash Player!" 与系统无障碍列表项同屏可采。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无纯图空文本盲区；但银行注入页 HTML 与 Telegram 控制通道由远端下发（GitHub aerebot123/564），静态包内无该页面文本，纯静态分析只能看到 Bank WebView 加载路径，需运行期抓取 .injections 文件才能取得钓鱼页原文。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转瞬间的 Toast + 系统无障碍总列表页** | com.android.settings 无障碍页 + Toast 文本 Please enable Flash Player! | 证明零说明直接跳转且用伪造品牌名催促，是判定 UTG 诱导最直接的一帧 | Toast 文本 Please enable Flash Player!；无障碍页出现条目 Flash Player；无任何前置说明页/弹窗 |
| **系统无障碍列表服务项详情** | 条目 Flash Player 与说明 Please allow the app to make it working right. | 说明文案与实际权限范围（canRetrieveWindowContent=true、typeAllMask）严重不符，是身份/用途隐瞒证据 | 服务名 Flash Player；说明 Please allow the app to make it working right.；包名 com.example.autoclicker |
| **获权后银行 App 覆盖页** | com.example.autoclicker.Bank WebView，URL 前缀 file://.../download/.injections/ | 确认获权真实用途为覆盖银行界面钓鱼，而非 Flash 相关功能 | 当前 Activity 为 com.example.autoclicker.Bank；WebView 载入 .injections/*.html；页面与前台银行 App 品牌一致 |
| **系统权限弹窗被自动代点** | packageinstaller/permissioncontroller 弹窗中 ALLOW 按钮被点击 | 证明无障碍能力被用于绕过用户授权确认 | 权限弹窗未触屏即消失/被点；短信、联系人权限状态变为已授予 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.example.autoclicker.MainActivity.onCreate`
- `com.example.autoclicker.AccessibilityService.onServiceConnected`
- `com.example.autoclicker.AccessibilityService.onAccessibilityEvent`
- `com.example.autoclicker.AccessibilityService.a`
- `com.example.autoclicker.Bank.onCreate`
- `res/xml/accessibility_service_config.xml + res/values/strings.xml#L30-L31`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，13 次工具调用）

**结论：该应用没有任何“引导说明页/教学弹窗”，而是冷启动即强制跳转系统无障碍设置，属于最粗暴的 UTG 诱导形态。**

1. **冷启动硬跳转**：[MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.example.autoclicker.MainActivity#onCreate>) 先做反分析检测（读 `http.proxyHost/http.proxyPort`，一旦设置代理即 `finishAndRemoveTask()` 退出），随后用 `Settings.Secure.getString("enabled_accessibility_services")` 逐项 `ComponentName` 比对自身服务；**未启用则直接 `startService(AccessibilityService)` + `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`**，并连续弹出两次 `Toast`：`"Please enable Flash Player!"`。无任何 Dialog、无取消/跳过按钮、无说明文案。
2. **拒权循环**：跳转后 Activity 结束流程；用户从设置页返回而未开启时，下一次冷启动（以及 `AccessibilityService.onServiceConnected()` 反向 `startActivity(MainActivity, BOTID)`、`AlarmReceiver` 每小时一次的重启）都会重新执行同一段判定并再次拉起设置页，形成反复重跳。
3. **无障碍说明极度模糊**：系统无障碍列表只显示应用名 `Flash Player`，说明文案为 [strings.xml:30](<resource-unit:#1 file:res/values/strings.xml#L30-L31>) `"Please allow the app to make it working right."`，完全不交代真实用途（点击银行界面、读验证码/联系人）。配置文件还把一个不存在的 `com.example.android.accessibility.ServiceSettingsActivity` 写成 `settingsActivity`。
4. **获权后立即滥用**：`onServiceConnected()` 设置 `eventTypes=-1` 全量监听，注册 1 小时周期 `AlarmReceiver`；`onCreate` 获权分支立即申请 `RECEIVE_SMS`/`READ_CONTACTS`、Toast `"Please wait..."`，并从 `https://github.com/yutronsayshi/aberebot123/raw/main/<locale>.zip` 下载注入包到 `.../files/download/.injections/`。
5. **权限弹窗自动点“允许”**：[AccessibilityService#a()](<resource-unit:#1.dex1 code:com.example.autoclicker.AccessibilityService#a>) 在 `packageinstaller`/`permissioncontroller` 界面上 `findAccessibilityNodeInfosByText("ALLOW")` 并 `performAction(CLICK)`（`public.xml` 证实 `0x7f0e0067 = "ALLOW"`）。
6. **反卸载**：[onAccessibilityEvent()](<resource-unit:#1.dex1 code:com.example.autoclicker.AccessibilityService#onAccessibilityEvent>) 中若 `settings` 页面出现文本 `"uninstall"`（`0x7f0e006b`）即发送 `CATEGORY_HOME` 把用户踢回桌面，阻止卸载。
7. **真实目的为银行钓鱼覆盖**：目标银行包（内置 200+ 银行/Gmail 名单）进入前台 `TYPE_WINDOW_STATE_CHANGED(2048)` 且注入 HTML 存在时，`Thread.sleep(4500)` 后拉起 [Bank.onCreate()](<resource-unit:#1.dex1 code:com.example.autoclicker.Bank#onCreate>)，WebView 加载 `file://.../.injections/<bank>.html` 覆盖银行 App。
8. 预筛的 `[zh-rCN] 不在允许的范围内：%1$s` 实为 Material 组件 `mtrl_picker_out_of_range` 框架字符串，与本样本诱导行为无关。
9. 注入 HTML 与 Telegram 控制通道（`api.telegram.org/bot…/sendMessage`，含 BOT ID、语言、已装银行列表、联系人）为远端资产，静态包内不可见。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍申请/跳转路径（MainActivity.onCreate 判定 + ACTION_ACCESSIBILITY_SETTINGS 跳转 + Toast + 无障碍服务全量监听与 ALLOW 自动点击）全部静态可见、无加壳无密文；仅下游银行注入 HTML（GitHub aerebot123/564 下发的 <locale>.zip 解到 .injections/）与 Telegram Bot 控制通道为远端资产，静态包内不可见。",
  "summary_one_liner": "伪装成 Flash Player 的 AbereBot 银行木马，冷启动检测无障碍未开启即直接跳系统无障碍设置并反复 Toast 提示，零说明零取消，获权后自动点 ALLOW、读联系人短信、下载远端注入页覆盖银行 App 并阻止卸载。",
  "disguise_identity": {
    "app_display_name": "Flash Player",
    "claimed_brand_or_persona": "Adobe Flash Player（伪造品牌，实际为银行钓鱼木马；包名 com.example.autoclicker 亦为无关占位名）",
    "a11y_service_label": "Flash Player（系统无障碍列表沿用应用 label @string/app_name，说明为 Please allow the app to make it working right.）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍说明文案极度模糊（Please allow the app to make it working right.）不披露真实用途；accessibility_service_config.xml 的 android:settingsActivity 指向不存在的 com.example.android.accessibility.ServiceSettingsActivity；包名 com.example.autoclicker 与显示名 Flash Player 完全不符；onCreate 检测 http.proxyHost/http.proxyPort，发现代理立即 finishAndRemoveTask() 反分析退出；真实功能文案（ALLOW/uninstall）以混淆资源 id 引用而非可读文本。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.example.autoclicker.MainActivity（LAUNCHER 入口，无布局内容）",
      "trigger_event": "onCreate：读取 System.getProperty(http.proxyHost/http.proxyPort) 做反分析判定",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面；检测到代理即静默退出",
      "user_action_requested": "无",
      "code_anchor": "com.example.autoclicker.MainActivity.onCreate"
    },
    {
      "step": 2,
      "stage": "跳无障碍设置",
      "screen_or_component": "MainActivity.onCreate → Settings.Secure 读取 enabled_accessibility_services 比对 ComponentName(MainActivity, AccessibilityService)",
      "trigger_event": "onCreate 中未在已启用列表找到自身无障碍服务组件",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（直接 startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))）",
      "shown_text_zh": "未做任何说明，直接把用户甩到系统「无障碍」设置总列表页",
      "user_action_requested": "要求用户自行在系统无障碍列表中找到 Flash Player 并打开开关；无取消、无跳过、无解释",
      "code_anchor": "com.example.autoclicker.MainActivity.onCreate"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "系统 Toast（连续弹出两次）",
      "trigger_event": "跳转 ACCESSIBILITY_SETTINGS 后立即执行",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "Please enable Flash Player!（\"Please enable \" + getString(0x7f0e001c) + \"!\"，0x7f0e001c = @string/app_name = Flash Player）",
      "shown_text_zh": "请启用 Flash Player！",
      "user_action_requested": "仅催促开启，无按钮、无关闭选项（Toast 自动消失）",
      "code_anchor": "com.example.autoclicker.MainActivity.onCreate"
    },
    {
      "step": 4,
      "stage": "系统无障碍列表项",
      "screen_or_component": "系统 设置 → 无障碍 → 已下载/已安装的服务 中的 com.example.autoclicker.AccessibilityService",
      "trigger_event": "用户进入无障碍设置页",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Flash Player / Please allow the app to make it working right.",
      "shown_text_zh": "Flash Player ／ 请允许该应用以使其正常工作。",
      "user_action_requested": "要求用户点击该条目并开启开关（说明文字未披露会读取屏幕内容、点击按钮、读短信与联系人）",
      "code_anchor": "res/xml/accessibility_service_config.xml + res/values/strings.xml#L30-L31"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity 再次 onCreate / AccessibilityService.onServiceConnected 反向拉起 MainActivity / AlarmReceiver 每小时 onReceive",
      "trigger_event": "用户从设置页返回但未开启服务；或应用被杀后再次冷启动；或 onServiceConnected 成功后 startActivity(MainActivity, BOTID)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Please enable Flash Player!",
      "shown_text_zh": "再次跳转无障碍设置并重复 Toast 催促",
      "user_action_requested": "无退出路径：每次进入应用都会被重新跳到设置页，不提供降级/手动模式",
      "code_anchor": "com.example.autoclicker.MainActivity.onCreate / com.example.autoclicker.AccessibilityService.onServiceConnected / com.example.autoclicker.AlarmReceiver.onReceive"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "AccessibilityService.onServiceConnected + MainActivity.onCreate 已启用分支",
      "trigger_event": "无障碍服务被系统连接（onServiceConnected），随后 onCreate 走 enabled 分支",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Please wait...",
      "shown_text_zh": "请稍候……（同时静默申请 RECEIVE_SMS / READ_CONTACTS、下载注入包、向 Telegram 上报 BOT ID 与已装银行列表）",
      "user_action_requested": "无操作提示，用户仅看到 Please wait...；系统随后弹出短信/联系人权限框",
      "code_anchor": "com.example.autoclicker.AccessibilityService.onServiceConnected / com.example.autoclicker.MainActivity.onCreate"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "AccessibilityService.a(AccessibilityNodeInfo) 监听 packageinstaller / permissioncontroller 窗口",
      "trigger_event": "onAccessibilityEvent 收到包名为 packageinstaller 或 permissioncontroller 的事件",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "ALLOW（@string/permission，id 0x7f0e0067）",
      "shown_text_zh": "自动查找文本为 ALLOW 的节点并 performAction(CLICK)，代用户点「允许」，绕过权限弹窗确认",
      "user_action_requested": "用户无需操作，权限确认被代点",
      "code_anchor": "com.example.autoclicker.AccessibilityService.a"
    },
    {
      "step": 8,
      "stage": "获权后动作",
      "screen_or_component": "AccessibilityService.onAccessibilityEvent 检测 settings 页面文本",
      "trigger_event": "事件包名包含 settings 且界面出现文本 uninstall（0x7f0e006b）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "uninstall",
      "shown_text_zh": "在系统设置（含卸载入口）页面看到「卸载」字样即发送 ACTION_MAIN/CATEGORY_HOME 跳回桌面，阻断卸载",
      "user_action_requested": "用户被强制踢回桌面，无法完成卸载",
      "code_anchor": "com.example.autoclicker.AccessibilityService.onAccessibilityEvent"
    },
    {
      "step": 9,
      "stage": "业务功能触发",
      "screen_or_component": "Bank Activity（WebView）加载 file://<externalFilesDir>/download/.injections/<bank>.html",
      "trigger_event": "目标银行包（或 com.google.android.gm）触发 TYPE_WINDOW_STATE_CHANGED(2048)，注入文件存在且网络连通，Thread.sleep(4500) 后 startActivity(Bank)",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "远端下发 HTML 内容，静态包内不可见",
      "shown_text_zh": "覆盖真实银行界面，展示伪造登录页窃取凭证/验证码",
      "user_action_requested": "用户在伪造页面输入账号密码与短信验证码",
      "code_anchor": "com.example.autoclicker.AccessibilityService.onAccessibilityEvent / com.example.autoclicker.Bank.onCreate"
    }
  ],
  "text_presentation_locations": [
    "系统 Toast：MainActivity.onCreate 未启用分支连续两次 Toast \"Please enable Flash Player!\"（无任何自定义弹窗/Activity 承载）",
    "系统无障碍列表条目：应用名 Flash Player + android:description \"Please allow the app to make it working right.\"（res/values/strings.xml#L30-L31）",
    "系统权限弹窗：由 AccessibilityService.a() 通过 findAccessibilityNodeInfosByText(\"ALLOW\") 代点，文本来自 @string/permission=ALLOW",
    "获权后 Toast：\"Please wait...\"（MainActivity.onCreate enabled 分支）",
    "远端 WebView 注入页：Bank.onCreate 加载 .injections/*.html，页面文案不在包内",
    "不存在任何 assets 本地 HTML 教学页、悬浮窗遮罩或高仿无障碍开关页"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Please enable Flash Player!",
      "text_zh": "请启用 Flash Player！",
      "source_location": "com.example.autoclicker.MainActivity.onCreate 硬编码 + @string/app_name",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Please allow the app to make it working right.",
      "text_zh": "请允许该应用以使其正常工作。",
      "source_location": "strings.xml key accessibility_service_description（系统无障碍列表说明）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Flash Player",
      "text_zh": "Flash Player（伪冒 Adobe 品牌）",
      "source_location": "strings.xml key app_name / AndroidManifest android:label",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Please wait...",
      "text_zh": "请稍候……",
      "source_location": "com.example.autoclicker.MainActivity.onCreate 硬编码",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "ALLOW",
      "text_zh": "允许",
      "source_location": "strings.xml key permission（AccessibilityService.a 用于自动点击）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "uninstall",
      "text_zh": "卸载",
      "source_location": "strings.xml key uninstall（onAccessibilityEvent 命中后跳桌面）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "无独立循环定时器：每次冷启动 onCreate 重新判定 enabled_accessibility_services，未启用即再次 startActivity(ACCESSIBILITY_SETTINGS)；此外 onServiceConnected 与 AlarmReceiver（1 小时 inexactRepeating）都会再次拉起 MainActivity 触发同一判定，用户返回设置页未开启后重进应用必被重跳，且无降级路径。",
    "overlay_or_fake_settings": "无遮罩、无悬浮窗、无高仿无障碍开关页；仅原生 Toast 催促 + 直接跳真实系统无障碍列表",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion 30，未做 Android 13 受限设置分步教学，也无 Session 安装器绕过）",
    "post_grant_anti_removal": "有：onAccessibilityEvent 监听 settings 页面文本 \"uninstall\"（0x7f0e006b）命中即发 ACTION_MAIN/CATEGORY_HOME 跳桌面阻断卸载；另在 packageinstaller/permissioncontroller 自动点 ALLOW 代授权",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动 MainActivity 后监测到 Intent action=android.settings.ACCESSIBILITY_SETTINGS 的 startActivity 瞬间（或窗口切到 com.android.settings 无障碍页时）立即截图/取 UI 树，此时 Toast \"Please enable Flash Player!\" 与系统无障碍列表项同屏可采。",
    "key_pages_to_capture": [
      {
        "page_role": "跳转瞬间的 Toast + 系统无障碍总列表页",
        "page_identifier": "com.android.settings 无障碍页 + Toast 文本 Please enable Flash Player!",
        "why_most_useful": "证明零说明直接跳转且用伪造品牌名催促，是判定 UTG 诱导最直接的一帧",
        "observable_utg_signals": ["Toast 文本 Please enable Flash Player!", "无障碍页出现条目 Flash Player", "无任何前置说明页/弹窗"]
      },
      {
        "page_role": "系统无障碍列表服务项详情",
        "page_identifier": "条目 Flash Player 与说明 Please allow the app to make it working right.",
        "why_most_useful": "说明文案与实际权限范围（canRetrieveWindowContent=true、typeAllMask）严重不符，是身份/用途隐瞒证据",
        "observable_utg_signals": ["服务名 Flash Player", "说明 Please allow the app to make it working right.", "包名 com.example.autoclicker"]
      },
      {
        "page_role": "获权后银行 App 覆盖页",
        "page_identifier": "com.example.autoclicker.Bank WebView，URL 前缀 file://.../download/.injections/",
        "why_most_useful": "确认获权真实用途为覆盖银行界面钓鱼，而非 Flash 相关功能",
        "observable_utg_signals": ["当前 Activity 为 com.example.autoclicker.Bank", "WebView 载入 .injections/*.html", "页面与前台银行 App 品牌一致"]
      },
      {
        "page_role": "系统权限弹窗被自动代点",
        "page_identifier": "packageinstaller/permissioncontroller 弹窗中 ALLOW 按钮被点击",
        "why_most_useful": "证明无障碍能力被用于绕过用户授权确认",
        "observable_utg_signals": ["权限弹窗未触屏即消失/被点", "短信、联系人权限状态变为已授予"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无纯图空文本盲区；但银行注入页 HTML 与 Telegram 控制通道由远端下发（GitHub aerebot123/564），静态包内无该页面文本，纯静态分析只能看到 Bank WebView 加载路径，需运行期抓取 .injections 文件才能取得钓鱼页原文。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_WEBVIEW_REMOTE_URL",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "LURE_DISMISS_SYSTEM_WARNING"
  ],
  "code_anchors": [
    "com.example.autoclicker.MainActivity.onCreate",
    "com.example.autoclicker.AccessibilityService.onServiceConnected",
    "com.example.autoclicker.AccessibilityService.onAccessibilityEvent",
    "com.example.autoclicker.AccessibilityService.a",
    "com.example.autoclicker.Bank.onCreate",
    "res/xml/accessibility_service_config.xml + res/values/strings.xml#L30-L31"
  ]
}
```

</details>
