# BN_025__27d0291028｜极简桌面与双击锁屏 — Olauncher

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：113.6s

## 1. 一句话核心结论

- **核心申请方式**：开源极简启动器在设置页用户主动打开「Double tap to lock」开关时弹出原生说明对话框，一个按钮打开外部教程网页、另一个在 Android 9+ 跳转系统无障碍列表；无冷启动强制、无遮罩、无拒权循环，服务被 packageNames 与 typeViewClicked 严格自限且仅执行锁屏全局动作
- **静态可见性说明**：引导链全部静态可见：DEX 明文（SettingsFragment.onClick/onLongClick、S0.x.a）、res/xml/accessibility_service_config.xml、res/values/strings.xml 均可完整读取；无加壳、无 AES 密文、无远端 HTML 引导页（仅外部浏览器打开 Notion 教程，不在 APK 内）
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `27d02910287065256f2e4df8cbf28fc7cbfa6c865294d5773158b633f250bdb8` |
| 包名 / 年份 | `app.olauncher` / 2025-2026 |
| 家族 / 品类 | **极简桌面与双击锁屏**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/app.olauncher_114.apk |
| 桌面显示名 | Olauncher |
| 引导页宣称品牌/身份 | Olauncher（开源极简启动器，作者 tanujnotes，github.com/tanujnotes/Olauncher） |
| 系统无障碍列表服务名 | Olauncher |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无 |
| 无障碍服务类名 | `app.olauncher.helper.MyAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：app.olauncher.debug, app.olauncher |
| 共现高危权限 | `PACKAGE_USAGE_STATS, QUERY_ALL_PACKAGES` |
| 系统设置项说明 (`android:description`) | The accessibility permission is required to enable the gesture - double tap to lock . Any data acquired by Olauncher via this service will not leave your device. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | app.olauncher.MainActivity（HOME/LAUNCHER，singleTask，无无障碍弹窗逻辑） | onCreate / 冷启动进入桌面 | 原生Activity | 无 | 无（不请求任何权限） | `app.olauncher.MainActivity（Manifest intent-filter HOME/LAUNCHER）` |
| 2 | 业务功能触发 | app.olauncher.ui.SettingsFragment（设置页）中 id 2131231233 的「Double tap to lock」开关行 | onClick：判断 Build.VERSION.SDK_INT >= 28 且 SharedPreferences LOCK_MODE==false | 原生Activity | **原文**：Double tap to lock<br>**译注**：设置项「双击锁屏」 | 用户主动点击该开关（可随时返回，不点击则永不涉及无障碍） | `app.olauncher.ui.SettingsFragment.onClick case 2131231233` |
| 3 | 引导说明页 | MaterialAlertDialog（由 f.j(context, 2131820653, message, 2131820583, 2131820786, new S0.x(this,0), new S0.x(this,1), null, 64) 构建） | 步骤 2 的点击回调内同步弹出 | 原生Dialog | **原文**：Please turn on Olauncher's accessibility service in your device's settings to enable Double tap to lock gesture. Please note that this service is only used for this particular feature. Our accessibility service does not collect or share any data.<br>**译注**：请在设备设置中开启 Olauncher 的无障碍服务以启用双击锁屏手势。请注意该服务仅用于此功能，我们的无障碍服务不会收集或分享任何数据。 | 二选一按钮：正向按钮（S0.x case 0）打开外部教程网页；负向按钮（S0.x default）跳转系统无障碍设置；按返回或点弹窗外可取消，无强制不可取消标记 | `app.olauncher.ui.SettingsFragment.onClick / res/values/strings.xml accessibility_disclosure` |
| 4 | 引导说明页 | 外部浏览器：https://tanujnotes.notion.site/Double-tap-to-lock-Olauncher-0f7fb103ec1f47d7a90cdfdcd7fb86ef | 点击对话框正向按钮 → S0.x.a() case 0 → z0.E.T(context, url) | 原生Activity | **原文**：https://tanujnotes.notion.site/Double-tap-to-lock-Olauncher-0f7fb103ec1f47d7a90cdfdcd7fb86ef<br>**译注**：跳转外部 Notion 页面查看「双击锁屏」使用说明（页面内容不在 APK 内，未纳入本次静态证据） | 用户自行阅读网页后返回 | `S0.x.a（case 0）` |
| 5 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表） | 点击对话框负向按钮 → S0.x.a() default 分支：SettingsFragment.Y(); if (SDK_INT >= 28) P(new Intent("android.settings.ACCESSIBILITY_SETTINGS")) | 系统无障碍页 | **原文**：Olauncher — The accessibility permission is required to enable the gesture - double tap to lock . Any data acquired by Olauncher via this service will not leave your device.<br>**译注**：系统无障碍列表中显示服务名「Olauncher」与说明「启用双击锁屏手势需要无障碍权限，Olauncher 通过该服务获取的任何数据都不会离开你的设备」 | 用户在系统页手动打开 Olauncher 开关（也可直接返回，不视为拒绝反馈） | `S0.x.a / res/xml/accessibility_service_config.xml android:description` |
| 6 | 跳无障碍设置 | 同上（长按捷径） | onLongClick case 2131231233 → P(new Intent("android.settings.ACCESSIBILITY_SETTINGS")) | 系统无障碍页 | 无 | 用户手动开启服务 | `app.olauncher.ui.SettingsFragment.onLongClick` |
| 7 | 获权后动作 | app.olauncher.helper.MyAccessibilityService（android:process=:serviceProcess） | onServiceConnected：写入 SharedPreferences app.olauncher LOCK_MODE=true；onAccessibilityEvent：source 为 FrameLayout 且 contentDescription 等于 lock_layout_description 时 performGlobalAction(8) | 不可静态还原 | **原文**：lock layout description to be used a unique id to lock screen<br>**译注**：获权后仅在本应用桌面空白区（该唯一 contentDescription 的 FrameLayout）被双击时执行 GLOBAL_ACTION_LOCK_SCREEN 锁屏，不读取其他应用窗口内容、不阻止撤权 | 无（无自点确认、无 GLOBAL_ACTION_BACK/HOME 反撤权、无通知栏重拉） | `app.olauncher.helper.MyAccessibilityService.onServiceConnected / onAccessibilityEvent` |
| 8 | 拒权反馈循环 | 无（返回桌面即结束） | 用户拒绝或从系统设置返回：LOCK_MODE 保持 false | 无 | **原文**：Olauncher failed to lock device. Please check your app settings.<br>**译注**：仅在用户再次尝试双击锁屏时以 toast 提示「Olauncher 锁定设备失败，请检查应用设置」，无 onResume 死循环重跳、无定时器拉起 | 用户可永久忽略该功能 | `res/values/strings.xml launcher_failed_to_lock_device` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 设置页开关行文案：res/values/strings.xml double_tap_to_lock / double_tap_lock（「Double tap to lock」）
- 引导对话框正文：res/values/strings.xml accessibility_disclosure（含换行分段），经 SettingsFragment.onClick 由 f.j(...) 传入 MaterialAlertDialog 展示
- 系统无障碍列表服务名与说明：service android:label="@string/app_name" 与 res/xml/accessibility_service_config.xml 的 android:description=@string/accessibility_service_description
- 外部教程页：不在 APK 内，由 S0.x.a case 0 用系统浏览器打开 tanujnotes.notion.site 页面
- 设备管理员相关说明：res/values/strings.xml admin_permission_message（Android 9 以下 DevicePolicyManager 路径的对话框）
- 锁屏失败提示：res/values/strings.xml launcher_failed_to_lock_device，经 Toast（z0.E.l0/k0）展示

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Please turn on Olauncher's accessibility service in your device's settings to enable Double tap to lock gesture. Please note that this service is only used for this particular feature. Our accessibility service does not collect or share any data. | 请在设备设置中开启 Olauncher 的无障碍服务，以启用「双击锁屏」手势。请注意该服务仅用于这一项功能，我们的无障碍服务不会收集或分享任何数据。 | `res/values/strings.xml key=accessibility_disclosure（弹窗正文，SettingsFragment.onClick）` | 良性透明说明 |
| en | The accessibility permission is required to enable the gesture - double tap to lock . Any data acquired by Olauncher via this service will not leave your device. | 启用「双击锁屏」手势需要无障碍权限。Olauncher 通过该服务获取的任何数据都不会离开你的设备。 | `res/values/strings.xml key=accessibility_service_description（res/xml/accessibility_service_config.xml android:description）` | 隐私承诺 |
| en | Olauncher promises to use the accessibility permission responsibly. Olauncher does not collect or share any data. | Olauncher 承诺负责任地使用无障碍权限。Olauncher 不收集、不分享任何数据。 | `res/values/strings.xml key=admin_permission_message（设备管理员对话框）` | 隐私承诺 |
| en | Olauncher failed to lock device. Please check your app settings. | Olauncher 锁定设备失败，请检查应用设置。 | `res/values/strings.xml key=launcher_failed_to_lock_device` | 良性透明说明 |
| en | lock layout description to be used a unique id to lock screen | 用于锁屏的布局描述，作为唯一标识（服务据此识别本应用桌面空白区双击事件） | `res/values/strings.xml key=lock_layout_description（MyAccessibilityService.onAccessibilityEvent 比对 getContentDescription）` | 良性透明说明 |
| en | Double tap to lock | 双击锁屏 | `res/values/strings.xml key=double_tap_to_lock / double_tap_to_lock_screen` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环：弹窗与跳转均为一次性 onClick 触发；用户从系统设置返回后 LOCK_MODE 仍为 false，仅在再次双击桌面时以 toast 提示「锁定设备失败」，无 onResume 重跳、无 Timer 拉起、无后台重弹
- **遮罩叠层 / 高仿系统设置页**：无：overlay 线索为空，代码中无 TYPE_APPLICATION_OVERLAY / 全屏悬浮引导窗 / 高仿系统无障碍开关页，仅原生 MaterialAlertDialog + 系统无障碍页
- **Android 13+ 受限设置（Restricted Settings）应对**：无：全包无 ACTION_APPLICATION_DETAILS_SETTINGS、无「点右上角允许受限设置」文案、无 Session 安装器绕过；restricted 线索对应的是单次显式 ACTION_ACCESSIBILITY_SETTINGS 跳转与说明文案本身
- **获权后即时行为与防撤权机制**：无：onServiceConnected 仅写 SharedPreferences LOCK_MODE=true；onAccessibilityEvent 唯一动作是 performGlobalAction(8) GLOBAL_ACTION_LOCK_SCREEN，不使用 GLOBAL_ACTION_BACK/HOME 或自动点击阻止撤权
- **良性降级 / 替代方案**：具备：不开启无障碍则双击锁屏功能不可用，桌面其余功能完全正常；Android 9 以下改走设备管理员（DevicePolicyManager + DeviceAdmin receiver）实现锁屏，且用户可随时在设置中移除管理员（removeActiveAdmin 后 toast「Admin permission removed.」）

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：无需冷启动等待：以「监测到 app.olauncher 弹出原生 Dialog」与「监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS」双触发；实操路径为自动化进入 SettingsFragment 并点击「Double tap to lock」开关行，随后 UTG 抓取弹窗页与紧随的系统无障碍列表页
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在一处纯静态盲区但不影响判定：对话框正向按钮打开的外部 Notion 教程网页不在 APK 内，其内容需运行期抓取才能核对；此外应用未加壳未加密，运行期 UTG 完全可用

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **业务触发后的原生说明弹窗页** | SettingsFragment 内 MaterialAlertDialog：标题+accessibility_disclosure 正文+两个按钮，文本含「Please turn on Olauncher's accessibility service」 | 这是本应用唯一的无障碍引导载体，可直接读出其说明是否透明、是否提供取消、按钮文案指向教程还是直跳设置 | 弹窗正文原文与换行结构；两个按钮文案（教程/去开启）；是否 setCancelable(false)、返回键是否可关闭；弹窗背后页面是否为设置页而非桌面遮罩 |
| **跳转后的系统无障碍服务列表项** | com.android.settings 无障碍页中的「Olauncher」条目及其说明摘要 | 核对服务名与 android:description 是否与弹窗口径一致、是否存在伪造 isAccessibilityTool 或同形字/空白挤出 | 服务显示名 Olauncher；说明文本含 not leave your device 承诺；开关默认关闭状态；列表是否被本应用悬浮窗覆盖（此处应为否） |
| **获权返回后的桌面双击锁屏验证页** | app.olauncher.MainActivity 桌面空白区（FrameLayout，contentDescription=lock_layout_description） | 验证获权后行为是否仅限自身桌面双击锁屏，而非读取其他应用或阻止撤权 | 双击后屏幕立即锁定；无自动回到设置页/无障碍开关的跳转；无通知栏或悬浮窗二次引导 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `app.olauncher.ui.SettingsFragment.onClick（case 2131231233：f.j 构造引导 Dialog + S0.x(this,0)/(this,1)）`
- `app.olauncher.ui.SettingsFragment.onLongClick（case 2131231233：直接 startActivity ACTION_ACCESSIBILITY_SETTINGS）`
- `S0.x.a（case 0 打开 tanujnotes.notion.site 教程；default 先 Y() 再 SDK>=28 跳 ACCESSIBILITY_SETTINGS）`
- `app.olauncher.helper.MyAccessibilityService.onServiceConnected / onAccessibilityEvent`
- `res/xml/accessibility_service_config.xml（packageNames 自限、typeViewClicked、android:description）`
- `res/values/strings.xml（accessibility_disclosure / accessibility_service_description / admin_permission_message / lock_layout_description）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（纯运行期 UTG 视角）

