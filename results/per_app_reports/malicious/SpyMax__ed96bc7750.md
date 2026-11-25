# MR_133__ed96bc7750｜SpyMax — null

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：205.3s

## 1. 一句话核心结论

- **核心申请方式**：用全透明无 UI 的启动器 Activity 在配置开关放行时直接静默拉起系统无障碍设置页，应用名与无障碍服务名均伪装为字面量 null、无任何说明文案与取消路径，获权后以全事件监听采集全屏文本外发。
- **静态可见性说明**：无障碍申请链路（启动器 M 的配置位判定、ACTION_ACCESSIBILITY_SETTINGS 跳转、onActivityResult 双分支归并、k 服务的 flags/事件采集）全部静态可见，无 HTML/WebView/远端页面参与；但触发与否由 res/values/strings.xml 的 group_properties="00000000" 八位开关决定（默认不跳无障碍页），且 res/raw/google.apk 为 0 字节，二阶段安装载荷在本样本中缺失。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `ed96bc775074cb74426d061a9ec4cb5d0078c1077d229c702fa5da9a1f4febae` |
| 包名 / 年份 | `yps.eton.application` / 2020 |
| 家族 / 品类 | **SpyMax**（同池样本数：23） |
| 原始来源标识 | https://blog.lookout.com/commercial-surveillanceware-operators-latest-to-take-advantage-of-covid-19 |
| 桌面显示名 | null |
| 引导页宣称品牌/身份 | 无任何品牌或身份宣称（label 与无障碍服务名均直接显示为字符串 null，不冒充系统或具体厂商） |
| 系统无障碍列表服务名 | null |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：app_name 与 service_name 均为字面量 "null"，使桌面图标名与系统无障碍服务列表项显示为 null；无障碍服务未声明 android:description（预筛 description 为空）；启动器 M 使用 Theme.Translucent.NoTitleBar 且布局仅空 <x/>，点击图标后无可辨识界面；另有 excludeFromRecents=true、icon=@drawable/transparent、label="" 的隐藏 Activity h，以及多处用空白字符拼接外发分隔符（c0c1c3a2c0c1c、fxf0x4x4x0fxf）规避字符串特征；未见伪造 isAccessibilityTool 或多 activity-alias。 |
| 无障碍服务类名 | `yps.eton.application.k` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | yps.eton.application.M（LAUNCHER，Theme.Translucent.NoTitleBar，layout activity_m.xml 仅 <x/>） | 用户点击桌面图标 → Activity.onCreate | 原生Activity | **原文**：无（布局为空 <x />，窗口全透明，无任何文案）<br>**译注**：界面完全空白透明，用户看不到任何提示或说明 | 无任何可交互控件，无按钮、无取消、无跳过 | `yps.eton.application.M#onCreate / res/layout/activity_m.xml / res/values/strings.xml(app_name=null)` |
| 2 | 引导说明页（缺失） | 无对应组件：全包不存在引导页、弹窗、WebView 或 HTML 资源 | 不适用——未实现任何说明或索取理由环节 | 不可静态还原 | 无 | 无 | `res/values/strings.xml 仅含 abc_* 与 8 条业务键，无任何说明文案` |
| 3 | 跳受限设置 | yps.eton.application.M#a() → 系统设置 android.settings.ACCESSIBILITY_SETTINGS | group_properties.charAt(6)=='1' 时，onCreate 走 a()（charAt(4)=='0' 分支）或 onActivityResult 无条件回调 a()，在 super.onBackPressed() 后 startActivity(NEW_TASK) | 系统无障碍页 | **原文**：intent.setAction("android.settings.ACCESSIBILITY_SETTINGS");<br>**译注**：直接打开系统无障碍服务设置页，列表中出现一个名为 null 的服务项 | 要求用户在系统列表中自行找到并开启名为 null 的无障碍服务；跳转本身无确认框 | `yps.eton.application.M#a` |
| 4 | 拒权反馈循环 | yps.eton.application.M#onActivityResult（设备管理员请求返回） | ADD_DEVICE_ADMIN 的 startActivityForResult(…,100) 返回，或任意结果码 | 原生Activity | **原文**：if (i2 == -1) { a(); } else { a(); } finish();<br>**译注**：无论用户同意还是拒绝设备管理员，均再次调用 a() 进入无障碍设置页并结束自身 | 无取消/拒绝后停留的降级路径；拒绝即被再次送往无障碍设置 | `yps.eton.application.M#onActivityResult` |
| 5 | 获权后动作 | yps.eton.application.k（AccessibilityService，label=@string/service_name=null，无 android:description） | 系统回调 onServiceConnected → setServiceInfo(flags=89, eventTypes=-1)；随后每次 onAccessibilityEvent | 系统无障碍页 | **原文**：accessibilityServiceInfo.flags = 89; accessibilityServiceInfo.eventTypes = -1;<br>**译注**：注册包含非重要视图、增强 Web 无障碍、上报视图 ID、获取交互窗口的全事件监听；把每个界面的全部文本、包名、时间写入私有 config<日期>.log，A.i 为真时经 socket 外发到 assdsiwi.ddns.net:1515 | 无需再操作，权限在后台持续生效 | `yps.eton.application.k#onServiceConnected / yps.eton.application.k#onAccessibilityEvent / yps.eton.application.k#a(String,Context)` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：仅显示字符串 "null"（service_name），且未声明 android:description，无任何用途说明
- 桌面启动器图标名称：仅显示 "null"（app_name）
- 应用内：无任何呈现位置——activity_m.xml 为空布局 <x/>，不存在 AlertDialog、引导 Activity、assets HTML、WebView 或悬浮窗
- 跳转系统设置后：不叠加任何遮罩或悬浮引导层，用户面对的是原生设置页

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | null | 空值字面量（非有效名称，界面显示为 null） | `res/values/strings.xml key=app_name` | 未知 |
| en | null | 空值字面量（系统无障碍服务列表项显示为 null） | `res/values/strings.xml key=service_name` | 未知 |
| en | 00000000 | 八位行为开关，默认全关（无障碍跳转位 charAt(6) 为 0，即默认不跳转） | `res/values/strings.xml key=group_properties` | 未知 |
| en | assdsiwi.ddns.net,1515 | C2 主机与端口（Socket 直连，非界面文案） | `res/values/strings.xml key=host` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：无 onResume 轮询式死循环；但 onActivityResult 的 if/else 双分支均调用 a()，即用户拒绝设备管理员授权后仍被立即送入无障碍设置页并 finish() 自身；另有 charAt(7)=='1' 时 AlarmManager 每 180000ms 重复拉起 Z 广播接收器的后台再激活通道（Z 的具体行为本轮未展开）
- **遮罩叠层 / 高仿系统设置页**：无。未使用 SYSTEM_ALERT_WINDOW 叠层引导，也未伪造高仿无障碍开关页，直接跳转系统原生设置页
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未使用 ACTION_APPLICATION_DETAILS_SETTINGS，无“右上角菜单允许受限设置”教学，无 Session 安装器绕过；targetSdkVersion=22 且无对应引导
- **获权后即时行为与防撤权机制**：未发现监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权的逻辑；但同包声明 DEVICE_ADMIN 接收器（yps.eton.application.D + res/xml/device_admin.xml）并在 charAt(4)!='0' 时申请激活设备管理员，构成独立的抗卸载/抗清除通道
- **良性降级 / 替代方案**：无。拒绝授权后既无降级模式也无手动替代路径

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 yps.eton.application.M 启动后 0.5s 内伴随 Activity 切换到 com.android.settings/.accessibility.AccessibilitySettings（或 intent=android.settings.ACCESSIBILITY_SETTINGS）的瞬间，同时抓取系统无障碍列表首屏
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在三点盲区：(1) 无障碍跳转受 group_properties 第 7 位控制，默认值 "00000000" 下不触发，若仅按默认配置运行会完全漏检，需先确认实际下发的配置串；(2) 二阶段载荷 res/raw/google.apk 在本样本中为 0 字节，UTG 无法观测到 APK 投递与安装页，只能看到逻辑存在；(3) 获权后的外发走原始 Socket 到 assdsiwi.ddns.net:1515，非常规 HTTP，常规流量层抓包难以解析内容，需配合文件系统侧 config<日期>.log 取证。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动入口（全透明空壳页）** | yps.eton.application.M，Theme.Translucent.NoTitleBar，根布局无可见子节点 | 证明应用未提供任何说明即直接跳转，是区分诱导式申请与良性透明告知的第一判据 | 启动后 Activity 树为空/无可见文本节点；Activity 存在时长极短（<1s）随即发生跳转；无任何对话框或权限理由弹窗 |
| **系统无障碍服务列表项（关键辨识页）** | com.android.settings 无障碍服务列表中显示名称为 null 的条目 | 直接暴露 app_name/service_name=null 的身份伪装与缺失 android:description，是本样本最具区分度的可见特征 | 列表项文本为 "null"；该条目无副标题/用途说明文本；紧邻列表项的应用包名为 yps.eton.application |
| **设备管理员授权页（拒权后强制再跳转的观察点）** | android.app.action.ADD_DEVICE_ADMIN 对应系统页，随后回到 M#onActivityResult | 用于验证拒绝授权后仍被强制送往无障碍设置的行为，构成无取消路径证据 | 设备管理员页返回后立即出现 ACCESSIBILITY_SETTINGS 跳转；无论点击取消或激活，后续页面序列一致 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `yps.eton.application.M#onCreate`
- `yps.eton.application.M#a`
- `yps.eton.application.M#onActivityResult`
- `yps.eton.application.k#onServiceConnected`
- `yps.eton.application.k#onAccessibilityEvent`
- `res/values/strings.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**核心判断：该样本完全没有“引导文案”。它的无障碍申请方式，是在配置开关允许时，用一个全透明、无 UI 的启动器 Activity，直接静默拉起系统无障碍设置页，然后把自己在列表中伪装成 `null`。**

1. **入口无界面**：LAUNCHER Activity [yps.eton.application.M](<resource-unit:#1.dex1 code:yps.eton.application.M>) 使用 `Theme.Translucent.NoTitleBar`，布局 [activity_m.xml](<resource-unit:#1 file:res/layout/activity_m.xml>) 只有一个空的 `<x />`；桌面名称与无障碍服务名都取自 [strings.xml](<resource-unit:#1 file:res/values/strings.xml>) 中的 `app_name` / `service_name`，值均为字面量 `null`。用户点击图标后，看不到任何说明页、弹窗或 WebView。

2. **跳转受限设置**：[M#a()](<resource-unit:#1.dex1 code:yps.eton.application.M#a>) 在 `group_properties.charAt(6)=='1'` 时执行 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS").setFlags(FLAG_ACTIVITY_NEW_TASK))`，并在同一方法里先 `super.onBackPressed()`。整个过程没有任何解释文本。

