# MB_028__e4a91ea474｜Gafgyt — System

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：107.9s

## 1. 一句话核心结论

- **核心申请方式**：完全不引导——应用以 "System" 名义把自己伪装成系统组件注册无障碍服务（声明可读全窗口内容与截获按键），服务本身无任何无障碍功能，仅在启用、收到事件、被关闭时反复拉起前台服务执行内置 libbot.so 僵尸网络二进制；主界面秒退无任何 UI。
- **静态可见性说明**：全包静态可见：未加壳，DEX 与资源均可完整反编译，解包目录不含 assets、HTML 或加密载荷；无动态加载与远端配置下发。唯一未深入的是 libbot.so 内部的 C2 与指令逻辑，但不影响无障碍相关页面流转的判定（该应用根本不存在引导页面）。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `e4a91ea474b3e1f751bd4467feca7d28b20e08819f9f05c4b95151397584b073` |
| 包名 / 年份 | `com.chingusapk.juan` / 2026 |
| 家族 / 品类 | **Gafgyt**（同池样本数：1） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | System |
| 引导页宣称品牌/身份 | 伪装为 Android 系统组件（System / System Keyboard / System Screensaver / System Security） |
| 系统无障碍列表服务名 | System |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：以系统组件命名冒充：app_name=System、accessibility_description=System accessibility services、ime_name=System Keyboard、dream_name=System Screensaver、trust_agent_name=System Security、qs_tile_name=System；未使用空白/换行挤出警告、同形字、多 activity-alias，也未声明伪造 isAccessibilityTool。另以「主 Activity 秒退无 UI」降低用户察觉。 |
| 无障碍服务类名 | `com.chingusapk.juan.AccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `BIND_DEVICE_ADMIN, BIND_NOTIFICATION_LISTENER_SERVICE, PACKAGE_USAGE_STATS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | System accessibility services |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.chingusapk.juan.MainActivity（LAUNCHER） | onCreate | 原生Activity | 无 | 无操作要求，界面一闪即退，无取消/跳过按钮 | `com.chingusapk.juan.MainActivity#onCreate` |
| 2 | 引导说明页 | 不存在 | 无 | 不可静态还原 | 无 | 无 | `search_text_in_app 全包零命中；解包目录无 assets/` |
| 3 | 跳无障碍设置 | 无程序化跳转；仅由用户自行在 设置 → 无障碍 中发现并启用 | 用户手动进入系统设置（应用不主动跳转） | 系统无障碍页 | **原文**：System / System accessibility services<br>**译注**：系统无障碍列表与详情页中显示的服务名称为「System」，描述为「系统无障碍服务」，使该服务看起来属于操作系统 | 用户自行点开开关启用，应用侧无任何提示、无教学、无反馈 | `res/values/strings.xml#L3-L4；res/xml/accessibility_service_config.xml` |
| 4 | 获权后动作 | com.chingusapk.juan.AccessibilityService → com.chingusapk.juan.KyorijService | onServiceConnected | 不可静态还原 | 无 | 无 | `com.chingusapk.juan.AccessibilityService#onServiceConnected；com.chingusapk.juan.KyorijService#doWork` |
| 5 | 拒权反馈循环 | com.chingusapk.juan.AccessibilityService（onAccessibilityEvent / onDestroy） | 任意无障碍事件回调、或用户关闭该无障碍服务触发 onDestroy | 不可静态还原 | 无 | 无 | `com.chingusapk.juan.AccessibilityService#onAccessibilityEvent / #onDestroy` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项与服务详情页：名称「System」（android:label=@string/app_name），描述「System accessibility services」（@string/accessibility_description）
- 系统输入法列表中显示「System Keyboard」（@string/ime_name，IMEService）
- 系统屏保/互动屏保列表中显示「System Screensaver」（@string/dream_name，DreamService）
- 系统信任代理设置中显示「System Security」（@string/trust_agent_name，TrustAgentService）
- 快捷设置磁贴显示「System」（@string/qs_tile_name，QSTileService）
- 应用内：无任何文字呈现——MainActivity 不调用 setContentView，无 layout 引导内容、无 Dialog、无 WebView、无 assets/HTML、无悬浮窗

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | System | 系统（应用桌面显示名与无障碍服务名） | `res/values/strings.xml: app_name / qs_tile_name` | 假反诈安全 |
| en | System accessibility services | 系统无障碍服务 | `res/values/strings.xml: accessibility_description → res/xml/accessibility_service_config.xml android:description` | 未知 |
| en | System Keyboard | 系统键盘 | `res/values/strings.xml: ime_name → res/xml/method.xml` | 未知 |
| en | System Screensaver | 系统屏保 | `res/values/strings.xml: dream_name` | 未知 |
| en | System Security | 系统安全 | `res/values/strings.xml: trust_agent_name → res/xml/trust_agent.xml` | 假反诈安全 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：无 UI 层面的拒权反馈：应用从不检测无障碍是否启用，也从不弹窗催促；仅在服务已启用后，任意无障碍事件回调与 onDestroy（用户撤权时）都会立即 startForegroundService(KyorijService) 重新拉起后台执行链，实现关闭即重启。
- **遮罩叠层 / 高仿系统设置页**：无。未使用 SYSTEM_ALERT_WINDOW 叠放引导遮罩，也未高仿系统无障碍开关页；应用界面完全空白且秒退。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未出现「应用详情 → 右上角菜单 → 允许受限设置」教学，也无 Session 安装器绕过代码。
- **获权后即时行为与防撤权机制**：无自点确认或 GLOBAL_ACTION_BACK/HOME 阻止撤权；对抗方式为 onDestroy 中重新 startForegroundService，使服务进程被反复重建。
- **良性降级 / 替代方案**：无。无手动模式、无 ADB 说明、无降级路径；无障碍未启用时应用不呈现任何替代界面。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：本样本无引导弹窗可等待，建议以「无障碍服务被启用」与「主 Activity 秒退」两个瞬间为锚：在启动 MainActivity 后 1s 内监测其 finish 与前台上报；随后手动进入 设置→无障碍 启用「System」后，立即抓取无障碍列表项与随后弹出的前台服务通知（KyorijService，channel kyorij_channel，NOTIFICATION_ID=1）。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区不是加壳，而是「无引导界面」：纯 UTG 页面流检测会因应用全程零 UI 而漏判，必须以无障碍服务列表项命名伪装 + 启用后前台服务通知出现作为替代信号。此外 libbot.so 的 C2 与攻击指令未做函数级逆向，属静态可见性之外的未决项。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已安装服务中名为「System」的条目，详情页描述为「System accessibility services」 | 该页是判定身份伪装的唯一用户可见载体；应用自身无任何界面，伪装全部体现在系统设置呈现的系统级命名上。 | 服务名称为 System 且描述为 System accessibility services；包名 com.chingusapk.juan 与显示名 System 明显不符；详情页无可理解的辅助功能说明 |
| **冷启动后的前台服务通知页** | 通知栏出现 KyorijService 的前台通知（channel kyorij_channel，含 [AUTO]/[BOT] 日志行） | 证明无障碍服务被启用后立即拉起后台载荷执行链，是无障碍权限与 libbot.so 执行之间的运行期连接证据。 | 通知标题/内容含 Kyorij 或 [AUTO] 前缀日志；通知在无任何用户界面交互后自行出现；通知持续存在且无法通过应用 UI 关闭 |
| **撤权返回后的设置页** | 在无障碍详情页关闭「System」开关后返回的界面 | 验证 onDestroy 重拉机制：关闭后服务立即重建，可捕捉设置页开关状态与实际运行状态不一致的对抗行为。 | 开关关闭后前台服务通知仍存在；通知或进程日志出现新的 [AUTO] 启动记录；再次进入无障碍页时开关状态反复 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.chingusapk.juan.AccessibilityService#onServiceConnected`
- `com.chingusapk.juan.AccessibilityService#onDestroy`
- `com.chingusapk.juan.KyorijService#doWork`
- `com.chingusapk.juan.KyorijService#getBotBinary`
- `res/xml/accessibility_service_config.xml`
- `res/values/strings.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**该样本不存在任何“无障碍权限引导”页面流转——这是本次定向审计最关键的否定性结论。** 静态可见性完整（无壳、DEX/资源未加密、无 assets/HTML），因此在 9 次工具调用内即可排除引导链。

- **没有引导界面**：全包检索 `ACTION_ACCESSIBILITY_SETTINGS`、`ACTION_APPLICATION_DETAILS_SETTINGS`、`android.settings`、`ACTION_MANAGE_OVERLAY_PERMISSION`、`isAccessibilityTool` 全部零命中；解包目录不含 `assets/`、任何 HTML、任何引导 layout。唯一 Activity 的 [MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.chingusapk.juan.MainActivity#onCreate>) 只做 `startService(KyorijService)` + `finish()`，**零 UI、秒退**。无弹窗、无悬浮窗、无遮罩、无受限设置教学、无拒权反馈循环。
- **无障碍服务的真实用途是驻留触发器**：类里没有任何无障碍逻辑，`onServiceConnected`/`onAccessibilityEvent`/`onDestroy` 三个方法体完全相同，都只是 `startForegroundService(KyorijService)`——包括用户**关闭**服务时（`onDestroy`）也会立刻重新拉起。
- **权限获取靠伪装而非引导**：[strings.xml](<resource-unit:#1 file:res/values/strings.xml#L3-L8>) 把 `app_name`、`accessibility_description`、`ime_name`、`dream_name`、`trust_agent_name` 全部命名为 "System"/"System Keyboard"/"System Screensaver"/"System Security"，让用户在系统无障碍列表里看到的是一个自称系统组件的条目；配置声明 `typeAllMask` + `canRetrieveWindowContent` + `flagRequestFilterKeyEvents` + `flagRetrieveInteractiveWindows`（可读全窗口内容、截获按键）。
- **获权即执行**：[KyorijService#doWork()](<resource-unit:#1.dex1 code:com.chingusapk.juan.KyorijService#doWork>) 从 `nativeLibraryDir` 取 [libbot.so](<resource-unit:#1.so1 file:all>)，用 `ProcessBuilder(bin, "apk")` 当独立可执行文件启动，退出后 2s→60s 退避无限重试。
- **UTG 视角的含义**：本样本属于“无引导页”类型，UI 上不会出现任何教程/警告话术；判别信号只能来自**无障碍列表项自称 System**、**Activity 秒退后出现前台服务通知**、以及**设置页返回瞬间服务被重新拉起**。

已登记风险 R-001（malware_trojan / high，source_mode=autonomous_audit）。未决：libbot.so 的 C2 与指令集未做函数级逆向，故僵尸网络具体危害范围未在结论中确认。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全包静态可见：未加壳，DEX 与资源均可完整反编译，解包目录不含 assets、HTML 或加密载荷；无动态加载与远端配置下发。唯一未深入的是 libbot.so 内部的 C2 与指令逻辑，但不影响无障碍相关页面流转的判定（该应用根本不存在引导页面）。",
  "summary_one_liner": "完全不引导——应用以 \"System\" 名义把自己伪装成系统组件注册无障碍服务（声明可读全窗口内容与截获按键），服务本身无任何无障碍功能，仅在启用、收到事件、被关闭时反复拉起前台服务执行内置 libbot.so 僵尸网络二进制；主界面秒退无任何 UI。",
  "disguise_identity": {
    "app_display_name": "System",
    "claimed_brand_or_persona": "伪装为 Android 系统组件（System / System Keyboard / System Screensaver / System Security）",
    "a11y_service_label": "System",
    "identity_mismatch": true,
    "obfuscation_tricks": "以系统组件命名冒充：app_name=System、accessibility_description=System accessibility services、ime_name=System Keyboard、dream_name=System Screensaver、trust_agent_name=System Security、qs_tile_name=System；未使用空白/换行挤出警告、同形字、多 activity-alias，也未声明伪造 isAccessibilityTool。另以「主 Activity 秒退无 UI」降低用户察觉。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.chingusapk.juan.MainActivity（LAUNCHER）",
      "trigger_event": "onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无任何界面文字；Activity 不调用 setContentView，启动 KyorijService 后立即 finish()",
      "user_action_requested": "无操作要求，界面一闪即退，无取消/跳过按钮",
      "code_anchor": "com.chingusapk.juan.MainActivity#onCreate"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "不存在",
      "trigger_event": "无",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "全包检索 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS / android.settings / ACTION_MANAGE_OVERLAY_PERMISSION 均无命中，无引导弹窗、无 WebView、无 HTML、无悬浮遮罩",
      "user_action_requested": "无",
      "code_anchor": "search_text_in_app 全包零命中；解包目录无 assets/"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "无程序化跳转；仅由用户自行在 设置 → 无障碍 中发现并启用",
      "trigger_event": "用户手动进入系统设置（应用不主动跳转）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "System / System accessibility services",
      "shown_text_zh": "系统无障碍列表与详情页中显示的服务名称为「System」，描述为「系统无障碍服务」，使该服务看起来属于操作系统",
      "user_action_requested": "用户自行点开开关启用，应用侧无任何提示、无教学、无反馈",
      "code_anchor": "res/values/strings.xml#L3-L4；res/xml/accessibility_service_config.xml"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "com.chingusapk.juan.AccessibilityService → com.chingusapk.juan.KyorijService",
      "trigger_event": "onServiceConnected",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无提示文字；直接 startForegroundService(KyorijService)，进入 doWork 循环，从 nativeLibraryDir 取 libbot.so 并以 ProcessBuilder(bin, \"apk\") 作为独立进程启动",
      "user_action_requested": "无",
      "code_anchor": "com.chingusapk.juan.AccessibilityService#onServiceConnected；com.chingusapk.juan.KyorijService#doWork"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "com.chingusapk.juan.AccessibilityService（onAccessibilityEvent / onDestroy）",
      "trigger_event": "任意无障碍事件回调、或用户关闭该无障碍服务触发 onDestroy",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无任何界面反馈；被关闭时 onDestroy 立即重新 startForegroundService(KyorijService)，形成关闭即重启的对抗效果（无 UI 死循环重跳）",
      "user_action_requested": "无",
      "code_anchor": "com.chingusapk.juan.AccessibilityService#onAccessibilityEvent / #onDestroy"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项与服务详情页：名称「System」（android:label=@string/app_name），描述「System accessibility services」（@string/accessibility_description）",
    "系统输入法列表中显示「System Keyboard」（@string/ime_name，IMEService）",
    "系统屏保/互动屏保列表中显示「System Screensaver」（@string/dream_name，DreamService）",
    "系统信任代理设置中显示「System Security」（@string/trust_agent_name，TrustAgentService）",
    "快捷设置磁贴显示「System」（@string/qs_tile_name，QSTileService）",
    "应用内：无任何文字呈现——MainActivity 不调用 setContentView，无 layout 引导内容、无 Dialog、无 WebView、无 assets/HTML、无悬浮窗"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "System",
      "text_zh": "系统（应用桌面显示名与无障碍服务名）",
      "source_location": "res/values/strings.xml: app_name / qs_tile_name",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "System accessibility services",
      "text_zh": "系统无障碍服务",
      "source_location": "res/values/strings.xml: accessibility_description → res/xml/accessibility_service_config.xml android:description",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "System Keyboard",
      "text_zh": "系统键盘",
      "source_location": "res/values/strings.xml: ime_name → res/xml/method.xml",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "System Screensaver",
      "text_zh": "系统屏保",
      "source_location": "res/values/strings.xml: dream_name",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "System Security",
      "text_zh": "系统安全",
      "source_location": "res/values/strings.xml: trust_agent_name → res/xml/trust_agent.xml",
      "rhetorical_frame": "假反诈安全"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "无 UI 层面的拒权反馈：应用从不检测无障碍是否启用，也从不弹窗催促；仅在服务已启用后，任意无障碍事件回调与 onDestroy（用户撤权时）都会立即 startForegroundService(KyorijService) 重新拉起后台执行链，实现关闭即重启。",
    "overlay_or_fake_settings": "无。未使用 SYSTEM_ALERT_WINDOW 叠放引导遮罩，也未高仿系统无障碍开关页；应用界面完全空白且秒退。",
    "restricted_settings_13plus_coaching": "无。未出现「应用详情 → 右上角菜单 → 允许受限设置」教学，也无 Session 安装器绕过代码。",
    "post_grant_anti_removal": "无自点确认或 GLOBAL_ACTION_BACK/HOME 阻止撤权；对抗方式为 onDestroy 中重新 startForegroundService，使服务进程被反复重建。",
    "benign_graceful_degradation": "无。无手动模式、无 ADB 说明、无降级路径；无障碍未启用时应用不呈现任何替代界面。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "本样本无引导弹窗可等待，建议以「无障碍服务被启用」与「主 Activity 秒退」两个瞬间为锚：在启动 MainActivity 后 1s 内监测其 finish 与前台上报；随后手动进入 设置→无障碍 启用「System」后，立即抓取无障碍列表项与随后弹出的前台服务通知（KyorijService，channel kyorij_channel，NOTIFICATION_ID=1）。",
    "key_pages_to_capture": [
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已安装服务中名为「System」的条目，详情页描述为「System accessibility services」",
        "why_most_useful": "该页是判定身份伪装的唯一用户可见载体；应用自身无任何界面，伪装全部体现在系统设置呈现的系统级命名上。",
        "observable_utg_signals": ["服务名称为 System 且描述为 System accessibility services", "包名 com.chingusapk.juan 与显示名 System 明显不符", "详情页无可理解的辅助功能说明"]
      },
      {
        "page_role": "冷启动后的前台服务通知页",
        "page_identifier": "通知栏出现 KyorijService 的前台通知（channel kyorij_channel，含 [AUTO]/[BOT] 日志行）",
        "why_most_useful": "证明无障碍服务被启用后立即拉起后台载荷执行链，是无障碍权限与 libbot.so 执行之间的运行期连接证据。",
        "observable_utg_signals": ["通知标题/内容含 Kyorij 或 [AUTO] 前缀日志", "通知在无任何用户界面交互后自行出现", "通知持续存在且无法通过应用 UI 关闭"]
      },
      {
        "page_role": "撤权返回后的设置页",
        "page_identifier": "在无障碍详情页关闭「System」开关后返回的界面",
        "why_most_useful": "验证 onDestroy 重拉机制：关闭后服务立即重建，可捕捉设置页开关状态与实际运行状态不一致的对抗行为。",
        "observable_utg_signals": ["开关关闭后前台服务通知仍存在", "通知或进程日志出现新的 [AUTO] 启动记录", "再次进入无障碍页时开关状态反复"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区不是加壳，而是「无引导界面」：纯 UTG 页面流检测会因应用全程零 UI 而漏判，必须以无障碍服务列表项命名伪装 + 启用后前台服务通知出现作为替代信号。此外 libbot.so 的 C2 与攻击指令未做函数级逆向，属静态可见性之外的未决项。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED"
  ],
  "code_anchors": [
    "com.chingusapk.juan.AccessibilityService#onServiceConnected",
    "com.chingusapk.juan.AccessibilityService#onDestroy",
    "com.chingusapk.juan.KyorijService#doWork",
    "com.chingusapk.juan.KyorijService#getBotBinary",
    "res/xml/accessibility_service_config.xml",
    "res/values/strings.xml"
  ]
}
```

</details>
