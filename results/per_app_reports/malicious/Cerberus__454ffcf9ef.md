# MB_071__454ffcf9ef｜Cerberus — Chrome

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：194.3s

## 1. 一句话核心结论

- **核心申请方式**：以 label=Chrome 的隐形无障碍服务（无 description）搭配加密资产 qAERL.json 在 Application 启动阶段反射装载二阶段载荷，引导弹窗与跳转无障碍设置的全部话术均在加密载荷内，静态仅能确认其伪装身份与读屏能力。
- **静态可见性说明**：声明层（Manifest 服务、能力 xml、标签）完全可见，但实现层完全不可见：Manifest 声明的无障碍服务 supreme.fee.merit.oxehxewpkoyayan 及全部 supreme.fee.merit.* 界面类在唯一 classes.dex 中零命中（二进制字符串计数为 0），实际代码藏于 677KB 高熵加密资产 assets/qAERL.json，由 Application.attachBaseContext 阶段经反射/字段注入与 Class.forName 装载并替换 Application，解密算法与密钥未在 DEX 明文中出现，静态无法还原任何引导文案或跳转逻辑。
- **命中的行为模式标签**：`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `454ffcf9ef438d5d3eee894d0b2f21326935857da76d5720a8dc0eeda8280f59` |
| 包名 / 年份 | `crack.base.hawk` / 2024 |
| 家族 / 品类 | **Cerberus**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Chrome |
| 引导页宣称品牌/身份 | Google Chrome 浏览器 |
| 系统无障碍列表服务名 | Chrome |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务 android:label="Chrome" 且完全没有 android:description，系统无障碍列表中不显示任何用途说明，警告文案被挤出；应用 label 同为 Chrome 但包名为 crack.base.hawk；全部类名/方法名为随机字母串（如 oxehxewpkoyayan、uktwfcvalo）；多个 label="" + Theme.NoDisplay + excludeFromRecents/noHistory 的隐形 Activity（tjzreoxto、axdimtlo、tukwybhoegzlkxj）用于无界面中转。 |
| 无障碍服务类名 | `supreme.fee.merit.oxehxewpkoyayan` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | supreme.fee.merit.uktwfcvalo（Manifest 声明 MAIN+LAUNCHER，另声明 android.app.role.SMS 角色） | 用户点击桌面图标启动；Application.attachBaseContext 先于该 Activity 执行完成载荷装载 | 不可静态还原 | 无 | 不可静态确认 | `crack.base.hawk.WPlHpDgOdIaFgTz.attachBaseContext / Manifest activity supreme.fee.merit.uktwfcvalo` |
| 2 | 引导说明页 | 载荷内引导界面（具体 Activity/Dialog/WebView 均不可静态还原） | 不可静态确认（载荷解密后自行决定，可能在冷启动 0 步或功能触发时） | 不可静态还原 | 无 | 不可静态确认 | `assets/qAERL.json（加密，未还原）` |
| 3 | 跳无障碍设置 | 系统设置 Settings.ACTION_ACCESSIBILITY_SETTINGS（预期，未在 DEX 中找到该字符串） | 不可静态确认 | 系统无障碍页 | **原文**：Chrome<br>**译注**：系统无障碍服务列表中将显示名为「Chrome」的服务项，无任何用途描述 | 要求用户手动打开该开关（是否为唯一路径不可静态确认） | `AndroidManifest.xml service supreme.fee.merit.oxehxewpkoyayan + res/xml/bgebtkpacvv.xml` |
| 4 | 获权后动作 | AccessibilityService 实例（canRetrieveWindowContent + flagReportViewIds） | 系统绑定服务后 onServiceConnected / onAccessibilityEvent（typeWindowContentChanged\|typeWindowStateChanged） | 不可静态还原 | 无 | 无 | `res/xml/bgebtkpacvv.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- AndroidManifest.xml：application android:label="Chrome"（桌面显示名）
- AndroidManifest.xml：无障碍服务 supreme.fee.merit.oxehxewpkoyayan 的 android:label="Chrome"（系统无障碍列表项名称，无 description）
- res/xml/bgebtkpacvv.xml：仅声明事件类型与 canRetrieveWindowContent，无任何说明文字
- 载荷层（assets/qAERL.json 解密后）：全部引导弹窗/Activity/WebView/悬浮窗文案均在此，静态不可见
- 包内无 assets 下的引导 HTML、无 strings.xml 明文（资源位于 resources.arsc），未发现任何明文无障碍教学文案

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Chrome | Chrome（谷歌浏览器） | `AndroidManifest.xml application android:label / service supreme.fee.merit.oxehxewpkoyayan android:label` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：跳转与重跳逻辑位于加密载荷内，DEX 中无 ACTION_ACCESSIBILITY_SETTINGS/ACTION_APPLICATION_DETAILS_SETTINGS 字符串，无法确认是否存在 onResume 死循环或定时器重跳
- **遮罩叠层 / 高仿系统设置页**：不可静态还原：未发现 GLOBAL_ACTION_BACK/HOME、TYPE_ACCESSIBILITY_OVERLAY、SYSTEM_ALERT_WINDOW 等明文字符串（Manifest 亦未申请 SYSTEM_ALERT_WINDOW），是否存在遮罩/高仿设置页无法静态判断
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdk=29，Manifest 未含相关线索；载荷层是否教学受限设置不可静态确认）
- **获权后即时行为与防撤权机制**：不可静态还原：已声明 DeviceAdmin receiver supreme.fee.merit.kmzdy（BIND_DEVICE_ADMIN，priority=136，监听 DEVICE_ADMIN_DISABLED/DISABLE_REQUESTED）、NotificationListenerService、BOOT_COMPLETED/SMS_RECEIVED 广播（priority=993）与多个 exported=true 的 Service，具备卸载对抗与开机复活通道，但获权后具体自保护动作在载荷内
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在冷启动包名 crack.base.hawk 首个非系统 Activity 出现的瞬间（预期为 supreme.fee.merit.uktwfcvalo 或其后的隐形中转 Activity），以及任何一次 Intent 跳转到 android.settings.ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 的瞬间拉起 UTG；建议同时 hook AccessibilityManagerService 的 enabled 状态变化以捕获获权瞬间界面。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：显著盲区：二阶段代码与全部引导文案位于加密资产 assets/qAERL.json，静态零文本；若载荷以纯图片/GIF 呈现引导（本样本具备 assets/tiles_*、大量 png/plist 资源），UTG 文本节点将为空，必须启用 OCR 与截图比对。另有无 description 导致的系统警告缺失，使系统页本身也不提供判别文本。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动首屏/引导说明页** | 包名 crack.base.hawk 的首个 Activity（声明为 supreme.fee.merit.uktwfcvalo），Theme.Translucent.NoTitleBar | 载荷解密后真正呈现的引导话术只在运行期存在，静态为零证据，这是唯一能取得诱导原文的入口 | 页面标题/正文文本（用于判定是否假更新、假安全、清理工具话术）；是否存在取消/返回/跳过按钮及其 enabled 属性；是否为 WebView 容器（可判断本地 HTML 还是远端 URL） |
| **跳转前教学/分步指引页** | 含「设置 → 无障碍 → Chrome」分步图示或半透明遮罩的界面 | 区分『一次性引导』与『分步教学 + 遮罩压栈』两种诱导强度，决定是否构成 COERCE_OVERLAY_STACK_ON_SETTINGS | 是否覆盖在系统设置之上（顶层窗口包名仍为 crack.base.hawk）；是否含 step 1/2/3 序号或箭头指示；是否出现「允许受限设置」相关文案 |
| **系统无障碍服务列表项** | Settings 页面中 label 为 Chrome 的条目 | 直接验证无 description 导致的警告挤出效果与用户可辨识度 | 条目文本仅为 Chrome、无副标题说明；开关状态变化时刻（获权瞬间） |
| **拒权/返回后反馈页** | 从系统设置返回后重新出现的 crack.base.hawk 界面 | 判定是否存在拒权反馈循环（onResume 重跳）这一强制型诱导特征 | 返回后 1-3 秒内是否再次跳转 ACCESSIBILITY_SETTINGS；界面是否变为不可取消弹窗 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `crack.base.hawk.WPlHpDgOdIaFgTz.attachBaseContext`
- `crack.base.hawk.DZzAiUuToMtEoLqHeLtRpMrKuLnXpCiSpItTnJoPeCxRmOe.littleriot`
- `crack.base.hawk.PHoXaTbQyEqWqXiMlWeAjTjLd.obtainfew`
- `crack.base.hawk.GNaYjTfEkItFqJl.magicdutch`
- `res/xml/bgebtkpacvv.xml`
- `assets/qAERL.json`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**静态可见性：packed_or_encrypted。** 无障碍权限引导的**全部运行期载体都不可静态还原**；只能确认“声明层”和“装载层”，无法看到“引导文案层”。

