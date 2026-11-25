# MB_021__a778818cc0｜FluBot — Voicemail

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：161.8s

## 1. 一句话核心结论

- **核心申请方式**：以 com.sina.weibo 包名 + Voicemail 显示名伪装的加壳木马，先由壳 Application 解密加载二阶段载荷再实施最宽权限无障碍监听与短信控制，引导页面本身藏于加密载荷内静态不可见。
- **静态可见性说明**：仅壳层与声明层静态可见：Manifest、无障碍服务配置、strings 资源、壳 Application 存根 com.pokemon.rider.a 与加密字符串加载器 com.pokemon.rider.v 可完整还原；真实业务代码（含无障碍引导页、ACTION_ACCESSIBILITY_SETTINGS 跳转、弹窗/WebView/遮罩、拒权循环）全部位于 assets/Monoco/Zw6IGlco.ppt 加密二阶段载荷内，首字节非任何标准魔数、无明文可检索字符串，静态不可还原；classes.dex 中 com.sina 包下 0 个类，Manifest 声明的所有组件类均缺失。
- **命中的行为模式标签**：`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `a778818cc08d213d1f66db5fa8b34aabc862569ecb99fd1aea37ff6ccab48400` |
| 包名 / 年份 | `com.sina.weibo` / 2023 |
| 家族 / 品类 | **FluBot**（同池样本数：2） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Voicemail |
| 引导页宣称品牌/身份 | 冒充新浪微博品牌（包名 com.sina.weibo），同时对用户呈现为「语音信箱 / Voicemail」工具 |
| 系统无障碍列表服务名 | Voicemail（系统无障碍列表中由 @string/app_name 与 android:description="/ Voicemail /" 呈现，无独立 service 标签） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 包名盗用 com.sina.weibo 但无 com.sina 包下任何类；2) 无障碍描述写作 "/ Voicemail /"，用斜杠与空格填充使条目视觉上类系统内置项；3) 加密载荷使用伪扩展名 .ppt 藏于 assets/Monoco/；4) Manifest 元数据 ProtectKey/RandomName/DexFolderName/ReplaceDexName 以 Unicode 乱码字符存储壳参数；5) 壳 Application 通过异或加密字符串 + 反射改写 ApplicationInfo.className 与 Instrumentation 隐藏真实入口；6) appComponentFactory 指向 p05db44d4.pcb30670a.p8fb4ec54.p2757da78 混淆类 |
| 无障碍服务类名 | `com.sina.weibo.p1d2dbd8f` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS` |
| 系统设置项说明 (`android:description`) | / Voicemail / |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.sina.weibo.p9c215b6d（Manifest 声明为 LAUNCHER，含 MAIN 与 LAUNCHER 双 intent-filter）；同名类在 classes.dex 中不存在 | 用户点击桌面 Voicemail 图标，系统拉起 LAUNCHER Activity | 不可静态还原 | **原文**：Voicemail<br>**译注**：桌面图标与任务名显示为「语音信箱」 | 点击图标启动（此步为常规启动，无诱导文案） | `AndroidManifest.xml <activity android:name="com.sina.weibo.p9c215b6d">；res/values/strings.xml app_name` |
| 2 | 冷启动入口 | com.pokemon.rider.a（壳 Application 存根，继承 com.pokemon.rider.m） | 进程创建时系统回调 attachBaseContext(Context)，随即执行 new v(context).a(context) | 不可静态还原 | 无 | 无用户交互 | `com.pokemon.rider.a#attachBaseContext → com.pokemon.rider.v#a(Context)` |
| 3 | 冷启动入口 | assets/Monoco/Zw6IGlco.ppt（878993 字节加密载荷） | 壳加载器 com.pokemon.rider.v#a(int) 异或还原类名后反射构造 DexClassLoader 读取该载荷并替换 ApplicationInfo.className / Instrumentation | 不可静态还原 | 无 | 无用户交互 | `com.pokemon.rider.v#a(java.lang.String) 与 com.pokemon.rider.v#a(int)；assets/Monoco/Zw6IGlco.ppt` |
| 4 | 引导说明页 | 真实业务 Activity / Dialog / WebView（类名位于加密载荷，无法枚举） | 无法静态确认（载荷解密后才可见）；明文 DEX 中 ACCESSIBILITY_SETTINGS、Voicemail 等检索均 0 命中 | 不可静态还原 | **原文**：无（静态不可取得；resources 中除 "/ Voicemail /" 外无任何引导文案）<br>**译注**：静态侧无法取得引导页原文 | 无法静态确认 | `加密载荷 assets/Monoco/Zw6IGlco.ppt（静态不可还原）` |
| 5 | 跳无障碍设置 | 系统「设置 → 无障碍 → 已下载的服务」页面（目标页可确认；跳转调用点不可确认） | 无法静态确认；跳转字符串不在明文 DEX 中 | 系统无障碍页 | **原文**：Voicemail<br>**译注**：系统无障碍服务列表中该条目显示为「Voicemail」，说明行为 "/ Voicemail /" | 要求用户在系统列表中开启该服务（是否可取消、是否有跳过按钮无法静态确认） | `AndroidManifest.xml <service android:name="com.sina.weibo.p1d2dbd8f" android:permission="android.permission.BIND_ACCESSIBILITY_SERVICE">；res/xml/accessibility_service_config.xml；res/values/strings.xml#L30-L31` |
| 6 | 获权后动作 | com.sina.weibo.p1d2dbd8f（typeAllMask + canRetrieveWindowContent + flagRetrieveInteractiveWindows 的全局无障碍服务） | 服务被系统绑定后接收 typeAllMask 全部事件；具体分发逻辑位于加密载荷 | 不可静态还原 | 无 | 无（获权后静默运行） | `res/xml/accessibility_service_config.xml（android:accessibilityEventTypes="typeAllMask"，android:canRetrieveWindowContent="true"）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 桌面图标与最近任务：@string/app_name = "Voicemail"（res/values/strings.xml）
- 系统无障碍服务列表条目名：复用 @string/app_name = "Voicemail"
- 系统无障碍服务列表条目说明：android:description = @string/accessibility_service_description = "/ Voicemail /"（用斜杠与空格填充，视觉上仿系统内置条目）
- 应用内引导弹窗 / 说明页 / WebView / 悬浮遮罩：静态不可定位，位于 assets/Monoco/Zw6IGlco.ppt 加密载荷内，需运行期 UTG 捕获
- assets/license.html、assets/license-ru.html：经核验为 WebView 类库的第三方许可证样式页，不含任何引导或无障碍文案，非诱导载体

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Voicemail | 语音信箱 | `res/values/strings.xml key=app_name` | 清理工具伪装 |
| en | / Voicemail / | / 语音信箱 / | `res/values/strings.xml key=accessibility_service_description（被 res/xml/accessibility_service_config.xml 的 android:description 引用）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：静态不可确认。明文 DEX 中不存在 ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS 调用点，onResume 重跳、Timer 定时拉起、悬浮窗遮罩等机制均位于加密载荷，须运行期观测。仅可确认配套申请了 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、KILL_BACKGROUND_PROCESSES、FOREGROUND_SERVICE 等维持后台存活的权限。
- **遮罩叠层 / 高仿系统设置页**：静态不可确认（载荷内）；Manifest 未申请 SYSTEM_ALERT_WINDOW，若存在遮罩需依赖无障碍自身窗口或 Activity 半透明主题实现
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=28，低于 Android 13 受限设置门槛；DEX 预筛亦无 SESSION_INSTALLER 以外的教唆链路，本次未在明文 DEX 中找到相关字符串）
- **获权后即时行为与防撤权机制**：静态不可确认（载荷内）。已确认可确认的攻击面为：无障碍服务持有 typeAllMask 全部事件 + flagRetrieveInteractiveWindows，理论上具备监听设置页并执行全局返回/主页以阻止撤权的能力，但具体实现未在明文层出现
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：两个锚点同时布控：① 进程启动瞬间（Voicemail 冷启动）即开始录屏，因为壳在 attachBaseContext 阶段就解密载荷，引导页可能在首个 Activity 之前完成注册；② 监测任何 Activity 启动或无障碍服务绑定的系统广播，尤其当顶层 Activity 属于 com.sina.weibo.* 或检测到 Settings.ACTION_ACCESSIBILITY_SETTINGS 的 intent 发起时立即锁定该帧。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：显著盲区：静态侧完全无法预知引导文案与 UI 结构，纯 UTG 必须依赖运行期录屏，若载荷检测到模拟器/调试环境而延迟或抑制引导（本样本具备 QUERY_ALL_PACKAGES 与反调试式壳），可能整场运行不出现诱导页，形成「静默无 UI」盲区；另若引导为纯图无文本的 GIF/PNG 指引，需 OCR 辅助。注：静态加壳本身不阻挡运行期 UTG，但会延迟到载荷解密后才出现诱导界面，需在冷启动即开始录屏以免漏帧。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页 / 说明页** | 包名 com.sina.weibo 下的 Activity 或 Dialog，标题/正文含 Voicemail 或语音信箱类措辞；若为 WebView 则检测 file:///android_asset 或远端 URL 加载 | 该页是区分「良性无障碍工具如实说明」与「诱导开启」的第一判据：有无明确取消按钮、有无恐吓/假更新话术、是否直接给出系统设置跳转按钮 | 是否存在可点击的取消/跳过控件（文本或 contentDescription 含 cancel/skip/not now/取消/跳过）；页面是否出现「必需」「必须开启」「否则无法使用」「设备异常」「安全风险」等胁迫措辞；是否有直接跳转无障碍设置的按钮文本（enable/activate/open settings/开启/立即开启）；WebView 加载的 URL 是 file:///android_asset 还是远端域名 |
| **跳转后的系统无障碍服务列表项** | Settings 无障碍页中的 "Voicemail" 条目，摘要为 "/ Voicemail /" | 确认应用确实把用户导向系统无障碍开关，且条目名/描述经过伪装，属身份混淆的直接视觉证据 | 条目文本是否为 Voicemail 及说明是否为 / Voicemail /（含斜杠空格填充）；是否存在与本应用图标/名称不一致的条目；是否出现「受限设置」提示（Android 13+ 才可能，本样本 targetSdk 28 预期不出现） |
| **设置页返回后的遮罩叠层或重跳页** | 从 Settings 返回后 0.5–2 秒内出现的新 Activity/Dialog，或无障碍开启前反复出现的同一引导页 | 判定拒权反馈循环与遮罩压栈是「诱导」升级为「强制胁迫」的关键，纯 UTG 帧序列可还原重跳次数与间隔 | 同一引导页在用户返回后是否再次出现（重复帧计数与时间间隔）；是否存在半透明遮罩层叠加于设置页之上；无障碍服务实际是否被开启（可交叉验证设置项状态变化） |
| **获权后首个动作页** | 无障碍开启后立即出现的界面或通知，或无障碍服务开始读取其他应用窗口（如短信、银行、输入法界面） | 验证 typeAllMask 最宽权限的实际用途，区分良性工具与短信木马控制链 | 开启后是否立即跳转短信/通讯录/银行类应用界面；是否出现请求短信权限或通知监听权限的二次弹窗；是否出现覆盖在其他应用之上的输入/点击动作 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.pokemon.rider.a#attachBaseContext`
- `com.pokemon.rider.a#onCreate`
- `com.pokemon.rider.v#a`
- `res/xml/accessibility_service_config.xml`
- `res/values/strings.xml#L30-L31`
- `assets/Monoco/Zw6IGlco.ppt`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 定向核验结论

