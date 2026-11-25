# BN_035__e344ded75f｜极简桌面与双击锁屏 — Supernova

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：187.2s

## 1. 一句话核心结论

- **核心申请方式**：应用仅在用户主动开启锁屏/手势功能时弹出原生说明弹窗并跳转系统无障碍设置页，服务实现为空壳且配置禁用手势，属透明、可选、可取消的良性按需申请。
- **静态可见性说明**：无障碍服务类、accessibility_service_config.xml、引导弹窗构建代码(y2.a/y2.d)、跳转点(x61.onClick/t61.R)、全部相关 strings 资源均完整静态可见；无加壳、无密文/远端 HTML 引导页。仅 y2.d 与 lj1.a 的完整方法体因 MCP 代码分析服务在本次会话后段连接失败未能逐行读取，弹窗按钮级细节为基于 x61 分支与 AlertDialog 构建模式的推断。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `e344ded75ff4a1f77fb4acd508027ed6b3b1b97bed9a7130da7dd7bcdd93b815` |
| 包名 / 年份 | `com.supernova.launcher` / 2025-2026 |
| 家族 / 品类 | **极简桌面与双击锁屏**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.supernova.launcher_24.apk |
| 桌面显示名 | Supernova |
| 引导页宣称品牌/身份 | Supernova Launcher（F-Droid 开源桌面） |
| 系统无障碍列表服务名 | Supernova |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。虽经 R8 混淆（类名 y2/x61/t61/lj1），但无障碍服务类名、服务标签、android:description 与文案均如实呈现，无空白/换行挤出警告、同形字、多 activity-alias 伪装或伪造 isAccessibilityTool |
| 无障碍服务类名 | `com.supernova.launcher.SupernovaAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_CONTACTS` |
| 系统设置项说明 (`android:description`) | Lets Supernova lock the screen from a gesture. Optional; no screen content is read. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 业务功能触发 | com.supernova.launcher.LauncherActivity / SettingsActivity 手势与锁屏设置（lock_method_accessibility、gestures_need_accessibility 条目） | 用户主动开启依赖无障碍的锁屏/最近任务/快捷设置手势，检测到服务未启用 | 原生Dialog | **原文**：Turn on the accessibility service / Lock screen, Recent apps and Quick settings need Supernova's accessibility service. Supernova uses it only for these actions.<br>**译注**：标题：开启无障碍服务；正文：锁屏、最近任务与快捷设置需要 Supernova 的无障碍服务。Supernova 仅将这些用于这些操作。 | 点击确认按钮前往无障碍设置；提供取消（普通 Dialog 负向按钮，监听器为 null 即直接关闭），可跳过 | `y2.a / y2.d（az0Var.m(2131689550=accessibility_needed_title)、az0Var.i(2131689549=accessibility_needed_message)）；文案见 res/values/strings.xml` |
| 2 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | Dialog 确认按钮回调 x61.onClick（switch b==3） | 系统无障碍页 | **原文**：无（系统页面）<br>**译注**：系统无障碍服务列表 | 用户在系统列表中手动找到 Supernova 并开启服务开关 | `x61.onClick → startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))；另 r6.i 亦有同名跳转` |
| 3 | 获权前的系统侧说明 | 系统无障碍列表中的服务条目（label + description） | 进入无障碍列表后系统渲染 service 元数据 | 系统无障碍页 | **原文**：Supernova — Lets Supernova lock the screen from a gesture. Optional; no screen content is read.<br>**译注**：Supernova — 允许 Supernova 通过手势锁屏。可选；不读取屏幕内容。 | 用户自行决定是否开启；说明明确标注为可选 | `res/xml/accessibility_service_config.xml → @string/accessibility_description；AndroidManifest.xml service android:label="@string/app_label"` |
| 4 | 获权后动作 | SupernovaAccessibilityService（静态实例 b）→ y2.d | 用户执行已绑定的锁屏/最近任务/快捷设置手势 | 不可静态还原 | 无 | 无需额外操作 | `com.supernova.launcher.SupernovaAccessibilityService#onServiceConnected（仅保存实例）、y2.d（三处 performGlobalAction 调用）` |
| 5 | 拒权反馈循环 | 无独立拒权处理页面 | 用户从系统设置返回且未开启服务 | 原生Activity | **原文**：Some gestures need this on. Tap to turn it on<br>**译注**：部分手势需要开启此服务。点按以开启。 | 停留在设置页/桌面，手势保持不可用，不强制重跳；用户可再次点按条目重试 | `res/values/strings.xml gestures_need_accessibility_summary；未发现 onResume 强制跳转或定时器` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 设置页手势项：res/values/strings.xml 的 gestures_need_accessibility / gestures_need_accessibility_summary（'Needs the accessibility service' / 'Some gestures need this on. Tap to turn it on'）
- 按需弹出的原生 AlertDialog：y2.a 与 y2.d 构建（az0Var.m(accessibility_needed_title) + az0Var.i(accessibility_needed_message)），同类文案亦被 lj1.a 引用
- 系统无障碍服务列表条目：android:label="@string/app_label"（Supernova）+ android:description="@string/accessibility_description"
- 锁屏方式设置项：res/values/strings.xml lock_method_accessibility（'Accessibility service'）
- 权限说明条目：permission_accessibility / permission_accessibility_use（'gestures that lock the screen or open recents and quick settings'）
- 通知访问流程（与无障碍无关）：notification_access_title / notification_access_popup / notification_access_restricted，由 t61.R + x61.onClick(b==1/b==2) 弹窗并跳 NOTIFICATION_LISTENER_DETAIL_SETTINGS 或 APPLICATION_DETAILS_SETTINGS

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Lets Supernova lock the screen from a gesture. Optional; no screen content is read. | 允许 Supernova 通过手势锁屏。可选；不读取屏幕内容。 | `res/values/strings.xml key=accessibility_description（被 res/xml/accessibility_service_config.xml 引用）` | 隐私承诺 |
| en | Lock screen, Recent apps and Quick settings need Supernova's accessibility service. Supernova uses it only for these actions. | 锁屏、最近任务与快捷设置需要 Supernova 的无障碍服务。Supernova 仅将这些用于这些操作。 | `res/values/strings.xml key=accessibility_needed_message（y2.a/y2.d/lj1.a 弹窗正文）` | 良性透明说明 |
| en | Turn on the accessibility service | 开启无障碍服务 | `res/values/strings.xml key=accessibility_needed_title（弹窗标题）` | 受限设置分步教学 |
| en | Some gestures need this on. Tap to turn it on | 部分手势需要开启此服务。点按以开启。 | `res/values/strings.xml key=gestures_need_accessibility_summary` | 良性透明说明 |
| en | If the notification access switch is greyed out, Android is blocking it because Supernova was not installed from the Play Store. Open App info, tap the ⋮ menu at the top right, choose Allow restricted settings, then open the notification access screen again. | 如果通知访问开关为灰色，是因为 Supernova 不是从 Play 商店安装的，Android 正在阻止它。打开应用信息，点右上角 ⋮ 菜单，选择“允许受限设置”，然后重新打开通知访问页面。 | `res/values/strings.xml key=notification_access_restricted（t61.R 弹窗正文，针对通知访问而非无障碍）` | 受限设置分步教学 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：未见强制循环：从系统设置返回后不重跳（未发现 onResume 内 startActivity(ACCESSIBILITY_SETTINGS)、无定时器/Handler 轮询拉起）；仅在设置项显示 'Some gestures need this on. Tap to turn it on'，由用户再次点按才重新弹窗跳转，属良性安全降级
- **遮罩叠层 / 高仿系统设置页**：无。未发现悬浮窗/SYSTEM_ALERT_WINDOW 引导层，也无高仿系统无障碍开关页；引导仅用应用内原生 AlertDialog + 系统设置页
- **Android 13+ 受限设置（Restricted Settings）应对**：无障碍流程无受限设置教学；仅通知访问流程 t61.R 在检测到安装来源非 com.android.vending 时弹出 notification_access_restricted，教用户 App info → ⋮ → Allow restricted settings（对象为通知访问，且与 AOSP 受限设置机制一致）
- **获权后即时行为与防撤权机制**：无。获权后仅保存服务实例并调用 performGlobalAction，未发现自动点击确认、自授权或监听设置页以 GLOBAL_ACTION_BACK/HOME 阻止撤权
- **良性降级 / 替代方案**：无障碍为明确可选能力：服务未开启时手势不可用但应用可正常作为桌面使用；字符串说明 'Optional; no screen content is read.'，且未开启时不阻断应用启动

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到从应用自身页面 startActivity 到 android.settings.ACCESSIBILITY_SETTINGS 的瞬间（x61.onClick / r6.i）或 android.settings.APPLICATION_DETAILS_SETTINGS（x61.onClick b==2）；亦可冷启动后手动触发一次锁屏手势，捕获前置 AlertDialog
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：纯 UTG 的主要盲区在于本应用引导为『按需触发』而非冷启动：若测试脚本不在桌面执行锁屏手势，将完全观察不到弹窗与跳转，易误判为无申请行为。另需注意 t61.R 的通知访问受限设置引导文案（含 'Allow restricted settings' 与 ⋮ 菜单教学）属通知访问流程，若仅按关键词匹配可能被误判为无障碍受限设置诱导。无纯图空文本引导、无远端 HTML 教学页、无加壳（静态加壳不阻挡运行期 UTG）。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转前的按需引导弹窗页** | com.supernova.launcher 前台 Activity 上叠加的原生 AlertDialog，标题 'Turn on the accessibility service' | 该弹窗是唯一主动引导入口，其标题/正文、按钮数量与可取消性直接区分透明说明与恐吓/不可取消诱导 | 对话框标题文本 Turn on the accessibility service；正文包含 'Optional' 或 'only for these actions' 的透明说明；是否存在负向/取消按钮（可取消性）；确认按钮文案与目标 intent（无障碍设置） |
| **系统无障碍服务列表项** | 系统 Settings 无障碍列表中 label='Supernova'、description 以 'Lets Supernova lock the screen from a gesture. Optional; no screen content is read.' 开头 | 核对服务名与系统侧说明是否与应用自称一致，识别空白挤出/同形字/伪造描述 | 服务条目显示名是否为 Supernova；description 是否明示 Optional 且不读取屏幕内容；是否存在多个同名服务项（多 alias 伪装） |
| **获权返回后的手势设置页（拒权反馈）** | SettingsActivity 手势/锁屏分组，条目 summary 'Some gestures need this on. Tap to turn it on' | 验证返回后是否死循环重跳或压栈遮罩，确认良性降级 | 返回后 1-3 秒内是否再次拉起系统设置页；是否出现全屏半透明遮罩/高仿开关页；设置项文本与开关状态是否与实际授权一致 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.supernova.launcher.SupernovaAccessibilityService#onAccessibilityEvent`
- `com.supernova.launcher.SupernovaAccessibilityService#onServiceConnected`
- `x61#onClick`
- `y2#a`
- `y2#d`
- `res/xml/accessibility_service_config.xml`
- `res/values/strings.xml（accessibility_description / accessibility_needed_title / accessibility_needed_message / gestures_need_accessibility_summary）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

MCP 代码分析服务后续调用出现连接失败（第 9–11 次重试均失败），基于已获取的证据收口。

## 分析结论（静态可见，无风险成立）

- **无障碍服务本身是空壳**：`SupernovaAccessibilityService.onAccessibilityEvent()`、`onInterrupt()` 方法体为空，仅在 `onServiceConnected()` 保存静态引用；配置仅订阅 `typeWindowStateChanged`、`canPerformGestures="false"`，与"只用 `performGlobalAction` 锁屏/最近任务/快捷设置"的说明一致，不存在读取屏幕内容的实现。
- **引导方式是"按需弹窗 + 跳系统设置"**：用户在手势/锁屏功能开启时才由 `y2.a`/`y2.d` 弹出原生 `AlertDialog`（标题 `accessibility_needed_title`、正文 `accessibility_needed_message`），确认按钮经 `x61.onClick`（`b==3`）`startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))` 跳系统无障碍列表；取消/跳过为普通 Dialog 按钮，未见 `onResume` 死循环重跳或定时器拉起。
- **无遮罩、无高仿设置页、无自点确认**：全包 `overlay=[]`，未见全屏悬浮窗引导层或伪造无障碍开关页；获权后仅 `y2.d` 调用 `performGlobalAction`，无 `GLOBAL_ACTION_BACK/HOME` 撤权阻止逻辑。
- **身份与文案诚实**：服务标签 `Supernova`、`android:description` 明示"可选、不读取屏幕内容"；手势设置项摘要为 `Some gestures need this on. Tap to turn it on`，属透明说明。
- **需注意但非无障碍诱导**：`t61.R` 会先判断安装来源（非 `com.android.vending` 时弹窗），并展示 `notification_access_restricted` 指引"App info → ⋮ → Allow restricted settings"，对象是**通知访问**而非无障碍，且为 AOSP 官方受限设置机制的如实说明；`QUERY_ALL_PACKAGES`/`READ_CONTACTS`/`CALL_PHONE` 属桌面/拨号业务所需，不构成无障碍权限诱导。

未决/覆盖边界：`y2.d` 与 `lj1.a` 的完整方法体因 MCP 服务中断未能逐行读取（弹窗按钮配置、`performGlobalAction` 参数常量取值），弹窗可取消性依据 `x61` 中 `null` 监听器与常规 `AlertDialog` 构建模式推断，属分析判断而非逐行证实。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍服务类、accessibility_service_config.xml、引导弹窗构建代码(y2.a/y2.d)、跳转点(x61.onClick/t61.R)、全部相关 strings 资源均完整静态可见；无加壳、无密文/远端 HTML 引导页。仅 y2.d 与 lj1.a 的完整方法体因 MCP 代码分析服务在本次会话后段连接失败未能逐行读取，弹窗按钮级细节为基于 x61 分支与 AlertDialog 构建模式的推断。",
  "summary_one_liner": "应用仅在用户主动开启锁屏/手势功能时弹出原生说明弹窗并跳转系统无障碍设置页，服务实现为空壳且配置禁用手势，属透明、可选、可取消的良性按需申请。",
  "disguise_identity": {
    "app_display_name": "Supernova",
    "claimed_brand_or_persona": "Supernova Launcher（F-Droid 开源桌面）",
    "a11y_service_label": "Supernova",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。虽经 R8 混淆（类名 y2/x61/t61/lj1），但无障碍服务类名、服务标签、android:description 与文案均如实呈现，无空白/换行挤出警告、同形字、多 activity-alias 伪装或伪造 isAccessibilityTool"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "业务功能触发",
      "screen_or_component": "com.supernova.launcher.LauncherActivity / SettingsActivity 手势与锁屏设置（lock_method_accessibility、gestures_need_accessibility 条目）",
      "trigger_event": "用户主动开启依赖无障碍的锁屏/最近任务/快捷设置手势，检测到服务未启用",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Turn on the accessibility service / Lock screen, Recent apps and Quick settings need Supernova's accessibility service. Supernova uses it only for these actions.",
      "shown_text_zh": "标题：开启无障碍服务；正文：锁屏、最近任务与快捷设置需要 Supernova 的无障碍服务。Supernova 仅将这些用于这些操作。",
      "user_action_requested": "点击确认按钮前往无障碍设置；提供取消（普通 Dialog 负向按钮，监听器为 null 即直接关闭），可跳过",
      "code_anchor": "y2.a / y2.d（az0Var.m(2131689550=accessibility_needed_title)、az0Var.i(2131689549=accessibility_needed_message)）；文案见 res/values/strings.xml"
    },
    {
      "step": 2,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "Dialog 确认按钮回调 x61.onClick（switch b==3）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（系统页面）",
      "shown_text_zh": "系统无障碍服务列表",
      "user_action_requested": "用户在系统列表中手动找到 Supernova 并开启服务开关",
      "code_anchor": "x61.onClick → startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))；另 r6.i 亦有同名跳转"
    },
    {
      "step": 3,
      "stage": "获权前的系统侧说明",
      "screen_or_component": "系统无障碍列表中的服务条目（label + description）",
      "trigger_event": "进入无障碍列表后系统渲染 service 元数据",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Supernova — Lets Supernova lock the screen from a gesture. Optional; no screen content is read.",
      "shown_text_zh": "Supernova — 允许 Supernova 通过手势锁屏。可选；不读取屏幕内容。",
      "user_action_requested": "用户自行决定是否开启；说明明确标注为可选",
      "code_anchor": "res/xml/accessibility_service_config.xml → @string/accessibility_description；AndroidManifest.xml service android:label=\"@string/app_label\""
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "SupernovaAccessibilityService（静态实例 b）→ y2.d",
      "trigger_event": "用户执行已绑定的锁屏/最近任务/快捷设置手势",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "执行 performGlobalAction 完成锁屏/返回桌面等全局动作，无界面提示",
      "user_action_requested": "无需额外操作",
      "code_anchor": "com.supernova.launcher.SupernovaAccessibilityService#onServiceConnected（仅保存实例）、y2.d（三处 performGlobalAction 调用）"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "无独立拒权处理页面",
      "trigger_event": "用户从系统设置返回且未开启服务",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Some gestures need this on. Tap to turn it on",
      "shown_text_zh": "部分手势需要开启此服务。点按以开启。",
      "user_action_requested": "停留在设置页/桌面，手势保持不可用，不强制重跳；用户可再次点按条目重试",
      "code_anchor": "res/values/strings.xml gestures_need_accessibility_summary；未发现 onResume 强制跳转或定时器"
    }
  ],
  "text_presentation_locations": [
    "设置页手势项：res/values/strings.xml 的 gestures_need_accessibility / gestures_need_accessibility_summary（'Needs the accessibility service' / 'Some gestures need this on. Tap to turn it on'）",
    "按需弹出的原生 AlertDialog：y2.a 与 y2.d 构建（az0Var.m(accessibility_needed_title) + az0Var.i(accessibility_needed_message)），同类文案亦被 lj1.a 引用",
    "系统无障碍服务列表条目：android:label=\"@string/app_label\"（Supernova）+ android:description=\"@string/accessibility_description\"",
    "锁屏方式设置项：res/values/strings.xml lock_method_accessibility（'Accessibility service'）",
    "权限说明条目：permission_accessibility / permission_accessibility_use（'gestures that lock the screen or open recents and quick settings'）",
    "通知访问流程（与无障碍无关）：notification_access_title / notification_access_popup / notification_access_restricted，由 t61.R + x61.onClick(b==1/b==2) 弹窗并跳 NOTIFICATION_LISTENER_DETAIL_SETTINGS 或 APPLICATION_DETAILS_SETTINGS"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Lets Supernova lock the screen from a gesture. Optional; no screen content is read.",
      "text_zh": "允许 Supernova 通过手势锁屏。可选；不读取屏幕内容。",
      "source_location": "res/values/strings.xml key=accessibility_description（被 res/xml/accessibility_service_config.xml 引用）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Lock screen, Recent apps and Quick settings need Supernova's accessibility service. Supernova uses it only for these actions.",
      "text_zh": "锁屏、最近任务与快捷设置需要 Supernova 的无障碍服务。Supernova 仅将这些用于这些操作。",
      "source_location": "res/values/strings.xml key=accessibility_needed_message（y2.a/y2.d/lj1.a 弹窗正文）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Turn on the accessibility service",
      "text_zh": "开启无障碍服务",
      "source_location": "res/values/strings.xml key=accessibility_needed_title（弹窗标题）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Some gestures need this on. Tap to turn it on",
      "text_zh": "部分手势需要开启此服务。点按以开启。",
      "source_location": "res/values/strings.xml key=gestures_need_accessibility_summary",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "If the notification access switch is greyed out, Android is blocking it because Supernova was not installed from the Play Store. Open App info, tap the ⋮ menu at the top right, choose Allow restricted settings, then open the notification access screen again.",
      "text_zh": "如果通知访问开关为灰色，是因为 Supernova 不是从 Play 商店安装的，Android 正在阻止它。打开应用信息，点右上角 ⋮ 菜单，选择“允许受限设置”，然后重新打开通知访问页面。",
      "source_location": "res/values/strings.xml key=notification_access_restricted（t61.R 弹窗正文，针对通知访问而非无障碍）",
      "rhetorical_frame": "受限设置分步教学"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "未见强制循环：从系统设置返回后不重跳（未发现 onResume 内 startActivity(ACCESSIBILITY_SETTINGS)、无定时器/Handler 轮询拉起）；仅在设置项显示 'Some gestures need this on. Tap to turn it on'，由用户再次点按才重新弹窗跳转，属良性安全降级",
    "overlay_or_fake_settings": "无。未发现悬浮窗/SYSTEM_ALERT_WINDOW 引导层，也无高仿系统无障碍开关页；引导仅用应用内原生 AlertDialog + 系统设置页",
    "restricted_settings_13plus_coaching": "无障碍流程无受限设置教学；仅通知访问流程 t61.R 在检测到安装来源非 com.android.vending 时弹出 notification_access_restricted，教用户 App info → ⋮ → Allow restricted settings（对象为通知访问，且与 AOSP 受限设置机制一致）",
    "post_grant_anti_removal": "无。获权后仅保存服务实例并调用 performGlobalAction，未发现自动点击确认、自授权或监听设置页以 GLOBAL_ACTION_BACK/HOME 阻止撤权",
    "benign_graceful_degradation": "无障碍为明确可选能力：服务未开启时手势不可用但应用可正常作为桌面使用；字符串说明 'Optional; no screen content is read.'，且未开启时不阻断应用启动"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到从应用自身页面 startActivity 到 android.settings.ACCESSIBILITY_SETTINGS 的瞬间（x61.onClick / r6.i）或 android.settings.APPLICATION_DETAILS_SETTINGS（x61.onClick b==2）；亦可冷启动后手动触发一次锁屏手势，捕获前置 AlertDialog",
    "key_pages_to_capture": [
      {
        "page_role": "跳转前的按需引导弹窗页",
        "page_identifier": "com.supernova.launcher 前台 Activity 上叠加的原生 AlertDialog，标题 'Turn on the accessibility service'",
        "why_most_useful": "该弹窗是唯一主动引导入口，其标题/正文、按钮数量与可取消性直接区分透明说明与恐吓/不可取消诱导",
        "observable_utg_signals": ["对话框标题文本 Turn on the accessibility service", "正文包含 'Optional' 或 'only for these actions' 的透明说明", "是否存在负向/取消按钮（可取消性）", "确认按钮文案与目标 intent（无障碍设置）"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统 Settings 无障碍列表中 label='Supernova'、description 以 'Lets Supernova lock the screen from a gesture. Optional; no screen content is read.' 开头",
        "why_most_useful": "核对服务名与系统侧说明是否与应用自称一致，识别空白挤出/同形字/伪造描述",
        "observable_utg_signals": ["服务条目显示名是否为 Supernova", "description 是否明示 Optional 且不读取屏幕内容", "是否存在多个同名服务项（多 alias 伪装）"]
      },
      {
        "page_role": "获权返回后的手势设置页（拒权反馈）",
        "page_identifier": "SettingsActivity 手势/锁屏分组，条目 summary 'Some gestures need this on. Tap to turn it on'",
        "why_most_useful": "验证返回后是否死循环重跳或压栈遮罩，确认良性降级",
        "observable_utg_signals": ["返回后 1-3 秒内是否再次拉起系统设置页", "是否出现全屏半透明遮罩/高仿开关页", "设置项文本与开关状态是否与实际授权一致"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "纯 UTG 的主要盲区在于本应用引导为『按需触发』而非冷启动：若测试脚本不在桌面执行锁屏手势，将完全观察不到弹窗与跳转，易误判为无申请行为。另需注意 t61.R 的通知访问受限设置引导文案（含 'Allow restricted settings' 与 ⋮ 菜单教学）属通知访问流程，若仅按关键词匹配可能被误判为无障碍受限设置诱导。无纯图空文本引导、无远端 HTML 教学页、无加壳（静态加壳不阻挡运行期 UTG）。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE"
  ],
  "code_anchors": [
    "com.supernova.launcher.SupernovaAccessibilityService#onAccessibilityEvent",
    "com.supernova.launcher.SupernovaAccessibilityService#onServiceConnected",
    "x61#onClick",
    "y2#a",
    "y2#d",
    "res/xml/accessibility_service_config.xml",
    "res/values/strings.xml（accessibility_description / accessibility_needed_title / accessibility_needed_message / gestures_need_accessibility_summary）"
  ]
}
```

</details>
