# MR_091__c91327f7e4｜BoostClicker — ConfigAPKs

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：64.2s

## 1. 一句话核心结论

- **核心申请方式**：空壳壳包 ConfigAPKs 以空白说明的 AccService + 无图标隐藏入口 AdTransActivity 为壳，无障碍事件经反射分派给 assets/cvzjem 加密载荷，诱导流程与权限申请页面全部在运行期由外部载荷下发，静态层仅暴露门禁校验与开机自启拉前台。
- **静态可见性说明**：Manifest、无障碍服务配置、strings、Activity/Service/Receiver 骨架与反射分派点全部静态可见；但真正的无障碍引导 UI（弹窗/WebView/遮罩/跳 ACTION_ACCESSIBILITY_SETTINGS）不在 classes.dex 内——AccService 把事件转发给 com.a.a.a，再经 g.a 反射调用 setAccessEvent/setAccessInterrupt/startA/startR/startS 等本包不存在的方法，实现在 assets/cvzjem 加密载荷（配 resource.json 索引 id=84）中，需动态加载后运行，静态不可还原。
- **命中的行为模式标签**：`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `c91327f7e48ca64c829c29e6bcb30451dab6c9d32386048165702df3a728c173` |
| 包名 / 年份 | `com.xolo.qifyf` / 2020 |
| 家族 / 品类 | **BoostClicker**（同池样本数：2） |
| 原始来源标识 | https://www.trendmicro.com/en_us/research/20/b/malicious-apps-on-google-play-communicate-with-trojans-install-malware-perform-mobile-ad-fraud.html |
| 桌面显示名 | ConfigAPKs |
| 引导页宣称品牌/身份 | 无明确品牌声明，仅以泛化名 ConfigAPKs（暗示配置/工具类）作为外壳身份 |
| 系统无障碍列表服务名 | ConfigAPKs（android:label=@string/app_name，用途说明 android:description=@string/access_desc 为空字符串） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务 android:description 指向空字符串资源（系统列表中用途说明为空白，用户无法判断授权后果）；AdTransActivity 声明 android.intent.action.MAIN 但无 LAUNCHER category，桌面无图标且 excludeFromRecents，仅能被显式 Intent/广播拉起；两处 Activity 均为 Theme.Translucent.NoTitleBar.Fullscreen 半透明全屏，无可见品牌界面；核心类名/包名统一 a、b、c、com.a.a.* 混淆，真实能力经反射按字符串名分发。 |
| 无障碍服务类名 | `com.app.assists.service.AccService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | @7F020000 |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.app.assists.AdTransActivity（半透明全屏，无 LAUNCHER 图标） | 被显式 Intent 或 MReceiver（BOOT_COMPLETED/USER_PRESENT/PACKAGE_ADDED）拉起后 onCreate | 原生Activity | **原文**：无（Theme.Translucent.NoTitleBar.Fullscreen，无任何可见文案）<br>**译注**：透明过渡页，界面无文字 | 无交互，用户仅看到当前界面被短暂覆盖 | `com.app.assists.AdTransActivity.onCreate` |
| 2 | 业务功能触发 | com.app.assists.a.a(Context) 环境门禁判定 | AdTransActivity.onCreate 中调用 a.a(getApplicationContext()) | 不可静态还原 | **原文**：isExistFile : / isDevelop : / hasLightSensorManager : / hasSimCard : / isWifiProxy : / isAppNumOk :（均为日志 tag 文本）<br>**译注**：判定是否为真实设备与指定投放对象：/Download/com.h5game.txt 存在即放行，开发者模式、代理、无 SIM、无光线传感器、应用数异常则终止 | 无（静默判定，不通过则整条链路不执行） | `com.app.assists.a.a(Context)` |
| 3 | 获权后动作 | 反射桥 com.a.a.a.a(int, Context, Intent) → 外部载荷方法 startA | 门禁通过后调用 com.a.a.a.a(10, this, getIntent())，经 g.a 反射执行 startA(Context, Activity, Intent) | 不可静态还原 | **原文**：show Ad activity（日志）<br>**译注**：真实广告/引导界面由外部加密载荷接管绘制，静态层无文案 | 不可静态还原 | `com.a.a.a.a(int, Context, Intent) / com.a.a.g.a` |
| 4 | 获权后动作 | com.app.assists.service.AccService（已注册无障碍服务） | 系统在服务被开启后回调 onAccessibilityEvent / onInterrupt | 不可静态还原 | **原文**：无（事件直接透传，不做本地处理）<br>**译注**：所有无障碍事件被转交外部载荷的 setAccessEvent，用于读取界面节点/模拟点击 | 不可静态还原（用户此前已在系统设置中开启该服务） | `com.app.assists.service.AccService.onAccessibilityEvent` |
| 5 | 遮罩叠层指引 | com.app.assists.TransActivity（半透明全屏过渡页） | onCreate / onResume 中调用 a()，检测屏幕点亮后立即 finish() | 原生Activity | **原文**：show activity（日志）<br>**译注**：亮屏即自动关闭的过渡页，配合外部载荷做页面覆盖/切页配合 | 无（无取消或跳过按钮） | `com.app.assists.TransActivity.a()` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：服务名显示为 ConfigAPKs（android:label=@string/app_name），用途说明为空白——res/xml/accessibility_service_config.xml 的 android:description 指向 res/values/strings.xml 中空字符串 access_desc
- 应用列表/系统设置应用详情：应用名 ConfigAPKs（res/values/strings.xml app_name），无自定义图标文案
- AdTransActivity 与 TransActivity：Theme.Translucent.NoTitleBar.Fullscreen，运行时无任何本地文案，用户看不到说明文字
- 真正的引导/说明文案（弹窗、WebView 教学页、悬浮遮罩）未出现在 classes.dex、res/ 或 assets/ 的可读资源中，需由 assets/cvzjem 加密载荷在运行期动态加载后渲染（不可静态还原）
- MReceiver 在 BOOT_COMPLETED/USER_PRESENT 后直接 startActivity 拉起前台页，构成无通知栏文案的静默回访入口

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | ConfigAPKs | ConfigAPKs（暗示为配置/工具类应用） | `res/values/strings.xml -> app_name（同时用作 android:label 与 accessibility-service android:name）` | 清理工具伪装 |
| en | （空字符串） | 无障碍服务用途说明为空，用户无法得知该服务会读取屏幕内容并模拟点击 | `res/values/strings.xml -> access_desc（<string name="access_desc" />）` | 教唆忽视警告 |
| en | show Ad activity / show activity / isExistFile : / isDevelop : / hasLightSensorManager : / hasSimCard : / isWifiProxy : / isAppNumOk : | 展示广告页 / 展示页面 / 文件存在：/ 是否开发者模式：/ 是否有光线传感器：/ 是否有 SIM 卡：/ 是否 Wi-Fi 代理：/ 应用数量是否正常： | `com.app.assists.c.a（日志）被 AdTransActivity.onCreate、TransActivity.a、com.app.assists.a.a 调用` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：静态层无证据。可见的仅有回访机制：MReceiver 监听 BOOT_COMPLETED/USER_PRESENT/PACKAGE_ADDED 后调用 context.startActivity(intent2) 主动拉起前台；是否存在跳设置后 onResume 死循环重跳、Timer 定时拉起，需动态加载载荷后观察
- **遮罩叠层 / 高仿系统设置页**：静态层未发现 overlay 引导窗代码，但应用持有 SYSTEM_ALERT_WINDOW 权限，且两个 Activity 均为 Translucent 全屏主题，具备叠放半透明遮罩的能力；具体叠层实现位于外部加密载荷，不可静态还原
- **Android 13+ 受限设置（Restricted Settings）应对**：无（全 DEX 无 ACTION_APPLICATION_DETAILS_SETTINGS、无 ACTION_ACCESSIBILITY_SETTINGS、无 isAccessibilityTool 相关逻辑；targetSdkVersion=21，远低于 Android 13 受限设置门槛）
- **获权后即时行为与防撤权机制**：无静态证据。可确认 AccService 在 onAccessibilityEvent/onInterrupt 中把事件全部透传给外部载荷（setAccessEvent/setAccessInterrupt），是否用 GLOBAL_ACTION_BACK/HOME 阻止撤权无法静态判定
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：最佳拉起时机为 MReceiver 收到 BOOT_COMPLETED / USER_PRESENT 后 startActivity 拉起 AdTransActivity 的瞬间（含锁屏解锁），以及 AdTransActivity.onCreate 门禁通过后反射执行 startA 之后的 3~5 秒内——此窗口外部载荷已完成加载并绘制引导界面；单纯监测 ACTION_ACCESSIBILITY_SETTINGS 跳转对本样本无效，因为该跳转由动态载荷在运行期发起
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：显著盲区：一阶段为空壳 Dropper，引导文案与按钮全在 assets/cvzjem 加密载荷中运行期解密，纯静态 UTG/资源扫描会看到'无任何诱导文案'；同时无障碍服务用途说明为空白，系统列表中无文字线索；若外部载荷采用纯图片/WebView 图片按钮承载引导文案，则必须 OCR。静态加壳本身不阻挡运行期 UTG 捕获，但需在 BOOT_COMPLETED/USER_PRESENT 拉起时机开始录制。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动/回访入口过渡页** | com.app.assists.AdTransActivity，Theme.Translucent.NoTitleBar.Fullscreen，无标题栏、界面几乎透明 | 这是整条诱导链唯一的静态入口，捕获它即可确认门禁通过并锁定后续引导界面的时间窗口 | 包名 com.xolo.qifyf + Activity 名 com.app.assists.AdTransActivity；界面无文本且无标题栏的半透明全屏节点树；紧接着出现的外部载荷渲染页面 |
| **运行期引导说明页/弹窗（由加密载荷渲染）** | 非应用自身 res 布局，节点树与包内资源不匹配，常见为 WebView 或动态创建的悬浮窗 | 无障碍诱导的核心文案与按钮只在此出现，是判定'是否诱导开启无障碍'的决定性证据 | WebView 节点或 WindowManager 添加的悬浮窗；包含'开启无障碍/辅助功能/权限'等关键词的按钮文本；唯一按钮且无取消/关闭按钮的弹窗结构 |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已下载的服务，条目名为 ConfigAPKs，副标题说明为空 | 可直接验证空白 description 伪装效果，并确认用户被引导到的正是该服务开关 | 条目文本 ConfigAPKs 且下方说明文本为空；开关节点处于关闭态、紧接被点击；当前前台包名为 com.android.settings 且子页面为 AccessibilitySettings |
| **获权后的无障碍运行态** | AccService 已启用，界面出现自动点击/自动翻页行为 | 确认授权后实际用途与声明身份（ConfigAPKs）完全不符 | 无障碍服务启用状态变化；非用户输入的连续点击/滑动事件；界面出现广告或跳转第三方页面 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.app.assists.service.AccService.onAccessibilityEvent / onInterrupt`
- `com.a.a.a.a(int, Context, Intent)（反射分派 startA/startR/startS）`
- `com.a.a.a.a(AccessibilityService, int, AccessibilityEvent)（反射分派 setAccessEvent/setAccessInterrupt）`
- `com.app.assists.AdTransActivity.onCreate`
- `com.app.assists.receiver.MReceiver.onReceive（BOOT_COMPLETED/USER_PRESENT → startActivity）`
- `res/xml/accessibility_service_config.xml + res/values/strings.xml#access_desc（空白说明）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（14 次工具调用内收口）