**核心判断：无障碍诱导的“运行期 UTG 页面流转”在本样本中无法静态还原，因为相关代码并不在 `classes.dex` 里，而是位于加密的二阶段载荷中。** 以下为已证实事实与边界。

### 已证实（静态可闭环）

- **Manifest 声明的组件全部缺失。** `classes.dex` 共 3780 个类，`com.sina` 包下 **0 个类**；`com.sina.weibo.p1d2dbd8f`（无障碍服务）、`p9c215b6d`（LAUNCHER）、`pce8f9a3a`、短信接收器等均无法解析，这说明业务代码被移出主 DEX。
- **自定义壳入口清晰。** [com.pokemon.rider.a#attachBaseContext](<resource-unit:#1.dex1 code:com.pokemon.rider.a#attachBaseContext>) 在 `super.attachBaseContext` 之后立即执行 `new v(context).a(context)`；[com.pokemon.rider.a#onCreate](<resource-unit:#1.dex1 code:com.pokemon.rider.a#onCreate>) 仅在加载成功后把调用转发给真实 Application，这是典型的壳存根结构。
- **加载器采用全量异或加密 + 反射。** [com.pokemon.rider.v#a](<resource-unit:#1.dex1 code:com.pokemon.rider.v#a>) 通过 `bArr[i] ^ i` 还原类名与反射方法名（索引 402/408/441/447/462/476/531/564/589/632/669），再反射改写 `ApplicationInfo.className` 并注入 `Instrumentation`。
- **加密载荷已定位。** [assets/Monoco/Zw6IGlco.ppt](<resource-unit:#1 file:assets/Monoco/Zw6IGlco.ppt>)（878,993 字节）使用伪 Office 扩展名，首字节 `62 F4 B0 01` 不匹配 ZIP/DEX/ELF 魔数，UTF-8 全文检索 `dex`/`classes`/`accessibility` 均为 0 命中，因此判定为加密载荷；Manifest 中 `ProtectKey`、`DexFolderName`、`ReplaceDexName`、`RandomName` 四个 Unicode 混淆元数据与该机制对应。
- **无障碍权限最宽。** [res/xml/accessibility_service_config.xml](<resource-unit:#1 file:res/xml/accessibility_service_config.xml>) 声明 `typeAllMask`、`canRetrieveWindowContent="true"`、`flagRetrieveInteractiveWindows`、`notificationTimeout="0"`，可读取全部窗口内容与全部事件类型。
- **身份错配。** 包名为 `com.sina.weibo`（新浪微博品牌），而 [res/values/strings.xml](<resource-unit:#1 file:res/values/strings.xml#L30-L31>) 中 `app_name` 与 `accessibility_service_description` 均为 `Voicemail` / `/ Voicemail /`。
- **排除项。** `assets/license.html`、`license-ru.html` 是 WebView 类库附带的许可证样式页（`font-family: sans-serif` 标准 boilerplate），与引导无关；`assets/66666692.appinfo.json` 等为阿里系小程序离线包元数据。

### 未能证实（覆盖边界）

- 在明文 DEX 中检索 `ACCESSIBILITY_SETTINGS`、`APPLICATION_DETAILS_SETTINGS`、`Voicemail`、`Monoco` 均 **0 命中**，证实跳转字符串、引导弹窗、遮罩层、拒权循环全部在加密载荷内，**无法从静态侧确认具体载体与触发时机**。
- 因此下文 `step_by_step_flow` 仅列出可确认的壳加载链路与 Manifest 级证据，诱导页本身标注为不可静态还原；UTG 侧需在载荷解密后于运行期捕获。

已登记风险 R-001（`malware_trojan` / high）。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "仅壳层与声明层静态可见：Manifest、无障碍服务配置、strings 资源、壳 Application 存根 com.pokemon.rider.a 与加密字符串加载器 com.pokemon.rider.v 可完整还原；真实业务代码（含无障碍引导页、ACTION_ACCESSIBILITY_SETTINGS 跳转、弹窗/WebView/遮罩、拒权循环）全部位于 assets/Monoco/Zw6IGlco.ppt 加密二阶段载荷内，首字节非任何标准魔数、无明文可检索字符串，静态不可还原；classes.dex 中 com.sina 包下 0 个类，Manifest 声明的所有组件类均缺失。",
  "summary_one_liner": "以 com.sina.weibo 包名 + Voicemail 显示名伪装的加壳木马，先由壳 Application 解密加载二阶段载荷再实施最宽权限无障碍监听与短信控制，引导页面本身藏于加密载荷内静态不可见。",
  "disguise_identity": {
    "app_display_name": "Voicemail",
    "claimed_brand_or_persona": "冒充新浪微博品牌（包名 com.sina.weibo），同时对用户呈现为「语音信箱 / Voicemail」工具",
    "a11y_service_label": "Voicemail（系统无障碍列表中由 @string/app_name 与 android:description=\"/ Voicemail /\" 呈现，无独立 service 标签）",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 包名盗用 com.sina.weibo 但无 com.sina 包下任何类；2) 无障碍描述写作 \"/ Voicemail /\"，用斜杠与空格填充使条目视觉上类系统内置项；3) 加密载荷使用伪扩展名 .ppt 藏于 assets/Monoco/；4) Manifest 元数据 ProtectKey/RandomName/DexFolderName/ReplaceDexName 以 Unicode 乱码字符存储壳参数；5) 壳 Application 通过异或加密字符串 + 反射改写 ApplicationInfo.className 与 Instrumentation 隐藏真实入口；6) appComponentFactory 指向 p05db44d4.pcb30670a.p8fb4ec54.p2757da78 混淆类"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.sina.weibo.p9c215b6d（Manifest 声明为 LAUNCHER，含 MAIN 与 LAUNCHER 双 intent-filter）；同名类在 classes.dex 中不存在",
      "trigger_event": "用户点击桌面 Voicemail 图标，系统拉起 LAUNCHER Activity",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Voicemail",
      "shown_text_zh": "桌面图标与任务名显示为「语音信箱」",
      "user_action_requested": "点击图标启动（此步为常规启动，无诱导文案）",
      "code_anchor": "AndroidManifest.xml <activity android:name=\"com.sina.weibo.p9c215b6d\">；res/values/strings.xml app_name"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "com.pokemon.rider.a（壳 Application 存根，继承 com.pokemon.rider.m）",
      "trigger_event": "进程创建时系统回调 attachBaseContext(Context)，随即执行 new v(context).a(context)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面，静默完成载荷解密与真实 Application 替换",
      "user_action_requested": "无用户交互",
      "code_anchor": "com.pokemon.rider.a#attachBaseContext → com.pokemon.rider.v#a(Context)"
    },
    {
      "step": 3,
      "stage": "冷启动入口",
      "screen_or_component": "assets/Monoco/Zw6IGlco.ppt（878993 字节加密载荷）",
      "trigger_event": "壳加载器 com.pokemon.rider.v#a(int) 异或还原类名后反射构造 DexClassLoader 读取该载荷并替换 ApplicationInfo.className / Instrumentation",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "载荷无任何可读明文，无界面输出",
      "user_action_requested": "无用户交互",
      "code_anchor": "com.pokemon.rider.v#a(java.lang.String) 与 com.pokemon.rider.v#a(int)；assets/Monoco/Zw6IGlco.ppt"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "真实业务 Activity / Dialog / WebView（类名位于加密载荷，无法枚举）",
      "trigger_event": "无法静态确认（载荷解密后才可见）；明文 DEX 中 ACCESSIBILITY_SETTINGS、Voicemail 等检索均 0 命中",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（静态不可取得；resources 中除 \"/ Voicemail /\" 外无任何引导文案）",
      "shown_text_zh": "静态侧无法取得引导页原文",
      "user_action_requested": "无法静态确认",
      "code_anchor": "加密载荷 assets/Monoco/Zw6IGlco.ppt（静态不可还原）"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统「设置 → 无障碍 → 已下载的服务」页面（目标页可确认；跳转调用点不可确认）",
      "trigger_event": "无法静态确认；跳转字符串不在明文 DEX 中",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Voicemail",
      "shown_text_zh": "系统无障碍服务列表中该条目显示为「Voicemail」，说明行为 \"/ Voicemail /\"",
      "user_action_requested": "要求用户在系统列表中开启该服务（是否可取消、是否有跳过按钮无法静态确认）",
      "code_anchor": "AndroidManifest.xml <service android:name=\"com.sina.weibo.p1d2dbd8f\" android:permission=\"android.permission.BIND_ACCESSIBILITY_SERVICE\">；res/xml/accessibility_service_config.xml；res/values/strings.xml#L30-L31"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.sina.weibo.p1d2dbd8f（typeAllMask + canRetrieveWindowContent + flagRetrieveInteractiveWindows 的全局无障碍服务）",
      "trigger_event": "服务被系统绑定后接收 typeAllMask 全部事件；具体分发逻辑位于加密载荷",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面，可读取全部窗口内容与交互窗口",
      "user_action_requested": "无（获权后静默运行）",
      "code_anchor": "res/xml/accessibility_service_config.xml（android:accessibilityEventTypes=\"typeAllMask\"，android:canRetrieveWindowContent=\"true\"）"
    }
  ],
  "text_presentation_locations": [
    "桌面图标与最近任务：@string/app_name = \"Voicemail\"（res/values/strings.xml）",
    "系统无障碍服务列表条目名：复用 @string/app_name = \"Voicemail\"",
    "系统无障碍服务列表条目说明：android:description = @string/accessibility_service_description = \"/ Voicemail /\"（用斜杠与空格填充，视觉上仿系统内置条目）",
    "应用内引导弹窗 / 说明页 / WebView / 悬浮遮罩：静态不可定位，位于 assets/Monoco/Zw6IGlco.ppt 加密载荷内，需运行期 UTG 捕获",
    "assets/license.html、assets/license-ru.html：经核验为 WebView 类库的第三方许可证样式页，不含任何引导或无障碍文案，非诱导载体"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Voicemail",
      "text_zh": "语音信箱",
      "source_location": "res/values/strings.xml key=app_name",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "/ Voicemail /",
      "text_zh": "/ 语音信箱 /",
      "source_location": "res/values/strings.xml key=accessibility_service_description（被 res/xml/accessibility_service_config.xml 的 android:description 引用）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "静态不可确认。明文 DEX 中不存在 ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS 调用点，onResume 重跳、Timer 定时拉起、悬浮窗遮罩等机制均位于加密载荷，须运行期观测。仅可确认配套申请了 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、KILL_BACKGROUND_PROCESSES、FOREGROUND_SERVICE 等维持后台存活的权限。",
    "overlay_or_fake_settings": "静态不可确认（载荷内）；Manifest 未申请 SYSTEM_ALERT_WINDOW，若存在遮罩需依赖无障碍自身窗口或 Activity 半透明主题实现",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=28，低于 Android 13 受限设置门槛；DEX 预筛亦无 SESSION_INSTALLER 以外的教唆链路，本次未在明文 DEX 中找到相关字符串）",
    "post_grant_anti_removal": "静态不可确认（载荷内）。已确认可确认的攻击面为：无障碍服务持有 typeAllMask 全部事件 + flagRetrieveInteractiveWindows，理论上具备监听设置页并执行全局返回/主页以阻止撤权的能力，但具体实现未在明文层出现",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "两个锚点同时布控：① 进程启动瞬间（Voicemail 冷启动）即开始录屏，因为壳在 attachBaseContext 阶段就解密载荷，引导页可能在首个 Activity 之前完成注册；② 监测任何 Activity 启动或无障碍服务绑定的系统广播，尤其当顶层 Activity 属于 com.sina.weibo.* 或检测到 Settings.ACTION_ACCESSIBILITY_SETTINGS 的 intent 发起时立即锁定该帧。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页 / 说明页",
        "page_identifier": "包名 com.sina.weibo 下的 Activity 或 Dialog，标题/正文含 Voicemail 或语音信箱类措辞；若为 WebView 则检测 file:///android_asset 或远端 URL 加载",
        "why_most_useful": "该页是区分「良性无障碍工具如实说明」与「诱导开启」的第一判据：有无明确取消按钮、有无恐吓/假更新话术、是否直接给出系统设置跳转按钮",
        "observable_utg_signals": [
          "是否存在可点击的取消/跳过控件（文本或 contentDescription 含 cancel/skip/not now/取消/跳过）",
          "页面是否出现「必需」「必须开启」「否则无法使用」「设备异常」「安全风险」等胁迫措辞",
          "是否有直接跳转无障碍设置的按钮文本（enable/activate/open settings/开启/立即开启）",
          "WebView 加载的 URL 是 file:///android_asset 还是远端域名"
        ]
      },
      {
        "page_role": "跳转后的系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍页中的 \"Voicemail\" 条目，摘要为 \"/ Voicemail /\"",
        "why_most_useful": "确认应用确实把用户导向系统无障碍开关，且条目名/描述经过伪装，属身份混淆的直接视觉证据",
        "observable_utg_signals": [
          "条目文本是否为 Voicemail 及说明是否为 / Voicemail /（含斜杠空格填充）",
          "是否存在与本应用图标/名称不一致的条目",
          "是否出现「受限设置」提示（Android 13+ 才可能，本样本 targetSdk 28 预期不出现）"
        ]
      },
      {
        "page_role": "设置页返回后的遮罩叠层或重跳页",
        "page_identifier": "从 Settings 返回后 0.5–2 秒内出现的新 Activity/Dialog，或无障碍开启前反复出现的同一引导页",
        "why_most_useful": "判定拒权反馈循环与遮罩压栈是「诱导」升级为「强制胁迫」的关键，纯 UTG 帧序列可还原重跳次数与间隔",
        "observable_utg_signals": [
          "同一引导页在用户返回后是否再次出现（重复帧计数与时间间隔）",
          "是否存在半透明遮罩层叠加于设置页之上",
          "无障碍服务实际是否被开启（可交叉验证设置项状态变化）"
        ]
      },
      {
        "page_role": "获权后首个动作页",
        "page_identifier": "无障碍开启后立即出现的界面或通知，或无障碍服务开始读取其他应用窗口（如短信、银行、输入法界面）",
        "why_most_useful": "验证 typeAllMask 最宽权限的实际用途，区分良性工具与短信木马控制链",
        "observable_utg_signals": [
          "开启后是否立即跳转短信/通讯录/银行类应用界面",
          "是否出现请求短信权限或通知监听权限的二次弹窗",
          "是否出现覆盖在其他应用之上的输入/点击动作"
        ]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "显著盲区：静态侧完全无法预知引导文案与 UI 结构，纯 UTG 必须依赖运行期录屏，若载荷检测到模拟器/调试环境而延迟或抑制引导（本样本具备 QUERY_ALL_PACKAGES 与反调试式壳），可能整场运行不出现诱导页，形成「静默无 UI」盲区；另若引导为纯图无文本的 GIF/PNG 指引，需 OCR 辅助。注：静态加壳本身不阻挡运行期 UTG，但会延迟到载荷解密后才出现诱导界面，需在冷启动即开始录屏以免漏帧。"
  },
  "behavior_pattern_tags": [
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH"
  ],
  "code_anchors": [
    "com.pokemon.rider.a#attachBaseContext",
    "com.pokemon.rider.a#onCreate",
    "com.pokemon.rider.v#a",
    "res/xml/accessibility_service_config.xml",
    "res/values/strings.xml#L30-L31",
    "assets/Monoco/Zw6IGlco.ppt"
  ]
}
```

</details>
