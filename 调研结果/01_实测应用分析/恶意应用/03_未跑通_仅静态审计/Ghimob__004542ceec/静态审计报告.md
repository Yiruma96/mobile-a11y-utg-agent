# MR_033__004542ceec｜Ghimob — Habilitar GoogleDocs

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：203.4s

## 1. 一句话核心结论

- **核心申请方式**：伪装成“启用 GoogleDocs”的银行木马，每次回到应用即不可取消地强制跳入系统无障碍服务详情页，拒绝返回则立即重跳、每 30 分钟通知拉回，获权后立即用全局 BACK/HOME 关闭设置页并禁用桌面图标隐藏自身。
- **静态可见性说明**：核心流程与目标组件全部静态可见，无加壳、无 VMP、无远端 HTML 或二阶段载荷。界面引导文案以自研 Base64+字符对偏移算法加密存放于 resources.arsc strings（密钥链 x.b.t->u(...,1010) 解出数值键 666，x.b.K/x.b.D 按索引取串），已用该密钥还原出 com.android.settings.Settings$AccessibilityInstalledServiceActivity、accessibility_enabled、com.intelsyss.plugins/com.intelsyss.plugins.a2y 等关键串；仅少数含葡萄牙语变音符号的按钮/提示文案未逐条枚举，不影响流程与页面流转判定。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `004542ceec2edc55d28350f3990143af4e5006592bbd72d5449d444e93a63fb8` |
| 包名 / 年份 | `com.intelsyss.plugins` / 2020 |
| 家族 / 品类 | **Ghimob**（同池样本数：4） |
| 原始来源标识 | https://securelist.com/ghimob-tetrade-threat-mobile-devices/99228/ |
| 桌面显示名 | Habilitar GoogleDocs |
| 引导页宣称品牌/身份 | Google（GoogleDocs / Google Defender） |
| 系统无障碍列表服务名 | 服务项 com.intelsyss.plugins.a2y；配置中未提供 android:description，系统无障碍列表以应用 label“Habilitar GoogleDocs”呈现，点击后 settingsActivity 指向 com.git.GoogleDefender.m1x（Google Defender） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 包名 com.intelsyss.plugins 与应用名“Habilitar GoogleDocs”完全无关，借用 Google 品牌；2) serviceconfig.xml 的 settingsActivity 指向 com.git.GoogleDefender.m1x，在系统无障碍界面呈现为第三方“Google Defender”组件而非真实入口 m1x；3) 全部界面文案以自研 Base64+字符对偏移（密钥 1010→666）加密存于 resources.arsc，静态扫描无法直接读到葡萄牙语引导语；4) 未设置 android:description，系统无障碍列表不展示能力说明，掩盖 canRetrieveWindowContent/canPerformGestures 全量能力；5) l() 检测模拟器/调试器后 killProcess 自杀，规避沙箱分析。 |
| 无障碍服务类名 | `com.intelsyss.plugins.a2y` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.intelsyss.plugins.m1x（LAUNCHER Activity，layout 2131296284=activity_main） | onCreate() | 原生Activity | **原文**：Habilitar GoogleDocs<br>**译注**：桌面图标名与页面标题：“启用 Google 文档”，界面内仅一个“ACTIVAR（激活）”按钮，其余控件被 setVisibility(8) 隐藏 | 仅呈现一个 ACTIVAR 按钮（2131165218），无取消/跳过按钮；按钮初始被隐藏，用户无有效交互选项 | `com.intelsyss.plugins.m1x.onCreate / res/layout/activity_main.xml` |
| 2 | 跳无障碍设置 | 系统设置 com.android.settings.Settings$AccessibilityInstalledServiceActivity（无障碍服务详情页），经 startActivityForResult(intent, 333) 进入 | onResume()：o() 判定本无障碍服务未开启后立即发起跳转 | 系统无障碍页 | **原文**：无（跳转前仅 Toast：b.D(this,15) + getString(2131427472)）<br>**译注**：跳转前弹出一条 Toast 提示，随后直接进入系统无障碍中本服务的开关页；不存在应用侧确认弹窗或说明页 | 在系统页面手动打开“Habilitar GoogleDocs / com.intelsyss.plugins.a2y”开关；无取消或跳过入口，按钮仅为 ACTIVAR | `com.intelsyss.plugins.m1x.onResume / x.b.D（索引 12/13/14/20）` |
| 3 | 拒权反馈循环 | 再次跳入无障碍服务设置页（startActivityForResult(..., 20)） | onActivityResult(requestCode=333, resultCode != RESULT_OK)：用户在设置页按返回或未开启开关 | 系统无障碍页 | 无 | 被迫再次面对同一开关；无“稍后”“取消”“不再提醒”路径 | `com.intelsyss.plugins.m1x.onActivityResult / x.b.D（索引 21）` |
| 4 | 业务功能触发 | 通知栏常驻通知（x.b.I 构造，contentIntent 指向 m1x）+ Timer m1x$a（1800000 ms） | onCreate 中 schedule(m1x$a, 1800000, 1800000)；onResume 中 b.I(...) 发通知 | 通知栏 | **原文**：getString(2131427472)（通知标题，加密资源，静态未解出明文）<br>**译注**：周期通知（标题为加密字符串），点击后回到应用并被再次推入无障碍设置页 | 点击通知即回到应用→自动再跳设置页；30 分钟一次循环拉回，无关闭引导入口 | `com.intelsyss.plugins.m1x$a.run / x.b.I` |
| 5 | 获权后动作 | AccessibilityService com.intelsyss.plugins.a2y | onServiceConnected()（用户开启开关后系统回调） | 系统无障碍页 | 无 | 无交互；用户已无法通过界面返回撤销授权，需自行重新进入系统设置 | `com.intelsyss.plugins.a2y.onServiceConnected / com.intelsyss.plugins.a2y.w` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 桌面图标与系统无障碍列表项：application label = Habilitar GoogleDocs（resources.arsc @7F0B0090），系统无障碍列表以该 label 作为服务条目名
- m1x 原生 Activity（layout activity_main，setContentView 2131296284）：仅显示 ACTIVAR 按钮，其余视图 setVisibility(8)，无说明文字页
- Toast（m1x.onResume / m1x$a.run）：b.D(this,15) + getString(2131427472)，文案加密存储，静态未解出明文
- 通知栏常驻通知（x.b.I，标题 getString(2131427472)，contentIntent 指向 m1x）
- 系统无障碍服务详情页（com.android.settings.Settings$AccessibilityInstalledServiceActivity）：应用不提供 android:description，该页不展示任何能力说明；点击条目则进入 serviceconfig.xml 指定的 com.git.GoogleDefender.m1x
- 全部界面文案（含 ACTIVAR/DESACTIVAR、Toast、通知标题）均以 Base64+字符对偏移加密存于 resources.arsc strings，需经 x.b.t/u 以密钥 1010→666 解密，非 assets 或 res/values 明文 XML

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| es | Habilitar GoogleDocs | 启用 Google 文档 | `resources.arsc @7F0B0090（application label）` | 良性透明说明 |
| es | ACTIVAR | 激活 | `加密 strings（x.b.D 索引串，密钥 666）/ m1x 按钮 2131165218` | 受限设置分步教学 |
| es | DESACTIVAR | 停用 | `加密 strings（x.b.D 索引串，密钥 666）` | 未知 |
| pt | Modo Seguro / Modo de Segurança | 安全模式 | `resources.arsc strings（密钥 666 解出，用于后续话术/日志字段）` | 假反诈安全 |
| pt | Redefina seu telefone / Redefina as configurações / Restaurar config / Restaurar dados / Fazer backup dos dados | 重置您的手机 / 重置设置 / 恢复配置 / 恢复数据 / 备份数据 | `resources.arsc strings（密钥 666 解出，属远端指令/话术模板）` | 假更新 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：onActivityResult(requestCode=333, resultCode != RESULT_OK) 立即以第二个 Intent（解密串索引 21）再次 startActivityForResult(..., 20) 重跳；每次 onResume 也再次无条件 startActivityForResult(333)；另有 Timer m1x$a 每 1800000 ms（30 分钟）发通知并带 FLAG_ACTIVITY_NEW_TASK 直接拉起设置页，形成三层重跳闭环
- **遮罩叠层 / 高仿系统设置页**：无悬浮窗遮罩、无高仿系统开关页；诱导靠冒充品牌的服务入口（serviceconfig.xml 的 settingsActivity 指向 com.git.GoogleDefender.m1x）+ 直跳系统无障碍服务详情页实现
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=27，未发现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转、'允许受限设置'分步教学或 Session 安装器绕过逻辑）
- **获权后即时行为与防撤权机制**：有：a2y.onServiceConnected() 在连接后立即 performGlobalAction(1)（BACK）与 performGlobalAction(2)（HOME）关闭用户所在的系统设置页，并 setComponentEnabledSetting(m1x, 2, 1) 禁用桌面启动组件隐藏图标；a2y.w() 由 onAccessibilityEvent 持续调用，用于后续继续压制返回操作
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：最佳时机为监控到 m1x 的 onResume 之后立即出现的 Activity 切换：当目标组件为 com.android.settings/.Settings$AccessibilityInstalledServiceActivity（或包名 com.android.settings 的无障碍服务详情页）且发起方为 com.intelsyss.plugins 时立即抓取；第二个时机是同一会话内 2 秒内对该页面的第二次 startActivity（拒绝回环），以及每 30 分钟的通知点击后重新拉起
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无纯图诱导、无 WebView、无远端 HTML，UTG 文本节点即可覆盖。唯一盲区是文案以自研 Base64+偏移加密存于 resources.arsc，运行前需解密（密钥 1010→666）才能读到明文；此外 l() 检测模拟器/调试器会 killProcess 自杀，在模拟器或可调试环境下可能抓不到任何页面，需在真机运行。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后强制跳入的系统无障碍服务详情页** | com.android.settings/.Settings$AccessibilityInstalledServiceActivity，页内服务项显示 Habilitar GoogleDocs / com.intelsyss.plugins.a2y | 这是唯一的授权落点，且由应用冷启动 0 步直达、无任何前置说明页，是判定'强制跳转+不可取消'最直接的证据 | Activity 组件名 com.android.settings.Settings$AccessibilityInstalledServiceActivity；调用方包名 com.intelsyss.plugins 与 requestCode 333 的 startActivityForResult；页面文本节点含 Habilitar GoogleDocs 与 a2y 服务名；页面无 android:description 对应的能力说明文本节点 |
| **拒权回环页（同一系统设置页的第二次压栈）** | 用户在设置页按返回后 ≤1s 内再次出现的 AccessibilityInstalledServiceActivity | 区分'按需引导'与'拒绝即死循环'，是 COERCE_REFUSAL_LOOP_RELAUNCH 的关键判别信号 | 返回操作后极短时间内同一 Activity 组件再次出现在前台；两次启动间隔小于 2 秒且调用栈相同；期间无任何应用侧 Toast/Dialog 说明节点 |
| **获权瞬间的系统设置页被关闭动作** | 无障碍开关被打开后 AccessibilityInstalledServiceActivity 在数百毫秒内被 BACK 关闭并回到桌面（HOME） | 证明 post_grant_anti_removal：服务一连接就用全局动作关闭设置页，阻止用户当场撤销 | 开关置位后目标设置页立即消失、前台变为 Launcher；无用户输入事件却发生 BACK/HOME 级页面切换；无障碍服务 com.intelsyss.plugins.a2y 连接事件与页面关闭时间重合 |
| **通知栏拉回页** | 每 30 分钟出现的通知（标题为加密字符串 2131427472），点击后回到 m1x 并再次跳设置页 | 证明后台周期性重新施压，非一次性引导 | 通知来源包名 com.intelsyss.plugins、contentIntent 指向 com.intelsyss.plugins.m1x；通知点击后 1s 内出现 AccessibilityInstalledServiceActivity；通知重复出现周期约 1800000 ms |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.intelsyss.plugins.m1x.onResume`
- `com.intelsyss.plugins.m1x.onActivityResult`
- `com.intelsyss.plugins.m1x$a.run`
- `com.intelsyss.plugins.a2y.onServiceConnected`
- `x.b.D / x.b.t / x.b.u`
- `res/xml/serviceconfig.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（纯运行期 UTG 视角）

