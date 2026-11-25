# MR_176__4da62e6802｜SpyNote — Android

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：211.9s

## 1. 一句话核心结论

- **核心申请方式**：应用无任何引导说明页，冷启动即在 onCreate/onResume 中依据字符串开关位无条件跳转系统无障碍设置页，返回未开启则反复重跳，获权后立刻禁用自身启动器图标以阻止撤权。
- **静态可见性说明**：DEX 未加壳未加密，无障碍跳转链、开关位字符串（strings.xml gp=11111）、服务标签与获权后隐藏图标逻辑全部静态可见；cctu7.c() 为 JADX 指令回退形态但控制流完整可读。无 assets HTML、无远端下发引导文案，因此不存在隐藏的引导页面需还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `4da62e68027d73abc9734b46b9dedd72fac2a529c7ad9cee5cc79e34979975ba` |
| 包名 / 年份 | `com.syria.tel` / 2020 |
| 家族 / 品类 | **SpyNote**（同池样本数：59） |
| 原始来源标识 | https://blog.lookout.com/nation-state-mobile-malware-targets-syrians-with-covid-19-lures |
| 桌面显示名 | Android |
| 引导页宣称品牌/身份 | 无任何品牌/身份宣称——直接冒用系统名 Android |
| 系统无障碍列表服务名 | Android |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务 label 与 app_name 同为 "Android" 冒充系统组件；android:description 完全缺失，系统无障碍列表中无任何用途说明；服务与 Activity 名均为 cctuN 混淆；开关位藏在 strings.xml 名为 gp 的 "11111" 字符串中按字符位解析，而非正常配置项 |
| 无障碍服务类名 | `com.syria.tel.cctu1` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.syria.tel.cctu7（唯一 LAUNCHER Activity，Theme.Translucent.NoTitleBar，excludeFromRecents=true） | 用户点击桌面图标 → onCreate(Bundle) | 原生Activity | 无 | 无任何可交互控件，无可取消/跳过选项 | `com.syria.tel.cctu7.onCreate` |
| 2 | 业务功能触发 | cctu7.c() → cctu7.b() → 新线程执行 cctu7$1.run | onCreate / onResume 均调用 c()；c() 末尾调用 b() 启动 Thread | 不可静态还原 | 无 | 无（用户无感知） | `com.syria.tel.cctu7.c / com.syria.tel.cctu7.b / com.syria.tel.cctu7$1.run` |
| 3 | 跳无障碍设置 | Intent(android.settings.ACCESSIBILITY_SETTINGS)，flags=268435456（NEW_TASK），startActivity 拉起系统无障碍设置页 | cctu7$1.run 中判断 string.charAt(1)=='1' && !cctu11.j（服务未连接）成立 | 系统无障碍页 | **原文**：无应用自定义文案；系统页列表中服务项显示为 "Android"（无描述）<br>**译注**：直接跳到系统「无障碍」设置页，用户在列表中看到一个名为 Android 的无说明服务开关 | 要求用户在该系统页面手动找到并开启名为 Android 的无障碍服务；应用侧不提供取消/跳过按钮 | `com.syria.tel.cctu7$1.run` |
| 4 | 拒权反馈循环 | 用户从系统设置返回 → cctu7.onResume → c() → b() → cctu7$1.run | Activity onResume 回调 | 系统无障碍页 | 无 | 只能开启服务或强制退出应用；无安全降级路径 | `com.syria.tel.cctu7.onResume / com.syria.tel.cctu7$1.run` |
| 5 | 获权后动作 | com.syria.tel.cctu1（无障碍服务）onServiceConnected；随后 cctu1.b() → cctu1.a() 禁用 cctu7 组件 | 系统绑定无障碍服务成功回调 onServiceConnected | 不可静态还原 | 无 | 无（用户无法再通过桌面图标回到应用撤销授权） | `com.syria.tel.cctu1.onServiceConnected / com.syria.tel.cctu1.a()` |
| 6 | 获权后动作 | com.syria.tel.cctu1.onAccessibilityEvent + com.syria.tel.cctu11 上报通道 | 任意应用的窗口内容变化事件（TYPE_ALL） | 不可静态还原 | 无 | 无 | `com.syria.tel.cctu1.onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 无任何应用侧引导/说明文字：cctu7 未 setContentView，未使用 AlertDialog/Toast/WebView/Overlay，res 下无 assets HTML，strings.xml 无无障碍相关文案
- 唯一的身份呈现位于系统无障碍服务列表：服务 label = @string/s = "Android"，且无 android:description，列表中不显示任何用途说明
- 桌面图标名 = @string/app_name = "Android"（伪装系统组件）
- strings.xml 中 gp="11111" 为纯开关位字符串，非用户可见文案
- 获权后启动器组件被禁用，桌面不再呈现任何应用入口

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Android | 安卓（系统名） | `res/values/strings.xml key=app_name 与 key=s` | 假反诈安全 |
| en | 11111 | 11111（开关位：第0位=禁用启动器组件，第1位=跳无障碍设置，第2位=抓应用图标，第3位=申请设备管理器，第4位=root探测） | `res/values/strings.xml key=gp` | 未知 |
| en | 82.137.218.185 | 82.137.218.185（C2 服务器地址） | `res/values/strings.xml key=h` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：onResume 无条件再次执行 c()→b()→cctu7$1.run，只要 cctu11.j 仍为 false 就再次 startActivity(ACTION_ACCESSIBILITY_SETTINGS)；用户从系统设置返回即被立刻重跳，无计数器上限也无退出提示
- **遮罩叠层 / 高仿系统设置页**：无：未使用 SYSTEM_ALERT_WINDOW 叠遮罩、无高仿无障碍开关页、无 GIF/图片指引（权限虽已声明但本链路未使用）
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdk=22，不涉及 Android 13 受限设置教学）
- **获权后即时行为与防撤权机制**：有：onServiceConnected 中调用 a()，通过 PackageManager.setComponentEnabledSetting(ComponentName(ctx, cctu7.class), COMPONENT_ENABLED_STATE_DISABLED=2, DONT_KILL_APP=1) 禁用启动器入口，使用户无法从桌面回到应用关闭服务；未使用 GLOBAL_ACTION_BACK/HOME 干扰撤权
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测冷启动后 1~3 秒内是否出现 Intent action=android.settings.ACCESSIBILITY_SETTINGS 的 Activity 切换（本应用为 0 步直达）；同时监测启动后是否从未渲染任何应用自有界面（半透明 Activity 立即跳转），以及授权完成后桌面图标/启动器组件是否消失
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：本应用无图引导、无温和外壳，UTG 文本检测盲区很小；但需注意：①界面为半透明空 Activity，若仅截图判定可能误认为“无界面闪退”，应结合 Activity 切换与 Intent action 判断；②获权后启动图标被禁用，若 UTG 流程依赖从桌面反复启动应用会失败，应以 adb 直接 am start 或监测服务状态复核；③另存在 raw 资源内嵌 APK 的二阶段投放（cctu7$2.run 落盘 base.apk 后拉起安装），该投放可能安装新包并切换外层身份，UTG 需持续跟踪 PACKAGE_ADDED 后的新前台应用。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动瞬间的应用界面（半透明空 Activity）** | com.syria.tel.cctu7，Theme.Translucent.NoTitleBar，无任何 View/文本 | 证明应用在跳转前完全没有说明/引导页面，属 0 步直达强制跳转，是区别于良性无障碍应用的决定性证据 | 界面节点树为空或无文字节点；Activity 停留时间极短（<1s）即切换到系统设置；无任何取消/跳过按钮节点 |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已下载的服务，条目文本 "Android"，无副标题描述 | 确认伪装身份与服务无描述，用户无法得知真实用途 | 条目文本恰为 Android；无 summary/description 文字；开关状态从 off 变为 on 的时机 |
| **拒权返回后的重跳页面** | 从系统设置按返回后 0~2 秒内再次出现 android.settings.ACCESSIBILITY_SETTINGS 页面 | 验证 onResume 死循环重跳，构成强制胁迫 | 返回后立即重复出现同一系统设置页；多次返回仍无法停留在桌面 |
| **获权后桌面状态** | Launcher 应用列表 / 桌面图标 | 验证授权后自禁用启动器组件导致的图标消失（抗撤权） | 包 com.syria.tel 在 Launcher 中不可见；设置→应用 中该包仍存在且无障碍服务为开启状态 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.syria.tel.cctu7.onCreate`
- `com.syria.tel.cctu7.onResume`
- `com.syria.tel.cctu7$1.run`
- `com.syria.tel.cctu1.onServiceConnected`
- `com.syria.tel.cctu1.a()`
- `res/values/strings.xml key=gp / key=s / key=app_name`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（UTG 运行期流转视角）

