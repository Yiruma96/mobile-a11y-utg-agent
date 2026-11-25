# MR_104__59aa5297b9｜SpyAgent — FBPRO

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：131.3s

## 1. 一句话核心结论

- **核心申请方式**：冷启动即以开关字符串控制、先自禁 LAUNCHER 图标再静默跳转 android.settings.ACCESSIBILITY_SETTINGS，全程零说明文案、零取消入口，获权后全量事件记录各应用界面文本外发 ddns.net 控制端。
- **静态可见性说明**：无障碍引导链（M.onCreate→M.a→ACCESSIBILITY_SETTINGS）完全静态可见，无加壳、无加密资源、无远端 HTML；引导环节本身不含任何文案资源，因此不存在藏于远端页面的说明内容。仅 C2（A 服务自定义分隔符协议 c0c1c3a2c0c1c）指令语义与远端下发内容需动态观测。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `59aa5297b983f2709a113eab96d1b1e18aa04029b1089ba0b3f23ed68f6659ab` |
| 包名 / 年份 | `yps.eton.application` / 2018 |
| 家族 / 品类 | **SpyAgent**（同池样本数：12） |
| 原始来源标识 | https://www.fortinet.com/blog/threat-research/android-spyware-now-dropping-legit-apps- |
| 桌面显示名 | FBPRO |
| 引导页宣称品牌/身份 | FBPRO（暗示 Facebook Pro 类第三方客户端，实际无任何 Facebook 业务功能，为远控窃密木马） |
| 系统无障碍列表服务名 | FBPRO（@string/service_name，与桌面名同名，系统无障碍列表中无功能说明） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务未声明 android:description（系统开启警告页无任何用途说明）；跳转前用 setComponentEnabledSetting 将自身 LAUNCHER 组件置为 DISABLED 使桌面图标消失、用户无法返回应用详情核对；伴生 Activity h 设 android:label="" + @drawable/transparent 透明图标 + excludeFromRecents；无 activity-alias 多开、无 isAccessibilityTool 伪造（targetSdkVersion=22 该 API 不存在） |
| 无障碍服务类名 | `yps.eton.application.k` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | yps.eton.application.M（LAUNCHER Activity，主题 @android:style/Theme.Translucent.NoTitleBar） | 用户点击桌面图标 FBPRO，进入 M.onCreate(Bundle) | 原生Activity | 无 | 无任何交互要求，用户尚未看到任何说明 | `yps.eton.application.M#onCreate` |
| 2 | 跳转前自我隐藏 | M.a() 内部执行 getPackageManager().setComponentEnabledSetting(new ComponentName(this, M.class), COMPONENT_ENABLED_STATE_DISABLED(2), DONT_KILL_APP(1)) 后 super.onBackPressed() | group_properties(0x7f080023)="10000100" 第 4 位为 '0' 进入 a()，第 0 位为 '1' 命中自禁分支 | 原生Activity | 无 | 无需操作；用户被动被退出应用界面，且无取消或跳过按钮 | `yps.eton.application.M#a` |
| 3 | 跳无障碍设置 | Intent("android.settings.ACCESSIBILITY_SETTINGS") + setFlags(FLAG_ACTIVITY_NEW_TASK) → 系统「无障碍 / 已下载的服务」列表页 | group_properties 第 6 位为 '1' 时在同一方法末尾 startActivity | 系统无障碍页 | **原文**：无（应用自身不提供任何说明文字；系统页内列表项显示为 "FBPRO"）<br>**译注**：用户被直接投放到系统无障碍服务列表，需自行找到并开启名为 FBPRO 的服务 | 要求用户手动在列表中点击 FBPRO 并确认开启；应用未提供任何用途解释，也无取消/跳过提示（应用此时已不在桌面） | `yps.eton.application.M#a` |
| 4 | 获权后动作 | yps.eton.application.k（AccessibilityService，label=@string/service_name="FBPRO"） | 用户在系统页开启服务，系统回调 k.onServiceConnected() | 不可静态还原 | **原文**：>>>onServiceConnected<br>**译注**：仅输出调试日志；随后 setServiceInfo(flags=89, eventTypes=-1, feedbackType=16)，并置 A.h=true 标记无障碍已就绪 | 无；服务在后台无感运行 | `yps.eton.application.k#onServiceConnected` |
| 5 | 获权后动作 | k.onAccessibilityEvent → 写 config<yyyy-MM-dd>.log → 线程外发 A 服务（host=elihfadifouad.ddns.net,1207） | 任意应用界面产生 AccessibilityEvent（eventTypes=-1 全量） | 不可静态还原 | **原文**：Package Name:= / Text:= / Time:= / ###--- End ---###9xf89fff9xf89<br>**译注**：逐条记录当前应用包名、界面全部文本与时间戳，落盘后外发控制端，等效全局键盘/屏幕文本记录 | 无 | `yps.eton.application.k#onAccessibilityEvent` |
| 6 | 拒权反馈循环 | 导出广播接收器 yps.eton.application.Z → startService(A)；BOOT_COMPLETED 接收器 B；AlarmManager 180s 重复（当前开关关闭） | 外部广播命中 Z.onReceive，或开机广播 B；M.onCreate 中 group_properties 第 7 位为 '1' 时注册 180000ms 重复 PendingIntent | 不可静态还原 | 无 | 无（无提示、无降级路径，用户无法感知复活） | `yps.eton.application.Z#onReceive` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 无任何引导/说明文字位置：应用未使用 Dialog、Toast、Activity 布局、WebView、assets HTML 或悬浮窗承载无障碍说明
- 系统无障碍列表项名称：@string/service_name = "FBPRO"（Manifest 中 service yps.eton.application.k 的 android:label）
- 系统无障碍开启警告页：k 未声明 android:description，故该页「此服务可读取屏幕全部内容」上方无任何应用自述用途
- 桌面图标名：@string/app_name = "FBPRO"（跳转后被 setComponentEnabledSetting 关闭，图标消失）
- 硬编码于 M.a() 的跳转目标字符串：android.settings.ACCESSIBILITY_SETTINGS（非用户可见文本）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | FBPRO | FBPRO（暗示 Facebook Pro 客户端） | `res/values/strings.xml → app_name / client_name / service_name` | 未知 |
| en | 10000100 | 内部功能开关位串：第0位=自禁图标、第4位=直接走无障碍分支、第6位=跳无障碍设置、第7位=180秒定时复活 | `res/values/strings.xml → group_properties（0x7f080023）` | 未知 |
| en | elihfadifouad.ddns.net,1207 | 控制端动态域名与端口 | `res/values/strings.xml → host（0x7f080024）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：M.onCreate 内为 try{}catch(Exception){} 静默块，无任何检测或提示；拒绝开启后应用已在第 2 步自禁 LAUNCHER 组件，桌面无图标可再次进入，改为依赖 exported 的 Z 广播接收器与 BOOT_COMPLETED 接收器 B 静默 startService(A)，由 A 服务的 startActivity 分支在后台重新投放 ACCESSIBILITY_SETTINGS（AlarmManager 每 180 秒重复拉起由 group_properties 第 7 位控制，本样本为 '0' 未启用）
- **遮罩叠层 / 高仿系统设置页**：无。SYSTEM_ALERT_WINDOW 权限已声明但无障碍引导路径不叠遮罩、不做高仿设置页，属更隐蔽的「无文案硬跳」式引导
- **Android 13+ 受限设置（Restricted Settings）应对**：无。全包无 ACTION_APPLICATION_DETAILS_SETTINGS、无「右上角菜单→允许受限设置」教学、无 Session 安装器绕过代码（targetSdkVersion=22，本就不受 Android 13 限制）
- **获权后即时行为与防撤权机制**：获权后不自点确认、不用 GLOBAL_ACTION_BACK/HOME 阻止撤权；但通过跳转前自禁 LAUNCHER 组件使图标消失、Activity h 透明无标签且 excludeFromRecents、以及 D 设备管理员接收器（ADD_DEVICE_ADMIN 分支，本配置未触发）提高卸载与撤权门槛
- **良性降级 / 替代方案**：无。不存在手动模式、仅观看模式、ADB 指引或任何降级路径

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在冷启动后监测到 Intent action == android.settings.ACCESSIBILITY_SETTINGS 的 startActivity 瞬间立即拉起 UTG（该跳转距进程启动仅数十毫秒，且应用界面本身透明无内容，不宜以「等待弹窗」为触发条件）；同时在检测到 LAUNCHER 组件被 setComponentEnabledSetting 置为 DISABLED 时补拍一次桌面图标消失状态。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：纯图空文本盲区不存在（引导环节无图无文案）。主要盲区有两点：一是应用界面为 Translucent 主题且自禁 LAUNCHER 组件，UTG 若仅在「应用自有页面出现」时启动采样会完全错过跳转；二是内嵌 base.apk 投放安装分支（M$1.run → ACTION_VIEW application/vnd.android.package-archive）被 merge_file="0" 关闭，静态存在但本样本不执行，UTG 运行期不会观察到二阶段安装器。C2 指令语义需动态抓包补充。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **系统无障碍服务列表页（跳转落点）** | 包名 com.android.settings 的 AccessibilitySettings Activity，列表项文本为 "FBPRO" | 这是本样本唯一呈现「申请无障碍」的可见界面；该页出现而此前无任何应用自述说明页，即构成零告知诱导的直接证据 | 无障碍设置页在冷启动后 1 秒内出现且此前无应用自有页面；列表项标签为 "FBPRO" 且无用途描述；应用进程已无可见前台 Activity（M 已 finish） |
| **跳转瞬间的前台窗口快照** | yps.eton.application.M（Theme.Translucent.NoTitleBar）短暂前台窗口 | 验证应用侧全程无 Dialog/WebView/说明文字，只有透明窗口一闪即过，可排除「先展示说明再跳转」的良性解释 | M 窗口节点树为空或无文本节点；M 与系统设置页切换间隔极短（<500ms）；桌面图标 FBPRO 消失 |
| **获权后服务运行态** | 系统无障碍「已开启的服务」条目 FBPRO + 应用私有目录 config<yyyy-MM-dd>.log | 确认服务开启后立即注册全量事件并落盘界面文本，把「引导开启」与「实际滥用」串联成完整链 | 无障碍服务状态变为 ON；logcat 出现 >>>onServiceConnected；files 目录生成 config<日期>.log 且内容含 Package Name:= 与 Text:= |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `yps.eton.application.M#onCreate`
- `yps.eton.application.M#a`
- `yps.eton.application.M#onActivityResult`
- `yps.eton.application.k#onServiceConnected`
- `yps.eton.application.k#onAccessibilityEvent`
- `res/values/strings.xml#L38-L42`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**无障碍引导的核心机制：无引导、无文案、冷启动直接跳系统设置页。** 该应用在无障碍申请环节没有任何说明页、弹窗、WebView 或悬浮窗，是纯代码硬跳转，完全静态可见。

