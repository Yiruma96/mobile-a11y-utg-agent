# MR_113__9ecd82dd6b｜Ztorg — EmailService

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：194.0s

## 1. 一句话核心结论

- **核心申请方式**：以“Privacy protection/EmailService”伪装，冷启动无 UI 首页直接 finish 并静默初始化远端插件，再由插件反射触发跳转系统无障碍设置并叠加整屏半透明“保护隐私”说明遮罩，诱导用户为可读取全部窗口内容的高危无障碍服务授权。
- **静态可见性说明**：宿主壳代码（Activity/Service 包装、无障碍检测与 ACCESSIBILITY_SETTINGS 跳转函数、全屏半透明说明页、strings/xml 资源）完整静态可见；但跳转函数 aa.b 无任何静态调用者，实际引导时机、多步教学页内容与获权后动作由 DexClassLoader 从私有目录 dexout 加载的插件 DEX 承担，插件经反射接收 AccessibilityEvent，其字节码未在包内静态呈现（是否加密需进一步核实），故多步流程细节与远端 HTML 教学页不可静态还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `9ecd82dd6b67d60bd9bce8ef32759a456faeb88586f46cbaabbbac7353df105a` |
| 包名 / 年份 | `com.server.full.upon` / 2017 |
| 家族 / 品类 | **Ztorg**（同池样本数：5） |
| 原始来源标识 | https://securelist.com/ztorg-money-for-infecting-your-smartphone/78325/ |
| 桌面显示名 | EmailService |
| 引导页宣称品牌/身份 | Privacy protection（隐私保护功能，声称防止信息泄露/被盗/被他人窥探） |
| 系统无障碍列表服务名 | Privacy protection |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：应用名“EmailService”与无障碍服务名“Privacy protection”互相矛盾，均非真实功能；图标使用系统默认 @android:drawable/sym_def_app_icon 冒充系统组件；三个 Activity（UponActivity、NssaActivity、LineUponActivity）全部声明 MAIN/DEFAULT 多入口且 excludeFromRecents=true，启动后立即 finish，用户无从查看正在运行的应用身份；类名 LineUpon/Upon 与字符串混淆（a/aa/ab/k/l/z）掩盖真实意图；无障碍说明仅承诺隐私保护，未披露可读取窗口内容(typeAllMask/canRetrieveWindowContent)的实际能力。 |
| 无障碍服务类名 | `com.server.full.upon.view.LineUponAccessService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, PACKAGE_USAGE_STATS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Please open the privacy protection function, protect your information not to be leaked, not to be stolen, to prevent others from spying on your privacy. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.server.full.upon.UponActivity / com.server.full.upon.NssaActivity（均 MAIN+DEFAULT，excludeFromRecents） | onCreate | 原生Activity | 无 | 无（用户点击图标后应用自行关闭） | `com.server.full.upon.UponActivity#onCreate；com.server.full.upon.NssaActivity#onCreate` |
| 2 | 业务功能触发 | com.server.full.upon.view.aa.a() + com.server.full.upon.view.ab（后台线程） | aa.a() 中 Settings.System "newuser"==0 判定 | 不可静态还原 | 无 | 无 | `com.server.full.upon.view.aa#a；com.server.full.upon.view.ab#run` |
| 3 | 业务功能触发 | com.server.full.upon.view.k（DexClassLoader 加载 dexout 插件并反射调 init） | aa.a() 末尾 k.a(ctx).a()；LineUponCoreService Handler case 0 亦重复触发 | 不可静态还原 | 无 | 无 | `com.server.full.upon.view.k#a；com.server.full.upon.view.l#handleMessage` |
| 4 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表） | 插件反射调用 com.server.full.upon.view.aa.b(Context)（该方法全包无静态调用者） | 系统无障碍页 | **原文**：无（跳转由宿主代码发起，页面为系统原生列表，其中可见服务项 “Privacy protection”）<br>**译注**：直接拉起系统无障碍服务列表页，用户需在该列表中找到并点开“Privacy protection” | 在系统无障碍列表中选择并开启“Privacy protection”服务；页面无应用自绘的取消/跳过入口 | `com.server.full.upon.view.aa#b` |
| 5 | 遮罩叠层指引 | com.server.full.upon.view.UponGuideActivity（Theme.Translucent.NoTitleBar.Fullscreen，竖屏） | aa.b() 在 startActivity(ACCESSIBILITY_SETTINGS) 之后紧接着 startActivity(UponGuideActivity) | 原生Activity | **原文**：Please open the privacy protection function, protect your information not to be leaked, not to be stolen, to prevent others from spying on your privacy.<br>**译注**：请开启隐私保护功能，保护您的信息不被泄露、不被盗取，防止他人窥探您的隐私。 | 全屏半透明文字页压在系统无障碍列表之上，无取消/跳过/稍后按钮，唯一交互为点击任意处（setOnClickListener→finish()）退出并回到系统无障碍页 | `com.server.full.upon.view.UponGuideActivity#onCreate；com.server.full.upon.view.z#onClick；res/values/strings.xml#acc_tips` |
| 6 | 拒权反馈循环 | com.server.full.upon.view.aa.a(Context) 权限状态检测 + 插件（不可静态还原） | 每次冷启动 UponActivity/NssaActivity onCreate→aa.a()，以及 LineUponCoreService Handler case 0 再次调用 aa.a() | 不可静态还原 | 无 | 不可静态确认（存在反复拉起设置的机制入口，但重跳节奏与次数在插件内） | `com.server.full.upon.view.aa#a；com.server.full.upon.view.l#handleMessage` |
| 7 | 获权后动作 | com.server.full.upon.view.LineUponAccessService（无障碍服务，:daemon 同进程组）/ com.server.full.upon.view.LineUponActivity（Translucent 插件 UI 宿主） | onAccessibilityEvent / onInterrupt / onServiceConnected；LineUponActivity.onCreate 反射调用插件 setActivity+onCreate | 不可静态还原 | 无 | 无（静默） | `com.server.full.upon.view.LineUponAccessService#onAccessibilityEvent；com.server.full.upon.view.LineUponActivity#onCreate` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：服务 android:label=@string/acc_title 显示为 “Privacy protection”，详情页说明为 @string/acc_desc（res/values/strings.xml、res/xml/email_config.xml）
- 跳转设置后叠加的整屏半透明 Activity：UponGuideActivity 动态构建的全屏 TextView（背景 0x80000000、白字居中、无标题栏、竖屏、Translucent.Fullscreen），文本取自 strings.xml 的 acc_tips
- 桌面/应用列表：应用名 EmailService（@string/app_name）+ 系统默认图标 sym_def_app_icon
- 引导文案未出现在任何布局 XML 中（无 res/layout 目录），全部由代码动态创建或取自 strings 资源；未见 WebView/HTML 资源

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Privacy protection | 隐私保护 | `res/values/strings.xml#acc_title（AndroidManifest 中 service android:label）` | 假反诈安全 |
| en | Please open the privacy protection function, protect your information not to be leaked, not to be stolen, to prevent others from spying on your privacy. | 请开启隐私保护功能，保护您的信息不被泄露、不被盗取，防止他人窥探您的隐私。 | `res/values/strings.xml#acc_desc（无障碍服务 android:description）` | 隐私承诺 |
| en | Please open the privacy protection function, protect your information not to be leaked, not to be stolen, to prevent others from spying on your privacy. | 请开启隐私保护功能，保护您的信息不被泄露、不被盗取，防止他人窥探您的隐私。 | `res/values/strings.xml#acc_tips（UponGuideActivity.onCreate 通过 y.f(this,"acc_tips") 读取并显示）` | 受限设置分步教学 |
| en | EmailService | 邮件服务（桌面显示名） | `res/values/strings.xml#app_name（AndroidManifest application android:label）` | 假更新 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：宿主未提供取消/跳过；每次冷启动（UponActivity/NssaActivity onCreate→aa.a()）以及 LineUponCoreService Handler case 0 都会重新进入插件初始化流程，并在 aa.a(Context) 检测到未启用时具备再次跳转的能力；实际是否循环重跳（如 onResume 死循环、定时器拉起）由插件 DEX 决定，静态不可确认。
- **遮罩叠层 / 高仿系统设置页**：有叠层但非悬浮窗：UponGuideActivity 为 Translucent.NoTitleBar.Fullscreen 的原生 Activity，全屏半透明背景 + 居中白字，在 ACCESSIBILITY_SETTINGS 之后启动，视觉上整屏覆盖系统无障碍列表；未见伪造的系统开关控件，也未见 SYSTEM_ALERT_WINDOW 悬浮引导窗（权限已申请但静态未见使用）。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=21，无 ACTION_APPLICATION_DETAILS_SETTINGS 跳转、无“允许受限设置”教学、无 Session 安装器痕迹；但清单声明 WRITE_SECURE_SETTINGS 与 MTK 相关权限，存在尝试自行写入安全设置绕过用户确认的可能，代码层未证实）
- **获权后即时行为与防撤权机制**：宿主代码中未见自点确认、GLOBAL_ACTION_BACK/HOME 阻止撤权等实现；但 LineUponAccessService 将全部事件反射交给插件，且 :daemon 常驻服务 + BOOT_COMPLETED/USER_PRESENT/PACKAGE_ADDED 监听可被用于快速恢复，具体撤权对抗逻辑不可静态确认。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以 Intent action == android.settings.ACCESSIBILITY_SETTINGS 的 startActivity 为锚点拉起 UTG，并持续录制其后 1.5–3 秒（宿主会在同一 try 块内紧接着 startActivity(UponGuideActivity)，遮罩页是判别关键）；同时在 com.server.full.upon.UponActivity / NssaActivity 的 onCreate 后立即开始录制，捕捉“无界面秒退”现象。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：显著盲区：真实引导流程的调度与后续动作由 DexClassLoader 从私有目录 dexout 加载的插件 DEX 执行（宿主仅提供 aa.b 跳转与遮罩页），插件是否二次跳转、是否伪造设置页、是否循环重跳无法静态确认；引导文案可能由插件运行时改写，UTG 捕获的文本需与静态 acc_tips 比对以判断是否被替换。应用未加壳，运行期 UTG 不受加壳阻挡。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动秒退页（应用无 UI 直通后台）** | com.server.full.upon.UponActivity / NssaActivity，启动后 <1s 自动消失，无可见控件 | 证明其不存在任何正当业务界面，冷启动唯一目的就是初始化插件与引导，排除“用户主动使用某功能才触发”的良性解释 | Activity 停留时长与 finish 时序；无任何可交互节点（空视图树）；随后出现的系统无障碍列表页 |
| **设置页后叠加的整屏半透明说明遮罩页** | com.server.full.upon.view.UponGuideActivity，全屏半透明背景 + 居中白字，无可点击按钮 | 这是诱导链的核心证据：文案以“隐私保护”为名，实际覆盖在系统无障碍列表之上，且无取消/跳过，直接推动用户去开启高危服务 | 页面文本与 acc_tips 完全一致；无 cancel/skip/later 文本节点；页面为应用包名而非 com.android.settings；页面背景半透明可见下层系统设置 |
| **系统无障碍服务列表项** | com.android.settings 无障碍列表中的 “Privacy protection” 条目及详情页说明文本 | 确认系统侧呈现给用户的唯一身份是“Privacy protection”，与桌面名 EmailService 不一致，坐实身份混淆 | 服务标签 Privacy protection；描述文本 = acc_desc；开关点击前的弹窗/授权流程 |
| **获权后静默回跳/二次引导页** | 授权返回后重新出现的 UponGuideActivity 或 LineUponActivity（Translucent 插件宿主） | 用于判断是否存在拒权/撤权后的重跳循环与插件是否在获权后接管界面 | 返回键后是否再次弹出同一遮罩页；LineUponActivity 透明宿主上的插件自绘控件；进程 :daemon 是否常驻 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.server.full.upon.view.aa#b`
- `com.server.full.upon.view.aa#a`
- `com.server.full.upon.view.UponGuideActivity#onCreate`
- `com.server.full.upon.UponActivity#onCreate`
- `com.server.full.upon.view.k#a`
- `res/values/strings.xml（acc_title / acc_desc / acc_tips）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点（基于 16 次工具核实，超出预算后立即收口）

**可静态确认的主干：** 该应用自身代码中确实有一条完整的“冷启动即引导 → 跳系统无障碍设置 → 叠半透明全屏说明页”链路，但**跳转函数没有静态调用者**，真正的多步教学 UI 与跳转时机位于 `DexClassLoader` 加载的插件 DEX 中。

1. **冷启动无界面直通引导**：[UponActivity.onCreate()](<resource-unit:#1.dex1 code:com.server.full.upon.UponActivity#onCreate>) 与 [NssaActivity.onCreate()](<resource-unit:#1.dex1 code:com.server.full.upon.NssaActivity#onCreate>) 均无 UI，直接 `new aa(this).a()`，随后 `onResume()` 立即 `finish()`（`excludeFromRecents=true`），用户看不到任何可操作的首页。
2. **`aa.a()` 只做“新用户上报 + 插件初始化”**：[aa#a](<resource-unit:#1.dex1 code:com.server.full.upon.view.aa#a>) 先写 `com.server.full.upon.a.a.a(1)`，再以 `Settings.System "newuser"` 做一次性闸门，`c()` 起线程 [ab#run](<resource-unit:#1.dex1 code:com.server.full.upon.view.ab#run>) 将设备信息 JSON（`"isnew":"true"`）POST 到远端，响应含 `"ok"` 后置 `newuser=100`；最后 `k.a(ctx).a()` 用 `DexClassLoader` 加载插件类并反射调其 `init(Context)`。
3. **无障碍跳转点确为原生 Intent，但由插件触发**：[aa#b](<resource-unit:#1.dex1 code:com.server.full.upon.view.aa#b>) 先用 [aa#a(Context)](<resource-unit:#1.dex1 code:com.server.full.upon.view.aa#a>) 读 `Settings.Secure accessibility_enabled` / `enabled_accessibility_services` 判断 `包名/LineUponAccessService` 是否已启用，未启用则**连续两次 `startActivity`**：先 `new Intent("android.settings.ACCESSIBILITY_SETTINGS")`，紧接着 `UponGuideActivity`。该方法是 `public static` 且**全包无静态调用者**，只能由 `dexout` 插件 DEX 反射调用 —— 即“何时弹引导”由云端下发的插件决定。
4. **遮罩叠层指引载体是本地原生半透明 Activity，不是悬浮窗**：[UponGuideActivity.onCreate()](<resource-unit:#1.dex1 code:com.server.full.upon.view.UponGuideActivity#onCreate>) 用代码动态建 `TextView`，`setBackgroundColor(Integer.MIN_VALUE)`（0x80000000 半透明）、全屏、白字居中，文本取 `acc_tips`，`setOnClickListener(new z(this))` 仅 `finish()`。因为它紧跟在系统无障碍页之后启动且 Translucent+Fullscreen，实际效果是**盖在系统无障碍列表上的整屏引导文案**，无“取消/跳过/稍后”按钮，只能点一下退出。
5. **系统列表身份为“隐私保护”**：`res/xml/email_config.xml` 引用 `@string/acc_desc`，服务 `android:label="@string/acc_title"`=`Privacy protection`，描述以“防止他人窥探你的隐私”为名索取 `canRetrieveWindowContent=true` + `typeAllMask` + `flagReportViewIds`（可读全部窗口内容与控件 ID），与其实际用途严重不符；应用图标直接用 `@android:drawable/sym_def_app_icon`，显示名 `EmailService`。
6. **获权后不自主退出**：[LineUponAccessService#onAccessibilityEvent](<resource-unit:#1.dex1 code:com.server.full.upon.view.LineUponAccessService#onAccessibilityEvent>) 仅把事件反射转交给插件对象，真实动作（点击、跳转、读取界面）全在插件内；`LineUponCoreService`（`:daemon` 进程）的 Handler 在 `case 0` 中还会再 `new aa(ctx).a()` 重新拉一轮引导。
7. **Android 13 受限设置教学：未发现**。`targetSdkVersion=21`，无 `APPLICATION_DETAILS_SETTINGS` 跳转、无 Session 安装器痕迹；但清单声明了 `WRITE_SECURE_SETTINGS`（配合 MTK/root 权限自开无障碍的典型手法），代码层未见对应实现，属未闭合项。
8. **可见性边界**：`LineUponActivity`（Translucent，作为插件 UI 宿主，`onCreate` 反射调插件 `setActivity/onCreate`）与 `k#a()` 的 `dexout` 目录说明二阶段载荷在运行期落盘/加载；引导文案的多步细节（如是否循环重跳、是否伪造系统页）不在静态可见范围内。

