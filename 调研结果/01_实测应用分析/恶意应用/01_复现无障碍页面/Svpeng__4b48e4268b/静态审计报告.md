# MR_102__4b48e4268b｜Svpeng — Avito

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：125.2s

## 1. 一句话核心结论

- **核心申请方式**：无界面权限门 Activity 串行检查无障碍/默认短信/设备管理员/悬浮窗，用 10 秒俄语 Toast 指使用户在系统无障碍列表中开启名为 Google Play 的服务，拒权后在 onActivityResult 中无限重跳 ACCESSIBILITY_SETTINGS，获权后自动确认短信默认弹窗并压制卸载。
- **静态可见性说明**：全部引导逻辑位于 classes.dex，界面文案虽以 AES/CBC/NoPadding + Base64 加密（a8esndjoq1f.pighyescnl，密钥与 IV 硬编码在调用点），已全部静态解密还原；无加壳、无远端下发页面，无障碍配置 res/xml/yvpgfzoc.xml 与 strings.xml 明文可见。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `4b48e4268b0befdfa3ce11c258d2fdd54096256312b3e31cc217994c30b8d123` |
| 包名 / 年份 | `com.ufotosoft.justshot` / 2019 |
| 家族 / 品类 | **Svpeng**（同池样本数：20） |
| 原始来源标识 | https://blog.zimperium.com/how-zimperiums-z9-detected-unknown-mobile-malware-overlooked-by-the-av-industry/ |
| 桌面显示名 | Avito |
| 引导页宣称品牌/身份 | Google Play（无障碍服务名）/ Avito（俄罗斯分类信息平台） |
| 系统无障碍列表服务名 | Google Play |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务 label 直接冒用 Google Play 品牌；android:description 完全缺失，系统无障碍列表项无任何用途说明；accessibility-service 的 settingsActivity 指向不存在的 com.example.root.myapplication.MainActivity；包名/类名批量伪造为 com.gameloft.android.ANMP.GloftGHHM、com.gamtertainment.worldwar2.*、com.yodo1.rodeo.*、me.skyvpn.app.* 等游戏/VPN 名；LAUNCHER Activity 声明 noHistory+excludeFromRecents 且 onCreate 立即 finish()，后台不留可见界面 |
| 无障碍服务类名 | `com.gameloft.android.ANMP.GloftGHHM.jylwi0uxkv2` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `READ_CONTACTS, READ_SMS, RECEIVE_SMS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.gamedevltd.wwh.nhod56njsnr（LAUNCHER Activity，label=Avito） | 用户点击图标 → onCreate → ldzjtebp → nhmvzucs → cdsopihm | 原生Activity | 无 | 无（用户看不到任何页面，只有短暂白屏） | `com.gamedevltd.wwh.nhod56njsnr#cdsopihm` |
| 2 | 引导说明页（缺失） | com.gameloft.android.ANMP.GloftGHHM.ium5n2zk7lq（权限门 Activity，无布局） | 后台服务 com.gamedevltd.wwh.nnrd5z7uvsy 拉起后执行 onCreate → ynarezuo() | 原生Activity | 无 | 无（未提供任何解释、确认或取消入口） | `com.gameloft.android.ANMP.GloftGHHM.ium5n2zk7lq#ynarezuo` |
| 3 | 跳无障碍设置 | Toast（10 秒 CountDownTimer）+ 系统设置 android.settings.ACCESSIBILITY_SETTINGS | ynarezuo() 中 kasq124ewxp.bjkmurhnpz() 判定无障碍未开启 → rimceqsyxl() | 系统无障碍页 | **原文**：Для работы приложения требуется включить: Google Play найдите его в этом меню и включите!<br>**译注**：为了应用正常工作需要开启：Google Play，请在此菜单中找到并启用它！ | 在系统无障碍列表中找到并打开名为 Google Play 的服务（Toast 无取消/跳过按钮，直接 startActivityForResult 跳转） | `com.gameloft.android.ANMP.GloftGHHM.ium5n2zk7lq#rimceqsyxl` |
| 4 | 遮罩叠层指引 | 系统无障碍设置页上的 Toast 叠层（CountDownTimer 每秒刷新，持续 10 秒） | Toast 显示后 toastCountDown.start() 与 startActivityForResult 同步执行，Toast 覆盖在设置页上 | 悬浮窗Overlay | **原文**：Для работы приложения требуется включить: Google Play найдите его в этом меню и включите!<br>**译注**：同一句俄语提示在系统设置页上方持续 10 秒滚动提示，指导用户定位服务项 | 按提示在列表中开启服务（无高仿开关页，仅文字叠层指路） | `com.gameloft.android.ANMP.GloftGHHM.ium5n2zk7lq$1（CountDownTimer）` |
| 5 | 拒权反馈循环 | onActivityResult(requestCode=125) → rimceqsyxl() 递归重跳 | 用户按返回键离开系统无障碍页或未开启服务 → onActivityResult 回调 → kasq124ewxp.bjkmurhnpz() 仍 false | 系统无障碍页 | **原文**：Для работы приложения требуется включить: Google Play найдите его в этом меню и включите!<br>**译注**：再次弹出同一 Toast 并再次强制跳转无障碍设置，形成无退出路径的循环 | 只能开启服务，否则被反复拉回系统设置（无跳过、无降级） | `com.gameloft.android.ANMP.GloftGHHM.ium5n2zk7lq#pursxeok` |
| 6 | 跳受限设置 | android.provider.Telephony.ACTION_CHANGE_DEFAULT（默认短信应用）/ android.app.action.ADD_DEVICE_ADMIN / 悬浮窗授权 | 无障碍已开启后 ynarezuo() 继续顺序检查 iajbhln/snyvwjhp/banthvynp，逐项跳转 | 系统无障碍页 | **原文**：Приложение проверено и является полностью безопасным! Выполнить запуск?<br>**译注**：应用已验证，完全安全！是否执行启动？（设备管理员授权说明文案） | 把本应用设为默认短信应用、激活设备管理员、授予悬浮窗权限 | `com.gameloft.android.ANMP.GloftGHHM.ium5n2zk7lq#dpnklyrzuj / #gjckwblz` |
| 7 | 获权后动作 | com.gameloft.android.ANMP.GloftGHHM.jylwi0uxkv2（无障碍服务）onServiceConnected / onAccessibilityEvent | 服务被系统连接 → sendBroadcast 通知宿主；后续 wclfnseq 处理 TYPE_WINDOW_STATE_CHANGED(32) | 不可静态还原 | 无 | 无（用户无感知，自动确认短信默认弹窗、压制卸载与设置页操作） | `com.gameloft.android.ANMP.GloftGHHM.jylwi0uxkv2#onServiceConnected / #wclfnseq` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍设置页上方的 Toast 叠层（10 秒、每秒刷新）：俄语“Для работы приложения требуется включить: Google Play найдите его в этом меню и включите!”
- 系统无障碍服务列表项名称：strings.xml 中 @string/olmcksnq = "Google Play"（res/xml/yvpgfzoc.xml 未声明 android:description，列表项无任何用途说明）
- 设备管理员激活页的说明文案：AES 解密串“Приложение проверено и является полностью безопасным! Выполнить запуск?”
- 桌面图标名称：@string/lsrdbycq = "Avito"（同时用于 LAUNCHER Activity 与 application label）
- 不存在任何 Activity 布局/WebView/HTML 承载说明文字（res/layout 下 4 个布局均未用于该引导链，无 assets HTML）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| ru | Для работы приложения требуется включить: | 为了应用正常工作需要开启： | `com.gameloft.android.ANMP.GloftGHHM.ium5n2zk7lq#rimceqsyxl（AES/CBC 解密串 2d3313d1…47aff）` | 教唆忽视警告 |
| ru | найдите его в этом меню и включите! | 请在此菜单中找到并启用它！ | `com.gameloft.android.ANMP.GloftGHHM.ium5n2zk7lq#rimceqsyxl（AES/CBC 解密串 42cdd471…da8f）` | 受限设置分步教学 |
| ru | Приложение проверено и является полностью безопасным! Выполнить запуск? | 应用已验证，完全安全！是否执行启动？ | `com.gameloft.android.ANMP.GloftGHHM.ium5n2zk7lq#gjckwblz（ADD_EXPLANATION，AES/CBC 解密串 a7ae5841…0820）` | 隐私承诺 |
| en | Google Play | Google Play（无障碍服务在系统列表中的显示名） | `res/values/strings.xml key olmcksnq` | 未知 |
| en | Avito | Avito（应用桌面显示名） | `res/values/strings.xml key lsrdbycq` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：onActivityResult(requestCode=125) 中若 kasq124ewxp.bjkmurhnpz() 仍判定无障碍未开启，立即再次调用 rimceqsyxl()，重新弹 10 秒 Toast 并再次 startActivityForResult(ACCESSIBILITY_SETTINGS)，用户按返回键离开设置页即被反复拉回，直到开启服务为止
- **遮罩叠层 / 高仿系统设置页**：无高仿无障碍开关页；仅在系统设置页之上叠加 10 秒 Toast 文字（CountDownTimer 每秒刷新）做定位指引
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=19，未涉及 Android 13 受限设置教学，也未使用 Session 安装器绕过）
- **获权后即时行为与防撤权机制**：无障碍服务 onServiceConnected 立即广播；wclfnseq 监听 com.android.packageinstaller.UninstallerActivity 与 com.android.settings/com.android.phone 窗口，自动点击 android:id/button1、button2、com.android.packageinstaller:id/cancel_button 取消卸载与拦截设置页；同时申请设备管理员（ADD_DEVICE_ADMIN）增加移除难度
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在 com.gameloft.android.ANMP.GloftGHHM.ium5n2zk7lq#rimceqsyxl 执行瞬间（冷启动后数秒内首次 startActivityForResult 携带 action=android.settings.ACCESSIBILITY_SETTINGS 时）拉起 UTG，此时 Toast 正在展示、系统无障碍页刚压栈，可同时捕获引导文字与目标服务项
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：引导文案全部为文本（Toast + 系统列表项 + 设备管理员说明），无需 OCR；唯一盲区是 LAUNCHER Activity 立即 finish() 且 excludeFromRecents，冷启动瞬间几乎无可截页面，UTG 需以“监测到跳转 ACCESSIBILITY_SETTINGS/Toast 文本”为触发条件而非等待应用自身界面；此外权限门 Activity 由后台服务 com.gamedevtld.wwh.nnrd5z7uvsy 拉起，若服务因条件不满足未启动，则冷启动不会出现引导，需要以重启/多轮冷启动复现。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后系统无障碍设置页（含 10 秒 Toast 叠层）** | Settings/无障碍设置 Activity（com.android.settings 无障碍列表）+ 顶层 Toast 文本节点 | 这是唯一承载诱导文案的界面，Toast 原文直接证明“为了应用正常工作需要开启”的话术与目标服务名 | Toast 文本“Для работы приложения требуется включить: Google Play найдите его в этом меню и включите!”；当前 package 已切至 com.android.settings 而前台应用为 com.ufotosoft.justshot；无障碍列表中 label 为 Google Play 的条目且无 summary/description 文本 |
| **系统无障碍服务列表项（Google Play）** | list item 文本 'Google Play' + 开关控件，无描述行 | 证明服务名冒用 Google Play 品牌、description 为空，用户无法从列表判断真实用途 | 节点 text='Google Play' 且 contentDescription 为空；同一列表项关联 package com.ufotosoft.justshot |
| **拒权返回后的循环重跳页** | 连续两次 ACCESSIBILITY_SETTINGS 压栈（间隔 <5s） | 证明无取消路径的强制循环，是区分恶意诱导与良性引导的决定性行为 | 同一秒级窗口内 ACCESSIBILITY_SETTINGS 反复出现在前台；返回键后 Toast 再次出现；无任何应用内说明页被展示 |
| **设备管理员激活页与默认短信选择页** | com.android.settings 设备管理员激活 Dialog（含 ADD_EXPLANATION 文案）/ SmsDefaultDialog | 证明无障碍获权后继续索要设备管理员与默认短信，属同一提权链 | 说明文本含“полностью безопасным”；包名 com.ufotosoft.justshot 出现在默认短信候选；随后无障碍服务自动点击 button1/cancel_button 的窗口变化 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.gameloft.android.ANMP.GloftGHHM.ium5n2zk7lq#rimceqsyxl`
- `com.gameloft.android.ANMP.GloftGHHM.ium5n2zk7lq#ynarezuo`
- `com.gameloft.android.ANMP.GloftGHHM.ium5n2zk7lq#pursxeok`
- `com.gameloft.android.ANMP.GloftGHHM.jylwi0uxkv2#wclfnseq`
- `res/xml/yvpgfzoc.xml`
- `res/values/strings.xml#olmcksnq`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（运行期引导链）

