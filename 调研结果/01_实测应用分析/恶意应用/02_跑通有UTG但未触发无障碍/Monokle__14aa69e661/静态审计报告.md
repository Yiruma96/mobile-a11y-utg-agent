# MR_009__14aa69e661｜Monokle — BBM

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：79.3s

## 1. 一句话核心结论

- **核心申请方式**：该样本不做任何用户引导：无障碍服务未在 Manifest 声明，改为用 Xposed 钩子把 Settings.Secure 的 enabled_accessibility_services/accessibility_enabled 读取结果篡改为自身组件与 "1"，实现零交互静默授权。
- **静态可见性说明**：无障碍相关全部逻辑静态完整可见：AccessService 与其 Xposed 钩子类均在 #1.dex1 中可直接反编译；Manifest 已解码确认无 accessibilityservice 声明；res/strings.xml 与 assets/ 无相关引导资源。未见加壳、VMP 或密文载荷参与无障碍路径，16 个 .so 为常规/业务库，未参与本命题。
- **命中的行为模式标签**：`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `14aa69e661332da6bbef5adf9ce3474cf320dab38423555fd0ec9f627c907a63` |
| 包名 / 年份 | `com.bbm` / 2019 |
| 家族 / 品类 | **Monokle**（同池样本数：25） |
| 原始来源标识 | https://www.lookout.com/documents/threat-reports/lookout-discovers-monokle-threat-report.pdf |
| 桌面显示名 | BBM |
| 引导页宣称品牌/身份 | BlackBerry BBM（com.bbm 正版外壳，应用名 BBM / @string/app_name），真实载荷自称为 com.system.security_update、包名前缀 com.smartagents.system_service |
| 系统无障碍列表服务名 | 无——AccessService 未在 AndroidManifest 中声明为 <service>，系统无障碍列表不会出现该项，也无 android:label / android:description |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：载荷以 com.system.security_update（“系统安全更新”）与 com.smartagents.system_service 的伪系统命名冒充系统服务；配套 HideApp 模块（HideApp.ActivityHider / FileConstructorModule / RuntimeModule）用于隐藏组件与文件；签名主体为 EMAILADDRESS=en@en.en, CN=en, OU=en, O=en, L=en, ST=en, C=en，非 BlackBerry 官方，属二次打包外壳。无空白/换行挤出警告、无同形字、无伪造 isAccessibilityTool。 |
| 无障碍服务类名 | `二阶段/嵌包或无直接声明` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, PACKAGE_USAGE_STATS, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 获权后动作 | com.system.security_update.xposed.keylogger.AccessService（未声明于 Manifest 的无障碍服务） | 系统/调用方读取 Settings.Secure 时被 KeyLogger$10.afterHookedMethod 篡改返回值为已启用，AccessService 随即 onServiceConnected | 系统无障碍页 | 无 | 无任何用户操作（无按钮、无取消、无跳过） | `com.system.security_update.xposed.keylogger.AccessService#onServiceConnected` |
| 2 | 获权后动作 | com.system.security_update.xposed.keylogger.AccessService#onAccessibilityEvent | onServiceConnected 设置 info.eventTypes=-1、info.flags=1 后接收全部无障碍事件（16=TYPE_VIEW_TEXT_CHANGED、32=窗口状态变化、8/16384/1） | 不可静态还原 | 无 | 无 | `com.system.security_update.xposed.keylogger.AccessService#onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 不存在任何引导/说明文字位置：AndroidManifest 中无 accessibilityservice 声明，故无 android:description / android:summary / android:settingsActivity
- res/values*/strings.xml 中 accessib 仅 1 处命中，为业务文案 msg_unmount_usb = "Sorry, the SD card is not accessible."，与无障碍无关
- assets/ 全目录检索 ccessib 与 security_update 均 0 命中，仅有 assets/html-*/*.html 的 BBM 扫描/帮助页
- 代码层无 ACTION_ACCESSIBILITY_SETTINGS 跳转（0 命中），无引导 Dialog / Activity / WebView / 悬浮窗实现

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | enabled_accessibility_services | （系统设置键名，非面向用户文案）已启用的无障碍服务列表 | `#1.dex1 com.system.security_update.xposed.keylogger.KeyLogger$10#afterHookedMethod 硬编码键名` | 未知 |
| en | com.smartagents.system_service/com.system.security_update.xposed.keylogger.AccessService | （被伪造写入的设置值）伪装成“smartagents 系统服务”的无障碍组件名 | `#1.dex1 com.system.security_update.xposed.keylogger.KeyLogger$10#afterHookedMethod 硬编码返回值` | 未知 |
| en | accessibility_enabled | （系统设置键名，非面向用户文案）无障碍总开关 | `#1.dex1 com.system.security_update.xposed.keylogger.KeyLogger$10#afterHookedMethod 硬编码键名，返回值 "1"` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：无拒绝循环——全程无用户交互点，不存在 onResume 重跳或定时器拉起；授权状态由 Xposed 钩子对 Settings.Secure.getStringForUser 的返回值覆写实现，与用户操作无关
- **遮罩叠层 / 高仿系统设置页**：无：无半透明引导遮罩、无全屏悬浮窗、无高仿系统无障碍开关页（SYSTEM_ALERT_WINDOW 权限存在但未用于无障碍引导）
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：获权后无需自点确认；通过钩子持续覆写 enabled_accessibility_services 与 accessibility_enabled 使系统读取值恒为已启用，用户在系统设置中无法看到或撤销该服务；另有 HideApp 模块（ActivityHider、FileConstructorModule、RuntimeModule）隐藏组件与文件以增强驻留
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：本样本无可等待的引导页跳转。纯 UTG 应在两方面挂钩：①监测 com.bbm 进程启动后是否加载 Xposed 模块（zygote 注入路径 com.system.security_update.xposed.XposedEntryPoint.initZygote / KeyLogger.handleLoadPackage）；②监测 Settings.Secure 读取 enabled_accessibility_services / accessibility_enabled 的调用方是否返回与系统数据库不一致的值（Hook Settings.Secure.getStringForUser 并比对 ContentResolver 原始查询）。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在显著检测盲区：本样本不使用任何界面诱导，纯 UTG 页面/文本流无法发现异常；授权证据只存在于 Xposed 钩子与 Settings 读取层，须依赖进程注入检测与 Settings.Secure 读取一致性比对。此外该载荷仅在已 Root 且安装 Xposed 框架的设备上生效，普通设备与模拟器上 AccessService 永不启动，动态分析可能完全观察不到无障碍行为。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **系统无障碍服务列表项（对照组）** | 系统“无障碍”设置页中不应出现 com.system.security_update 相关条目；若出现且名称为 system_service/系统更新类，则直接命中伪装 | 本样本授权完全绕过该页，捕获该页可证明“无引导、无声明、列表无项”，与 R-001 结论互证 | 列表内不存在 com.system.security_update.xposed.keylogger.AccessService 条目；列表内不存在任何 com.smartagents.system_service 前缀服务 |
| **冷启动界面（外壳掩护层）** | com.bbm.ui.activities.StartupActivity（LAUNCHER）→ MainActivity，正常 BBM 登录/聊天界面 | 确认用户侧看到的只是良性 BBM 外壳，全程无权限申请弹窗，排除“存在但未被发现”的引导页 | 无权限/无障碍相关对话框或说明文案；界面文本均为 BBM 业务文案（如 'A newer version of BBM is required.'） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.system.security_update.xposed.keylogger.KeyLogger$10#afterHookedMethod`
- `com.system.security_update.xposed.keylogger.KeyLogger#handleLoadPackage`
- `com.system.security_update.xposed.keylogger.AccessService#onServiceConnected`
- `com.system.security_update.xposed.keylogger.AccessService#onAccessibilityEvent`
- `com.system.security_update.xposed.XposedEntryPoint#initZygote`
- `AndroidManifest.xml（无 accessibilityservice 声明；存在 com.system.security_update.BackgroundService 与 7 个 com.system.security_update.receivers.*）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（围绕“无障碍权限引导流转”）

**结论：该样本完全不存在面向用户的无障碍权限引导链路（UTG 视角下无任何引导页可捕获），其授权通过 Xposed 钩子伪造系统设置读取值实现“零交互”授权。**

已核验要点：

1. **Manifest 无无障碍服务声明**：全量检索 `AndroidManifest.xml` 中 `BIND_ACCESSIBILITY` / `accessibilityservice` 均为 0 命中；`com.system.security_update.xposed.keylogger.AccessService` 未作为 `<service>` 出现。因此系统“无障碍”列表里**根本不会出现该服务项**，`android:description`、`android:summary` 等标签也无从存在（与预筛 `无障碍服务类=[]` 一致）。
2. **无 `ACTION_ACCESSIBILITY_SETTINGS` 跳转点**：`#1.dex1` 中该 action 与 `ACTION_APPLICATION_DETAILS_SETTINGS` 字符串均无命中；预筛 DEX 线索里的 `A11Y_OVERLAY` / `WATCH_SETTINGS` 在本样本中并未落实为跳转或遮罩实现。
3. **无任何本地引导资源**：`res/values*/strings.xml` 中 `accessib` 仅命中 1 处业务文案（`msg_unmount_usb` = "Sorry, the SD card is not accessible."），与无障碍无关；`assets/` 全目录检索 `ccessib` 与 `security_update` 均 0 命中（仅有 BBM 业务帮助 HTML）。
4. **真实授权机制在 Xposed 层**：[KeyLogger$10.afterHookedMethod()](<resource-unit:#1.dex1 code:com.system.security_update.xposed.keylogger.KeyLogger$10#afterHookedMethod>) 在 `Settings.Secure.getStringForUser` 返回后按 key 覆写结果——`enabled_accessibility_services` → `"com.smartagents.system_service/com.system.security_update.xposed.keylogger.AccessService"`，`accessibility_enabled` → `"1"`；即令所有读取方“看到”无障碍已开启且本服务在列。
5. **服务能力入口**：[AccessService.onServiceConnected()](<resource-unit:#1.dex1 code:com.system.security_update.xposed.keylogger.AccessService#onServiceConnected>) 设置 `eventTypes=-1`、`flags=1`（全部事件类型），[AccessService.onAccessibilityEvent()](<resource-unit:#1.dex1 code:com.system.security_update.xposed.keylogger.AccessService#onAccessibilityEvent>) 以事件 16/32/8 维护 `sForegroundPackage` 与 `sAppToAccessBuffer`，逐应用截取界面文本。
6. **加载路径**：[KeyLogger.handleLoadPackage()](<resource-unit:#1.dex1 code:com.system.security_update.xposed.keylogger.KeyLogger#handleLoadPackage>) → `hookContextAttach` 钩 `Application.attach`，由 [XposedEntryPoint.initZygote()](<resource-unit:#1.dex1 code:com.system.security_update.xposed.XposedEntryPoint#initZygote>) / `handleLoadPackage` 在 zygote 阶段注入；Manifest 中配套驻留组件为 `com.system.security_update.BackgroundService` 及 7 个 `com.system.security_update.receivers.*` 广播接收器（`BIND_ACCESSIBILITY` 权限缺失，服务权限为自定义 `com.system.security_update.permission.SERVICE`）。

**对 UTG 检测的意义**：本样本属于“无引导页 + 静默提权”型，纯运行期 UTG 文本/页面流基本无法捕获诱导界面；判别应转向“进程内是否加载 Xposed 模块 / 系统无障碍列表与 Settings 值是否被篡改”的运行时证据（需 Root+Xposed 环境，否则该服务永不生效）。既有项目风险 R-001 已覆盖此命题，本轮不新增风险记录。

**覆盖边界**：未跨层逆向 16 个 `.so`（均为 libcurl/libssl/libsqlite3/gnustl/BBM 自有媒体与传输库等常规或业务组件，与无障碍引导无关）；`libbbmcore.so` 未深挖，但无障碍相关逻辑已完整落在 DEX 层可见。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍相关全部逻辑静态完整可见：AccessService 与其 Xposed 钩子类均在 #1.dex1 中可直接反编译；Manifest 已解码确认无 accessibilityservice 声明；res/strings.xml 与 assets/ 无相关引导资源。未见加壳、VMP 或密文载荷参与无障碍路径，16 个 .so 为常规/业务库，未参与本命题。",
  "summary_one_liner": "该样本不做任何用户引导：无障碍服务未在 Manifest 声明，改为用 Xposed 钩子把 Settings.Secure 的 enabled_accessibility_services/accessibility_enabled 读取结果篡改为自身组件与 \"1\"，实现零交互静默授权。",
  "disguise_identity": {
    "app_display_name": "BBM",
    "claimed_brand_or_persona": "BlackBerry BBM（com.bbm 正版外壳，应用名 BBM / @string/app_name），真实载荷自称为 com.system.security_update、包名前缀 com.smartagents.system_service",
    "a11y_service_label": "无——AccessService 未在 AndroidManifest 中声明为 <service>，系统无障碍列表不会出现该项，也无 android:label / android:description",
    "identity_mismatch": true,
    "obfuscation_tricks": "载荷以 com.system.security_update（“系统安全更新”）与 com.smartagents.system_service 的伪系统命名冒充系统服务；配套 HideApp 模块（HideApp.ActivityHider / FileConstructorModule / RuntimeModule）用于隐藏组件与文件；签名主体为 EMAILADDRESS=en@en.en, CN=en, OU=en, O=en, L=en, ST=en, C=en，非 BlackBerry 官方，属二次打包外壳。无空白/换行挤出警告、无同形字、无伪造 isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "获权后动作",
      "screen_or_component": "com.system.security_update.xposed.keylogger.AccessService（未声明于 Manifest 的无障碍服务）",
      "trigger_event": "系统/调用方读取 Settings.Secure 时被 KeyLogger$10.afterHookedMethod 篡改返回值为已启用，AccessService 随即 onServiceConnected",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无任何界面呈现；系统无障碍列表中不出现该服务",
      "user_action_requested": "无任何用户操作（无按钮、无取消、无跳过）",
      "code_anchor": "com.system.security_update.xposed.keylogger.AccessService#onServiceConnected"
    },
    {
      "step": 2,
      "stage": "获权后动作",
      "screen_or_component": "com.system.security_update.xposed.keylogger.AccessService#onAccessibilityEvent",
      "trigger_event": "onServiceConnected 设置 info.eventTypes=-1、info.flags=1 后接收全部无障碍事件（16=TYPE_VIEW_TEXT_CHANGED、32=窗口状态变化、8/16384/1）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "后台静默记录前台包名与界面文本（sForegroundPackage / sAppToAccessBuffer），无界面",
      "user_action_requested": "无",
      "code_anchor": "com.system.security_update.xposed.keylogger.AccessService#onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "不存在任何引导/说明文字位置：AndroidManifest 中无 accessibilityservice 声明，故无 android:description / android:summary / android:settingsActivity",
    "res/values*/strings.xml 中 accessib 仅 1 处命中，为业务文案 msg_unmount_usb = \"Sorry, the SD card is not accessible.\"，与无障碍无关",
    "assets/ 全目录检索 ccessib 与 security_update 均 0 命中，仅有 assets/html-*/*.html 的 BBM 扫描/帮助页",
    "代码层无 ACTION_ACCESSIBILITY_SETTINGS 跳转（0 命中），无引导 Dialog / Activity / WebView / 悬浮窗实现"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "enabled_accessibility_services",
      "text_zh": "（系统设置键名，非面向用户文案）已启用的无障碍服务列表",
      "source_location": "#1.dex1 com.system.security_update.xposed.keylogger.KeyLogger$10#afterHookedMethod 硬编码键名",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "com.smartagents.system_service/com.system.security_update.xposed.keylogger.AccessService",
      "text_zh": "（被伪造写入的设置值）伪装成“smartagents 系统服务”的无障碍组件名",
      "source_location": "#1.dex1 com.system.security_update.xposed.keylogger.KeyLogger$10#afterHookedMethod 硬编码返回值",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "accessibility_enabled",
      "text_zh": "（系统设置键名，非面向用户文案）无障碍总开关",
      "source_location": "#1.dex1 com.system.security_update.xposed.keylogger.KeyLogger$10#afterHookedMethod 硬编码键名，返回值 \"1\"",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "无拒绝循环——全程无用户交互点，不存在 onResume 重跳或定时器拉起；授权状态由 Xposed 钩子对 Settings.Secure.getStringForUser 的返回值覆写实现，与用户操作无关",
    "overlay_or_fake_settings": "无：无半透明引导遮罩、无全屏悬浮窗、无高仿系统无障碍开关页（SYSTEM_ALERT_WINDOW 权限存在但未用于无障碍引导）",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "获权后无需自点确认；通过钩子持续覆写 enabled_accessibility_services 与 accessibility_enabled 使系统读取值恒为已启用，用户在系统设置中无法看到或撤销该服务；另有 HideApp 模块（ActivityHider、FileConstructorModule、RuntimeModule）隐藏组件与文件以增强驻留",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "本样本无可等待的引导页跳转。纯 UTG 应在两方面挂钩：①监测 com.bbm 进程启动后是否加载 Xposed 模块（zygote 注入路径 com.system.security_update.xposed.XposedEntryPoint.initZygote / KeyLogger.handleLoadPackage）；②监测 Settings.Secure 读取 enabled_accessibility_services / accessibility_enabled 的调用方是否返回与系统数据库不一致的值（Hook Settings.Secure.getStringForUser 并比对 ContentResolver 原始查询）。",
    "key_pages_to_capture": [
      {
        "page_role": "系统无障碍服务列表项（对照组）",
        "page_identifier": "系统“无障碍”设置页中不应出现 com.system.security_update 相关条目；若出现且名称为 system_service/系统更新类，则直接命中伪装",
        "why_most_useful": "本样本授权完全绕过该页，捕获该页可证明“无引导、无声明、列表无项”，与 R-001 结论互证",
        "observable_utg_signals": ["列表内不存在 com.system.security_update.xposed.keylogger.AccessService 条目", "列表内不存在任何 com.smartagents.system_service 前缀服务"]
      },
      {
        "page_role": "冷启动界面（外壳掩护层）",
        "page_identifier": "com.bbm.ui.activities.StartupActivity（LAUNCHER）→ MainActivity，正常 BBM 登录/聊天界面",
        "why_most_useful": "确认用户侧看到的只是良性 BBM 外壳，全程无权限申请弹窗，排除“存在但未被发现”的引导页",
        "observable_utg_signals": ["无权限/无障碍相关对话框或说明文案", "界面文本均为 BBM 业务文案（如 'A newer version of BBM is required.'）"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在显著检测盲区：本样本不使用任何界面诱导，纯 UTG 页面/文本流无法发现异常；授权证据只存在于 Xposed 钩子与 Settings 读取层，须依赖进程注入检测与 Settings.Secure 读取一致性比对。此外该载荷仅在已 Root 且安装 Xposed 框架的设备上生效，普通设备与模拟器上 AccessService 永不启动，动态分析可能完全观察不到无障碍行为。"
  },
  "behavior_pattern_tags": [
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.system.security_update.xposed.keylogger.KeyLogger$10#afterHookedMethod",
    "com.system.security_update.xposed.keylogger.KeyLogger#handleLoadPackage",
    "com.system.security_update.xposed.keylogger.AccessService#onServiceConnected",
    "com.system.security_update.xposed.keylogger.AccessService#onAccessibilityEvent",
    "com.system.security_update.xposed.XposedEntryPoint#initZygote",
    "AndroidManifest.xml（无 accessibilityservice 声明；存在 com.system.security_update.BackgroundService 与 7 个 com.system.security_update.receivers.*）"
  ]
}
```

</details>