**已证实的声明层事实**
- 无障碍服务 [supreme.fee.merit.oxehxewpkoyayan](<resource-unit:#1 manifest:components>) 声明 `BIND_ACCESSIBILITY_SERVICE`，`android:label="Chrome"`，**没有 `android:description`**；系统无障碍列表里只会显示“Chrome”，没有任何用途说明，警告文案被完全挤掉。
- 服务能力配置文件 [res/xml/bgebtkpacvv.xml](<resource-unit:#1 file:res/xml/bgebtkpacvv.xml>)：`canRetrieveWindowContent="true"` + `typeWindowContentChanged|typeWindowStateChanged` + `flagReportViewIds`，即**读取任意前台窗口文本与控件 ID**（覆盖钓鱼与自动点击所需的全部能力）。
- 应用 `android:label="Chrome"`，包名却为 `crack.base.hawk`；`versionName=1.0`、`versionCode=1`、`targetSdk=29`，是典型快速拼装样本。
- Manifest 中还包含一批“隐形 Activity”：`tjzreoxto`（`label=""`、`Theme.NoDisplay`、`excludeFromRecents`）、`axdimtlo`/`tukwybhoegzlkxj`（`label=""`、`noHistory`/`NoDisplay`、共用同一 icon），这是投放/中转页的典型形态。
- Launcher Activity 为 `supreme.fee.merit.uktwfcvalo`（`MAIN` + `LAUNCHER`），另有 `android.app.role.SMS` 角色声明。

**已证实的装载层事实（为什么静态看不到引导）**
- 唯一 DEX（4.5 MB）中 `supreme`、`fee/merit`、`oxehxewpkoyayan`、`accessibilityservice`、`AccessibilityService` 字符串出现次数**均为 0**；`search_function_definitions` 对上述标识零命中——**Manifest 声明的服务类、Launcher Activity 在 DEX 里根本不存在**。
- [WPlHpDgOdIaFgTz.attachBaseContext()](<resource-unit:#1.dex1 code:crack.base.hawk.WPlHpDgOdIaFgTz#attachBaseContext>) 在 `super.attachBaseContext` 前后即调用 [GNaYjTfEkItFqJl.magicdutch()](<resource-unit:#1.dex1 code:crack.base.hawk.GNaYjTfEkItFqJl#magicdutch>) 与 [DZzAiUuToMtEoLqHeLtRpMrKuLnXpCiSpItTnJoPeCxRmOe.littleriot()](<resource-unit:#1.dex1 code:crack.base.hawk.DZzAiUuToMtEoLqHeLtRpMrKuLnXpCiSpItTnJoPeCxRmOe#littleriot>)；后者以 `Class.forName` + `getDeclaredField` + `setAccessible` + `WeakReference` 操作字段与类对象。
- [PHoXaTbQyEqWqXiMlWeAjTjLd.obtainfew()](<resource-unit:#1.dex1 code:crack.base.hawk.PHoXaTbQyEqWqXiMlWeAjTjLd#obtainfew>) 通过 `Class.forName(str, true, getClassLoader()).newInstance()` 实例化另一个 `Application` 并复制 `getApplicationContext()`——**壳式宿主接管**。
- `assets/qAERL.json` 为 677 KB **高熵二进制**（首字节 `DA FF 23 1A…`，非 JSON 明文），包内无任何明文配置/HTML 引导页；`assets/doc/*.htm` 仅为 QQ 同步/网络提示等第三方 SDK 残留。

**判断**：一阶段 Dropper + 加密二阶段。引导弹窗、跳转 `ACTION_ACCESSIBILITY_SETTINGS` 的 Intent、拒权循环、获权后自保护**全部位于 `qAERL.json` 解密后的内存 DEX 中**，`attachBaseContext` 阶段即完成还原，早于任何 UI 呈现，因此静态无法取得任何一句引导原文。UTG 检测必须在**运行期首个 Activity 出现与跳转系统无障碍页的瞬间**取证，静态审计到此为边界。

**未决与覆盖边界**：`qAERL.json` 的解密密钥/算法未在 DEX 明文中暴露（`assets/config` 目录不可读、无 `DexClassLoader`/`defineClass` 明文串，疑由 native 或反射拼接提供）；本次未做载荷静态还原，故引导话术、是否有取消按钮、拒权后是否 `onResume` 死循环、获权后是否用 `GLOBAL_ACTION_BACK` 阻止撤权均**无法从包内静态证据确认**，不作为已证实事实。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "声明层（Manifest 服务、能力 xml、标签）完全可见，但实现层完全不可见：Manifest 声明的无障碍服务 supreme.fee.merit.oxehxewpkoyayan 及全部 supreme.fee.merit.* 界面类在唯一 classes.dex 中零命中（二进制字符串计数为 0），实际代码藏于 677KB 高熵加密资产 assets/qAERL.json，由 Application.attachBaseContext 阶段经反射/字段注入与 Class.forName 装载并替换 Application，解密算法与密钥未在 DEX 明文中出现，静态无法还原任何引导文案或跳转逻辑。",
  "summary_one_liner": "以 label=Chrome 的隐形无障碍服务（无 description）搭配加密资产 qAERL.json 在 Application 启动阶段反射装载二阶段载荷，引导弹窗与跳转无障碍设置的全部话术均在加密载荷内，静态仅能确认其伪装身份与读屏能力。",
  "disguise_identity": {
    "app_display_name": "Chrome",
    "claimed_brand_or_persona": "Google Chrome 浏览器",
    "a11y_service_label": "Chrome",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务 android:label=\"Chrome\" 且完全没有 android:description，系统无障碍列表中不显示任何用途说明，警告文案被挤出；应用 label 同为 Chrome 但包名为 crack.base.hawk；全部类名/方法名为随机字母串（如 oxehxewpkoyayan、uktwfcvalo）；多个 label=\"\" + Theme.NoDisplay + excludeFromRecents/noHistory 的隐形 Activity（tjzreoxto、axdimtlo、tukwybhoegzlkxj）用于无界面中转。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "supreme.fee.merit.uktwfcvalo（Manifest 声明 MAIN+LAUNCHER，另声明 android.app.role.SMS 角色）",
      "trigger_event": "用户点击桌面图标启动；Application.attachBaseContext 先于该 Activity 执行完成载荷装载",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "该 Activity 实现类在 DEX 中不存在，界面内容由 qAERL.json 解密后的载荷决定，静态不可见",
      "user_action_requested": "不可静态确认",
      "code_anchor": "crack.base.hawk.WPlHpDgOdIaFgTz.attachBaseContext / Manifest activity supreme.fee.merit.uktwfcvalo"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "载荷内引导界面（具体 Activity/Dialog/WebView 均不可静态还原）",
      "trigger_event": "不可静态确认（载荷解密后自行决定，可能在冷启动 0 步或功能触发时）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "包内无任何明文引导文案；assets/doc/*.htm 仅为第三方 SDK 残留的网络提示页，非无障碍引导",
      "user_action_requested": "不可静态确认",
      "code_anchor": "assets/qAERL.json（加密，未还原）"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 Settings.ACTION_ACCESSIBILITY_SETTINGS（预期，未在 DEX 中找到该字符串）",
      "trigger_event": "不可静态确认",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Chrome",
      "shown_text_zh": "系统无障碍服务列表中将显示名为「Chrome」的服务项，无任何用途描述",
      "user_action_requested": "要求用户手动打开该开关（是否为唯一路径不可静态确认）",
      "code_anchor": "AndroidManifest.xml service supreme.fee.merit.oxehxewpkoyayan + res/xml/bgebtkpacvv.xml"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "AccessibilityService 实例（canRetrieveWindowContent + flagReportViewIds）",
      "trigger_event": "系统绑定服务后 onServiceConnected / onAccessibilityEvent（typeWindowContentChanged|typeWindowStateChanged）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "读取前台窗口全部文本与控件 ID，后续动作（覆盖、自动点击、自保护）在载荷内",
      "user_action_requested": "无",
      "code_anchor": "res/xml/bgebtkpacvv.xml"
    }
  ],
  "text_presentation_locations": [
    "AndroidManifest.xml：application android:label=\"Chrome\"（桌面显示名）",
    "AndroidManifest.xml：无障碍服务 supreme.fee.merit.oxehxewpkoyayan 的 android:label=\"Chrome\"（系统无障碍列表项名称，无 description）",
    "res/xml/bgebtkpacvv.xml：仅声明事件类型与 canRetrieveWindowContent，无任何说明文字",
    "载荷层（assets/qAERL.json 解密后）：全部引导弹窗/Activity/WebView/悬浮窗文案均在此，静态不可见",
    "包内无 assets 下的引导 HTML、无 strings.xml 明文（资源位于 resources.arsc），未发现任何明文无障碍教学文案"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Chrome",
      "text_zh": "Chrome（谷歌浏览器）",
      "source_location": "AndroidManifest.xml application android:label / service supreme.fee.merit.oxehxewpkoyayan android:label",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：跳转与重跳逻辑位于加密载荷内，DEX 中无 ACTION_ACCESSIBILITY_SETTINGS/ACTION_APPLICATION_DETAILS_SETTINGS 字符串，无法确认是否存在 onResume 死循环或定时器重跳",
    "overlay_or_fake_settings": "不可静态还原：未发现 GLOBAL_ACTION_BACK/HOME、TYPE_ACCESSIBILITY_OVERLAY、SYSTEM_ALERT_WINDOW 等明文字符串（Manifest 亦未申请 SYSTEM_ALERT_WINDOW），是否存在遮罩/高仿设置页无法静态判断",
    "restricted_settings_13plus_coaching": "无（targetSdk=29，Manifest 未含相关线索；载荷层是否教学受限设置不可静态确认）",
    "post_grant_anti_removal": "不可静态还原：已声明 DeviceAdmin receiver supreme.fee.merit.kmzdy（BIND_DEVICE_ADMIN，priority=136，监听 DEVICE_ADMIN_DISABLED/DISABLE_REQUESTED）、NotificationListenerService、BOOT_COMPLETED/SMS_RECEIVED 广播（priority=993）与多个 exported=true 的 Service，具备卸载对抗与开机复活通道，但获权后具体自保护动作在载荷内",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在冷启动包名 crack.base.hawk 首个非系统 Activity 出现的瞬间（预期为 supreme.fee.merit.uktwfcvalo 或其后的隐形中转 Activity），以及任何一次 Intent 跳转到 android.settings.ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 的瞬间拉起 UTG；建议同时 hook AccessibilityManagerService 的 enabled 状态变化以捕获获权瞬间界面。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动首屏/引导说明页",
        "page_identifier": "包名 crack.base.hawk 的首个 Activity（声明为 supreme.fee.merit.uktwfcvalo），Theme.Translucent.NoTitleBar",
        "why_most_useful": "载荷解密后真正呈现的引导话术只在运行期存在，静态为零证据，这是唯一能取得诱导原文的入口",
        "observable_utg_signals": ["页面标题/正文文本（用于判定是否假更新、假安全、清理工具话术）", "是否存在取消/返回/跳过按钮及其 enabled 属性", "是否为 WebView 容器（可判断本地 HTML 还是远端 URL）"]
      },
      {
        "page_role": "跳转前教学/分步指引页",
        "page_identifier": "含「设置 → 无障碍 → Chrome」分步图示或半透明遮罩的界面",
        "why_most_useful": "区分『一次性引导』与『分步教学 + 遮罩压栈』两种诱导强度，决定是否构成 COERCE_OVERLAY_STACK_ON_SETTINGS",
        "observable_utg_signals": ["是否覆盖在系统设置之上（顶层窗口包名仍为 crack.base.hawk）", "是否含 step 1/2/3 序号或箭头指示", "是否出现「允许受限设置」相关文案"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 页面中 label 为 Chrome 的条目",
        "why_most_useful": "直接验证无 description 导致的警告挤出效果与用户可辨识度",
        "observable_utg_signals": ["条目文本仅为 Chrome、无副标题说明", "开关状态变化时刻（获权瞬间）"]
      },
      {
        "page_role": "拒权/返回后反馈页",
        "page_identifier": "从系统设置返回后重新出现的 crack.base.hawk 界面",
        "why_most_useful": "判定是否存在拒权反馈循环（onResume 重跳）这一强制型诱导特征",
        "observable_utg_signals": ["返回后 1-3 秒内是否再次跳转 ACCESSIBILITY_SETTINGS", "界面是否变为不可取消弹窗"]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "显著盲区：二阶段代码与全部引导文案位于加密资产 assets/qAERL.json，静态零文本；若载荷以纯图片/GIF 呈现引导（本样本具备 assets/tiles_*、大量 png/plist 资源），UTG 文本节点将为空，必须启用 OCR 与截图比对。另有无 description 导致的系统警告缺失，使系统页本身也不提供判别文本。"
  },
  "behavior_pattern_tags": [
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "TRIG_COLD_START_BLOCK",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH"
  ],
  "code_anchors": [
    "crack.base.hawk.WPlHpDgOdIaFgTz.attachBaseContext",
    "crack.base.hawk.DZzAiUuToMtEoLqHeLtRpMrKuLnXpCiSpItTnJoPeCxRmOe.littleriot",
    "crack.base.hawk.PHoXaTbQyEqWqXiMlWeAjTjLd.obtainfew",
    "crack.base.hawk.GNaYjTfEkItFqJl.magicdutch",
    "res/xml/bgebtkpacvv.xml",
    "assets/qAERL.json"
  ]
}
```

</details>
