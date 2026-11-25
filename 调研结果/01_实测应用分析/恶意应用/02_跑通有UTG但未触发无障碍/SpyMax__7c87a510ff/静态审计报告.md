# MR_010__7c87a510ff｜SpyMax — AppName

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：192.9s

## 1. 一句话核心结论

- **核心申请方式**：应用无任何App内说明或教学，启动入口Activity即刻finish并在后台线程按配置位串裸跳系统无障碍设置页，系统列表中仅以"Service"之名、无描述呈现，同一开关串还并联静默设备管理器授权与su提权。
- **静态可见性说明**：无障碍跳转代码本体完整静态可见（无壳、无加密资源、无WebView），但触发由字符串资源 abcd06（本地值"10000"）的逐位开关决定，且 ysszamqyia19.pkfvgtngbzwgeqjureag00 接受运行期传入开关串、无静态调用者，说明该跳转可能由配置/云控在运行期开启；开关串是否被 saveRES 或远端写入无法静态闭环。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `7c87a510ff43866ba135c3ab6623b1fab5d6924d6238daafc68276eda8c55bf6` |
| 包名 / 年份 | `yps.eton.application` / 2020 |
| 家族 / 品类 | **SpyMax**（同池样本数：23） |
| 原始来源标识 | https://blog.lookout.com/commercial-surveillanceware-operators-latest-to-take-advantage-of-covid-19 |
| 桌面显示名 | AppName |
| 引导页宣称品牌/身份 | 仿冒 Facebook 登录界面（act_16.xml 使用 facebookk 图标与 Login/Register Here/Forgot password 文案；act_26.xml 为 golo 标志的 Sign in 页） |
| 系统无障碍列表服务名 | Service |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务 label 仅为泛化词 "Service" 且完全省略 android:description；设备管理器请求的 ADD_EXPLANATION 传入空串 BuildConfig.FLAVOR，系统授权弹窗不显示任何用途说明；关键字符串以 "spyandroid" 占位符 + String.replace("spyandroid","") 拆解拼装（如 spyandroidsu→su、spyandroidFacebspyandroidook→Facebook）；桌面名"AppName"、图标 ic_launcher 与仿Facebook页面身份互不一致；所有Activity均 excludeFromRecents，任务栏不可见。 |
| 无障碍服务类名 | `yps.eton.application.ysszamqyia1` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | yps.eton.application.ysszamqyia7（MAIN/LAUNCHER，excludeFromRecents=true） | onCreate(Bundle) | 原生Activity | **原文**：无（onCreate 首行即 finish()，无 setContentView）<br>**译注**：启动瞬间无任何界面，Activity 立即关闭 | 无，用户无任何选择或取消机会 | `yps.eton.application.ysszamqyia7.onCreate` |
| 2 | 业务功能触发 | 后台线程 ysszamqyia7$1.run（持 ReentrantLock 串行执行），由 eflobknlcjtaefcmmgjt()/izezqztvpopulbhmjqvg() 在 onCreate 与 onResume 中派发 | onCreate/onResume 调用配置分发函数后启动 Runnable | 不可静态还原（后台线程，无界面） | 无 | 无 | `yps.eton.application.ysszamqyia7.eflobknlcjtaefcmmgjt → ysszamqyia7$1.run` |
| 3 | 跳受限设置 | 系统「设备管理器」激活确认页（ACTION_ADD_DEVICE_ADMIN） | 开关串 abcd06.charAt(3)=='1' 时 startActivityForResult(intent, 100) | 系统无障碍页 | **原文**：putExtra("android.app.extra.ADD_EXPLANATION", BuildConfig.FLAVOR)  // 空串<br>**译注**：系统设备管理器授权页，但用途说明为空，用户看不到任何申请理由 | 系统页面上只有「激活/取消」，App 未提供任何解释或拒绝后的替代路径 | `yps.eton.application.ysszamqyia7$1.run` |
| 4 | 跳无障碍设置 | 系统「无障碍」设置页（android.settings.ACCESSIBILITY_SETTINGS） | 开关串 abcd06.charAt(1)=='1' 时构造 Intent(FLAG_ACTIVITY_NEW_TASK) 并 startActivity | 系统无障碍页 | **原文**：nggovzkfvjjmtqutoquz.setFlags(268435456); nggovzkfvjjmtqutoquz.setAction("android.settings.ACCESSIBILITY_SETTINGS"); startActivity(...)<br>**译注**：直接跳到系统无障碍服务列表，无任何跳转前说明页、弹窗或遮罩指引 | 要求用户在系统列表中自行找到并开启名为 "Service" 的服务；App 内无解释、无取消/跳过按钮 | `yps.eton.application.ysszamqyia7$1.run` |
| 5 | 跳无障碍设置 | 系统「无障碍」设置页（备用实现，入参为外部传入开关串） | pkfvgtngbzwgeqjureag00(cfgString, context, skip) 中 cfgString.charAt(1)=='1' 且 skip==false | 系统无障碍页 | **原文**：nggovzkfvjjmtqutoquz.setFlags(268435456); nggovzkfvjjmtqutoquz.setAction("android.settings.ACCESSIBILITY_SETTINGS"); getApplicationContex.startActivity(nggovzkfvjjmtqutoquz);<br>**译注**：以运行期传入的配置串决定是否再次裸跳无障碍设置页 | 同上，无任何说明与取消选项 | `yps.eton.application.ysszamqyia19.pkvfgtngbzwgeqjureag00` |
| 6 | 获权后动作 | yps.eton.application.ysszamqyia1（AccessibilityService）onServiceConnected | 用户在系统列表开启服务后系统回调 onServiceConnected | 不可静态还原（服务运行态，无界面） | **原文**：r0.flags = 89; r0.eventTypes = -1; r0.feedbackType = 16;<br>**译注**：注册为监听全部事件类型（eventTypes=-1）、flags=89 的无障碍服务，随后进入读取短信/通话/通讯录与远控通信逻辑 | 无需进一步操作，获权即静默接管 | `yps.eton.application.ysszamqyia1.onServiceConnected` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 无 App 内引导/说明文字：ysszamqyia7.onCreate 首行 finish()，全流程无 setContentView、无 AlertDialog、无 Toast
- 系统无障碍服务列表条目：label=@string/abcd03 → 原文 "Service"（res/values/strings.xml），无 android:description
- 系统设备管理器激活页：ADD_EXPLANATION 被显式置为空串，页面无任何用途说明文本
- 桌面图标名称：@string/app_name → "AppName"
- 仿冒品牌页（非无障碍链）：res/layout/act_16.xml（"Login"、" New user ? Register Here "、" Forgot password ? "、facebookk 图标）、res/layout/act_26.xml（"Sign in"、golo 标志）
- res/layout/sshat.xml：仿聊天界面 "Write a message"（远控消息通道，非无障碍引导）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Service | 服务 | `res/values/strings.xml → abcd03（无障碍服务与多个组件 label）` | 未知 |
| en | AppName | AppName（无实义的占位式应用名） | `res/values/strings.xml → app_name` | 未知 |
| en | Login | 登录 | `res/layout/act_16.xml、act_26.xml（Button @id/login, onClick=save）` | 假反诈安全 |
| en | New user ? Register Here | 新用户？在此注册 | `res/layout/act_16.xml、act_26.xml（TextView @id/signup）` | 未知 |
| en | Forgot password ? | 忘记密码？ | `res/layout/act_16.xml（TextView @id/forgotpassword）` | 未知 |
| en | Sign in | 登录 | `res/layout/act_26.xml（TextView）` | 未知 |
| en | Write a message | 输入消息 | `res/layout/sshat.xml（EditText @id/messageEditText）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：未发现死循环重跳或定时拉起逻辑：路径中无 getEnabledAccessibilityServiceList 校验、无 Timer/Handler 周期重跳、无 onResume 条件重跳（onResume 仅再次调用同一配置分发函数，仍受 abcd06 位串门控）。用户返回后不进入任何反馈或降级页面。
- **遮罩叠层 / 高仿系统设置页**：无。跳转前无遮罩、无全屏悬浮窗、无高仿无障碍开关页；仅裸跳系统真实设置页。应用虽申请 SYSTEM_ALERT_WINDOW 且 ysszamqyia5 通过 WindowManager.addView 具备悬浮窗能力，但该能力未接入无障碍引导链。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。targetSdkVersion=22（Android 5.0/6.0 时代样本），代码中不存在 ACTION_APPLICATION_DETAILS_SETTINGS、不存在「点右上角菜单允许受限设置」或 Session 安装器绕过的教学文本。
- **获权后即时行为与防撤权机制**：无。获权后 onServiceConnected 仅设置 flags=89、eventTypes=-1 全量监听并转入数据采集，未见 performGlobalAction(GLOBAL_ACTION_BACK/HOME)、未见监听设置页自点确认或阻止撤权。
- **良性降级 / 替代方案**：无。未提供手动模式、ADB 说明或仅观看模式等替代路径，也未向用户解释该权限用途。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到 startActivity 的目标 Action 为 android.settings.ACCESSIBILITY_SETTINGS（Intent flags=0x10000000、无任何 Extra）的瞬间拉起 UTG，尤其是冷启动 ysszamqyia7 后 1.5s（代码中 Thread.sleep(1500L)）内；同时可 hook ACTION_ADD_DEVICE_ADMIN 作为同组开关位的辅助观测点。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无纯图/OCR 盲区（本样本引导链无图片型诱导）。真实盲区有二：一是 abcd06 位串本地值为 "10000"，无障碍位（charAt(1)）默认关闭，若云控/配置未下发则运行期看不到跳转，UTG 可能空跑——需先确认开关串是否被改写；二是应用配置了 raw/google.apk 内置载荷与 DDNS 远控，无障碍链之后的行为依赖服务端指令，UTG 只能覆盖授权瞬间与首屏，不能覆盖指令驱动的后续动作。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转前状态（无引导页，验证「零说明裸跳」）** | 冷启动后 0~1.5s 内屏幕仍为桌面/上一应用，包名 yps.eton.application 无任何 Activity 界面（launcher Activity 已 finish） | 证明应用未提供任何知情说明，直接以系统页替代解释，是区分「诱导/静默」与「良性透明说明」的决定性画面 | 屏幕无本应用任何窗口；通知栏/任务列表无本应用任务（excludeFromRecents）；1.5s 后系统无障碍页突然压栈 |
| **系统无障碍服务列表项（身份伪装核心）** | 设置→无障碍 列表中出现名为 "Service" 的条目，无副标题/描述文本 | 直接暴露 label 泛化、无 description 的身份混淆手法，是判定 ID 伪装与告知缺失的关键页面 | 条目文本仅为 Service；无描述行（无 android:description）；同页存在系统标准服务作为对照 |
| **系统设备管理器激活页（同开关串并联的受限设置）** | 系统「激活设备管理器？」页，说明区域为空 | 验证 ADD_EXPLANATION 空串导致系统警告失去用途说明，佐证同一配置位串驱动的连环授权 | 说明文本为空/缺失；激活按钮可用；包名 yps.eton.application 可见 |
| **获权后状态（服务接管确认）** | 无障碍列表中 "Service" 变为已开启状态；应用无新界面出现 | 确认获权后应用不展示任何正常业务界面而是转入后台采集，支撑「表面功能与实际执行不一致」 | 服务开关为开启态；前台无本应用 Activity；后台出现常驻服务/网络连接 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `yps.eton.application.ysszamqyia7$1.run`
- `yps.eton.application.ysszamqyia19.pkvfgtngbzwgeqjureag00`
- `yps.eton.application.ysszamqyia7.onCreate`
- `yps.eton.application.ysszamqyia1.onServiceConnected`
- `res/values/strings.xml#abcd03`
- `res/layout/act_16.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，静态为主）

**可见性判断：** 无障碍授权引导路径本身**静态可见**（无壳、无密文、无 WebView），但其**触发由本地配置串 `abcd06` 门控**，且包内另有一处接受运行期配置串的同类跳转实现（无静态调用者），因此运行期是否真正弹出需结合云控/配置写入判断。

**关键事实链**

1. **启动入口极简、无引导 UI**：桌面入口 [ysszamqyia7](<resource-unit:#1.dex1 code:yps.eton.application.ysszamqyia7>)（`MAIN/LAUNCHER`，`excludeFromRecents=true`，label=`@string/app_name`="AppName"）在 `onCreate()` 里立即 `finish()`，随后起后台线程；`onResume()` 也再次调用同一配置分发函数。全程**没有任何说明页、弹窗、HTML 或悬浮遮罩**。
2. **跳转点**：[ysszamqyia7$1.run](<resource-unit:#1.dex1 code:yps.eton.application.ysszamqyia7$1#run>) 读取 `R.string.abcd06` 作为开关位串，`charAt(1)=='1'` 时构造 `Intent`，`setFlags(0x10000000)`、`setAction("android.settings.ACCESSIBILITY_SETTINGS")`，直接 `startActivity` 拉起**系统无障碍设置页**——没有任何 App 内解释，用户一进去看到的是系统列表里的 `Service` 条目。
3. **同一开关串还串联了另外两条高危引导**：`charAt(3)=='1'` 时用 `ACTION_ADD_DEVICE_ADMIN` 请求设备管理器，且 `ADD_EXPLANATION` 被赋为 `BuildConfig.FLAVOR`（空串，系统对话框不显示任何用途说明）；`charAt(4)=='1'` 时 `Runtime.exec("spyandroidsu".replace("spyandroid",""))` 即 `su`（字符串拆解混淆）。本地 `abcd06="10000"`，即仅 `charAt(0)` 分支在本包内默认开启，无障碍/设备管理器/root 三路在本地配置下为关闭态——**是否开启由配置串决定**。
4. **第二处同类实现**：[ysszamqyia19.pkfvgtngbzwgeqjureag00](<resource-unit:#1.dex1 code:yps.eton.application.ysszamqyia19#pkfvgtngbzwgeqjureag00>) 接收外部传入的开关串与 `Context`，`charAt(1)=='1'` 时同样裸跳 `ACCESSIBILITY_SETTINGS`；该函数无静态调用者，提示开关串可由运行期/远端提供。
5. **身份伪装与说明缺失**：无障碍服务 [ysszamqyia1](<resource-unit:#1.dex1 code:yps.eton.application.ysszamqyia1>)（`BIND_ACCESSIBILITY_SERVICE`）在 Manifest 中 label=`@string/abcd03`，其值仅为 **"Service"**，且**无 `android:description`**——系统无障碍列表里只会显示一个名为 "Service" 的条目，不交代用途。桌面名为 "AppName"，`act_16.xml`/`act_26.xml` 则是**仿 Facebook 登录页**（`facebookk`、`golo` 图、"Login"/"Sign in"/"New user ? Register here"/"Forgot password ?"，`saveLog()` 将输入拼成 `user:/pass:` 写盘），品牌冒用明显。
6. **无拒权反馈循环代码**：路径内未见 `getEnabledAccessibilityServiceList`、`performGlobalAction`、`GLOBAL_ACTION_BACK/HOME`、`onResume` 定时重跳等撤权对抗或死循环实现（`ysszamqyia5` 有 `WindowManager.addView` 悬浮窗能力，但未接入无障碍引导链）。`ACTION_APPLICATION_DETAILS_SETTINGS` 与 13+ 受限设置教学在代码中**不存在**（`targetSdkVersion=22`，属 Android 5/6 时代样本）。
7. **其他并存能力（非本次命题）**：`raw/google.apk` 内置 APK、`assdsiwi.ddns.net:1515` C2、短信/通话/通讯录/录音全量权限与 `MediaProjection` 初始化，指向远控木马主体。

**未决与边界**：`abcd06` 开关串是否存在运行期改写/云控下发（`saveRES` 写文件机制、`ysszamqyia19` 的外部入参）未能完全闭环，因此无障碍引导的实际触发时机与频率需动态验证。

**UTG 建议**：最佳观测点是监听 `startActivity` 目标为 `android.settings.ACCESSIBILITY_SETTINGS`（`flags=0x10000000`，无 `EXTRA`）的瞬间，以及随后系统无障碍列表中 label 为 "Service" 的条目。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "无障碍跳转代码本体完整静态可见（无壳、无加密资源、无WebView），但触发由字符串资源 abcd06（本地值\"10000\"）的逐位开关决定，且 ysszamqyia19.pkfvgtngbzwgeqjureag00 接受运行期传入开关串、无静态调用者，说明该跳转可能由配置/云控在运行期开启；开关串是否被 saveRES 或远端写入无法静态闭环。",
  "summary_one_liner": "应用无任何App内说明或教学，启动入口Activity即刻finish并在后台线程按配置位串裸跳系统无障碍设置页，系统列表中仅以\"Service\"之名、无描述呈现，同一开关串还并联静默设备管理器授权与su提权。",
  "disguise_identity": {
    "app_display_name": "AppName",
    "claimed_brand_or_persona": "仿冒 Facebook 登录界面（act_16.xml 使用 facebookk 图标与 Login/Register Here/Forgot password 文案；act_26.xml 为 golo 标志的 Sign in 页）",
    "a11y_service_label": "Service",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务 label 仅为泛化词 \"Service\" 且完全省略 android:description；设备管理器请求的 ADD_EXPLANATION 传入空串 BuildConfig.FLAVOR，系统授权弹窗不显示任何用途说明；关键字符串以 \"spyandroid\" 占位符 + String.replace(\"spyandroid\",\"\") 拆解拼装（如 spyandroidsu→su、spyandroidFacebspyandroidook→Facebook）；桌面名\"AppName\"、图标 ic_launcher 与仿Facebook页面身份互不一致；所有Activity均 excludeFromRecents，任务栏不可见。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "yps.eton.application.ysszamqyia7（MAIN/LAUNCHER，excludeFromRecents=true）",
      "trigger_event": "onCreate(Bundle)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（onCreate 首行即 finish()，无 setContentView）",
      "shown_text_zh": "启动瞬间无任何界面，Activity 立即关闭",
      "user_action_requested": "无，用户无任何选择或取消机会",
      "code_anchor": "yps.eton.application.ysszamqyia7.onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "后台线程 ysszamqyia7$1.run（持 ReentrantLock 串行执行），由 eflobknlcjtaefcmmgjt()/izezqztvpopulbhmjqvg() 在 onCreate 与 onResume 中派发",
      "trigger_event": "onCreate/onResume 调用配置分发函数后启动 Runnable",
      "ui_carrier": "不可静态还原（后台线程，无界面）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "后台静默执行，无任何提示",
      "user_action_requested": "无",
      "code_anchor": "yps.eton.application.ysszamqyia7.eflobknlcjtaefcmmgjt → ysszamqyia7$1.run"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "系统「设备管理器」激活确认页（ACTION_ADD_DEVICE_ADMIN）",
      "trigger_event": "开关串 abcd06.charAt(3)=='1' 时 startActivityForResult(intent, 100)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "putExtra(\"android.app.extra.ADD_EXPLANATION\", BuildConfig.FLAVOR)  // 空串",
      "shown_text_zh": "系统设备管理器授权页，但用途说明为空，用户看不到任何申请理由",
      "user_action_requested": "系统页面上只有「激活/取消」，App 未提供任何解释或拒绝后的替代路径",
      "code_anchor": "yps.eton.application.ysszamqyia7$1.run"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统「无障碍」设置页（android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "开关串 abcd06.charAt(1)=='1' 时构造 Intent(FLAG_ACTIVITY_NEW_TASK) 并 startActivity",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "nggovzkfvjjmtqutoquz.setFlags(268435456); nggovzkfvjjmtqutoquz.setAction(\"android.settings.ACCESSIBILITY_SETTINGS\"); startActivity(...)",
      "shown_text_zh": "直接跳到系统无障碍服务列表，无任何跳转前说明页、弹窗或遮罩指引",
      "user_action_requested": "要求用户在系统列表中自行找到并开启名为 \"Service\" 的服务；App 内无解释、无取消/跳过按钮",
      "code_anchor": "yps.eton.application.ysszamqyia7$1.run"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统「无障碍」设置页（备用实现，入参为外部传入开关串）",
      "trigger_event": "pkfvgtngbzwgeqjureag00(cfgString, context, skip) 中 cfgString.charAt(1)=='1' 且 skip==false",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "nggovzkfvjjmtqutoquz.setFlags(268435456); nggovzkfvjjmtqutoquz.setAction(\"android.settings.ACCESSIBILITY_SETTINGS\"); getApplicationContex.startActivity(nggovzkfvjjmtqutoquz);",
      "shown_text_zh": "以运行期传入的配置串决定是否再次裸跳无障碍设置页",
      "user_action_requested": "同上，无任何说明与取消选项",
      "code_anchor": "yps.eton.application.ysszamqyia19.pkvfgtngbzwgeqjureag00"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "yps.eton.application.ysszamqyia1（AccessibilityService）onServiceConnected",
      "trigger_event": "用户在系统列表开启服务后系统回调 onServiceConnected",
      "ui_carrier": "不可静态还原（服务运行态，无界面）",
      "shown_text_verbatim": "r0.flags = 89; r0.eventTypes = -1; r0.feedbackType = 16;",
      "shown_text_zh": "注册为监听全部事件类型（eventTypes=-1）、flags=89 的无障碍服务，随后进入读取短信/通话/通讯录与远控通信逻辑",
      "user_action_requested": "无需进一步操作，获权即静默接管",
      "code_anchor": "yps.eton.application.ysszamqyia1.onServiceConnected"
    }
  ],
  "text_presentation_locations": [
    "无 App 内引导/说明文字：ysszamqyia7.onCreate 首行 finish()，全流程无 setContentView、无 AlertDialog、无 Toast",
    "系统无障碍服务列表条目：label=@string/abcd03 → 原文 \"Service\"（res/values/strings.xml），无 android:description",
    "系统设备管理器激活页：ADD_EXPLANATION 被显式置为空串，页面无任何用途说明文本",
    "桌面图标名称：@string/app_name → \"AppName\"",
    "仿冒品牌页（非无障碍链）：res/layout/act_16.xml（\"Login\"、\" New user ? Register Here \"、\" Forgot password ? \"、facebookk 图标）、res/layout/act_26.xml（\"Sign in\"、golo 标志）",
    "res/layout/sshat.xml：仿聊天界面 \"Write a message\"（远控消息通道，非无障碍引导）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Service",
      "text_zh": "服务",
      "source_location": "res/values/strings.xml → abcd03（无障碍服务与多个组件 label）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "AppName",
      "text_zh": "AppName（无实义的占位式应用名）",
      "source_location": "res/values/strings.xml → app_name",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Login",
      "text_zh": "登录",
      "source_location": "res/layout/act_16.xml、act_26.xml（Button @id/login, onClick=save）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": " New user ? Register Here ",
      "text_zh": "新用户？在此注册",
      "source_location": "res/layout/act_16.xml、act_26.xml（TextView @id/signup）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": " Forgot password ? ",
      "text_zh": "忘记密码？",
      "source_location": "res/layout/act_16.xml（TextView @id/forgotpassword）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Sign in",
      "text_zh": "登录",
      "source_location": "res/layout/act_26.xml（TextView）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Write a message",
      "text_zh": "输入消息",
      "source_location": "res/layout/sshat.xml（EditText @id/messageEditText）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "未发现死循环重跳或定时拉起逻辑：路径中无 getEnabledAccessibilityServiceList 校验、无 Timer/Handler 周期重跳、无 onResume 条件重跳（onResume 仅再次调用同一配置分发函数，仍受 abcd06 位串门控）。用户返回后不进入任何反馈或降级页面。",
    "overlay_or_fake_settings": "无。跳转前无遮罩、无全屏悬浮窗、无高仿无障碍开关页；仅裸跳系统真实设置页。应用虽申请 SYSTEM_ALERT_WINDOW 且 ysszamqyia5 通过 WindowManager.addView 具备悬浮窗能力，但该能力未接入无障碍引导链。",
    "restricted_settings_13plus_coaching": "无。targetSdkVersion=22（Android 5.0/6.0 时代样本），代码中不存在 ACTION_APPLICATION_DETAILS_SETTINGS、不存在「点右上角菜单允许受限设置」或 Session 安装器绕过的教学文本。",
    "post_grant_anti_removal": "无。获权后 onServiceConnected 仅设置 flags=89、eventTypes=-1 全量监听并转入数据采集，未见 performGlobalAction(GLOBAL_ACTION_BACK/HOME)、未见监听设置页自点确认或阻止撤权。",
    "benign_graceful_degradation": "无。未提供手动模式、ADB 说明或仅观看模式等替代路径，也未向用户解释该权限用途。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到 startActivity 的目标 Action 为 android.settings.ACCESSIBILITY_SETTINGS（Intent flags=0x10000000、无任何 Extra）的瞬间拉起 UTG，尤其是冷启动 ysszamqyia7 后 1.5s（代码中 Thread.sleep(1500L)）内；同时可 hook ACTION_ADD_DEVICE_ADMIN 作为同组开关位的辅助观测点。",
    "key_pages_to_capture": [
      {
        "page_role": "跳转前状态（无引导页，验证「零说明裸跳」）",
        "page_identifier": "冷启动后 0~1.5s 内屏幕仍为桌面/上一应用，包名 yps.eton.application 无任何 Activity 界面（launcher Activity 已 finish）",
        "why_most_useful": "证明应用未提供任何知情说明，直接以系统页替代解释，是区分「诱导/静默」与「良性透明说明」的决定性画面",
        "observable_utg_signals": ["屏幕无本应用任何窗口", "通知栏/任务列表无本应用任务（excludeFromRecents）", "1.5s 后系统无障碍页突然压栈"]
      },
      {
        "page_role": "系统无障碍服务列表项（身份伪装核心）",
        "page_identifier": "设置→无障碍 列表中出现名为 \"Service\" 的条目，无副标题/描述文本",
        "why_most_useful": "直接暴露 label 泛化、无 description 的身份混淆手法，是判定 ID 伪装与告知缺失的关键页面",
        "observable_utg_signals": ["条目文本仅为 Service", "无描述行（无 android:description）", "同页存在系统标准服务作为对照"]
      },
      {
        "page_role": "系统设备管理器激活页（同开关串并联的受限设置）",
        "page_identifier": "系统「激活设备管理器？」页，说明区域为空",
        "why_most_useful": "验证 ADD_EXPLANATION 空串导致系统警告失去用途说明，佐证同一配置位串驱动的连环授权",
        "observable_utg_signals": ["说明文本为空/缺失", "激活按钮可用", "包名 yps.eton.application 可见"]
      },
      {
        "page_role": "获权后状态（服务接管确认）",
        "page_identifier": "无障碍列表中 \"Service\" 变为已开启状态；应用无新界面出现",
        "why_most_useful": "确认获权后应用不展示任何正常业务界面而是转入后台采集，支撑「表面功能与实际执行不一致」",
        "observable_utg_signals": ["服务开关为开启态", "前台无本应用 Activity", "后台出现常驻服务/网络连接"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无纯图/OCR 盲区（本样本引导链无图片型诱导）。真实盲区有二：一是 abcd06 位串本地值为 \"10000\"，无障碍位（charAt(1)）默认关闭，若云控/配置未下发则运行期看不到跳转，UTG 可能空跑——需先确认开关串是否被改写；二是应用配置了 raw/google.apk 内置载荷与 DDNS 远控，无障碍链之后的行为依赖服务端指令，UTG 只能覆盖授权瞬间与首屏，不能覆盖指令驱动的后续动作。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "LURE_DISMISS_SYSTEM_WARNING",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "yps.eton.application.ysszamqyia7$1.run",
    "yps.eton.application.ysszamqyia19.pkvfgtngbzwgeqjureag00",
    "yps.eton.application.ysszamqyia7.onCreate",
    "yps.eton.application.ysszamqyia1.onServiceConnected",
    "res/values/strings.xml#abcd03",
    "res/layout/act_16.xml"
  ]
}
```

</details>
