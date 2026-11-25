# MR_118__d86e540090｜StealJob — Google Update Service

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：92.8s

## 1. 一句话核心结论

- **核心申请方式**：冒用 'Google Update Service' 品牌，冷启动即弹不可取消原生对话框，仅给 'Ok' 一键直达系统无障碍列表诱骗开启可读取全屏文本的 ninere 服务，拒绝或退出则禁用自身组件并删除桌面图标隐身。
- **静态可见性说明**：引导链全部为 DEX 内原生 Java 代码与本地资源实现，无加壳、无 AES 载荷、无远端 HTML、无动态下发 UI；引导文案硬编码于 MainActivity.onCreate，字符串资源仅 res/values/strings.xml 一条 app_name，无障碍能力声明在 res/xml/accessibility.xml，均可完整静态还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `d86e540090342256986bfb56795f5d6ae3a3fb2814c2a3f3f85d8fb98929fcf9` |
| 包名 / 年份 | `com.update.gooqle` / 2019 |
| 家族 / 品类 | **StealJob**（同池样本数：4） |
| 原始来源标识 | https://ti.360.net/blog/articles/stealjob-new-android-malware-used-by-donot-apt-group-en/ |
| 桌面显示名 | Google Update Service |
| 引导页宣称品牌/身份 | Google Update Service（Google 官方更新服务） |
| 系统无障碍列表服务名 | Google Update Service |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：三处身份（桌面 label、无障碍服务 label、accessibility.xml 的 android:description）统一冒用 Google 品牌，包名 com.update.gooqle 用 'gooqle' 同形拼写近似 'google'；类名整体混淆（nine.ninere、hundred、ten.ten、onere）掩盖真实用途；无空白/换行挤出警告、无多 activity-alias、无伪造 isAccessibilityTool。 |
| 无障碍服务类名 | `com.jgoogle.android.gservicekns.nine.ninere` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, SEND_SMS, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Google Update Service |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.jgoogle.android.gservicekns.MainActivity（LAUNCHER Activity） | onCreate(Bundle) 在 super.onCreate 后先执行 c.o() 注册 job_demo_tag 周期任务，再调用 a(Context) 检查无障碍是否已开启 | 原生Activity | 无 | 无需操作，进入即自动判定 | `com.jgoogle.android.gservicekns.MainActivity#onCreate` |
| 2 | 引导说明页 | AlertDialog（AlertDialog.Builder 原生对话框，setCancelable(false)） | a(Context) 读取 Settings.Secure.accessibility_enabled 与 enabled_accessibility_services，未匹配到 "包名/com.jgoogle.android.gservicekns.nine.ninere" 时返回 false，onCreate 随即弹出 | 原生Dialog | **原文**：Please enable 'Accessibility' for 'Google Update Service' to get this working. Tap on 'Ok' to go to Accessibility Settings.<br>**译注**：请为“Google Update Service”开启“无障碍”功能以便其正常工作。点击“确定”前往无障碍设置。 | 仅有一个 PositiveButton“Ok”；setCancelable(false)，无取消/跳过/稍后按钮，返回键直接退出并触发隐藏逻辑 | `com.jgoogle.android.gservicekns.MainActivity#onCreate（setMessage/setCancelable/setPositiveButton）` |
| 3 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表） | MainActivity$1.onClick(DialogInterface, int) 被“Ok”触发，执行 startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS")) | 系统无障碍页 | 无 | 用户在系统列表中手动勾选并确认“Google Update Service”；应用不提供任何应用内二次引导页或分步图文教学 | `com.jgoogle.android.gservicekns.MainActivity$1#onClick` |
| 4 | 拒权反馈循环 | MainActivity 自身 + PackageManager 组件禁用 + 桌面快捷方式删除广播 | 用户按返回键（onBackPressed）或 Activity 销毁（onDestroy）时调用 a() | 不可静态还原 | 无 | 无提示、无解释；用户仅观察到图标消失，无法再通过桌面入口复核或撤权 | `com.jgoogle.android.gservicekns.MainActivity#onBackPressed → MainActivity#a()` |
| 5 | 获权后动作 | com.jgoogle.android.gservicekns.nine.ninere（AccessibilityService，canRetrieveWindowContent=true） | 系统绑定服务触发 onServiceConnected()；随后 onAccessibilityEvent(AccessibilityEvent) 处理 8/16/32/2048 事件 | 不可静态还原 | 无 | 无需操作，获权后即静默采集屏幕文本 | `com.jgoogle.android.gservicekns.nine.ninere#onServiceConnected / #onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity.onCreate 中不可取消的原生 AlertDialog（setCancelable(false)）——唯一的应用内引导文案载体，纯 Java 硬编码字符串，未走 strings.xml
- res/values/strings.xml 的 app_name = "Google Update Service"——同时用于桌面图标名、无障碍服务 label 与 accessibility.xml 的 android:description，是系统无障碍列表项的展示文本
- res/xml/accessibility.xml 第 2 行 android:description="@string/app_name"——系统无障碍设置列表中该服务下方的说明文字
- 无 WebView/HTML 教学页、无悬浮窗遮罩、无伪系统设置界面、无通知栏提示

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Please enable 'Accessibility' for 'Google Update Service' to get this working. Tap on 'Ok' to go to Accessibility Settings. | 请为“Google Update Service”开启“无障碍”功能以便其正常工作。点击“确定”前往无障碍设置。 | `硬编码于 com.jgoogle.android.gservicekns.MainActivity#onCreate 的 alertDialog$Builder.setMessage(...)` | 假更新 |
| en | Google Update Service | 谷歌更新服务 | `res/values/strings.xml 第 20 行 key=app_name（同时作为无障碍服务 label 与 accessibility.xml 的 android:description）` | 假更新 |
| en | Ok | 确定 | `硬编码于 com.jgoogle.android.gservicekns.MainActivity#onCreate 的 setPositiveButton("Ok", new MainActivity$1(this))` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不死循环重跳。onBackPressed 与 onDestroy 均调用 MainActivity#a()，静默执行 setComponentEnabledSetting(getComponentName(), COMPONENT_ENABLED_STATE_DISABLED, DONT_KILL_APP) 禁用启动组件并广播 UNINSTALL_SHORTCUT 删除桌面图标；应用从桌面消失，用户难以再次进入复核或撤权，也规避安全软件的人工复查。
- **遮罩叠层 / 高仿系统设置页**：无。不使用半透明遮罩、全屏悬浮窗或高仿系统无障碍开关页，完全依赖系统原生设置页（ACTION_ACCESSIBILITY_SETTINGS）。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。代码中未出现 ACTION_APPLICATION_DETAILS_SETTINGS，也没有“右上角菜单允许受限设置”或 Session 安装器绕过等分步教学；targetSdkVersion=22，本身不受 Android 13 受限设置机制约束。
- **获权后即时行为与防撤权机制**：无自点确认、无 GLOBAL_ACTION_BACK/HOME 阻止撤权；但通过禁用自身组件 + 删除桌面快捷方式使应用隐身，属获权后的反排查手段。
- **良性降级 / 替代方案**：无。不存在手动模式、仅观看模式或任何不开启无障碍的替代使用路径。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动 MainActivity 后首个 AlertDialog 弹出瞬间（文本含 'Please enable' 与 'Google Update Service'），以及紧随其后的 startActivity("android.settings.ACCESSIBILITY_SETTINGS") 跳转动作；两者间隔极短，建议在冷启动后 1 秒内开始高频抓页。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：引导文案为纯文本原生 Dialog，可被 UTG 直接提取，无需 OCR。需注意两点：(1) 该应用不使用任何应用内二次教学页或遮罩层，获权后的实际行为（屏幕文本采集与外发）发生在无障碍服务内部，UTG 只能观察到系统无障碍列表与桌面变化，需配合网络抓包或 Hook Settings.Secure / AccessibilityEvent 佐证；(2) 冷启动弹窗到跳转设置页间隔极短，若抓页频率不足可能漏掉弹窗，建议在 application onCreate 或 MainActivity onCreate 处下 Hook 触发抓页。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页（唯一应用内引导载体）** | AlertDialog 文本 'Please enable \'Accessibility\' for \'Google Update Service\' to get this working.'，仅一个 'Ok' 按钮，无取消/关闭按钮 | 该弹窗是判定“强制诱导”的核心证据：不可取消 + 单按钮 + 冒用 Google 品牌 + 不说明用途，四要素同时出现在同一页面，可直接定性。 | 对话框存在且无 cancel/negative 按钮节点；按钮文案为 'Ok'，点击后立即进入 android.settings.ACCESSIBILITY_SETTINGS；文案中出现 'Google Update Service' 与 'Accessibility' 的强制关联；对话框背后无其他业务界面（MainActivity 无 setContentView 业务布局） |
| **系统无障碍服务列表项** | com.android.settings 无障碍列表中名为 'Google Update Service' 的条目及其下方说明文字 | 确认应用在系统列表中伪装成 Google 更新服务、说明文字与桌面名一致且完全未披露“读取屏幕内容”能力，是身份冒用的直接可视证据。 | 列表项标题为 'Google Update Service'；说明文字同为 'Google Update Service'，无用途说明；勾选后系统弹出的高危能力警告页（允许查看和控制屏幕）；返回桌面后启动图标已消失 |
| **拒权后桌面状态（图标消失）** | 返回键退出后桌面 launcher 中不再存在该应用图标 | 验证“拒绝即隐身”的反排查行为，是区别于普通良性无障碍应用的关键运行期特征。 | 返回键后应用界面直接关闭且无二次弹窗；桌面图标/快捷方式消失；adb shell pm list packages 仍存在 com.update.gooqle 但 launcher 组件被禁用 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.jgoogle.android.gservicekns.MainActivity#onCreate`
- `com.jgoogle.android.gservicekns.MainActivity$1#onClick`
- `com.jgoogle.android.gservicekns.MainActivity#a(android.content.Context)`
- `com.jgoogle.android.gservicekns.MainActivity#a()`
- `com.jgoogle.android.gservicekns.nine.ninere#onAccessibilityEvent`
- `res/xml/accessibility.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论

**可见性：完全静态可见（无加壳、无密文载荷、无远端 HTML 引导）。** 整条引导链为原生 Java 代码实现，不含 WebView、不含悬浮窗遮罩、不含伪系统设置页。

**引导链（单步强制式，无任何柔性设计）：**

1. **冷启动入口** — `MainActivity.onCreate()` 先调用 `c.o()` 注册 Evernote Job，随后调用 `a(Context)` 检查无障碍状态。
2. **状态判定** — 读 `Settings.Secure.accessibility_enabled` 与 `enabled_accessibility_services`，逐项比对 `包名/ninere 规范类名`，精确判断本应用服务是否被勾选。
3. **引导说明页（不可取消原生 Dialog）** — `AlertDialog.Builder`，`setCancelable(false)`，只有 `PositiveButton("Ok")`；无取消、无跳过、无"稍后再说"、无隐私用途说明。文案直接把"Google Update Service"当作可信主体。
4. **跳受限设置** — `MainActivity$1.onClick()` 执行 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`。**代码中不存在 `ACTION_APPLICATION_DETAILS_SETTINGS`，也没有 Android 13+ 受限设置分步教学**，全部依赖用户在系统无障碍列表中自行找到该项。
5. **拒权反馈** — 用户按返回键（`onBackPressed`）不重弹、不循环，而是直接调用 `a()`：`setComponentEnabledSetting(..., COMPONENT_ENABLED_STATE_DISABLED, DONT_KILL_APP)` 禁用自身启动组件 + 广播 `UNINSTALL_SHORTCUT` 删除桌面图标。即"拒绝即隐身"，规避撤权与安全复核，比死循环重跳更隐蔽。
6. **获权后动作** — `ninere.onServiceConnected()` 初始化 MD5 与缓存；`onAccessibilityEvent()` 监听 8/16/32/2048 事件，采集前台包名与 `event.getText()` 累积入列表后由 `ninere$a` 线程外发（屏幕文本窃取，StealJob 家族典型）。

