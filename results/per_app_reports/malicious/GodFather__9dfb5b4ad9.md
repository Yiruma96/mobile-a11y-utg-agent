# MB_096__9dfb5b4ad9｜GodFather — Android Protect

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：154.1s

## 1. 一句话核心结论

- **核心申请方式**：以'Android Protect'全盘复刻Google Play Protect扫描页（未发现有害应用+Scan按钮），点击即读取enabled_accessibility_services判定未授权并深链ACCESSIBILITY_SETTINGS直接定位到com.spotify.music.InputService条目，后台服务与15秒定时器持续重跳催办，授权后即建立WebSocket远控通道。
- **静态可见性说明**：无障碍诱导全链路（入口Activity→仿Play Protect布局→checkAccess→ACCESSIBILITY_SETTINGS深链→后台服务/15秒定时重复拉起）均以明文Java/资源静态可见；唯一非静态项为引导Toast文案，取自SharedPreferences键StringAccessibility（由elsewardsreacquaintance.DefaultVariable从混淆字符串表quasirespectablefarsounding写入，可被远程覆盖），其余资源未发现加壳/AES/远端HTML。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `9dfb5b4ad9aac36c2d7fbb93f8668faa819cb0df16f4a55d00f1cdda89c9a6d2` |
| 包名 / 年份 | `com.infosoft.docutain` / 2023 |
| 家族 / 品类 | **GodFather**（同池样本数：11） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Android Protect |
| 引导页宣称品牌/身份 | Google Play Protect / Android 官方安全扫描（Google 品牌） |
| 系统无障碍列表服务名 | Android Protect |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务类置于com.spotify.music命名空间并复用开源VNC输入服务残留资源；服务android:label取@string/app_name即'Android Protect'；serviceconfig.xml无android:description（系统列表不展示任何风险说明）；settingsActivity指向外来占位类com.example.root.myapplication.MainActivity；存在label=""且excludeFromRecents的辅助Activity（levolacticEscanaba）；类名/字段名整体随机化并含控制流平坦化（hashCode开关跳转） |
| 无障碍服务类名 | `com.spotify.music.InputService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_CONTACTS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.infosoft.docutain.datamediaGrenadian（LAUNCHER Activity，Theme.AppCompat.NoActionBar） | onCreate：setContentView(2131361822) 后立即 startActivity(enfirehorseplays, class=HOME)，并启动 transectionhipjoint、cuveeacquiescence 前台服务与 startAlarm(15000) | 原生Activity | **原文**：Android Protect / No harmful apps found / Android protect hasn't scanned yet. / Scan / Recently scanned apps / +20 more / Apps have not been scanned yet. / Android Protect regularly checks your apps and device for harmful behavior. You'll be notified of any security risks found. / Learn more<br>**译注**：标题「Android Protect」；「未发现有害应用」；「Android Protect 尚未扫描」；按钮「扫描」；「最近扫描的应用」「+20 个更多」「应用尚未扫描」；「Android Protect 会定期检查您的应用与设备是否存在有害行为，发现安全风险会通知您」；「了解更多」 | 点击绿色「Scan」按钮；页面左上角另有返回箭头（back），无跳过/取消流程的显式文案 | `com.infosoft.docutain.datamediaGrenadian.onCreate + res/layout/activity_play.xml` |
| 2 | 业务功能触发 | Scan 按钮监听器 datamediaGrenadian$3 → elsewardsreacquaintance.checkAccess | onClick：先 checkAccess(getApplicationContext()) 读取 Settings.Secure.enabled_accessibility_services 判断是否 contains(getPackageName()) | 原生Activity | **原文**：无（点击后无任何真实扫描动作，仅做权限状态判断）<br>**译注**：无界面反馈，直接进入权限判断分支 | 用户以为触发安全扫描，实际被转入无障碍授权判定 | `com.infosoft.docutain.datamediaGrenadian$3.onClick / com.infosoft.docutain.elsewardsreacquaintance.checkAccess` |
| 3 | 跳无障碍设置 | datamediaGrenadian.access_intent → 系统 android.settings.ACCESSIBILITY_SETTINGS（三星机型先试 com.samsung.accessibility.installed_service） | checkAccess 返回 false 时由 onClick 调用 access_intent；设置页通过 :settings:fragment_args_key 深链定位到目标服务 | 系统无障碍页 | **原文**：Intent 携带 ":settings:fragment_args_key" = "com.infosoft.docutain/com.spotify.music.InputService"；Toast 文本 = PRead("StringAccessibility") + " 'Android Protect'"<br>**译注**：系统无障碍设置页自动滚动并高亮到列表项「Android Protect」，同时屏幕中央 Toast 提示（内容为远程下发的引导语 + 应用名 'Android Protect'） | 在系统无障碍列表中打开「Android Protect」服务开关；系统页本身无跳过按钮，用户需自行返回 | `com.infosoft.docutain.datamediaGrenadian.access_intent / res/xml/serviceconfig.xml` |
| 4 | 拒权反馈循环 | com.infosoft.docutain.Services.transectionhipjoint$1（后台 Service 线程）+ elsewardsreacquaintance.startAlarm(15000) | 后台 run() 反复 checkAccess；未授权时按 DEVICE()==0/1/2/3 与 HUW_VERSION() 分支，重复 new Intent("android.settings.ACCESSIBILITY_SETTINGS").setFlags(0x10000000) 并 startActivity，同时 sendNotification 催办 | 系统无障碍页 | **原文**：Intent("android.settings.ACCESSIBILITY_SETTINGS")；Toast = PRead("StringAccessibility") + " 'Android Protect'"<br>**译注**：用户返回或未开启时，后台再次把系统无障碍设置页顶到前台并重复弹 Toast，形成持续催办；15 秒定时器保证冷启动后周期性触发 | 反复要求用户回到设置页打开无障碍开关，无取消路径 | `com.infosoft.docutain.Services.transectionhipjoint$1.run / com.infosoft.docutain.datamediaGrenadian.onCreate` |
| 5 | 获权后动作 | com.spotify.music.InputService（AccessibilityService，onServiceConnected/onAccessibilityEvent/onKeyEvent/onPointerEvent） | 系统绑定服务后 onServiceConnected 初始化，静态字段 WebSocketConnection f4717d53e 等（TAG "Grabber"）建立远控通道 | 不可静态还原 | **原文**：无界面；服务标签仅 "Android Protect"，无 android:description<br>**译注**：授权后无任何界面提示，直接进入后台窗口读取与手势注入通道状态 | 无需用户操作，权限已静默生效 | `com.spotify.music.InputService.onServiceConnected / res/xml/serviceconfig.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- datamediaGrenadian 启动页（res/layout/activity_play.xml）原生 TextView："Android Protect"、"No harmful apps found"、"Android protect hasn't scanned yet."、"Recently scanned apps"、"+20 more"、"Apps have not been scanned yet."、"Android Protect regularly checks your apps and device for harmful behavior..."、"Learn more"
- 同一布局 GifImageView（drawable 2131099748）+ guard1~guard6 图标组成的"已扫描应用"伪造列表
- 按钮文案 "Scan"（res/layout/activity_play.xml，id/scan）与 "CONTINUE"（strings.xml key=button）
- 跳转系统无障碍页后居中 Toast：PRead("StringAccessibility") + " 'Android Protect'"（datamediaGrenadian.access_intent、necessarianencyclopedia.access_intent、transectionhipjoint$1.run 三处一致）
- 系统无障碍服务列表项名称：@string/app_name = "Android Protect"（服务无 android:description，列表内不呈现任何权限说明）
- strings.xml 中遗留的开源 VNC 输入服务文案（input_a11y_title "Accessibility disabled"、input_a11y_msg "To be able to remotely control your device, you need to enable accessibility..."）——未被本流程引用，属代码复用残留
- 未发现本地或远端 HTML/WebView 引导页、未发现悬浮窗遮罩引导（assets 目录仅 fonts）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Android Protect | Android 保护 | `res/values/strings.xml key=app_name；res/layout/activity_play.xml id/store` | 假反诈安全 |
| en | No harmful apps found | 未发现有害应用 | `res/layout/activity_play.xml id/textNoHarm` | 假反诈安全 |
| en | Android Protect regularly checks your apps and device for harmful behavior. You'll be notified of any security risks found. | Android Protect 会定期检查您的应用与设备是否存在有害行为，发现任何安全风险都会通知您。 | `res/layout/activity_play.xml id/textDetails` | 假反诈安全 |
| en | Android protect hasn't scanned yet. | Android Protect 尚未进行扫描。 | `res/layout/activity_play.xml id/textScanned` | 故障恐吓 |
| en | Apps have not been scanned yet. | 这些应用尚未被扫描。 | `res/layout/activity_play.xml id/textSmallScanned` | 故障恐吓 |
| en | Scan | 扫描 | `res/layout/activity_play.xml id/scan` | 清理工具伪装 |
| en | Accessibility disabled | 无障碍未启用 | `res/values/strings.xml key=input_a11y_title（开源 VNC 残留，流程未直接引用）` | 未知 |
| en | To be able to remotely control your device, you need to enable accessibility for. Do you want to enable accessibility now? | 为了能够远程控制您的设备，您需要为其启用无障碍功能。您是否现在启用无障碍？ | `res/values/strings.xml key=input_a11y_msg（开源 VNC 残留，流程未直接引用）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`shallow_1_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：后台服务 transectionhipjoint$1.run 与 startAlarm 15 秒定时任务持续 checkAccess；未授权即重新构造同一 ACCESSIBILITY_SETTINGS 深链 startActivity（FLAG_ACTIVITY_NEW_TASK），并按 DEVICE()/HUW_VERSION() 机型分支差异化处理，配合 sendNotification 通知栏催办，用户返回应用后仍会被再次顶到设置页
- **遮罩叠层 / 高仿系统设置页**：未发现悬浮窗引导遮罩或高仿系统无障碍开关页；采用真实系统无障碍页 + :settings:fragment_args_key 深链精准定位 + 居中 Toast 组合，SYSTEM_ALERT_WINDOW 权限已申请但引导流程未使用
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdk 31，流程未涉及应用详情页受限设置教学；另存在 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、ACTION_NOTIFICATION_LISTENER_SETTINGS、MANAGE_OVERLAY_PERMISSION 分步申请逻辑，但无 13+ 受限设置文案教学）
- **获权后即时行为与防撤权机制**：未发现自点确认或 GLOBAL_ACTION_BACK/HOME 阻止撤权；但存在设备管理器接收器（BIND_DEVICE_ADMIN + res/xml/devad）与 Postdiocletiannonserious 中针对 com.android.settings:id/switch_widget、switch_text、action_button 的控件定位逻辑，具备在设置页自动点击开关的能力
- **良性降级 / 替代方案**：无（点击 Scan 后无任何替代路径或降级模式，唯一分支是权限判断与重复跳转）

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS（或 com.samsung.accessibility.installed_service）且 Intent extras 含键 :settings:fragment_args_key 时立即截图；其次为冷启动进入 com.infosoft.docutain.datamediaGrenadian 时对 activity_play 布局截图（含 Scan 按钮与「No harmful apps found」）
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无明显盲区：引导文字全部为原生 TextView/Toast 可被 UTG 直接读取，无图片化文本、无 WebView 远端页面、无加壳。需注意两点：1) 引导 Toast 文案由远程配置 StringAccessibility 决定，首次运行可能为空或为本地兜底；2) 后台重复拉起按 DEVICE()/HUW_VERSION() 分支差异化，部分机型可能仅走通知栏催办而不直接跳设置页，建议同时监听通知与 Activity 栈变化。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动伪装扫描页** | com.infosoft.docutain.datamediaGrenadian，白色背景 ConstraintLayout，标题 Android Protect + GIF + 「No harmful apps found」+ 绿色 Scan 按钮 | 该页是仿冒 Google Play Protect 的核心载体，页面文案与实际零扫描行为直接构成虚假安全功能证据 | 文本节点 No harmful apps found；文本节点 Scan；文本节点 Android Protect；无任何进度/扫描结果控件 |
| **跳转后系统无障碍列表定位页** | com.android.settings 无障碍服务列表，列表项名称 Android Protect（无副标题说明） | 可确认深链 fragment_args_key 生效导致列表自动滚动/高亮到目标服务，且该项无 android:description，用户无法获知真实风险 | 包名 com.android.settings 出现在前台；列表项文本 Android Protect 且无描述文本；开关控件 resource-id switch_widget/switch_text |
| **居中引导 Toast** | Toast 窗口（gravity CENTER，包名 com.infosoft.docutain），文本形如 <远程引导语> 'Android Protect' | Toast 文案来自远程配置 StringAccessibility，是判定云端可控引导文案的唯一动态证据点 | Toast 文本含 Android Protect 引号包裹；Toast 出现在无障碍设置页之上；同一 Toast 在后台重复拉起时再次出现 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.infosoft.docutain.datamediaGrenadian.onCreate`
- `com.infosoft.docutain.datamediaGrenadian.access_intent`
- `com.infosoft.docutain.datamediaGrenadian$3.onClick`
- `com.infosoft.docutain.elsewardsreacquaintance.checkAccess`
- `com.infosoft.docutain.Services.transectionhipjoint$1.run`
- `res/xml/serviceconfig.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论