**1. 引导流程本身不在静态 DEX 内 —— 这是个"空壳 + 反射分派"结构**
- `com.app.assists.service.AccService` 只做一件事：把 `onAccessibilityEvent` / `onInterrupt` 转发给 [com.a.a.a.a()](<resource-unit:#1.dex1 code:com.a.a.a#a>)，后者再用 `g.a(service, "setAccessEvent", …)` 反射调用**本 DEX 中不存在的方法名**（`setAccessEvent` / `setAccessInterrupt` / `startA` / `startR` / `startS`）。这类"调用目标不在本包"的反射桥是典型的动态载荷分发壳。
- 全 DEX 搜索 `ACTION_ACCESSIBILITY_SETTINGS`、`ACTION_APPLICATION_DETAILS_SETTINGS`、`isAccessibilityTool`、`SYSTEM_ALERT_WINDOW` 字符串**零命中**；`startActivity` 仅在 [MReceiver.onReceive()](<resource-unit:#1.dex1 code:com.app.assists.receiver.MReceiver#onReceive>) 出现一次。因此"跳设置页 / 引导弹窗 / WebView 教学页"的代码不在可见层。
- `assets/cvzjem` + [assets/resource.json](<resource-unit:#1 file:assets/resource.json>)（`{"data":"cvzjem","id":"84"}`）为加密/索引化的载荷资产，与上述反射分派配合构成一阶段 Dropper。

**2. 已确证的"身份与权限面"事实**
- 桌面/应用名 `ConfigAPKs`，无障碍服务 `android:label="@string/app_name"`，但 [res/xml/accessibility_service_config.xml](<resource-unit:#1 file:res/xml/accessibility_service_config.xml>) 的 `android:description="@string/access_desc"` 对应 [strings.xml](<resource-unit:#1 file:res/values/strings.xml#L3>) 中是**空字符串** `<string name="access_desc" />` —— 系统无障碍列表中该服务的用途说明为空白，用户无从判断其真实用途。
- `AdTransActivity` 带 `android.intent.action.MAIN` 但**无 `LAUNCHER` category**，且 `Translucent.NoTitleBar.Fullscreen` + `excludeFromRecents`：用户点不出图标，只能被显式 Intent / 广播拉起（[AdTransActivity.onCreate()](<resource-unit:#1.dex1 code:com.app.assists.AdTransActivity#onCreate>)）。
- [MReceiver](<resource-unit:#1 manifest:components>) 监听 `BOOT_COMPLETED` / `USER_PRESENT` / `PACKAGE_ADDED` 后直接 `context.startActivity(intent2)`，具备开机后自动弹出前台页的能力（后台重拉）。
- [TransActivity.a()](<resource-unit:#1.dex1 code:com.app.assists.TransActivity#a>) 仅做 `isScreenOn()` → `finish()`，是典型的亮屏瞬隐/切页配合逻辑。

**3. 环境门禁（反分析 + 定向投放）**
[com.app.assists.a.a(Context)](<resource-unit:#1.dex1 code:com.app.assists.a#a>) 在展示前依次校验：`/Download/com.h5game.txt` 存在则直接放行、`development_settings_enabled`（开发者模式）→ 拒绝、光线传感器、SIM 卡、`http.proxyHost` 代理 → 拒绝、已装应用数量。命中即"真实用户/指定投放名单"，规避沙箱与代理抓包。

**4. 结论与边界**
无障碍诱导的**具体文案、弹窗载体、跳转时序均藏于动态加载载荷**，静态不可还原；可确认的是恶意侧的结构性证据：空白服务说明、无图标隐藏入口、反射分派到外部载荷、开机自启拉前台、环境门禁。因引导链未闭合，本次不登记"诱导无障碍"风险命题。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "Manifest、无障碍服务配置、strings、Activity/Service/Receiver 骨架与反射分派点全部静态可见；但真正的无障碍引导 UI（弹窗/WebView/遮罩/跳 ACTION_ACCESSIBILITY_SETTINGS）不在 classes.dex 内——AccService 把事件转发给 com.a.a.a，再经 g.a 反射调用 setAccessEvent/setAccessInterrupt/startA/startR/startS 等本包不存在的方法，实现在 assets/cvzjem 加密载荷（配 resource.json 索引 id=84）中，需动态加载后运行，静态不可还原。",
  "summary_one_liner": "空壳壳包 ConfigAPKs 以空白说明的 AccService + 无图标隐藏入口 AdTransActivity 为壳，无障碍事件经反射分派给 assets/cvzjem 加密载荷，诱导流程与权限申请页面全部在运行期由外部载荷下发，静态层仅暴露门禁校验与开机自启拉前台。",
  "disguise_identity": {
    "app_display_name": "ConfigAPKs",
    "claimed_brand_or_persona": "无明确品牌声明，仅以泛化名 ConfigAPKs（暗示配置/工具类）作为外壳身份",
    "a11y_service_label": "ConfigAPKs（android:label=@string/app_name，用途说明 android:description=@string/access_desc 为空字符串）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务 android:description 指向空字符串资源（系统列表中用途说明为空白，用户无法判断授权后果）；AdTransActivity 声明 android.intent.action.MAIN 但无 LAUNCHER category，桌面无图标且 excludeFromRecents，仅能被显式 Intent/广播拉起；两处 Activity 均为 Theme.Translucent.NoTitleBar.Fullscreen 半透明全屏，无可见品牌界面；核心类名/包名统一 a、b、c、com.a.a.* 混淆，真实能力经反射按字符串名分发。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.app.assists.AdTransActivity（半透明全屏，无 LAUNCHER 图标）",
      "trigger_event": "被显式 Intent 或 MReceiver（BOOT_COMPLETED/USER_PRESENT/PACKAGE_ADDED）拉起后 onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（Theme.Translucent.NoTitleBar.Fullscreen，无任何可见文案）",
      "shown_text_zh": "透明过渡页，界面无文字",
      "user_action_requested": "无交互，用户仅看到当前界面被短暂覆盖",
      "code_anchor": "com.app.assists.AdTransActivity.onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.app.assists.a.a(Context) 环境门禁判定",
      "trigger_event": "AdTransActivity.onCreate 中调用 a.a(getApplicationContext())",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "isExistFile : / isDevelop : / hasLightSensorManager : / hasSimCard : / isWifiProxy : / isAppNumOk :（均为日志 tag 文本）",
      "shown_text_zh": "判定是否为真实设备与指定投放对象：/Download/com.h5game.txt 存在即放行，开发者模式、代理、无 SIM、无光线传感器、应用数异常则终止",
      "user_action_requested": "无（静默判定，不通过则整条链路不执行）",
      "code_anchor": "com.app.assists.a.a(Context)"
    },
    {
      "step": 3,
      "stage": "获权后动作",
      "screen_or_component": "反射桥 com.a.a.a.a(int, Context, Intent) → 外部载荷方法 startA",
      "trigger_event": "门禁通过后调用 com.a.a.a.a(10, this, getIntent())，经 g.a 反射执行 startA(Context, Activity, Intent)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "show Ad activity（日志）",
      "shown_text_zh": "真实广告/引导界面由外部加密载荷接管绘制，静态层无文案",
      "user_action_requested": "不可静态还原",
      "code_anchor": "com.a.a.a.a(int, Context, Intent) / com.a.a.g.a"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "com.app.assists.service.AccService（已注册无障碍服务）",
      "trigger_event": "系统在服务被开启后回调 onAccessibilityEvent / onInterrupt",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（事件直接透传，不做本地处理）",
      "shown_text_zh": "所有无障碍事件被转交外部载荷的 setAccessEvent，用于读取界面节点/模拟点击",
      "user_action_requested": "不可静态还原（用户此前已在系统设置中开启该服务）",
      "code_anchor": "com.app.assists.service.AccService.onAccessibilityEvent"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.app.assists.TransActivity（半透明全屏过渡页）",
      "trigger_event": "onCreate / onResume 中调用 a()，检测屏幕点亮后立即 finish()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "show activity（日志）",
      "shown_text_zh": "亮屏即自动关闭的过渡页，配合外部载荷做页面覆盖/切页配合",
      "user_action_requested": "无（无取消或跳过按钮）",
      "code_anchor": "com.app.assists.TransActivity.a()"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：服务名显示为 ConfigAPKs（android:label=@string/app_name），用途说明为空白——res/xml/accessibility_service_config.xml 的 android:description 指向 res/values/strings.xml 中空字符串 access_desc",
    "应用列表/系统设置应用详情：应用名 ConfigAPKs（res/values/strings.xml app_name），无自定义图标文案",
    "AdTransActivity 与 TransActivity：Theme.Translucent.NoTitleBar.Fullscreen，运行时无任何本地文案，用户看不到说明文字",
    "真正的引导/说明文案（弹窗、WebView 教学页、悬浮遮罩）未出现在 classes.dex、res/ 或 assets/ 的可读资源中，需由 assets/cvzjem 加密载荷在运行期动态加载后渲染（不可静态还原）",
    "MReceiver 在 BOOT_COMPLETED/USER_PRESENT 后直接 startActivity 拉起前台页，构成无通知栏文案的静默回访入口"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "ConfigAPKs",
      "text_zh": "ConfigAPKs（暗示为配置/工具类应用）",
      "source_location": "res/values/strings.xml -> app_name（同时用作 android:label 与 accessibility-service android:name）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "（空字符串）",
      "text_zh": "无障碍服务用途说明为空，用户无法得知该服务会读取屏幕内容并模拟点击",
      "source_location": "res/values/strings.xml -> access_desc（<string name=\"access_desc\" />）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "show Ad activity / show activity / isExistFile : / isDevelop : / hasLightSensorManager : / hasSimCard : / isWifiProxy : / isAppNumOk :",
      "text_zh": "展示广告页 / 展示页面 / 文件存在：/ 是否开发者模式：/ 是否有光线传感器：/ 是否有 SIM 卡：/ 是否 Wi-Fi 代理：/ 应用数量是否正常：",
      "source_location": "com.app.assists.c.a（日志）被 AdTransActivity.onCreate、TransActivity.a、com.app.assists.a.a 调用",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "静态层无证据。可见的仅有回访机制：MReceiver 监听 BOOT_COMPLETED/USER_PRESENT/PACKAGE_ADDED 后调用 context.startActivity(intent2) 主动拉起前台；是否存在跳设置后 onResume 死循环重跳、Timer 定时拉起，需动态加载载荷后观察",
    "overlay_or_fake_settings": "静态层未发现 overlay 引导窗代码，但应用持有 SYSTEM_ALERT_WINDOW 权限，且两个 Activity 均为 Translucent 全屏主题，具备叠放半透明遮罩的能力；具体叠层实现位于外部加密载荷，不可静态还原",
    "restricted_settings_13plus_coaching": "无（全 DEX 无 ACTION_APPLICATION_DETAILS_SETTINGS、无 ACTION_ACCESSIBILITY_SETTINGS、无 isAccessibilityTool 相关逻辑；targetSdkVersion=21，远低于 Android 13 受限设置门槛）",
    "post_grant_anti_removal": "无静态证据。可确认 AccService 在 onAccessibilityEvent/onInterrupt 中把事件全部透传给外部载荷（setAccessEvent/setAccessInterrupt），是否用 GLOBAL_ACTION_BACK/HOME 阻止撤权无法静态判定",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "最佳拉起时机为 MReceiver 收到 BOOT_COMPLETED / USER_PRESENT 后 startActivity 拉起 AdTransActivity 的瞬间（含锁屏解锁），以及 AdTransActivity.onCreate 门禁通过后反射执行 startA 之后的 3~5 秒内——此窗口外部载荷已完成加载并绘制引导界面；单纯监测 ACTION_ACCESSIBILITY_SETTINGS 跳转对本样本无效，因为该跳转由动态载荷在运行期发起",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动/回访入口过渡页",
        "page_identifier": "com.app.assists.AdTransActivity，Theme.Translucent.NoTitleBar.Fullscreen，无标题栏、界面几乎透明",
        "why_most_useful": "这是整条诱导链唯一的静态入口，捕获它即可确认门禁通过并锁定后续引导界面的时间窗口",
        "observable_utg_signals": ["包名 com.xolo.qifyf + Activity 名 com.app.assists.AdTransActivity", "界面无文本且无标题栏的半透明全屏节点树", "紧接着出现的外部载荷渲染页面"]
      },
      {
        "page_role": "运行期引导说明页/弹窗（由加密载荷渲染）",
        "page_identifier": "非应用自身 res 布局，节点树与包内资源不匹配，常见为 WebView 或动态创建的悬浮窗",
        "why_most_useful": "无障碍诱导的核心文案与按钮只在此出现，是判定'是否诱导开启无障碍'的决定性证据",
        "observable_utg_signals": ["WebView 节点或 WindowManager 添加的悬浮窗", "包含'开启无障碍/辅助功能/权限'等关键词的按钮文本", "唯一按钮且无取消/关闭按钮的弹窗结构"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已下载的服务，条目名为 ConfigAPKs，副标题说明为空",
        "why_most_useful": "可直接验证空白 description 伪装效果，并确认用户被引导到的正是该服务开关",
        "observable_utg_signals": ["条目文本 ConfigAPKs 且下方说明文本为空", "开关节点处于关闭态、紧接被点击", "当前前台包名为 com.android.settings 且子页面为 AccessibilitySettings"]
      },
      {
        "page_role": "获权后的无障碍运行态",
        "page_identifier": "AccService 已启用，界面出现自动点击/自动翻页行为",
        "why_most_useful": "确认授权后实际用途与声明身份（ConfigAPKs）完全不符",
        "observable_utg_signals": ["无障碍服务启用状态变化", "非用户输入的连续点击/滑动事件", "界面出现广告或跳转第三方页面"]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "显著盲区：一阶段为空壳 Dropper，引导文案与按钮全在 assets/cvzjem 加密载荷中运行期解密，纯静态 UTG/资源扫描会看到'无任何诱导文案'；同时无障碍服务用途说明为空白，系统列表中无文字线索；若外部载荷采用纯图片/WebView 图片按钮承载引导文案，则必须 OCR。静态加壳本身不阻挡运行期 UTG 捕获，但需在 BOOT_COMPLETED/USER_PRESENT 拉起时机开始录制。"
  },
  "behavior_pattern_tags": [
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "COERCE_OVERLAY_STACK_ON_SETTINGS"
  ],
  "code_anchors": [
    "com.app.assists.service.AccService.onAccessibilityEvent / onInterrupt",
    "com.a.a.a.a(int, Context, Intent)（反射分派 startA/startR/startS）",
    "com.a.a.a.a(AccessibilityService, int, AccessibilityEvent)（反射分派 setAccessEvent/setAccessInterrupt）",
    "com.app.assists.AdTransActivity.onCreate",
    "com.app.assists.receiver.MReceiver.onReceive（BOOT_COMPLETED/USER_PRESENT → startActivity）",
    "res/xml/accessibility_service_config.xml + res/values/strings.xml#access_desc（空白说明）"
  ]
}
```

</details>