3. **配置驱动的 8 位开关**：`group_properties="00000000"` 是 `A` 服务、`M`、`k` 共同读取的行为位图：`charAt(0)` 控制是否释放并安装 APK；`charAt(4)` 控制是否走设备管理员路径，否则跳转无障碍设置；`charAt(6)` 控制无障碍跳转；`charAt(7)` 控制每 180 秒重复的 `AlarmManager` 拉起 `Z`。**默认值下无障碍跳转不触发**，说明这是由云端或构建配置下发的开关，而非硬编码行为。

4. **没有拒绝或取消出口**：[M#onActivityResult()](<resource-unit:#1.dex1 code:yps.eton.application.M#onActivityResult>) 中 `i2==-1` 与 `else` 两个分支都调用 `a()` 并 `finish()`；用户拒绝设备管理员后，仍会被送入无障碍设置页。未发现 `ACTION_APPLICATION_DETAILS_SETTINGS`，也没有针对 Android 13+ 受限设置的“右上角菜单”教学。

5. **无障碍服务本身的形态**：[k#onServiceConnected()](<resource-unit:#1.dex1 code:yps.eton.application.k#onServiceConnected>) 设置 `flags=89`（`INCLUDE_NOT_IMPORTANT_VIEWS|REQUEST_ENHANCED_WEB_ACCESSIBILITY|REPORT_VIEW_IDS|RETRIEVE_INTERACTIVE_WINDOWS`）、`eventTypes=-1`（全事件），并在 Manifest 中**不声明 `android:description`**。获权后 [k#onAccessibilityEvent()](<resource-unit:#1.dex1 code:yps.eton.application.k#onAccessibilityEvent>) 把全屏事件文本、包名、时间写入私有 `configYYYY-MM-DD.log`；当 `A.i` 为真时，经 `A.b` socket 外发到 `assdsiwi.ddns.net:1515`。服务在系统中显示为“null”，且没有说明，用户无法辨识其用途。

6. **没有遮罩、没有假设置页、没有 HTML**：全包无 `assets/`，`res/layout` 仅含 support/chat 布局，无 WebView、无 Overlay、无高仿无障碍开关页。`res/raw/google.apk` 长度为 **0 字节**，二阶段安装载荷在本样本中已被剥离；[M$1#run()](<resource-unit:#1.dex1 code:yps.eton.application.M$1#run>) 的 `ACTION_VIEW` + `application/vnd.android.package-archive` 投递逻辑仍完整存在。

7. **UTG 视角的判别信号**：最有效的时刻是“全透明启动器 Activity 立即让位于系统无障碍设置页”这一组合；`null` 标签在系统列表中的呈现，是区分该家族最直接的可见特征。

**覆盖边界**：`Z` 接收器的具体拉起内容、`A` 服务的完整 C2 协议族未在本轮展开；`group_properties` 的默认值使无障碍路径在本 APK 中处于“就绪但未开启”状态，实际触发依赖配置下发。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍申请链路（启动器 M 的配置位判定、ACTION_ACCESSIBILITY_SETTINGS 跳转、onActivityResult 双分支归并、k 服务的 flags/事件采集）全部静态可见，无 HTML/WebView/远端页面参与；但触发与否由 res/values/strings.xml 的 group_properties=\"00000000\" 八位开关决定（默认不跳无障碍页），且 res/raw/google.apk 为 0 字节，二阶段安装载荷在本样本中缺失。",
  "summary_one_liner": "用全透明无 UI 的启动器 Activity 在配置开关放行时直接静默拉起系统无障碍设置页，应用名与无障碍服务名均伪装为字面量 null、无任何说明文案与取消路径，获权后以全事件监听采集全屏文本外发。",
  "disguise_identity": {
    "app_display_name": "null",
    "claimed_brand_or_persona": "无任何品牌或身份宣称（label 与无障碍服务名均直接显示为字符串 null，不冒充系统或具体厂商）",
    "a11y_service_label": "null",
    "identity_mismatch": true,
    "obfuscation_tricks": "app_name 与 service_name 均为字面量 \"null\"，使桌面图标名与系统无障碍服务列表项显示为 null；无障碍服务未声明 android:description（预筛 description 为空）；启动器 M 使用 Theme.Translucent.NoTitleBar 且布局仅空 <x/>，点击图标后无可辨识界面；另有 excludeFromRecents=true、icon=@drawable/transparent、label=\"\" 的隐藏 Activity h，以及多处用空白字符拼接外发分隔符（c0c1c3a2c0c1c、fxf0x4x4x0fxf）规避字符串特征；未见伪造 isAccessibilityTool 或多 activity-alias。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "yps.eton.application.M（LAUNCHER，Theme.Translucent.NoTitleBar，layout activity_m.xml 仅 <x/>）",
      "trigger_event": "用户点击桌面图标 → Activity.onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（布局为空 <x />，窗口全透明，无任何文案）",
      "shown_text_zh": "界面完全空白透明，用户看不到任何提示或说明",
      "user_action_requested": "无任何可交互控件，无按钮、无取消、无跳过",
      "code_anchor": "yps.eton.application.M#onCreate / res/layout/activity_m.xml / res/values/strings.xml(app_name=null)"
    },
    {
      "step": 2,
      "stage": "引导说明页（缺失）",
      "screen_or_component": "无对应组件：全包不存在引导页、弹窗、WebView 或 HTML 资源",
      "trigger_event": "不适用——未实现任何说明或索取理由环节",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "不存在任何无障碍用途说明或隐私告知",
      "user_action_requested": "无",
      "code_anchor": "res/values/strings.xml 仅含 abc_* 与 8 条业务键，无任何说明文案"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "yps.eton.application.M#a() → 系统设置 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "group_properties.charAt(6)=='1' 时，onCreate 走 a()（charAt(4)=='0' 分支）或 onActivityResult 无条件回调 a()，在 super.onBackPressed() 后 startActivity(NEW_TASK)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "intent.setAction(\"android.settings.ACCESSIBILITY_SETTINGS\");",
      "shown_text_zh": "直接打开系统无障碍服务设置页，列表中出现一个名为 null 的服务项",
      "user_action_requested": "要求用户在系统列表中自行找到并开启名为 null 的无障碍服务；跳转本身无确认框",
      "code_anchor": "yps.eton.application.M#a"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "yps.eton.application.M#onActivityResult（设备管理员请求返回）",
      "trigger_event": "ADD_DEVICE_ADMIN 的 startActivityForResult(…,100) 返回，或任意结果码",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "if (i2 == -1) { a(); } else { a(); } finish();",
      "shown_text_zh": "无论用户同意还是拒绝设备管理员，均再次调用 a() 进入无障碍设置页并结束自身",
      "user_action_requested": "无取消/拒绝后停留的降级路径；拒绝即被再次送往无障碍设置",
      "code_anchor": "yps.eton.application.M#onActivityResult"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "yps.eton.application.k（AccessibilityService，label=@string/service_name=null，无 android:description）",
      "trigger_event": "系统回调 onServiceConnected → setServiceInfo(flags=89, eventTypes=-1)；随后每次 onAccessibilityEvent",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "accessibilityServiceInfo.flags = 89; accessibilityServiceInfo.eventTypes = -1;",
      "shown_text_zh": "注册包含非重要视图、增强 Web 无障碍、上报视图 ID、获取交互窗口的全事件监听；把每个界面的全部文本、包名、时间写入私有 config<日期>.log，A.i 为真时经 socket 外发到 assdsiwi.ddns.net:1515",
      "user_action_requested": "无需再操作，权限在后台持续生效",
      "code_anchor": "yps.eton.application.k#onServiceConnected / yps.eton.application.k#onAccessibilityEvent / yps.eton.application.k#a(String,Context)"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：仅显示字符串 \"null\"（service_name），且未声明 android:description，无任何用途说明",
    "桌面启动器图标名称：仅显示 \"null\"（app_name）",
    "应用内：无任何呈现位置——activity_m.xml 为空布局 <x/>，不存在 AlertDialog、引导 Activity、assets HTML、WebView 或悬浮窗",
    "跳转系统设置后：不叠加任何遮罩或悬浮引导层，用户面对的是原生设置页"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "null",
      "text_zh": "空值字面量（非有效名称，界面显示为 null）",
      "source_location": "res/values/strings.xml key=app_name",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "null",
      "text_zh": "空值字面量（系统无障碍服务列表项显示为 null）",
      "source_location": "res/values/strings.xml key=service_name",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "00000000",
      "text_zh": "八位行为开关，默认全关（无障碍跳转位 charAt(6) 为 0，即默认不跳转）",
      "source_location": "res/values/strings.xml key=group_properties",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "assdsiwi.ddns.net,1515",
      "text_zh": "C2 主机与端口（Socket 直连，非界面文案）",
      "source_location": "res/values/strings.xml key=host",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "无 onResume 轮询式死循环；但 onActivityResult 的 if/else 双分支均调用 a()，即用户拒绝设备管理员授权后仍被立即送入无障碍设置页并 finish() 自身；另有 charAt(7)=='1' 时 AlarmManager 每 180000ms 重复拉起 Z 广播接收器的后台再激活通道（Z 的具体行为本轮未展开）",
    "overlay_or_fake_settings": "无。未使用 SYSTEM_ALERT_WINDOW 叠层引导，也未伪造高仿无障碍开关页，直接跳转系统原生设置页",
    "restricted_settings_13plus_coaching": "无。未使用 ACTION_APPLICATION_DETAILS_SETTINGS，无“右上角菜单允许受限设置”教学，无 Session 安装器绕过；targetSdkVersion=22 且无对应引导",
    "post_grant_anti_removal": "未发现监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权的逻辑；但同包声明 DEVICE_ADMIN 接收器（yps.eton.application.D + res/xml/device_admin.xml）并在 charAt(4)!='0' 时申请激活设备管理员，构成独立的抗卸载/抗清除通道",
    "benign_graceful_degradation": "无。拒绝授权后既无降级模式也无手动替代路径"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 yps.eton.application.M 启动后 0.5s 内伴随 Activity 切换到 com.android.settings/.accessibility.AccessibilitySettings（或 intent=android.settings.ACCESSIBILITY_SETTINGS）的瞬间，同时抓取系统无障碍列表首屏",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动入口（全透明空壳页）",
        "page_identifier": "yps.eton.application.M，Theme.Translucent.NoTitleBar，根布局无可见子节点",
        "why_most_useful": "证明应用未提供任何说明即直接跳转，是区分诱导式申请与良性透明告知的第一判据",
        "observable_utg_signals": ["启动后 Activity 树为空/无可见文本节点", "Activity 存在时长极短（<1s）随即发生跳转", "无任何对话框或权限理由弹窗"]
      },
      {
        "page_role": "系统无障碍服务列表项（关键辨识页）",
        "page_identifier": "com.android.settings 无障碍服务列表中显示名称为 null 的条目",
        "why_most_useful": "直接暴露 app_name/service_name=null 的身份伪装与缺失 android:description，是本样本最具区分度的可见特征",
        "observable_utg_signals": ["列表项文本为 \"null\"", "该条目无副标题/用途说明文本", "紧邻列表项的应用包名为 yps.eton.application"]
      },
      {
        "page_role": "设备管理员授权页（拒权后强制再跳转的观察点）",
        "page_identifier": "android.app.action.ADD_DEVICE_ADMIN 对应系统页，随后回到 M#onActivityResult",
        "why_most_useful": "用于验证拒绝授权后仍被强制送往无障碍设置的行为，构成无取消路径证据",
        "observable_utg_signals": ["设备管理员页返回后立即出现 ACCESSIBILITY_SETTINGS 跳转", "无论点击取消或激活，后续页面序列一致"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在三点盲区：(1) 无障碍跳转受 group_properties 第 7 位控制，默认值 \"00000000\" 下不触发，若仅按默认配置运行会完全漏检，需先确认实际下发的配置串；(2) 二阶段载荷 res/raw/google.apk 在本样本中为 0 字节，UTG 无法观测到 APK 投递与安装页，只能看到逻辑存在；(3) 获权后的外发走原始 Socket 到 assdsiwi.ddns.net:1515，非常规 HTTP，常规流量层抓包难以解析内容，需配合文件系统侧 config<日期>.log 取证。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED"
  ],
  "code_anchors": [
    "yps.eton.application.M#onCreate",
    "yps.eton.application.M#a",
    "yps.eton.application.M#onActivityResult",
    "yps.eton.application.k#onServiceConnected",
    "yps.eton.application.k#onAccessibilityEvent",
    "res/values/strings.xml"
  ]
}
```

</details>
