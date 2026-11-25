# MR_134__3317fae9ed｜Svpeng — Авито

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：139.1s

## 1. 一句话核心结论

- **核心申请方式**：无任何引导页面或教学图文，仅用一条冒充「Google Play」的俄语 10 秒 Toast 说明后直接跳转系统无障碍列表，并在 onActivityResult 检测未启用时无限重跳，形成不可取消的强制开启回路
- **静态可见性说明**：未加壳，DEX 完整可反编译；引导文案虽以 AES/CBC/NoPadding 密文硬编码，但密钥与 IV 均在包内且静态可解（已实测解出俄语明文），引导逻辑、跳转与回环判定全部静态可见，无远端 HTML/WebView 参与无障碍引导
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `3317fae9ed06922a5508689237f44fe3dfb56150b6f8c015fba5deb8525b5fab` |
| 包名 / 年份 | `com.nanohead.fort.last.world.war.bestActionGame` / 2019 |
| 家族 / 品类 | **Svpeng**（同池样本数：20） |
| 原始来源标识 | https://blog.zimperium.com/how-zimperiums-z9-detected-unknown-mobile-malware-overlooked-by-the-av-industry/ |
| 桌面显示名 | Авито |
| 引导页宣称品牌/身份 | Google Play（在 Toast 中要求用户到无障碍菜单里找到名为「Google Play」的项并开启，实为自身 com.dubocf.skyrusher.vbutkamd9xn 服务） |
| 系统无障碍列表服务名 | Google Play |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务显示名硬编码为 Google Play 以冒充官方商店；无障碍配置缺失 android:description，系统列表中不展示任何用途说明；accessibility-service 配置残留模板值 settingsActivity="com.example.root.myapplication.MainActivity"；类名/包名高度伪装（com.google.android.stardroid、com.ubisoft.adventure.valiant_hearts_trial、com.king.blossomblast、telugu.telugulatestnews、com.dubocf.skyrusher 等多套互不相关命名空间混杂，属多别名伪装）；全部关键字符串 AES 加密存储以规避字符串检索 |
| 无障碍服务类名 | `com.dubocf.skyrusher.vbutkamd9xn` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `READ_CONTACTS, READ_SMS, RECEIVE_SMS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.google.android.stardroid.gjd8e69n4vu（LAUNCHER，portrait，noHistory） | 用户点击桌面图标 → onCreate → zpvoertu → nnxlmaiv(Bundle) | 不可静态还原 | 无 | 无（静默执行，不呈现任何界面） | `com.google.android.stardroid.gjd8e69n4vu.nnxlmaiv` |
| 2 | 业务功能触发 | telugu.telugulatestnews.n30ud6p52j1（带 SEND/SENDTO intent-filter 的权限闸门 Activity，singleTop，portrait） | 由前述服务/广播链唤起（该 Activity 未注册 LAUNCHER）→ onCreate → wqoafgzl → n7jun4m9i5l.vgrdawlpjn() 判定无障碍未启用 | 原生Activity | 无 | 无（无取消/跳过按钮，无法停留在本页） | `telugu.telugulatestnews.n30ud6p52j1.wqoafgzl` |
| 3 | 引导说明页 | 原生 Toast（CountDownTimer 10000ms，每秒刷新） | sgcxlfnao() 被 onCreate/onActivityResult 调用后立即 show() | 悬浮窗Overlay | **原文**：Для работы приложения требуется включены: Google Play Найдите его в этом меню и включите!<br>**译注**：应用运行需要开启：Google Play。请在此菜单中找到它并开启！ | 要求用户记住并在随后的系统无障碍列表中手动开启名为「Google Play」的服务；无取消、无跳过、无说明为何需要无障碍权限 | `telugu.telugulatestnews.n30ud6p52j1.sgcxlfnao + com.dubocf.skyrusher.w2m0x1fbqg8.wagokyr（AES 解密）` |
| 4 | 跳无障碍设置 | 系统设置页 Settings.ACTION_ACCESSIBILITY_SETTINGS（android.settings.ACCESSIBILITY_SETTINGS） | Toast.show() 与计时器 start() 之后立即 startActivityForResult(intent, 125) | 系统无障碍页 | 无 | 在系统无障碍列表中点击「Google Play」开关（无应用侧引导遮罩、无高仿设置页） | `telugu.telugulatestnews.n30ud6p52j1.sgcxlfnao（requestCode qcpnxatw_ftdcixjn_xhnwnovi_potymkrw = 125）` |
| 5 | 拒权反馈循环 | n30ud6p52j1.onActivityResult → sgcxlfnao() 回环 | onActivityResult(requestCode==125)：若 n7jun4m9i5l.vgrdawlpjn(getApplicationContext()) 仍返回未启用 | 原生Dialog | **原文**：Для работы приложения требуется включены: Google Play Найдите его в этом меню и включите!<br>**译注**：同一 Toast 再次弹出并再次跳转系统无障碍页，用户返回/拒绝即被无限重跳，无任何降级或退出路径 | 只能开启无障碍服务；不提供取消、跳过或稍后再说 | `telugu.telugulatestnews.n30ud6p52j1.oqydnbrg` |
| 6 | 获权后动作 | wqoafgzl 后续校验分支 → tb4nw8xotkm 广播 → finish() | 无障碍已启用后，继续判定 n7jun4m9i5l.nqjfmbiz()（短信）、qoukyxsv()（设备管理员，bubbleshooter.orig.xnqmwkbg5jd）、ynwxmsjcq()（悬浮窗 SYSTEM_ALERT_WINDOW） | 原生Activity | 无 | 无（自动收敛，界面关闭） | `telugu.telugulatestnews.n30ud6p52j1.wqoafgzl / oqydnbrg` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 原生 Toast（悬浮提示，10 秒倒计时，非对话框）：telugu.telugulatestnews.n30ud6p52j1.sgcxlfnao 中由 hf6a9dgcu80.qvnfthwr 解密后拼接 getString(R.string.uwnfdpre) 生成
- res/values/strings.xml 的 uwnfdpre = 「Google Play」，作为 Toast 中间段嵌入并同时作为无障碍服务 android:label 显示在系统无障碍列表
- res/values/strings.xml 的 abojqmtg = 「Авито」，作为 application 与 LAUNCHER Activity 的桌面图标名称
- 系统无障碍服务列表项：由 res/xml/fahsjrog.xml 配置，无 android:description，列表中仅有名称「Google Play」而无任何用途说明
- 未发现任何 AlertDialog、自定义引导 Activity 布局、assets HTML、WebView 教学页或悬浮引导遮罩用于无障碍引导

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| ru | Для работы приложения требуется включены: | 应用运行需要开启： | `AES 密文硬编码于 telugu.telugulatestnews.n30ud6p52j1.sgcxlfnao 第一个参数（key=f3d5ba617e28d840cb42103a96c9fe75, iv=f3e68502a714bc9d），经 com.dubocf.skyrusher.w2m0x1fbqg8.wagokyr 解密` | 教唆忽视警告 |
| ru | Найдите его в этом меню и включите! | 请在此菜单中找到它并开启！ | `同一 Toast 第二段密文（key=ace5b2648fc036031b1e8a592d97fd47, iv=a6e912f3d5cb4870），telugu.telugulatestnews.n30ud6p52j1.sgcxlfnao` | 教唆忽视警告 |
| en | Google Play | 谷歌应用商店（被冒用的品牌名） | `res/values/strings.xml key=uwnfdpre（同时用于 Toast 拼接与 service android:label）` | 未知 |
| ru | Авито | Avito（俄罗斯分类信息平台品牌名） | `res/values/strings.xml key=abojqmtg（application/android:label 与 LAUNCHER Activity label）` | 未知 |
| en | first_start / gcm / init_bootable / yes | 首次启动 / GCM 推送 / 开机自启初始化 / 是 | `gjd8e69n4vu.nnxlmaiv 中 AES 解密得到的配置键值（SharedPreferences 写入）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：onActivityResult(requestCode=125) 中再次判定无障碍未启用则直接回调 sgcxlfnao()，重新弹 10 秒 Toast 并再次 startActivityForResult 跳 ACCESSIBILITY_SETTINGS；用户返回或拒绝即被无限重跳，直至服务被开启，无退出/降级路径
- **遮罩叠层 / 高仿系统设置页**：无半透明引导遮罩、无全屏悬浮窗、无高仿系统无障碍开关页；仅一条原生 Toast 作为唯一说明载体（SYSTEM_ALERT_WINDOW 权限与悬浮窗闸门 utpximfw 属后续独立权限步骤，未用于无障碍引导）
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=19，全 DEX 中无 ACTION_APPLICATION_DETAILS_SETTINGS、无 ACTION_USAGE_ACCESS、无 Android 13 受限设置教学文案）
- **获权后即时行为与防撤权机制**：未在无障碍链路中发现自点确认、GLOBAL_ACTION_BACK/HOME 阻止撤权的代码；但存在独立设备管理员闸门（receiver bubbleshooter.orig.xnqmwkbg5jd，BIND_DEVICE_ADMIN + onDisableRequested 解密提示文案），属另一条防卸载链路，本次未逐条取证
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以 startActivityForResult/startActivity 的 intent action 为触发器：监测到 android.settings.ACCESSIBILITY_SETTINGS（requestCode 125）立即抓取跳转前 1~2 帧；同时在冷启动后 5 秒内轮询顶层包名，捕获 Activity telugu.telugulatestnews.n30ud6p52j1 出现即抓屏；用户从设置页返回后 800ms 内再次抓屏以验证 Toast 重弹回环
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无图空文本或温和外壳式引导；主要盲区在于：一阶段为静默初始化 Activity（gjd8e69n4vu）无任何 UI，且所有引导文案经 AES 加密存储，纯静态关键词检索（如 accessibility、guide、enable）会漏掉；另无障碍服务本身无 description，仅凭系统列表难以判断用途，需结合服务类 com.dubocf.skyrusher.vbutkamd9xn 的行为做判定

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转前 Toast 引导层（本样本唯一文案载体）** | 系统 Toast 浮层，文本包含「Для работы приложения требуется включены: Google Play」 | 这是该样本全部诱导话语的唯一出口，能直接固定其冒充品牌与『应用必需』话术，且其存在时长 10 秒便于捕获 | Toast/浮层节点文本含 Google Play 与 Найдите его в этом меню；Toast 与应用界面同屏，且无任何按钮/取消控件；Toast 出现后顶层 Activity 立即切换为系统 Settings |
| **系统无障碍服务列表项（冒充品牌落地处）** | com.android.settings 无障碍页，列表项名称「Google Play」，无 description 摘要 | 区分用户看到的系统侧身份与应用真实包名/服务类是否一致，是判定品牌冒用与『无用途说明』违规的关键页 | 列表项文本为 Google Play 但其 settingsActivity 指向 com.example.root.myapplication.MainActivity；服务项无用途描述文本（android:description 缺失）；返回上一级后界面立即再次跳到本页（回环重跳） |
| **权限闸门 Activity（无文案但决定链路）** | telugu.telugulatestnews.n30ud6p52j1（包 com.nanohead.fort.last.world.war.bestActionGame），portrait、无可见控件 | 该 Activity 是四项权限闸门的调度点，捕获其出现即可确认恶意入口而非普通游戏界面 | 顶层 Activity 类名属于无关命名空间 telugu.telugulatestnews；界面无布局节点却频繁 startActivity 跳系统设置；onResume/onActivityResult 后重复跳转同一 intent |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `telugu.telugulatestnews.n30ud6p52j1.sgcxlfnao`
- `telugu.telugulatestnews.n30ud6p52j1.oqydnbrg`
- `telugu.telugulatestnews.n30ud6p52j1.wqoafgzl`
- `com.dubocf.skyrusher.w2m0x1fbqg8.wagokyr`
- `res/xml/fahsjrog.xml`
- `res/values/strings.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验）

**核心机制**：该样本的无障碍权限获取完全不依赖任何引导页面或教学 HTML；它采用**Toast 浮层口播 + 直接跳系统无障碍列表 + onActivityResult 回环重试**的最简恶意模式。

- **入口链**：桌面启动器 [gjd8e69n4vu.onCreate](<resource-unit:#1.dex1 code:com.google.android.stardroid.gjd8e69n4vu#onCreate>) → `zpvoertu` → [nnxlmaiv](<resource-unit:#1.dex1 code:com.google.android.stardroid.gjd8e69n4vu#nnxlmaiv>) 仅做 GCM 注册、拉起 `rj4z09dy6ob` 服务、写入 `first_start`/`gcm`/`init_bootable` 配置并向 [tb4nw8xotkm](<resource-unit:#1.dex1 code:com.king.blossomblast.tb4nw8xotkm>) 广播后 `finish()`，全程无 UI。
- **权限门页**：带 `SEND/SENDTO` intent-filter 的 [n30ud6p52j1](<resource-unit:#1.dex1 code:telugu.telugulatestnews.n30ud6p52j1>) 是被服务链唤起的“权限闸门”页，其 [wqoafgzl](<resource-unit:#1.dex1 code:telugu.telugulatestnews.n30ud6p52j1#wqoafgzl>)（onCreate）按顺序校验无障碍 → 短信 → 设备管理员 → 悬浮窗四项，首项不满足即调用 [sgcxlfnao](<resource-unit:#1.dex1 code:telugu.telugulatestnews.n30ud6p52j1#sgcxlfnao>)。
- **引导文案即一条 Toast（10 秒）**：文本由 AES/CBC/NoPadding 硬编码密文在运行时解密（[wagokyr](<resource-unit:#1.dex1 code:com.dubocf.skyrusher.w2m0x1fbqg8#wagokyr>)），实测明文为俄语：`Для работы приложения требуется включены: ` + **`Google Play`** + ` Найдите его в этом меню и включите!`（“应用运行需要开启：Google Play。请在此菜单中找到它并开启！”）。
- **跳转与拒权循环**：Toast 弹出后立即 `startActivityForResult(new Intent("android.settings.ACCESSIBILITY_SETTINGS"), 125)`；[oqydnbrg](<resource-unit:#1.dex1 code:telugu.telugulatestnews.n30ud6p52j1#oqydnbrg>)（onActivityResult）在 requestCode=125 且无障碍仍未启用时**再次调用 `sgcxlfnao()`**，形成 Toast→设置页→返回→再 Toast 的死循环，无取消/跳过/降级路径。
- **身份伪装**：桌面名 `Авито`（俄语分类信息品牌），无障碍列表显示名 `Google Play`（[strings.xml](<resource-unit:#1.dex1 file:res/values/strings.xml#L1-L6>) 中 `uwnfdpre`），服务真实类在 `com.dubocf.skyrusher` 包下，且 [fahsjrog.xml](<resource-unit:#1.dex1 file:res/xml/fahsjrog.xml#L1-L3>) 里 `settingsActivity="com.example.root.myapplication.MainActivity"` 是模板残留；**无 `android:description`**，用户无法在系统列表看到任何用途说明。
- **覆盖范围**：`ACTION_APPLICATION_DETAILS_SETTINGS` 与 `ACTION_USAGE_ACCESS` 在全 DEX 中**零命中**；targetSdk=19，不存在 Android 13+ 受限设置分步教学、也无 `isAccessibilityTool` 伪造字段。
- **静态可见性**：未加壳，AES 密文与密钥均在包内，可完整静态还原，`static_visibility=clear`。

> 说明：本次受 14 次调用硬约束，未对 `ivrualsmhn`/`cxudiqmf`/`utpximfw`（短信/设备管理员/悬浮窗闸门）逐条反编译，也未写入项目风险台账；上述三步仅按调用序位与权限常量确认存在，文案未取证。

```json
{
  "static_visibility": "clear",
  "visibility_note": "未加壳，DEX 完整可反编译；引导文案虽以 AES/CBC/NoPadding 密文硬编码，但密钥与 IV 均在包内且静态可解（已实测解出俄语明文），引导逻辑、跳转与回环判定全部静态可见，无远端 HTML/WebView 参与无障碍引导",
  "summary_one_liner": "无任何引导页面或教学图文，仅用一条冒充「Google Play」的俄语 10 秒 Toast 说明后直接跳转系统无障碍列表，并在 onActivityResult 检测未启用时无限重跳，形成不可取消的强制开启回路",
  "disguise_identity": {
    "app_display_name": "Авито",
    "claimed_brand_or_persona": "Google Play（在 Toast 中要求用户到无障碍菜单里找到名为「Google Play」的项并开启，实为自身 com.dubocf.skyrusher.vbutkamd9xn 服务）",
    "a11y_service_label": "Google Play",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务显示名硬编码为 Google Play 以冒充官方商店；无障碍配置缺失 android:description，系统列表中不展示任何用途说明；accessibility-service 配置残留模板值 settingsActivity=\"com.example.root.myapplication.MainActivity\"；类名/包名高度伪装（com.google.android.stardroid、com.ubisoft.adventure.valiant_hearts_trial、com.king.blossomblast、telugu.telugulatestnews、com.dubocf.skyrusher 等多套互不相关命名空间混杂，属多别名伪装）；全部关键字符串 AES 加密存储以规避字符串检索"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.google.android.stardroid.gjd8e69n4vu（LAUNCHER，portrait，noHistory）",
      "trigger_event": "用户点击桌面图标 → onCreate → zpvoertu → nnxlmaiv(Bundle)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面；仅做初始化：GCM 注册、startService(rj4z09dy6ob)、写入 first_start/gcm/init_bootable 配置、向 tb4nw8xotkm 广播后 finish()",
      "user_action_requested": "无（静默执行，不呈现任何界面）",
      "code_anchor": "com.google.android.stardroid.gjd8e69n4vu.nnxlmaiv"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "telugu.telugulatestnews.n30ud6p52j1（带 SEND/SENDTO intent-filter 的权限闸门 Activity，singleTop，portrait）",
      "trigger_event": "由前述服务/广播链唤起（该 Activity 未注册 LAUNCHER）→ onCreate → wqoafgzl → n7jun4m9i5l.vgrdawlpjn() 判定无障碍未启用",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "该页本身无布局文案，仅作为依次校验无障碍、短信、设备管理员、悬浮窗四项权限的闸门，首项失败即进入引导",
      "user_action_requested": "无（无取消/跳过按钮，无法停留在本页）",
      "code_anchor": "telugu.telugulatestnews.n30ud6p52j1.wqoafgzl"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "原生 Toast（CountDownTimer 10000ms，每秒刷新）",
      "trigger_event": "sgcxlfnao() 被 onCreate/onActivityResult 调用后立即 show()",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Для работы приложения требуется включены: Google Play Найдите его в этом меню и включите!",
      "shown_text_zh": "应用运行需要开启：Google Play。请在此菜单中找到它并开启！",
      "user_action_requested": "要求用户记住并在随后的系统无障碍列表中手动开启名为「Google Play」的服务；无取消、无跳过、无说明为何需要无障碍权限",
      "code_anchor": "telugu.telugulatestnews.n30ud6p52j1.sgcxlfnao + com.dubocf.skyrusher.w2m0x1fbqg8.wagokyr（AES 解密）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 Settings.ACTION_ACCESSIBILITY_SETTINGS（android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "Toast.show() 与计时器 start() 之后立即 startActivityForResult(intent, 125)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "直接打开系统无障碍服务列表，列表中显示服务名「Google Play」（无 android:description 说明），用户需自行找到并打开开关",
      "user_action_requested": "在系统无障碍列表中点击「Google Play」开关（无应用侧引导遮罩、无高仿设置页）",
      "code_anchor": "telugu.telugulatestnews.n30ud6p52j1.sgcxlfnao（requestCode qcpnxatw_ftdcixjn_xhnwnovi_potymkrw = 125）"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "n30ud6p52j1.onActivityResult → sgcxlfnao() 回环",
      "trigger_event": "onActivityResult(requestCode==125)：若 n7jun4m9i5l.vgrdawlpjn(getApplicationContext()) 仍返回未启用",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Для работы приложения требуется включены: Google Play Найдите его в этом меню и включите!",
      "shown_text_zh": "同一 Toast 再次弹出并再次跳转系统无障碍页，用户返回/拒绝即被无限重跳，无任何降级或退出路径",
      "user_action_requested": "只能开启无障碍服务；不提供取消、跳过或稍后再说",
      "code_anchor": "telugu.telugulatestnews.n30ud6p52j1.oqydnbrg"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "wqoafgzl 后续校验分支 → tb4nw8xotkm 广播 → finish()",
      "trigger_event": "无障碍已启用后，继续判定 n7jun4m9i5l.nqjfmbiz()（短信）、qoukyxsv()（设备管理员，bubbleshooter.orig.xnqmwkbg5jd）、ynwxmsjcq()（悬浮窗 SYSTEM_ALERT_WINDOW）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "四项均满足后发送 tvnzdei_zilojpu_xqcrywe_jzgcelq 动作广播并 finish()，转入后台服务（无障碍服务 com.dubocf.skyrusher.vbutkamd9xn 开始工作）",
      "user_action_requested": "无（自动收敛，界面关闭）",
      "code_anchor": "telugu.telugulatestnews.n30ud6p52j1.wqoafgzl / oqydnbrg"
    }
  ],
  "text_presentation_locations": [
    "原生 Toast（悬浮提示，10 秒倒计时，非对话框）：telugu.telugulatestnews.n30ud6p52j1.sgcxlfnao 中由 hf6a9dgcu80.qvnfthwr 解密后拼接 getString(R.string.uwnfdpre) 生成",
    "res/values/strings.xml 的 uwnfdpre = 「Google Play」，作为 Toast 中间段嵌入并同时作为无障碍服务 android:label 显示在系统无障碍列表",
    "res/values/strings.xml 的 abojqmtg = 「Авито」，作为 application 与 LAUNCHER Activity 的桌面图标名称",
    "系统无障碍服务列表项：由 res/xml/fahsjrog.xml 配置，无 android:description，列表中仅有名称「Google Play」而无任何用途说明",
    "未发现任何 AlertDialog、自定义引导 Activity 布局、assets HTML、WebView 教学页或悬浮引导遮罩用于无障碍引导"
  ],
  "verbatim_texts": [
    {
      "lang": "ru",
      "text_verbatim": "Для работы приложения требуется включены: ",
      "text_zh": "应用运行需要开启：",
      "source_location": "AES 密文硬编码于 telugu.telugulatestnews.n30ud6p52j1.sgcxlfnao 第一个参数（key=f3d5ba617e28d840cb42103a96c9fe75, iv=f3e68502a714bc9d），经 com.dubocf.skyrusher.w2m0x1fbqg8.wagokyr 解密",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "ru",
      "text_verbatim": "Найдите его в этом меню и включите!",
      "text_zh": "请在此菜单中找到它并开启！",
      "source_location": "同一 Toast 第二段密文（key=ace5b2648fc036031b1e8a592d97fd47, iv=a6e912f3d5cb4870），telugu.telugulatestnews.n30ud6p52j1.sgcxlfnao",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Google Play",
      "text_zh": "谷歌应用商店（被冒用的品牌名）",
      "source_location": "res/values/strings.xml key=uwnfdpre（同时用于 Toast 拼接与 service android:label）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "ru",
      "text_verbatim": "Авито",
      "text_zh": "Avito（俄罗斯分类信息平台品牌名）",
      "source_location": "res/values/strings.xml key=abojqmtg（application/android:label 与 LAUNCHER Activity label）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "first_start / gcm / init_bootable / yes",
      "text_zh": "首次启动 / GCM 推送 / 开机自启初始化 / 是",
      "source_location": "gjd8e69n4vu.nnxlmaiv 中 AES 解密得到的配置键值（SharedPreferences 写入）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "onActivityResult(requestCode=125) 中再次判定无障碍未启用则直接回调 sgcxlfnao()，重新弹 10 秒 Toast 并再次 startActivityForResult 跳 ACCESSIBILITY_SETTINGS；用户返回或拒绝即被无限重跳，直至服务被开启，无退出/降级路径",
    "overlay_or_fake_settings": "无半透明引导遮罩、无全屏悬浮窗、无高仿系统无障碍开关页；仅一条原生 Toast 作为唯一说明载体（SYSTEM_ALERT_WINDOW 权限与悬浮窗闸门 utpximfw 属后续独立权限步骤，未用于无障碍引导）",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=19，全 DEX 中无 ACTION_APPLICATION_DETAILS_SETTINGS、无 ACTION_USAGE_ACCESS、无 Android 13 受限设置教学文案）",
    "post_grant_anti_removal": "未在无障碍链路中发现自点确认、GLOBAL_ACTION_BACK/HOME 阻止撤权的代码；但存在独立设备管理员闸门（receiver bubbleshooter.orig.xnqmwkbg5jd，BIND_DEVICE_ADMIN + onDisableRequested 解密提示文案），属另一条防卸载链路，本次未逐条取证",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以 startActivityForResult/startActivity 的 intent action 为触发器：监测到 android.settings.ACCESSIBILITY_SETTINGS（requestCode 125）立即抓取跳转前 1~2 帧；同时在冷启动后 5 秒内轮询顶层包名，捕获 Activity telugu.telugulatestnews.n30ud6p52j1 出现即抓屏；用户从设置页返回后 800ms 内再次抓屏以验证 Toast 重弹回环",
    "key_pages_to_capture": [
      {
        "page_role": "跳转前 Toast 引导层（本样本唯一文案载体）",
        "page_identifier": "系统 Toast 浮层，文本包含「Для работы приложения требуется включены: Google Play」",
        "why_most_useful": "这是该样本全部诱导话语的唯一出口，能直接固定其冒充品牌与『应用必需』话术，且其存在时长 10 秒便于捕获",
        "observable_utg_signals": [
          "Toast/浮层节点文本含 Google Play 与 Найдите его в этом меню",
          "Toast 与应用界面同屏，且无任何按钮/取消控件",
          "Toast 出现后顶层 Activity 立即切换为系统 Settings"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项（冒充品牌落地处）",
        "page_identifier": "com.android.settings 无障碍页，列表项名称「Google Play」，无 description 摘要",
        "why_most_useful": "区分用户看到的系统侧身份与应用真实包名/服务类是否一致，是判定品牌冒用与『无用途说明』违规的关键页",
        "observable_utg_signals": [
          "列表项文本为 Google Play 但其 settingsActivity 指向 com.example.root.myapplication.MainActivity",
          "服务项无用途描述文本（android:description 缺失）",
          "返回上一级后界面立即再次跳到本页（回环重跳）"
        ]
      },
      {
        "page_role": "权限闸门 Activity（无文案但决定链路）",
        "page_identifier": "telugu.telugulatestnews.n30ud6p52j1（包 com.nanohead.fort.last.world.war.bestActionGame），portrait、无可见控件",
        "why_most_useful": "该 Activity 是四项权限闸门的调度点，捕获其出现即可确认恶意入口而非普通游戏界面",
        "observable_utg_signals": [
          "顶层 Activity 类名属于无关命名空间 telugu.telugulatestnews",
          "界面无布局节点却频繁 startActivity 跳系统设置",
          "onResume/onActivityResult 后重复跳转同一 intent"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无图空文本或温和外壳式引导；主要盲区在于：一阶段为静默初始化 Activity（gjd8e69n4vu）无任何 UI，且所有引导文案经 AES 加密存储，纯静态关键词检索（如 accessibility、guide、enable）会漏掉；另无障碍服务本身无 description，仅凭系统列表难以判断用途，需结合服务类 com.dubocf.skyrusher.vbutkamd9xn 的行为做判定"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE"
  ],
  "code_anchors": [
    "telugu.telugulatestnews.n30ud6p52j1.sgcxlfnao",
    "telugu.telugulatestnews.n30ud6p52j1.oqydnbrg",
    "telugu.telugulatestnews.n30ud6p52j1.wqoafgzl",
    "com.dubocf.skyrusher.w2m0x1fbqg8.wagokyr",
    "res/xml/fahsjrog.xml",
    "res/values/strings.xml"
  ]
}
```

</details>
