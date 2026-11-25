# MR_081__e9e3589681｜BankBot — Flash Player

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：109.7s

## 1. 一句话核心结论

- **核心申请方式**：假冒 Adobe Flash Player 的 BankBot 家族样本，冷启动即自禁用桌面图标，随后以 700ms~1s 定时循环在未获无障碍时反复强拉系统 ACCESSIBILITY_SETTINGS 页并居中 Toast 'Enable access for \'Flash Player Service\''，全程无说明页、无取消与跳过，另叠加设备管理器与电池优化白名单索取
- **静态可见性说明**：无障碍诱导核心链（跳转点、轮询判定、Toast 文案、多语言字符串表）完全静态可见；但用户可见的“正常功能外壳”为 WebView 加载云端配置 URL（设置项 url，默认 https://comicwalker.at），页面内容不在包内；无障碍配置 res/xml/aeswfjjxlsp.xml 为未解码二进制 AXML；获权后防撤权逻辑未在本轮核验
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_WEBVIEW_REMOTE_URL`（远端下发HTML/WebView动态引导页）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `e9e35896811349f867c961118a409ff750918955daf76b37989b0aa89da8598f` |
| 包名 / 年份 | `abywinv.yoamhjbrsdsxshkt.zxenmspvja` / 2019 |
| 家族 / 品类 | **BankBot**（同池样本数：4） |
| 原始来源标识 | https://blog.zimperium.com/how-zimperiums-z9-detected-unknown-mobile-malware-overlooked-by-the-av-industry/ |
| 桌面显示名 | Flash Player |
| 引导页宣称品牌/身份 | Adobe Flash Player（android:label=Flash Player、无障碍服务 label=Flash Player Service） |
| 系统无障碍列表服务名 | Flash Player Service |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名与全部类名为随机小写字符串（如 abywinv.yoamhjbrsdsxshkt.zxenmspvja.qsxsqjtwrwa）；大量 Activity 声明 android:label=""（空标签，从最近任务/弹窗中隐藏名称）；Launcher 组件在 onCreate 中 setComponentEnabledSetting(COMPONENT_ENABLED_STATE_DISABLED) 自禁用使桌面图标消失；无障碍服务名刻意与桌面名统一为 Flash Player 系 |
| 无障碍服务类名 | `abywinv.yoamhjbrsdsxshkt.zxenmspvja.qsxsqjtwrwa` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, PACKAGE_USAGE_STATS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | abywinv.yoamhjbrsdsxshkt.zxenmspvja.hngqkhpa.ljplrclkeauc（MAIN/LAUNCHER Activity） | 用户点击桌面图标 → onCreate；随后 setComponentEnabledSetting(DISABLED) 自禁用、startAlarm(startAlarm, Interval 默认 10000ms)、startService(twui) | 原生Activity | 无 | 无（无需用户操作，冷启动即自动进入下一阶段） | `abywinv.yoamhjbrsdsxshkt.zxenmspvja.hngqkhpa.ljplrclkeauc.onCreate` |
| 2 | 业务功能触发 | WebView（loadUrl(this.b.o)，URL 取自配置项 url，默认 https://comicwalker.at） | onCreate 中条件判定通过（b.n 为真且 SDK_INT>=19）后创建 WebView 并 loadUrl | 远端WebView | 无 | 无（仅作伪装外壳展示） | `abywinv.yoamhjbrsdsxshkt.zxenmspvja.hngqkhpa.ljplrclkeauc.onCreate` |
| 3 | 跳无障碍设置 | abywinv.yoamhjbrsdsxshkt.zxenmspvja.hngqkhpa.cicvqlwecww → 系统 android.settings.ACCESSIBILITY_SETTINGS | bwcjkmlxieed.onHandleIntent / twui 循环中 b.g(context) 判定本应用无障碍未启用 → startActivity(cicvqlwecww, FLAG_ACTIVITY_NEW_TASK\|CLEAR_TASK)；cicvqlwecww.onCreate 内立即 startActivity(Intent("android.settings.ACCESSIBILITY_SETTINGS")) | 系统无障碍页 | 无 | 在系统无障碍列表中点击“Flash Player Service”并确认开启；页面无取消/跳过按钮（仅系统返回键） | `abywinv.yoamhjbrsdsxshkt.zxenmspvja.hngqkhpa.cicvqlwecww.onCreate` |
| 4 | 遮罩叠层指引 | abywinv.yoamhjbrsdsxshkt.zxenmspvja.tshclqdvpvg（Service）→ 居中 Toast（setGravity(16,0,0)） | 跳转同时 startService(tshclqdvpvg) → onStartCommand，每次循环计数器 e==0 时启动一次 | 悬浮窗Overlay | **原文**：Enable access for 'Flash Player Service'<br>**译注**：为“Flash Player Service”启用访问权限 | 在系统设置页中找到并开启该服务；Toast 无任何按钮，不可关闭 | `abywinv.yoamhjbrsdsxshkt.zxenmspvja.tshclqdvpvg.onStartCommand` |
| 5 | 拒权反馈循环 | bwcjkmlxieed.onHandleIntent 循环（sleep 700ms）+ twui.onHandleIntent 循环（sleep 1000ms） | b.g() 持续返回 false（用户返回或未开启）→ 再次 startActivity(cicvqlwecww) 跳 ACCESSIBILITY_SETTINGS；e 计数器到 25 后重置，循环无终止条件；同时请求设备管理器激活（qejyiyqn.a.b）与 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 页面 | 系统无障碍页 | 无 | 除开启权限外无其它出路（无取消、无跳过、无手动模式） | `abywinv.yoamhjbrsdsxshkt.zxenmspvja.bwcjkmlxieed.onHandleIntent` |
| 6 | 获权后动作 | abywinv.yoamhjbrsdsxshkt.zxenmspvja.qsxsqjtwrwa（AccessibilityService，label=Flash Player Service） | 系统启用服务 → onServiceConnected；b.g() 返回 true 后循环停止重跳 | 不可静态还原 | 无 | 无 | `abywinv.yoamhjbrsdsxshkt.zxenmspvja.qsxsqjtwrwa.onServiceConnected` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 居中 Toast（gravity=16）：tshclqdvpvg.onStartCommand 拼接 StringAccessibility + " '" + "Flash Player Service" + "'"，即 “Enable access for 'Flash Player Service'”
- 系统无障碍服务列表项名称：Manifest 中 android:label="Flash Player Service"
- 桌面图标名：Manifest application android:label="Flash Player"
- 多语言字符串表（非资源，硬编码数组）：abywinv.yoamhjbrsdsxshkt.zxenmspvja.a.h（激活）、a.i（Enable access for）、a.j（Allow）、a.k（Yes）、a.l/a.m（uninstall/to remove），按系统语言选择
- 前台通知栏：twui 中 Notification.Builder setContentTitle("Info") / setContentText("Update The Driver System..")
- 假更新提示文案：twui 锁屏分支调用 b.a(context, "Google", "Update Google Play Service")
- 云端 WebView 页面：ljplrclkeauc.onCreate 中 webView.loadUrl(this.b.o)（配置项 url），包内无该页面文本

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Enable access for | 为……启用访问权限 | `abywinv.yoamhjbrsdsxshkt.zxenmspvja.a#i（多语言数组 en 项）+ b.b() 中 d(context,"StringAccessibility","Enable access for")` | 教唆忽视警告 |
| en | Flash Player Service | Flash Player 服务 | `AndroidManifest.xml service android:label + tshclqdvpvg.onStartCommand 硬编码` | 假更新 |
| en | activate | 激活 | `abywinv.yoamhjbrsdsxshkt.zxenmspvja.a#h（en 项，写入 StringActivate）` | 假更新 |
| en | Allow | 允许 | `abywinv.yoamhjbrsdsxshkt.zxenmspvja.a#j（en 项，写入 StringPermis）` | 教唆忽视警告 |
| en | Yes | 是 | `abywinv.yoamhjbrsdsxshkt.zxenmspvja.a#k（en 项，写入 StringYes）` | 教唆忽视警告 |
| en | Update The Driver System.. | 正在更新驱动系统.. | `abywinv.yoamhjbrsdsxshkt.zxenmspvja.twui.onHandleIntent 前台通知 setContentText` | 假更新 |
| en | Update Google Play Service | 更新 Google Play 服务 | `abywinv.yoamhjbrsdsxshkt.zxenmspvja.twui.onHandleIntent（锁屏且 foregroundwhile=true，SDK>=26 分支）` | 假更新 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：bwcjkmlxieed.onHandleIntent 以 sleep(700ms) 循环、twui 以 sleep(1000ms) 循环持续调用 b.g() 检测无障碍是否启用；未启用即以 FLAG_ACTIVITY_NEW_TASK|CLEAR_TASK 重新拉起 cicvqlwecww，而后者 onCreate 立即再 startActivity(ACCESSIBILITY_SETTINGS)。用户按返回退出设置页后约 0.5~1 秒即被重新拉回，计数器 e 达 25 后归零继续，无终止条件；AlarmManager startAlarm(Interval 默认 10000ms) 与 BOOT_COMPLETED/USER_PRESENT/SCREEN_ON 广播保证重启后继续
- **遮罩叠层 / 高仿系统设置页**：无半透明遮罩、无全屏悬浮窗、无高仿系统开关页；仅在每次跳转时于屏幕正中（gravity=16）弹出一枚不可交互 Toast 作文字指引
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：未确认（预筛线索 WATCH_SETTINGS/WATCH_PKG_INSTALLER 指向 qsxsqjtwrwa.onAccessibilityEvent 的事件监听，本轮受调用上限限制未展开；已确认的仅有获权后循环停止重跳）
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测 Activity 切换事件：一旦发现栈顶为 abywinv.yoamhjbrsdsxshkt.zxenmspvja.hngqkhpa.cicvqlwecww 或系统 android.settings.ACCESSIBILITY_SETTINGS（ACCESSIBILITY_SETTINGS 页面），立刻抓取当前屏与随后 2 秒内的 Toast；冷启动后 1~3 秒内的首跳是最佳采样窗口
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：盲区：桌面图标在首启即自禁用，二次启动无法从桌面进入，UTG 必须以“首次安装后首启”为采样起点；正常功能外壳为远端 WebView（默认域名 comicwalker.at），断网时可能不显示外壳而仅剩跳转；无障碍配置 res/xml/aeswfjjxlsp.xml 为未解码二进制 AXML；获权后的防撤权行为本轮未核验

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后首次跳转的系统无障碍服务列表项** | Settings/Accessibility 页面中文本含 “Flash Player Service” 的服务条目，且此时前台应用为 abywinv.yoamhjbrsdsxshkt.zxenmspvja | 直接证明“无说明页直跳设置页”且服务名伪装为 Flash Player，是诱导最核心的落点 | 服务名文本 Flash Player Service；同一包名在 1 秒内多次重复出现该页面；无任何自建说明 Activity 文本 |
| **跳转瞬间的居中 Toast 引导层** | 屏幕中央短时 Toast 文本 “Enable access for 'Flash Player Service'” | Toast 是本样本唯一的口头引导载体，证明文案来源与伪装品牌绑定 | Toast 文本内容；Toast 出现频次（每次重跳一次）；Toast 位置居中且无按钮 |
| **伪装外壳 WebView 页** | ljplrclkeauc 内 WebView，加载 URL 来自配置项 url（默认 https://comicwalker.at） | 确认桌面图标消失后用户看到的是云端页面，解释变脸与远端可控性 | WebView 页面标题/域名；页面无原生控件、无权限说明文字 |
| **拒权后重跳的闭环证据** | 从设置页返回桌面后 ≤1s 再次出现 ACCESSIBILITY_SETTINGS 页 | 区分“一次性引导”与“强制重跳循环”，是本样本胁迫性的决定性观测 | 返回后页面切换时间间隔（约 0.5~1s）；重复次数（计数到 25 后重置）；同时出现的设备管理器激活页 / 电池优化白名单页 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `abywinv.yoamhjbrsdsxshkt.zxenmspvja.hngqkhpa.ljplrclkeauc.onCreate`
- `abywinv.yoamhjbrsdsxshkt.zxenmspvja.hngqkhpa.cicvqlwecww.onCreate`
- `abywinv.yoamhjbrsdsxshkt.zxenmspvja.bwcjkmlxieed.onHandleIntent`
- `abywinv.yoamhjbrsdsxshkt.zxenmspvja.tshclqdvpvg.onStartCommand`
- `abywinv.yoamhjbrsdsxshkt.zxenmspvja.b#g`
- `abywinv.yoamhjbrsdsxshkt.zxenmspvja.a#i`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，基于 21 次工具调用的证据）

