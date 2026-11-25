# MR_075__3bf85d0aff｜CallerSpy — rat

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：99.0s

## 1. 一句话核心结论

- **核心申请方式**：该应用对无障碍权限零引导、零检测、零设置跳转，靠空白启动页闪退后台保活，静默潜伏等待用户自行在系统设置中开启一个无任何说明文本的裸名无障碍服务。
- **静态可见性说明**：无障碍权限申请路径完全静态可见：全包无加壳（初判 False，DEX 可完整反编译），无 assets、无 WebView、无加密载荷、无动态加载入口；结论为『不存在引导流程』，该否定性结论由代码与资源双向检索确认，非因不可见而缺失。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `3bf85d0aff5ddc0c57e43b879631ee692d98d01f5c964336471f1cdfe0d291f8` |
| 包名 / 年份 | `com.example.rat` / 2019 |
| 家族 / 品类 | **CallerSpy**（同池样本数：4） |
| 原始来源标识 | https://www.trendmicro.com/en_us/research/19/l/mobile-cyberespionage-campaign-distributed-through-callerspy-mounts-initial-phase-of-a-targeted-attack.html |
| 桌面显示名 | rat |
| 引导页宣称品牌/身份 | 无任何品牌或身份宣称（界面为空，无引导文案）；仅在后台以通知文案 "Chat is running" 伪装为聊天类应用以维持前台服务存活 |
| 系统无障碍列表服务名 | rat（logger.xml 未设 android:label/summary/description，系统无障碍列表仅显示应用名 rat） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍配置沿用他人样本痕迹：logger.xml 中 packageNames 硬编码为 com.example.andres.eventcapture，运行期 onServiceConnected 又覆写为 com.camacc，均与本包 com.example.rat 不符；android:settingsActivity 留空、无 android:description 与 android:summary，使系统无障碍列表条目无任何解释文本；三个 Activity 均 android:excludeFromRecents="true" 且使用 Theme.Transparent 空白壳；前台通知标题正文均为 "Chat is running" 伪装聊天应用 |
| 无障碍服务类名 | `com.example.rat.service.logger` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：com.example.andres.eventcapture |
| 共现高危权限 | `CALL_PHONE, CAMERA, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECORD_AUDIO` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.example.rat.MainActivity（launcher Activity） | 用户点击桌面图标，onCreate 执行 | 原生Activity | **原文**：无（res/layout/activity_main.xml 仅含一个 android:text="" 的 TextView）<br>**译注**：纯空白页面，无任何文字、图标或按钮 | 无任何操作请求；页面不等待输入，onCreate 末尾直接调用 finish() | `com.example.rat.MainActivity.onCreate / res/layout/activity_main.xml` |
| 2 | 冷启动入口 | Evernote JobManager 任务队列（alive_listener、alive_enviorment_scehdular、sync_data_locally、alive_latest_files_watcher、remote_sync） | MainActivity.onCreate 中连续 5 次 JobRequest.Builder.schedule()，随后 finish() | 不可静态还原 | 无 | 无 | `com.example.rat.MainActivity.onCreate` |
| 3 | 获权后动作 | com.example.rat.service.forground_service（进程 :MyService，前台服务） | onCreate → startForeground(1, ...)，onStartCommand 连接 Socket.IO 并注册 update_status 监听 | 通知栏 | **原文**：Chat is running<br>**译注**：聊天正在运行 | 无；通知 setOngoing(true) 常驻不可滑动清除，用户无法直接关闭 | `com.example.rat.service.forground_service.onCreate` |
| 4 | 引导说明页 | 不存在——全包无引导 Activity / Dialog / WebView / 悬浮窗 | 无触发点：未检索到 ACTION_ACCESSIBILITY_SETTINGS、ACTION_APPLICATION_DETAILS_SETTINGS、android.settings.*、AccessibilityManager 的任何引用 | 不可静态还原 | 无 | 无；应用既不提示也不检测授权状态，权限获取完全依赖用户自行进入系统设置 | `com.example.rat.MainActivity.onCreate（全包检索无命中）` |
| 5 | 跳无障碍设置 | 系统设置 → 无障碍 → 已下载的服务 → rat（com.example.rat.service.logger） | 由用户自行手动进入，非应用触发 | 系统无障碍页 | **原文**：无（res/xml/logger.xml 中 android:settingsActivity=""，未声明 android:description、android:summary）<br>**译注**：系统无障碍列表中仅显示服务名 rat，无任何功能说明，用户无法从界面得知该服务会读取全部窗口内容并拦截按键 | 用户在无告知前提下自行决定开启；应用侧无取消/跳过概念（因为根本没有请求） | `res/xml/logger.xml` |
| 6 | 获权后动作 | com.example.rat.service.logger（AccessibilityService） | 系统回调 onServiceConnected() | 不可静态还原 | **原文**：无（仅 Log.v("Hello", "on Service Connected")）<br>**译注**：无界面反馈；静默将事件类型覆写为 -1（全类型）、notificationTimeout=100ms、packageNames=com.camacc | 无；onKeyEvent 记录音量键后 return true 吞掉按键事件，不向用户回显任何提示 | `com.example.rat.service.logger.onServiceConnected / com.example.rat.service.logger.onKeyEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- res/layout/activity_main.xml：唯一的启动页布局，TextView 的 android:text 为空字符串，无任何引导文字
- res/values/strings.xml：仅有 app_name=rat 与 AppCompat 内置字符串（abc_*、search_menu_title 等），无一条引导/说明/权限申请文案
- res/xml/logger.xml：无障碍服务配置，android:settingsActivity 为空、无 android:description、无 android:summary —— 系统无障碍列表条目呈现为无说明的裸名 rat
- com.example.rat.service.forground_service.onCreate：通知栏常驻文案 "Chat is running"（伪装聊天应用，与无障碍无关）
- res/layout/custom_dialog.xml：仅含一个 text=" Ok " 的 Button，且未被任何业务类实例化使用，无说明性内容
- assets/ 目录：不存在（空），无任何本地 HTML 引导页
- 结论：全包不存在任何面向用户的无障碍授权说明文字，也不存在弹窗、WebView、悬浮遮罩等承载位置

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Chat is running | 聊天正在运行 | `硬编码于 com.example.rat.service.forground_service.onCreate（NotificationCompat.Builder.setContentTitle/setContentText）` | 清理工具伪装 |
| en | rat | rat（老鼠，同时是远程访问木马 RAT 的缩写） | `res/values/strings.xml 的 app_name，同时作为无障碍服务在系统列表中的显示名` | 未知 |
| en | Ok | 确定 | `res/layout/custom_dialog.xml 的 Button android:text（未被业务代码引用）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：无任何循环机制：应用既不跳转设置页，也不检测授权状态，不存在 onResume 重跳、Timer 拉起或拒绝后的反馈；用户即使永久不授权，应用行为亦无变化，仅在后台持续保活并等待服务被系统启用
- **遮罩叠层 / 高仿系统设置页**：无；未检索到 WindowManager.addView 业务调用、SYSTEM_ALERT_WINDOW 权限、TYPE_APPLICATION_OVERLAY/TYPE_SYSTEM_ALERT 常量，也无高仿系统无障碍开关页
- **Android 13+ 受限设置（Restricted Settings）应对**：无；targetSdkVersion=22（远低于 Android 13），不涉及受限设置教学，也无 Session 安装器绕过代码
- **获权后即时行为与防撤权机制**：无自点确认或 GLOBAL_ACTION_BACK/HOME 撤权阻断逻辑（onAccessibilityEvent 为空实现，onInterrupt 为空实现）；保活改由 Evernote JobManager 周期任务 + 前台服务 "Chat is running" 通知承担
- **良性降级 / 替代方案**：无；应用不提供任何替代路径或降级说明，授权与否均静默运行后台采集任务

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：本应用不会拉起 ACCESSIBILITY_SETTINGS 或 APP_DETAILS，无法用设置跳转作钩子。应以『启动 com.example.rat 后 1.5 秒内界面即刻消失 + 出现 com.example.rat.service.forground_service 前台通知』为触发点，随后手动进入 系统设置→无障碍→已下载的服务 抓取 rat 条目页；若需覆盖授权后行为，则在开启服务后回到主屏并按键，观察音量键被吞与无反馈现象。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无纯图空文本诱导，也无加壳/密文载荷阻碍运行期 UTG。唯一盲区是『零引导』本身：由于应用不跳设置、不弹窗、不检测授权，纯 UTG 在冷启动阶段几乎无可捕获的引导画面，需结合静态证据（无 ACTION_ACCESSIBILITY_SETTINGS 引用、logger.xml 无 description）才能闭环判定为静默潜伏而非引导缺失的良性应用。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动空白壳页（关键反证：证明无引导界面）** | com.example.rat.MainActivity，Theme 使用 AppTheme，布局仅一个空 TextView；excludeFromRecents=true，UTG 上表现为无文本、无按钮的空白窗口并在毫秒级消失 | 若该页存在任何权限说明文字，则属引导式申请；实测为空白且立即 finish，可直接判定应用不向用户做任何告知，这是区分『隐蔽引导』与『零引导静默潜伏』的决定性画面 | Activity 名 com.example.rat.MainActivity 且文本节点数为 0；页面停留时间极短（onCreate 末尾 finish()）；无任何 Dialog/WebView 子节点 |
| **系统无障碍服务列表项（关键：证明无说明文本）** | 系统设置 com.android.settings 无障碍页中名为 rat 的条目，无 summary 副标题 | 该条目是用户唯一能看到无障碍服务存在的地方；android:description/summary 均为空，故条目无解释文字，可证明应用未履行告知义务，用户是在完全不知情下开启全窗口内容读取权限 | 条目文本仅 "rat"，无副标题/说明行；不存在 settingsActivity 跳转入口（无设置齿轮）；开关状态可被外部开启，应用侧无任何提示 |
| **伪装常驻通知（证明社会工程伪装手法）** | 通知栏来自 com.example.rat、渠道由 createNotificationChannel 创建，标题与正文均为 Chat is running，setOngoing(true) | 该通知是应用唯一的对外可见文本，伪装为聊天应用以降低用户对后台常驻进程的怀疑，是判断其规避用户注意的补充信号 | 通知标题/正文 verbatim "Chat is running"；ongoing=true 不可滑动清除；通知来源包名 com.example.rat 与文案语义不一致 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.example.rat.MainActivity.onCreate`
- `com.example.rat.service.logger.onServiceConnected`
- `com.example.rat.service.logger.onKeyEvent`
- `com.example.rat.service.forground_service.onCreate`
- `res/xml/logger.xml`
- `res/layout/activity_main.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

