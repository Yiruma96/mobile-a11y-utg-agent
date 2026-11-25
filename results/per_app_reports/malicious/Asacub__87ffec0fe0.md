# MR_108__87ffec0fe0｜Asacub — CМС - Пoслание

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：262.2s

## 1. 一句话核心结论

- **核心申请方式**：桌面入口一启动即自禁用隐身，后台 Handler 每 10.47 秒在锁屏上拉起透明 Activity，弹出不可取消的伪造“系统故障”弹窗并用三步文字教学把用户送进系统无障碍设置，开启伪装成“系统应用程序”的无障碍服务。
- **静态可见性说明**：全部引导链路在 classes.dex 明文中完整可见：无加壳、无 AES 载荷、无远端 HTML/WebView。仅远端控制服务器 http://wedonairin.com/dfz9ix6x1oo2a56imb/index.php 下发的包名/控件ID黑名单（SharedPreferences 键 Packet / 58aaffd78d9）与开关指令在运行期获取，属获权后动作的云控参数，不影响权限引导页面的静态还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `87ffec0fe0e7a83e6433694d7f24cfde2f70fc45800aa2acb8e816ceba428951` |
| 包名 / 年份 | `ru.tent.paralyzed` / 2018 |
| 家族 / 品类 | **Asacub**（同池样本数：9） |
| 原始来源标识 | https://securelist.com/the-rise-of-mobile-banker-asacub/87591/ |
| 桌面显示名 | CМС - Пoслание |
| 引导页宣称品牌/身份 | 系统组件（弹窗标题“Сиcтeмнaя нeполадка / 系统故障”，要求启用名为“Cистeмноe приложeниe / 系统应用程序”的服务） |
| 系统无障碍列表服务名 | Cистeмноe приложeниe |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：西里尔/拉丁同形字混排：服务名 Cистeмноe приложeниe 与桌面名 CМС - Пoслание 中 и/е/о/М/С 交替使用西里尔与拉丁字母，绕过肉眼与关键词比对；无障碍配置 @xml/iwrrcpapl 完全省略 android:description，系统列表不显示任何用途说明；LAUNCHER Activity 首次运行后 setComponentEnabledSetting(COMPONENT_ENABLED_STATE_DISABLED) 自禁用，桌面图标消失以规避事后取证与卸载；仅一个 activity-alias 层面的无（未使用多 alias），未伪造 isAccessibilityTool。 |
| 无障碍服务类名 | `ru.tent.paralyzed.CabinetViable` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_CONTACTS, READ_SMS, RECEIVE_SMS, SEND_SMS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | ru.tent.paralyzed.DineConventional（LAUNCHER Activity，android:noHistory="true"） | 用户点击桌面图标 → onCreate | 原生Activity | 无 | 无（用户仅看到图标闪退，无按钮、无提示） | `ru.tent.paralyzed.DineConventional.onCreate / DineConventional.a` |
| 2 | 业务功能触发 | ru.tent.paralyzed.Correction（Application）+ HandlerThread 定时任务 Correction$3 | Application.onCreate → b() 启动 HandlerThread 并 postDelayed(10470ms) 循环；条件 b.a==false（无障碍未连接） | 不可静态还原（无 UI，纯后台定时器） | 无 | 无 | `ru.tent.paralyzed.Correction.onCreate / Correction.b / Correction$3.run` |
| 3 | 引导说明页 | ru.tent.paralyzed.Invasion（透明 Activity，android:showWhenLocked="true" android:turnScreenOn="true"）中的 AlertDialog | Correction$3.run 中 startActivity(Invasion)（flags 0x70000000）→ Invasion.onCreate → requestDismissKeyguard + 播放闹钟铃声 → a() 显示弹窗 | 原生Dialog | **原文**：Сиcтeмнaя нeполадка / Для устраннeния прoблемы Вам нeoбхoдимo включить 'Cистeмноe приложeниe'<br>1.Для этогo пeрейдите нa страницу нaстроeк<br>2.Выбeритe из cпиcкa 'Cистeмноe приложeниe'<br>3.Включитe егo.<br>**译注**：系统故障 / 为了消除该问题，您必须启用“系统应用程序”：1. 为此请转到设置页面；2. 从列表中选择“系统应用程序”；3. 将其启用。 | 只能点击唯一按钮「Пeрeйти к нaстрoйкам」（前往设置）；setCancelable(false)，无取消、无跳过、无关闭按钮 | `ru.tent.paralyzed.Invasion.a / Invasion.onCreate` |
| 4 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表页） | 弹窗 PositiveButton 回调 Invasion$1.onClick → Invasion.b() | 系统无障碍页 | **原文**：无（应用侧无自定义文案，交由系统页呈现列表项 Cистeмноe приложeниe）<br>**译注**：系统无障碍服务列表，其中一项显示为“系统应用程序”，无描述说明 | 用户需手动在列表中找到并打开“系统应用程序”开关 | `ru.tent.paralyzed.Invasion$1.onClick / Invasion.b（new Intent("android.settings.ACCESSIBILITY_SETTINGS") + FLAG_ACTIVITY_NEW_TASK + finish()）` |
| 5 | 拒权反馈循环 | Correction$1（1000ms 轮询）+ 再次拉起 Invasion 弹窗 | Correction$1.run 每秒调用 b.b() 读 Settings.Secure.enabled_accessibility_services，判断是否包含 "ru.tent.paralyzed"；未包含则 b.b=true 并重新 postDelayed(Correction$3, 10470ms) 拉起同一弹窗 | 原生Dialog（循环复用第 3 步弹窗） | **原文**：Сиcтeмнaя нeполадка / Для устраннeния прoблемы Вам нeoбхoдимo включить 'Cистeмноe приложeниe'<br>**译注**：系统故障 / 为了消除该问题，您必须启用“系统应用程序” | 无法拒绝：用户返回设置页或不开启，弹窗会在约 10.5 秒后再次出现，形成死循环 | `ru.tent.paralyzed.Correction$1.run / ru.tent.paralyzed.b.b / ru.tent.paralyzed.Correction.c` |
| 6 | 获权后动作 | ru.tent.paralyzed.CabinetViable（AccessibilityService）→ 启动 ru.tent.paralyzed.MountainPreoccupation 核心服务 | onServiceConnected() → b.a=true → c.e(getApplicationContext())；此后 onAccessibilityEvent 在 typeWindowContentChanged/StateChanged/WindowsChanged 事件上执行 | 悬浮窗Overlay（无自绘界面，以无障碍节点操作代替 UI） | **原文**：无（无自绘界面；动作由 performGlobalAction(1) 与 performAction(16) 完成）<br>**译注**：自动执行全局返回、自动点击指定控件，可压制用户撤销无障碍授权的操作；同时跳转 ACTION_CHANGE_DEFAULT 抢占默认短信应用 | 无（用户在不知情下被自动化操作） | `ru.tent.paralyzed.CabinetViable.onServiceConnected / CabinetViable.onAccessibilityEvent / CabinetViable.a(String,AccessibilityNodeInfo) / ru.tent.paralyzed.b.a` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- Invasion.onCreate → Invasion.a()：原生 AlertDialog，标题「Сиcтeмнaя нeполадка」，正文三步教学，setCancelable(false)，单一 PositiveButton「Пeрeйти к нaстрoйкам」；无自定义 layout、无 WebView
- 系统无障碍服务列表项标签：AndroidManifest.xml 中 <service android:label="Cистeмноe приложeниe" android:name="ru.tent.paralyzed.CabinetViable">
- 系统无障碍服务详情/说明区：res/xml/iwrrcpapl.xml 未声明 android:description，故空白无说明
- 桌面应用名：AndroidManifest.xml application android:label="CМС - Пoслание"（首次运行后随 LAUNCHER Activity 自禁用而消失）
- 无 assets 内 HTML、无 strings.xml 引导文案、无悬浮引导遮罩、无高仿系统设置页

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| ru | Сиcтeмнaя нeполадка | 系统故障 | `硬编码于 ru.tent.paralyzed.Invasion.a()（AlertDialog.Builder.setTitle）` | 故障恐吓 |
| ru | Для устраннeния прoблемы Вам нeoбхoдимo включить 'Cистeмноe приложeниe'<br>1.Для этогo пeрейдите нa страницу нaстроeк<br>2.Выбeритe из cпиcкa 'Cистeмноe приложeниe'<br>3.Включитe егo. | 为了消除该问题，您必须启用“系统应用程序”：1. 为此请转到设置页面；2. 从列表中选择“系统应用程序”；3. 将其启用。 | `硬编码于 ru.tent.paralyzed.Invasion.a()（AlertDialog.Builder.setMessage）` | 故障恐吓 + 受限设置分步教学 |
| ru | Пeрeйти к нaстрoйкам | 前往设置 | `硬编码于 ru.tent.paralyzed.Invasion.a()（setPositiveButton，唯一按钮）` | 受限设置分步教学 |
| ru | Cистeмноe приложeниe | 系统应用程序 | `AndroidManifest.xml 无障碍 service android:label` | 假更新 |
| ru | CМС - Пoслание | 短信 - 消息 | `AndroidManifest.xml application android:label` | 清理工具伪装 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：Correction$1 每 1000 ms 读取 Settings.Secure.enabled_accessibility_services 判断是否含本包名；未启用则置 b.b 标志并 postDelayed(Correction$3, 10470ms) 无限重新拉起 Invasion 弹窗。用户从系统设置页按返回/不开启，约 10.5 秒后弹窗再次出现在当前界面之上（NEW_TASK + 锁屏可弹），直到用户开启无障碍为止；开机广播 FolkNeglect 每分钟 AlarmManager 唤醒会重新激活整个循环。
- **遮罩叠层 / 高仿系统设置页**：无半透明引导遮罩、无全屏悬浮窗、无高仿系统无障碍开关页。Invasion 为 Theme.Translucent.NoTitleBar 的透明 Activity 承载原生 AlertDialog，仅覆盖系统页之上的弹窗层；获权后也不绘制 Overlay，改用无障碍节点操作（performGlobalAction / performAction(16)）实现等效控制。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：是。CabinetViable.onAccessibilityEvent 在窗口变化事件中对云控下发的包名匹配成功后执行 performGlobalAction(1)（GLOBAL_ACTION_BACK），并通过 findAccessibilityNodeInfosByViewId + performAction(16) 自动点击指定控件，可在用户进入应用详情/设置页撤销授权时自动返回或代为点按；同时 b.a() 立即以 ACTION_CHANGE_DEFAULT 抢占默认短信应用，进一步固化驻留。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：两种时点同时挂：①监测到 startActivity 的 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS（Invasion.b）；②监测到 Invasion 透明 Activity 被拉起（含锁屏/息屏场景）。前者捕捉跳转瞬间，后者捕捉伪造弹窗正文——该弹窗可在无任何用户点击的情况下由后台定时器触发，必须靠 Activity 生命周期而非点击事件拉起 UTG。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。引导文案为纯文本硬编码，无图片诱饵、无 WebView、无远端下发页面。唯一运行期变量是云控服务器 http://wedonairin.com/dfz9ix6x1oo2a56imb/index.php 下发的包名/控件 ID 黑名单（存 SharedPreferences 键 Packet、58aaffd78d9），仅影响获权后的自动化点击目标，不影响无障碍引导页面的 UTG 识别。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动/后台拉起的伪造系统故障弹窗页** | ru.tent.paralyzed.Invasion（Theme.Translucent.NoTitleBar，showWhenLocked=true），界面为标题“Сиcтeмнaя нeполадка”的 AlertDialog，仅一个按钮 | 这是整条诱导链唯一的信息载体，一次性给出伪故障恐吓 + 三步教学 + 不可取消三个判定要素 | 标题与正文俄文原文（含西里尔同形字）；仅存在 1 个按钮节点，且无取消/关闭节点；弹窗出现在非本应用前台（如锁屏或桌面）之上；调用方 Activity 名为 Invasion、包名 ru.tent.paralyzed |
| **系统无障碍服务列表项** | com.android.settings 无障碍服务列表中的 “Cистeмноe приложeниe” 条目 | 直接证明服务名冒充系统组件、且无任何描述说明，是身份错配的现场证据 | 条目文本 Cистeмноe приложeниe（西里尔同形字）；条目下无 summary/description 文本；条目关联包名 ru.tent.paralyzed |
| **设置页后的拒权重跳循环** | 用户从无障碍页返回后约 10.5 秒再次出现的同一 Invasion 弹窗 | 验证无取消机制与循环施压，区分一次性引导与强制循环 | 同一弹窗文本在用户返回后再次出现；两次出现间隔约 10470ms；用户未点击任何按钮即被再次覆盖 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `ru.tent.paralyzed.DineConventional.onCreate`
- `ru.tent.paralyzed.DineConventional.a`
- `ru.tent.paralyzed.Correction$3.run`
- `ru.tent.paralyzed.Invasion.a`
- `ru.tent.paralyzed.Invasion.b`
- `res/xml/iwrrcpapl.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（运行期 UTG 页面流转视角）

**可见性：完全静态可见（`clear`）** — 无加壳、无 AES 载荷、无远端 HTML，全部引导逻辑都在 `classes.dex` 的明文代码里。

**完整引导链路（4 步，无取消分支）：**

1. **冷启动即隐身**：桌面入口 [DineConventional.onCreate()](<resource-unit:#1.dex1 code:ru.tent.paralyzed.DineConventional#onCreate>) 调 [a()](<resource-unit:#1.dex1 code:ru.tent.paralyzed.DineConventional#a>) 用 `setComponentEnabledSetting(..., 2, 1)` 把自身 LAUNCHER Activity 禁用后 `finish()`（且 `noHistory=true`）。用户点图标只见闪退，无任何界面。
2. **后台定时拉起**：[Correction.onCreate()](<resource-unit:#1.dex1 code:ru.tent.paralyzed.Correction#onCreate>) 启动 HandlerThread，[Correction$3.run()](<resource-unit:#1.dex1 code:ru.tent.paralyzed.Correction$3#run>) 在 `b.a==false` 时 `startActivity(Invasion)`（`0x70000000`），周期 **10470 ms** 无限重投；`Invasion` 声明 `showWhenLocked`/`turnScreenOn`，`onCreate` 还 `requestDismissKeyguard` + 播放闹钟铃声，可在锁屏/息屏直接弹窗。
3. **伪造"系统故障"不可取消弹窗 + 三步教学**：[Invasion.a()](<resource-unit:#1.dex1 code:ru.tent.paralyzed.Invasion#a>) 建 `AlertDialog`，`setCancelable(false)`，**仅一个** PositiveButton「Пeрeйти к нaстрoйкам」（前往设置），无取消/跳过/返回可用。
4. **跳系统无障碍页**：[Invasion$1.onClick](<resource-unit:#1.dex1 code:ru.tent.paralyzed.Invasion$1#onClick>) → [Invasion.b()](<resource-unit:#1.dex1 code:ru.tent.paralyzed.Invasion#b>) `new Intent("android.settings.ACCESSIBILITY_SETTINGS")` + `FLAG_ACTIVITY_NEW_TASK` → `startActivity` + `finish()`。**未使用** `ACTION_APPLICATION_DETAILS_SETTINGS`，故无 Android 13+ 受限设置教学。

**拒权反馈循环**：[Correction$1.run()](<resource-unit:#1.dex1 code:ru.tent.paralyzed.Correction$1#run>) 每 1000 ms 调 [b.b()](<resource-unit:#1.dex1 code:ru.tent.paralyzed.b#b>) 读 `Settings.Secure.enabled_accessibility_services` 判是否含 `ru.tent.paralyzed`；未启用则每 10.47 s 重跳弹窗，用户无法靠返回键或退出设置页摆脱。

**获权后动作**：[CabinetViable.onServiceConnected()](<resource-unit:#1.dex1 code:ru.tent.paralyzed.CabinetViable#onServiceConnected>) 置标志并启动核心服务；[onAccessibilityEvent()](<resource-unit:#1.dex1 code:ru.tent.paralyzed.CabinetViable#onAccessibilityEvent>) 用 `performGlobalAction(1)`（GLOBAL_ACTION_BACK）+ `findAccessibilityNodeInfosByViewId`/`performAction(16)` 自动点按，可压制撤权流程；同时 [b.a()](<resource-unit:#1.dex1 code:ru.tent.paralyzed.b#a>) 立刻 `ACTION_CHANGE_DEFAULT` 抢占默认短信应用。

**身份伪装**：系统无障碍列表项标签 `Cистeмноe приложeниe`（"系统应用程序"），西里尔 `и/е/о` 与拉丁同形字混排；桌面名 `CМС - Пoслание` 同样 `М/о` 同形；[res/xml/iwrrcpapl.xml](<resource-unit:#1 file:res/xml/iwrrcpapl.xml#L2-L3>) 无 `android:description`，不说明用途却 `canRetrieveWindowContent="true"` 且监听全部窗口变化。

---

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部引导链路在 classes.dex 明文中完整可见：无加壳、无 AES 载荷、无远端 HTML/WebView。仅远端控制服务器 http://wedonairin.com/dfz9ix6x1oo2a56imb/index.php 下发的包名/控件ID黑名单（SharedPreferences 键 Packet / 58aaffd78d9）与开关指令在运行期获取，属获权后动作的云控参数，不影响权限引导页面的静态还原。",
  "summary_one_liner": "桌面入口一启动即自禁用隐身，后台 Handler 每 10.47 秒在锁屏上拉起透明 Activity，弹出不可取消的伪造“系统故障”弹窗并用三步文字教学把用户送进系统无障碍设置，开启伪装成“系统应用程序”的无障碍服务。",
  "disguise_identity": {
    "app_display_name": "CМС - Пoслание",
    "claimed_brand_or_persona": "系统组件（弹窗标题“Сиcтeмнaя нeполадка / 系统故障”，要求启用名为“Cистeмноe приложeниe / 系统应用程序”的服务）",
    "a11y_service_label": "Cистeмноe приложeниe",
    "identity_mismatch": true,
    "obfuscation_tricks": "西里尔/拉丁同形字混排：服务名 Cистeмноe приложeниe 与桌面名 CМС - Пoслание 中 и/е/о/М/С 交替使用西里尔与拉丁字母，绕过肉眼与关键词比对；无障碍配置 @xml/iwrrcpapl 完全省略 android:description，系统列表不显示任何用途说明；LAUNCHER Activity 首次运行后 setComponentEnabledSetting(COMPONENT_ENABLED_STATE_DISABLED) 自禁用，桌面图标消失以规避事后取证与卸载；仅一个 activity-alias 层面的无（未使用多 alias），未伪造 isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "ru.tent.paralyzed.DineConventional（LAUNCHER Activity，android:noHistory=\"true\"）",
      "trigger_event": "用户点击桌面图标 → onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无任何界面，Activity 立即 finish",
      "user_action_requested": "无（用户仅看到图标闪退，无按钮、无提示）",
      "code_anchor": "ru.tent.paralyzed.DineConventional.onCreate / DineConventional.a"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "ru.tent.paralyzed.Correction（Application）+ HandlerThread 定时任务 Correction$3",
      "trigger_event": "Application.onCreate → b() 启动 HandlerThread 并 postDelayed(10470ms) 循环；条件 b.a==false（无障碍未连接）",
      "ui_carrier": "不可静态还原（无 UI，纯后台定时器）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "后台每 10.47 秒检查一次无障碍连接标志，未连接即再次拉起引导页",
      "user_action_requested": "无",
      "code_anchor": "ru.tent.paralyzed.Correction.onCreate / Correction.b / Correction$3.run"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "ru.tent.paralyzed.Invasion（透明 Activity，android:showWhenLocked=\"true\" android:turnScreenOn=\"true\"）中的 AlertDialog",
      "trigger_event": "Correction$3.run 中 startActivity(Invasion)（flags 0x70000000）→ Invasion.onCreate → requestDismissKeyguard + 播放闹钟铃声 → a() 显示弹窗",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Сиcтeмнaя нeполадка / Для устраннeния прoблемы Вам нeoбхoдимo включить 'Cистeмноe приложeниe'\n1.Для этогo пeрейдите нa страницу нaстроeк\n2.Выбeритe из cпиcкa 'Cистeмноe приложeниe'\n3.Включитe егo.",
      "shown_text_zh": "系统故障 / 为了消除该问题，您必须启用“系统应用程序”：1. 为此请转到设置页面；2. 从列表中选择“系统应用程序”；3. 将其启用。",
      "user_action_requested": "只能点击唯一按钮「Пeрeйти к нaстрoйкам」（前往设置）；setCancelable(false)，无取消、无跳过、无关闭按钮",
      "code_anchor": "ru.tent.paralyzed.Invasion.a / Invasion.onCreate"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表页）",
      "trigger_event": "弹窗 PositiveButton 回调 Invasion$1.onClick → Invasion.b()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用侧无自定义文案，交由系统页呈现列表项 Cистeмноe приложeниe）",
      "shown_text_zh": "系统无障碍服务列表，其中一项显示为“系统应用程序”，无描述说明",
      "user_action_requested": "用户需手动在列表中找到并打开“系统应用程序”开关",
      "code_anchor": "ru.tent.paralyzed.Invasion$1.onClick / Invasion.b（new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\") + FLAG_ACTIVITY_NEW_TASK + finish()）"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "Correction$1（1000ms 轮询）+ 再次拉起 Invasion 弹窗",
      "trigger_event": "Correction$1.run 每秒调用 b.b() 读 Settings.Secure.enabled_accessibility_services，判断是否包含 \"ru.tent.paralyzed\"；未包含则 b.b=true 并重新 postDelayed(Correction$3, 10470ms) 拉起同一弹窗",
      "ui_carrier": "原生Dialog（循环复用第 3 步弹窗）",
      "shown_text_verbatim": "Сиcтeмнaя нeполадка / Для устраннeния прoблемы Вам нeoбхoдимo включить 'Cистeмноe приложeниe'",
      "shown_text_zh": "系统故障 / 为了消除该问题，您必须启用“系统应用程序”",
      "user_action_requested": "无法拒绝：用户返回设置页或不开启，弹窗会在约 10.5 秒后再次出现，形成死循环",
      "code_anchor": "ru.tent.paralyzed.Correction$1.run / ru.tent.paralyzed.b.b / ru.tent.paralyzed.Correction.c"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "ru.tent.paralyzed.CabinetViable（AccessibilityService）→ 启动 ru.tent.paralyzed.MountainPreoccupation 核心服务",
      "trigger_event": "onServiceConnected() → b.a=true → c.e(getApplicationContext())；此后 onAccessibilityEvent 在 typeWindowContentChanged/StateChanged/WindowsChanged 事件上执行",
      "ui_carrier": "悬浮窗Overlay（无自绘界面，以无障碍节点操作代替 UI）",
      "shown_text_verbatim": "无（无自绘界面；动作由 performGlobalAction(1) 与 performAction(16) 完成）",
      "shown_text_zh": "自动执行全局返回、自动点击指定控件，可压制用户撤销无障碍授权的操作；同时跳转 ACTION_CHANGE_DEFAULT 抢占默认短信应用",
      "user_action_requested": "无（用户在不知情下被自动化操作）",
      "code_anchor": "ru.tent.paralyzed.CabinetViable.onServiceConnected / CabinetViable.onAccessibilityEvent / CabinetViable.a(String,AccessibilityNodeInfo) / ru.tent.paralyzed.b.a"
    }
  ],
  "text_presentation_locations": [
    "Invasion.onCreate → Invasion.a()：原生 AlertDialog，标题「Сиcтeмнaя нeполадка」，正文三步教学，setCancelable(false)，单一 PositiveButton「Пeрeйти к нaстрoйкам」；无自定义 layout、无 WebView",
    "系统无障碍服务列表项标签：AndroidManifest.xml 中 <service android:label=\"Cистeмноe приложeниe\" android:name=\"ru.tent.paralyzed.CabinetViable\">",
    "系统无障碍服务详情/说明区：res/xml/iwrrcpapl.xml 未声明 android:description，故空白无说明",
    "桌面应用名：AndroidManifest.xml application android:label=\"CМС - Пoслание\"（首次运行后随 LAUNCHER Activity 自禁用而消失）",
    "无 assets 内 HTML、无 strings.xml 引导文案、无悬浮引导遮罩、无高仿系统设置页"
  ],
  "verbatim_texts": [
    {
      "lang": "ru",
      "text_verbatim": "Сиcтeмнaя нeполадка",
      "text_zh": "系统故障",
      "source_location": "硬编码于 ru.tent.paralyzed.Invasion.a()（AlertDialog.Builder.setTitle）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "ru",
      "text_verbatim": "Для устраннeния прoблемы Вам нeoбхoдимo включить 'Cистeмноe приложeниe'\n1.Для этогo пeрейдите нa страницу нaстроeк\n2.Выбeритe из cпиcкa 'Cистeмноe приложeниe'\n3.Включитe егo.",
      "text_zh": "为了消除该问题，您必须启用“系统应用程序”：1. 为此请转到设置页面；2. 从列表中选择“系统应用程序”；3. 将其启用。",
      "source_location": "硬编码于 ru.tent.paralyzed.Invasion.a()（AlertDialog.Builder.setMessage）",
      "rhetorical_frame": "故障恐吓 + 受限设置分步教学"
    },
    {
      "lang": "ru",
      "text_verbatim": "Пeрeйти к нaстрoйкам",
      "text_zh": "前往设置",
      "source_location": "硬编码于 ru.tent.paralyzed.Invasion.a()（setPositiveButton，唯一按钮）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "ru",
      "text_verbatim": "Cистeмноe приложeниe",
      "text_zh": "系统应用程序",
      "source_location": "AndroidManifest.xml 无障碍 service android:label",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "ru",
      "text_verbatim": "CМС - Пoслание",
      "text_zh": "短信 - 消息",
      "source_location": "AndroidManifest.xml application android:label",
      "rhetorical_frame": "清理工具伪装"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "Correction$1 每 1000 ms 读取 Settings.Secure.enabled_accessibility_services 判断是否含本包名；未启用则置 b.b 标志并 postDelayed(Correction$3, 10470ms) 无限重新拉起 Invasion 弹窗。用户从系统设置页按返回/不开启，约 10.5 秒后弹窗再次出现在当前界面之上（NEW_TASK + 锁屏可弹），直到用户开启无障碍为止；开机广播 FolkNeglect 每分钟 AlarmManager 唤醒会重新激活整个循环。",
    "overlay_or_fake_settings": "无半透明引导遮罩、无全屏悬浮窗、无高仿系统无障碍开关页。Invasion 为 Theme.Translucent.NoTitleBar 的透明 Activity 承载原生 AlertDialog，仅覆盖系统页之上的弹窗层；获权后也不绘制 Overlay，改用无障碍节点操作（performGlobalAction / performAction(16)）实现等效控制。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "是。CabinetViable.onAccessibilityEvent 在窗口变化事件中对云控下发的包名匹配成功后执行 performGlobalAction(1)（GLOBAL_ACTION_BACK），并通过 findAccessibilityNodeInfosByViewId + performAction(16) 自动点击指定控件，可在用户进入应用详情/设置页撤销授权时自动返回或代为点按；同时 b.a() 立即以 ACTION_CHANGE_DEFAULT 抢占默认短信应用，进一步固化驻留。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "两种时点同时挂：①监测到 startActivity 的 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS（Invasion.b）；②监测到 Invasion 透明 Activity 被拉起（含锁屏/息屏场景）。前者捕捉跳转瞬间，后者捕捉伪造弹窗正文——该弹窗可在无任何用户点击的情况下由后台定时器触发，必须靠 Activity 生命周期而非点击事件拉起 UTG。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动/后台拉起的伪造系统故障弹窗页",
        "page_identifier": "ru.tent.paralyzed.Invasion（Theme.Translucent.NoTitleBar，showWhenLocked=true），界面为标题“Сиcтeмнaя нeполадка”的 AlertDialog，仅一个按钮",
        "why_most_useful": "这是整条诱导链唯一的信息载体，一次性给出伪故障恐吓 + 三步教学 + 不可取消三个判定要素",
        "observable_utg_signals": ["标题与正文俄文原文（含西里尔同形字）", "仅存在 1 个按钮节点，且无取消/关闭节点", "弹窗出现在非本应用前台（如锁屏或桌面）之上", "调用方 Activity 名为 Invasion、包名 ru.tent.paralyzed"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍服务列表中的 “Cистeмноe приложeниe” 条目",
        "why_most_useful": "直接证明服务名冒充系统组件、且无任何描述说明，是身份错配的现场证据",
        "observable_utg_signals": ["条目文本 Cистeмноe приложeниe（西里尔同形字）", "条目下无 summary/description 文本", "条目关联包名 ru.tent.paralyzed"]
      },
      {
        "page_role": "设置页后的拒权重跳循环",
        "page_identifier": "用户从无障碍页返回后约 10.5 秒再次出现的同一 Invasion 弹窗",
        "why_most_useful": "验证无取消机制与循环施压，区分一次性引导与强制循环",
        "observable_utg_signals": ["同一弹窗文本在用户返回后再次出现", "两次出现间隔约 10470ms", "用户未点击任何按钮即被再次覆盖"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。引导文案为纯文本硬编码，无图片诱饵、无 WebView、无远端下发页面。唯一运行期变量是云控服务器 http://wedonairin.com/dfz9ix6x1oo2a56imb/index.php 下发的包名/控件 ID 黑名单（存 SharedPreferences 键 Packet、58aaffd78d9），仅影响获权后的自动化点击目标，不影响无障碍引导页面的 UTG 识别。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH"
  ],
  "code_anchors": [
    "ru.tent.paralyzed.DineConventional.onCreate",
    "ru.tent.paralyzed.DineConventional.a",
    "ru.tent.paralyzed.Correction$3.run",
    "ru.tent.paralyzed.Invasion.a",
    "ru.tent.paralyzed.Invasion.b",
    "res/xml/iwrrcpapl.xml"
  ]
}
```

</details>
