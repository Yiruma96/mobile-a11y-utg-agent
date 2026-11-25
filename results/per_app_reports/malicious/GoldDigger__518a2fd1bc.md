# MB_062__518a2fd1bc｜GoldDigger — PEA SMART PRO

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：149.9s

## 1. 一句话核心结论

- **核心申请方式**：以泰国电力局官方 App『PEA SMART PRO』身份伪装，在无障碍配置中伪造 isAccessibilityTool=true 隐藏系统隐私警告，再用泰文隐私承诺话术把用户引向无障碍开关，真实引导逻辑封装在 assets 内加密载荷中。
- **静态可见性说明**：Manifest、无障碍配置 XML、资源字符串与透明/别名组件声明完整静态可见；但业务实现整体被抽取：classes.dex 仅剩 com.nashsiqiu.shell.ProxyApplication 壳类，无任何 c56ddef9… 业务类与 ACCESSIBILITY_SETTINGS 字符串，真实代码存放于加密载荷 assets/OoooooOooo（1.98MB，非 dex 魔数）并由 assets/vwwwwwvwww/{arch}/libdpt.so 解密加载，assets/app_name 仅存真实 Application 类名。因此引导弹窗、跳设置 Intent、onResume 拒权循环、获权后自动点击等运行期页面流转逻辑无法静态还原。
- **命中的行为模式标签**：`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_FAKE_IS_ACCESSIBILITY_TOOL`（伪造android:isAccessibilityTool="true"）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `518a2fd1bca2e4c5d4db5f41c0230f0986ce3ca3bbdc4d1b211a949b0631abb7` |
| 包名 / 年份 | `com.lavju.pigfcb.lrymx.lhl` / 2025 |
| 家族 / 品类 | **GoldDigger**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | PEA SMART PRO |
| 引导页宣称品牌/身份 | 泰国地方电力局（การไฟฟ้าส่วนภูมิภาค / PEA）官方应用程序 PEA SMART PRO |
| 系统无障碍列表服务名 | PEA SMART PRO |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 无障碍配置 android:isAccessibilityTool="true" 伪造系统无障碍工具标记，规避 Android 13+ 隐私警告与受限设置二次确认；2) activity-alias 多别名：asd.fgh.component.AliasTmpActivity 的 android:label="\u2064"（U+2064 不可见填充字符），AliasGoogleActivity/AliasActivity 可切换为空白或他人图标名称；3) asd.fgh.thaw.TA/BA 为全透明、immersive、excludeFromRecents、taskAffinity=:TA 的隐身 Activity；4) TransplentPermissionActivity 透明主题+noHistory+singleTask+excludeFromRecents，用于无痕跳转与回跳；5) 无障碍说明仅提供泰文，且中文/繁体权限教学文案混排；6) 四个 ABI 的 libdpt.so 被伪装存放在 assets/ 而非 lib/，规避常规 so 扫描；7) 真实 Application 类名不写入 Manifest 而藏于 assets/app_name。 |
| 无障碍服务类名 | `c56ddef9ebb3c4be8ba7cf6c2f70f7be5.c43e95c997cf14b07966e5119de1a1367.c89a2b2ed4b964162b044e43f5a1cfca2.service.FocusService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=True` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | เป็น Application ของการไฟฟ้าส่วนภูมิภาค ที่ผ่านการตรวจสอบเเล้ว ต้องได้รับอนุญาตจากการเข้าถึง ข้อเเนะนำ:เมื่อคุณเปิดสวิตซ์ฟังก์ชั่นรักษาความปลอดภัยแล้ว คุณจะได้รับการเเจ้งเตือนจากระบบ PEA SMART PRO ยืนยันจะไม่ละเมิดสิทธิส่วนบุคคลของผู้ใช้ โปรดวางใจในการเปิดใช้งาน |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | c56ddef9ebb3c4be8ba7cf6c2f70f7be5.c43e95c997cf14b07966e5119de1a1367.c89a2b2ed4b964162b044e43f5a1cfca2.ui.SplashActivity（MAIN/LAUNCHER，exported=true） | 点击桌面图标 → onCreate | 原生Activity | **原文**：无（Splash 文案在加密载荷内，静态不可读）<br>**译注**：启动画面，具体文案不可静态还原 | 无，自动跳转 | `#1 manifest:components → ui.SplashActivity；实际跳转逻辑位于 assets/OoooooOooo（加密）` |
| 2 | 引导说明页 | 无障碍服务说明（系统无障碍列表条目）+ 推测为 ui.ActivationActivity / ui.WaitCheckActivity / ui.CheckPermissionActivity 承接引导 | 冷启动或业务功能触发后进入授权引导（具体触发点不可静态还原） | 系统无障碍页（android:description 文本）+ 原生Activity（内容不可静态还原） | **原文**：เป็น Application ของการไฟฟ้าส่วนภูมิภาค ที่ผ่านการตรวจสอบเเล้ว ต้องได้รับอนุญาตจากการเข้าถึง ข้อเเนะนำ:เมื่อคุณเปิดสวิตซ์ฟังก์ชั่นรักษาความปลอดภัยแล้ว คุณจะได้รับการเเจ้งเตือนจากระบบ PEA SMART PRO ยืนยันจะไม่ละเมิดสิทธิส่วนบุคคลของผู้ใช้ โปรดวางใจในการเปิดใช้งาน<br>**译注**：这是泰国地方电力局（PEA）已通过审核的 Application，必须获得访问授权。提示：当您打开安全功能开关后，您将收到来自 PEA SMART PRO 系统的通知。我们确认不会侵犯用户的个人隐私，请放心开启使用。 | 要求用户去开启无障碍开关（是否存在取消/跳过按钮不可静态还原） | `#1 manifest:components（service FocusService meta-data android:accessibilityservice=@7F13000F）；#1 file:res/values/public.xml/touch_accessibility_service_config.xml（android:description=@7F10001B）` |
| 3 | 跳无障碍设置 | 系统设置 → 无障碍 → 已下载的服务 → PEA SMART PRO（Settings$AccessibilitySettings / InstalledAccessibilityDetailsSettings） | 代码内 startActivity(ACTION_ACCESSIBILITY_SETTINGS)（跳转点位于加密载荷内，未取得静态调用证据） | 系统无障碍页 | **原文**：PEA SMART PRO（服务名）<br>**译注**：系统无障碍列表中显示的服务名，与桌面名完全一致，伪装为同一官方应用 | 用户在系统无障碍列表中点选 PEA SMART PRO 并打开开关；因 isAccessibilityTool=true，系统不会显示『此应用可查看屏幕内容/控制设备』的隐私警告页 | `#1 manifest:components（service …service.FocusService，permission=BIND_ACCESSIBILITY_SERVICE，exported=false）；#1 file:res/values/public.xml/touch_accessibility_service_config.xml（android:isAccessibilityTool="true"）` |
| 4 | 遮罩叠层指引 | c56ddef9…ui.TransplentPermissionActivity（透明主题、noHistory、singleTask、excludeFromRecents）+ 推测悬浮窗（SYSTEM_ALERT_WINDOW 已申请） | 跳转设置后返回或定时器拉起（逻辑不可静态还原） | 不可静态还原（透明 Activity 已声明，覆盖内容与是否绘制半透明遮罩无法从静态证据确认） | **原文**：无（不可静态还原）<br>**译注**：透明承接页，具体叠层文案不可静态还原 | 不可静态还原 | `#1 manifest:components（ui.TransplentPermissionActivity，theme=@7F110305，noHistory=true）` |
| 5 | 拒权反馈循环 | 不可静态还原（推测由透明 Activity + 前台服务重新拉起设置页） | 不可静态还原（未取得 onResume/Timer 代码证据） | 不可静态还原 | **原文**：1.取得权限失败，无法执行操作。<br><br>2.若因先前拒绝了权限授予，而没有出现权限请求画面，請至『設定→應用程式→當前App→權限』，將「%s」勾選允許。<br>**译注**：1. 获取权限失败，无法执行操作。2. 若因先前拒绝了权限授予而没有出现权限请求画面，请到『设置 → 应用程序 → 当前App → 权限』，将「%s」勾选允许。 | 按提示逐级进入应用详情页手动勾选权限（受限设置分步教学模板）；是否存在跳过按钮不可静态还原 | `resources.arsc 字符串（strings.xml 键，繁体/简体双版本）；assets/OoooooOooo（呈现位置加密）` |
| 6 | 获权后动作 | FocusService（AccessibilityService）+ record.DisplayService / ScreenRecordService / CameraService / AudioService / LiveKitService / RemoteService | 系统绑定无障碍服务后 onServiceConnected（代码在加密载荷内） | 不可静态还原 | 无 | 无需操作，服务静默运行 | `#1 manifest:components（service …service.FocusService；record.DisplayService/CameraService/AudioService/LiveKitService；ca0a8af8…record.ScreenRecordService）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表条目：服务名『PEA SMART PRO』（android:label=@7F100072，与桌面名 @7F100071 完全相同）
- 系统无障碍服务详情页说明区：泰文长文案（android:description=@7F10001B，内容见 verbatim_texts）
- 系统无障碍服务隐私提示页：因 isAccessibilityTool="true" 而被系统抑制，不再展示『可查看屏幕内容、控制设备』警告——这是本样本最关键的『少一步』设计
- 应用内权限失败提示（AlertDialog 或 Toast 形态，具体载体在加密载荷内）：繁体/简体双版本『取得权限失败，无法执行操作…請至『設定→應用程式→當前App→權限』』，用于把用户导向应用详情页/权限页
- 透明承接页 TransplentPermissionActivity（theme=@7F110305，noHistory，excludeFromRecents）：跳设置与回跳的过渡载体，用户无感知
- activity-alias 名称位：asd.fgh.component.AliasTmpActivity 的 android:label="\u2064"（不可见字符），可使桌面/列表项显示为空白
- assets/ 目录内可能存在的本地引导页资源：未发现 .html/.js 引导页，引导 UI 由加密载荷动态构建或为原生布局

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| th | เป็น Application ของการไฟฟ้าส่วนภูมิภาค ที่ผ่านการตรวจสอบเเล้ว ต้องได้รับอนุญาตจากการเข้าถึง ข้อเเนะนำ:เมื่อคุณเปิดสวิตซ์ฟังก์ชั่นรักษาความปลอดภัยแล้ว คุณจะได้รับการเเจ้งเตือนจากระบบ PEA SMART PRO ยืนยันจะไม่ละเมิดสิทธิส่วนบุคคลของผู้ใช้ โปรดวางใจในการเปิดใช้งาน | 这是泰国地方电力局（PEA）已通过审核的 Application，必须获得访问授权。提示：当您打开安全功能开关后，您将收到来自 PEA SMART PRO 系统的通知。我们确认不会侵犯用户的个人隐私，请放心开启使用。 | `resources.arsc 字符串 @7F10001B（strings.xml），经无障碍服务配置 android:description 引用` | 假反诈安全 |
| zh-TW | 1.取得权限失败，无法执行操作。<br><br>2.若因先前拒绝了权限授予，而没有出现权限请求画面，請至『設定→應用程式→當前App→權限』，將「%s」勾選允許。 | 1. 获取权限失败，无法执行操作。2. 若因先前拒绝了权限授予而没有出现权限请求画面，请到『设置 → 应用程序 → 当前App → 权限』，将「%s」勾选允许。 | `resources.arsc / res/values/strings.xml（对应预筛 [DEFAULT] 条目）` | 受限设置分步教学 |
| zh-CN | 1.取得权限失败，无法执行操作。 2.若因先前拒绝了权限授予，而没有出现权限请求画面，请『设置 → 应用程序 → 当前App → 权限』，将「%s」勾选允许。 | 同义简体版本：获取权限失败，需手动到设置里为当前应用勾选对应权限。 | `resources.arsc / res/values/strings.xml` | 受限设置分步教学 |
| en | Background Services | 后台服务（用于把常驻/自启动包装成正常系统能力） | `resources.arsc 字符串（预筛 [DEFAULT] 条目）` | 未知 |
| en | Sorry, the page encountered a problem and needs to be closed | 抱歉，页面遇到问题需要关闭（故障恐吓式话术，可迫使重试） | `resources.arsc 字符串（预筛 [DEFAULT] 条目）` | 故障恐吓 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原。已确认存在 TransplentPermissionActivity（透明、noHistory、singleTask、excludeFromRecents）与已声明 SYSTEM_ALERT_WINDOW 权限，具备『跳设置后透明回跳 + 悬浮层重新拉起』的结构条件，但 onResume/Timer 重跳代码位于加密载荷 assets/OoooooOooo 内，未取得直接证据。
- **遮罩叠层 / 高仿系统设置页**：确认存在透明 Activity 承接页（TransplentPermissionActivity，theme=@7F110305，noHistory=true，excludeFromRecents=true）与 SYSTEM_ALERT_WINDOW 权限声明，具备遮罩/浮层能力；未发现高仿系统无障碍开关页的资源或布局证据。实际是否叠放半透明引导遮罩不可静态还原。
- **Android 13+ 受限设置（Restricted Settings）应对**：存在受限设置/权限分步教学文案模板：『請至『設定→應用程式→當前App→權限』，將「%s」勾選允許』（繁/简双版本）；但因无障碍配置声明 isAccessibilityTool="true"，Android 13+ 对『受限设置』的额外二次确认被系统自动跳过，实际上无需再教用户点右上角菜单允许受限设置。
- **获权后即时行为与防撤权机制**：不可静态还原。已确认无障碍服务声明 accessibilityFlags=0x5A（含 FILTER_KEY_EVENTS，可拦截返回键等按键事件）与 canPerformGestures=true（可模拟点击），具备阻止撤权/自动点确认的技术能力，但 GLOBAL_ACTION_BACK/HOME 阻止撤权的具体代码位于加密载荷内，未取得直接证据。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：最佳时机：监测到 startActivity 的 Intent 动作为 android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.APPLICATION_DETAILS_SETTINGS 的瞬间，以及紧随其后的透明 Activity（TransplentPermissionActivity）出现；由于该应用伪造 isAccessibilityTool=true，系统不会弹出隐私警告页，因此必须在『用户点击桌面图标后的前 3 秒内』开始逐帧 UTG 采样，以捕获引导弹窗与跳转前后的页面栈变化。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：1) 业务代码整体加密于 assets/OoooooOooo，由 assets 内的 libdpt.so 解密加载，静态无法确认跳转点与拒权循环实现；2) 无障碍配置伪造 isAccessibilityTool=true，使系统隐私警告页不出现，纯 UTG 采样若只盯『警告页』会漏检；3) activity-alias label 使用 U+2064 不可见字符，桌面/列表可能呈现空白名称，OCR 与文本比对易判为空；4) TransplentPermissionActivity 透明无内容，UTG 在该页可能只看到下层设置界面；5) 静态加壳本身不阻挡运行期 UTG，必须实际运行才能补齐流程。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后首个应用内引导页（SplashActivity → Activation/WaitCheck/CheckPermission 链）** | com.lavju.pigfcb.lrymx.lhl 的 Activity，界面含泰文/中文权限说明与单个『开启』类按钮，包名与 PEA 品牌文案同屏 | 决定该应用是冷启动即阻断诱导，还是功能触发式诱导，是判定诱导主动性的核心页面 | 页面文本是否含 PEA SMART PRO / การไฟฟ้าส่วนภูมิภาค 品牌词；是否存在取消/跳过/稍后按钮；页面是否不可返回（返回键被拦截或直接退出） |
| **跳转前引导/教学页** | 含『設定→應用程式→當前App→權限』或泰文开启指引文本的页面，或跳转前 800ms 内的最后一帧应用内界面 | 证明存在分步教学与话术包装，区分『透明说明』与『教唆开启高危权限』 | 文本中是否出现设置路径指引；是否出现隐私承诺语句（ไม่ละเมิดสิทธิส่วนบุคคล / 不会侵犯隐私）；是否出现安全/防盗/账户保护类恐吓词 |
| **系统无障碍服务列表项与详情页** | com.android.settings 无障碍列表中的『PEA SMART PRO』条目；详情页说明区泰文长文案 | 确认 isAccessibilityTool=true 导致的『隐私警告页缺失』效果，以及服务名与桌面名一致的伪装 | 列表中服务名文本；是否缺少『此服务可查看屏幕内容』警告段；详情页描述文本语言与内容 |
| **设置页返回后的叠层/回跳页** | TransplentPermissionActivity（透明无界面）或悬浮窗覆盖在系统设置之上 | 判定是否存在拒权循环重跳与遮罩叠层引导 | 返回后是否再次跳入设置（页面栈出现重复 settings Activity）；是否有半透明遮罩/悬浮层覆盖设置页；是否出现 GLOBAL_ACTION_BACK 导致设置页被自动退出 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `#1 manifest:components（service c56ddef9ebb3c4be8ba7cf6c2f70f7be5.c43e95c997cf14b07966e5119de1a1367.c89a2b2ed4b964162b044e43f5a1cfca2.service.FocusService，android:label=@7F100072，meta-data android:accessibilityservice=@7F13000F）`
- `#1 file:res/values/public.xml/touch_accessibility_service_config.xml（android:isAccessibilityTool="true"，accessibilityFlags="0x0000005A"，canPerformGestures="true"，android:description=@7F10001B）`
- `#1 manifest:components（activity …ui.TransplentPermissionActivity，theme=@7F110305，noHistory=true，excludeFromRecents=true；activity-alias asd.fgh.component.AliasTmpActivity android:label="⁤"）`
- `#1 file:assets/OoooooOooo（1,979,518 字节加密载荷，真实业务代码载体）`
- `#1 file:assets/app_name（存放真实 Application 类名 c56ddef9…c89a2b2ed4b964162b044e43f5a1cfca2.App）`
- `#1.dex1 code:com.nashsiqiu.shell.ProxyApplication（壳 Application，Manifest android:name 指向）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 一、结论要点

**静态可见性：`packed_or_encrypted`（真实代码不在 DEX 内）**

1. **`classes.dex` 是壳，不是业务代码**：`classes.dex` 只包含 `com.nashsiqiu.shell.ProxyApplication`（`android:name` 指向它），全文检索 `c56ddef9…`、`FocusService`、`ACCESSIBILITY_SETTINGS`、`PEA SMART PRO` 均为 **0 命中**。真实实现位于 [assets/OoooooOooo](<resource-unit:#1 file:assets/OoooooOooo>)（1,979,518 字节，头部为 `01 00 03 00 10 00…`，非 dex/zip 魔数，无 `dex\n` 特征，属加密载荷），配合 [assets/vwwwwwvwww/arm64/libdpt.so](<resource-unit:#1 file:assets/vwwwwwvwww/arm64/libdpt.so>)（四个 ABI 的 `.so` 被放进 `assets/` 而非 `lib/`，典型二阶段解密加载器）与 [assets/app_name](<resource-unit:#1 file:assets/app_name>)（仅存放真实 Application 类名 `c56ddef9…c89a2b2ed4b964162b044e43f5a1cfca2.App`）。**引导弹窗、跳转点、`onResume` 拒权循环等运行期 UI 流转逻辑全部位于该加密载荷内，静态不可还原。**

2. **无障碍配置本身已足以定性"诱导 + 伪装"**：从资源 `@7F13000F` 还原出的 [touch_accessibility_service_config.xml](<resource-unit:#1 file:res/values/public.xml/touch_accessibility_service_config.xml>) 声明
   `android:isAccessibilityTool="true"`、`accessibilityEventTypes="0xFFFFFFFF"`、`feedbackType="0xFFFFFFFF"`、`notificationTimeout="10"`、`accessibilityFlags="0x0000005A"`（含 `REPORT_VIEW_IDS`+`FILTER_KEY_EVENTS`+`ENHANCED_WEB_ACCESSIBILITY`+`TOUCH_EXPLORATION`）、`canRetrieveWindowContent="true"`、`canPerformGestures="true"`。
   - `isAccessibilityTool="true"` 是**伪造"系统无障碍工具"标记**：Android 13+ 会据此隐藏"此服务可查看屏幕内容、控制设备"的隐私警告，并跳过"受限设置"二次确认流程，使诱导页面无需任何"分步教学"即可一键开启；同时规避应用商店对无障碍滥用的审查。
   - `0xFFFFFFFF` 全事件 + 10ms 超时 + `canPerformGestures` 表明其目标是**全量读屏 + 模拟手势自动点击**（非辅助残障用途）。

3. **身份伪装链完整**：桌面 `android:label=@7F100071` 与无障碍服务 `android:label=@7F100072` 均为 **"PEA SMART PRO"**，无障碍说明为泰文，自称"泰国地方电力局（การไฟฟ้าส่วนภูมิภาค）已通过审核的官方 Application"，并以"不侵犯个人隐私、请放心开启"作隐私承诺——**与真实 PEA 官方应用无关的第三方包名 `com.lavju.pigfcb.lrymx.lhl`**。

4. **同类隐身手法并行存在**：[AndroidManifest.xml](<resource-unit:#1 manifest:components>) 中 `asd.fgh.thaw.TA/BA` 为全透明、`excludeFromRecents`、`immersive` 的 Activity；`asd.fgh.component.AliasTmpActivity` 的 `android:label="⁤"`（U+2064 不可见填充字符），配合 `activity-alias` 多别名切换，可在设置页/无障碍列表/桌面上呈现为空白或他人名称；`TransplentPermissionActivity`（透明主题、`noHistory`、`singleTask`、`excludeFromRecents`）用于无痕承接跳转与回跳。设备采集侧还有 `DisplayService`/`ScreenRecordService`/`CameraService`/`AudioService`/`FaceActivity`/`UploadIDPhotosActivity`（人脸 + 证件采集），符合 GoldDigger 家族的银行木马画像。

5. **可见的"教用户去设置里开权限"文案确实存在**：字符串资源中含繁体中文"1.取得权限失败，无法执行操作…請至『設定→應用程式→當前App→權限』，將「%s」勾選允許。"及简体版本，属典型的**受限设置分步教学**话术模板；但其**呈现在哪个 Activity / 是否不可取消 / 是否有 onResume 拒权循环，因代码在加密载荷内而无法静态确认**。

> 覆盖边界：`assets/OoooooOooo` 为加密载荷（静态还原需 `libdpt.so` 解密流程，超出本次 14 次调用预算），`ACTION_ACCESSIBILITY_SETTINGS` / `ACTION_APPLICATION_DETAILS_SETTINGS` 的具体跳转代码、引导页文案与拒权循环逻辑均未取得静态证据；本次未进行动态运行验证。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "Manifest、无障碍配置 XML、资源字符串与透明/别名组件声明完整静态可见；但业务实现整体被抽取：classes.dex 仅剩 com.nashsiqiu.shell.ProxyApplication 壳类，无任何 c56ddef9… 业务类与 ACCESSIBILITY_SETTINGS 字符串，真实代码存放于加密载荷 assets/OoooooOooo（1.98MB，非 dex 魔数）并由 assets/vwwwwwvwww/{arch}/libdpt.so 解密加载，assets/app_name 仅存真实 Application 类名。因此引导弹窗、跳设置 Intent、onResume 拒权循环、获权后自动点击等运行期页面流转逻辑无法静态还原。",
  "summary_one_liner": "以泰国电力局官方 App『PEA SMART PRO』身份伪装，在无障碍配置中伪造 isAccessibilityTool=true 隐藏系统隐私警告，再用泰文隐私承诺话术把用户引向无障碍开关，真实引导逻辑封装在 assets 内加密载荷中。",
  "disguise_identity": {
    "app_display_name": "PEA SMART PRO",
    "claimed_brand_or_persona": "泰国地方电力局（การไฟฟ้าส่วนภูมิภาค / PEA）官方应用程序 PEA SMART PRO",
    "a11y_service_label": "PEA SMART PRO",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 无障碍配置 android:isAccessibilityTool=\"true\" 伪造系统无障碍工具标记，规避 Android 13+ 隐私警告与受限设置二次确认；2) activity-alias 多别名：asd.fgh.component.AliasTmpActivity 的 android:label=\"\\u2064\"（U+2064 不可见填充字符），AliasGoogleActivity/AliasActivity 可切换为空白或他人图标名称；3) asd.fgh.thaw.TA/BA 为全透明、immersive、excludeFromRecents、taskAffinity=:TA 的隐身 Activity；4) TransplentPermissionActivity 透明主题+noHistory+singleTask+excludeFromRecents，用于无痕跳转与回跳；5) 无障碍说明仅提供泰文，且中文/繁体权限教学文案混排；6) 四个 ABI 的 libdpt.so 被伪装存放在 assets/ 而非 lib/，规避常规 so 扫描；7) 真实 Application 类名不写入 Manifest 而藏于 assets/app_name。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "c56ddef9ebb3c4be8ba7cf6c2f70f7be5.c43e95c997cf14b07966e5119de1a1367.c89a2b2ed4b964162b044e43f5a1cfca2.ui.SplashActivity（MAIN/LAUNCHER，exported=true）",
      "trigger_event": "点击桌面图标 → onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（Splash 文案在加密载荷内，静态不可读）",
      "shown_text_zh": "启动画面，具体文案不可静态还原",
      "user_action_requested": "无，自动跳转",
      "code_anchor": "#1 manifest:components → ui.SplashActivity；实际跳转逻辑位于 assets/OoooooOooo（加密）"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "无障碍服务说明（系统无障碍列表条目）+ 推测为 ui.ActivationActivity / ui.WaitCheckActivity / ui.CheckPermissionActivity 承接引导",
      "trigger_event": "冷启动或业务功能触发后进入授权引导（具体触发点不可静态还原）",
      "ui_carrier": "系统无障碍页（android:description 文本）+ 原生Activity（内容不可静态还原）",
      "shown_text_verbatim": "เป็น Application ของการไฟฟ้าส่วนภูมิภาค ที่ผ่านการตรวจสอบเเล้ว ต้องได้รับอนุญาตจากการเข้าถึง ข้อเเนะนำ:เมื่อคุณเปิดสวิตซ์ฟังก์ชั่นรักษาความปลอดภัยแล้ว คุณจะได้รับการเเจ้งเตือนจากระบบ PEA SMART PRO ยืนยันจะไม่ละเมิดสิทธิส่วนบุคคลของผู้ใช้ โปรดวางใจในการเปิดใช้งาน",
      "shown_text_zh": "这是泰国地方电力局（PEA）已通过审核的 Application，必须获得访问授权。提示：当您打开安全功能开关后，您将收到来自 PEA SMART PRO 系统的通知。我们确认不会侵犯用户的个人隐私，请放心开启使用。",
      "user_action_requested": "要求用户去开启无障碍开关（是否存在取消/跳过按钮不可静态还原）",
      "code_anchor": "#1 manifest:components（service FocusService meta-data android:accessibilityservice=@7F13000F）；#1 file:res/values/public.xml/touch_accessibility_service_config.xml（android:description=@7F10001B）"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已下载的服务 → PEA SMART PRO（Settings$AccessibilitySettings / InstalledAccessibilityDetailsSettings）",
      "trigger_event": "代码内 startActivity(ACTION_ACCESSIBILITY_SETTINGS)（跳转点位于加密载荷内，未取得静态调用证据）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "PEA SMART PRO（服务名）",
      "shown_text_zh": "系统无障碍列表中显示的服务名，与桌面名完全一致，伪装为同一官方应用",
      "user_action_requested": "用户在系统无障碍列表中点选 PEA SMART PRO 并打开开关；因 isAccessibilityTool=true，系统不会显示『此应用可查看屏幕内容/控制设备』的隐私警告页",
      "code_anchor": "#1 manifest:components（service …service.FocusService，permission=BIND_ACCESSIBILITY_SERVICE，exported=false）；#1 file:res/values/public.xml/touch_accessibility_service_config.xml（android:isAccessibilityTool=\"true\"）"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "c56ddef9…ui.TransplentPermissionActivity（透明主题、noHistory、singleTask、excludeFromRecents）+ 推测悬浮窗（SYSTEM_ALERT_WINDOW 已申请）",
      "trigger_event": "跳转设置后返回或定时器拉起（逻辑不可静态还原）",
      "ui_carrier": "不可静态还原（透明 Activity 已声明，覆盖内容与是否绘制半透明遮罩无法从静态证据确认）",
      "shown_text_verbatim": "无（不可静态还原）",
      "shown_text_zh": "透明承接页，具体叠层文案不可静态还原",
      "user_action_requested": "不可静态还原",
      "code_anchor": "#1 manifest:components（ui.TransplentPermissionActivity，theme=@7F110305，noHistory=true）"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "不可静态还原（推测由透明 Activity + 前台服务重新拉起设置页）",
      "trigger_event": "不可静态还原（未取得 onResume/Timer 代码证据）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "1.取得权限失败，无法执行操作。<br><br>2.若因先前拒绝了权限授予，而没有出现权限请求画面，請至『設定→應用程式→當前App→權限』，將「%s」勾選允許。",
      "shown_text_zh": "1. 获取权限失败，无法执行操作。2. 若因先前拒绝了权限授予而没有出现权限请求画面，请到『设置 → 应用程序 → 当前App → 权限』，将「%s」勾选允许。",
      "user_action_requested": "按提示逐级进入应用详情页手动勾选权限（受限设置分步教学模板）；是否存在跳过按钮不可静态还原",
      "code_anchor": "resources.arsc 字符串（strings.xml 键，繁体/简体双版本）；assets/OoooooOooo（呈现位置加密）"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "FocusService（AccessibilityService）+ record.DisplayService / ScreenRecordService / CameraService / AudioService / LiveKitService / RemoteService",
      "trigger_event": "系统绑定无障碍服务后 onServiceConnected（代码在加密载荷内）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面，转入后台读屏与模拟点击",
      "user_action_requested": "无需操作，服务静默运行",
      "code_anchor": "#1 manifest:components（service …service.FocusService；record.DisplayService/CameraService/AudioService/LiveKitService；ca0a8af8…record.ScreenRecordService）"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表条目：服务名『PEA SMART PRO』（android:label=@7F100072，与桌面名 @7F100071 完全相同）",
    "系统无障碍服务详情页说明区：泰文长文案（android:description=@7F10001B，内容见 verbatim_texts）",
    "系统无障碍服务隐私提示页：因 isAccessibilityTool=\"true\" 而被系统抑制，不再展示『可查看屏幕内容、控制设备』警告——这是本样本最关键的『少一步』设计",
    "应用内权限失败提示（AlertDialog 或 Toast 形态，具体载体在加密载荷内）：繁体/简体双版本『取得权限失败，无法执行操作…請至『設定→應用程式→當前App→權限』』，用于把用户导向应用详情页/权限页",
    "透明承接页 TransplentPermissionActivity（theme=@7F110305，noHistory，excludeFromRecents）：跳设置与回跳的过渡载体，用户无感知",
    "activity-alias 名称位：asd.fgh.component.AliasTmpActivity 的 android:label=\"\\u2064\"（不可见字符），可使桌面/列表项显示为空白",
    "assets/ 目录内可能存在的本地引导页资源：未发现 .html/.js 引导页，引导 UI 由加密载荷动态构建或为原生布局"
  ],
  "verbatim_texts": [
    {
      "lang": "th",
      "text_verbatim": "เป็น Application ของการไฟฟ้าส่วนภูมิภาค ที่ผ่านการตรวจสอบเเล้ว ต้องได้รับอนุญาตจากการเข้าถึง ข้อเเนะนำ:เมื่อคุณเปิดสวิตซ์ฟังก์ชั่นรักษาความปลอดภัยแล้ว คุณจะได้รับการเเจ้งเตือนจากระบบ PEA SMART PRO ยืนยันจะไม่ละเมิดสิทธิส่วนบุคคลของผู้ใช้ โปรดวางใจในการเปิดใช้งาน",
      "text_zh": "这是泰国地方电力局（PEA）已通过审核的 Application，必须获得访问授权。提示：当您打开安全功能开关后，您将收到来自 PEA SMART PRO 系统的通知。我们确认不会侵犯用户的个人隐私，请放心开启使用。",
      "source_location": "resources.arsc 字符串 @7F10001B（strings.xml），经无障碍服务配置 android:description 引用",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "zh-TW",
      "text_verbatim": "1.取得权限失败，无法执行操作。<br><br>2.若因先前拒绝了权限授予，而没有出现权限请求画面，請至『設定→應用程式→當前App→權限』，將「%s」勾選允許。",
      "text_zh": "1. 获取权限失败，无法执行操作。2. 若因先前拒绝了权限授予而没有出现权限请求画面，请到『设置 → 应用程序 → 当前App → 权限』，将「%s」勾选允许。",
      "source_location": "resources.arsc / res/values/strings.xml（对应预筛 [DEFAULT] 条目）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "zh-CN",
      "text_verbatim": "1.取得权限失败，无法执行操作。 2.若因先前拒绝了权限授予，而没有出现权限请求画面，请『设置 → 应用程序 → 当前App → 权限』，将「%s」勾选允许。",
      "text_zh": "同义简体版本：获取权限失败，需手动到设置里为当前应用勾选对应权限。",
      "source_location": "resources.arsc / res/values/strings.xml",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Background Services",
      "text_zh": "后台服务（用于把常驻/自启动包装成正常系统能力）",
      "source_location": "resources.arsc 字符串（预筛 [DEFAULT] 条目）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Sorry, the page encountered a problem and needs to be closed",
      "text_zh": "抱歉，页面遇到问题需要关闭（故障恐吓式话术，可迫使重试）",
      "source_location": "resources.arsc 字符串（预筛 [DEFAULT] 条目）",
      "rhetorical_frame": "故障恐吓"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原。已确认存在 TransplentPermissionActivity（透明、noHistory、singleTask、excludeFromRecents）与已声明 SYSTEM_ALERT_WINDOW 权限，具备『跳设置后透明回跳 + 悬浮层重新拉起』的结构条件，但 onResume/Timer 重跳代码位于加密载荷 assets/OoooooOooo 内，未取得直接证据。",
    "overlay_or_fake_settings": "确认存在透明 Activity 承接页（TransplentPermissionActivity，theme=@7F110305，noHistory=true，excludeFromRecents=true）与 SYSTEM_ALERT_WINDOW 权限声明，具备遮罩/浮层能力；未发现高仿系统无障碍开关页的资源或布局证据。实际是否叠放半透明引导遮罩不可静态还原。",
    "restricted_settings_13plus_coaching": "存在受限设置/权限分步教学文案模板：『請至『設定→應用程式→當前App→權限』，將「%s」勾選允許』（繁/简双版本）；但因无障碍配置声明 isAccessibilityTool=\"true\"，Android 13+ 对『受限设置』的额外二次确认被系统自动跳过，实际上无需再教用户点右上角菜单允许受限设置。",
    "post_grant_anti_removal": "不可静态还原。已确认无障碍服务声明 accessibilityFlags=0x5A（含 FILTER_KEY_EVENTS，可拦截返回键等按键事件）与 canPerformGestures=true（可模拟点击），具备阻止撤权/自动点确认的技术能力，但 GLOBAL_ACTION_BACK/HOME 阻止撤权的具体代码位于加密载荷内，未取得直接证据。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "最佳时机：监测到 startActivity 的 Intent 动作为 android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.APPLICATION_DETAILS_SETTINGS 的瞬间，以及紧随其后的透明 Activity（TransplentPermissionActivity）出现；由于该应用伪造 isAccessibilityTool=true，系统不会弹出隐私警告页，因此必须在『用户点击桌面图标后的前 3 秒内』开始逐帧 UTG 采样，以捕获引导弹窗与跳转前后的页面栈变化。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后首个应用内引导页（SplashActivity → Activation/WaitCheck/CheckPermission 链）",
        "page_identifier": "com.lavju.pigfcb.lrymx.lhl 的 Activity，界面含泰文/中文权限说明与单个『开启』类按钮，包名与 PEA 品牌文案同屏",
        "why_most_useful": "决定该应用是冷启动即阻断诱导，还是功能触发式诱导，是判定诱导主动性的核心页面",
        "observable_utg_signals": ["页面文本是否含 PEA SMART PRO / การไฟฟ้าส่วนภูมิภาค 品牌词", "是否存在取消/跳过/稍后按钮", "页面是否不可返回（返回键被拦截或直接退出）"]
      },
      {
        "page_role": "跳转前引导/教学页",
        "page_identifier": "含『設定→應用程式→當前App→權限』或泰文开启指引文本的页面，或跳转前 800ms 内的最后一帧应用内界面",
        "why_most_useful": "证明存在分步教学与话术包装，区分『透明说明』与『教唆开启高危权限』",
        "observable_utg_signals": ["文本中是否出现设置路径指引", "是否出现隐私承诺语句（ไม่ละเมิดสิทธิส่วนบุคคล / 不会侵犯隐私）", "是否出现安全/防盗/账户保护类恐吓词"]
      },
      {
        "page_role": "系统无障碍服务列表项与详情页",
        "page_identifier": "com.android.settings 无障碍列表中的『PEA SMART PRO』条目；详情页说明区泰文长文案",
        "why_most_useful": "确认 isAccessibilityTool=true 导致的『隐私警告页缺失』效果，以及服务名与桌面名一致的伪装",
        "observable_utg_signals": ["列表中服务名文本", "是否缺少『此服务可查看屏幕内容』警告段", "详情页描述文本语言与内容"]
      },
      {
        "page_role": "设置页返回后的叠层/回跳页",
        "page_identifier": "TransplentPermissionActivity（透明无界面）或悬浮窗覆盖在系统设置之上",
        "why_most_useful": "判定是否存在拒权循环重跳与遮罩叠层引导",
        "observable_utg_signals": ["返回后是否再次跳入设置（页面栈出现重复 settings Activity）", "是否有半透明遮罩/悬浮层覆盖设置页", "是否出现 GLOBAL_ACTION_BACK 导致设置页被自动退出"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在显著盲区：1) 业务代码整体加密于 assets/OoooooOooo，由 assets 内的 libdpt.so 解密加载，静态无法确认跳转点与拒权循环实现；2) 无障碍配置伪造 isAccessibilityTool=true，使系统隐私警告页不出现，纯 UTG 采样若只盯『警告页』会漏检；3) activity-alias label 使用 U+2064 不可见字符，桌面/列表可能呈现空白名称，OCR 与文本比对易判为空；4) TransplentPermissionActivity 透明无内容，UTG 在该页可能只看到下层设置界面；5) 静态加壳本身不阻挡运行期 UTG，必须实际运行才能补齐流程。"
  },
  "behavior_pattern_tags": [
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_FAKE_IS_ACCESSIBILITY_TOOL",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "#1 manifest:components（service c56ddef9ebb3c4be8ba7cf6c2f70f7be5.c43e95c997cf14b07966e5119de1a1367.c89a2b2ed4b964162b044e43f5a1cfca2.service.FocusService，android:label=@7F100072，meta-data android:accessibilityservice=@7F13000F）",
    "#1 file:res/values/public.xml/touch_accessibility_service_config.xml（android:isAccessibilityTool=\"true\"，accessibilityFlags=\"0x0000005A\"，canPerformGestures=\"true\"，android:description=@7F10001B）",
    "#1 manifest:components（activity …ui.TransplentPermissionActivity，theme=@7F110305，noHistory=true，excludeFromRecents=true；activity-alias asd.fgh.component.AliasTmpActivity android:label=\"⁤\"）",
    "#1 file:assets/OoooooOooo（1,979,518 字节加密载荷，真实业务代码载体）",
    "#1 file:assets/app_name（存放真实 Application 类名 c56ddef9…c89a2b2ed4b964162b044e43f5a1cfca2.App）",
    "#1.dex1 code:com.nashsiqiu.shell.ProxyApplication（壳 Application，Manifest android:name 指向）"
  ]
}
```

**未决问题与覆盖边界**：`assets/OoooooOooo` 的解密流程（`libdpt.so` + `com.nashsiqiu.shell.ProxyApplication`）未展开，因此 `ACTION_ACCESSIBILITY_SETTINGS` 跳转点、引导弹窗不可取消性、`onResume` 拒权循环、获权后自动点击/阻止撤权的具体实现均属**静态不可见**；本次受 14 次调用预算约束未做动态运行验证，也未向项目风险台账写入记录（已确认命题：伪装 PEA 电力局品牌 + `isAccessibilityTool` 伪造 + 加密载荷驱动的无障碍诱导）。

</details>