已完成定向核验（共 11 次工具调用）。以下为结论。

## 结论要点

**核心发现：该应用根本不存在任何无障碍权限申请/引导流程——不是"隐蔽引导"，而是"零引导"。**

- **冷启动即退场**：[MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.example.rat.MainActivity#onCreate>) 仅 `setContentView(R.layout.activity_main)` → 排布 5 个 Job → 立刻 `finish()`；[activity_main.xml](<resource-unit:#1 file:res/layout/activity_main.xml>) 只有一个 `android:text=""` 的空 TextView，界面为空白。
- **无任何设置跳转**：全包（代码 + 资源 + smali）对 `ACTION_ACCESSIBILITY_SETTINGS`、`ACTION_APPLICATION_DETAILS_SETTINGS`、`android.settings.*`、`com.android.settings` 的检索**全部 0 命中**；`AccessibilityManager`、`getEnabledAccessibilityServiceList`、`isAccessibilityServiceEnabled` 也均无调用——应用连"是否已授权"都不检测。
- **无引导载体**：无 `WebView`（唯一命中是 `LinkifyCompat` 的 `WebView.findAddress`）、无 `WindowManager.addView` 悬浮窗（命中均为 AppCompat 内部）、无 `Toast`、无 `AlertDialog` 实例化；`assets/` 目录为空，无 HTML；`strings.xml` 仅含 `app_name=rat` 与 AppCompat 内置文案，无一句引导说明。
- **无障碍服务自身完全静默**：[logger.xml](<resource-unit:#1 file:res/xml/logger.xml>) 的 `android:settingsActivity=""`、无 `android:description`、无 `android:summary`，系统无障碍列表里只显示 "rat" 一个裸名，无解释文本。
- **服务参数与包名不一致（复制痕迹）**：`logger.xml` 声明 `packageNames="com.example.andres.eventcapture"`，而 [onServiceConnected()](<resource-unit:#1.dex1 code:com.example.rat.service.logger#onServiceConnected>) 运行期又覆写为 `com.camacc` + `eventTypes = -1`（全类型）；`onKeyEvent` 对音量键记录后 `return true` 吞键。说明该无障碍组件直接沿用他人样本配置，未针对本包适配。
- **唯一"主动告知"是伪装的常驻通知**：[forground_service.onCreate()](<resource-unit:#1.dex1 code:com.example.rat.service.forground_service#onCreate>) 以标题/正文 `"Chat is running"` 建立前台通知，用于保活，与无障碍授权无关，且刻意伪装为聊天类应用。
- **UTG 视角**：由于跳转 `ACCESSIBILITY_SETTINGS` 的瞬间不存在，纯 UTG 只能捕获"系统无障碍列表中的 rat 项"与"空白 Activity 一闪而过"两个画面；判定该应用诱导的关键不在引导页，而在**无障碍项无说明 + 空白壳页 + 伪装通知**三者共现。

与既有 [R-001](<resource-unit:#1 manifest:components>) 结论一致（无障碍服务静默潜伏、无引导），本次为该条风险补充了"零设置跳转、零检测、零引导载体"的反向证据，不另立重复风险命题。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍权限申请路径完全静态可见：全包无加壳（初判 False，DEX 可完整反编译），无 assets、无 WebView、无加密载荷、无动态加载入口；结论为『不存在引导流程』，该否定性结论由代码与资源双向检索确认，非因不可见而缺失。",
  "summary_one_liner": "该应用对无障碍权限零引导、零检测、零设置跳转，靠空白启动页闪退后台保活，静默潜伏等待用户自行在系统设置中开启一个无任何说明文本的裸名无障碍服务。",
  "disguise_identity": {
    "app_display_name": "rat",
    "claimed_brand_or_persona": "无任何品牌或身份宣称（界面为空，无引导文案）；仅在后台以通知文案 \"Chat is running\" 伪装为聊天类应用以维持前台服务存活",
    "a11y_service_label": "rat（logger.xml 未设 android:label/summary/description，系统无障碍列表仅显示应用名 rat）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍配置沿用他人样本痕迹：logger.xml 中 packageNames 硬编码为 com.example.andres.eventcapture，运行期 onServiceConnected 又覆写为 com.camacc，均与本包 com.example.rat 不符；android:settingsActivity 留空、无 android:description 与 android:summary，使系统无障碍列表条目无任何解释文本；三个 Activity 均 android:excludeFromRecents=\"true\" 且使用 Theme.Transparent 空白壳；前台通知标题正文均为 \"Chat is running\" 伪装聊天应用"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.example.rat.MainActivity（launcher Activity）",
      "trigger_event": "用户点击桌面图标，onCreate 执行",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（res/layout/activity_main.xml 仅含一个 android:text=\"\" 的 TextView）",
      "shown_text_zh": "纯空白页面，无任何文字、图标或按钮",
      "user_action_requested": "无任何操作请求；页面不等待输入，onCreate 末尾直接调用 finish()",
      "code_anchor": "com.example.rat.MainActivity.onCreate / res/layout/activity_main.xml"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "Evernote JobManager 任务队列（alive_listener、alive_enviorment_scehdular、sync_data_locally、alive_latest_files_watcher、remote_sync）",
      "trigger_event": "MainActivity.onCreate 中连续 5 次 JobRequest.Builder.schedule()，随后 finish()",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面；启动页一闪而过，任务转入后台作业调度",
      "user_action_requested": "无",
      "code_anchor": "com.example.rat.MainActivity.onCreate"
    },
    {
      "step": 3,
      "stage": "获权后动作",
      "screen_or_component": "com.example.rat.service.forground_service（进程 :MyService，前台服务）",
      "trigger_event": "onCreate → startForeground(1, ...)，onStartCommand 连接 Socket.IO 并注册 update_status 监听",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "Chat is running",
      "shown_text_zh": "聊天正在运行",
      "user_action_requested": "无；通知 setOngoing(true) 常驻不可滑动清除，用户无法直接关闭",
      "code_anchor": "com.example.rat.service.forground_service.onCreate"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "不存在——全包无引导 Activity / Dialog / WebView / 悬浮窗",
      "trigger_event": "无触发点：未检索到 ACTION_ACCESSIBILITY_SETTINGS、ACTION_APPLICATION_DETAILS_SETTINGS、android.settings.*、AccessibilityManager 的任何引用",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "应用从不向用户说明需要无障碍权限，也不引导用户前往设置页",
      "user_action_requested": "无；应用既不提示也不检测授权状态，权限获取完全依赖用户自行进入系统设置",
      "code_anchor": "com.example.rat.MainActivity.onCreate（全包检索无命中）"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已下载的服务 → rat（com.example.rat.service.logger）",
      "trigger_event": "由用户自行手动进入，非应用触发",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（res/xml/logger.xml 中 android:settingsActivity=\"\"，未声明 android:description、android:summary）",
      "shown_text_zh": "系统无障碍列表中仅显示服务名 rat，无任何功能说明，用户无法从界面得知该服务会读取全部窗口内容并拦截按键",
      "user_action_requested": "用户在无告知前提下自行决定开启；应用侧无取消/跳过概念（因为根本没有请求）",
      "code_anchor": "res/xml/logger.xml"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.example.rat.service.logger（AccessibilityService）",
      "trigger_event": "系统回调 onServiceConnected()",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（仅 Log.v(\"Hello\", \"on Service Connected\")）",
      "shown_text_zh": "无界面反馈；静默将事件类型覆写为 -1（全类型）、notificationTimeout=100ms、packageNames=com.camacc",
      "user_action_requested": "无；onKeyEvent 记录音量键后 return true 吞掉按键事件，不向用户回显任何提示",
      "code_anchor": "com.example.rat.service.logger.onServiceConnected / com.example.rat.service.logger.onKeyEvent"
    }
  ],
  "text_presentation_locations": [
    "res/layout/activity_main.xml：唯一的启动页布局，TextView 的 android:text 为空字符串，无任何引导文字",
    "res/values/strings.xml：仅有 app_name=rat 与 AppCompat 内置字符串（abc_*、search_menu_title 等），无一条引导/说明/权限申请文案",
    "res/xml/logger.xml：无障碍服务配置，android:settingsActivity 为空、无 android:description、无 android:summary —— 系统无障碍列表条目呈现为无说明的裸名 rat",
    "com.example.rat.service.forground_service.onCreate：通知栏常驻文案 \"Chat is running\"（伪装聊天应用，与无障碍无关）",
    "res/layout/custom_dialog.xml：仅含一个 text=\" Ok \" 的 Button，且未被任何业务类实例化使用，无说明性内容",
    "assets/ 目录：不存在（空），无任何本地 HTML 引导页",
    "结论：全包不存在任何面向用户的无障碍授权说明文字，也不存在弹窗、WebView、悬浮遮罩等承载位置"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Chat is running",
      "text_zh": "聊天正在运行",
      "source_location": "硬编码于 com.example.rat.service.forground_service.onCreate（NotificationCompat.Builder.setContentTitle/setContentText）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "rat",
      "text_zh": "rat（老鼠，同时是远程访问木马 RAT 的缩写）",
      "source_location": "res/values/strings.xml 的 app_name，同时作为无障碍服务在系统列表中的显示名",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": " Ok ",
      "text_zh": "确定",
      "source_location": "res/layout/custom_dialog.xml 的 Button android:text（未被业务代码引用）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "无任何循环机制：应用既不跳转设置页，也不检测授权状态，不存在 onResume 重跳、Timer 拉起或拒绝后的反馈；用户即使永久不授权，应用行为亦无变化，仅在后台持续保活并等待服务被系统启用",
    "overlay_or_fake_settings": "无；未检索到 WindowManager.addView 业务调用、SYSTEM_ALERT_WINDOW 权限、TYPE_APPLICATION_OVERLAY/TYPE_SYSTEM_ALERT 常量，也无高仿系统无障碍开关页",
    "restricted_settings_13plus_coaching": "无；targetSdkVersion=22（远低于 Android 13），不涉及受限设置教学，也无 Session 安装器绕过代码",
    "post_grant_anti_removal": "无自点确认或 GLOBAL_ACTION_BACK/HOME 撤权阻断逻辑（onAccessibilityEvent 为空实现，onInterrupt 为空实现）；保活改由 Evernote JobManager 周期任务 + 前台服务 \"Chat is running\" 通知承担",
    "benign_graceful_degradation": "无；应用不提供任何替代路径或降级说明，授权与否均静默运行后台采集任务"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "本应用不会拉起 ACCESSIBILITY_SETTINGS 或 APP_DETAILS，无法用设置跳转作钩子。应以『启动 com.example.rat 后 1.5 秒内界面即刻消失 + 出现 com.example.rat.service.forground_service 前台通知』为触发点，随后手动进入 系统设置→无障碍→已下载的服务 抓取 rat 条目页；若需覆盖授权后行为，则在开启服务后回到主屏并按键，观察音量键被吞与无反馈现象。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动空白壳页（关键反证：证明无引导界面）",
        "page_identifier": "com.example.rat.MainActivity，Theme 使用 AppTheme，布局仅一个空 TextView；excludeFromRecents=true，UTG 上表现为无文本、无按钮的空白窗口并在毫秒级消失",
        "why_most_useful": "若该页存在任何权限说明文字，则属引导式申请；实测为空白且立即 finish，可直接判定应用不向用户做任何告知，这是区分『隐蔽引导』与『零引导静默潜伏』的决定性画面",
        "observable_utg_signals": [
          "Activity 名 com.example.rat.MainActivity 且文本节点数为 0",
          "页面停留时间极短（onCreate 末尾 finish()）",
          "无任何 Dialog/WebView 子节点"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项（关键：证明无说明文本）",
        "page_identifier": "系统设置 com.android.settings 无障碍页中名为 rat 的条目，无 summary 副标题",
        "why_most_useful": "该条目是用户唯一能看到无障碍服务存在的地方；android:description/summary 均为空，故条目无解释文字，可证明应用未履行告知义务，用户是在完全不知情下开启全窗口内容读取权限",
        "observable_utg_signals": [
          "条目文本仅 \"rat\"，无副标题/说明行",
          "不存在 settingsActivity 跳转入口（无设置齿轮）",
          "开关状态可被外部开启，应用侧无任何提示"
        ]
      },
      {
        "page_role": "伪装常驻通知（证明社会工程伪装手法）",
        "page_identifier": "通知栏来自 com.example.rat、渠道由 createNotificationChannel 创建，标题与正文均为 Chat is running，setOngoing(true)",
        "why_most_useful": "该通知是应用唯一的对外可见文本，伪装为聊天应用以降低用户对后台常驻进程的怀疑，是判断其规避用户注意的补充信号",
        "observable_utg_signals": [
          "通知标题/正文 verbatim \"Chat is running\"",
          "ongoing=true 不可滑动清除",
          "通知来源包名 com.example.rat 与文案语义不一致"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无纯图空文本诱导，也无加壳/密文载荷阻碍运行期 UTG。唯一盲区是『零引导』本身：由于应用不跳设置、不弹窗、不检测授权，纯 UTG 在冷启动阶段几乎无可捕获的引导画面，需结合静态证据（无 ACTION_ACCESSIBILITY_SETTINGS 引用、logger.xml 无 description）才能闭环判定为静默潜伏而非引导缺失的良性应用。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.example.rat.MainActivity.onCreate",
    "com.example.rat.service.logger.onServiceConnected",
    "com.example.rat.service.logger.onKeyEvent",
    "com.example.rat.service.forground_service.onCreate",
    "res/xml/logger.xml",
    "res/layout/activity_main.xml"
  ]
}
```

</details>