**身份伪装要点：** 桌面名、无障碍服务 label、`accessibility.xml` 的 `android:description` 三处**统一**为 `Google Update Service`，与包名 `com.update.gooqle` 呼应，形成完整假品牌闭环；服务说明完全不暴露"读取屏幕内容"的真实用途（配置 `canRetrieveWindowContent="true"` + 5 类事件）。代码类名全混淆为 `nine.ninere`、`hundred`、`ten.ten` 等，属家族特征命名。

**已登记风险：** R-001（high / malware_trojan，source_mode = autonomous_audit）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "引导链全部为 DEX 内原生 Java 代码与本地资源实现，无加壳、无 AES 载荷、无远端 HTML、无动态下发 UI；引导文案硬编码于 MainActivity.onCreate，字符串资源仅 res/values/strings.xml 一条 app_name，无障碍能力声明在 res/xml/accessibility.xml，均可完整静态还原。",
  "summary_one_liner": "冒用 'Google Update Service' 品牌，冷启动即弹不可取消原生对话框，仅给 'Ok' 一键直达系统无障碍列表诱骗开启可读取全屏文本的 ninere 服务，拒绝或退出则禁用自身组件并删除桌面图标隐身。",
  "disguise_identity": {
    "app_display_name": "Google Update Service",
    "claimed_brand_or_persona": "Google Update Service（Google 官方更新服务）",
    "a11y_service_label": "Google Update Service",
    "identity_mismatch": true,
    "obfuscation_tricks": "三处身份（桌面 label、无障碍服务 label、accessibility.xml 的 android:description）统一冒用 Google 品牌，包名 com.update.gooqle 用 'gooqle' 同形拼写近似 'google'；类名整体混淆（nine.ninere、hundred、ten.ten、onere）掩盖真实用途；无空白/换行挤出警告、无多 activity-alias、无伪造 isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.jgoogle.android.gservicekns.MainActivity（LAUNCHER Activity）",
      "trigger_event": "onCreate(Bundle) 在 super.onCreate 后先执行 c.o() 注册 job_demo_tag 周期任务，再调用 a(Context) 检查无障碍是否已开启",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "该步无可视界面，仅后台注册任务并检测无障碍开关状态",
      "user_action_requested": "无需操作，进入即自动判定",
      "code_anchor": "com.jgoogle.android.gservicekns.MainActivity#onCreate"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "AlertDialog（AlertDialog.Builder 原生对话框，setCancelable(false)）",
      "trigger_event": "a(Context) 读取 Settings.Secure.accessibility_enabled 与 enabled_accessibility_services，未匹配到 \"包名/com.jgoogle.android.gservicekns.nine.ninere\" 时返回 false，onCreate 随即弹出",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Please enable 'Accessibility' for 'Google Update Service' to get this working. Tap on 'Ok' to go to Accessibility Settings.",
      "shown_text_zh": "请为“Google Update Service”开启“无障碍”功能以便其正常工作。点击“确定”前往无障碍设置。",
      "user_action_requested": "仅有一个 PositiveButton“Ok”；setCancelable(false)，无取消/跳过/稍后按钮，返回键直接退出并触发隐藏逻辑",
      "code_anchor": "com.jgoogle.android.gservicekns.MainActivity#onCreate（setMessage/setCancelable/setPositiveButton）"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表）",
      "trigger_event": "MainActivity$1.onClick(DialogInterface, int) 被“Ok”触发，执行 startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "跳转至系统无障碍设置列表，由用户自行在列表中找到名为“Google Update Service”的服务并手动打开开关",
      "user_action_requested": "用户在系统列表中手动勾选并确认“Google Update Service”；应用不提供任何应用内二次引导页或分步图文教学",
      "code_anchor": "com.jgoogle.android.gservicekns.MainActivity$1#onClick"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity 自身 + PackageManager 组件禁用 + 桌面快捷方式删除广播",
      "trigger_event": "用户按返回键（onBackPressed）或 Activity 销毁（onDestroy）时调用 a()",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "不重弹对话框、不循环拉起设置页，而是直接静默禁用启动组件并广播 com.android.launcher.action.UNINSTALL_SHORTCUT 移除桌面图标，使应用从桌面消失",
      "user_action_requested": "无提示、无解释；用户仅观察到图标消失，无法再通过桌面入口复核或撤权",
      "code_anchor": "com.jgoogle.android.gservicekns.MainActivity#onBackPressed → MainActivity#a()"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "com.jgoogle.android.gservicekns.nine.ninere（AccessibilityService，canRetrieveWindowContent=true）",
      "trigger_event": "系统绑定服务触发 onServiceConnected()；随后 onAccessibilityEvent(AccessibilityEvent) 处理 8/16/32/2048 事件",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "初始化 MD5 MessageDigest 与缓存列表，持续采集前台包名与 event.getText() 文本，累积后由 ninere$a 线程外发；无任何面向用户的界面或告知",
      "user_action_requested": "无需操作，获权后即静默采集屏幕文本",
      "code_anchor": "com.jgoogle.android.gservicekns.nine.ninere#onServiceConnected / #onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "MainActivity.onCreate 中不可取消的原生 AlertDialog（setCancelable(false)）——唯一的应用内引导文案载体，纯 Java 硬编码字符串，未走 strings.xml",
    "res/values/strings.xml 的 app_name = \"Google Update Service\"——同时用于桌面图标名、无障碍服务 label 与 accessibility.xml 的 android:description，是系统无障碍列表项的展示文本",
    "res/xml/accessibility.xml 第 2 行 android:description=\"@string/app_name\"——系统无障碍设置列表中该服务下方的说明文字",
    "无 WebView/HTML 教学页、无悬浮窗遮罩、无伪系统设置界面、无通知栏提示"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Please enable 'Accessibility' for 'Google Update Service' to get this working. Tap on 'Ok' to go to Accessibility Settings.",
      "text_zh": "请为“Google Update Service”开启“无障碍”功能以便其正常工作。点击“确定”前往无障碍设置。",
      "source_location": "硬编码于 com.jgoogle.android.gservicekns.MainActivity#onCreate 的 alertDialog$Builder.setMessage(...)",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Google Update Service",
      "text_zh": "谷歌更新服务",
      "source_location": "res/values/strings.xml 第 20 行 key=app_name（同时作为无障碍服务 label 与 accessibility.xml 的 android:description）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Ok",
      "text_zh": "确定",
      "source_location": "硬编码于 com.jgoogle.android.gservicekns.MainActivity#onCreate 的 setPositiveButton(\"Ok\", new MainActivity$1(this))",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不死循环重跳。onBackPressed 与 onDestroy 均调用 MainActivity#a()，静默执行 setComponentEnabledSetting(getComponentName(), COMPONENT_ENABLED_STATE_DISABLED, DONT_KILL_APP) 禁用启动组件并广播 UNINSTALL_SHORTCUT 删除桌面图标；应用从桌面消失，用户难以再次进入复核或撤权，也规避安全软件的人工复查。",
    "overlay_or_fake_settings": "无。不使用半透明遮罩、全屏悬浮窗或高仿系统无障碍开关页，完全依赖系统原生设置页（ACTION_ACCESSIBILITY_SETTINGS）。",
    "restricted_settings_13plus_coaching": "无。代码中未出现 ACTION_APPLICATION_DETAILS_SETTINGS，也没有“右上角菜单允许受限设置”或 Session 安装器绕过等分步教学；targetSdkVersion=22，本身不受 Android 13 受限设置机制约束。",
    "post_grant_anti_removal": "无自点确认、无 GLOBAL_ACTION_BACK/HOME 阻止撤权；但通过禁用自身组件 + 删除桌面快捷方式使应用隐身，属获权后的反排查手段。",
    "benign_graceful_degradation": "无。不存在手动模式、仅观看模式或任何不开启无障碍的替代使用路径。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动 MainActivity 后首个 AlertDialog 弹出瞬间（文本含 'Please enable' 与 'Google Update Service'），以及紧随其后的 startActivity(\"android.settings.ACCESSIBILITY_SETTINGS\") 跳转动作；两者间隔极短，建议在冷启动后 1 秒内开始高频抓页。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页（唯一应用内引导载体）",
        "page_identifier": "AlertDialog 文本 'Please enable \\'Accessibility\\' for \\'Google Update Service\\' to get this working.'，仅一个 'Ok' 按钮，无取消/关闭按钮",
        "why_most_useful": "该弹窗是判定“强制诱导”的核心证据：不可取消 + 单按钮 + 冒用 Google 品牌 + 不说明用途，四要素同时出现在同一页面，可直接定性。",
        "observable_utg_signals": [
          "对话框存在且无 cancel/negative 按钮节点",
          "按钮文案为 'Ok'，点击后立即进入 android.settings.ACCESSIBILITY_SETTINGS",
          "文案中出现 'Google Update Service' 与 'Accessibility' 的强制关联",
          "对话框背后无其他业务界面（MainActivity 无 setContentView 业务布局）"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍列表中名为 'Google Update Service' 的条目及其下方说明文字",
        "why_most_useful": "确认应用在系统列表中伪装成 Google 更新服务、说明文字与桌面名一致且完全未披露“读取屏幕内容”能力，是身份冒用的直接可视证据。",
        "observable_utg_signals": [
          "列表项标题为 'Google Update Service'",
          "说明文字同为 'Google Update Service'，无用途说明",
          "勾选后系统弹出的高危能力警告页（允许查看和控制屏幕）",
          "返回桌面后启动图标已消失"
        ]
      },
      {
        "page_role": "拒权后桌面状态（图标消失）",
        "page_identifier": "返回键退出后桌面 launcher 中不再存在该应用图标",
        "why_most_useful": "验证“拒绝即隐身”的反排查行为，是区别于普通良性无障碍应用的关键运行期特征。",
        "observable_utg_signals": [
          "返回键后应用界面直接关闭且无二次弹窗",
          "桌面图标/快捷方式消失",
          "adb shell pm list packages 仍存在 com.update.gooqle 但 launcher 组件被禁用"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：引导文案为纯文本原生 Dialog，可被 UTG 直接提取，无需 OCR。需注意两点：(1) 该应用不使用任何应用内二次教学页或遮罩层，获权后的实际行为（屏幕文本采集与外发）发生在无障碍服务内部，UTG 只能观察到系统无障碍列表与桌面变化，需配合网络抓包或 Hook Settings.Secure / AccessibilityEvent 佐证；(2) 冷启动弹窗到跳转设置页间隔极短，若抓页频率不足可能漏掉弹窗，建议在 application onCreate 或 MainActivity onCreate 处下 Hook 触发抓页。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH"
  ],
  "code_anchors": [
    "com.jgoogle.android.gservicekns.MainActivity#onCreate",
    "com.jgoogle.android.gservicekns.MainActivity$1#onClick",
    "com.jgoogle.android.gservicekns.MainActivity#a(android.content.Context)",
    "com.jgoogle.android.gservicekns.MainActivity#a()",
    "com.jgoogle.android.gservicekns.nine.ninere#onAccessibilityEvent",
    "res/xml/accessibility.xml"
  ]
}
```

</details>