**静态可见性**：完全可见。未发现加壳、AES 密文载荷、远端 HTML 或无源码混淆跳转；所有无障碍引导逻辑都在 DEX 与 `res/values/strings.xml` 内明文可读。

**引导链（无冷启动强制弹窗）**

1. **入口是业务开关，而非冷启动**：`SettingsFragment.onClick` 中 id `2131231233`（“Double tap to lock”开关）被点击；若 `LOCK_MODE` 为 false 且系统不支持/未启用，则弹出一个原生 `MaterialAlertDialog`（由 `f.j(...)` 构造），而不是直跳设置页。
2. **同一入口的长按是“直达设置”捷径**：[SettingsFragment.onLongClick](<resource-unit:#1.dex1 code:app.olauncher.ui.SettingsFragment#onLongClick>) 中 case `2131231233` 直接 `P(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`，无任何中间说明。
3. **弹窗提供“了解详情”与“去开启”两个分支**：[S0.x.a()](<resource-unit:#1.dex1 code:S0.x#a>) 的 `case 0` 用 `z0.E.T(...)` 打开外部浏览器教程页 `https://tanujnotes.notion.site/Double-tap-to-lock-Olauncher-...`；`default` 分支先 `SettingsFragment.Y()`（关闭/收尾），再 `if (SDK_INT >= 28) P(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`——即 **仅在 Android 9+ 跳系统无障碍列表**；低版本走 `DevicePolicyManager` 设备管理员（`app.olauncher.listener.DeviceAdmin` + `res/xml/policies`）老路径。
4. **无 `ACTION_APPLICATION_DETAILS_SETTINGS`、无“受限设置”教学、无 13+ 绕过**：全包搜索该 action 零命中；`restricted=['JUMP_A11Y_SETTINGS','RESTRICTED_STR']` 的实际实现就是上述单次显式跳转 + `android:description` 文案，不是受限设置分步教学。
5. **无遮罩/悬浮窗/高仿设置页**：overlay 线索为空，代码中无 `TYPE_APPLICATION_OVERLAY`、无伪造开关页；引导仅靠原生 Dialog + 系统无障碍页 + 外部教程网页（外部网页不在 APK 内）。
6. **无拒权循环**：`onResume` 未重新拉起弹窗/设置页；`LOCK_MODE` 只在服务真正连上时由 [onServiceConnected](<resource-unit:#1.dex1 code:app.olauncher.helper.MyAccessibilityService#onServiceConnected>) 置 true，失败则保留 false 并给 toast（`launcher_failed_to_lock_device`）。用户关弹窗即退回桌面，功能降级为不可用。
7. **获权后行为严格自限**：`accessibility_service_config.xml` 限定 `packageNames="app.olauncher.debug, app.olauncher"`、`accessibilityEventTypes="typeViewClicked"`、`canRetrieveWindowContent=true`；[onAccessibilityEvent](<resource-unit:#1.dex1 code:app.olauncher.helper.MyAccessibilityService#onAccessibilityEvent>) 仅在事件源为 `android.widget.FrameLayout` 且 `contentDescription` 等于 `lock_layout_description` 时执行 `performGlobalAction(8)`（GLOBAL_ACTION_LOCK_SCREEN）。**不是** `GLOBAL_ACTION_BACK/HOME` 撤权阻止型 anti-removal，`PERFORM_GLOBAL_ACTION` 线索属误报性质的中性能力。
8. **身份一致**：显示名 `Olauncher`、无障碍服务 label `Olauncher`、`android:description` 与 `accessibility_disclosure` 均如实说明用途并承诺不收集数据，无同形字/空白挤出/多 alias 伪装；`FakeHomeActivity` 虽存在但 `android:enabled="false"` 且属启动器隐藏应用特性，不是无障碍诱导载体。

```json
{
  "static_visibility": "clear",
  "visibility_note": "引导链全部静态可见：DEX 明文（SettingsFragment.onClick/onLongClick、S0.x.a）、res/xml/accessibility_service_config.xml、res/values/strings.xml 均可完整读取；无加壳、无 AES 密文、无远端 HTML 引导页（仅外部浏览器打开 Notion 教程，不在 APK 内）",
  "summary_one_liner": "开源极简启动器在设置页用户主动打开「Double tap to lock」开关时弹出原生说明对话框，一个按钮打开外部教程网页、另一个在 Android 9+ 跳转系统无障碍列表；无冷启动强制、无遮罩、无拒权循环，服务被 packageNames 与 typeViewClicked 严格自限且仅执行锁屏全局动作",
  "disguise_identity": {
    "app_display_name": "Olauncher",
    "claimed_brand_or_persona": "Olauncher（开源极简启动器，作者 tanujnotes，github.com/tanujnotes/Olauncher）",
    "a11y_service_label": "Olauncher",
    "identity_mismatch": false,
    "obfuscation_tricks": "无"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "app.olauncher.MainActivity（HOME/LAUNCHER，singleTask，无无障碍弹窗逻辑）",
      "trigger_event": "onCreate / 冷启动进入桌面",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "冷启动不出现任何无障碍提示，仅显示极简桌面与时钟",
      "user_action_requested": "无（不请求任何权限）",
      "code_anchor": "app.olauncher.MainActivity（Manifest intent-filter HOME/LAUNCHER）"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "app.olauncher.ui.SettingsFragment（设置页）中 id 2131231233 的「Double tap to lock」开关行",
      "trigger_event": "onClick：判断 Build.VERSION.SDK_INT >= 28 且 SharedPreferences LOCK_MODE==false",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Double tap to lock",
      "shown_text_zh": "设置项「双击锁屏」",
      "user_action_requested": "用户主动点击该开关（可随时返回，不点击则永不涉及无障碍）",
      "code_anchor": "app.olauncher.ui.SettingsFragment.onClick case 2131231233"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "MaterialAlertDialog（由 f.j(context, 2131820653, message, 2131820583, 2131820786, new S0.x(this,0), new S0.x(this,1), null, 64) 构建）",
      "trigger_event": "步骤 2 的点击回调内同步弹出",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Please turn on Olauncher's accessibility service in your device's settings to enable Double tap to lock gesture. Please note that this service is only used for this particular feature. Our accessibility service does not collect or share any data.",
      "shown_text_zh": "请在设备设置中开启 Olauncher 的无障碍服务以启用双击锁屏手势。请注意该服务仅用于此功能，我们的无障碍服务不会收集或分享任何数据。",
      "user_action_requested": "二选一按钮：正向按钮（S0.x case 0）打开外部教程网页；负向按钮（S0.x default）跳转系统无障碍设置；按返回或点弹窗外可取消，无强制不可取消标记",
      "code_anchor": "app.olauncher.ui.SettingsFragment.onClick / res/values/strings.xml accessibility_disclosure"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "外部浏览器：https://tanujnotes.notion.site/Double-tap-to-lock-Olauncher-0f7fb103ec1f47d7a90cdfdcd7fb86ef",
      "trigger_event": "点击对话框正向按钮 → S0.x.a() case 0 → z0.E.T(context, url)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "https://tanujnotes.notion.site/Double-tap-to-lock-Olauncher-0f7fb103ec1f47d7a90cdfdcd7fb86ef",
      "shown_text_zh": "跳转外部 Notion 页面查看「双击锁屏」使用说明（页面内容不在 APK 内，未纳入本次静态证据）",
      "user_action_requested": "用户自行阅读网页后返回",
      "code_anchor": "S0.x.a（case 0）"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表）",
      "trigger_event": "点击对话框负向按钮 → S0.x.a() default 分支：SettingsFragment.Y(); if (SDK_INT >= 28) P(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Olauncher — The accessibility permission is required to enable the gesture - double tap to lock . Any data acquired by Olauncher via this service will not leave your device.",
      "shown_text_zh": "系统无障碍列表中显示服务名「Olauncher」与说明「启用双击锁屏手势需要无障碍权限，Olauncher 通过该服务获取的任何数据都不会离开你的设备」",
      "user_action_requested": "用户在系统页手动打开 Olauncher 开关（也可直接返回，不视为拒绝反馈）",
      "code_anchor": "S0.x.a / res/xml/accessibility_service_config.xml android:description"
    },
    {
      "step": 6,
      "stage": "跳无障碍设置",
      "screen_or_component": "同上（长按捷径）",
      "trigger_event": "onLongClick case 2131231233 → P(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "长按该设置行直接跳系统无障碍设置，无二次确认、无任何拦截",
      "user_action_requested": "用户手动开启服务",
      "code_anchor": "app.olauncher.ui.SettingsFragment.onLongClick"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "app.olauncher.helper.MyAccessibilityService（android:process=:serviceProcess）",
      "trigger_event": "onServiceConnected：写入 SharedPreferences app.olauncher LOCK_MODE=true；onAccessibilityEvent：source 为 FrameLayout 且 contentDescription 等于 lock_layout_description 时 performGlobalAction(8)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "lock layout description to be used a unique id to lock screen",
      "shown_text_zh": "获权后仅在本应用桌面空白区（该唯一 contentDescription 的 FrameLayout）被双击时执行 GLOBAL_ACTION_LOCK_SCREEN 锁屏，不读取其他应用窗口内容、不阻止撤权",
      "user_action_requested": "无（无自点确认、无 GLOBAL_ACTION_BACK/HOME 反撤权、无通知栏重拉）",
      "code_anchor": "app.olauncher.helper.MyAccessibilityService.onServiceConnected / onAccessibilityEvent"
    },
    {
      "step": 8,
      "stage": "拒权反馈循环",
      "screen_or_component": "无（返回桌面即结束）",
      "trigger_event": "用户拒绝或从系统设置返回：LOCK_MODE 保持 false",
      "ui_carrier": "无",
      "shown_text_verbatim": "Olauncher failed to lock device. Please check your app settings.",
      "shown_text_zh": "仅在用户再次尝试双击锁屏时以 toast 提示「Olauncher 锁定设备失败，请检查应用设置」，无 onResume 死循环重跳、无定时器拉起",
      "user_action_requested": "用户可永久忽略该功能",
      "code_anchor": "res/values/strings.xml launcher_failed_to_lock_device"
    }
  ],
  "text_presentation_locations": [
    "设置页开关行文案：res/values/strings.xml double_tap_to_lock / double_tap_lock（「Double tap to lock」）",
    "引导对话框正文：res/values/strings.xml accessibility_disclosure（含换行分段），经 SettingsFragment.onClick 由 f.j(...) 传入 MaterialAlertDialog 展示",
    "系统无障碍列表服务名与说明：service android:label=\"@string/app_name\" 与 res/xml/accessibility_service_config.xml 的 android:description=@string/accessibility_service_description",
    "外部教程页：不在 APK 内，由 S0.x.a case 0 用系统浏览器打开 tanujnotes.notion.site 页面",
    "设备管理员相关说明：res/values/strings.xml admin_permission_message（Android 9 以下 DevicePolicyManager 路径的对话框）",
    "锁屏失败提示：res/values/strings.xml launcher_failed_to_lock_device，经 Toast（z0.E.l0/k0）展示"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Please turn on Olauncher's accessibility service in your device's settings to enable Double tap to lock gesture. Please note that this service is only used for this particular feature. Our accessibility service does not collect or share any data.",
      "text_zh": "请在设备设置中开启 Olauncher 的无障碍服务，以启用「双击锁屏」手势。请注意该服务仅用于这一项功能，我们的无障碍服务不会收集或分享任何数据。",
      "source_location": "res/values/strings.xml key=accessibility_disclosure（弹窗正文，SettingsFragment.onClick）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "The accessibility permission is required to enable the gesture - double tap to lock . Any data acquired by Olauncher via this service will not leave your device.",
      "text_zh": "启用「双击锁屏」手势需要无障碍权限。Olauncher 通过该服务获取的任何数据都不会离开你的设备。",
      "source_location": "res/values/strings.xml key=accessibility_service_description（res/xml/accessibility_service_config.xml android:description）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Olauncher promises to use the accessibility permission responsibly. Olauncher does not collect or share any data.",
      "text_zh": "Olauncher 承诺负责任地使用无障碍权限。Olauncher 不收集、不分享任何数据。",
      "source_location": "res/values/strings.xml key=admin_permission_message（设备管理员对话框）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Olauncher failed to lock device. Please check your app settings.",
      "text_zh": "Olauncher 锁定设备失败，请检查应用设置。",
      "source_location": "res/values/strings.xml key=launcher_failed_to_lock_device",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "lock layout description to be used a unique id to lock screen",
      "text_zh": "用于锁屏的布局描述，作为唯一标识（服务据此识别本应用桌面空白区双击事件）",
      "source_location": "res/values/strings.xml key=lock_layout_description（MyAccessibilityService.onAccessibilityEvent 比对 getContentDescription）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Double tap to lock",
      "text_zh": "双击锁屏",
      "source_location": "res/values/strings.xml key=double_tap_to_lock / double_tap_to_lock_screen",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环：弹窗与跳转均为一次性 onClick 触发；用户从系统设置返回后 LOCK_MODE 仍为 false，仅在再次双击桌面时以 toast 提示「锁定设备失败」，无 onResume 重跳、无 Timer 拉起、无后台重弹",
    "overlay_or_fake_settings": "无：overlay 线索为空，代码中无 TYPE_APPLICATION_OVERLAY / 全屏悬浮引导窗 / 高仿系统无障碍开关页，仅原生 MaterialAlertDialog + 系统无障碍页",
    "restricted_settings_13plus_coaching": "无：全包无 ACTION_APPLICATION_DETAILS_SETTINGS、无「点右上角允许受限设置」文案、无 Session 安装器绕过；restricted 线索对应的是单次显式 ACTION_ACCESSIBILITY_SETTINGS 跳转与说明文案本身",
    "post_grant_anti_removal": "无：onServiceConnected 仅写 SharedPreferences LOCK_MODE=true；onAccessibilityEvent 唯一动作是 performGlobalAction(8) GLOBAL_ACTION_LOCK_SCREEN，不使用 GLOBAL_ACTION_BACK/HOME 或自动点击阻止撤权",
    "benign_graceful_degradation": "具备：不开启无障碍则双击锁屏功能不可用，桌面其余功能完全正常；Android 9 以下改走设备管理员（DevicePolicyManager + DeviceAdmin receiver）实现锁屏，且用户可随时在设置中移除管理员（removeActiveAdmin 后 toast「Admin permission removed.」）"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "无需冷启动等待：以「监测到 app.olauncher 弹出原生 Dialog」与「监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS」双触发；实操路径为自动化进入 SettingsFragment 并点击「Double tap to lock」开关行，随后 UTG 抓取弹窗页与紧随的系统无障碍列表页",
    "key_pages_to_capture": [
      {
        "page_role": "业务触发后的原生说明弹窗页",
        "page_identifier": "SettingsFragment 内 MaterialAlertDialog：标题+accessibility_disclosure 正文+两个按钮，文本含「Please turn on Olauncher's accessibility service」",
        "why_most_useful": "这是本应用唯一的无障碍引导载体，可直接读出其说明是否透明、是否提供取消、按钮文案指向教程还是直跳设置",
        "observable_utg_signals": ["弹窗正文原文与换行结构", "两个按钮文案（教程/去开启）", "是否 setCancelable(false)、返回键是否可关闭", "弹窗背后页面是否为设置页而非桌面遮罩"]
      },
      {
        "page_role": "跳转后的系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍页中的「Olauncher」条目及其说明摘要",
        "why_most_useful": "核对服务名与 android:description 是否与弹窗口径一致、是否存在伪造 isAccessibilityTool 或同形字/空白挤出",
        "observable_utg_signals": ["服务显示名 Olauncher", "说明文本含 not leave your device 承诺", "开关默认关闭状态", "列表是否被本应用悬浮窗覆盖（此处应为否）"]
      },
      {
        "page_role": "获权返回后的桌面双击锁屏验证页",
        "page_identifier": "app.olauncher.MainActivity 桌面空白区（FrameLayout，contentDescription=lock_layout_description）",
        "why_most_useful": "验证获权后行为是否仅限自身桌面双击锁屏，而非读取其他应用或阻止撤权",
        "observable_utg_signals": ["双击后屏幕立即锁定", "无自动回到设置页/无障碍开关的跳转", "无通知栏或悬浮窗二次引导"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在一处纯静态盲区但不影响判定：对话框正向按钮打开的外部 Notion 教程网页不在 APK 内，其内容需运行期抓取才能核对；此外应用未加壳未加密，运行期 UTG 完全可用"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "app.olauncher.ui.SettingsFragment.onClick（case 2131231233：f.j 构造引导 Dialog + S0.x(this,0)/(this,1)）",
    "app.olauncher.ui.SettingsFragment.onLongClick（case 2131231233：直接 startActivity ACTION_ACCESSIBILITY_SETTINGS）",
    "S0.x.a（case 0 打开 tanujnotes.notion.site 教程；default 先 Y() 再 SDK>=28 跳 ACCESSIBILITY_SETTINGS）",
    "app.olauncher.helper.MyAccessibilityService.onServiceConnected / onAccessibilityEvent",
    "res/xml/accessibility_service_config.xml（packageNames 自限、typeViewClicked、android:description）",
    "res/values/strings.xml（accessibility_disclosure / accessibility_service_description / admin_permission_message / lock_layout_description）"
  ]
}
```

**边界与未决项**：外部 Notion 教程页内容未纳入静态证据（运行期需抓取）；本次未在真机执行，故未观测弹窗实际按钮文案与系统设置页渲染。结论基于包内完整可读的 DEX/XML/资源，未发现任何恶意诱导或规避审核的机制，也未登记风险。

</details>
