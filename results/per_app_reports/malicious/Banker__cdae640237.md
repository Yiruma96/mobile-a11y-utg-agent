# MR_142__cdae640237｜Banker — Coronavirus Finder

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：156.1s

## 1. 一句话核心结论

- **核心申请方式**：以“Coronavirus Finder”疫情追踪为外壳的银行木马，第一阶段 Application 在 attachBaseContext 解密 assets/db_dex.nmp 并动态加载第二阶段 DEX，第二阶段才实现无障碍开启引导与后续支付页伪装；引导页实现本身完全藏在加密载荷中，静态仅可见同名无障碍服务与“需要无障碍以检测感染者位置”的说明文案。
- **静态可见性说明**：AndroidManifest.xml 声明的全部业务组件（含无障碍服务与 ActivityEnableAccessibility/ActivityPermission/ActivityAllPermissions/ActivityDozeAndPermissions/ActivityPlayProtect/ActivityShowAlert/ActivityWebViewPush）所属包 zsezrfpgojacmkyfhbotthbkgi.zqzngmsqlapqqoxfwweuoui.qfulgeigxoyklbrciyug 在 classes.dex 中不存在（仅 5 个包、813 类，无该包）；真正的 DEX 以加密形态存于 assets/db_dex.nmp（44,394B，首字节 00 25 36 41 67 7f 48 54，无 dex/zip 魔数），由 Application.attachBaseContext 经 Ralphalunar.doublefind 反射读取 AssetManager 解密落盘后动态加载，故无障碍引导的页面流转、跳转 Intent 与拒权循环逻辑均不可静态还原；仅 Manifest 组件声明、strings.xml 文案与 serviceconfig.xml 配置可见。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `cdae640237fa190c62f0b1d89e504dc0d728e771026b241b1a549f9c8b6d57c0` |
| 包名 / 年份 | `bgmqkf.xpybwomhl.ljpfhtxfxx` / 2020 |
| 家族 / 品类 | **Banker**（同池样本数：9） |
| 原始来源标识 | https://labs.bitdefender.com/2020/03/android-apps-and-malware-capitalize-on-coronavirus/ |
| 桌面显示名 | Coronavirus Finder |
| 引导页宣称品牌/身份 | Coronavirus Finder（疫情/感染者位置追踪工具）；同时准备 Google Play / GPay 支付页面伪装素材（button_text=Verify Payment Method、gpay_logo.png） |
| 系统无障碍列表服务名 | Coronavirus Finder（service 的 android:label=@string/app_name，与桌面名完全一致） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 无障碍服务 label 复用 @string/app_name，使系统无障碍列表条目与桌面应用名完全一致，用户无法从名称分辨；2) 说明文案首句为 'Coronavirus Finder requires accessibility access in order to automatically detect and display locations of infected people around.'，第二句另起一行并以换行+空行隔开 'Please, enable it to fully integrate the Application.'，利用换行把“系统警告式说明”与真实索取意图分离（strings.xml 中保留原始 \n 换行）；3) 全部业务组件置于同一长随机包名下并按 taskAffinity=com.a1/a2/a3/a4 分任务栈，ActivityEnableAccessibility 单独 taskAffinity=com.a1，便于从任意栈顶拉起且不暴露于最近任务（MainActivity、ActivityPermission、ActivityShowAlert 等均 excludeFromRecents/noHistory）；4) 类名/方法名整体随机化（Rcaveoxygen、Quncoversize 等 60+ 随机 Activity 作为噪声掩护），并用大量无效算术、循环与字段读写做控制流/死代码混淆；5) res/xml/serviceconfig.xml 仅声明 canRetrieveWindowContent，未声明 accessibilityFlags/事件类型，说明配置极简，真实能力由运行时第二阶段代码自设。 |
| 无障碍服务类名 | `zsezrfpgojacmkyfhbotthbkgi.zqzngmsqlapqqoxfwweuoui.qfulgeigxoyklbrciyug.ServiceAccessibility` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS` |
| 系统设置项说明 (`android:description`) | Coronavirus Finder requires accessibility access in order to automatically detect and display locations of infected people around. <br>Please, enable it to fully integrate the Application. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | bgmqkf.xpybwomhl.ljpfhtxfxx.Scameramention（Application，android:name 声明）→ 私有目录中解密落盘的二阶段 DEX | 进程创建时 attachBaseContext(Context) 被系统回调 | 不可静态还原 | 无 | 无（用户无感知） | `bgmqkf.xpybwomhl.ljpfhtxfxx.Scameramention.attachBaseContext → Ralphalunar.doublefind / Gmomentprice.aboutelectric；assets/db_dex.nmp` |
| 2 | 引导说明页 | zsezrfpgojacmkyfhbotthbkgi.zqzngmsqlapqqoxfwweuoui.qfulgeigxoyklbrciyug.ActivityEnableAccessibility（taskAffinity=com.a1，无 label，无 excludeFromRecents） | 无法静态确认（组件在加密载荷中实现；推测由二阶段 DEX 在主界面或权限流水线后拉起） | 不可静态还原 | **原文**：Coronavirus Finder requires accessibility access in order to automatically detect and display locations of infected people around. <br>Please, enable it to fully integrate the Application.<br>**译注**：Coronavirus Finder 需要无障碍权限，以便自动检测并显示周围感染者的位置。请开启该权限，以便完整使用本应用。 | 无法静态确认（该 Activity 无 label，可能为引导说明+确认按钮；是否有取消/跳过按钮不可见） | `AndroidManifest.xml: <activity android:name="...ActivityEnableAccessibility" android:taskAffinity="com.a1"/>；res/values/strings.xml#accessibility_description；res/xml/serviceconfig.xml` |
| 3 | 跳无障碍设置 | 系统 Settings.ACTION_ACCESSIBILITY_SETTINGS 无障碍服务列表（目标条目 label = Coronavirus Finder） | 无法静态确认（推测为 ActivityEnableAccessibility 内点击按钮后 startActivity(Intent(ACTION_ACCESSIBILITY_SETTINGS))） | 系统无障碍页 | **原文**：Coronavirus Finder<br>**译注**：系统无障碍服务列表中显示的应用/服务名（与桌面显示名一致） | 用户需在系统列表中手动找到并开启名为 Coronavirus Finder 的无障碍服务 | `AndroidManifest.xml: <service ...ServiceAccessibility android:label="@string/app_name"> + <meta-data android:name="android.accessibilityservice" android:resource="@xml/serviceconfig"/>；res/xml/serviceconfig.xml` |
| 4 | 跳受限设置（应用详情） | 系统 Settings.ACTION_APPLICATION_DETAILS_SETTINGS 应用详情页；伴随 ActivityPermission（noHistory=true、excludeFromRecents）、ActivityAllPermissions（clearTaskOnLaunch、taskAffinity=com.a4）、ActivityDozeAndPermissions（taskAffinity=com.a2）等权限流水线 Activity | 无法静态确认 | 不可静态还原 | 无 | 无法静态确认（疑似要求用户在应用详情中授予短信/电话/通讯录权限并忽略电池优化） | `AndroidManifest.xml: ActivityPermission / ActivityAllPermissions / ActivityDozeAndPermissions / ActivityPlayProtect；uses-permission 列表` |
| 5 | 拒权反馈循环 | 无法静态确认（ActivityShowAlert（noHistory、excludeFromRecents）与 ActivityWebViewPush 为候选载体） | 无法静态确认（可能为 onResume 检测服务未启用后重跳） | 不可静态还原 | 无 | 无法静态确认 | `AndroidManifest.xml: ActivityShowAlert / ActivityWebViewPush / ActivityEnableAccessibility(taskAffinity=com.a1)` |
| 6 | 获权后动作 | zsezrfpgojacmkyfhbotthbkgi.zqzngmsqlapqqoxfwweuoui.qfulgeigxoyklbrciyug.ServiceAccessibility（canRetrieveWindowContent=true）+ ServiceSendSMS / ServiceHiddenSMS / ServiceSMSPermissions / ReceiverIncomingSms(priority 998) / ActivityGenerateFakeSMS / ActivityInjectionPhoto / ActivityChangeSmsManager | 无障碍服务被系统绑定后回调 onServiceConnected（实现不可见） | 不可静态还原 | **原文**：Verify Payment Method<br>**译注**：“验证支付方式”（strings.xml button_text，配合 res/drawable-v24/gpay_logo.png 与 res/layout/google_alert.xml 构建的伪造 Google Play/GPay 支付页） | 无法静态确认（疑似诱导在伪造支付页输入卡号/验证码） | `res/values/strings.xml#button_text；res/layout/google_alert.xml；res/layout/webview_small.xml；AndroidManifest.xml 短信/无障碍服务声明` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表条目名称：android:label="@string/app_name" = "Coronavirus Finder"（与桌面图标名完全一致，无任何服务专属后缀）
- 系统无障碍服务说明：res/xml/serviceconfig.xml 的 android:description="@string/accessibility_description"，即 "Coronavirus Finder requires accessibility access in order to automatically detect and display locations of infected people around.\nPlease, enable it to fully integrate the Application."（含换行分隔）
- 应用内引导说明页：ActivityEnableAccessibility（taskAffinity=com.a1）—— 该 Activity 无 label，具体布局/弹窗实现位于加密载荷 assets/db_dex.nmp 解密后的 DEX，静态不可见
- 权限/优化提示流水线：ActivityPermission（noHistory、excludeFromRecents）、ActivityAllPermissions（clearTaskOnLaunch）、ActivityDozeAndPermissions、ActivityPlayProtect —— 文案不可静态还原
- 告警/推送类承载：ActivityShowAlert（noHistory、excludeFromRecents）、ActivityWebViewPush（noHistory）、res/layout/webview_small.xml（内嵌 WebView 容器，加载地址不可静态还原）
- 支付凭证页素材：res/values/strings.xml 的 button_text="Verify Payment Method"、image_alt="Google Play Logo"，配合 res/drawable-v24/gpay_logo.png 与 res/layout/google_alert.xml
- 本地 HTML 仅为合规外壳（assets/consent_policy.html = Avast Software s.r.o. 同意政策；assets/eula.html = 2018 版 EULA），与本应用引导无关，属借用第三方模板的噪声/伪装素材

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Coronavirus Finder requires accessibility access in order to automatically detect and display locations of infected people around. <br>Please, enable it to fully integrate the Application. | Coronavirus Finder 需要无障碍权限，以便自动检测并显示周围感染者的位置。请开启该权限，以便完整使用本应用。 | `res/values/strings.xml#accessibility_description（由 res/xml/serviceconfig.xml 的 android:description 引用）` | 假反诈安全 \| 良性透明说明（表面为疫情追踪功能说明，实为索取全局窗口读取权限的合理化包装） |
| en | Coronavirus Finder | Coronavirus Finder（新冠病毒查找器） | `res/values/strings.xml#app_name（同时用作 application label 与无障碍 service label）` | 假更新 \| 良性透明说明（以疫情追踪工具身份作为整体伪装，服务名与桌面名一致以消除系统列表中的辨识线索） |
| en | Verify Payment Method | 验证支付方式 | `res/values/strings.xml#button_text（配合 res/layout/google_alert.xml、res/drawable-v24/gpay_logo.png）` | 假反诈安全 \| 未知（伪造 Google Play 支付验证界面，属获权后的凭证窃取环节） |
| en | Google Play Logo | Google Play 标志 | `res/values/strings.xml#image_alt` | 未知（品牌仿冒素材的无障碍替代文本） |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：无法静态确认。可静态支撑的结构性线索：ActivityEnableAccessibility 使用独立 taskAffinity=com.a1，ActivityShowAlert 与 ActivityWebViewPush 均为 noHistory+excludeFromRecents（可反复拉起且不留最近任务记录），ActivityAllPermissions/ActivityPlayProtect 为 clearTaskOnLaunch=true，并存在 _ServiceRestartReceiver（label=RestartServiceWhenStopped）与 InitService/GlobalService 常驻服务；具体 onResume 重跳或定时器逻辑位于加密载荷 db_dex.nmp 解密后的 DEX。
- **遮罩叠层 / 高仿系统设置页**：未在静态可见范围内发现 SYSTEM_ALERT_WINDOW 权限或高仿系统无障碍开关页；但存在 res/layout/webview_small.xml（内嵌 WebView 容器，可用于在系统设置页上方叠层展示网页引导）与 ActivityWebViewPush（noHistory），具体叠层/遮罩实现位于加密载荷中，静态不可判定。
- **Android 13+ 受限设置（Restricted Settings）应对**：无法静态确认；Manifest 中仅可见 ActivityPlayProtect（clearTaskOnLaunch=true、taskAffinity=com.a3）与 ActivityAllPermissions 等权限流水线组件，其文案与分步教学逻辑在加密载荷内。
- **获权后即时行为与防撤权机制**：无法静态确认；静态仅可见 _ServiceRestartReceiver（BOOT_COMPLETED/QUICKBOOT_POWERON/PACKAGE_REPLACED 优先级 990）与 InitService/GlobalService 用于保活，未在可见代码中发现 GLOBAL_ACTION_BACK/HOME 阻止撤权或自点确认的实现。
- **良性降级 / 替代方案**：无。应用无任何替代路径或降级模式证据；无障碍说明文案直接以“不开启即无法完整使用应用”为条件施压，而非提供手动模式。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：由于一阶段 Application 会在 attachBaseContext 解密载荷，建议在冷启动后即以 1 秒间隔轮询当前前台窗口：一旦出现 ActivityEnableAccessibility（taskAffinity com.a1）、ActivityPermission/ActivityAllPermissions/ActivityDozeAndPermissions，或前台包名变为 com.android.settings 且界面含 accessibility 关键字，立即抓取该帧及其后 800ms 内的压栈页面。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区：一阶段 classes.dex 不含任何引导 UI 代码，全部引导逻辑位于 assets/db_dex.nmp 加密载荷，静态无法确认跳转 Intent、拒权循环与叠层实现，必须以运行期 UTG 补齐；此外无障碍配置 serviceconfig.xml 极简（仅 canRetrieveWindowContent），系统列表中的说明可能因长度被截断而弱化警示；若第二阶段进一步下发远端 HTML/配置控制引导文案，则 UTG 需同步抓取 WebView 加载的 URL。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导说明页（跳设置前的教学页）** | Activity 名 ActivityEnableAccessibility，任务栈 affinity=com.a1，界面含 'Coronavirus Finder requires accessibility access' 与开启/确认按钮 | 这是判定“是否以疫情追踪为名诱导开启无障碍”的直接界面证据，也是文案与按钮是否可取消的唯一运行时来源 | 页面标题/正文文本与 accessibility_description 是否一致；是否存在取消/跳过/稍后按钮；是否同时出现权限列表或支付相关控件；Activity 组件名与 taskAffinity 是否可读取 |
| **系统无障碍服务列表项** | Settings 无障碍页中名为 'Coronavirus Finder' 的条目及其开关、说明摘要 | 证明服务名与桌面名同名的身份混淆，并确认应用确实跳转 ACTION_ACCESSIBILITY_SETTINGS 而非自绘假开关页 | 列表条目显示名与桌面名是否完全一致；条目说明文本是否被截断/含换行分段；是否为真实系统设置页（包名 com.android.settings） |
| **设置页后压栈的遮罩/引导层** | 从 Settings 返回或停留时，栈顶出现 ActivityWebViewPush（noHistory）或 webview_small 布局的 WebView、或 ActivityShowAlert 弹窗 | 识别是否存在叠层指引或拒权后强制重跳，这是区分'一次性说明'与'强制胁迫'的关键 | 设置页上方是否出现应用自身的悬浮/全屏遮罩；WebView 加载的是本地 asset 还是远端 URL；返回键后 1-3 秒内是否被重新拉回设置页；同一 Activity 是否被反复重建 |
| **获权后动作（伪造支付页）** | ActivityShowAlert / ActivityWebViewPush 展示含 'Verify Payment Method' 按钮与 Google Play 标志的界面（google_alert.xml 布局） | 把“无障碍诱导”与“支付凭证窃取”因果闭合，确认权限索取的真实目的 | 按钮文本 'Verify Payment Method'；是否出现卡号/验证码输入框；是否由目标银行/钱包类前台应用触发（无障碍读取窗口后注入） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `bgmqkf.xpybwomhl.ljpfhtxfxx.Scameramention.attachBaseContext（一阶段载荷解密入口）`
- `bgmqkf.xpybwomhl.ljpfhtxfxx.Ralphalunar.doublefind（反射读取 AssetManager 加密流并落盘）`
- `bgmqkf.xpybwomhl.ljpfhtxfxx.Gmomentprice.aboutelectric（Class.forName 反射设置 DexClassLoader 路径）`
- `AndroidManifest.xml: zsezrfpgojacmkyfhbotthbkgi.zqzngmsqlapqqoxfwweuoui.qfulgeigxoyklbrciyug.ServiceAccessibility / ActivityEnableAccessibility(taskAffinity=com.a1)`
- `res/xml/serviceconfig.xml + res/values/strings.xml#accessibility_description`
- `assets/db_dex.nmp（加密二阶段 DEX，44,394 B）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**静态可见性：核心引导逻辑不可见（加密载荷）。** 已核实的事实链如下：

1. **`classes.dex` 只是第一阶段加载器，并不是真正的恶意主体。** `AndroidManifest.xml` 中声明的所有业务组件（无障碍服务、`ActivityEnableAccessibility`、`ActivityPermission`、`ActivityAllPermissions`、`ActivityDozeAndPermissions`、`ActivityPlayProtect`、`ActivityShowAlert`、`ActivityWebViewPush`、短信拦截等）都位于包 `zsezrfpgojacmkyfhbotthbkgi.zqzngmsqlapqqoxfwweuoui.qfulgeigxoyklbrciyug`，但该包在 [classes.dex](<resource-unit:#1.dex1 code:bgmqkf.xpybwomhl.ljpfhtxfxx.Scameramention>) 中**完全不存在**（813 个类只覆盖 `com`、`bgmqkf`、`frewbziejl` 等 5 个包）。
2. **载荷在 Application 启动的最早期被解密并写入磁盘。** [Scameramention.attachBaseContext()](<resource-unit:#1.dex1 code:bgmqkf.xpybwomhl.ljpfhtxfxx.Scameramention#attachBaseContext>) 依次调用 `wooddraft` 和 `glowliquid`（`context.getDir(...)` 私有目录）、`fingerhead`、`missneutral` 到 [Ralphalunar.doublefind()](<resource-unit:#1.dex1 code:bgmqkf.xpybwomhl.ljpfhtxfxx.Ralphalunar#doublefind>)。`doublefind` 通过 `getAssets()` 反射和 `AssetManager` 反射，把 asset 中的加密流复制到应用私有目录（缓冲区 3 MB），再通过 [Gmomentprice.aboutelectric()](<resource-unit:#1.dex1 code:bgmqkf.xpybwomhl.ljpfhtxfxx.Gmomentprice#aboutelectric>) 用 `Class.forName` 和字段反射设置加载器；源码中可见 `Ldalvik/system/DexClassLoader;` 常量。
3. **加密载荷候选文件已确认。** `assets/db_dex.nmp`（44,394 B）首字节为 `00 25 36 41 67 7f 48 54...`，完全无 DEX/ZIP 魔数；`assets/db_evoapk.dat` 首字节为 `41 76 61 73 74 56 70 73 45 41 31 2b`（"AvastVpsEA1+"，属 VPN 配置，非代码载荷）。
4. **无障碍身份伪装与文本载体已静态确认**：`app_name` = `Coronavirus Finder`（借疫情追踪类应用外壳）；无障碍服务 `android:label="@string/app_name"`（系统列表中显示同名）；`res/xml/serviceconfig.xml` 只声明 `canRetrieveWindowContent="true"`，且**未声明任何 `accessibilityFlags`、`canPerformGestures` 或事件类型**，属“空壳式”配置；说明文案为 `accessibility_description`；另有 `button_text` = `Verify Payment Method` 与 `res/drawable-v24/gpay_logo.png`（Google Play / GPay 支付页伪装素材），指向后续支付凭证窃取环节。
5. **无法静态核验的部分**：`ActivityEnableAccessibility` 等组件的 `onCreate`、`onResume` 跳转逻辑，`ACTION_ACCESSIBILITY_SETTINGS` 与 `ACTION_APPLICATION_DETAILS_SETTINGS` 调用点，引导弹窗与拒权重跳循环，以及叠层遮罩，全部位于 `db_dex.nmp` 解密后的 DEX 内。检索 `#1.dex1` 的 `accessibility`、`ACTION_ACCESSIBILITY_SETTINGS`、`APPLICATION_DETAILS_SETTINGS` 均无命中（`no_matches`）。因此，纯运行期 UTG 步骤只能给出**组件级预期**，不能给出方法级证据。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "AndroidManifest.xml 声明的全部业务组件（含无障碍服务与 ActivityEnableAccessibility/ActivityPermission/ActivityAllPermissions/ActivityDozeAndPermissions/ActivityPlayProtect/ActivityShowAlert/ActivityWebViewPush）所属包 zsezrfpgojacmkyfhbotthbkgi.zqzngmsqlapqqoxfwweuoui.qfulgeigxoyklbrciyug 在 classes.dex 中不存在（仅 5 个包、813 类，无该包）；真正的 DEX 以加密形态存于 assets/db_dex.nmp（44,394B，首字节 00 25 36 41 67 7f 48 54，无 dex/zip 魔数），由 Application.attachBaseContext 经 Ralphalunar.doublefind 反射读取 AssetManager 解密落盘后动态加载，故无障碍引导的页面流转、跳转 Intent 与拒权循环逻辑均不可静态还原；仅 Manifest 组件声明、strings.xml 文案与 serviceconfig.xml 配置可见。",
  "summary_one_liner": "以“Coronavirus Finder”疫情追踪为外壳的银行木马，第一阶段 Application 在 attachBaseContext 解密 assets/db_dex.nmp 并动态加载第二阶段 DEX，第二阶段才实现无障碍开启引导与后续支付页伪装；引导页实现本身完全藏在加密载荷中，静态仅可见同名无障碍服务与“需要无障碍以检测感染者位置”的说明文案。",
  "disguise_identity": {
    "app_display_name": "Coronavirus Finder",
    "claimed_brand_or_persona": "Coronavirus Finder（疫情/感染者位置追踪工具）；同时准备 Google Play / GPay 支付页面伪装素材（button_text=Verify Payment Method、gpay_logo.png）",
    "a11y_service_label": "Coronavirus Finder（service 的 android:label=@string/app_name，与桌面名完全一致）",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 无障碍服务 label 复用 @string/app_name，使系统无障碍列表条目与桌面应用名完全一致，用户无法从名称分辨；2) 说明文案首句为 'Coronavirus Finder requires accessibility access in order to automatically detect and display locations of infected people around.'，第二句另起一行并以换行+空行隔开 'Please, enable it to fully integrate the Application.'，利用换行把“系统警告式说明”与真实索取意图分离（strings.xml 中保留原始 \\n 换行）；3) 全部业务组件置于同一长随机包名下并按 taskAffinity=com.a1/a2/a3/a4 分任务栈，ActivityEnableAccessibility 单独 taskAffinity=com.a1，便于从任意栈顶拉起且不暴露于最近任务（MainActivity、ActivityPermission、ActivityShowAlert 等均 excludeFromRecents/noHistory）；4) 类名/方法名整体随机化（Rcaveoxygen、Quncoversize 等 60+ 随机 Activity 作为噪声掩护），并用大量无效算术、循环与字段读写做控制流/死代码混淆；5) res/xml/serviceconfig.xml 仅声明 canRetrieveWindowContent，未声明 accessibilityFlags/事件类型，说明配置极简，真实能力由运行时第二阶段代码自设。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "bgmqkf.xpybwomhl.ljpfhtxfxx.Scameramention（Application，android:name 声明）→ 私有目录中解密落盘的二阶段 DEX",
      "trigger_event": "进程创建时 attachBaseContext(Context) 被系统回调",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "该阶段无界面，仅完成载荷解密与动态加载",
      "user_action_requested": "无（用户无感知）",
      "code_anchor": "bgmqkf.xpybwomhl.ljpfhtxfxx.Scameramention.attachBaseContext → Ralphalunar.doublefind / Gmomentprice.aboutelectric；assets/db_dex.nmp"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "zsezrfpgojacmkyfhbotthbkgi.zqzngmsqlapqqoxfwweuoui.qfulgeigxoyklbrciyug.ActivityEnableAccessibility（taskAffinity=com.a1，无 label，无 excludeFromRecents）",
      "trigger_event": "无法静态确认（组件在加密载荷中实现；推测由二阶段 DEX 在主界面或权限流水线后拉起）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Coronavirus Finder requires accessibility access in order to automatically detect and display locations of infected people around. \nPlease, enable it to fully integrate the Application.",
      "shown_text_zh": "Coronavirus Finder 需要无障碍权限，以便自动检测并显示周围感染者的位置。请开启该权限，以便完整使用本应用。",
      "user_action_requested": "无法静态确认（该 Activity 无 label，可能为引导说明+确认按钮；是否有取消/跳过按钮不可见）",
      "code_anchor": "AndroidManifest.xml: <activity android:name=\"...ActivityEnableAccessibility\" android:taskAffinity=\"com.a1\"/>；res/values/strings.xml#accessibility_description；res/xml/serviceconfig.xml"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统 Settings.ACTION_ACCESSIBILITY_SETTINGS 无障碍服务列表（目标条目 label = Coronavirus Finder）",
      "trigger_event": "无法静态确认（推测为 ActivityEnableAccessibility 内点击按钮后 startActivity(Intent(ACTION_ACCESSIBILITY_SETTINGS))）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Coronavirus Finder",
      "shown_text_zh": "系统无障碍服务列表中显示的应用/服务名（与桌面显示名一致）",
      "user_action_requested": "用户需在系统列表中手动找到并开启名为 Coronavirus Finder 的无障碍服务",
      "code_anchor": "AndroidManifest.xml: <service ...ServiceAccessibility android:label=\"@string/app_name\"> + <meta-data android:name=\"android.accessibilityservice\" android:resource=\"@xml/serviceconfig\"/>；res/xml/serviceconfig.xml"
    },
    {
      "step": 4,
      "stage": "跳受限设置（应用详情）",
      "screen_or_component": "系统 Settings.ACTION_APPLICATION_DETAILS_SETTINGS 应用详情页；伴随 ActivityPermission（noHistory=true、excludeFromRecents）、ActivityAllPermissions（clearTaskOnLaunch、taskAffinity=com.a4）、ActivityDozeAndPermissions（taskAffinity=com.a2）等权限流水线 Activity",
      "trigger_event": "无法静态确认",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "静态仅见组件声明与权限组合（CALL_PHONE/READ_SMS/RECEIVE_SMS/SEND_SMS/READ_CONTACTS/REQUEST_IGNORE_BATTERY_OPTIMIZATIONS），页面文案与 13+ 受限设置教学代码均在加密载荷中",
      "user_action_requested": "无法静态确认（疑似要求用户在应用详情中授予短信/电话/通讯录权限并忽略电池优化）",
      "code_anchor": "AndroidManifest.xml: ActivityPermission / ActivityAllPermissions / ActivityDozeAndPermissions / ActivityPlayProtect；uses-permission 列表"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "无法静态确认（ActivityShowAlert（noHistory、excludeFromRecents）与 ActivityWebViewPush 为候选载体）",
      "trigger_event": "无法静态确认（可能为 onResume 检测服务未启用后重跳）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无静态文本证据；只能确认存在可反复拉起的无历史 Activity 与多个独立 taskAffinity",
      "user_action_requested": "无法静态确认",
      "code_anchor": "AndroidManifest.xml: ActivityShowAlert / ActivityWebViewPush / ActivityEnableAccessibility(taskAffinity=com.a1)"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "zsezrfpgojacmkyfhbotthbkgi.zqzngmsqlapqqoxfwweuoui.qfulgeigxoyklbrciyug.ServiceAccessibility（canRetrieveWindowContent=true）+ ServiceSendSMS / ServiceHiddenSMS / ServiceSMSPermissions / ReceiverIncomingSms(priority 998) / ActivityGenerateFakeSMS / ActivityInjectionPhoto / ActivityChangeSmsManager",
      "trigger_event": "无障碍服务被系统绑定后回调 onServiceConnected（实现不可见）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Verify Payment Method",
      "shown_text_zh": "“验证支付方式”（strings.xml button_text，配合 res/drawable-v24/gpay_logo.png 与 res/layout/google_alert.xml 构建的伪造 Google Play/GPay 支付页）",
      "user_action_requested": "无法静态确认（疑似诱导在伪造支付页输入卡号/验证码）",
      "code_anchor": "res/values/strings.xml#button_text；res/layout/google_alert.xml；res/layout/webview_small.xml；AndroidManifest.xml 短信/无障碍服务声明"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表条目名称：android:label=\"@string/app_name\" = \"Coronavirus Finder\"（与桌面图标名完全一致，无任何服务专属后缀）",
    "系统无障碍服务说明：res/xml/serviceconfig.xml 的 android:description=\"@string/accessibility_description\"，即 \"Coronavirus Finder requires accessibility access in order to automatically detect and display locations of infected people around.\\nPlease, enable it to fully integrate the Application.\"（含换行分隔）",
    "应用内引导说明页：ActivityEnableAccessibility（taskAffinity=com.a1）—— 该 Activity 无 label，具体布局/弹窗实现位于加密载荷 assets/db_dex.nmp 解密后的 DEX，静态不可见",
    "权限/优化提示流水线：ActivityPermission（noHistory、excludeFromRecents）、ActivityAllPermissions（clearTaskOnLaunch）、ActivityDozeAndPermissions、ActivityPlayProtect —— 文案不可静态还原",
    "告警/推送类承载：ActivityShowAlert（noHistory、excludeFromRecents）、ActivityWebViewPush（noHistory）、res/layout/webview_small.xml（内嵌 WebView 容器，加载地址不可静态还原）",
    "支付凭证页素材：res/values/strings.xml 的 button_text=\"Verify Payment Method\"、image_alt=\"Google Play Logo\"，配合 res/drawable-v24/gpay_logo.png 与 res/layout/google_alert.xml",
    "本地 HTML 仅为合规外壳（assets/consent_policy.html = Avast Software s.r.o. 同意政策；assets/eula.html = 2018 版 EULA），与本应用引导无关，属借用第三方模板的噪声/伪装素材"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Coronavirus Finder requires accessibility access in order to automatically detect and display locations of infected people around. \nPlease, enable it to fully integrate the Application.",
      "text_zh": "Coronavirus Finder 需要无障碍权限，以便自动检测并显示周围感染者的位置。请开启该权限，以便完整使用本应用。",
      "source_location": "res/values/strings.xml#accessibility_description（由 res/xml/serviceconfig.xml 的 android:description 引用）",
      "rhetorical_frame": "假反诈安全 | 良性透明说明（表面为疫情追踪功能说明，实为索取全局窗口读取权限的合理化包装）"
    },
    {
      "lang": "en",
      "text_verbatim": "Coronavirus Finder",
      "text_zh": "Coronavirus Finder（新冠病毒查找器）",
      "source_location": "res/values/strings.xml#app_name（同时用作 application label 与无障碍 service label）",
      "rhetorical_frame": "假更新 | 良性透明说明（以疫情追踪工具身份作为整体伪装，服务名与桌面名一致以消除系统列表中的辨识线索）"
    },
    {
      "lang": "en",
      "text_verbatim": "Verify Payment Method",
      "text_zh": "验证支付方式",
      "source_location": "res/values/strings.xml#button_text（配合 res/layout/google_alert.xml、res/drawable-v24/gpay_logo.png）",
      "rhetorical_frame": "假反诈安全 | 未知（伪造 Google Play 支付验证界面，属获权后的凭证窃取环节）"
    },
    {
      "lang": "en",
      "text_verbatim": "Google Play Logo",
      "text_zh": "Google Play 标志",
      "source_location": "res/values/strings.xml#image_alt",
      "rhetorical_frame": "未知（品牌仿冒素材的无障碍替代文本）"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "无法静态确认。可静态支撑的结构性线索：ActivityEnableAccessibility 使用独立 taskAffinity=com.a1，ActivityShowAlert 与 ActivityWebViewPush 均为 noHistory+excludeFromRecents（可反复拉起且不留最近任务记录），ActivityAllPermissions/ActivityPlayProtect 为 clearTaskOnLaunch=true，并存在 _ServiceRestartReceiver（label=RestartServiceWhenStopped）与 InitService/GlobalService 常驻服务；具体 onResume 重跳或定时器逻辑位于加密载荷 db_dex.nmp 解密后的 DEX。",
    "overlay_or_fake_settings": "未在静态可见范围内发现 SYSTEM_ALERT_WINDOW 权限或高仿系统无障碍开关页；但存在 res/layout/webview_small.xml（内嵌 WebView 容器，可用于在系统设置页上方叠层展示网页引导）与 ActivityWebViewPush（noHistory），具体叠层/遮罩实现位于加密载荷中，静态不可判定。",
    "restricted_settings_13plus_coaching": "无法静态确认；Manifest 中仅可见 ActivityPlayProtect（clearTaskOnLaunch=true、taskAffinity=com.a3）与 ActivityAllPermissions 等权限流水线组件，其文案与分步教学逻辑在加密载荷内。",
    "post_grant_anti_removal": "无法静态确认；静态仅可见 _ServiceRestartReceiver（BOOT_COMPLETED/QUICKBOOT_POWERON/PACKAGE_REPLACED 优先级 990）与 InitService/GlobalService 用于保活，未在可见代码中发现 GLOBAL_ACTION_BACK/HOME 阻止撤权或自点确认的实现。",
    "benign_graceful_degradation": "无。应用无任何替代路径或降级模式证据；无障碍说明文案直接以“不开启即无法完整使用应用”为条件施压，而非提供手动模式。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "由于一阶段 Application 会在 attachBaseContext 解密载荷，建议在冷启动后即以 1 秒间隔轮询当前前台窗口：一旦出现 ActivityEnableAccessibility（taskAffinity com.a1）、ActivityPermission/ActivityAllPermissions/ActivityDozeAndPermissions，或前台包名变为 com.android.settings 且界面含 accessibility 关键字，立即抓取该帧及其后 800ms 内的压栈页面。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导说明页（跳设置前的教学页）",
        "page_identifier": "Activity 名 ActivityEnableAccessibility，任务栈 affinity=com.a1，界面含 'Coronavirus Finder requires accessibility access' 与开启/确认按钮",
        "why_most_useful": "这是判定“是否以疫情追踪为名诱导开启无障碍”的直接界面证据，也是文案与按钮是否可取消的唯一运行时来源",
        "observable_utg_signals": ["页面标题/正文文本与 accessibility_description 是否一致", "是否存在取消/跳过/稍后按钮", "是否同时出现权限列表或支付相关控件", "Activity 组件名与 taskAffinity 是否可读取"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍页中名为 'Coronavirus Finder' 的条目及其开关、说明摘要",
        "why_most_useful": "证明服务名与桌面名同名的身份混淆，并确认应用确实跳转 ACTION_ACCESSIBILITY_SETTINGS 而非自绘假开关页",
        "observable_utg_signals": ["列表条目显示名与桌面名是否完全一致", "条目说明文本是否被截断/含换行分段", "是否为真实系统设置页（包名 com.android.settings）"]
      },
      {
        "page_role": "设置页后压栈的遮罩/引导层",
        "page_identifier": "从 Settings 返回或停留时，栈顶出现 ActivityWebViewPush（noHistory）或 webview_small 布局的 WebView、或 ActivityShowAlert 弹窗",
        "why_most_useful": "识别是否存在叠层指引或拒权后强制重跳，这是区分'一次性说明'与'强制胁迫'的关键",
        "observable_utg_signals": ["设置页上方是否出现应用自身的悬浮/全屏遮罩", "WebView 加载的是本地 asset 还是远端 URL", "返回键后 1-3 秒内是否被重新拉回设置页", "同一 Activity 是否被反复重建"]
      },
      {
        "page_role": "获权后动作（伪造支付页）",
        "page_identifier": "ActivityShowAlert / ActivityWebViewPush 展示含 'Verify Payment Method' 按钮与 Google Play 标志的界面（google_alert.xml 布局）",
        "why_most_useful": "把“无障碍诱导”与“支付凭证窃取”因果闭合，确认权限索取的真实目的",
        "observable_utg_signals": ["按钮文本 'Verify Payment Method'", "是否出现卡号/验证码输入框", "是否由目标银行/钱包类前台应用触发（无障碍读取窗口后注入）"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区：一阶段 classes.dex 不含任何引导 UI 代码，全部引导逻辑位于 assets/db_dex.nmp 加密载荷，静态无法确认跳转 Intent、拒权循环与叠层实现，必须以运行期 UTG 补齐；此外无障碍配置 serviceconfig.xml 极简（仅 canRetrieveWindowContent），系统列表中的说明可能因长度被截断而弱化警示；若第二阶段进一步下发远端 HTML/配置控制引导文案，则 UTG 需同步抓取 WebView 加载的 URL。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "bgmqkf.xpybwomhl.ljpfhtxfxx.Scameramention.attachBaseContext（一阶段载荷解密入口）",
    "bgmqkf.xpybwomhl.ljpfhtxfxx.Ralphalunar.doublefind（反射读取 AssetManager 加密流并落盘）",
    "bgmqkf.xpybwomhl.ljpfhtxfxx.Gmomentprice.aboutelectric（Class.forName 反射设置 DexClassLoader 路径）",
    "AndroidManifest.xml: zsezrfpgojacmkyfhbotthbkgi.zqzngmsqlapqqoxfwweuoui.qfulgeigxoyklbrciyug.ServiceAccessibility / ActivityEnableAccessibility(taskAffinity=com.a1)",
    "res/xml/serviceconfig.xml + res/values/strings.xml#accessibility_description",
    "assets/db_dex.nmp（加密二阶段 DEX，44,394 B）"
  ]
}
```

</details>
