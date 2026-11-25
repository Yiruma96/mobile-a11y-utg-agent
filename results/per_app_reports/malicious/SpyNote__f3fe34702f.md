# MB_042__f3fe34702f｜SpyNote — media player

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：163.3s

## 1. 一句话核心结论

- **核心申请方式**：以透明无界面 Launcher Activity 冷启动后静默直跳系统无障碍设置页，无任何文字说明与取消入口，靠 onResume 循环重跳逼用户授权，获权后禁用自身图标并投放内嵌二阶段 APK。
- **静态可见性说明**：无障碍引导链完全静态可见：C7.c() 中 ACTION_ACCESSIBILITY_SETTINGS 跳转、C7$1.run() 的重跳与图标隐藏、C7$2.run() 的 raw 载荷落盘均由明文 DEX 逻辑构成，无加壳、无 AES 密文、无远端 HTML。仅两处不完整：res/raw/google.apk 在解包目录中为 0 字节（二阶段载荷内容无法核验），C11 网络指令字符串经 C11.a(long) 混淆且协议未展开。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `f3fe34702fefe9dfb8bf50f2d2ca475a8a3150f3dee3c07b09994947d540b3a1` |
| 包名 / 年份 | `cmf0.c3b5bm90zq.patch` / 2026 |
| 家族 / 品类 | **SpyNote**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | media player |
| 引导页宣称品牌/身份 | 无品牌伪装，仅以通用「媒体播放器」名义 + 随机包名 cmf0.c3b5bm90zq.patch 混淆来源 |
| 系统无障碍列表服务名 | service player |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务未声明 android:description 也未提供 accessibilityservice 元数据，系统列表无任何说明文字；服务名 service player 与桌面名 media player 均为泛化占位名；包名 cmf0.c3b5bm90zq.patch 为类 Base64 随机串；Launcher Activity 使用 Theme.Translucent.NoTitleBar + excludeFromRecents 且不 setContentView，实现零界面冷启动 |
| 无障碍服务类名 | `cmf0.c3b5bm90zq.patch.C1` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | cmf0.c3b5bm90zq.patch.C7（Launcher Activity，Theme.Translucent.NoTitleBar，excludeFromRecents=true） | 用户点击桌面图标 media player → onCreate() → 立即调用 c() | 原生Activity | **原文**：无（未调用 setContentView，窗口为透明无标题）<br>**译注**：无任何可见界面，屏幕仅闪一下或保持原样 | 无交互，用户仅感知到点击图标后无反应 | `cmf0.c3b5bm90zq.patch.C7#onCreate → C7#c` |
| 2 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS（列表项显示 service player） | C7.c() 中 getString(@string/gp).charAt(1)=='1' 且 C11.j==false 时构造 Intent 并 startActivity | 系统无障碍页 | **原文**：service player（系统无障碍列表服务名）；无 android:description 说明文字<br>**译注**：系统无障碍服务列表中直接出现名为「service player」的开关项，且无任何功能说明 | 要求用户手动找到并开启 service player 无障碍开关；本步无取消/跳过按钮，也未提供任何解释 | `cmf0.c3b5bm90zq.patch.C7$1#run（new Intent("android.settings.ACCESSIBILITY_SETTINGS"), setFlags(268435456), startActivity）` |
| 3 | 拒权反馈循环 | C7（透明 Activity）→ 系统无障碍设置页 | 用户按返回键离开设置页 → C7.onResume() → c() → b() → new Thread(C7$1).start() → 再次 startActivity(ACCESSIBILITY_SETTINGS) | 系统无障碍页 | 无 | 只能被动反复面对系统无障碍页，无「稍后再说」「跳过」入口 | `cmf0.c3b5bm90zq.patch.C7#onResume / C7#c / C7#b / C7$1#run` |
| 4 | 跳受限设置（设备管理器） | 系统对话框 android.app.action.ADD_DEVICE_ADMIN | C7$1.run() 中 gp.charAt(3)=='1' 且设备管理器未激活 → startActivityForResult(intent, 100) | 原生Dialog | **原文**：android.app.extra.ADD_EXPLANATION = ""（空字符串）<br>**译注**：系统设备管理器激活弹窗中「说明」为空，用户看不到任何申请理由 | 要求用户点击「激活」；系统弹窗自带取消 | `cmf0.c3b5bm90zq.patch.C7$1#run（ADD_DEVICE_ADMIN / ADD_EXPLANATION 空串）` |
| 5 | 获权后动作 | C7 自行 finish() + PackageManager.setComponentEnabledSetting(C7, 2, 1) | 无障碍已启用（C11.j==true）且设备管理器已激活 → C7.c() 调用 a() 并 finish() | 不可静态还原（无界面） | 无 | 无提示，用户不会收到任何通知 | `cmf0.c3b5bm90zq.patch.C7#c → C7#a()（setComponentEnabledSetting COMPONENT_ENABLED_STATE_DISABLED）` |
| 6 | 获权后动作 | 外置存储 <dir>/base.apk → 系统安装器（ACTION_VIEW application/vnd.android.package-archive）或 su pm install -r | C7.c() 满足双开关后 b() 起线程，C7$2.run() 从 res/raw 读取内嵌 APK 落盘并拉起安装 | 原生Dialog | **原文**：无（应用侧未提供任何安装说明文字）<br>**译注**：直接弹出系统安装器要求安装一个与 media player 无关的二次包 | 要求用户点击「安装」；无应用侧解释 | `cmf0.c3b5bm90zq.patch.C7$2#run（openRawResource(2131427328) → base.apk → ACTION_VIEW / su pm install）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 应用侧完全没有引导文字：无 AlertDialog、无引导 Activity、无 WebView、无 HTML/strings 说明资源、无悬浮窗遮罩（strings.xml 中仅 app_name=media player、s=service player 等占位串，无任何诱导文案）
- 唯一可见文本出现在系统无障碍列表：服务标签 service player（@string/s）；因服务未声明 android:description 且无 accessibilityservice 元数据，该项说明区为空
- 系统设备管理器激活弹窗中「说明」为 ADD_EXPLANATION=""（显式空串），呈现为空白说明
- C6 会话聊天 Activity（label=@string/s，portrait）在 onWin 场景下显示远端下发文本，与本无障碍引导链无因果关系

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | media player | 媒体播放器 | `res/values/strings.xml @string/app_name（android:label，桌面显示名）` | 良性透明说明 |
| en | service player | 播放器服务 | `res/values/strings.xml @string/s（C1 无障碍服务 android:label，亦为 C6 Activity label）` | 未知 |
| en | 00000 | 无（内部开关串，非用户可见） | `res/values/strings.xml @string/gp；被 C7.c() 与 C7$1.run() 按 charAt(0..4) 解析为图标隐藏/无障碍跳转/设备管理器/root 检测开关` | 未知 |
| en | tcp1.tunnel4.com | tcp1.tunnel4.com（C2C 服务器域名） | `res/values/strings.xml @string/h（端口 @string/p=40918，ID @string/n=JoHnDz，版本 @string/v=2.1.2.79）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：C7.onCreate() 与 onResume() 均调用 c()，c() 在无障碍未启用（C11.j==false）时经 b() 起线程执行 C7$1.run() 再次 startActivity(ACTION_ACCESSIBILITY_SETTINGS)；用户从系统设置页返回即触发 onResume 重跳，无退避、无次数上限、无提示
- **遮罩叠层 / 高仿系统设置页**：无叠层遮罩、无悬浮窗、无高仿系统设置页；纯系统无障碍页跳转（SYSTEM_ALERT_WINDOW 权限被声明但引导链未使用）
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未出现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转、未出现「受限设置」引导文案，也未使用 Session 安装器绕过（targetSdkVersion=22，机制上无需该引导）
- **获权后即时行为与防撤权机制**：有。获权且设备管理器激活后，C7.c() 调用 a() 执行 PackageManager.setComponentEnabledSetting(C7, COMPONENT_ENABLED_STATE_DISABLED=2, DONT_KILL_APP=1) 禁用自身 Launcher 组件，桌面图标消失，用户失去撤销入口；另注册 BIND_DEVICE_ADMIN 的 C2 阻止常规卸载，并由 C13/C4 监听 BOOT_COMPLETED 持久化
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到应用进程发起 startActivity 且 intent action == "android.settings.ACCESSIBILITY_SETTINGS"（或顶层窗口从 Launcher 直接变为 Settings$AccessibilitySettings）时立即拉起 UTG 采集；该跳转由 C7.c() 在冷启动约数十毫秒内无界面发起，需在点击图标前预挂 Hook
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：该样本无任何图/文诱饵，UTG 侧的关键盲区是「零界面」本身：若仅在界面出现后才拉起采集，会完全错过跳转瞬间。另注意 @string/gp 当前为 "00000"，本构建默认未开启无障碍跳转与图标隐藏，需以改写 gp 或运行时观察 charAt(1) 分支的方式验证；res/raw/google.apk 在解包目录中为 0 字节，二阶段载荷内容未核验。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动零界面阶段（跳转前 0~1s）** | 顶层 Activity 为 cmf0.c3b5bm90zq.patch.C7 且窗口透明、无 View 树、任务栈 excludeFromRecents | 证明应用不存在任何说明/告知界面，是「静默诱导」与「良性透明说明」的决定性分界证据 | 顶层 Activity 名 C7 且 contentView 为空；屏幕像素与应用启动前一致（无任何渲染）；启动后 <1s 即切换到系统 Settings 包 |
| **系统无障碍服务列表项** | com.android.settings 无障碍页中的 service player 条目，summary/description 区域为空 | 证明系统侧说明为空、服务名与媒体播放器身份不符，是身份伪装与说明缺失的直接证据 | 列表项文本 service player；条目无 description 文本节点；开关初始为 off 且无使用说明引导 |
| **设置页后返回压栈重跳页** | 连续两次出现 Settings 无障碍页，间隔约等于用户按返回键的时间 | 证明 onResume 循环重跳，用户无法以「拒绝」方式退出 | Settings 无障碍页出现 ≥2 次；两次出现之间无应用自有页面；返回键后 <1s 再次进入 Settings |
| **获权后桌面图标消失 / 二阶段安装器** | 授权并激活设备管理器后，Launcher 中 media player 图标消失；随后出现 application/vnd.android.package-archive 系统安装器 | 证明反撤权与二阶段投放，说明该无障碍权限服务于后续载荷而非任何媒体功能 | Launcher 包列表缺少 cmf0.c3b5bm90zq.patch 图标；出现 PackageInstaller 界面且来源路径含 /base.apk；设备管理器激活弹窗说明为空白 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `cmf0.c3b5bm90zq.patch.C7#onCreate`
- `cmf0.c3b5bm90zq.patch.C7#c`
- `cmf0.c3b5bm90zq.patch.C7$1#run`
- `cmf0.c3b5bm90zq.patch.C7#a（setComponentEnabledSetting 自禁用图标）`
- `cmf0.c3b5bm90zq.patch.C7$2#run`
- `res/values/strings.xml（app_name / s / gp / h / p / n / v）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**核心结论：该样本在申请无障碍权限时完全不展示任何文字说明。** 它没有引导页、弹窗、WebView 或悬浮遮罩，只采用「不可见透明 Activity 冷启动后直接跳转系统无障碍设置页」的静默方式，并利用 `onResume` 反复重跳形成拒绝循环；获得权限后，它会让自身启动图标消失。

1. **入口完全隐藏**：Launcher 入口 [C7](<resource-unit:#1.dex1 code:cmf0.c3b5bm90zq.patch.C7#onCreate>) 在 Manifest 中配置为 `Theme.Translucent.NoTitleBar` 且 `excludeFromRecents=true`，`onCreate` 不调用 `setContentView`，因此用户点击“media player”图标后不会看到任何界面，程序直接进入调度逻辑。
2. **静默跳转无障碍设置**：[C7.c()](<resource-unit:#1.dex1 code:cmf0.c3b5bm90zq.patch.C7#c>) 解析开关串 `@string/gp`（值 `"00000"`）；当 `charAt(1)=='1'` 且静态标志 `C11.j==false` 时，它构造 `new Intent("android.settings.ACCESSIBILITY_SETTINGS")` 并加上 `FLAG_ACTIVITY_NEW_TASK`，然后直接调用 `startActivity`，整个过程没有任何前置说明。
3. **拒绝后循环重跳**：[C7.onCreate()](<resource-unit:#1.dex1 code:cmf0.c3b5bm90zq.patch.C7#onCreate>) 与 `onResume()` 都调用 `c()`，再经 [C7.b()](<resource-unit:#1.dex1 code:cmf0.c3b5bm90zq.patch.C7#b>) 起线程执行 [C7$1.run()](<resource-unit:#1.dex1 code:cmf0.c3b5bm90zq.patch.C7$1#run>)。用户从设置页返回后，`onResume` 会再次触发跳转，形成“返回后又被拉起”的循环；该循环没有取消或跳过按钮。
4. **同一调度链顺带请求设备管理器**：当 `charAt(3)=='1'` 时，代码以 `ADD_EXPLANATION=""`（空说明）弹出 `ADD_DEVICE_ADMIN` 系统对话框；当 `charAt(4)=='1'` 时，[C7.d()](<resource-unit:#1.dex1 code:cmf0.c3b5bm90zq.patch.C7#d>) 用 `su` 加 `screencap` 检测 root。
5. **获得权限后隐匿**：当无障碍与设备管理器都已就绪，`c()` 会调用 `finish()` 并执行 [C7$1.run()](<resource-unit:#1.dex1 code:cmf0.c3b5bm90zq.patch.C7$1#run>)。它通过 `setComponentEnabledSetting(C7, 2, 1)` 禁用自身 Launcher 组件（前提是 `gp.charAt(0)=='1'`），使桌面图标消失，以此防止用户撤销权限或卸载应用。
6. **同一链上还有二阶段投放**：[C7$2.run()](<resource-unit:#1.dex1 code:cmf0.c3b5bm90zq.patch.C7$2#run>) 从 `res/raw` 读取内嵌安装包并写入外置存储 `.../base.apk`；没有 root 时用 `ACTION_VIEW` 拉起系统安装器，有 root 时用 `su` 执行 `pm install -r`。
7. **身份伪装**：桌面名称为 `media player`（`@string/app_name`），无障碍服务名称为 `service player`（`@string/s`）；服务没有 `android:description`，也没有 `accessibilityservice` 元数据，因此系统无障碍列表中没有说明文字。这与媒体播放器身份严重不符。
8. **配置与静态可见性**：`@string/gp="00000"` 是编译期写死的开关串，当前构建中的无障碍跳转、设备管理器、root 检测和图标隐藏开关全部为 `'0'`，即**机制完整存在，但本条样本的默认构建未开启**。C2C 参数 `tcp1.tunnel4.com:40918` 与 ID `JoHnDz` 为明文；网络指令部分在 `C11` 内做了字符串混淆（`C11.a(long)` 还原），但引导链本身完全静态可见。

> 说明：受本轮 14 次工具调用上限约束，证据图已注册（`EG-7FA3F1155617`、`EG-C9A57D0784F2`），风险台账写入未执行。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导链完全静态可见：C7.c() 中 ACTION_ACCESSIBILITY_SETTINGS 跳转、C7$1.run() 的重跳与图标隐藏、C7$2.run() 的 raw 载荷落盘均由明文 DEX 逻辑构成，无加壳、无 AES 密文、无远端 HTML。仅两处不完整：res/raw/google.apk 在解包目录中为 0 字节（二阶段载荷内容无法核验），C11 网络指令字符串经 C11.a(long) 混淆且协议未展开。",
  "summary_one_liner": "以透明无界面 Launcher Activity 冷启动后静默直跳系统无障碍设置页，无任何文字说明与取消入口，靠 onResume 循环重跳逼用户授权，获权后禁用自身图标并投放内嵌二阶段 APK。",
  "disguise_identity": {
    "app_display_name": "media player",
    "claimed_brand_or_persona": "无品牌伪装，仅以通用「媒体播放器」名义 + 随机包名 cmf0.c3b5bm90zq.patch 混淆来源",
    "a11y_service_label": "service player",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务未声明 android:description 也未提供 accessibilityservice 元数据，系统列表无任何说明文字；服务名 service player 与桌面名 media player 均为泛化占位名；包名 cmf0.c3b5bm90zq.patch 为类 Base64 随机串；Launcher Activity 使用 Theme.Translucent.NoTitleBar + excludeFromRecents 且不 setContentView，实现零界面冷启动"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "cmf0.c3b5bm90zq.patch.C7（Launcher Activity，Theme.Translucent.NoTitleBar，excludeFromRecents=true）",
      "trigger_event": "用户点击桌面图标 media player → onCreate() → 立即调用 c()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（未调用 setContentView，窗口为透明无标题）",
      "shown_text_zh": "无任何可见界面，屏幕仅闪一下或保持原样",
      "user_action_requested": "无交互，用户仅感知到点击图标后无反应",
      "code_anchor": "cmf0.c3b5bm90zq.patch.C7#onCreate → C7#c"
    },
    {
      "step": 2,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS（列表项显示 service player）",
      "trigger_event": "C7.c() 中 getString(@string/gp).charAt(1)=='1' 且 C11.j==false 时构造 Intent 并 startActivity",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "service player（系统无障碍列表服务名）；无 android:description 说明文字",
      "shown_text_zh": "系统无障碍服务列表中直接出现名为「service player」的开关项，且无任何功能说明",
      "user_action_requested": "要求用户手动找到并开启 service player 无障碍开关；本步无取消/跳过按钮，也未提供任何解释",
      "code_anchor": "cmf0.c3b5bm90zq.patch.C7$1#run（new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"), setFlags(268435456), startActivity）"
    },
    {
      "step": 3,
      "stage": "拒权反馈循环",
      "screen_or_component": "C7（透明 Activity）→ 系统无障碍设置页",
      "trigger_event": "用户按返回键离开设置页 → C7.onResume() → c() → b() → new Thread(C7$1).start() → 再次 startActivity(ACCESSIBILITY_SETTINGS)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "返回后立即被再次弹回无障碍设置页，形成反复拉起",
      "user_action_requested": "只能被动反复面对系统无障碍页，无「稍后再说」「跳过」入口",
      "code_anchor": "cmf0.c3b5bm90zq.patch.C7#onResume / C7#c / C7#b / C7$1#run"
    },
    {
      "step": 4,
      "stage": "跳受限设置（设备管理器）",
      "screen_or_component": "系统对话框 android.app.action.ADD_DEVICE_ADMIN",
      "trigger_event": "C7$1.run() 中 gp.charAt(3)=='1' 且设备管理器未激活 → startActivityForResult(intent, 100)",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "android.app.extra.ADD_EXPLANATION = \"\"（空字符串）",
      "shown_text_zh": "系统设备管理器激活弹窗中「说明」为空，用户看不到任何申请理由",
      "user_action_requested": "要求用户点击「激活」；系统弹窗自带取消",
      "code_anchor": "cmf0.c3b5bm90zq.patch.C7$1#run（ADD_DEVICE_ADMIN / ADD_EXPLANATION 空串）"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "C7 自行 finish() + PackageManager.setComponentEnabledSetting(C7, 2, 1)",
      "trigger_event": "无障碍已启用（C11.j==true）且设备管理器已激活 → C7.c() 调用 a() 并 finish()",
      "ui_carrier": "不可静态还原（无界面）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "授权后应用图标从桌面消失，用户无法再通过桌面入口撤销权限或卸载",
      "user_action_requested": "无提示，用户不会收到任何通知",
      "code_anchor": "cmf0.c3b5bm90zq.patch.C7#c → C7#a()（setComponentEnabledSetting COMPONENT_ENABLED_STATE_DISABLED）"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "外置存储 <dir>/base.apk → 系统安装器（ACTION_VIEW application/vnd.android.package-archive）或 su pm install -r",
      "trigger_event": "C7.c() 满足双开关后 b() 起线程，C7$2.run() 从 res/raw 读取内嵌 APK 落盘并拉起安装",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "无（应用侧未提供任何安装说明文字）",
      "shown_text_zh": "直接弹出系统安装器要求安装一个与 media player 无关的二次包",
      "user_action_requested": "要求用户点击「安装」；无应用侧解释",
      "code_anchor": "cmf0.c3b5bm90zq.patch.C7$2#run（openRawResource(2131427328) → base.apk → ACTION_VIEW / su pm install）"
    }
  ],
  "text_presentation_locations": [
    "应用侧完全没有引导文字：无 AlertDialog、无引导 Activity、无 WebView、无 HTML/strings 说明资源、无悬浮窗遮罩（strings.xml 中仅 app_name=media player、s=service player 等占位串，无任何诱导文案）",
    "唯一可见文本出现在系统无障碍列表：服务标签 service player（@string/s）；因服务未声明 android:description 且无 accessibilityservice 元数据，该项说明区为空",
    "系统设备管理器激活弹窗中「说明」为 ADD_EXPLANATION=\"\"（显式空串），呈现为空白说明",
    "C6 会话聊天 Activity（label=@string/s，portrait）在 onWin 场景下显示远端下发文本，与本无障碍引导链无因果关系"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "media player",
      "text_zh": "媒体播放器",
      "source_location": "res/values/strings.xml @string/app_name（android:label，桌面显示名）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "service player",
      "text_zh": "播放器服务",
      "source_location": "res/values/strings.xml @string/s（C1 无障碍服务 android:label，亦为 C6 Activity label）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "00000",
      "text_zh": "无（内部开关串，非用户可见）",
      "source_location": "res/values/strings.xml @string/gp；被 C7.c() 与 C7$1.run() 按 charAt(0..4) 解析为图标隐藏/无障碍跳转/设备管理器/root 检测开关",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "tcp1.tunnel4.com",
      "text_zh": "tcp1.tunnel4.com（C2C 服务器域名）",
      "source_location": "res/values/strings.xml @string/h（端口 @string/p=40918，ID @string/n=JoHnDz，版本 @string/v=2.1.2.79）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "C7.onCreate() 与 onResume() 均调用 c()，c() 在无障碍未启用（C11.j==false）时经 b() 起线程执行 C7$1.run() 再次 startActivity(ACTION_ACCESSIBILITY_SETTINGS)；用户从系统设置页返回即触发 onResume 重跳，无退避、无次数上限、无提示",
    "overlay_or_fake_settings": "无叠层遮罩、无悬浮窗、无高仿系统设置页；纯系统无障碍页跳转（SYSTEM_ALERT_WINDOW 权限被声明但引导链未使用）",
    "restricted_settings_13plus_coaching": "无。未出现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转、未出现「受限设置」引导文案，也未使用 Session 安装器绕过（targetSdkVersion=22，机制上无需该引导）",
    "post_grant_anti_removal": "有。获权且设备管理器激活后，C7.c() 调用 a() 执行 PackageManager.setComponentEnabledSetting(C7, COMPONENT_ENABLED_STATE_DISABLED=2, DONT_KILL_APP=1) 禁用自身 Launcher 组件，桌面图标消失，用户失去撤销入口；另注册 BIND_DEVICE_ADMIN 的 C2 阻止常规卸载，并由 C13/C4 监听 BOOT_COMPLETED 持久化",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到应用进程发起 startActivity 且 intent action == \"android.settings.ACCESSIBILITY_SETTINGS\"（或顶层窗口从 Launcher 直接变为 Settings$AccessibilitySettings）时立即拉起 UTG 采集；该跳转由 C7.c() 在冷启动约数十毫秒内无界面发起，需在点击图标前预挂 Hook",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动零界面阶段（跳转前 0~1s）",
        "page_identifier": "顶层 Activity 为 cmf0.c3b5bm90zq.patch.C7 且窗口透明、无 View 树、任务栈 excludeFromRecents",
        "why_most_useful": "证明应用不存在任何说明/告知界面，是「静默诱导」与「良性透明说明」的决定性分界证据",
        "observable_utg_signals": ["顶层 Activity 名 C7 且 contentView 为空", "屏幕像素与应用启动前一致（无任何渲染）", "启动后 <1s 即切换到系统 Settings 包"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍页中的 service player 条目，summary/description 区域为空",
        "why_most_useful": "证明系统侧说明为空、服务名与媒体播放器身份不符，是身份伪装与说明缺失的直接证据",
        "observable_utg_signals": ["列表项文本 service player", "条目无 description 文本节点", "开关初始为 off 且无使用说明引导"]
      },
      {
        "page_role": "设置页后返回压栈重跳页",
        "page_identifier": "连续两次出现 Settings 无障碍页，间隔约等于用户按返回键的时间",
        "why_most_useful": "证明 onResume 循环重跳，用户无法以「拒绝」方式退出",
        "observable_utg_signals": ["Settings 无障碍页出现 ≥2 次", "两次出现之间无应用自有页面", "返回键后 <1s 再次进入 Settings"]
      },
      {
        "page_role": "获权后桌面图标消失 / 二阶段安装器",
        "page_identifier": "授权并激活设备管理器后，Launcher 中 media player 图标消失；随后出现 application/vnd.android.package-archive 系统安装器",
        "why_most_useful": "证明反撤权与二阶段投放，说明该无障碍权限服务于后续载荷而非任何媒体功能",
        "observable_utg_signals": ["Launcher 包列表缺少 cmf0.c3b5bm90zq.patch 图标", "出现 PackageInstaller 界面且来源路径含 /base.apk", "设备管理器激活弹窗说明为空白"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "该样本无任何图/文诱饵，UTG 侧的关键盲区是「零界面」本身：若仅在界面出现后才拉起采集，会完全错过跳转瞬间。另注意 @string/gp 当前为 \"00000\"，本构建默认未开启无障碍跳转与图标隐藏，需以改写 gp 或运行时观察 charAt(1) 分支的方式验证；res/raw/google.apk 在解包目录中为 0 字节，二阶段载荷内容未核验。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED"
  ],
  "code_anchors": [
    "cmf0.c3b5bm90zq.patch.C7#onCreate",
    "cmf0.c3b5bm90zq.patch.C7#c",
    "cmf0.c3b5bm90zq.patch.C7$1#run",
    "cmf0.c3b5bm90zq.patch.C7#a（setComponentEnabledSetting 自禁用图标）",
    "cmf0.c3b5bm90zq.patch.C7$2#run",
    "res/values/strings.xml（app_name / s / gp / h / p / n / v）"
  ]
}
```

</details>
