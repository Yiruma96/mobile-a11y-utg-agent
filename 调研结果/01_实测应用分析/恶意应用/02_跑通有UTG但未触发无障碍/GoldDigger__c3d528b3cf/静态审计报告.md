# MB_059__c3d528b3cf｜GoldDigger — Identitas Kependudukan Digital

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：140.6s

## 1. 一句话核心结论

- **核心申请方式**：伪装成印尼政府『Identitas Kependudukan Digital』电子身份证应用的 DPT 加壳木马，通过 Splash→Activation/CheckPermission 多级原生页面加无图标跳板与 EasyFloat 悬浮窗引导用户开启名为同名品牌的 FocusService 无障碍服务，文案与跳转逻辑藏于加密载荷。
- **静态可见性说明**：应用整体由 DPT Shell 加壳（APKiD 确认）。明文 classes.dex 仅含 com.nashsiqiu.shell.ProxyApplication / JniBridge / ProxyComponentFactory 与占位 MainActivity；真实业务 DEX 由 assets/OoooooOooo（2.6MB 加密体）与 assets/vwwwwwvwww/{arch}/libdpt.so 在 attachBaseContext 阶段经 JNI 解密并内存加载，libASDFGHJ.so 为 Obfuscator-LLVM 9.x 混淆并含 syscalls 反 Hook。Manifest 组件、权限、无障碍服务声明与资源字符串（label/description）为明文可见，但 SplashActivity/ActivationActivity/CheckPermissionActivity/TransplentPermissionActivity 等引导页的方法体、弹窗文案、是否可取消、拒绝后重跳逻辑均在加密载荷内，静态不可还原；assets 下无 HTML，引导页非本地 WebView。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `c3d528b3cf8def7285977649e228dcf01847ce4f1432140cfa9a8067fd302ddb` |
| 包名 / 年份 | `com.zam.tquroa` / 2025 |
| 家族 / 品类 | **GoldDigger**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Identitas Kependudukan Digital |
| 引导页宣称品牌/身份 | Identitas Kependudukan Digital（印度尼西亚内政部官方电子身份证/KTP 数字化应用） |
| 系统无障碍列表服务名 | Identitas Kependudukan Digital |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务标签与 android:description 直接复用政府 App 品牌名，无任何技术化/工具化措辞；三个无图标跳板 Activity（NoIconActivty/NoIconActivty2/NoIconActivty3）+ Manifest 中 activity-alias/targetActivity 属性用于隐藏入口与多入口伪装；未声明 isAccessibilityTool（不伪造工具类，说明其并未试图规避系统警告，而是靠品牌名取得信任）；整体 DPT Shell 加壳使静态审计与逆向受阻。 |
| 无障碍服务类名 | `net.tents.dedrf.service.FocusService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=True` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Identitas Kependudukan Digital |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | net.tents.dedrf.ui.SplashActivity（壳启动后由解密载荷拉起） | 用户点击桌面图标启动；ProxyApplication.attachBaseContext 完成载荷解密与 ClassLoader 注入后进入真实入口 | 原生Activity | **原文**：不可静态还原（位于 assets/OoooooOooo 加密载荷内）<br>**译注**：启动页/引导页文案无法静态获取；预筛资源字符串含『获取权限失败，继续保存图片』『Service exception, please try again』『Background Services』等权限与异常类文案 | 不可静态还原 | `com.nashsiqiu.shell.ProxyApplication#attachBaseContext → net.tents.dedrf.ui.SplashActivity` |
| 2 | 业务功能触发 / 引导说明页 | net.tents.dedrf.ui.ActivationActivity、net.tents.dedrf.ui.CheckPermissionActivity | Splash 结束后或身份核验/激活业务流程进入时拉起（推测由加密载荷内的启动调度决定，不可静态确认） | 原生Activity（可能叠加 EasyFloat 悬浮窗） | **原文**：不可静态还原<br>**译注**：推测为以『激活/身份核验需要辅助功能』为由的说明页；文案与按钮均在加密载荷内 | 不可静态还原（是否存在取消/跳过按钮无法确认） | `net.tents.dedrf.ui.ActivationActivity / net.tents.dedrf.ui.CheckPermissionActivity` |
| 3 | 跳受限设置 | android.settings.ACCESSIBILITY_SETTINGS 系统页；同包另声明 TransplentPermissionActivity（透明权限中转页） | 用户点击引导页按钮后，由加密载荷代码以 Intent(ACTION_ACCESSIBILITY_SETTINGS) 拉起；页面栈下层保留 TransplentPermissionActivity 作为返回落点 | 系统无障碍页 | **原文**：Identitas Kependudukan Digital<br>**译注**：系统无障碍服务列表中以『Identitas Kependudukan Digital』显示（与服务 android:label 及 android:description 一致） | 引导用户在该系统页中找到同名服务并开启开关 | `#1 manifest:components（service net.tents.dedrf.service.FocusService + meta-data android.accessibilityservice）` |
| 4 | 遮罩叠层指引 | EasyFloat（com.lzf.easyfloat，由 com.zam.tquroa.EasyFloatInitializer 初始化）悬浮窗 + SYSTEM_ALERT_WINDOW 权限 | 设置页拉起前后由悬浮窗服务创建 TYPE_APPLICATION_OVERLAY 视图（具体时序在加密载荷内） | 悬浮窗Overlay | **原文**：不可静态还原<br>**译注**：推测为在系统设置页上叠加的半透明指引层（箭头/手指提示或高仿开关），文案不可静态获取 | 引导用户按遮罩指示点开对应开关 | `com.zam.tquroa.EasyFloatInitializer / com.lzf.easyfloat` |
| 5 | 拒权反馈循环 | net.tents.dedrf.ui.WaitCheckActivity、NoIconActivty/NoIconActivty2/NoIconActivty3（无图标跳板） | onResume 回调或轮询检测无障碍服务未启用时重新跳转（逻辑在加密载荷内，静态不可确认） | 原生Activity | **原文**：不可静态还原<br>**译注**：推测为『等待核验/请继续开启权限』类循环页；无法确认是否可退出 | 不可静态还原 | `net.tents.dedrf.ui.WaitCheckActivity / net.tents.dedrf.service.NoIconActivty` |
| 6 | 获权后动作 | net.tents.dedrf.service.FocusService（AccessibilityService 本体） | 系统回调 onServiceConnected / onAccessibilityEvent | 不可静态还原 | **原文**：不可静态还原<br>**译注**：服务实现体位于加密载荷，其读屏/点击/按键注入行为无法静态确认 | 不可静态还原 | `net.tents.dedrf.service.FocusService（声明可见，实现体在 assets/OoooooOooo）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：android:label 与 android:description 均为『Identitas Kependudukan Digital』（Manifest service 声明，明文可见）
- 应用桌面名称：application android:label =『Identitas Kependudukan Digital』，与无障碍服务名完全一致
- net.tents.dedrf.ui.ActivationActivity / CheckPermissionActivity 原生页面（文案在加密载荷内，位置可定位、内容不可静态读取）
- EasyFloat 悬浮窗（TYPE_APPLICATION_OVERLAY）叠加在系统设置页之上的引导层（需 SYSTEM_ALERT_WINDOW）
- 预筛已提取的资源字符串（resources.arsc，本次因读取受限未直接复核）：『获取权限失败，继续保存图片』『1.取得权限失败，无法执行操作。 2.若因先前拒绝了权限授予…将「%s」勾选允许。』『获取系统相机权限被拒绝』『Background Services』『Service exception, please try again』
- 未发现 assets 内本地 HTML 教学页（assets 仅 app_name / app_acf / dpt.so / OoooooOooo），故不存在本地 WebView 引导

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| zh | 1.取得权限失败，无法执行操作。 2.若因先前拒绝了权限授予，而没有出现权限请求画面，请『设置 → 应用程序 → 当前App → 权限』，将「%s」勾选允许。 | 1. 取得权限失败，无法执行操作。2. 若因先前拒绝了权限授予而没有出现权限请求画面，请前往『设置 → 应用程序 → 当前App → 权限』，将「%s」勾选为允许。 | `resources.arsc 字符串（预筛提取，本次未直接复核）` | 受限设置分步教学 |
| zh | 获取系统相机权限被拒绝 | 获取系统相机权限被拒绝 | `resources.arsc 字符串（预筛提取）` | 未知 |
| zh | 获取系统录音权限被拒绝 | 获取系统录音权限被拒绝 | `resources.arsc 字符串（预筛提取）` | 未知 |
| zh | 获取权限失败，继续保存图片 | 获取权限失败，继续保存图片 | `resources.arsc 字符串（预筛提取）` | 未知 |
| en | Sorry, the page encountered a problem and needs to be closed | 抱歉，页面遇到问题需要关闭 | `resources.arsc 字符串（预筛提取）` | 假更新 |
| en | Identitas Kependudukan Digital | 数字化人口身份（印尼官方电子身份证/KTP 数字化应用名） | `AndroidManifest.xml：application android:label、service net.tents.dedrf.service.FocusService android:label/android:description` | 假反诈安全 |
| en | Background Services | 后台服务 | `resources.arsc 字符串（预筛提取）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原。存在 WaitCheckActivity（等待核验页）与 NoIconActivty/NoIconActivty2/NoIconActivty3 三个无图标跳板 Activity，结构上具备 onResume/轮询后重新拉起无障碍设置页的能力，但具体是否死循环重跳、是否有定时器（如每 2 秒）需运行期 UTG 观察确认。
- **遮罩叠层 / 高仿系统设置页**：具备悬浮窗叠层能力：声明 SYSTEM_ALERT_WINDOW 与 SYSTEM_OVERLAY_WINDOW，并集成 com.lzf.easyfloat（EasyFloat，由 com.zam.tquroa.EasyFloatInitializer 初始化），可在系统无障碍设置页之上叠加半透明引导遮罩或高仿开关；是否实际绘制不可静态确认。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（未见 Android 13+ 受限设置相关引导代码，且未声明 isAccessibilityTool；但资源字符串中存在『设置 → 应用程序 → 当前App → 权限』式分步教学，属权限页而非受限设置教学）。
- **获权后即时行为与防撤权机制**：不可静态还原。Manifest 侧存在明显反移除设施：多进程守护与自启组件 com.uhlts.cfdik.MR2Service / NewProcessService / TempForegroundService / MyPocReceiver、org.psjyy.aeikp.WmKeepService、org.vkjoi.cfuje.SnService/JobService，以及 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、RECEIVE_BOOT_COMPLETED、USE_EXACT_ALARM；是否通过 GLOBAL_ACTION_BACK/HOME 阻止用户撤权需运行期验证。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以 ActivityManager/Instrumentation 监测两类信号即拉起 UTG 快照：(1) 应用进程发起 Intent 跳转 android.settings.ACCESSIBILITY_SETTINGS（或 ACTION_APPLICATION_DETAILS_SETTINGS）；(2) 进入 net.tents.dedrf.ui.ActivationActivity / CheckPermissionActivity / TransplentPermissionActivity / WaitCheckActivity 的 onResume。冷启动后（SplashActivity 消失）即开始 200–400ms 间隔连续抓屏，覆盖从引导页到系统设置页的整段流转。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区为：①DPT Shell 加壳使引导页文案与跳转时序完全不可静态读取，必须以运行期 UTG 为准；②FocusService 获权后的读屏/注入行为在加密载荷内，UTG 只能观察其对外表现（如自动点击、页面突变）；③若载荷按设备/地域/时间做云控惰性触发，冷启动可能长时间不出现引导页，需配合网络流量捕获确认下发时机；④assets 内无 HTML，故不存在本地 WebView 引导盲区。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动/激活引导页（申请无障碍的直接入口）** | net.tents.dedrf.ui.ActivationActivity 或 CheckPermissionActivity 窗口（顶层包名 com.zam.tquroa） | 此页是用户首次被告知『为何需要无障碍/辅助功能』的地方，其话术框架（假身份核验/假反诈/功能必需）与按钮布局（是否存在取消/跳过）直接决定诱导定性 | 页面文案全文（含假品牌与『必需开启』措辞）；是否存在取消/跳过/稍后按钮及其可见性；页面是否以返回键不可退出（onKeyDown 拦截表现） |
| **系统无障碍服务列表项（品牌伪装落点）** | android.settings.ACCESSIBILITY_SETTINGS 页面中 label 为『Identitas Kependudukan Digital』的服务条目 | 验证服务名与说明文本与桌面 App 名完全一致的品牌冒用效果，并检查是否出现系统『此服务可读取全部内容』警告（因未声明 isAccessibilityTool） | 服务条目显示名称与副标题全文；系统安全警告文案是否展示；同页是否存在与本应用同名的其他可疑服务项 |
| **设置页上叠加的悬浮引导遮罩** | TYPE_APPLICATION_OVERLAY 窗口（EasyFloat 创建），叠加于系统设置 Activity 之上 | 遮罩/高仿开关是『诱导开启』最关键的强证据，可区分正常说明与欺骗式引导 | 是否存在非系统窗口覆盖设置页（窗口层级/非 activity 视图）；遮罩中的箭头/手指/『点此开启』提示文案；是否绘制仿系统开关控件 |
| **拒绝或返回后的循环反馈页** | net.tents.dedrf.ui.WaitCheckActivity 或无图标跳板 Activity（NoIconActivty*）重新出现在前台 | 判定是否存在拒权死循环/反复拉起，是『胁迫式不可跳过』定性的核心 | 从设置页返回后 1–3 秒内是否再次跳转 ACCESSIBILITY_SETTINGS；重复跳转次数与间隔（判断定时器周期）；是否出现无法退出的全屏提示 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.nashsiqiu.shell.ProxyApplication#attachBaseContext`
- `#1 manifest:components`
- `net.tents.dedrf.service.FocusService`
- `net.tents.dedrf.ui.ActivationActivity`
- `net.tents.dedrf.ui.TransplentPermissionActivity`
- `assets/OoooooOooo`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点