**核心机制：无任何 UI 的“权限门”Activity + 10 秒俄语 Toast + 反复跳转系统无障碍设置**

1. **启动链**：`com.gamedevltd.wwh.nhod56njsnr`（桌面名 `Avito`）为 LAUNCHER，`onCreate` 内立即 `finish()`，只做初始化（写 `first_start`/`api_url`/`gcm` 配置）并 `startService(nnrd5z7uvsy)`，**不留任何界面**。
2. **权限门**：`com.gameloft.android.ANMP.GloftGHHM.ium5n2zk7lq` 的 `ynarezuo()`（onCreate 实现）按固定顺序串行检查：**无障碍 → 默认短信应用 → 设备管理员 → 悬浮窗**，任一未开启就跳对应系统页，全部满足才 `finish()`。全程**无说明页、无确认弹窗、无取消按钮**。
3. **无障碍引导**：`rimceqsyxl()` 先弹 `Toast`（CountDownTimer 每 1 秒刷新、共 10 秒），文案由 AES/CBC 解密拼接：`"Для работы приложения требуется включить: " + getString(olmcksnq) + " найдите его в этом меню и включите!"`，即"为了应用正常工作需要开启：**Google Play**，请在此菜单中找到并启用它！"，紧接着 `startActivityForResult(Intent("android.settings.ACCESSIBILITY_SETTINGS"), 125)`。
4. **拒权循环**：`onActivityResult(125)` 中若 `kasq124ewxp.bjkmurhnpz()` 仍为未开启，则**再次调用 `rimceqsyxl()`**（Toast+重跳），形成无限重跳闭环。
5. **获权后动作**：继续 `ACTION_CHANGE_DEFAULT`（把自身设为默认短信）与 `ADD_DEVICE_ADMIN`（说明文案"应用已验证、完全安全！执行启动？"），再申请悬浮窗；无障碍服务 `onServiceConnected` 发广播；`jylwi0uxkv2#wclfnseq` 监听 `com.android.settings`/`com.android.phone`/`packageinstaller` 的 `UninstallerActivity`、`SmsDefaultDialog` 并点击 `button1/button2/cancel_button`，即**自动确认短信默认弹窗、压制卸载确认**（反移除）。
6. **身份伪装**：应用名 `Avito`、无障碍服务名 `Google Play`（`@string/olmcksnq`）、无 `android:description`（系统列表无任何说明），包/类名伪造成 gameloft、gamtertainment、yodo1 等游戏；`accessibility-service` 的 `settingsActivity` 指向不存在的 `com.example.root.myapplication.MainActivity`。
7. **静态可见性**：字符串为 AES/CBC + Base64 加密（`a8esndjoq1f.pighyescnl`），但密钥/IV 硬编码在调用点，已全部解出，**逻辑完整静态可见，无加壳、无远端 HTML**。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部引导逻辑位于 classes.dex，界面文案虽以 AES/CBC/NoPadding + Base64 加密（a8esndjoq1f.pighyescnl，密钥与 IV 硬编码在调用点），已全部静态解密还原；无加壳、无远端下发页面，无障碍配置 res/xml/yvpgfzoc.xml 与 strings.xml 明文可见。",
  "summary_one_liner": "无界面权限门 Activity 串行检查无障碍/默认短信/设备管理员/悬浮窗，用 10 秒俄语 Toast 指使用户在系统无障碍列表中开启名为 Google Play 的服务，拒权后在 onActivityResult 中无限重跳 ACCESSIBILITY_SETTINGS，获权后自动确认短信默认弹窗并压制卸载。",
  "disguise_identity": {
    "app_display_name": "Avito",
    "claimed_brand_or_persona": "Google Play（无障碍服务名）/ Avito（俄罗斯分类信息平台）",
    "a11y_service_label": "Google Play",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务 label 直接冒用 Google Play 品牌；android:description 完全缺失，系统无障碍列表项无任何用途说明；accessibility-service 的 settingsActivity 指向不存在的 com.example.root.myapplication.MainActivity；包名/类名批量伪造为 com.gameloft.android.ANMP.GloftGHHM、com.gamtertainment.worldwar2.*、com.yodo1.rodeo.*、me.skyvpn.app.* 等游戏/VPN 名；LAUNCHER Activity 声明 noHistory+excludeFromRecents 且 onCreate 立即 finish()，后台不留可见界面"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.gamedevltd.wwh.nhod56njsnr（LAUNCHER Activity，label=Avito）",
      "trigger_event": "用户点击图标 → onCreate → ldzjtebp → nhmvzucs → cdsopihm",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面，初始化后立即 finish()",
      "user_action_requested": "无（用户看不到任何页面，只有短暂白屏）",
      "code_anchor": "com.gamedevltd.wwh.nhod56njsnr#cdsopihm"
    },
    {
      "step": 2,
      "stage": "引导说明页（缺失）",
      "screen_or_component": "com.gameloft.android.ANMP.GloftGHHM.ium5n2zk7lq（权限门 Activity，无布局）",
      "trigger_event": "后台服务 com.gamedevltd.wwh.nnrd5z7uvsy 拉起后执行 onCreate → ynarezuo()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无任何说明页/弹窗，直接进入系统设置跳转",
      "user_action_requested": "无（未提供任何解释、确认或取消入口）",
      "code_anchor": "com.gameloft.android.ANMP.GloftGHHM.ium5n2zk7lq#ynarezuo"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "Toast（10 秒 CountDownTimer）+ 系统设置 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "ynarezuo() 中 kasq124ewxp.bjkmurhnpz() 判定无障碍未开启 → rimceqsyxl()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Для работы приложения требуется включить: Google Play найдите его в этом меню и включите!",
      "shown_text_zh": "为了应用正常工作需要开启：Google Play，请在此菜单中找到并启用它！",
      "user_action_requested": "在系统无障碍列表中找到并打开名为 Google Play 的服务（Toast 无取消/跳过按钮，直接 startActivityForResult 跳转）",
      "code_anchor": "com.gameloft.android.ANMP.GloftGHHM.ium5n2zk7lq#rimceqsyxl"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "系统无障碍设置页上的 Toast 叠层（CountDownTimer 每秒刷新，持续 10 秒）",
      "trigger_event": "Toast 显示后 toastCountDown.start() 与 startActivityForResult 同步执行，Toast 覆盖在设置页上",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Для работы приложения требуется включить: Google Play найдите его в этом меню и включите!",
      "shown_text_zh": "同一句俄语提示在系统设置页上方持续 10 秒滚动提示，指导用户定位服务项",
      "user_action_requested": "按提示在列表中开启服务（无高仿开关页，仅文字叠层指路）",
      "code_anchor": "com.gameloft.android.ANMP.GloftGHHM.ium5n2zk7lq$1（CountDownTimer）"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "onActivityResult(requestCode=125) → rimceqsyxl() 递归重跳",
      "trigger_event": "用户按返回键离开系统无障碍页或未开启服务 → onActivityResult 回调 → kasq124ewxp.bjkmurhnpz() 仍 false",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Для работы приложения требуется включить: Google Play найдите его в этом меню и включите!",
      "shown_text_zh": "再次弹出同一 Toast 并再次强制跳转无障碍设置，形成无退出路径的循环",
      "user_action_requested": "只能开启服务，否则被反复拉回系统设置（无跳过、无降级）",
      "code_anchor": "com.gameloft.android.ANMP.GloftGHHM.ium5n2zk7lq#pursxeok"
    },
    {
      "step": 6,
      "stage": "跳受限设置",
      "screen_or_component": "android.provider.Telephony.ACTION_CHANGE_DEFAULT（默认短信应用）/ android.app.action.ADD_DEVICE_ADMIN / 悬浮窗授权",
      "trigger_event": "无障碍已开启后 ynarezuo() 继续顺序检查 iajbhln/snyvwjhp/banthvynp，逐项跳转",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Приложение проверено и является полностью безопасным! Выполнить запуск?",
      "shown_text_zh": "应用已验证，完全安全！是否执行启动？（设备管理员授权说明文案）",
      "user_action_requested": "把本应用设为默认短信应用、激活设备管理员、授予悬浮窗权限",
      "code_anchor": "com.gameloft.android.ANMP.GloftGHHM.ium5n2zk7lq#dpnklyrzuj / #gjckwblz"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "com.gameloft.android.ANMP.GloftGHHM.jylwi0uxkv2（无障碍服务）onServiceConnected / onAccessibilityEvent",
      "trigger_event": "服务被系统连接 → sendBroadcast 通知宿主；后续 wclfnseq 处理 TYPE_WINDOW_STATE_CHANGED(32)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面；监听 com.android.settings / com.android.phone / com.android.packageinstaller.UninstallerActivity / com.android.settings.SmsDefaultDialog，自动点击 android:id/button1、button2、cancel_button",
      "user_action_requested": "无（用户无感知，自动确认短信默认弹窗、压制卸载与设置页操作）",
      "code_anchor": "com.gameloft.android.ANMP.GloftGHHM.jylwi0uxkv2#onServiceConnected / #wclfnseq"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍设置页上方的 Toast 叠层（10 秒、每秒刷新）：俄语“Для работы приложения требуется включить: Google Play найдите его в этом меню и включите!”",
    "系统无障碍服务列表项名称：strings.xml 中 @string/olmcksnq = \"Google Play\"（res/xml/yvpgfzoc.xml 未声明 android:description，列表项无任何用途说明）",
    "设备管理员激活页的说明文案：AES 解密串“Приложение проверено и является полностью безопасным! Выполнить запуск?”",
    "桌面图标名称：@string/lsrdbycq = \"Avito\"（同时用于 LAUNCHER Activity 与 application label）",
    "不存在任何 Activity 布局/WebView/HTML 承载说明文字（res/layout 下 4 个布局均未用于该引导链，无 assets HTML）"
  ],
  "verbatim_texts": [
    {
      "lang": "ru",
      "text_verbatim": "Для работы приложения требуется включить: ",
      "text_zh": "为了应用正常工作需要开启：",
      "source_location": "com.gameloft.android.ANMP.GloftGHHM.ium5n2zk7lq#rimceqsyxl（AES/CBC 解密串 2d3313d1…47aff）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "ru",
      "text_verbatim": " найдите его в этом меню и включите!",
      "text_zh": "请在此菜单中找到并启用它！",
      "source_location": "com.gameloft.android.ANMP.GloftGHHM.ium5n2zk7lq#rimceqsyxl（AES/CBC 解密串 42cdd471…da8f）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "ru",
      "text_verbatim": "Приложение проверено и является полностью безопасным! Выполнить запуск?",
      "text_zh": "应用已验证，完全安全！是否执行启动？",
      "source_location": "com.gameloft.android.ANMP.GloftGHHM.ium5n2zk7lq#gjckwblz（ADD_EXPLANATION，AES/CBC 解密串 a7ae5841…0820）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Google Play",
      "text_zh": "Google Play（无障碍服务在系统列表中的显示名）",
      "source_location": "res/values/strings.xml key olmcksnq",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Avito",
      "text_zh": "Avito（应用桌面显示名）",
      "source_location": "res/values/strings.xml key lsrdbycq",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "onActivityResult(requestCode=125) 中若 kasq124ewxp.bjkmurhnpz() 仍判定无障碍未开启，立即再次调用 rimceqsyxl()，重新弹 10 秒 Toast 并再次 startActivityForResult(ACCESSIBILITY_SETTINGS)，用户按返回键离开设置页即被反复拉回，直到开启服务为止",
    "overlay_or_fake_settings": "无高仿无障碍开关页；仅在系统设置页之上叠加 10 秒 Toast 文字（CountDownTimer 每秒刷新）做定位指引",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=19，未涉及 Android 13 受限设置教学，也未使用 Session 安装器绕过）",
    "post_grant_anti_removal": "无障碍服务 onServiceConnected 立即广播；wclfnseq 监听 com.android.packageinstaller.UninstallerActivity 与 com.android.settings/com.android.phone 窗口，自动点击 android:id/button1、button2、com.android.packageinstaller:id/cancel_button 取消卸载与拦截设置页；同时申请设备管理员（ADD_DEVICE_ADMIN）增加移除难度",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在 com.gameloft.android.ANMP.GloftGHHM.ium5n2zk7lq#rimceqsyxl 执行瞬间（冷启动后数秒内首次 startActivityForResult 携带 action=android.settings.ACCESSIBILITY_SETTINGS 时）拉起 UTG，此时 Toast 正在展示、系统无障碍页刚压栈，可同时捕获引导文字与目标服务项",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后系统无障碍设置页（含 10 秒 Toast 叠层）",
        "page_identifier": "Settings/无障碍设置 Activity（com.android.settings 无障碍列表）+ 顶层 Toast 文本节点",
        "why_most_useful": "这是唯一承载诱导文案的界面，Toast 原文直接证明“为了应用正常工作需要开启”的话术与目标服务名",
        "observable_utg_signals": ["Toast 文本“Для работы приложения требуется включить: Google Play найдите его в этом меню и включите!”", "当前 package 已切至 com.android.settings 而前台应用为 com.ufotosoft.justshot", "无障碍列表中 label 为 Google Play 的条目且无 summary/description 文本"]
      },
      {
        "page_role": "系统无障碍服务列表项（Google Play）",
        "page_identifier": "list item 文本 'Google Play' + 开关控件，无描述行",
        "why_most_useful": "证明服务名冒用 Google Play 品牌、description 为空，用户无法从列表判断真实用途",
        "observable_utg_signals": ["节点 text='Google Play' 且 contentDescription 为空", "同一列表项关联 package com.ufotosoft.justshot"]
      },
      {
        "page_role": "拒权返回后的循环重跳页",
        "page_identifier": "连续两次 ACCESSIBILITY_SETTINGS 压栈（间隔 <5s）",
        "why_most_useful": "证明无取消路径的强制循环，是区分恶意诱导与良性引导的决定性行为",
        "observable_utg_signals": ["同一秒级窗口内 ACCESSIBILITY_SETTINGS 反复出现在前台", "返回键后 Toast 再次出现", "无任何应用内说明页被展示"]
      },
      {
        "page_role": "设备管理员激活页与默认短信选择页",
        "page_identifier": "com.android.settings 设备管理员激活 Dialog（含 ADD_EXPLANATION 文案）/ SmsDefaultDialog",
        "why_most_useful": "证明无障碍获权后继续索要设备管理员与默认短信，属同一提权链",
        "observable_utg_signals": ["说明文本含“полностью безопасным”", "包名 com.ufotosoft.justshot 出现在默认短信候选", "随后无障碍服务自动点击 button1/cancel_button 的窗口变化"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "引导文案全部为文本（Toast + 系统列表项 + 设备管理员说明），无需 OCR；唯一盲区是 LAUNCHER Activity 立即 finish() 且 excludeFromRecents，冷启动瞬间几乎无可截页面，UTG 需以“监测到跳转 ACCESSIBILITY_SETTINGS/Toast 文本”为触发条件而非等待应用自身界面；此外权限门 Activity 由后台服务 com.gamedevtld.wwh.nnrd5z7uvsy 拉起，若服务因条件不满足未启动，则冷启动不会出现引导，需要以重启/多轮冷启动复现。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE"
  ],
  "code_anchors": [
    "com.gameloft.android.ANMP.GloftGHHM.ium5n2zk7lq#rimceqsyxl",
    "com.gameloft.android.ANMP.GloftGHHM.ium5n2zk7lq#ynarezuo",
    "com.gameloft.android.ANMP.GloftGHHM.ium5n2zk7lq#pursxeok",
    "com.gameloft.android.ANMP.GloftGHHM.jylwi0uxkv2#wclfnseq",
    "res/xml/yvpgfzoc.xml",
    "res/values/strings.xml#olmcksnq"
  ]
}
```

</details>
