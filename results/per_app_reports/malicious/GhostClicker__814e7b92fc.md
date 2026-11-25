# MR_034__814e7b92fc｜GhostClicker — Ram Cleaner

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：114.2s

## 1. 一句话核心结论

- **核心申请方式**：冷启动即弹不可取消的 RAM Cleaner 弹窗，以内部代号 Amit 请求开启无障碍服务，但 Yes 按钮实际只跳用量访问设置页，无障碍服务需用户自行到系统列表找到名为 amit 的条目开启，且服务仅监听前台窗口变化落日志。
- **静态可见性说明**：无障碍引导链（MainActivity.p 判断+弹窗、f.onClick 跳转、accessibilityservice.xml 声明、服务 onServiceConnected/onAccessibilityEvent）全部静态可见，无加壳、无 AES 密文、无远端 HTML。仅获权后的下游点击/落地动作在本 DEX 中未出现，可能由 FCM 下发的 AppLink/Package 经 NotificationActivity 透明页在运行期决定，属功能未闭合而非隐藏代码。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `814e7b92fcd2090d53a7ba590caedc6bc3710d6406bb363e604982b9fa2e2bb4` |
| 包名 / 年份 | `dt.ram.cleaner.speed.booster` / 2017 |
| 家族 / 品类 | **GhostClicker**（同池样本数：4） |
| 原始来源标识 | https://www.trendmicro.com/en_us/research/17/h/ghostclicker-adware-is-a-phantomlike-android-click-fraud.html |
| 桌面显示名 | Ram Cleaner |
| 引导页宣称品牌/身份 | RAM Cleaner 内存清理加速工具（自称可清理后台释放内存）；代码与市场链接指向 com.ram.cleanmaster，联系邮箱 certitudellc.info@gmail.com |
| 系统无障碍列表服务名 | amit |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务 android:label 使用与应用功能毫无关系的人名式代号 amit，系统列表中无法据此识别用途；description 仅为 @string/app_name（Ram Cleaner），accessibilityservice.xml 未提供任何用途说明；弹窗正文仅写 Enable Amit service here 而不解释为何需要无障碍；Toast 文案为未替换的模板占位串 Your string here；Manifest 中另有借用 GMS 包名段的 com.google.android.gms.logs.b（label Plus Service）注册为设备管理器，以及 com.google.android.gms.logs.Logger 透明无历史 Activity；MainActivity 设置 excludeFromRecents |
| 无障碍服务类名 | `com.ram.cleanmaster.WindowChangeDetectingService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | RAM Cleaner |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.ram.cleanmaster.MainActivity（LAUNCHER，excludeFromRecents=true，纵向固定） | onCreate -> l() 初始化控件后立即调用 p() | 原生Activity | **原文**：Running Task : 0 / Total RAM / Available RAM<br>**译注**：运行任务数、总内存、可用内存等清理工具主界面数据 | 无需操作，界面加载后自动进入第 2 步弹窗 | `com.ram.cleanmaster.MainActivity.onCreate / MainActivity.l / MainActivity.m` |
| 2 | 引导说明页 | AppCompat AlertDialog（android.support.v7.a.p，构建于 MainActivity.p 内） | p() 内 a(Context) 返回 false（Settings.Secure accessibility_enabled != 1 或 enabled_accessibility_services 中不含 包名/com.ram.cleanmaster.WindowChangeDetectingService） | 原生Dialog | **原文**：RAM Cleaner / Enable Amit service here / Yes / No<br>**译注**：标题“RAM Cleaner”，正文“在此启用 Amit 服务”，按钮“是”/“否” | 点 Yes 继续；点 No 仅取消本对话框、留在主界面（对话框本身 .a(false) 不可通过返回键/点击外部取消） | `com.ram.cleanmaster.MainActivity.p` |
| 3 | 跳受限设置 | 系统设置 android.settings.USAGE_ACCESS_SETTINGS（用量访问设置页），前置一个自定义 View 的 Toast | 对话框 Yes 按钮回调 com.ram.cleanmaster.f.onClick | 系统无障碍页 | **原文**：Your string here<br>**译注**：Toast 显示未替换的模板占位文字“你的字符串在此”（实际页面为系统的用量访问权限列表，与无障碍权限无关） | 被要求在该系统页面中授权，但该页并不包含无障碍开关，用户无法在此完成引导所述操作 | `com.ram.cleanmaster.f.onClick` |
| 4 | 跳无障碍设置 | 系统设置 → 无障碍 → 已下载/已安装服务列表项 amit（无应用内跳转，需用户自行寻找） | 无代码触发；仅由用户手动导航（全包无 ACCESSIBILITY_SETTINGS 调用点） | 系统无障碍页 | **原文**：amit / RAM Cleaner<br>**译注**：系统无障碍列表中显示的服务名“amit”，说明文字“RAM Cleaner” | 要求用户自行找到 amit 项并打开开关（应用未提供任何直达入口或图示指引） | `res/xml/accessibilityservice.xml; AndroidManifest.xml service android:label="amit"` |
| 5 | 获权后动作 | com.ram.cleanmaster.WindowChangeDetectingService（AccessibilityService） | onServiceConnected 设置 eventTypes=32（TYPE_WINDOW_STATE_CHANGED）、flags=2；随后每次前台窗口切换触发 onAccessibilityEvent | 不可静态还原 | **原文**：CurrentActivity / CurrentActivity-------- / CurrentActivity Name / CurrentActivity---icon<br>**译注**：无界面呈现；仅向 Logcat 记录当前前台 Activity 的组件名、包名、应用名与图标资源 id | 无需用户操作，后台静默监听窗口变化 | `com.ram.cleanmaster.WindowChangeDetectingService.onServiceConnected / onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 冷启动 MainActivity 内不可取消的 AppCompat AlertDialog（标题 RAM Cleaner、正文 Enable Amit service here、按钮 Yes/No），由 MainActivity.p 构建
- 点击 Yes 后顶部重力（setGravity(49)）自定义 View Toast，文案为未替换占位串 Your string here，见 com.ram.cleanmaster.f.onClick
- 系统无障碍服务列表项：android:label="amit" 与 android:description="@string/app_name"（RAM Cleaner），见 AndroidManifest.xml 与 res/xml/accessibilityservice.xml
- 主界面 TextView：Running Task : N、总/可用/已用内存 MB 数值（清理工具伪装的功能外观）
- SettingsActivity 内 Auto RAM Booster 开关与 Toast（Auto RAM Booster ON/OFF），与本引导链无关但构成工具化外观
- 无 WebView/HTML/悬浮窗/通知栏承载本引导链的任何文案

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | RAM Cleaner | RAM 清理器 | `com.ram.cleanmaster.MainActivity.p 硬编码 pVar.a("RAM Cleaner")` | 清理工具伪装 |
| en | Enable Amit service here | 在此启用 Amit 服务 | `com.ram.cleanmaster.MainActivity.p 硬编码 pVar.b("Enable Amit service here")` | 教唆忽视警告 |
| en | Yes | 是 | `com.ram.cleanmaster.MainActivity.p 硬编码 .a("Yes", new f(this))` | 受限设置分步教学 |
| en | No | 否 | `com.ram.cleanmaster.MainActivity.p 硬编码 .b("No", new e(this))` | 未知 |
| en | Your string here | 你的字符串放在这里（未替换的模板占位文本） | `com.ram.cleanmaster.f.onClick 硬编码 Toast.makeText` | 未知 |
| en | amit | 阿米特（人名式代号，未说明任何功能用途） | `AndroidManifest.xml <service android:label="amit">` | 未知 |
| en | RAM Cleaner | RAM 清理器（系统无障碍列表中的服务说明文字） | `res/xml/accessibilityservice.xml android:description="@string/app_name"` | 清理工具伪装 |
| en | Auto RAM Booster ON | 自动内存加速已开启 | `com.ram.cleanmaster.l.b 硬编码 Toast` | 清理工具伪装 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：点 No 仅 dialog.cancel()，不退出应用；无 onResume/Timer 重跳。但 p() 挂在 onCreate 的 l() 流程中，用户每次重新进入 MainActivity（含从设置页返回后再次启动）都会再弹一次同一不可取消弹窗，形成每次进入即弹的弱循环。从系统设置返回时 MainActivity.onResume 只刷新 AdView，不重新检测也不重跳。
- **遮罩叠层 / 高仿系统设置页**：无。SYSTEM_ALERT_WINDOW 已声明但本链未见任何悬浮窗/半透明遮罩/高仿无障碍开关页实现；引导仅为普通原生 AlertDialog。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。targetSdkVersion=22（Android 5.1 时代样本），不存在 Android 13+ 受限设置教学，也无 Session 安装器绕过。
- **获权后即时行为与防撤权机制**：无。服务获权后仅 onServiceConnected 设置监听参数并记录前台窗口日志，未见自点确认、GLOBAL_ACTION_BACK/HOME、监听设置页阻止撤权等行为。
- **良性降级 / 替代方案**：无。拒权后应用仍可作普通清理工具使用（主界面与 Auto RAM Booster 开关不依赖无障碍），但未以任何文案说明该降级路径或权限可选性。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在冷启动 MainActivity 首次绘制后（onCreate→p 弹窗瞬间）抓取，以及在监测到 Intent 跳转 android.settings.USAGE_ACCESS_SETTINGS 的同一时刻抓取跳转前后两屏；随后手动进入系统无障碍列表抓取 amit 条目的呈现状态。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在两处盲区：一是 Toast 文案为未替换的模板占位串 Your string here，说明该引导模块为批量套壳产物，同家族其他样本文案可能完全不同，需按包名/服务标签而非文案做指纹；二是获权后的真实用途（前台窗口监听→可能的广告自点击）在本 DEX 中未闭合，可能由 FCM 下发的 AppLink/Package 经 Manifest 中的透明 NotificationActivity 或 com.google.android.gms.logs.b 设备管理器在运行期决定，纯静态 UTG 无法捕获该阶段。静态无加壳，不构成 UTG 阻碍。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页** | com.ram.cleanmaster.MainActivity 之上的 AppCompat AlertDialog，标题 RAM Cleaner、正文 Enable Amit service here、Yes/No 两按钮，无取消入口 | 这是唯一的权限索取话术载体，可直接证明诱导话术、不可取消性与服务代号 Amit 的呈现方式 | 对话框标题与正文文本；仅 Yes/No 两按钮且无关闭/取消控件；对话框背景可见主界面内存清理数据，说明为冷启动即弹；点击对话框外部/返回键不消失 |
| **跳转后的系统页面（引导与目标错位证据）** | 系统设置 用量访问（Usage Access）应用列表，包名 dt.ram.cleaner.speed.booster 对应条目 | Yes 按钮实际跳的是用量访问设置而非无障碍设置，可证明引导行为与宣称目的不符，是区分误导演示与正常引导的关键 | 页面标题为“用量访问/Usage access”而非无障碍；页面内无任何无障碍服务开关；顶部残留自定义 Toast 文案 Your string here |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已安装服务中的 amit 条目，副标题 RAM Cleaner | 证明服务在系统中的实际暴露名称与用途说明完全无法让用户判断其真实能力（仅窗口变化监听） | 服务名 amit；说明文字 RAM Cleaner；该条目在开启后无任何应用内引导回流 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.ram.cleanmaster.MainActivity.p`
- `com.ram.cleanmaster.MainActivity.a`
- `com.ram.cleanmaster.f.onClick`
- `com.ram.cleanmaster.e.onClick`
- `com.ram.cleanmaster.WindowChangeDetectingService.onServiceConnected`
- `res/xml/accessibilityservice.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