**静态可见性**：代码与资源明文可还原，无加壳、无远端 HTML。引导文案经 `x.b.u` 自研 Base64+字符对偏移算法加密存放于 `resources.arsc` 的 strings 中，密钥链为 `x.b.t → u(...,1010)` 解出 `x.b.K` 的数值键 **666**，据此可批量解密；我已用该密钥还原出设置页组件名、`accessibility_enabled`、服务组件名等关键字符串。少量含葡萄牙语变音符号的界面文案未逐条枚举，但不影响流程判定。

**引导链路（UTG 可捕获的实际页面流转）**

1. **冷启动即入局**：桌面图标显示为 `Habilitar GoogleDocs`，启动入口 [m1x.onCreate()](<resource-unit:#1.dex1 code:com.intelsyss.plugins.m1x#onCreate>) 加载 `activity_main`，先把“ACTIVAR”按钮设为 `setVisibility(8)` 隐藏，并注册 30 分钟周期定时器 `m1x$a`。同时 `l()` 检测模拟器/调试器（`sdk_google_phone_x86`、`goldfish`、`ranchu`、`vbox86` 等），命中即 `killProcess` 自杀——这是反沙箱前置开关，真机 UTG 不受影响。
2. **onResume 无条件强制跳设置页**：[m1x.onResume()](<resource-unit:#1.dex1 code:com.intelsyss.plugins.m1x#onResume>) 先以 [o()](<resource-unit:#1.dex1 code:com.intelsyss.plugins.m1x#o>) 读 `Settings.Secure.accessibility_enabled` 与 `enabled_accessibility_services` 判断本服务是否已开启；未开启则**立刻** `startActivityForResult(intent, 333)`，目标组件由解密字符串给出，即 `com.android.settings.Settings$AccessibilityInstalledServiceActivity`——Android 8+ 的**单个无障碍服务详情页**（不是列表页），用户看到的就是本应用那一项开关页。同一分支还弹 Toast 并经 `x.b.I` 发常驻通知，`contentIntent` 指回 `m1x` 自身。
3. **无取消/跳过**：界面上只把 ACTIVAR 按钮（`findViewById(2131165218)`）设为可见，`2131165272`/`2131165234` 两个控件全部 `setVisibility(8)`，代码中不存在“稍后/跳过”分支，按钮本身也非取消用途，仅作为再次被拉起的落脚点。
4. **拒绝即回环**：[onActivityResult()](<resource-unit:#1.dex1 code:com.intelsyss.plugins.m1x#onActivityResult>) 对 `requestCode==333` 且 `resultCode != RESULT_OK` 的情况，立即构造第二个 Intent（action 取解密串索引 21）再次 `startActivityForResult(..., 20)`。用户在设置页按返回、未开启开关，就立刻被压回同一系统页，形成“返回→再进”的硬循环。
5. **定时重拉**：[m1x$a.run()](<resource-unit:#1.dex1 code:com.intelsyss.plugins.m1x#run>) 每 1800000 ms（30 分钟）重发通知并带 `FLAG_ACTIVITY_NEW_TASK` 直接 `startActivity` 回设置页；若期间已授权（`o()` 为真）则隐藏按钮并 `finish`。
6. **冒充身份的入口**：无障碍服务 `com.intelsyss.plugins.a2y` 的配置 [res/xml/serviceconfig.xml](<resource-unit:#1 file:res/xml/serviceconfig.xml>) 把 `settingsActivity` 指向 `com.git.GoogleDefender.m1x`，在系统无障碍界面点击该项时进入的是“Google Defender”命名的 Activity；应用 label 为 `Habilitar GoogleDocs`，包名 `com.intelsyss.plugins` 与之毫无关联。
7. **获权后即锁死退路**：[a2y.onServiceConnected()](<resource-unit:#1.dex1 code:com.intelsyss.plugins.a2y#onServiceConnected>) 一上来连发 `performGlobalAction(1)`（BACK）与 `performGlobalAction(2)`（HOME），把用户正停留的设置页直接关掉；随后 `setComponentEnabledSetting(m1x, 2, 1)` 禁用桌面启动组件使图标消失，再用 `serviceInfo.flags = 119`、`eventTypes = -1` 接管全量事件与窗口内容。`a2y.w()` 在 `onAccessibilityEvent` 中持续被调用，用于事后继续压制返回操作。

**关键判断**：全程没有悬浮窗遮罩、没有高仿系统开关页、没有 WebView 教学页、也没有 Android 13+“允许受限设置”分步教学（`targetSdkVersion=27`，未见 `ACTION_APPLICATION_DETAILS_SETTINGS`）。诱导完全依靠“冒充 Google 品牌的应用名 + 直跳系统服务详情页 + 不可取消 + 返回即回环 + 30 分钟通知拉回 + 获权后 BACK/HOME 压制”这套组合，属于典型的 2020 年巴西银行木马家族（Ghimob 系）无障碍授权劫持手法。该链路已由项目既有风险 R-001 覆盖，本次核验结论与之一致。

```json
{
  "static_visibility": "clear",
  "visibility_note": "核心流程与目标组件全部静态可见，无加壳、无 VMP、无远端 HTML 或二阶段载荷。界面引导文案以自研 Base64+字符对偏移算法加密存放于 resources.arsc strings（密钥链 x.b.t->u(...,1010) 解出数值键 666，x.b.K/x.b.D 按索引取串），已用该密钥还原出 com.android.settings.Settings$AccessibilityInstalledServiceActivity、accessibility_enabled、com.intelsyss.plugins/com.intelsyss.plugins.a2y 等关键串；仅少数含葡萄牙语变音符号的按钮/提示文案未逐条枚举，不影响流程与页面流转判定。",
  "summary_one_liner": "伪装成“启用 GoogleDocs”的银行木马，每次回到应用即不可取消地强制跳入系统无障碍服务详情页，拒绝返回则立即重跳、每 30 分钟通知拉回，获权后立即用全局 BACK/HOME 关闭设置页并禁用桌面图标隐藏自身。",
  "disguise_identity": {
    "app_display_name": "Habilitar GoogleDocs",
    "claimed_brand_or_persona": "Google（GoogleDocs / Google Defender）",
    "a11y_service_label": "服务项 com.intelsyss.plugins.a2y；配置中未提供 android:description，系统无障碍列表以应用 label“Habilitar GoogleDocs”呈现，点击后 settingsActivity 指向 com.git.GoogleDefender.m1x（Google Defender）",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 包名 com.intelsyss.plugins 与应用名“Habilitar GoogleDocs”完全无关，借用 Google 品牌；2) serviceconfig.xml 的 settingsActivity 指向 com.git.GoogleDefender.m1x，在系统无障碍界面呈现为第三方“Google Defender”组件而非真实入口 m1x；3) 全部界面文案以自研 Base64+字符对偏移（密钥 1010→666）加密存于 resources.arsc，静态扫描无法直接读到葡萄牙语引导语；4) 未设置 android:description，系统无障碍列表不展示能力说明，掩盖 canRetrieveWindowContent/canPerformGestures 全量能力；5) l() 检测模拟器/调试器后 killProcess 自杀，规避沙箱分析。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.intelsyss.plugins.m1x（LAUNCHER Activity，layout 2131296284=activity_main）",
      "trigger_event": "onCreate()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Habilitar GoogleDocs",
      "shown_text_zh": "桌面图标名与页面标题：“启用 Google 文档”，界面内仅一个“ACTIVAR（激活）”按钮，其余控件被 setVisibility(8) 隐藏",
      "user_action_requested": "仅呈现一个 ACTIVAR 按钮（2131165218），无取消/跳过按钮；按钮初始被隐藏，用户无有效交互选项",
      "code_anchor": "com.intelsyss.plugins.m1x.onCreate / res/layout/activity_main.xml"
    },
    {
      "step": 2,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 com.android.settings.Settings$AccessibilityInstalledServiceActivity（无障碍服务详情页），经 startActivityForResult(intent, 333) 进入",
      "trigger_event": "onResume()：o() 判定本无障碍服务未开启后立即发起跳转",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（跳转前仅 Toast：b.D(this,15) + getString(2131427472)）",
      "shown_text_zh": "跳转前弹出一条 Toast 提示，随后直接进入系统无障碍中本服务的开关页；不存在应用侧确认弹窗或说明页",
      "user_action_requested": "在系统页面手动打开“Habilitar GoogleDocs / com.intelsyss.plugins.a2y”开关；无取消或跳过入口，按钮仅为 ACTIVAR",
      "code_anchor": "com.intelsyss.plugins.m1x.onResume / x.b.D（索引 12/13/14/20）"
    },
    {
      "step": 3,
      "stage": "拒权反馈循环",
      "screen_or_component": "再次跳入无障碍服务设置页（startActivityForResult(..., 20)）",
      "trigger_event": "onActivityResult(requestCode=333, resultCode != RESULT_OK)：用户在设置页按返回或未开启开关",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "用户返回后不做任何说明，立即被再次压回同一系统设置页，形成返回→重跳的死循环",
      "user_action_requested": "被迫再次面对同一开关；无“稍后”“取消”“不再提醒”路径",
      "code_anchor": "com.intelsyss.plugins.m1x.onActivityResult / x.b.D（索引 21）"
    },
    {
      "step": 4,
      "stage": "业务功能触发",
      "screen_or_component": "通知栏常驻通知（x.b.I 构造，contentIntent 指向 m1x）+ Timer m1x$a（1800000 ms）",
      "trigger_event": "onCreate 中 schedule(m1x$a, 1800000, 1800000)；onResume 中 b.I(...) 发通知",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "getString(2131427472)（通知标题，加密资源，静态未解出明文）",
      "shown_text_zh": "周期通知（标题为加密字符串），点击后回到应用并被再次推入无障碍设置页",
      "user_action_requested": "点击通知即回到应用→自动再跳设置页；30 分钟一次循环拉回，无关闭引导入口",
      "code_anchor": "com.intelsyss.plugins.m1x$a.run / x.b.I"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "AccessibilityService com.intelsyss.plugins.a2y",
      "trigger_event": "onServiceConnected()（用户开启开关后系统回调）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务一连上即执行 performGlobalAction(1)=返回 与 performGlobalAction(2)=主页，把用户正在操作的无障碍设置页强行关闭，并禁用 m1x 启动组件使桌面图标消失",
      "user_action_requested": "无交互；用户已无法通过界面返回撤销授权，需自行重新进入系统设置",
      "code_anchor": "com.intelsyss.plugins.a2y.onServiceConnected / com.intelsyss.plugins.a2y.w"
    }
  ],
  "text_presentation_locations": [
    "桌面图标与系统无障碍列表项：application label = Habilitar GoogleDocs（resources.arsc @7F0B0090），系统无障碍列表以该 label 作为服务条目名",
    "m1x 原生 Activity（layout activity_main，setContentView 2131296284）：仅显示 ACTIVAR 按钮，其余视图 setVisibility(8)，无说明文字页",
    "Toast（m1x.onResume / m1x$a.run）：b.D(this,15) + getString(2131427472)，文案加密存储，静态未解出明文",
    "通知栏常驻通知（x.b.I，标题 getString(2131427472)，contentIntent 指向 m1x）",
    "系统无障碍服务详情页（com.android.settings.Settings$AccessibilityInstalledServiceActivity）：应用不提供 android:description，该页不展示任何能力说明；点击条目则进入 serviceconfig.xml 指定的 com.git.GoogleDefender.m1x",
    "全部界面文案（含 ACTIVAR/DESACTIVAR、Toast、通知标题）均以 Base64+字符对偏移加密存于 resources.arsc strings，需经 x.b.t/u 以密钥 1010→666 解密，非 assets 或 res/values 明文 XML"
  ],
  "verbatim_texts": [
    {
      "lang": "es",
      "text_verbatim": "Habilitar GoogleDocs",
      "text_zh": "启用 Google 文档",
      "source_location": "resources.arsc @7F0B0090（application label）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "es",
      "text_verbatim": "ACTIVAR",
      "text_zh": "激活",
      "source_location": "加密 strings（x.b.D 索引串，密钥 666）/ m1x 按钮 2131165218",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "es",
      "text_verbatim": "DESACTIVAR",
      "text_zh": "停用",
      "source_location": "加密 strings（x.b.D 索引串，密钥 666）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "pt",
      "text_verbatim": "Modo Seguro / Modo de Segurança",
      "text_zh": "安全模式",
      "source_location": "resources.arsc strings（密钥 666 解出，用于后续话术/日志字段）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "pt",
      "text_verbatim": "Redefina seu telefone / Redefina as configurações / Restaurar config / Restaurar dados / Fazer backup dos dados",
      "text_zh": "重置您的手机 / 重置设置 / 恢复配置 / 恢复数据 / 备份数据",
      "source_location": "resources.arsc strings（密钥 666 解出，属远端指令/话术模板）",
      "rhetorical_frame": "假更新"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "onActivityResult(requestCode=333, resultCode != RESULT_OK) 立即以第二个 Intent（解密串索引 21）再次 startActivityForResult(..., 20) 重跳；每次 onResume 也再次无条件 startActivityForResult(333)；另有 Timer m1x$a 每 1800000 ms（30 分钟）发通知并带 FLAG_ACTIVITY_NEW_TASK 直接拉起设置页，形成三层重跳闭环",
    "overlay_or_fake_settings": "无悬浮窗遮罩、无高仿系统开关页；诱导靠冒充品牌的服务入口（serviceconfig.xml 的 settingsActivity 指向 com.git.GoogleDefender.m1x）+ 直跳系统无障碍服务详情页实现",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=27，未发现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转、'允许受限设置'分步教学或 Session 安装器绕过逻辑）",
    "post_grant_anti_removal": "有：a2y.onServiceConnected() 在连接后立即 performGlobalAction(1)（BACK）与 performGlobalAction(2)（HOME）关闭用户所在的系统设置页，并 setComponentEnabledSetting(m1x, 2, 1) 禁用桌面启动组件隐藏图标；a2y.w() 由 onAccessibilityEvent 持续调用，用于后续继续压制返回操作",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "最佳时机为监控到 m1x 的 onResume 之后立即出现的 Activity 切换：当目标组件为 com.android.settings/.Settings$AccessibilityInstalledServiceActivity（或包名 com.android.settings 的无障碍服务详情页）且发起方为 com.intelsyss.plugins 时立即抓取；第二个时机是同一会话内 2 秒内对该页面的第二次 startActivity（拒绝回环），以及每 30 分钟的通知点击后重新拉起",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后强制跳入的系统无障碍服务详情页",
        "page_identifier": "com.android.settings/.Settings$AccessibilityInstalledServiceActivity，页内服务项显示 Habilitar GoogleDocs / com.intelsyss.plugins.a2y",
        "why_most_useful": "这是唯一的授权落点，且由应用冷启动 0 步直达、无任何前置说明页，是判定'强制跳转+不可取消'最直接的证据",
        "observable_utg_signals": [
          "Activity 组件名 com.android.settings.Settings$AccessibilityInstalledServiceActivity",
          "调用方包名 com.intelsyss.plugins 与 requestCode 333 的 startActivityForResult",
          "页面文本节点含 Habilitar GoogleDocs 与 a2y 服务名",
          "页面无 android:description 对应的能力说明文本节点"
        ]
      },
      {
        "page_role": "拒权回环页（同一系统设置页的第二次压栈）",
        "page_identifier": "用户在设置页按返回后 ≤1s 内再次出现的 AccessibilityInstalledServiceActivity",
        "why_most_useful": "区分'按需引导'与'拒绝即死循环'，是 COERCE_REFUSAL_LOOP_RELAUNCH 的关键判别信号",
        "observable_utg_signals": [
          "返回操作后极短时间内同一 Activity 组件再次出现在前台",
          "两次启动间隔小于 2 秒且调用栈相同",
          "期间无任何应用侧 Toast/Dialog 说明节点"
        ]
      },
      {
        "page_role": "获权瞬间的系统设置页被关闭动作",
        "page_identifier": "无障碍开关被打开后 AccessibilityInstalledServiceActivity 在数百毫秒内被 BACK 关闭并回到桌面（HOME）",
        "why_most_useful": "证明 post_grant_anti_removal：服务一连接就用全局动作关闭设置页，阻止用户当场撤销",
        "observable_utg_signals": [
          "开关置位后目标设置页立即消失、前台变为 Launcher",
          "无用户输入事件却发生 BACK/HOME 级页面切换",
          "无障碍服务 com.intelsyss.plugins.a2y 连接事件与页面关闭时间重合"
        ]
      },
      {
        "page_role": "通知栏拉回页",
        "page_identifier": "每 30 分钟出现的通知（标题为加密字符串 2131427472），点击后回到 m1x 并再次跳设置页",
        "why_most_useful": "证明后台周期性重新施压，非一次性引导",
        "observable_utg_signals": [
          "通知来源包名 com.intelsyss.plugins、contentIntent 指向 com.intelsyss.plugins.m1x",
          "通知点击后 1s 内出现 AccessibilityInstalledServiceActivity",
          "通知重复出现周期约 1800000 ms"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无纯图诱导、无 WebView、无远端 HTML，UTG 文本节点即可覆盖。唯一盲区是文案以自研 Base64+偏移加密存于 resources.arsc，运行前需解密（密钥 1010→666）才能读到明文；此外 l() 检测模拟器/调试器会 killProcess 自杀，在模拟器或可调试环境下可能抓不到任何页面，需在真机运行。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.intelsyss.plugins.m1x.onResume",
    "com.intelsyss.plugins.m1x.onActivityResult",
    "com.intelsyss.plugins.m1x$a.run",
    "com.intelsyss.plugins.a2y.onServiceConnected",
    "x.b.D / x.b.t / x.b.u",
    "res/xml/serviceconfig.xml"
  ]
}
```

</details>