**静态可见性：clear**。引导流程全程静态可还原，未发现加壳、VMP 或加密载荷；仅引导 Toast 文案来自远程可写配置（`PRead("StringAccessibility")`），逐字内容不在资源中固定。

**核心链条（4 段）**

1. **仿冒身份**：LAUNCHER 入口 [datamediaGrenadian](<resource-unit:#1.dex1 code:com.infosoft.docutain.datamediaGrenadian#onCreate>) 加载 [activity_play.xml](<resource-unit:#1 file:res/layout/activity_play.xml>)，页面标题、图标、GIF、文案逐字模仿 Google Play Protect：「Android Protect」「No harmful apps found」「Android Protect regularly checks your apps and device for harmful behavior.」「Scan」。`app_name` 亦为 `Android Protect`。
2. **点击即跳转**：[onClick](<resource-unit:#1.dex1 code:com.infosoft.docutain.datamediaGrenadian$3#onClick>) → [checkAccess](<resource-unit:#1.dex1 code:com.infosoft.docutain.elsewardsreacquaintance#checkAccess>) 读取 `Settings.Secure."enabled_accessibility_services"` 并判断是否含本包名 → 未授权则 [access_intent](<resource-unit:#1.dex1 code:com.infosoft.docutain.datamediaGrenadian#access_intent>)。
3. **深链精准定位**：优先 `com.samsung.accessibility.installed_service`，否则 `android.settings.ACCESSIBILITY_SETTINGS`，并塞入 `:settings:fragment_args_key` = `com.infosoft.docutain/com.spotify.music.InputService`，使系统设置页**直接滚动并高亮到该服务开关项**；随后弹居中 Toast（`远程文案 + " 'Android Protect'"`，`2131492891` = `app_name`）。
4. **拒权循环 + 获权后远控**：`datamediaGrenadian.onCreate` 启动 `transectionhipjoint`、`cuveeacquiescence` 前台服务与 `startAlarm(15000)` 定时任务；[transectionhipjoint$1.run](<resource-unit:#1.dex1 code:com.infosoft.docutain.Services.transectionhipjoint$1#run>) 反复 `checkAccess` 并按 `DEVICE()`/`HUW_VERSION()` 机型分支重复拉起同一深链设置页。授权后 `InputService` 持有 4 个静态 `WebSocketConnection` 字段（TAG `Grabber`），即远程指令通道。

**身份混淆要点**
- 无障碍服务类位于 `com.spotify.music.InputService` 命名空间，复用开源 VNC 输入服务残留（`input_a11y_*` 字符串、`settings_port 5900`、`settings_password "123"`），但列表标签取 `@string/app_name` = **Android Protect**。
- [serviceconfig.xml](<resource-unit:#1 file:res/xml/serviceconfig.xml>) **无 `android:description`**（系统列表不给用户任何风险说明），`settingsActivity` 指向外来占位类 `com.example.root.myapplication.MainActivity`；能力却含 `canRetrieveWindowContent`、`canPerformGestures`、`flagRetrieveInteractiveWindows`。
- 另有 `levolacticEscanaba`（`label=""`、`excludeFromRecents`、`singleTask`）等空名 Activity 作为辅助隐藏页。

**UTG 捕获建议**：在检测到 `ACCESSIBILITY_SETTINGS` 启动且 extras 含 `:settings:fragment_args_key` 时立即截图，此时系统页已定位到 `Android Protect` 条目，是最强判别点。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍诱导全链路（入口Activity→仿Play Protect布局→checkAccess→ACCESSIBILITY_SETTINGS深链→后台服务/15秒定时重复拉起）均以明文Java/资源静态可见；唯一非静态项为引导Toast文案，取自SharedPreferences键StringAccessibility（由elsewardsreacquaintance.DefaultVariable从混淆字符串表quasirespectablefarsounding写入，可被远程覆盖），其余资源未发现加壳/AES/远端HTML。",
  "summary_one_liner": "以'Android Protect'全盘复刻Google Play Protect扫描页（未发现有害应用+Scan按钮），点击即读取enabled_accessibility_services判定未授权并深链ACCESSIBILITY_SETTINGS直接定位到com.spotify.music.InputService条目，后台服务与15秒定时器持续重跳催办，授权后即建立WebSocket远控通道。",
  "disguise_identity": {
    "app_display_name": "Android Protect",
    "claimed_brand_or_persona": "Google Play Protect / Android 官方安全扫描（Google 品牌）",
    "a11y_service_label": "Android Protect",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务类置于com.spotify.music命名空间并复用开源VNC输入服务残留资源；服务android:label取@string/app_name即'Android Protect'；serviceconfig.xml无android:description（系统列表不展示任何风险说明）；settingsActivity指向外来占位类com.example.root.myapplication.MainActivity；存在label=\"\"且excludeFromRecents的辅助Activity（levolacticEscanaba）；类名/字段名整体随机化并含控制流平坦化（hashCode开关跳转）"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.infosoft.docutain.datamediaGrenadian（LAUNCHER Activity，Theme.AppCompat.NoActionBar）",
      "trigger_event": "onCreate：setContentView(2131361822) 后立即 startActivity(enfirehorseplays, class=HOME)，并启动 transectionhipjoint、cuveeacquiescence 前台服务与 startAlarm(15000)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Android Protect / No harmful apps found / Android protect hasn't scanned yet. / Scan / Recently scanned apps / +20 more / Apps have not been scanned yet. / Android Protect regularly checks your apps and device for harmful behavior. You'll be notified of any security risks found. / Learn more",
      "shown_text_zh": "标题「Android Protect」；「未发现有害应用」；「Android Protect 尚未扫描」；按钮「扫描」；「最近扫描的应用」「+20 个更多」「应用尚未扫描」；「Android Protect 会定期检查您的应用与设备是否存在有害行为，发现安全风险会通知您」；「了解更多」",
      "user_action_requested": "点击绿色「Scan」按钮；页面左上角另有返回箭头（back），无跳过/取消流程的显式文案",
      "code_anchor": "com.infosoft.docutain.datamediaGrenadian.onCreate + res/layout/activity_play.xml"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "Scan 按钮监听器 datamediaGrenadian$3 → elsewardsreacquaintance.checkAccess",
      "trigger_event": "onClick：先 checkAccess(getApplicationContext()) 读取 Settings.Secure.enabled_accessibility_services 判断是否 contains(getPackageName())",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（点击后无任何真实扫描动作，仅做权限状态判断）",
      "shown_text_zh": "无界面反馈，直接进入权限判断分支",
      "user_action_requested": "用户以为触发安全扫描，实际被转入无障碍授权判定",
      "code_anchor": "com.infosoft.docutain.datamediaGrenadian$3.onClick / com.infosoft.docutain.elsewardsreacquaintance.checkAccess"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "datamediaGrenadian.access_intent → 系统 android.settings.ACCESSIBILITY_SETTINGS（三星机型先试 com.samsung.accessibility.installed_service）",
      "trigger_event": "checkAccess 返回 false 时由 onClick 调用 access_intent；设置页通过 :settings:fragment_args_key 深链定位到目标服务",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Intent 携带 \":settings:fragment_args_key\" = \"com.infosoft.docutain/com.spotify.music.InputService\"；Toast 文本 = PRead(\"StringAccessibility\") + \" 'Android Protect'\"",
      "shown_text_zh": "系统无障碍设置页自动滚动并高亮到列表项「Android Protect」，同时屏幕中央 Toast 提示（内容为远程下发的引导语 + 应用名 'Android Protect'）",
      "user_action_requested": "在系统无障碍列表中打开「Android Protect」服务开关；系统页本身无跳过按钮，用户需自行返回",
      "code_anchor": "com.infosoft.docutain.datamediaGrenadian.access_intent / res/xml/serviceconfig.xml"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "com.infosoft.docutain.Services.transectionhipjoint$1（后台 Service 线程）+ elsewardsreacquaintance.startAlarm(15000)",
      "trigger_event": "后台 run() 反复 checkAccess；未授权时按 DEVICE()==0/1/2/3 与 HUW_VERSION() 分支，重复 new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\").setFlags(0x10000000) 并 startActivity，同时 sendNotification 催办",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Intent(\"android.settings.ACCESSIBILITY_SETTINGS\")；Toast = PRead(\"StringAccessibility\") + \" 'Android Protect'\"",
      "shown_text_zh": "用户返回或未开启时，后台再次把系统无障碍设置页顶到前台并重复弹 Toast，形成持续催办；15 秒定时器保证冷启动后周期性触发",
      "user_action_requested": "反复要求用户回到设置页打开无障碍开关，无取消路径",
      "code_anchor": "com.infosoft.docutain.Services.transectionhipjoint$1.run / com.infosoft.docutain.datamediaGrenadian.onCreate"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "com.spotify.music.InputService（AccessibilityService，onServiceConnected/onAccessibilityEvent/onKeyEvent/onPointerEvent）",
      "trigger_event": "系统绑定服务后 onServiceConnected 初始化，静态字段 WebSocketConnection f4717d53e 等（TAG \"Grabber\"）建立远控通道",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无界面；服务标签仅 \"Android Protect\"，无 android:description",
      "shown_text_zh": "授权后无任何界面提示，直接进入后台窗口读取与手势注入通道状态",
      "user_action_requested": "无需用户操作，权限已静默生效",
      "code_anchor": "com.spotify.music.InputService.onServiceConnected / res/xml/serviceconfig.xml"
    }
  ],
  "text_presentation_locations": [
    "datamediaGrenadian 启动页（res/layout/activity_play.xml）原生 TextView：\"Android Protect\"、\"No harmful apps found\"、\"Android protect hasn't scanned yet.\"、\"Recently scanned apps\"、\"+20 more\"、\"Apps have not been scanned yet.\"、\"Android Protect regularly checks your apps and device for harmful behavior...\"、\"Learn more\"",
    "同一布局 GifImageView（drawable 2131099748）+ guard1~guard6 图标组成的\"已扫描应用\"伪造列表",
    "按钮文案 \"Scan\"（res/layout/activity_play.xml，id/scan）与 \"CONTINUE\"（strings.xml key=button）",
    "跳转系统无障碍页后居中 Toast：PRead(\"StringAccessibility\") + \" 'Android Protect'\"（datamediaGrenadian.access_intent、necessarianencyclopedia.access_intent、transectionhipjoint$1.run 三处一致）",
    "系统无障碍服务列表项名称：@string/app_name = \"Android Protect\"（服务无 android:description，列表内不呈现任何权限说明）",
    "strings.xml 中遗留的开源 VNC 输入服务文案（input_a11y_title \"Accessibility disabled\"、input_a11y_msg \"To be able to remotely control your device, you need to enable accessibility...\"）——未被本流程引用，属代码复用残留",
    "未发现本地或远端 HTML/WebView 引导页、未发现悬浮窗遮罩引导（assets 目录仅 fonts）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Android Protect",
      "text_zh": "Android 保护",
      "source_location": "res/values/strings.xml key=app_name；res/layout/activity_play.xml id/store",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "No harmful apps found",
      "text_zh": "未发现有害应用",
      "source_location": "res/layout/activity_play.xml id/textNoHarm",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Android Protect regularly checks your apps and device for harmful behavior. You'll be notified of any security risks found.",
      "text_zh": "Android Protect 会定期检查您的应用与设备是否存在有害行为，发现任何安全风险都会通知您。",
      "source_location": "res/layout/activity_play.xml id/textDetails",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Android protect hasn't scanned yet.",
      "text_zh": "Android Protect 尚未进行扫描。",
      "source_location": "res/layout/activity_play.xml id/textScanned",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Apps have not been scanned yet.",
      "text_zh": "这些应用尚未被扫描。",
      "source_location": "res/layout/activity_play.xml id/textSmallScanned",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Scan",
      "text_zh": "扫描",
      "source_location": "res/layout/activity_play.xml id/scan",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility disabled",
      "text_zh": "无障碍未启用",
      "source_location": "res/values/strings.xml key=input_a11y_title（开源 VNC 残留，流程未直接引用）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "To be able to remotely control your device, you need to enable accessibility for. Do you want to enable accessibility now?",
      "text_zh": "为了能够远程控制您的设备，您需要为其启用无障碍功能。您是否现在启用无障碍？",
      "source_location": "res/values/strings.xml key=input_a11y_msg（开源 VNC 残留，流程未直接引用）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "shallow_1_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "后台服务 transectionhipjoint$1.run 与 startAlarm 15 秒定时任务持续 checkAccess；未授权即重新构造同一 ACCESSIBILITY_SETTINGS 深链 startActivity（FLAG_ACTIVITY_NEW_TASK），并按 DEVICE()/HUW_VERSION() 机型分支差异化处理，配合 sendNotification 通知栏催办，用户返回应用后仍会被再次顶到设置页",
    "overlay_or_fake_settings": "未发现悬浮窗引导遮罩或高仿系统无障碍开关页；采用真实系统无障碍页 + :settings:fragment_args_key 深链精准定位 + 居中 Toast 组合，SYSTEM_ALERT_WINDOW 权限已申请但引导流程未使用",
    "restricted_settings_13plus_coaching": "无（targetSdk 31，流程未涉及应用详情页受限设置教学；另存在 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、ACTION_NOTIFICATION_LISTENER_SETTINGS、MANAGE_OVERLAY_PERMISSION 分步申请逻辑，但无 13+ 受限设置文案教学）",
    "post_grant_anti_removal": "未发现自点确认或 GLOBAL_ACTION_BACK/HOME 阻止撤权；但存在设备管理器接收器（BIND_DEVICE_ADMIN + res/xml/devad）与 Postdiocletiannonserious 中针对 com.android.settings:id/switch_widget、switch_text、action_button 的控件定位逻辑，具备在设置页自动点击开关的能力",
    "benign_graceful_degradation": "无（点击 Scan 后无任何替代路径或降级模式，唯一分支是权限判断与重复跳转）"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS（或 com.samsung.accessibility.installed_service）且 Intent extras 含键 :settings:fragment_args_key 时立即截图；其次为冷启动进入 com.infosoft.docutain.datamediaGrenadian 时对 activity_play 布局截图（含 Scan 按钮与「No harmful apps found」）",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动伪装扫描页",
        "page_identifier": "com.infosoft.docutain.datamediaGrenadian，白色背景 ConstraintLayout，标题 Android Protect + GIF + 「No harmful apps found」+ 绿色 Scan 按钮",
        "why_most_useful": "该页是仿冒 Google Play Protect 的核心载体，页面文案与实际零扫描行为直接构成虚假安全功能证据",
        "observable_utg_signals": ["文本节点 No harmful apps found", "文本节点 Scan", "文本节点 Android Protect", "无任何进度/扫描结果控件"]
      },
      {
        "page_role": "跳转后系统无障碍列表定位页",
        "page_identifier": "com.android.settings 无障碍服务列表，列表项名称 Android Protect（无副标题说明）",
        "why_most_useful": "可确认深链 fragment_args_key 生效导致列表自动滚动/高亮到目标服务，且该项无 android:description，用户无法获知真实风险",
        "observable_utg_signals": ["包名 com.android.settings 出现在前台", "列表项文本 Android Protect 且无描述文本", "开关控件 resource-id switch_widget/switch_text"]
      },
      {
        "page_role": "居中引导 Toast",
        "page_identifier": "Toast 窗口（gravity CENTER，包名 com.infosoft.docutain），文本形如 <远程引导语> 'Android Protect'",
        "why_most_useful": "Toast 文案来自远程配置 StringAccessibility，是判定云端可控引导文案的唯一动态证据点",
        "observable_utg_signals": ["Toast 文本含 Android Protect 引号包裹", "Toast 出现在无障碍设置页之上", "同一 Toast 在后台重复拉起时再次出现"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无明显盲区：引导文字全部为原生 TextView/Toast 可被 UTG 直接读取，无图片化文本、无 WebView 远端页面、无加壳。需注意两点：1) 引导 Toast 文案由远程配置 StringAccessibility 决定，首次运行可能为空或为本地兜底；2) 后台重复拉起按 DEVICE()/HUW_VERSION() 分支差异化，部分机型可能仅走通知栏催办而不直接跳设置页，建议同时监听通知与 Activity 栈变化。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_GIF_OR_IMAGE_GUIDE",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.infosoft.docutain.datamediaGrenadian.onCreate",
    "com.infosoft.docutain.datamediaGrenadian.access_intent",
    "com.infosoft.docutain.datamediaGrenadian$3.onClick",
    "com.infosoft.docutain.elsewardsreacquaintance.checkAccess",
    "com.infosoft.docutain.Services.transectionhipjoint$1.run",
    "res/xml/serviceconfig.xml"
  ]
}
```

</details>