**核心事实：本应用没有任何“引导/说明”页面，而是冷启动后无条件直接跳转系统无障碍设置页，并在获权后自禁用桌面图标。**

1. **入口无 UI**：唯一 LAUNCHER Activity [cctu7](<resource-unit:#1.dex1 code:com.syria.tel.cctu7>) 的 `onCreate` 与 `onResume` 都只调用私有方法 `c()`，没有 `setContentView` 引导页、没有 AlertDialog、没有 WebView、没有 Overlay。`c()` → `b()` 起线程执行 [cctu7$1.run](<resource-unit:#1.dex1 code:com.syria.tel.cctu7$1#run>)。
2. **跳转条件来自资源字符串**：`run()` 读 `getString(2131492897)`，即 [res/values/strings.xml 的 gp="11111"](<resource-unit:#1 file:res/values/strings.xml#L36>)，判断 `charAt(1)=='1' && !cctu11.j`（服务未连接）后即 `setAction("android.settings.ACCESSIBILITY_SETTINGS")` + `startActivity`。全包仅此一处引用该 action。
3. **无取消、无降级，返回即重跳**：`onResume` 再次进入同一链路，用户从系统设置返回后若仍未开启，立即被再次推入设置页——构成拒绝/返回循环。全程没有“跳过/取消/稍后”按钮，也没有任何功能说明或隐私承诺文案。
4. **身份伪装**：`app_name`=`Android`，无障碍服务 `android:label`=`@string/s`=`Android`，**没有 `android:description`**。用户进入系统无障碍列表只看到一个名为 “Android” 的无描述服务项，无法判断真实用途。
5. **获权后立即隐藏图标**：[cctu1.onServiceConnected](<resource-unit:#1.dex1 code:com.syria.tel.cctu1#onServiceConnected>) 置 `cctu11.j=true` 并调用 `b()`，`b()` 满足开关位时调用 `a()`，以 `setComponentEnabledSetting(ComponentName(ctx, cctu7.class), 2, 1)` 把启动器组件设为 DISABLED——桌面图标消失，撤回授权路径被阻断。
6. **获权后行为**：服务设 `eventTypes=-1`（全事件）、`flags=89`，在 [onAccessibilityEvent](<resource-unit:#1.dex1 code:com.syria.tel.cctu1#onAccessibilityEvent>) 中抓取窗口全部文本、包名与应用图标，写入外置存储并上报 `82.137.218.185`（strings.xml `h`），为典型 SpyNote 键盘记录/屏幕内容窃取。
7. **附带**：`gp.charAt(3)=='1'` 时还会 `ACTION_ADD_DEVICE_ADMIN` 申请设备管理器；`charAt(4)=='1'` 时 `Runtime.exec("su")` 执行 `screencap` 探测 root；raw 资源中的内嵌 APK 由 `cctu7$2.run` 落盘 `base.apk` 并以 `application/vnd.android.package-archive` 拉起安装或 `pm install -r`（一阶段投放）。

**覆盖边界**：`cctu7.c()` 反编译为 JADX 指令回退，但控制流与跳转点已明确；未见加壳/密文，`assets/` 无 HTML，字符串资源即开关配置，静态可见性完整。

```json
{
  "static_visibility": "clear",
  "visibility_note": "DEX 未加壳未加密，无障碍跳转链、开关位字符串（strings.xml gp=11111）、服务标签与获权后隐藏图标逻辑全部静态可见；cctu7.c() 为 JADX 指令回退形态但控制流完整可读。无 assets HTML、无远端下发引导文案，因此不存在隐藏的引导页面需还原。",
  "summary_one_liner": "应用无任何引导说明页，冷启动即在 onCreate/onResume 中依据字符串开关位无条件跳转系统无障碍设置页，返回未开启则反复重跳，获权后立刻禁用自身启动器图标以阻止撤权。",
  "disguise_identity": {
    "app_display_name": "Android",
    "claimed_brand_or_persona": "无任何品牌/身份宣称——直接冒用系统名 Android",
    "a11y_service_label": "Android",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务 label 与 app_name 同为 \"Android\" 冒充系统组件；android:description 完全缺失，系统无障碍列表中无任何用途说明；服务与 Activity 名均为 cctuN 混淆；开关位藏在 strings.xml 名为 gp 的 \"11111\" 字符串中按字符位解析，而非正常配置项"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.syria.tel.cctu7（唯一 LAUNCHER Activity，Theme.Translucent.NoTitleBar，excludeFromRecents=true）",
      "trigger_event": "用户点击桌面图标 → onCreate(Bundle)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面内容：onCreate 仅调用 super.onCreate(bundle) 与私有方法 c()，未调用 setContentView，Activity 为半透明无标题主题，用户几乎看不到界面",
      "user_action_requested": "无任何可交互控件，无可取消/跳过选项",
      "code_anchor": "com.syria.tel.cctu7.onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "cctu7.c() → cctu7.b() → 新线程执行 cctu7$1.run",
      "trigger_event": "onCreate / onResume 均调用 c()；c() 末尾调用 b() 启动 Thread",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "后台线程读取 strings.xml 中 gp=\"11111\"，按 charAt(1)=='1' 判定是否执行无障碍跳转",
      "user_action_requested": "无（用户无感知）",
      "code_anchor": "com.syria.tel.cctu7.c / com.syria.tel.cctu7.b / com.syria.tel.cctu7$1.run"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "Intent(android.settings.ACCESSIBILITY_SETTINGS)，flags=268435456（NEW_TASK），startActivity 拉起系统无障碍设置页",
      "trigger_event": "cctu7$1.run 中判断 string.charAt(1)=='1' && !cctu11.j（服务未连接）成立",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无应用自定义文案；系统页列表中服务项显示为 \"Android\"（无描述）",
      "shown_text_zh": "直接跳到系统「无障碍」设置页，用户在列表中看到一个名为 Android 的无说明服务开关",
      "user_action_requested": "要求用户在该系统页面手动找到并开启名为 Android 的无障碍服务；应用侧不提供取消/跳过按钮",
      "code_anchor": "com.syria.tel.cctu7$1.run"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "用户从系统设置返回 → cctu7.onResume → c() → b() → cctu7$1.run",
      "trigger_event": "Activity onResume 回调",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "若 cctu11.j 仍为 false（未开启服务），立即再次 startActivity 拉起无障碍设置页，形成无法退出的循环",
      "user_action_requested": "只能开启服务或强制退出应用；无安全降级路径",
      "code_anchor": "com.syria.tel.cctu7.onResume / com.syria.tel.cctu7$1.run"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "com.syria.tel.cctu1（无障碍服务）onServiceConnected；随后 cctu1.b() → cctu1.a() 禁用 cctu7 组件",
      "trigger_event": "系统绑定无障碍服务成功回调 onServiceConnected",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务置 cctu11.j=true、eventTypes=-1、flags=89 开始全事件监听；同时将启动器组件 cctu7 设为 COMPONENT_ENABLED_STATE_DISABLED，桌面图标消失",
      "user_action_requested": "无（用户无法再通过桌面图标回到应用撤销授权）",
      "code_anchor": "com.syria.tel.cctu1.onServiceConnected / com.syria.tel.cctu1.a()"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.syria.tel.cctu1.onAccessibilityEvent + com.syria.tel.cctu11 上报通道",
      "trigger_event": "任意应用的窗口内容变化事件（TYPE_ALL）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "抓取当前窗口全部文本（AccessibilityEvent.getText()）、包名、应用图标，写入外置存储 config<日期>.log，并上报至 82.137.218.185",
      "user_action_requested": "无",
      "code_anchor": "com.syria.tel.cctu1.onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "无任何应用侧引导/说明文字：cctu7 未 setContentView，未使用 AlertDialog/Toast/WebView/Overlay，res 下无 assets HTML，strings.xml 无无障碍相关文案",
    "唯一的身份呈现位于系统无障碍服务列表：服务 label = @string/s = \"Android\"，且无 android:description，列表中不显示任何用途说明",
    "桌面图标名 = @string/app_name = \"Android\"（伪装系统组件）",
    "strings.xml 中 gp=\"11111\" 为纯开关位字符串，非用户可见文案",
    "获权后启动器组件被禁用，桌面不再呈现任何应用入口"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Android",
      "text_zh": "安卓（系统名）",
      "source_location": "res/values/strings.xml key=app_name 与 key=s",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "11111",
      "text_zh": "11111（开关位：第0位=禁用启动器组件，第1位=跳无障碍设置，第2位=抓应用图标，第3位=申请设备管理器，第4位=root探测）",
      "source_location": "res/values/strings.xml key=gp",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "82.137.218.185",
      "text_zh": "82.137.218.185（C2 服务器地址）",
      "source_location": "res/values/strings.xml key=h",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "onResume 无条件再次执行 c()→b()→cctu7$1.run，只要 cctu11.j 仍为 false 就再次 startActivity(ACTION_ACCESSIBILITY_SETTINGS)；用户从系统设置返回即被立刻重跳，无计数器上限也无退出提示",
    "overlay_or_fake_settings": "无：未使用 SYSTEM_ALERT_WINDOW 叠遮罩、无高仿无障碍开关页、无 GIF/图片指引（权限虽已声明但本链路未使用）",
    "restricted_settings_13plus_coaching": "无（targetSdk=22，不涉及 Android 13 受限设置教学）",
    "post_grant_anti_removal": "有：onServiceConnected 中调用 a()，通过 PackageManager.setComponentEnabledSetting(ComponentName(ctx, cctu7.class), COMPONENT_ENABLED_STATE_DISABLED=2, DONT_KILL_APP=1) 禁用启动器入口，使用户无法从桌面回到应用关闭服务；未使用 GLOBAL_ACTION_BACK/HOME 干扰撤权",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测冷启动后 1~3 秒内是否出现 Intent action=android.settings.ACCESSIBILITY_SETTINGS 的 Activity 切换（本应用为 0 步直达）；同时监测启动后是否从未渲染任何应用自有界面（半透明 Activity 立即跳转），以及授权完成后桌面图标/启动器组件是否消失",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动瞬间的应用界面（半透明空 Activity）",
        "page_identifier": "com.syria.tel.cctu7，Theme.Translucent.NoTitleBar，无任何 View/文本",
        "why_most_useful": "证明应用在跳转前完全没有说明/引导页面，属 0 步直达强制跳转，是区别于良性无障碍应用的决定性证据",
        "observable_utg_signals": [
          "界面节点树为空或无文字节点",
          "Activity 停留时间极短（<1s）即切换到系统设置",
          "无任何取消/跳过按钮节点"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已下载的服务，条目文本 \"Android\"，无副标题描述",
        "why_most_useful": "确认伪装身份与服务无描述，用户无法得知真实用途",
        "observable_utg_signals": [
          "条目文本恰为 Android",
          "无 summary/description 文字",
          "开关状态从 off 变为 on 的时机"
        ]
      },
      {
        "page_role": "拒权返回后的重跳页面",
        "page_identifier": "从系统设置按返回后 0~2 秒内再次出现 android.settings.ACCESSIBILITY_SETTINGS 页面",
        "why_most_useful": "验证 onResume 死循环重跳，构成强制胁迫",
        "observable_utg_signals": [
          "返回后立即重复出现同一系统设置页",
          "多次返回仍无法停留在桌面"
        ]
      },
      {
        "page_role": "获权后桌面状态",
        "page_identifier": "Launcher 应用列表 / 桌面图标",
        "why_most_useful": "验证授权后自禁用启动器组件导致的图标消失（抗撤权）",
        "observable_utg_signals": [
          "包 com.syria.tel 在 Launcher 中不可见",
          "设置→应用 中该包仍存在且无障碍服务为开启状态"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "本应用无图引导、无温和外壳，UTG 文本检测盲区很小；但需注意：①界面为半透明空 Activity，若仅截图判定可能误认为“无界面闪退”，应结合 Activity 切换与 Intent action 判断；②获权后启动图标被禁用，若 UTG 流程依赖从桌面反复启动应用会失败，应以 adb 直接 am start 或监测服务状态复核；③另存在 raw 资源内嵌 APK 的二阶段投放（cctu7$2.run 落盘 base.apk 后拉起安装），该投放可能安装新包并切换外层身份，UTG 需持续跟踪 PACKAGE_ADDED 后的新前台应用。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED"
  ],
  "code_anchors": [
    "com.syria.tel.cctu7.onCreate",
    "com.syria.tel.cctu7.onResume",
    "com.syria.tel.cctu7$1.run",
    "com.syria.tel.cctu1.onServiceConnected",
    "com.syria.tel.cctu1.a()",
    "res/values/strings.xml key=gp / key=s / key=app_name"
  ]
}
```

</details>