- **触发点**：[M.onCreate()](<resource-unit:#1.dex1 code:yps.eton.application.M#onCreate>) 读取字符串资源 `0x7f080023`（`group_properties` = `10000100`），第 4 位为 `'0'` 时调用 [M.a()](<resource-unit:#1.dex1 code:yps.eton.application.M#a>)。
- **跳转前自我隐藏**：`M.a()` 中第 0 位为 `'1'` → `setComponentEnabledSetting(M, COMPONENT_ENABLED_STATE_DISABLED, DONT_KILL_APP)` 关闭自身 LAUNCHER 组件，再 `super.onBackPressed()` 退出界面；随后第 6 位为 `'1'` → `new Intent("android.settings.ACCESSIBILITY_SETTINGS")` + `FLAG_ACTIVITY_NEW_TASK` 直接拉起系统无障碍服务列表。**用户看到的顺序是：点击图标→界面瞬间消失→被丢到系统无障碍页**，且图标已从桌面消失，无法回头查看应用信息。
- **零告知证据**：Manifest 中 `yps.eton.application.k` 服务仅声明 `BIND_ACCESSIBILITY_SERVICE` 权限，**未声明 `android:description`**；`strings.xml` 中不存在任何引导/说明文案，`service_name` 仅为 `FBPRO`。全包仅一处 `android.settings.` 字符串（无 `ACTION_APPLICATION_DETAILS_SETTINGS`、无 Android 13 受限设置教学、无 Session 安装器绕过）。
- **拒绝无回环、但靠后台复活**：本配置下不触发 `startActivityForResult` 设备管理员分支，故 `onActivityResult` 双分支回跳路径未激活；复活依赖导出的 [Z.onReceive()](<resource-unit:#1.dex1 code:yps.eton.application.Z#onReceive>)（任意广播即 `startService(A)`）与 `BOOT_COMPLETED` 接收器 B，以及未启用的 180 秒 `AlarmManager` 重复拉起（`group_properties` 第 7 位为 `'0'`，当前关闭）。
- **获权后立即用于键盘记录**：[k.onServiceConnected()](<resource-unit:#1.dex1 code:yps.eton.application.k#onServiceConnected>) 注册 `eventTypes=-1`、`flags=89`、`feedbackType=16`；[k.onAccessibilityEvent()](<resource-unit:#1.dex1 code:yps.eton.application.k#onAccessibilityEvent>) 把每个应用的 `Package Name:= / Text:= / Time:=` 写入 `config<日期>.log` 并起线程外发至 `elihfadifouad.ddns.net,1207`。
- **未触发但已存在的分支**：内嵌 `base.apk` 释放安装（`M$1.run` → `ACTION_VIEW` `application/vnd.android.package-archive`，落到 `/<service_name>/base.apk`）由 `merge_file` 开关控制，本样本 `merge_file="0"` 关闭。
- **UTG 检测建议**：不必等弹窗，应监控 `ACCESSIBILITY_SETTINGS` 跳转瞬间与随后系统列表页；该样本无 OCR 需求（无图、无文案）。

已登记风险：**R-001**（malware_trojan / high）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导链（M.onCreate→M.a→ACCESSIBILITY_SETTINGS）完全静态可见，无加壳、无加密资源、无远端 HTML；引导环节本身不含任何文案资源，因此不存在藏于远端页面的说明内容。仅 C2（A 服务自定义分隔符协议 c0c1c3a2c0c1c）指令语义与远端下发内容需动态观测。",
  "summary_one_liner": "冷启动即以开关字符串控制、先自禁 LAUNCHER 图标再静默跳转 android.settings.ACCESSIBILITY_SETTINGS，全程零说明文案、零取消入口，获权后全量事件记录各应用界面文本外发 ddns.net 控制端。",
  "disguise_identity": {
    "app_display_name": "FBPRO",
    "claimed_brand_or_persona": "FBPRO（暗示 Facebook Pro 类第三方客户端，实际无任何 Facebook 业务功能，为远控窃密木马）",
    "a11y_service_label": "FBPRO（@string/service_name，与桌面名同名，系统无障碍列表中无功能说明）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务未声明 android:description（系统开启警告页无任何用途说明）；跳转前用 setComponentEnabledSetting 将自身 LAUNCHER 组件置为 DISABLED 使桌面图标消失、用户无法返回应用详情核对；伴生 Activity h 设 android:label=\"\" + @drawable/transparent 透明图标 + excludeFromRecents；无 activity-alias 多开、无 isAccessibilityTool 伪造（targetSdkVersion=22 该 API 不存在）"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "yps.eton.application.M（LAUNCHER Activity，主题 @android:style/Theme.Translucent.NoTitleBar）",
      "trigger_event": "用户点击桌面图标 FBPRO，进入 M.onCreate(Bundle)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "透明无标题主题，界面不渲染任何内容（无文字、无图标、无按钮）",
      "user_action_requested": "无任何交互要求，用户尚未看到任何说明",
      "code_anchor": "yps.eton.application.M#onCreate"
    },
    {
      "step": 2,
      "stage": "跳转前自我隐藏",
      "screen_or_component": "M.a() 内部执行 getPackageManager().setComponentEnabledSetting(new ComponentName(this, M.class), COMPONENT_ENABLED_STATE_DISABLED(2), DONT_KILL_APP(1)) 后 super.onBackPressed()",
      "trigger_event": "group_properties(0x7f080023)=\"10000100\" 第 4 位为 '0' 进入 a()，第 0 位为 '1' 命中自禁分支",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "界面立即关闭（onBackPressed），桌面图标随后消失",
      "user_action_requested": "无需操作；用户被动被退出应用界面，且无取消或跳过按钮",
      "code_anchor": "yps.eton.application.M#a"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "Intent(\"android.settings.ACCESSIBILITY_SETTINGS\") + setFlags(FLAG_ACTIVITY_NEW_TASK) → 系统「无障碍 / 已下载的服务」列表页",
      "trigger_event": "group_properties 第 6 位为 '1' 时在同一方法末尾 startActivity",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用自身不提供任何说明文字；系统页内列表项显示为 \"FBPRO\"）",
      "shown_text_zh": "用户被直接投放到系统无障碍服务列表，需自行找到并开启名为 FBPRO 的服务",
      "user_action_requested": "要求用户手动在列表中点击 FBPRO 并确认开启；应用未提供任何用途解释，也无取消/跳过提示（应用此时已不在桌面）",
      "code_anchor": "yps.eton.application.M#a"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "yps.eton.application.k（AccessibilityService，label=@string/service_name=\"FBPRO\"）",
      "trigger_event": "用户在系统页开启服务，系统回调 k.onServiceConnected()",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": ">>>onServiceConnected",
      "shown_text_zh": "仅输出调试日志；随后 setServiceInfo(flags=89, eventTypes=-1, feedbackType=16)，并置 A.h=true 标记无障碍已就绪",
      "user_action_requested": "无；服务在后台无感运行",
      "code_anchor": "yps.eton.application.k#onServiceConnected"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "k.onAccessibilityEvent → 写 config<yyyy-MM-dd>.log → 线程外发 A 服务（host=elihfadifouad.ddns.net,1207）",
      "trigger_event": "任意应用界面产生 AccessibilityEvent（eventTypes=-1 全量）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Package Name:= / Text:= / Time:= / ###--- End ---###9xf89fff9xf89",
      "shown_text_zh": "逐条记录当前应用包名、界面全部文本与时间戳，落盘后外发控制端，等效全局键盘/屏幕文本记录",
      "user_action_requested": "无",
      "code_anchor": "yps.eton.application.k#onAccessibilityEvent"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "导出广播接收器 yps.eton.application.Z → startService(A)；BOOT_COMPLETED 接收器 B；AlarmManager 180s 重复（当前开关关闭）",
      "trigger_event": "外部广播命中 Z.onReceive，或开机广播 B；M.onCreate 中 group_properties 第 7 位为 '1' 时注册 180000ms 重复 PendingIntent",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "用户拒绝开启后，后台服务通过导出广播/开机广播被重新拉起，可再次经 A 服务的 startActivity 分支重新投放设置页",
      "user_action_requested": "无（无提示、无降级路径，用户无法感知复活）",
      "code_anchor": "yps.eton.application.Z#onReceive"
    }
  ],
  "text_presentation_locations": [
    "无任何引导/说明文字位置：应用未使用 Dialog、Toast、Activity 布局、WebView、assets HTML 或悬浮窗承载无障碍说明",
    "系统无障碍列表项名称：@string/service_name = \"FBPRO\"（Manifest 中 service yps.eton.application.k 的 android:label）",
    "系统无障碍开启警告页：k 未声明 android:description，故该页「此服务可读取屏幕全部内容」上方无任何应用自述用途",
    "桌面图标名：@string/app_name = \"FBPRO\"（跳转后被 setComponentEnabledSetting 关闭，图标消失）",
    "硬编码于 M.a() 的跳转目标字符串：android.settings.ACCESSIBILITY_SETTINGS（非用户可见文本）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "FBPRO",
      "text_zh": "FBPRO（暗示 Facebook Pro 客户端）",
      "source_location": "res/values/strings.xml → app_name / client_name / service_name",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "10000100",
      "text_zh": "内部功能开关位串：第0位=自禁图标、第4位=直接走无障碍分支、第6位=跳无障碍设置、第7位=180秒定时复活",
      "source_location": "res/values/strings.xml → group_properties（0x7f080023）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "elihfadifouad.ddns.net,1207",
      "text_zh": "控制端动态域名与端口",
      "source_location": "res/values/strings.xml → host（0x7f080024）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "M.onCreate 内为 try{}catch(Exception){} 静默块，无任何检测或提示；拒绝开启后应用已在第 2 步自禁 LAUNCHER 组件，桌面无图标可再次进入，改为依赖 exported 的 Z 广播接收器与 BOOT_COMPLETED 接收器 B 静默 startService(A)，由 A 服务的 startActivity 分支在后台重新投放 ACCESSIBILITY_SETTINGS（AlarmManager 每 180 秒重复拉起由 group_properties 第 7 位控制，本样本为 '0' 未启用）",
    "overlay_or_fake_settings": "无。SYSTEM_ALERT_WINDOW 权限已声明但无障碍引导路径不叠遮罩、不做高仿设置页，属更隐蔽的「无文案硬跳」式引导",
    "restricted_settings_13plus_coaching": "无。全包无 ACTION_APPLICATION_DETAILS_SETTINGS、无「右上角菜单→允许受限设置」教学、无 Session 安装器绕过代码（targetSdkVersion=22，本就不受 Android 13 限制）",
    "post_grant_anti_removal": "获权后不自点确认、不用 GLOBAL_ACTION_BACK/HOME 阻止撤权；但通过跳转前自禁 LAUNCHER 组件使图标消失、Activity h 透明无标签且 excludeFromRecents、以及 D 设备管理员接收器（ADD_DEVICE_ADMIN 分支，本配置未触发）提高卸载与撤权门槛",
    "benign_graceful_degradation": "无。不存在手动模式、仅观看模式、ADB 指引或任何降级路径"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在冷启动后监测到 Intent action == android.settings.ACCESSIBILITY_SETTINGS 的 startActivity 瞬间立即拉起 UTG（该跳转距进程启动仅数十毫秒，且应用界面本身透明无内容，不宜以「等待弹窗」为触发条件）；同时在检测到 LAUNCHER 组件被 setComponentEnabledSetting 置为 DISABLED 时补拍一次桌面图标消失状态。",
    "key_pages_to_capture": [
      {
        "page_role": "系统无障碍服务列表页（跳转落点）",
        "page_identifier": "包名 com.android.settings 的 AccessibilitySettings Activity，列表项文本为 \"FBPRO\"",
        "why_most_useful": "这是本样本唯一呈现「申请无障碍」的可见界面；该页出现而此前无任何应用自述说明页，即构成零告知诱导的直接证据",
        "observable_utg_signals": ["无障碍设置页在冷启动后 1 秒内出现且此前无应用自有页面", "列表项标签为 \"FBPRO\" 且无用途描述", "应用进程已无可见前台 Activity（M 已 finish）"]
      },
      {
        "page_role": "跳转瞬间的前台窗口快照",
        "page_identifier": "yps.eton.application.M（Theme.Translucent.NoTitleBar）短暂前台窗口",
        "why_most_useful": "验证应用侧全程无 Dialog/WebView/说明文字，只有透明窗口一闪即过，可排除「先展示说明再跳转」的良性解释",
        "observable_utg_signals": ["M 窗口节点树为空或无文本节点", "M 与系统设置页切换间隔极短（<500ms）", "桌面图标 FBPRO 消失"]
      },
      {
        "page_role": "获权后服务运行态",
        "page_identifier": "系统无障碍「已开启的服务」条目 FBPRO + 应用私有目录 config<yyyy-MM-dd>.log",
        "why_most_useful": "确认服务开启后立即注册全量事件并落盘界面文本，把「引导开启」与「实际滥用」串联成完整链",
        "observable_utg_signals": ["无障碍服务状态变为 ON", "logcat 出现 >>>onServiceConnected", "files 目录生成 config<日期>.log 且内容含 Package Name:= 与 Text:="]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "纯图空文本盲区不存在（引导环节无图无文案）。主要盲区有两点：一是应用界面为 Translucent 主题且自禁 LAUNCHER 组件，UTG 若仅在「应用自有页面出现」时启动采样会完全错过跳转；二是内嵌 base.apk 投放安装分支（M$1.run → ACTION_VIEW application/vnd.android.package-archive）被 merge_file=\"0\" 关闭，静态存在但本样本不执行，UTG 运行期不会观察到二阶段安装器。C2 指令语义需动态抓包补充。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED"
  ],
  "code_anchors": [
    "yps.eton.application.M#onCreate",
    "yps.eton.application.M#a",
    "yps.eton.application.M#onActivityResult",
    "yps.eton.application.k#onServiceConnected",
    "yps.eton.application.k#onAccessibilityEvent",
    "res/values/strings.xml#L38-L42"
  ]
}
```

</details>