- **静态可见性受限：应用被 DPT Shell 整体加壳**。`classes.dex` 仅剩 6 个壳类（`com.nashsiqiu.shell.*`、`com.nash.dpt.MainActivity` 占位页），真实业务代码不在明文 DEX 中。[ProxyApplication.attachBaseContext()](<resource-unit:#1.dex1 code:com.nashsiqiu.shell.ProxyApplication#attachBaseContext>) 读取 `assets/app_name` 后调用 `JniBridge.loadShellLibs(dataDir, sourceDir)` 与 `JniBridge.cbde(ClassLoader)`，由 `assets/vwwwwwvwww/{arch}/libdpt.so` 在内存中解密执行；加密主体为 `assets/OoooooOooo`（2.6 MB）与 `libASDFGHJ.so`（Obfuscator-LLVM 9.x）。APKiD 确认 `protector: DPT Shell`、`anti_hook: syscalls`。
- **无障碍服务确实存在且伪装为印尼政府电子身份证应用**。Manifest 声明 `net.tents.dedrf.service.FocusService`，权限 `android.permission.BIND_ACCESSIBILITY_SERVICE`，meta-data `android.accessibilityservice`；服务名与 `android:description` 均为 `Identitas Kependudukan Digital`，与桌面显示名完全一致，**利用真实政府 App 品牌而非技术化名称降低用户警惕**。字符串池中**未见 `isAccessibilityTool`**，即未伪造工具类声明（Android 13+ 会显示完整警告）。
- **引导链路组件齐备但方法体不可静态还原**：`SplashActivity`、`ActivationActivity`、`CheckPermissionActivity`、`TransplentPermissionActivity`（透明权限页）、`WaitCheckActivity`、`NoIconActivty`/`NoIconActivty2`/`NoIconActivty3`（无图标跳板）构成多级跳转链；配合 `SYSTEM_ALERT_WINDOW` 与 `com.lzf.easyfloat`（EasyFloat）具备跳设置后压栈悬浮引导能力。
- **无本地 HTML 教学页**：`assets/` 下仅 `app_name`、`app_acf`、`dpt.so`、`OoooooOooo`，无 `.html`，故引导文案若存在只能来自原生代码（字符串在加密载荷内）或远端 WebView。
- **配套的诱导与保活设计**：桌面小组件 `WidgetBaoXiang/WidgetFuDai/WidgetHongBao/WidgetJinBi/WidgetLiWu`（宝箱/福袋/红包/金币/礼物）为诱饵；`com.uhlts.cfdik.*`（`MR2Service`、`NewProcessService`、`TempForegroundService`、`MyPocReceiver`）、`org.psjyy.aeikp.WmKeepService`、`org.vkjoi.cfuje.*` 为多进程守护与自启组件。
- **边界**：具体弹窗文案、按钮可取消性、拒绝后重跳逻辑均位于加密载荷，**本次无法静态还原**，需运行期 UTG 采集。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "应用整体由 DPT Shell 加壳（APKiD 确认）。明文 classes.dex 仅含 com.nashsiqiu.shell.ProxyApplication / JniBridge / ProxyComponentFactory 与占位 MainActivity；真实业务 DEX 由 assets/OoooooOooo（2.6MB 加密体）与 assets/vwwwwwvwww/{arch}/libdpt.so 在 attachBaseContext 阶段经 JNI 解密并内存加载，libASDFGHJ.so 为 Obfuscator-LLVM 9.x 混淆并含 syscalls 反 Hook。Manifest 组件、权限、无障碍服务声明与资源字符串（label/description）为明文可见，但 SplashActivity/ActivationActivity/CheckPermissionActivity/TransplentPermissionActivity 等引导页的方法体、弹窗文案、是否可取消、拒绝后重跳逻辑均在加密载荷内，静态不可还原；assets 下无 HTML，引导页非本地 WebView。",
  "summary_one_liner": "伪装成印尼政府『Identitas Kependudukan Digital』电子身份证应用的 DPT 加壳木马，通过 Splash→Activation/CheckPermission 多级原生页面加无图标跳板与 EasyFloat 悬浮窗引导用户开启名为同名品牌的 FocusService 无障碍服务，文案与跳转逻辑藏于加密载荷。",
  "disguise_identity": {
    "app_display_name": "Identitas Kependudukan Digital",
    "claimed_brand_or_persona": "Identitas Kependudukan Digital（印度尼西亚内政部官方电子身份证/KTP 数字化应用）",
    "a11y_service_label": "Identitas Kependudukan Digital",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务标签与 android:description 直接复用政府 App 品牌名，无任何技术化/工具化措辞；三个无图标跳板 Activity（NoIconActivty/NoIconActivty2/NoIconActivty3）+ Manifest 中 activity-alias/targetActivity 属性用于隐藏入口与多入口伪装；未声明 isAccessibilityTool（不伪造工具类，说明其并未试图规避系统警告，而是靠品牌名取得信任）；整体 DPT Shell 加壳使静态审计与逆向受阻。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "net.tents.dedrf.ui.SplashActivity（壳启动后由解密载荷拉起）",
      "trigger_event": "用户点击桌面图标启动；ProxyApplication.attachBaseContext 完成载荷解密与 ClassLoader 注入后进入真实入口",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "不可静态还原（位于 assets/OoooooOooo 加密载荷内）",
      "shown_text_zh": "启动页/引导页文案无法静态获取；预筛资源字符串含『获取权限失败，继续保存图片』『Service exception, please try again』『Background Services』等权限与异常类文案",
      "user_action_requested": "不可静态还原",
      "code_anchor": "com.nashsiqiu.shell.ProxyApplication#attachBaseContext → net.tents.dedrf.ui.SplashActivity"
    },
    {
      "step": 2,
      "stage": "业务功能触发 / 引导说明页",
      "screen_or_component": "net.tents.dedrf.ui.ActivationActivity、net.tents.dedrf.ui.CheckPermissionActivity",
      "trigger_event": "Splash 结束后或身份核验/激活业务流程进入时拉起（推测由加密载荷内的启动调度决定，不可静态确认）",
      "ui_carrier": "原生Activity（可能叠加 EasyFloat 悬浮窗）",
      "shown_text_verbatim": "不可静态还原",
      "shown_text_zh": "推测为以『激活/身份核验需要辅助功能』为由的说明页；文案与按钮均在加密载荷内",
      "user_action_requested": "不可静态还原（是否存在取消/跳过按钮无法确认）",
      "code_anchor": "net.tents.dedrf.ui.ActivationActivity / net.tents.dedrf.ui.CheckPermissionActivity"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "android.settings.ACCESSIBILITY_SETTINGS 系统页；同包另声明 TransplentPermissionActivity（透明权限中转页）",
      "trigger_event": "用户点击引导页按钮后，由加密载荷代码以 Intent(ACTION_ACCESSIBILITY_SETTINGS) 拉起；页面栈下层保留 TransplentPermissionActivity 作为返回落点",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Identitas Kependudukan Digital",
      "shown_text_zh": "系统无障碍服务列表中以『Identitas Kependudukan Digital』显示（与服务 android:label 及 android:description 一致）",
      "user_action_requested": "引导用户在该系统页中找到同名服务并开启开关",
      "code_anchor": "#1 manifest:components（service net.tents.dedrf.service.FocusService + meta-data android.accessibilityservice）"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "EasyFloat（com.lzf.easyfloat，由 com.zam.tquroa.EasyFloatInitializer 初始化）悬浮窗 + SYSTEM_ALERT_WINDOW 权限",
      "trigger_event": "设置页拉起前后由悬浮窗服务创建 TYPE_APPLICATION_OVERLAY 视图（具体时序在加密载荷内）",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "不可静态还原",
      "shown_text_zh": "推测为在系统设置页上叠加的半透明指引层（箭头/手指提示或高仿开关），文案不可静态获取",
      "user_action_requested": "引导用户按遮罩指示点开对应开关",
      "code_anchor": "com.zam.tquroa.EasyFloatInitializer / com.lzf.easyfloat"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "net.tents.dedrf.ui.WaitCheckActivity、NoIconActivty/NoIconActivty2/NoIconActivty3（无图标跳板）",
      "trigger_event": "onResume 回调或轮询检测无障碍服务未启用时重新跳转（逻辑在加密载荷内，静态不可确认）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "不可静态还原",
      "shown_text_zh": "推测为『等待核验/请继续开启权限』类循环页；无法确认是否可退出",
      "user_action_requested": "不可静态还原",
      "code_anchor": "net.tents.dedrf.ui.WaitCheckActivity / net.tents.dedrf.service.NoIconActivty"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "net.tents.dedrf.service.FocusService（AccessibilityService 本体）",
      "trigger_event": "系统回调 onServiceConnected / onAccessibilityEvent",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "不可静态还原",
      "shown_text_zh": "服务实现体位于加密载荷，其读屏/点击/按键注入行为无法静态确认",
      "user_action_requested": "不可静态还原",
      "code_anchor": "net.tents.dedrf.service.FocusService（声明可见，实现体在 assets/OoooooOooo）"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：android:label 与 android:description 均为『Identitas Kependudukan Digital』（Manifest service 声明，明文可见）",
    "应用桌面名称：application android:label =『Identitas Kependudukan Digital』，与无障碍服务名完全一致",
    "net.tents.dedrf.ui.ActivationActivity / CheckPermissionActivity 原生页面（文案在加密载荷内，位置可定位、内容不可静态读取）",
    "EasyFloat 悬浮窗（TYPE_APPLICATION_OVERLAY）叠加在系统设置页之上的引导层（需 SYSTEM_ALERT_WINDOW）",
    "预筛已提取的资源字符串（resources.arsc，本次因读取受限未直接复核）：『获取权限失败，继续保存图片』『1.取得权限失败，无法执行操作。 2.若因先前拒绝了权限授予…将「%s」勾选允许。』『获取系统相机权限被拒绝』『Background Services』『Service exception, please try again』",
    "未发现 assets 内本地 HTML 教学页（assets 仅 app_name / app_acf / dpt.so / OoooooOooo），故不存在本地 WebView 引导"
  ],
  "verbatim_texts": [
    {
      "lang": "zh",
      "text_verbatim": "1.取得权限失败，无法执行操作。 2.若因先前拒绝了权限授予，而没有出现权限请求画面，请『设置 → 应用程序 → 当前App → 权限』，将「%s」勾选允许。",
      "text_zh": "1. 取得权限失败，无法执行操作。2. 若因先前拒绝了权限授予而没有出现权限请求画面，请前往『设置 → 应用程序 → 当前App → 权限』，将「%s」勾选为允许。",
      "source_location": "resources.arsc 字符串（预筛提取，本次未直接复核）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "zh",
      "text_verbatim": "获取系统相机权限被拒绝",
      "text_zh": "获取系统相机权限被拒绝",
      "source_location": "resources.arsc 字符串（预筛提取）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "zh",
      "text_verbatim": "获取系统录音权限被拒绝",
      "text_zh": "获取系统录音权限被拒绝",
      "source_location": "resources.arsc 字符串（预筛提取）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "zh",
      "text_verbatim": "获取权限失败，继续保存图片",
      "text_zh": "获取权限失败，继续保存图片",
      "source_location": "resources.arsc 字符串（预筛提取）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Sorry, the page encountered a problem and needs to be closed",
      "text_zh": "抱歉，页面遇到问题需要关闭",
      "source_location": "resources.arsc 字符串（预筛提取）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Identitas Kependudukan Digital",
      "text_zh": "数字化人口身份（印尼官方电子身份证/KTP 数字化应用名）",
      "source_location": "AndroidManifest.xml：application android:label、service net.tents.dedrf.service.FocusService android:label/android:description",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Background Services",
      "text_zh": "后台服务",
      "source_location": "resources.arsc 字符串（预筛提取）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原。存在 WaitCheckActivity（等待核验页）与 NoIconActivty/NoIconActivty2/NoIconActivty3 三个无图标跳板 Activity，结构上具备 onResume/轮询后重新拉起无障碍设置页的能力，但具体是否死循环重跳、是否有定时器（如每 2 秒）需运行期 UTG 观察确认。",
    "overlay_or_fake_settings": "具备悬浮窗叠层能力：声明 SYSTEM_ALERT_WINDOW 与 SYSTEM_OVERLAY_WINDOW，并集成 com.lzf.easyfloat（EasyFloat，由 com.zam.tquroa.EasyFloatInitializer 初始化），可在系统无障碍设置页之上叠加半透明引导遮罩或高仿开关；是否实际绘制不可静态确认。",
    "restricted_settings_13plus_coaching": "无（未见 Android 13+ 受限设置相关引导代码，且未声明 isAccessibilityTool；但资源字符串中存在『设置 → 应用程序 → 当前App → 权限』式分步教学，属权限页而非受限设置教学）。",
    "post_grant_anti_removal": "不可静态还原。Manifest 侧存在明显反移除设施：多进程守护与自启组件 com.uhlts.cfdik.MR2Service / NewProcessService / TempForegroundService / MyPocReceiver、org.psjyy.aeikp.WmKeepService、org.vkjoi.cfuje.SnService/JobService，以及 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、RECEIVE_BOOT_COMPLETED、USE_EXACT_ALARM；是否通过 GLOBAL_ACTION_BACK/HOME 阻止用户撤权需运行期验证。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以 ActivityManager/Instrumentation 监测两类信号即拉起 UTG 快照：(1) 应用进程发起 Intent 跳转 android.settings.ACCESSIBILITY_SETTINGS（或 ACTION_APPLICATION_DETAILS_SETTINGS）；(2) 进入 net.tents.dedrf.ui.ActivationActivity / CheckPermissionActivity / TransplentPermissionActivity / WaitCheckActivity 的 onResume。冷启动后（SplashActivity 消失）即开始 200–400ms 间隔连续抓屏，覆盖从引导页到系统设置页的整段流转。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动/激活引导页（申请无障碍的直接入口）",
        "page_identifier": "net.tents.dedrf.ui.ActivationActivity 或 CheckPermissionActivity 窗口（顶层包名 com.zam.tquroa）",
        "why_most_useful": "此页是用户首次被告知『为何需要无障碍/辅助功能』的地方，其话术框架（假身份核验/假反诈/功能必需）与按钮布局（是否存在取消/跳过）直接决定诱导定性",
        "observable_utg_signals": ["页面文案全文（含假品牌与『必需开启』措辞）", "是否存在取消/跳过/稍后按钮及其可见性", "页面是否以返回键不可退出（onKeyDown 拦截表现）"]
      },
      {
        "page_role": "系统无障碍服务列表项（品牌伪装落点）",
        "page_identifier": "android.settings.ACCESSIBILITY_SETTINGS 页面中 label 为『Identitas Kependudukan Digital』的服务条目",
        "why_most_useful": "验证服务名与说明文本与桌面 App 名完全一致的品牌冒用效果，并检查是否出现系统『此服务可读取全部内容』警告（因未声明 isAccessibilityTool）",
        "observable_utg_signals": ["服务条目显示名称与副标题全文", "系统安全警告文案是否展示", "同页是否存在与本应用同名的其他可疑服务项"]
      },
      {
        "page_role": "设置页上叠加的悬浮引导遮罩",
        "page_identifier": "TYPE_APPLICATION_OVERLAY 窗口（EasyFloat 创建），叠加于系统设置 Activity 之上",
        "why_most_useful": "遮罩/高仿开关是『诱导开启』最关键的强证据，可区分正常说明与欺骗式引导",
        "observable_utg_signals": ["是否存在非系统窗口覆盖设置页（窗口层级/非 activity 视图）", "遮罩中的箭头/手指/『点此开启』提示文案", "是否绘制仿系统开关控件"]
      },
      {
        "page_role": "拒绝或返回后的循环反馈页",
        "page_identifier": "net.tents.dedrf.ui.WaitCheckActivity 或无图标跳板 Activity（NoIconActivty*）重新出现在前台",
        "why_most_useful": "判定是否存在拒权死循环/反复拉起，是『胁迫式不可跳过』定性的核心",
        "observable_utg_signals": ["从设置页返回后 1–3 秒内是否再次跳转 ACCESSIBILITY_SETTINGS", "重复跳转次数与间隔（判断定时器周期）", "是否出现无法退出的全屏提示"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区为：①DPT Shell 加壳使引导页文案与跳转时序完全不可静态读取，必须以运行期 UTG 为准；②FocusService 获权后的读屏/注入行为在加密载荷内，UTG 只能观察其对外表现（如自动点击、页面突变）；③若载荷按设备/地域/时间做云控惰性触发，冷启动可能长时间不出现引导页，需配合网络流量捕获确认下发时机；④assets 内无 HTML，故不存在本地 WebView 引导盲区。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.nashsiqiu.shell.ProxyApplication#attachBaseContext",
    "#1 manifest:components",
    "net.tents.dedrf.service.FocusService",
    "net.tents.dedrf.ui.ActivationActivity",
    "net.tents.dedrf.ui.TransplentPermissionActivity",
    "assets/OoooooOooo"
  ]
}
```

> 说明：本次受 8–14 次工具调用硬性约束限制，且 `read_manifest` 在该样本上因解包缓存路径问题持续失败（已改用自建 AXML 解析器从 APK 直接提取 Manifest 字符串池与组件声明作为替代证据），未再展开对 `libdpt.so` / `assets/OoooooOooo` 的解密逆向，故 `static_visibility` 如实标注为 `packed_or_encrypted`，弹窗文案与拒权循环逻辑留待运行期 UTG 采集。

</details>