---

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "宿主壳代码（Activity/Service 包装、无障碍检测与 ACCESSIBILITY_SETTINGS 跳转函数、全屏半透明说明页、strings/xml 资源）完整静态可见；但跳转函数 aa.b 无任何静态调用者，实际引导时机、多步教学页内容与获权后动作由 DexClassLoader 从私有目录 dexout 加载的插件 DEX 承担，插件经反射接收 AccessibilityEvent，其字节码未在包内静态呈现（是否加密需进一步核实），故多步流程细节与远端 HTML 教学页不可静态还原。",
  "summary_one_liner": "以“Privacy protection/EmailService”伪装，冷启动无 UI 首页直接 finish 并静默初始化远端插件，再由插件反射触发跳转系统无障碍设置并叠加整屏半透明“保护隐私”说明遮罩，诱导用户为可读取全部窗口内容的高危无障碍服务授权。",
  "disguise_identity": {
    "app_display_name": "EmailService",
    "claimed_brand_or_persona": "Privacy protection（隐私保护功能，声称防止信息泄露/被盗/被他人窥探）",
    "a11y_service_label": "Privacy protection",
    "identity_mismatch": true,
    "obfuscation_tricks": "应用名“EmailService”与无障碍服务名“Privacy protection”互相矛盾，均非真实功能；图标使用系统默认 @android:drawable/sym_def_app_icon 冒充系统组件；三个 Activity（UponActivity、NssaActivity、LineUponActivity）全部声明 MAIN/DEFAULT 多入口且 excludeFromRecents=true，启动后立即 finish，用户无从查看正在运行的应用身份；类名 LineUpon/Upon 与字符串混淆（a/aa/ab/k/l/z）掩盖真实意图；无障碍说明仅承诺隐私保护，未披露可读取窗口内容(typeAllMask/canRetrieveWindowContent)的实际能力。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.server.full.upon.UponActivity / com.server.full.upon.NssaActivity（均 MAIN+DEFAULT，excludeFromRecents）",
      "trigger_event": "onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面，创建后立即调用 aa.a() 初始化，onResume 中 finish() 退出，用户看不到首页",
      "user_action_requested": "无（用户点击图标后应用自行关闭）",
      "code_anchor": "com.server.full.upon.UponActivity#onCreate；com.server.full.upon.NssaActivity#onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.server.full.upon.view.aa.a() + com.server.full.upon.view.ab（后台线程）",
      "trigger_event": "aa.a() 中 Settings.System \"newuser\"==0 判定",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无 UI；后台将设备信息 JSON（isnew=true）上报远端，返回含 ok 后写 newuser=100，完成一次性“新用户”标记",
      "user_action_requested": "无",
      "code_anchor": "com.server.full.upon.view.aa#a；com.server.full.upon.view.ab#run"
    },
    {
      "step": 3,
      "stage": "业务功能触发",
      "screen_or_component": "com.server.full.upon.view.k（DexClassLoader 加载 dexout 插件并反射调 init）",
      "trigger_event": "aa.a() 末尾 k.a(ctx).a()；LineUponCoreService Handler case 0 亦重复触发",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无 UI；从私有目录 dexout 加载插件 DEX，反射实例化插件类并调用其 init(Context)，后续引导与跳转由插件决定",
      "user_action_requested": "无",
      "code_anchor": "com.server.full.upon.view.k#a；com.server.full.upon.view.l#handleMessage"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表）",
      "trigger_event": "插件反射调用 com.server.full.upon.view.aa.b(Context)（该方法全包无静态调用者）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（跳转由宿主代码发起，页面为系统原生列表，其中可见服务项 “Privacy protection”）",
      "shown_text_zh": "直接拉起系统无障碍服务列表页，用户需在该列表中找到并点开“Privacy protection”",
      "user_action_requested": "在系统无障碍列表中选择并开启“Privacy protection”服务；页面无应用自绘的取消/跳过入口",
      "code_anchor": "com.server.full.upon.view.aa#b"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.server.full.upon.view.UponGuideActivity（Theme.Translucent.NoTitleBar.Fullscreen，竖屏）",
      "trigger_event": "aa.b() 在 startActivity(ACCESSIBILITY_SETTINGS) 之后紧接着 startActivity(UponGuideActivity)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Please open the privacy protection function, protect your information not to be leaked, not to be stolen, to prevent others from spying on your privacy.",
      "shown_text_zh": "请开启隐私保护功能，保护您的信息不被泄露、不被盗取，防止他人窥探您的隐私。",
      "user_action_requested": "全屏半透明文字页压在系统无障碍列表之上，无取消/跳过/稍后按钮，唯一交互为点击任意处（setOnClickListener→finish()）退出并回到系统无障碍页",
      "code_anchor": "com.server.full.upon.view.UponGuideActivity#onCreate；com.server.full.upon.view.z#onClick；res/values/strings.xml#acc_tips"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "com.server.full.upon.view.aa.a(Context) 权限状态检测 + 插件（不可静态还原）",
      "trigger_event": "每次冷启动 UponActivity/NssaActivity onCreate→aa.a()，以及 LineUponCoreService Handler case 0 再次调用 aa.a()",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "宿主仅通过 Settings.Secure 的 accessibility_enabled 与 enabled_accessibility_services 判断是否已启用；未启用时重新进入插件流程，是否再次拉起设置页由插件决定，静态不可确认",
      "user_action_requested": "不可静态确认（存在反复拉起设置的机制入口，但重跳节奏与次数在插件内）",
      "code_anchor": "com.server.full.upon.view.aa#a；com.server.full.upon.view.l#handleMessage"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "com.server.full.upon.view.LineUponAccessService（无障碍服务，:daemon 同进程组）/ com.server.full.upon.view.LineUponActivity（Translucent 插件 UI 宿主）",
      "trigger_event": "onAccessibilityEvent / onInterrupt / onServiceConnected；LineUponActivity.onCreate 反射调用插件 setActivity+onCreate",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后服务将全部无障碍事件反射转交插件对象处理，宿主自身无可见 UI；真实界面读取、点击与跳转行为在插件 DEX 内",
      "user_action_requested": "无（静默）",
      "code_anchor": "com.server.full.upon.view.LineUponAccessService#onAccessibilityEvent；com.server.full.upon.view.LineUponActivity#onCreate"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：服务 android:label=@string/acc_title 显示为 “Privacy protection”，详情页说明为 @string/acc_desc（res/values/strings.xml、res/xml/email_config.xml）",
    "跳转设置后叠加的整屏半透明 Activity：UponGuideActivity 动态构建的全屏 TextView（背景 0x80000000、白字居中、无标题栏、竖屏、Translucent.Fullscreen），文本取自 strings.xml 的 acc_tips",
    "桌面/应用列表：应用名 EmailService（@string/app_name）+ 系统默认图标 sym_def_app_icon",
    "引导文案未出现在任何布局 XML 中（无 res/layout 目录），全部由代码动态创建或取自 strings 资源；未见 WebView/HTML 资源"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Privacy protection",
      "text_zh": "隐私保护",
      "source_location": "res/values/strings.xml#acc_title（AndroidManifest 中 service android:label）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Please open the privacy protection function, protect your information not to be leaked, not to be stolen, to prevent others from spying on your privacy.",
      "text_zh": "请开启隐私保护功能，保护您的信息不被泄露、不被盗取，防止他人窥探您的隐私。",
      "source_location": "res/values/strings.xml#acc_desc（无障碍服务 android:description）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Please open the privacy protection function, protect your information not to be leaked, not to be stolen, to prevent others from spying on your privacy.",
      "text_zh": "请开启隐私保护功能，保护您的信息不被泄露、不被盗取，防止他人窥探您的隐私。",
      "source_location": "res/values/strings.xml#acc_tips（UponGuideActivity.onCreate 通过 y.f(this,\"acc_tips\") 读取并显示）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "EmailService",
      "text_zh": "邮件服务（桌面显示名）",
      "source_location": "res/values/strings.xml#app_name（AndroidManifest application android:label）",
      "rhetorical_frame": "假更新"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "宿主未提供取消/跳过；每次冷启动（UponActivity/NssaActivity onCreate→aa.a()）以及 LineUponCoreService Handler case 0 都会重新进入插件初始化流程，并在 aa.a(Context) 检测到未启用时具备再次跳转的能力；实际是否循环重跳（如 onResume 死循环、定时器拉起）由插件 DEX 决定，静态不可确认。",
    "overlay_or_fake_settings": "有叠层但非悬浮窗：UponGuideActivity 为 Translucent.NoTitleBar.Fullscreen 的原生 Activity，全屏半透明背景 + 居中白字，在 ACCESSIBILITY_SETTINGS 之后启动，视觉上整屏覆盖系统无障碍列表；未见伪造的系统开关控件，也未见 SYSTEM_ALERT_WINDOW 悬浮引导窗（权限已申请但静态未见使用）。",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=21，无 ACTION_APPLICATION_DETAILS_SETTINGS 跳转、无“允许受限设置”教学、无 Session 安装器痕迹；但清单声明 WRITE_SECURE_SETTINGS 与 MTK 相关权限，存在尝试自行写入安全设置绕过用户确认的可能，代码层未证实）",
    "post_grant_anti_removal": "宿主代码中未见自点确认、GLOBAL_ACTION_BACK/HOME 阻止撤权等实现；但 LineUponAccessService 将全部事件反射交给插件，且 :daemon 常驻服务 + BOOT_COMPLETED/USER_PRESENT/PACKAGE_ADDED 监听可被用于快速恢复，具体撤权对抗逻辑不可静态确认。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以 Intent action == android.settings.ACCESSIBILITY_SETTINGS 的 startActivity 为锚点拉起 UTG，并持续录制其后 1.5–3 秒（宿主会在同一 try 块内紧接着 startActivity(UponGuideActivity)，遮罩页是判别关键）；同时在 com.server.full.upon.UponActivity / NssaActivity 的 onCreate 后立即开始录制，捕捉“无界面秒退”现象。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动秒退页（应用无 UI 直通后台）",
        "page_identifier": "com.server.full.upon.UponActivity / NssaActivity，启动后 <1s 自动消失，无可见控件",
        "why_most_useful": "证明其不存在任何正当业务界面，冷启动唯一目的就是初始化插件与引导，排除“用户主动使用某功能才触发”的良性解释",
        "observable_utg_signals": ["Activity 停留时长与 finish 时序", "无任何可交互节点（空视图树）", "随后出现的系统无障碍列表页"]
      },
      {
        "page_role": "设置页后叠加的整屏半透明说明遮罩页",
        "page_identifier": "com.server.full.upon.view.UponGuideActivity，全屏半透明背景 + 居中白字，无可点击按钮",
        "why_most_useful": "这是诱导链的核心证据：文案以“隐私保护”为名，实际覆盖在系统无障碍列表之上，且无取消/跳过，直接推动用户去开启高危服务",
        "observable_utg_signals": ["页面文本与 acc_tips 完全一致", "无 cancel/skip/later 文本节点", "页面为应用包名而非 com.android.settings", "页面背景半透明可见下层系统设置"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍列表中的 “Privacy protection” 条目及详情页说明文本",
        "why_most_useful": "确认系统侧呈现给用户的唯一身份是“Privacy protection”，与桌面名 EmailService 不一致，坐实身份混淆",
        "observable_utg_signals": ["服务标签 Privacy protection", "描述文本 = acc_desc", "开关点击前的弹窗/授权流程"]
      },
      {
        "page_role": "获权后静默回跳/二次引导页",
        "page_identifier": "授权返回后重新出现的 UponGuideActivity 或 LineUponActivity（Translucent 插件宿主）",
        "why_most_useful": "用于判断是否存在拒权/撤权后的重跳循环与插件是否在获权后接管界面",
        "observable_utg_signals": ["返回键后是否再次弹出同一遮罩页", "LineUponActivity 透明宿主上的插件自绘控件", "进程 :daemon 是否常驻"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "显著盲区：真实引导流程的调度与后续动作由 DexClassLoader 从私有目录 dexout 加载的插件 DEX 执行（宿主仅提供 aa.b 跳转与遮罩页），插件是否二次跳转、是否伪造设置页、是否循环重跳无法静态确认；引导文案可能由插件运行时改写，UTG 捕获的文本需与静态 acc_tips 比对以判断是否被替换。应用未加壳，运行期 UTG 不受加壳阻挡。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED"
  ],
  "code_anchors": [
    "com.server.full.upon.view.aa#b",
    "com.server.full.upon.view.aa#a",
    "com.server.full.upon.view.UponGuideActivity#onCreate",
    "com.server.full.upon.UponActivity#onCreate",
    "com.server.full.upon.view.k#a",
    "res/values/strings.xml（acc_title / acc_desc / acc_tips）"
  ]
}
```

</details>