已核验完毕。核心事实（静态清晰可见，无加壳/加密载荷）：

**1. 引导链只有两步，且「Yes」按钮跳的不是无障碍设置页**
- 冷启动 [MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.ram.cleanmaster.MainActivity#onCreate>) → `l()` → [MainActivity.p()](<resource-unit:#1.dex1 code:com.ram.cleanmaster.MainActivity#p>) 用 `a(Context)` 读 `Settings.Secure.accessibility_enabled` 与 `enabled_accessibility_services`（比对 `包名/com.ram.cleanmaster.WindowChangeDetectingService`）判断是否已授权；未授权即弹**不可取消**（`.a(false)`）的 AppCompat AlertDialog：标题 `RAM Cleaner`，正文 `Enable Amit service here`，按钮 `Yes` / `No`。
- 点 `Yes` 走 [f.onClick()](<resource-unit:#1.dex1 code:com.ram.cleanmaster.f#onClick>)：先 `Toast` 一个 `Your string here`（占位串未替换，说明是模板化拼装的壳式引导），随后 `startActivity(new Intent("android.settings.USAGE_ACCESS_SETTINGS"))` —— 打开的是**用量访问（Usage Access）设置页**，而非无障碍设置页。
- 全包内 `ACCESSIBILITY_SETTINGS` **零命中**：应用从未直接跳无障碍列表，只能靠用户自己在系统设置里找到列表项 `amit` 并手动开启。`No` 走 [e.onClick()](<resource-unit:#1.dex1 code:com.ram.cleanmaster.e#onClick>) 仅 `dialog.cancel()`，不退出应用。

**2. 身份与用途说明严重不匹配（关键判定点）**
- 无障碍服务在系统列表显示名是 `amit`（人名式无意义标签，`<service android:label="amit">`），说明文字 `@string/app_name`=`RAM Cleaner`，即 [res/xml/accessibilityservice.xml](<resource-unit:#1 file:res/xml/accessibilityservice.xml#L1-L3>) 只声明了 `android:description`，**完全没有 `android:accessibilityFlags` / `canRetrieveWindowContent` 之外的用途声明，也没有任何"为什么需要此权限"的说明文本**。标签与应用功能（内存清理）毫无关系，用户无法从 `amit` 判断这是什么。
- 包名 `dt.ram.cleaner.speed.booster`，但代码命名空间 `com.ram.cleanmaster`，市场链接指向另一包名 `com.ram.cleanmaster`，联系邮箱 `certitudellc.info@gmail.com`；另有 `com.google.android.gms.logs.b`（label `Plus Service`）注册为**设备管理器**（`@xml/admin` + `DEVICE_ADMIN_ENABLED`），借用 GMS 包名段伪装。

**3. 获权后的实际动作：仅监听窗口变化并落日志**
[WindowChangeDetectingService.onServiceConnected()](<resource-unit:#1.dex1 code:com.ram.cleanmaster.WindowChangeDetectingService#onServiceConnected>) 把 `eventTypes` 设为 `32`（TYPE_WINDOW_STATE_CHANGED）、`flags=2`（FLAG_REPORT_VIEW_IDS）；[onAccessibilityEvent()](<resource-unit:#1.dex1 code:com.ram.cleanmaster.WindowChangeDetectingService#onAccessibilityEvent>) 对每个前台 Activity 记录 `CurrentActivity` / 包名 / 应用名 / icon 到 Logcat。**本链内未见 `performGlobalAction`、`dispatchGesture`、`performAction`、`findAccessibilityNodeInfosByText` 等点击/注入能力**，即"窗口监听器"已就位但点击器未在同一 DEX 中确认（GhostClicker 家族的典型两段式：先布点，后由远端/FCM 推送的 `AppLink`/`Package` 经 `NotificationActivity` 透明页触发）。

**4. 拒权反馈与辅助载体**
- 无 `onResume` 死循环重跳（`MainActivity.onResume` 只刷广告），但 `p()` 在每次 `onCreate` 都被调用，故每次重进主界面都会再弹一次同一对话框 —— 属"每次进入即弹"的弱循环。
- `SYSTEM_ALERT_WINDOW`、`DISABLE_KEYGUARD`、`GET_TASKS`、`KILL_BACKGROUND_PROCESSES` 已申请；本引导链**未使用悬浮窗遮罩、未伪造系统设置页、无 13+ 受限设置教学、无获权后自点确认/阻止撤权**。
- `SettingsActivity` 的 `Auto RAM Booster` 开关（`l.b()` 起 60 秒 AlarmManager 周期清理）与无障碍权限无耦合，是纯功能面。

**结论**：这是一条"**冷启动不可取消弹窗 + 占位 Toast + 误导向用量访问设置页 + 系统列表项使用无关人名 `amit` 且无用途说明**"的弱引导型 UTG 链；诱导主要靠"清理工具伪装 + 标题冒用应用名、正文只用内部代号 Amit 掩盖真实用途"，而非强遮罩/高仿页面。UTG 抓取的最佳时机就是冷启动 0 步弹窗与 `USAGE_ACCESS_SETTINGS` 跳转瞬间，以及用户手动进系统无障碍列表时 `amit` 项的呈现。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导链（MainActivity.p 判断+弹窗、f.onClick 跳转、accessibilityservice.xml 声明、服务 onServiceConnected/onAccessibilityEvent）全部静态可见，无加壳、无 AES 密文、无远端 HTML。仅获权后的下游点击/落地动作在本 DEX 中未出现，可能由 FCM 下发的 AppLink/Package 经 NotificationActivity 透明页在运行期决定，属功能未闭合而非隐藏代码。",
  "summary_one_liner": "冷启动即弹不可取消的 RAM Cleaner 弹窗，以内部代号 Amit 请求开启无障碍服务，但 Yes 按钮实际只跳用量访问设置页，无障碍服务需用户自行到系统列表找到名为 amit 的条目开启，且服务仅监听前台窗口变化落日志。",
  "disguise_identity": {
    "app_display_name": "Ram Cleaner",
    "claimed_brand_or_persona": "RAM Cleaner 内存清理加速工具（自称可清理后台释放内存）；代码与市场链接指向 com.ram.cleanmaster，联系邮箱 certitudellc.info@gmail.com",
    "a11y_service_label": "amit",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务 android:label 使用与应用功能毫无关系的人名式代号 amit，系统列表中无法据此识别用途；description 仅为 @string/app_name（Ram Cleaner），accessibilityservice.xml 未提供任何用途说明；弹窗正文仅写 Enable Amit service here 而不解释为何需要无障碍；Toast 文案为未替换的模板占位串 Your string here；Manifest 中另有借用 GMS 包名段的 com.google.android.gms.logs.b（label Plus Service）注册为设备管理器，以及 com.google.android.gms.logs.Logger 透明无历史 Activity；MainActivity 设置 excludeFromRecents"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.ram.cleanmaster.MainActivity（LAUNCHER，excludeFromRecents=true，纵向固定）",
      "trigger_event": "onCreate -> l() 初始化控件后立即调用 p()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Running Task : 0 / Total RAM / Available RAM",
      "shown_text_zh": "运行任务数、总内存、可用内存等清理工具主界面数据",
      "user_action_requested": "无需操作，界面加载后自动进入第 2 步弹窗",
      "code_anchor": "com.ram.cleanmaster.MainActivity.onCreate / MainActivity.l / MainActivity.m"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "AppCompat AlertDialog（android.support.v7.a.p，构建于 MainActivity.p 内）",
      "trigger_event": "p() 内 a(Context) 返回 false（Settings.Secure accessibility_enabled != 1 或 enabled_accessibility_services 中不含 包名/com.ram.cleanmaster.WindowChangeDetectingService）",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "RAM Cleaner / Enable Amit service here / Yes / No",
      "shown_text_zh": "标题“RAM Cleaner”，正文“在此启用 Amit 服务”，按钮“是”/“否”",
      "user_action_requested": "点 Yes 继续；点 No 仅取消本对话框、留在主界面（对话框本身 .a(false) 不可通过返回键/点击外部取消）",
      "code_anchor": "com.ram.cleanmaster.MainActivity.p"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "系统设置 android.settings.USAGE_ACCESS_SETTINGS（用量访问设置页），前置一个自定义 View 的 Toast",
      "trigger_event": "对话框 Yes 按钮回调 com.ram.cleanmaster.f.onClick",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Your string here",
      "shown_text_zh": "Toast 显示未替换的模板占位文字“你的字符串在此”（实际页面为系统的用量访问权限列表，与无障碍权限无关）",
      "user_action_requested": "被要求在该系统页面中授权，但该页并不包含无障碍开关，用户无法在此完成引导所述操作",
      "code_anchor": "com.ram.cleanmaster.f.onClick"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已下载/已安装服务列表项 amit（无应用内跳转，需用户自行寻找）",
      "trigger_event": "无代码触发；仅由用户手动导航（全包无 ACCESSIBILITY_SETTINGS 调用点）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "amit / RAM Cleaner",
      "shown_text_zh": "系统无障碍列表中显示的服务名“amit”，说明文字“RAM Cleaner”",
      "user_action_requested": "要求用户自行找到 amit 项并打开开关（应用未提供任何直达入口或图示指引）",
      "code_anchor": "res/xml/accessibilityservice.xml; AndroidManifest.xml service android:label=\"amit\""
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "com.ram.cleanmaster.WindowChangeDetectingService（AccessibilityService）",
      "trigger_event": "onServiceConnected 设置 eventTypes=32（TYPE_WINDOW_STATE_CHANGED）、flags=2；随后每次前台窗口切换触发 onAccessibilityEvent",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "CurrentActivity / CurrentActivity-------- / CurrentActivity Name / CurrentActivity---icon",
      "shown_text_zh": "无界面呈现；仅向 Logcat 记录当前前台 Activity 的组件名、包名、应用名与图标资源 id",
      "user_action_requested": "无需用户操作，后台静默监听窗口变化",
      "code_anchor": "com.ram.cleanmaster.WindowChangeDetectingService.onServiceConnected / onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "冷启动 MainActivity 内不可取消的 AppCompat AlertDialog（标题 RAM Cleaner、正文 Enable Amit service here、按钮 Yes/No），由 MainActivity.p 构建",
    "点击 Yes 后顶部重力（setGravity(49)）自定义 View Toast，文案为未替换占位串 Your string here，见 com.ram.cleanmaster.f.onClick",
    "系统无障碍服务列表项：android:label=\"amit\" 与 android:description=\"@string/app_name\"（RAM Cleaner），见 AndroidManifest.xml 与 res/xml/accessibilityservice.xml",
    "主界面 TextView：Running Task : N、总/可用/已用内存 MB 数值（清理工具伪装的功能外观）",
    "SettingsActivity 内 Auto RAM Booster 开关与 Toast（Auto RAM Booster ON/OFF），与本引导链无关但构成工具化外观",
    "无 WebView/HTML/悬浮窗/通知栏承载本引导链的任何文案"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "RAM Cleaner",
      "text_zh": "RAM 清理器",
      "source_location": "com.ram.cleanmaster.MainActivity.p 硬编码 pVar.a(\"RAM Cleaner\")",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Amit service here",
      "text_zh": "在此启用 Amit 服务",
      "source_location": "com.ram.cleanmaster.MainActivity.p 硬编码 pVar.b(\"Enable Amit service here\")",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Yes",
      "text_zh": "是",
      "source_location": "com.ram.cleanmaster.MainActivity.p 硬编码 .a(\"Yes\", new f(this))",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "No",
      "text_zh": "否",
      "source_location": "com.ram.cleanmaster.MainActivity.p 硬编码 .b(\"No\", new e(this))",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Your string here",
      "text_zh": "你的字符串放在这里（未替换的模板占位文本）",
      "source_location": "com.ram.cleanmaster.f.onClick 硬编码 Toast.makeText",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "amit",
      "text_zh": "阿米特（人名式代号，未说明任何功能用途）",
      "source_location": "AndroidManifest.xml <service android:label=\"amit\">",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "RAM Cleaner",
      "text_zh": "RAM 清理器（系统无障碍列表中的服务说明文字）",
      "source_location": "res/xml/accessibilityservice.xml android:description=\"@string/app_name\"",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Auto RAM Booster ON",
      "text_zh": "自动内存加速已开启",
      "source_location": "com.ram.cleanmaster.l.b 硬编码 Toast",
      "rhetorical_frame": "清理工具伪装"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "点 No 仅 dialog.cancel()，不退出应用；无 onResume/Timer 重跳。但 p() 挂在 onCreate 的 l() 流程中，用户每次重新进入 MainActivity（含从设置页返回后再次启动）都会再弹一次同一不可取消弹窗，形成每次进入即弹的弱循环。从系统设置返回时 MainActivity.onResume 只刷新 AdView，不重新检测也不重跳。",
    "overlay_or_fake_settings": "无。SYSTEM_ALERT_WINDOW 已声明但本链未见任何悬浮窗/半透明遮罩/高仿无障碍开关页实现；引导仅为普通原生 AlertDialog。",
    "restricted_settings_13plus_coaching": "无。targetSdkVersion=22（Android 5.1 时代样本），不存在 Android 13+ 受限设置教学，也无 Session 安装器绕过。",
    "post_grant_anti_removal": "无。服务获权后仅 onServiceConnected 设置监听参数并记录前台窗口日志，未见自点确认、GLOBAL_ACTION_BACK/HOME、监听设置页阻止撤权等行为。",
    "benign_graceful_degradation": "无。拒权后应用仍可作普通清理工具使用（主界面与 Auto RAM Booster 开关不依赖无障碍），但未以任何文案说明该降级路径或权限可选性。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在冷启动 MainActivity 首次绘制后（onCreate→p 弹窗瞬间）抓取，以及在监测到 Intent 跳转 android.settings.USAGE_ACCESS_SETTINGS 的同一时刻抓取跳转前后两屏；随后手动进入系统无障碍列表抓取 amit 条目的呈现状态。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页",
        "page_identifier": "com.ram.cleanmaster.MainActivity 之上的 AppCompat AlertDialog，标题 RAM Cleaner、正文 Enable Amit service here、Yes/No 两按钮，无取消入口",
        "why_most_useful": "这是唯一的权限索取话术载体，可直接证明诱导话术、不可取消性与服务代号 Amit 的呈现方式",
        "observable_utg_signals": ["对话框标题与正文文本", "仅 Yes/No 两按钮且无关闭/取消控件", "对话框背景可见主界面内存清理数据，说明为冷启动即弹", "点击对话框外部/返回键不消失"]
      },
      {
        "page_role": "跳转后的系统页面（引导与目标错位证据）",
        "page_identifier": "系统设置 用量访问（Usage Access）应用列表，包名 dt.ram.cleaner.speed.booster 对应条目",
        "why_most_useful": "Yes 按钮实际跳的是用量访问设置而非无障碍设置，可证明引导行为与宣称目的不符，是区分误导演示与正常引导的关键",
        "observable_utg_signals": ["页面标题为“用量访问/Usage access”而非无障碍", "页面内无任何无障碍服务开关", "顶部残留自定义 Toast 文案 Your string here"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已安装服务中的 amit 条目，副标题 RAM Cleaner",
        "why_most_useful": "证明服务在系统中的实际暴露名称与用途说明完全无法让用户判断其真实能力（仅窗口变化监听）",
        "observable_utg_signals": ["服务名 amit", "说明文字 RAM Cleaner", "该条目在开启后无任何应用内引导回流"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在两处盲区：一是 Toast 文案为未替换的模板占位串 Your string here，说明该引导模块为批量套壳产物，同家族其他样本文案可能完全不同，需按包名/服务标签而非文案做指纹；二是获权后的真实用途（前台窗口监听→可能的广告自点击）在本 DEX 中未闭合，可能由 FCM 下发的 AppLink/Package 经 Manifest 中的透明 NotificationActivity 或 com.google.android.gms.logs.b 设备管理器在运行期决定，纯静态 UTG 无法捕获该阶段。静态无加壳，不构成 UTG 阻碍。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_DISMISS_SYSTEM_WARNING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION"
  ],
  "code_anchors": [
    "com.ram.cleanmaster.MainActivity.p",
    "com.ram.cleanmaster.MainActivity.a",
    "com.ram.cleanmaster.f.onClick",
    "com.ram.cleanmaster.e.onClick",
    "com.ram.cleanmaster.WindowChangeDetectingService.onServiceConnected",
    "res/xml/accessibilityservice.xml"
  ]
}
```

</details>