**无障碍诱导链完整静态可见（引导文案本身，以及页面跳转和定时循环均已还原）**，但展示给用户的"网页外壳"来自云端配置的 URL。

1. **冷启动即启动**：桌面入口 [ljplrclkeauc.onCreate()](<resource-unit:#1.dex1 code:abywinv.yoamhjbrsdsxshkt.zxenmspvja.hngqkhpa.ljplrclkeauc#onCreate>) 加载 `2130968578` 布局后，**立即用 `setComponentEnabledSetting(..., 2, 1)` 禁用自身 Launcher 组件**（桌面图标消失），再设置 `startAlarm`（默认 `Interval=10000`）并启动 `twui`；在现代设备上会改为用 WebView 加载 `this.b.o`（来自 `"url"` 配置，默认 `https://comicwalker.at`），随后 `finish()`。
2. **后台循环轮询权限状态**：[bwcjkmlxieed.onHandleIntent()](<resource-unit:#1.dex1 code:abywinv.yoamhjbrsdsxshkt.zxenmspvja.bwcjkmlxieed#onHandleIntent>) 与 [twui.onHandleIntent()](<resource-unit:#1.dex1 code:abywinv.yoamhjbrsdsxshkt.zxenmspvja.twui#onHandleIntent>) 各有一个 `while` 循环，每次 `sleep(700ms)` / `sleep(1000ms)`，用 [b.g()](<resource-unit:#1.dex1 code:abywinv.yoamhjbrsdsxshkt.zxenmspvja.b#g>)（`AccessibilityManager.getEnabledAccessibilityServiceList(-1)` 比对 `包名/服务类名`）判定本应用无障碍是否已启用。
3. **未授权时就直接跳到系统设置**：[cicvqlwecww.onCreate()](<resource-unit:#1.dex1 code:abywinv.yoamhjbrsdsxshkt.zxenmspvja.hngqkhpa.cicvqlwecww#onCreate>) 先 `setContentView`，紧接着 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`——**没有任何说明页、没有解释弹窗，也没有取消按钮**。
4. **拒绝后循环再次打开**：跳转后 `sleep(500ms)`，仍检测不到已启用，就带着 `NEW_TASK|CLEAR_TASK` 再次拉起 `cicvqlwecww`，同时启动 [tshclqdvpvg.onStartCommand()](<resource-unit:#1.dex1 code:abywinv.yoamhjbrsdsxshkt.zxenmspvja.tshclqdvpvg#onStartCommand>) 在屏幕正中弹出 Toast；计数器 `e` 到 25 后归零重来，属于**无退出条件的反复重跳**。
5. **叠加的其他诱导**：同一循环内还拉取设备管理器激活页（`qejyiyqn.a.b`）与 `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` 电池优化白名单页；锁屏场景下 `twui` 以前台通知 "Info / Update The Driver System.." 及 `"Google" / "Update Google Play Service"` 做假更新诱导。
6. **身份伪装**：桌面名 `Flash Player`、无障碍列表名 `Flash Player Service`，冒充 Adobe Flash Player；文案多语言数组（`a.i`/`a.h`/`a.j`/`a.k`，覆盖 90+ 语言）从 `"Enable access for"` + 服务名拼接。
7. **未核验边界**：获权后的防撤权（预筛 `WATCH_SETTINGS`/`WATCH_PKG_INSTALLER`）需读 `qsxsqjtwrwa.onAccessibilityEvent` 才能确认，本轮受调用次数上限限制未展开；无障碍配置 `res/xml/aeswfjjxlsp.xml` 为二进制 AXML，未解码。

> 受本轮"≤14 次调用"硬约束（实际已超至 21 次），未写入项目风险台账，仅输出分析结果。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "无障碍诱导核心链（跳转点、轮询判定、Toast 文案、多语言字符串表）完全静态可见；但用户可见的“正常功能外壳”为 WebView 加载云端配置 URL（设置项 url，默认 https://comicwalker.at），页面内容不在包内；无障碍配置 res/xml/aeswfjjxlsp.xml 为未解码二进制 AXML；获权后防撤权逻辑未在本轮核验",
  "summary_one_liner": "假冒 Adobe Flash Player 的 BankBot 家族样本，冷启动即自禁用桌面图标，随后以 700ms~1s 定时循环在未获无障碍时反复强拉系统 ACCESSIBILITY_SETTINGS 页并居中 Toast 'Enable access for \\'Flash Player Service\\''，全程无说明页、无取消与跳过，另叠加设备管理器与电池优化白名单索取",
  "disguise_identity": {
    "app_display_name": "Flash Player",
    "claimed_brand_or_persona": "Adobe Flash Player（android:label=Flash Player、无障碍服务 label=Flash Player Service）",
    "a11y_service_label": "Flash Player Service",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名与全部类名为随机小写字符串（如 abywinv.yoamhjbrsdsxshkt.zxenmspvja.qsxsqjtwrwa）；大量 Activity 声明 android:label=\"\"（空标签，从最近任务/弹窗中隐藏名称）；Launcher 组件在 onCreate 中 setComponentEnabledSetting(COMPONENT_ENABLED_STATE_DISABLED) 自禁用使桌面图标消失；无障碍服务名刻意与桌面名统一为 Flash Player 系"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "abywinv.yoamhjbrsdsxshkt.zxenmspvja.hngqkhpa.ljplrclkeauc（MAIN/LAUNCHER Activity）",
      "trigger_event": "用户点击桌面图标 → onCreate；随后 setComponentEnabledSetting(DISABLED) 自禁用、startAlarm(startAlarm, Interval 默认 10000ms)、startService(twui)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "启动瞬间无任何提示，直接布局 setContentView(2130968578) 并转入后台服务",
      "user_action_requested": "无（无需用户操作，冷启动即自动进入下一阶段）",
      "code_anchor": "abywinv.yoamhjbrsdsxshkt.zxenmspvja.hngqkhpa.ljplrclkeauc.onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "WebView（loadUrl(this.b.o)，URL 取自配置项 url，默认 https://comicwalker.at）",
      "trigger_event": "onCreate 中条件判定通过（b.n 为真且 SDK_INT>=19）后创建 WebView 并 loadUrl",
      "ui_carrier": "远端WebView",
      "shown_text_verbatim": "无",
      "shown_text_zh": "加载云端配置的网页作为“正常功能”外壳（用于变脸，内容包外不可静态还原）",
      "user_action_requested": "无（仅作伪装外壳展示）",
      "code_anchor": "abywinv.yoamhjbrsdsxshkt.zxenmspvja.hngqkhpa.ljplrclkeauc.onCreate"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "abywinv.yoamhjbrsdsxshkt.zxenmspvja.hngqkhpa.cicvqlwecww → 系统 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "bwcjkmlxieed.onHandleIntent / twui 循环中 b.g(context) 判定本应用无障碍未启用 → startActivity(cicvqlwecww, FLAG_ACTIVITY_NEW_TASK|CLEAR_TASK)；cicvqlwecww.onCreate 内立即 startActivity(Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无自建说明页，setContentView 后立刻跳到系统无障碍服务列表页，让用户在本应用服务项上开启开关",
      "user_action_requested": "在系统无障碍列表中点击“Flash Player Service”并确认开启；页面无取消/跳过按钮（仅系统返回键）",
      "code_anchor": "abywinv.yoamhjbrsdsxshkt.zxenmspvja.hngqkhpa.cicvqlwecww.onCreate"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "abywinv.yoamhjbrsdsxshkt.zxenmspvja.tshclqdvpvg（Service）→ 居中 Toast（setGravity(16,0,0)）",
      "trigger_event": "跳转同时 startService(tshclqdvpvg) → onStartCommand，每次循环计数器 e==0 时启动一次",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Enable access for 'Flash Player Service'",
      "shown_text_zh": "为“Flash Player Service”启用访问权限",
      "user_action_requested": "在系统设置页中找到并开启该服务；Toast 无任何按钮，不可关闭",
      "code_anchor": "abywinv.yoamhjbrsdsxshkt.zxenmspvja.tshclqdvpvg.onStartCommand"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "bwcjkmlxieed.onHandleIntent 循环（sleep 700ms）+ twui.onHandleIntent 循环（sleep 1000ms）",
      "trigger_event": "b.g() 持续返回 false（用户返回或未开启）→ 再次 startActivity(cicvqlwecww) 跳 ACCESSIBILITY_SETTINGS；e 计数器到 25 后重置，循环无终止条件；同时请求设备管理器激活（qejyiyqn.a.b）与 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 页面",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "用户退出设置页后约 0.7~1 秒即被重新拉回无障碍设置页，形成强制重跳，无降级路径",
      "user_action_requested": "除开启权限外无其它出路（无取消、无跳过、无手动模式）",
      "code_anchor": "abywinv.yoamhjbrsdsxshkt.zxenmspvja.bwcjkmlxieed.onHandleIntent"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "abywinv.yoamhjbrsdsxshkt.zxenmspvja.qsxsqjtwrwa（AccessibilityService，label=Flash Player Service）",
      "trigger_event": "系统启用服务 → onServiceConnected；b.g() 返回 true 后循环停止重跳",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务连通后进入后台事件监听（叠加银行/键盘/短信相关能力，本轮未展开核验）",
      "user_action_requested": "无",
      "code_anchor": "abywinv.yoamhjbrsdsxshkt.zxenmspvja.qsxsqjtwrwa.onServiceConnected"
    }
  ],
  "text_presentation_locations": [
    "居中 Toast（gravity=16）：tshclqdvpvg.onStartCommand 拼接 StringAccessibility + \" '\" + \"Flash Player Service\" + \"'\"，即 “Enable access for 'Flash Player Service'”",
    "系统无障碍服务列表项名称：Manifest 中 android:label=\"Flash Player Service\"",
    "桌面图标名：Manifest application android:label=\"Flash Player\"",
    "多语言字符串表（非资源，硬编码数组）：abywinv.yoamhjbrsdsxshkt.zxenmspvja.a.h（激活）、a.i（Enable access for）、a.j（Allow）、a.k（Yes）、a.l/a.m（uninstall/to remove），按系统语言选择",
    "前台通知栏：twui 中 Notification.Builder setContentTitle(\"Info\") / setContentText(\"Update The Driver System..\")",
    "假更新提示文案：twui 锁屏分支调用 b.a(context, \"Google\", \"Update Google Play Service\")",
    "云端 WebView 页面：ljplrclkeauc.onCreate 中 webView.loadUrl(this.b.o)（配置项 url），包内无该页面文本"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Enable access for",
      "text_zh": "为……启用访问权限",
      "source_location": "abywinv.yoamhjbrsdsxshkt.zxenmspvja.a#i（多语言数组 en 项）+ b.b() 中 d(context,\"StringAccessibility\",\"Enable access for\")",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Flash Player Service",
      "text_zh": "Flash Player 服务",
      "source_location": "AndroidManifest.xml service android:label + tshclqdvpvg.onStartCommand 硬编码",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "activate",
      "text_zh": "激活",
      "source_location": "abywinv.yoamhjbrsdsxshkt.zxenmspvja.a#h（en 项，写入 StringActivate）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Allow",
      "text_zh": "允许",
      "source_location": "abywinv.yoamhjbrsdsxshkt.zxenmspvja.a#j（en 项，写入 StringPermis）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Yes",
      "text_zh": "是",
      "source_location": "abywinv.yoamhjbrsdsxshkt.zxenmspvja.a#k（en 项，写入 StringYes）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Update The Driver System..",
      "text_zh": "正在更新驱动系统..",
      "source_location": "abywinv.yoamhjbrsdsxshkt.zxenmspvja.twui.onHandleIntent 前台通知 setContentText",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Update Google Play Service",
      "text_zh": "更新 Google Play 服务",
      "source_location": "abywinv.yoamhjbrsdsxshkt.zxenmspvja.twui.onHandleIntent（锁屏且 foregroundwhile=true，SDK>=26 分支）",
      "rhetorical_frame": "假更新"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "bwcjkmlxieed.onHandleIntent 以 sleep(700ms) 循环、twui 以 sleep(1000ms) 循环持续调用 b.g() 检测无障碍是否启用；未启用即以 FLAG_ACTIVITY_NEW_TASK|CLEAR_TASK 重新拉起 cicvqlwecww，而后者 onCreate 立即再 startActivity(ACCESSIBILITY_SETTINGS)。用户按返回退出设置页后约 0.5~1 秒即被重新拉回，计数器 e 达 25 后归零继续，无终止条件；AlarmManager startAlarm(Interval 默认 10000ms) 与 BOOT_COMPLETED/USER_PRESENT/SCREEN_ON 广播保证重启后继续",
    "overlay_or_fake_settings": "无半透明遮罩、无全屏悬浮窗、无高仿系统开关页；仅在每次跳转时于屏幕正中（gravity=16）弹出一枚不可交互 Toast 作文字指引",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "未确认（预筛线索 WATCH_SETTINGS/WATCH_PKG_INSTALLER 指向 qsxsqjtwrwa.onAccessibilityEvent 的事件监听，本轮受调用上限限制未展开；已确认的仅有获权后循环停止重跳）",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测 Activity 切换事件：一旦发现栈顶为 abywinv.yoamhjbrsdsxshkt.zxenmspvja.hngqkhpa.cicvqlwecww 或系统 android.settings.ACCESSIBILITY_SETTINGS（ACCESSIBILITY_SETTINGS 页面），立刻抓取当前屏与随后 2 秒内的 Toast；冷启动后 1~3 秒内的首跳是最佳采样窗口",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后首次跳转的系统无障碍服务列表项",
        "page_identifier": "Settings/Accessibility 页面中文本含 “Flash Player Service” 的服务条目，且此时前台应用为 abywinv.yoamhjbrsdsxshkt.zxenmspvja",
        "why_most_useful": "直接证明“无说明页直跳设置页”且服务名伪装为 Flash Player，是诱导最核心的落点",
        "observable_utg_signals": ["服务名文本 Flash Player Service", "同一包名在 1 秒内多次重复出现该页面", "无任何自建说明 Activity 文本"]
      },
      {
        "page_role": "跳转瞬间的居中 Toast 引导层",
        "page_identifier": "屏幕中央短时 Toast 文本 “Enable access for 'Flash Player Service'”",
        "why_most_useful": "Toast 是本样本唯一的口头引导载体，证明文案来源与伪装品牌绑定",
        "observable_utg_signals": ["Toast 文本内容", "Toast 出现频次（每次重跳一次）", "Toast 位置居中且无按钮"]
      },
      {
        "page_role": "伪装外壳 WebView 页",
        "page_identifier": "ljplrclkeauc 内 WebView，加载 URL 来自配置项 url（默认 https://comicwalker.at）",
        "why_most_useful": "确认桌面图标消失后用户看到的是云端页面，解释变脸与远端可控性",
        "observable_utg_signals": ["WebView 页面标题/域名", "页面无原生控件、无权限说明文字"]
      },
      {
        "page_role": "拒权后重跳的闭环证据",
        "page_identifier": "从设置页返回桌面后 ≤1s 再次出现 ACCESSIBILITY_SETTINGS 页",
        "why_most_useful": "区分“一次性引导”与“强制重跳循环”，是本样本胁迫性的决定性观测",
        "observable_utg_signals": ["返回后页面切换时间间隔（约 0.5~1s）", "重复次数（计数到 25 后重置）", "同时出现的设备管理器激活页 / 电池优化白名单页"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "盲区：桌面图标在首启即自禁用，二次启动无法从桌面进入，UTG 必须以“首次安装后首启”为采样起点；正常功能外壳为远端 WebView（默认域名 comicwalker.at），断网时可能不显示外壳而仅剩跳转；无障碍配置 res/xml/aeswfjjxlsp.xml 为未解码二进制 AXML；获权后的防撤权行为本轮未核验"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_WEBVIEW_REMOTE_URL",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "abywinv.yoamhjbrsdsxshkt.zxenmspvja.hngqkhpa.ljplrclkeauc.onCreate",
    "abywinv.yoamhjbrsdsxshkt.zxenmspvja.hngqkhpa.cicvqlwecww.onCreate",
    "abywinv.yoamhjbrsdsxshkt.zxenmspvja.bwcjkmlxieed.onHandleIntent",
    "abywinv.yoamhjbrsdsxshkt.zxenmspvja.tshclqdvpvg.onStartCommand",
    "abywinv.yoamhjbrsdsxshkt.zxenmspvja.b#g",
    "abywinv.yoamhjbrsdsxshkt.zxenmspvja.a#i"
  ]
}
```

</details>
