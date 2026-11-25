# MB_167__9e57476abd｜Unattributed — Oбнoвлeниe Мinеcraft...

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：144.1s

## 1. 一句话核心结论

- **核心申请方式**：以「安装系统更新/安全应用」为壳，用带手机模拟插画的三步教学页教用户去系统无障碍列表开启自家服务（伪造 isAccessibilityTool=true、服务名即伪更新应用名），被拦截时还教用户关闭悬浮窗与录屏以绕过隐藏请求报错。
- **静态可见性说明**：classes.dex 仅 5 个类，为显式 decoy 模式外壳（TalavovuFactory58e8 日志 'Provider missing in decoy mode'），Manifest 声明的无障碍服务 DagadizexoService_a186、启动 Activity、GatewayActivity 均不在 DEX 中；真实逻辑藏于加密资产 assets/bglwnb/{iypitkpj.db,mmsvczyt.db,pmnprcvk.bin}（高熵非 dex/zip 头），由 libldpnddb.so 按明文路径读取、libreality_transport.so 提供 ring/curve25519 加密传输，静态无法还原跳转代码与云控开关。可完整静态可见的部分为全部引导文案 res/values/strings.xml、引导页布局 activity_coral_cobra.xml、无障碍元数据 res/xml/acc_service.xml 与 WebView 布局 activity_hidden.xml / activity_web_view.xml。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_FAKE_SETTINGS_SCREEN`（高仿系统无障碍设置列表/假开关页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`ID_FAKE_IS_ACCESSIBILITY_TOOL`（伪造android:isAccessibilityTool="true"）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `9e57476abdac74d094d55d9868308f2ab88090be12e0f0460ec129d53ccf244a` |
| 包名 / 年份 | `com.vuji.luzudomi` / 2026 |
| 家族 / 品类 | **Unattributed**（同池样本数：13） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Oбнoвлeниe Мinеcraft... |
| 引导页宣称品牌/身份 | Minecraft 更新（Oбнoвлeниe = 俄语“更新”）+ 系统安全保护/系统更新器；另冒充 Google Services Framework、System Core、Network Interface 等系统组件 |
| 系统无障碍列表服务名 | Oбнoвлeниe Мinеcraft...（android:label=@string/app_name，与无障碍描述 @string/app_name 一致，列表里看不到任何“无障碍/辅助”字样） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：①同形字混排：用西里尔 О/б/н/е/и/с 与拉丁 М/i 拼出 Oбнoвлeниe Мinеcraft，末尾加省略号制造截断感；②无障碍描述与标签全部复用 @string/app_name，隐藏服务真实用途；③acc_service.xml 伪造 android:isAccessibilityTool="true"，企图绕过 Android 13+ 受限设置告警；④启动入口只挂 LEANBACK_LAUNCHER（无 LAUNCHER），无桌面图标，规避用户察觉与常规启动检测；⑤大量 Theme.NoDisplay + label 为随机十六进制（933fa/44cba/83a8a…）的隐藏 Activity 作静默跳转跳板；⑥服务/Provider 使用随机后缀类名（_a186/_aaf2/_68e27311 进程名）与多进程拆分；⑦cc_hidden_request_hint 教用户关闭悬浮窗、侧栏并停止录屏以消除系统“隐藏请求”报错。 |
| 无障碍服务类名 | `com.vuji.luzudomi.services.DagadizexoService_a186` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=True` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, PROCESS_OUTGOING_CALLS, QUERY_ALL_PACKAGES, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Oбнoвлeниe Мinеcraft... |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.vuji.luzudomi.activities.GoniyulujufoActivity_a12f（Manifest 唯一带 intent-filter 的启动 Activity，仅 LEANBACK_LAUNCHER，excludeFromRecents=true、noHistory=true） | 系统/后台或 LEANBACK 入口启动；noHistory+excludeFromRecents 使其不留在最近任务中 | 原生Activity | **原文**：无（Theme.AppCompat.Light.NoActionBar，启动页文案在加密载荷内，静态不可见）<br>**译注**：启动页内容静态不可还原，后续由加密载荷决定跳转 | 无显式交互，自动跳转下一页 | `#1 manifest:components（GoniyulujufoActivity_a12f）；真实跳转代码在 assets/bglwnb/*.db 加密载荷` |
| 2 | 引导说明页 | cc_ 系列引导页（布局 res/layout/activity_coral_cobra.xml：锁图标 + cc_header + cc_title + cc_desc + 手机模拟插画 cardIllustration + 三步说明 + OPEN SETTINGS 按钮） | 启动页/定时器/云控指令拉起该引导 Activity（具体调用点在加密载荷内） | 原生Activity | **原文**：INSTALLING SECURE APP / ACTIVATION OF PROTECTION / To protect your personal data from leaks, the app needs to activate the "Accessibility" feature. Follow the instructions below to open settings.<br>**译注**：「正在安装安全应用」/「启用保护」/「为防止您的个人数据泄露，应用需要开启『无障碍』功能，请按下方说明打开设置。」 | 阅读说明后点击底部 OPEN SETTINGS 按钮（布局中未见取消/跳过按钮，仅关闭靠返回键） | `res/layout/activity_coral_cobra.xml + res/values/strings.xml（cc_header/cc_title/cc_desc/cc_button）` |
| 3 | 遮罩叠层指引 | 引导页内嵌的手机模拟插画：drawable/phone_mock_frame 画框 + 伪状态栏 12:00 + 伪列表项 tvMockAppName（@string/app_name）+ drawable/mock_toggle_off 假开关 + cc_mock_title | 与引导页同屏渲染，作为“系统设置页长什么样”的视觉暗示 | 悬浮窗Overlay | **原文**：12:00 / Accessibility / Oбнoвлeниe Мinеcraft... / 1. Tap 'OPEN SETTINGS' below. / 2. On the opened screen, find %1$s. / 3. Enable the switch next to it.<br>**译注**：「12:00」/「无障碍」/「Oбнoвлeниe Мinеcraft...」/「1. 点击下方『打开设置』。2. 在打开的页面中找到 %1$s。3. 打开它右侧的开关。」 | 按图示在系统无障碍列表中找到与插画同名的条目并开启开关（插画用假开关把系统操作“伪装成本页内操作”） | `res/layout/activity_coral_cobra.xml（llAccessibilityIllustration / tvMockAppName / mock_toggle_off）+ strings.xml（cc_mock_title/cc_step_1/2/3）` |
| 4 | 跳无障碍设置 | ACTION_ACCESSIBILITY_SETTINGS 系统页；无障碍服务元数据指向 android:settingsActivity=".activities.GatewayActivity"；目标服务 com.vuji.luzudomi.services.DagadizexoService_a186（process=:vnc_Svc_68e27311，permission=BIND_ACCESSIBILITY_SERVICE） | 点击 OPEN SETTINGS（cc_button）触发 startActivity 跳系统无障碍设置；调用点在加密载荷内 | 系统无障碍页 | **原文**：OPEN SETTINGS（按钮）；系统页显示条目名 = Oбнoвлeниe Мinеcraft...<br>**译注**：「打开设置」按钮；跳转后系统无障碍服务列表中显示条目为伪装名「Oбнoвлeниe Мinеcraft...」 | 在系统无障碍列表中定位同名条目并手动拨开开关（无系统级跳过路径，需用户真实操作） | `res/xml/acc_service.xml（settingsActivity=GatewayActivity、isAccessibilityTool=true、typeAllMask、canTakeScreenshot=true）+ AndroidManifest.xml DagadizexoService_a186` |
| 5 | 拒权反馈循环 | 引导页等待态（tvStep/ viewProgress / cc_waiting_accessibility）；系统“隐藏请求”报错提示时的补救说明 cc_hidden_request_hint | onResume / 轮询检测无障碍服务未启用时回到引导页显示等待；或系统拦截时展示补救文案 | 原生Activity | **原文**：Waiting for accessibility… / If you see an error about a hidden request — close floating windows, side panels, and stop screen recording, then try again.<br>**译注**：「正在等待无障碍…」/「如果你看到关于“隐藏请求”的错误——请关闭悬浮窗、侧栏并停止屏幕录制，然后重试。」 | 返回应用后继续等待/再次点击 OPEN SETTINGS 重试；被拦截时按提示关闭悬浮窗与录屏以消除系统告警 | `res/values/strings.xml（cc_waiting_accessibility / cc_hidden_request_hint）+ activity_coral_cobra.xml（tvStep/viewProgress）` |
| 6 | 获权后动作 | 设备管理员申请页（cc_admin_*）+ 悬浮窗引导（pixel_guide_*）+ 默认短信应用设置（set_default_sms_app）；另有 ov_* 全屏“系统更新”进度覆盖层与 au_* 更新提示；隐藏 WebView 载体 activity_hidden.xml / activity_web_view.xml；无障碍服务 DagadizexoService_a186 进入 :vnc_Svc 进程 | 无障碍开关被拨开后（服务 onServiceConnected 回调，代码在加密载荷内）继续推进下一项权限；或由云控指令触发 | 原生Dialog | **原文**：SYSTEM PROTECTION / ACTIVATE PROTECTION / Without this permission, the app cannot work / To protect diagnostic data and prevent unauthorized access, administrator rights are required. / Protection from malware / Encryption of system data / File integrity control / Waiting for protection activation… / Grant 'Display Over Other Apps' Access / 2. Set as Default SMS App / Select our app in the 'SMS app' section / Having trouble? Skip<br>**译注**：「系统保护」/「启用保护」/「没有此权限应用无法运行」/「为保护诊断数据并防止未授权访问，需要管理员权限。」/「防恶意软件」/「系统数据加密」/「文件完整性控制」/「正在等待保护启用…」/「授予『在其他应用上层显示』权限」/「2. 设为默认短信应用」/「在『短信应用』中选择我们的应用」/「遇到问题？跳过」 | 依次激活设备管理员、授予悬浮窗、设为默认短信应用；短信角色步骤提供「跳过」退路，其余步骤以“没有此权限应用无法运行”施压 | `res/values/strings.xml（cc_admin_* / pixel_guide_* / set_default_sms_app / skip_role_check_button / ov_* / au_*）+ res/layout/activity_hidden.xml、activity_web_view.xml + AndroidManifest.xml ViwexixubuReceiver_5a4e(BIND_DEVICE_ADMIN)` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 引导 Activity（res/layout/activity_coral_cobra.xml）顶部标题栏：锁图标 + cc_header「INSTALLING SECURE APP」
- 同页正文：cc_title「ACTIVATION OF PROTECTION」+ cc_desc「为防止您的个人数据泄露，应用需要开启『无障碍』…」
- 同页卡片插画区：phone_mock_frame 假手机 + 伪状态栏 12:00 + cc_mock_title「Accessibility」+ tvMockAppName 显示伪装应用名 + mock_toggle_off 假开关（把系统设置页做成页内示意图）
- 同页三步说明：cc_step_1/2/3，其中 %1$s 动态填入伪装应用名
- 同页底部按钮：cc_button「OPEN SETTINGS」
- 同页等待态：tvStep / viewProgress / cc_waiting_accessibility「Waiting for accessibility…」
- 同页系统拦截补救：cc_hidden_request_hint（教用户关闭悬浮窗、侧栏、停止录屏）
- 系统无障碍服务列表：android:label 与 android:description 均为 @string/app_name，即「Oбнoвлeниe Мinеcraft...」（不显示任何辅助功能说明）
- 设备管理员激活对话框：cc_admin_title「SYSTEM PROTECTION」、cc_admin_desc、cc_admin_reason_1/2/3、cc_admin_button「ACTIVATE PROTECTION」、cc_admin_warning、cc_waiting_admin
- 悬浮窗引导：pixel_guide_step_title「Grant 'Display Over Other Apps' Access」、pixel_guide_enable_app
- 默认短信应用引导：set_default_sms_app、set_default_sms_app_toast、set_default_sms_app_granted、skip_role_check_button「Having trouble? Skip」
- 伪装系统更新提示：au_title「Installing system update…」、au_warning、battery_permission_warning
- 全屏“更新进度”覆盖层文案：ov_phase1_title/sub1-3、ov_phase2_title/sub、ov_phase3_title/sub、ov_complete「Update installed!」、ov_wait_update
- WebView 载体：activity_hidden.xml（全屏 WebView，无可见控件）、activity_web_view.xml（loadingGif 加载图 + WebView），内容为本地或远端 URL（静态不可判定）
- 通知栏：notification_permission_request / notification_permission_toast（通知权限兜底提示）；system_service_label「Google Services Framework」用于通知/服务冒名

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | INSTALLING SECURE APP | 正在安装安全应用 | `res/values/strings.xml: cc_header` | 假更新 |
| en | ACTIVATION OF PROTECTION | 启用保护 | `res/values/strings.xml: cc_title` | 假反诈安全 |
| en | To protect your personal data from leaks, the app needs to activate the "Accessibility" feature. Follow the instructions below to open settings. | 为防止您的个人数据泄露，本应用需要开启“无障碍”功能。请按下方说明打开设置。 | `res/values/strings.xml: cc_desc` | 隐私承诺 |
| en | 1. Tap 'OPEN SETTINGS' below. | 1. 点击下方“打开设置”。 | `res/values/strings.xml: cc_step_1` | 受限设置分步教学 |
| en | 2. On the opened screen, find %1$s. | 2. 在打开的页面中找到 %1$s。 | `res/values/strings.xml: cc_step_2` | 受限设置分步教学 |
| en | 3. Enable the switch next to it. | 3. 打开它右侧的开关。 | `res/values/strings.xml: cc_step_3` | 受限设置分步教学 |
| en | OPEN SETTINGS | 打开设置 | `res/values/strings.xml: cc_button` | 受限设置分步教学 |
| en | Accessibility | 无障碍 | `res/values/strings.xml: cc_mock_title（用于页内假系统页插画标题）` | 受限设置分步教学 |
| en | Waiting for accessibility… | 正在等待无障碍… | `res/values/strings.xml: cc_waiting_accessibility` | 受限设置分步教学 |
| en | If you see an error about a hidden request — close floating windows, side panels, and stop screen recording, then try again. | 如果你看到关于“隐藏请求”的错误——请关闭悬浮窗、侧栏并停止屏幕录制，然后重试。 | `res/values/strings.xml: cc_hidden_request_hint` | 教唆忽视警告 |
| en | To protect diagnostic data and prevent unauthorized access, administrator rights are required. | 为保护诊断数据并防止未授权访问，需要管理员权限。 | `res/values/strings.xml: cc_admin_desc` | 假反诈安全 |
| en | ACTIVATE PROTECTION | 启用保护 | `res/values/strings.xml: cc_admin_button` | 假反诈安全 |
| en | Without this permission, the app cannot work | 没有此权限，应用无法运行 | `res/values/strings.xml: cc_admin_warning` | 故障恐吓 |
| en | Protection from malware / Encryption of system data / File integrity control | 防恶意软件 / 系统数据加密 / 文件完整性控制 | `res/values/strings.xml: cc_admin_reason_1/2/3` | 假反诈安全 |
| en | Installing system update… | 正在安装系统更新… | `res/values/strings.xml: au_title` | 假更新 |
| en | Do not restart or use your device during the update to avoid data loss and system errors. | 更新期间请勿重启或使用设备，以免数据丢失与系统错误。 | `res/values/strings.xml: au_warning` | 假更新 |
| en | Unpacking system update… / Verifying packages… / Preparing installation… / Applying system patches… / Cleaning up temporary files… / Update installed! | 正在解包系统更新… / 正在校验安装包… / 正在准备安装… / 正在应用系统补丁… / 正在清理临时文件… / 更新已安装！ | `res/values/strings.xml: ov_phase1_sub1-3 / ov_phase2_sub / ov_phase3_sub / ov_complete` | 假更新 |
| en | Grant 'Display Over Other Apps' Access | 授予“在其他应用上层显示”权限 | `res/values/strings.xml: pixel_guide_step_title` | 受限设置分步教学 |
| en | 2. Set as Default SMS App | 2. 设为默认短信应用 | `res/values/strings.xml: set_default_sms_app` | 受限设置分步教学 |
| en | Select our app in the 'SMS app' section | 在“短信应用”一栏中选择我们的应用 | `res/values/strings.xml: set_default_sms_app_toast` | 受限设置分步教学 |
| en | Having trouble? Skip | 遇到问题？跳过 | `res/values/strings.xml: skip_role_check_button` | 受限设置分步教学 |
| ru | Oбнoвлeниe Мinеcraft... | Minecraft 更新…（使用西里尔同形字母混排拉丁字母） | `res/values/strings.xml: app_name（同时作为无障碍 label 与 description）` | 假更新 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：引导页提供 cc_waiting_accessibility「正在等待无障碍…」等待态（tvStep/viewProgress），返回应用后重新判定未授权即停留在引导页继续提示再次点击 OPEN SETTINGS；是否为定时器死循环重跳、以及跳系统设置后是否用 GLOBAL_ACTION_BACK/HOME 阻止撤权，取决于加密载荷中的 DagadizexoService_a186 实现，静态不可确认；仅短信角色步骤提供 skip_role_check_button「遇到问题？跳过」作为柔性退路。
- **遮罩叠层 / 高仿系统设置页**：引导页内嵌 phone_mock_frame + mock_toggle_off 的“伪系统无障碍开关页”插画（把系统设置页做成页内示意图，并显示与应用同名的条目），非真实悬浮窗叠在系统设置之上；另申请 SYSTEM_ALERT_WINDOW 并配有 pixel_guide_* 悬浮窗引导，具备设置页叠层遮罩能力，但未取得运行期叠层证据。
- **Android 13+ 受限设置（Restricted Settings）应对**：无明确的分步教用户进应用详情→右上角菜单→允许受限设置文案；其替代手法是伪造 android:isAccessibilityTool="true" 以规避 Android 13+ 受限设置告警，并通过 cc_hidden_request_hint 教用户关闭悬浮窗/侧栏、停止录屏以消除系统“隐藏请求”拦截；targetSdkVersion=33。
- **获权后即时行为与防撤权机制**：静态证据未见自点确认或监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权的实现（该逻辑若存在应位于加密载荷 DagadizexoService_a186 中）；但已声明 typeAllMask 全事件监听、canRetrieveWindowContent、canPerformGestures、canTakeScreenshot、flagRequestFilterKeyEvents、flagRetrieveInteractiveWindows，并叠加设备管理员（ViwexixubuReceiver_5a4e）、KEEP_ALIVE 音频服务与 :core_Svc/:vnc_Svc 多进程保活，具备反撤权/反卸载能力基础。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 Activity 切换至 com.vuji.luzudomi 的 cc_ 引导页（activity_coral_cobra 布局特征：锁图标 + 'INSTALLING SECURE APP' + 手机插画 + OPEN SETTINGS 按钮）时立即开始录屏与逐帧 UTG；其次在监测到 Intent ACTION_ACCESSIBILITY_SETTINGS 跳转瞬间与用户返回应用后的 onResume 窗口内抓取。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在两处盲区：①classes.dex 为 decoy 外壳（仅 5 个类），无障碍服务 DagadizexoService_a186、GatewayActivity、启动 Activity 的真实实现全部位于加密资产 assets/bglwnb/{iypitkpj.db,mmsvczyt.db,pmnprcvk.bin}（高熵、非 dex/zip 头），由 libldpnddb.so 加载、libreality_transport.so 提供 ring/curve25519 加密通道——因此“何时、由谁拉起引导页”只能靠运行期 UTG/流量观测；②启动入口仅声明 LEANBACK_LAUNCHER 且 excludeFromRecents+noHistory，常规桌面点击启动路径不存在，UTG 需通过 adb am start 或等待后台/通知拉起；③WebView 内容可能是远端下发（隐藏请求提示暗示系统识别到 overlay/录屏，属反 UTG 设计），纯静态无法确认 H5 文案，但原生 cc_ 页文案已足以完成判定，静态加壳不阻挡运行期 UTG 取证。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导说明页（cc_ 页，最重要）** | 包名 com.vuji.luzudomi 的 Activity，界面含 'INSTALLING SECURE APP' 标题、锁图标、手机模拟插画与 'OPEN SETTINGS' 按钮 | 该页一次性呈现伪装身份、隐私承诺话术、伪系统开关插画与三步教学，是“诱导开无障碍”的完整证据面 | 文本 INSTALLING SECURE APP / ACTIVATION OF PROTECTION；文本 OPEN SETTINGS 按钮可点击节点；含 'Accessibility' 与伪装应用名的插画 TextView 节点；三步文案 '1. Tap...' '2. On the opened screen, find' '3. Enable the switch'；页面无取消/跳过按钮 |
| **跳转前/后 WebView 教学或遮罩页** | 全屏 WebView 的 Activity（布局仅 WebView 或 loadingGif+WebView），无可见原生控件 | 验证是否存在远端 HTML 教学页或 GIF 动画引导（静态只看到空 WebView 布局，URL 在加密载荷内），区分本地资源与远端下发 | WebView 内 H5 文本/按钮节点（如 'Enable'、'Allow'）；loadingGif 加载动画节点；WebView 首次加载 URL 与来源域名 |
| **系统无障碍服务列表项** | com.android.settings 无障碍设置页中 label 为 'Oбнoвлeниe Мinеcraft...' 的条目（无任何辅助功能描述） | 证明服务名与描述完全等同伪更新应用名，系统层面无“辅助功能”提示，是身份混淆的直接证据 | 条目文本 Oбнoвлeниe Мinеcraft...（含西里尔同形字）；条目下无 description 副标题；开关初始为关闭、由用户手动拨开 |
| **设置页返回后的等待态/拒权反馈页** | 回到 cc_ 引导页显示 'Waiting for accessibility…' 与进度指示（tvStep/viewProgress 可见） | 判定拒权后是否重跳、是否死循环施压，以及是否出现 'hidden request' 补救提示（教用户关悬浮窗/停录屏） | 文本 Waiting for accessibility…；文本 'close floating windows, side panels, and stop screen recording'；同一 Activity 在短周期内反复重建；返回键是否被拦截 |
| **获权后的权限阶梯页与假更新覆盖层** | 设备管理员激活页（'SYSTEM PROTECTION'/'ACTIVATE PROTECTION'）、悬浮窗引导页、默认短信应用选择页，以及 'System update / Installing update…' 全屏进度层 | 记录无障碍获权后的后续动作顺序与假更新叙事延续，支撑“系统更新器”伪装的完整链路 | 文本 SYSTEM PROTECTION / ACTIVATE PROTECTION；文本 Grant 'Display Over Other Apps' Access；文本 Set as Default SMS App / Having trouble? Skip；文本 System update / Applying system patches… / Update installed! |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `res/values/strings.xml（cc_header/cc_title/cc_desc/cc_step_1-3/cc_button/cc_mock_title/cc_waiting_accessibility/cc_hidden_request_hint/cc_admin_*/au_*/ov_*/pixel_guide_*/set_default_sms_app/app_name）`
- `res/xml/acc_service.xml（isAccessibilityTool="true"、settingsActivity=".activities.GatewayActivity"、typeAllMask、canTakeScreenshot、description=@string/app_name）`
- `res/layout/activity_coral_cobra.xml（llAccessibilityIllustration / tvMockAppName / mock_toggle_off / tvStep1-3 / cc_button）`
- `res/layout/activity_hidden.xml、res/layout/activity_web_view.xml（全屏 WebView 载体）`
- `com.vuji.luzudomi.TalavovuFactory58e8#instantiateProvider（'Provider missing in decoy mode'，证明 DEX 为诱饵壳层）`
- `assets/bglwnb/{iypitkpj.db,mmsvczyt.db,pmnprcvk.bin} + lib/arm64-v8a/libldpnddb.so（加密载荷与其加载器）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（基于静态证据，DEX 为诱饵壳层）

**静态可见性判定：`packed_or_encrypted`**。`classes.dex` 仅有 5 个类，是刻意设计的"decoy mode"（诱饵模式）外壳：[TalavovuFactory58e8](<resource-unit:#1.dex1 code:com.vuji.luzudomi.TalavovuFactory58e8>) 在 Provider 缺失时仅打日志 `"Provider missing in decoy mode: "` 并返回 `NoOpProvider`；Manifest 中声明的无障碍服务 `DagadizexoService_a186`、启动页 `GoniyulujufoActivity_a12f`、引导页 `GatewayActivity` 等真实组件在 DEX 中全部不存在。真实代码位于加密资产 `assets/bglwnb/{iypitkpj.db,mmsvczyt.db,pmnprcvk.bin}`（文件头均为高熵随机字节，非标准 dex/zip），由 [libldpnddb.so](<resource-unit:#1.so2>) 通过明文路径字符串 `bglwnb/mmsvczyt.db`、`bglwnb/iypitkpj.db`、`bglwnb/pmnprcvk.bin` 读取；`libreality_transport.so` 内含 Rust `ring 0.17.14` + `curve25519-dalek` 的 AEAD/HKDF/ECDH，是控制通道的加密传输层。

**但引导流程的文案与布局是完整静态可见的**——所有无障碍诱导话术集中在 [res/values/strings.xml](<resource-unit:#1 file:res/values/strings.xml>)，引导页布局在 [res/layout/activity_coral_cobra.xml](<resource-unit:#1 file:res/layout/activity_coral_cobra.xml>)，无障碍配置在 [res/xml/acc_service.xml](<resource-unit:#1 file:res/xml/acc_service.xml>)。因此运行期 UTG 页面流转可被精确预测，仅"哪段代码在何时拉起它"藏在加密载荷内。

**核心诱导机制（cc_ 前缀即 "coaching/click-coach" 系列）：**
1. 应用以"安装安全应用 / 系统更新"为外壳，[cc_header](<resource-unit:#1 file:res/values/strings.xml#L1>) 为 `INSTALLING SECURE APP`，标题 `ACTIVATION OF PROTECTION`。
2. 以"保护个人数据不泄露"为名要求开启无障碍（`cc_desc`），**不是**说明无障碍的实际用途（读屏/窗口内容/手势/截图），属隐私承诺式欺骗。
3. 页内嵌**手机模拟插画**：`phone_mock_frame` 画框 + `mock_toggle_off` 假开关 + `tvMockAppName`（显示伪装名），把系统设置页做成"本页示意图"，降低用户对"跳出去开无障碍"的警觉（`cc_mock_title` = `Accessibility`）。
4. 三步分步教学 `cc_step_1/2/3` + `OPEN SETTINGS` 按钮，直接跳 `ACTION_ACCESSIBILITY_SETTINGS`（服务元数据 `android:settingsActivity=".activities.GatewayActivity"`）。
5. 返回后轮询 `cc_waiting_accessibility`（`Waiting for accessibility…`）；若被系统拦截，`cc_hidden_request_hint` 教用户**关闭悬浮窗、侧栏并停止录屏**再重试——即教用户消除"隐藏请求"报错，这是明确的反检测/反录屏教唆。
6. 权限阶梯：无障碍之后接设备管理员（`cc_admin_*` / `ACTIVATE PROTECTION`）、悬浮窗（`pixel_guide_step_title`）、默认短信应用（`set_default_sms_app`），并留 `skip_role_check_button`（`Having trouble? Skip`）作为柔性绕行。

**身份伪装要点：** 桌面名 `Oбнoвлeниe Мinеcraft...` 使用西里尔字母同形字（О/б/н/е/и/с 混排拉丁 М、i、craft）冒充"Minecraft 更新"；无障碍列表描述直接复用 `@string/app_name`（服务名 = 应用名 = 伪更新名）；`acc_service.xml` 声明 `android:isAccessibilityTool="true"` 伪造"辅助工具"属性，并申请 `canTakeScreenshot`、`canRetrieveWindowContent`、`flagRequestFilterKeyEvents`、`typeAllMask` 全事件监听——远超任何"系统更新/安全保护"所需。另有 `system_service_label` = `Google Services Framework`、服务 label `System Core` / `Network Interface` 的系统组件冒充。启动入口只声明 `LEANBACK_LAUNCHER`（无普通 `LAUNCHER`），无桌面图标，靠后台/通知拉起；大量 `Theme.NoDisplay` 且 `label` 为随机十六进制（`933fa`、`44cba`…）的隐藏 Activity 用于静默跳转。

**证据边界：** 未执行动态分析，未能取得跳转调用的类名/方法名（DEX 诱饵 + 载荷加密），也未解密 `bglwnb/*.db`；`cc_*` 与 `au_*`/`ov_*` 的调用时序、拒绝后是否死循环重跳，均需 UTG 运行期确认。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "classes.dex 仅 5 个类，为显式 decoy 模式外壳（TalavovuFactory58e8 日志 'Provider missing in decoy mode'），Manifest 声明的无障碍服务 DagadizexoService_a186、启动 Activity、GatewayActivity 均不在 DEX 中；真实逻辑藏于加密资产 assets/bglwnb/{iypitkpj.db,mmsvczyt.db,pmnprcvk.bin}（高熵非 dex/zip 头），由 libldpnddb.so 按明文路径读取、libreality_transport.so 提供 ring/curve25519 加密传输，静态无法还原跳转代码与云控开关。可完整静态可见的部分为全部引导文案 res/values/strings.xml、引导页布局 activity_coral_cobra.xml、无障碍元数据 res/xml/acc_service.xml 与 WebView 布局 activity_hidden.xml / activity_web_view.xml。",
  "summary_one_liner": "以「安装系统更新/安全应用」为壳，用带手机模拟插画的三步教学页教用户去系统无障碍列表开启自家服务（伪造 isAccessibilityTool=true、服务名即伪更新应用名），被拦截时还教用户关闭悬浮窗与录屏以绕过隐藏请求报错。",
  "disguise_identity": {
    "app_display_name": "Oбнoвлeниe Мinеcraft...",
    "claimed_brand_or_persona": "Minecraft 更新（Oбнoвлeниe = 俄语“更新”）+ 系统安全保护/系统更新器；另冒充 Google Services Framework、System Core、Network Interface 等系统组件",
    "a11y_service_label": "Oбнoвлeниe Мinеcraft...（android:label=@string/app_name，与无障碍描述 @string/app_name 一致，列表里看不到任何“无障碍/辅助”字样）",
    "identity_mismatch": true,
    "obfuscation_tricks": "①同形字混排：用西里尔 О/б/н/е/и/с 与拉丁 М/i 拼出 Oбнoвлeниe Мinеcraft，末尾加省略号制造截断感；②无障碍描述与标签全部复用 @string/app_name，隐藏服务真实用途；③acc_service.xml 伪造 android:isAccessibilityTool=\"true\"，企图绕过 Android 13+ 受限设置告警；④启动入口只挂 LEANBACK_LAUNCHER（无 LAUNCHER），无桌面图标，规避用户察觉与常规启动检测；⑤大量 Theme.NoDisplay + label 为随机十六进制（933fa/44cba/83a8a…）的隐藏 Activity 作静默跳转跳板；⑥服务/Provider 使用随机后缀类名（_a186/_aaf2/_68e27311 进程名）与多进程拆分；⑦cc_hidden_request_hint 教用户关闭悬浮窗、侧栏并停止录屏以消除系统“隐藏请求”报错。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.vuji.luzudomi.activities.GoniyulujufoActivity_a12f（Manifest 唯一带 intent-filter 的启动 Activity，仅 LEANBACK_LAUNCHER，excludeFromRecents=true、noHistory=true）",
      "trigger_event": "系统/后台或 LEANBACK 入口启动；noHistory+excludeFromRecents 使其不留在最近任务中",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（Theme.AppCompat.Light.NoActionBar，启动页文案在加密载荷内，静态不可见）",
      "shown_text_zh": "启动页内容静态不可还原，后续由加密载荷决定跳转",
      "user_action_requested": "无显式交互，自动跳转下一页",
      "code_anchor": "#1 manifest:components（GoniyulujufoActivity_a12f）；真实跳转代码在 assets/bglwnb/*.db 加密载荷"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "cc_ 系列引导页（布局 res/layout/activity_coral_cobra.xml：锁图标 + cc_header + cc_title + cc_desc + 手机模拟插画 cardIllustration + 三步说明 + OPEN SETTINGS 按钮）",
      "trigger_event": "启动页/定时器/云控指令拉起该引导 Activity（具体调用点在加密载荷内）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "INSTALLING SECURE APP / ACTIVATION OF PROTECTION / To protect your personal data from leaks, the app needs to activate the \"Accessibility\" feature. Follow the instructions below to open settings.",
      "shown_text_zh": "「正在安装安全应用」/「启用保护」/「为防止您的个人数据泄露，应用需要开启『无障碍』功能，请按下方说明打开设置。」",
      "user_action_requested": "阅读说明后点击底部 OPEN SETTINGS 按钮（布局中未见取消/跳过按钮，仅关闭靠返回键）",
      "code_anchor": "res/layout/activity_coral_cobra.xml + res/values/strings.xml（cc_header/cc_title/cc_desc/cc_button）"
    },
    {
      "step": 3,
      "stage": "遮罩叠层指引",
      "screen_or_component": "引导页内嵌的手机模拟插画：drawable/phone_mock_frame 画框 + 伪状态栏 12:00 + 伪列表项 tvMockAppName（@string/app_name）+ drawable/mock_toggle_off 假开关 + cc_mock_title",
      "trigger_event": "与引导页同屏渲染，作为“系统设置页长什么样”的视觉暗示",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "12:00 / Accessibility / Oбнoвлeниe Мinеcraft... / 1. Tap 'OPEN SETTINGS' below. / 2. On the opened screen, find %1$s. / 3. Enable the switch next to it.",
      "shown_text_zh": "「12:00」/「无障碍」/「Oбнoвлeниe Мinеcraft...」/「1. 点击下方『打开设置』。2. 在打开的页面中找到 %1$s。3. 打开它右侧的开关。」",
      "user_action_requested": "按图示在系统无障碍列表中找到与插画同名的条目并开启开关（插画用假开关把系统操作“伪装成本页内操作”）",
      "code_anchor": "res/layout/activity_coral_cobra.xml（llAccessibilityIllustration / tvMockAppName / mock_toggle_off）+ strings.xml（cc_mock_title/cc_step_1/2/3）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "ACTION_ACCESSIBILITY_SETTINGS 系统页；无障碍服务元数据指向 android:settingsActivity=\".activities.GatewayActivity\"；目标服务 com.vuji.luzudomi.services.DagadizexoService_a186（process=:vnc_Svc_68e27311，permission=BIND_ACCESSIBILITY_SERVICE）",
      "trigger_event": "点击 OPEN SETTINGS（cc_button）触发 startActivity 跳系统无障碍设置；调用点在加密载荷内",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "OPEN SETTINGS（按钮）；系统页显示条目名 = Oбнoвлeниe Мinеcraft...",
      "shown_text_zh": "「打开设置」按钮；跳转后系统无障碍服务列表中显示条目为伪装名「Oбнoвлeниe Мinеcraft...」",
      "user_action_requested": "在系统无障碍列表中定位同名条目并手动拨开开关（无系统级跳过路径，需用户真实操作）",
      "code_anchor": "res/xml/acc_service.xml（settingsActivity=GatewayActivity、isAccessibilityTool=true、typeAllMask、canTakeScreenshot=true）+ AndroidManifest.xml DagadizexoService_a186"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "引导页等待态（tvStep/ viewProgress / cc_waiting_accessibility）；系统“隐藏请求”报错提示时的补救说明 cc_hidden_request_hint",
      "trigger_event": "onResume / 轮询检测无障碍服务未启用时回到引导页显示等待；或系统拦截时展示补救文案",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Waiting for accessibility… / If you see an error about a hidden request — close floating windows, side panels, and stop screen recording, then try again.",
      "shown_text_zh": "「正在等待无障碍…」/「如果你看到关于“隐藏请求”的错误——请关闭悬浮窗、侧栏并停止屏幕录制，然后重试。」",
      "user_action_requested": "返回应用后继续等待/再次点击 OPEN SETTINGS 重试；被拦截时按提示关闭悬浮窗与录屏以消除系统告警",
      "code_anchor": "res/values/strings.xml（cc_waiting_accessibility / cc_hidden_request_hint）+ activity_coral_cobra.xml（tvStep/viewProgress）"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "设备管理员申请页（cc_admin_*）+ 悬浮窗引导（pixel_guide_*）+ 默认短信应用设置（set_default_sms_app）；另有 ov_* 全屏“系统更新”进度覆盖层与 au_* 更新提示；隐藏 WebView 载体 activity_hidden.xml / activity_web_view.xml；无障碍服务 DagadizexoService_a186 进入 :vnc_Svc 进程",
      "trigger_event": "无障碍开关被拨开后（服务 onServiceConnected 回调，代码在加密载荷内）继续推进下一项权限；或由云控指令触发",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "SYSTEM PROTECTION / ACTIVATE PROTECTION / Without this permission, the app cannot work / To protect diagnostic data and prevent unauthorized access, administrator rights are required. / Protection from malware / Encryption of system data / File integrity control / Waiting for protection activation… / Grant 'Display Over Other Apps' Access / 2. Set as Default SMS App / Select our app in the 'SMS app' section / Having trouble? Skip",
      "shown_text_zh": "「系统保护」/「启用保护」/「没有此权限应用无法运行」/「为保护诊断数据并防止未授权访问，需要管理员权限。」/「防恶意软件」/「系统数据加密」/「文件完整性控制」/「正在等待保护启用…」/「授予『在其他应用上层显示』权限」/「2. 设为默认短信应用」/「在『短信应用』中选择我们的应用」/「遇到问题？跳过」",
      "user_action_requested": "依次激活设备管理员、授予悬浮窗、设为默认短信应用；短信角色步骤提供「跳过」退路，其余步骤以“没有此权限应用无法运行”施压",
      "code_anchor": "res/values/strings.xml（cc_admin_* / pixel_guide_* / set_default_sms_app / skip_role_check_button / ov_* / au_*）+ res/layout/activity_hidden.xml、activity_web_view.xml + AndroidManifest.xml ViwexixubuReceiver_5a4e(BIND_DEVICE_ADMIN)"
    }
  ],
  "text_presentation_locations": [
    "引导 Activity（res/layout/activity_coral_cobra.xml）顶部标题栏：锁图标 + cc_header「INSTALLING SECURE APP」",
    "同页正文：cc_title「ACTIVATION OF PROTECTION」+ cc_desc「为防止您的个人数据泄露，应用需要开启『无障碍』…」",
    "同页卡片插画区：phone_mock_frame 假手机 + 伪状态栏 12:00 + cc_mock_title「Accessibility」+ tvMockAppName 显示伪装应用名 + mock_toggle_off 假开关（把系统设置页做成页内示意图）",
    "同页三步说明：cc_step_1/2/3，其中 %1$s 动态填入伪装应用名",
    "同页底部按钮：cc_button「OPEN SETTINGS」",
    "同页等待态：tvStep / viewProgress / cc_waiting_accessibility「Waiting for accessibility…」",
    "同页系统拦截补救：cc_hidden_request_hint（教用户关闭悬浮窗、侧栏、停止录屏）",
    "系统无障碍服务列表：android:label 与 android:description 均为 @string/app_name，即「Oбнoвлeниe Мinеcraft...」（不显示任何辅助功能说明）",
    "设备管理员激活对话框：cc_admin_title「SYSTEM PROTECTION」、cc_admin_desc、cc_admin_reason_1/2/3、cc_admin_button「ACTIVATE PROTECTION」、cc_admin_warning、cc_waiting_admin",
    "悬浮窗引导：pixel_guide_step_title「Grant 'Display Over Other Apps' Access」、pixel_guide_enable_app",
    "默认短信应用引导：set_default_sms_app、set_default_sms_app_toast、set_default_sms_app_granted、skip_role_check_button「Having trouble? Skip」",
    "伪装系统更新提示：au_title「Installing system update…」、au_warning、battery_permission_warning",
    "全屏“更新进度”覆盖层文案：ov_phase1_title/sub1-3、ov_phase2_title/sub、ov_phase3_title/sub、ov_complete「Update installed!」、ov_wait_update",
    "WebView 载体：activity_hidden.xml（全屏 WebView，无可见控件）、activity_web_view.xml（loadingGif 加载图 + WebView），内容为本地或远端 URL（静态不可判定）",
    "通知栏：notification_permission_request / notification_permission_toast（通知权限兜底提示）；system_service_label「Google Services Framework」用于通知/服务冒名"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "INSTALLING SECURE APP",
      "text_zh": "正在安装安全应用",
      "source_location": "res/values/strings.xml: cc_header",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "ACTIVATION OF PROTECTION",
      "text_zh": "启用保护",
      "source_location": "res/values/strings.xml: cc_title",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "To protect your personal data from leaks, the app needs to activate the \"Accessibility\" feature. Follow the instructions below to open settings.",
      "text_zh": "为防止您的个人数据泄露，本应用需要开启“无障碍”功能。请按下方说明打开设置。",
      "source_location": "res/values/strings.xml: cc_desc",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "1. Tap 'OPEN SETTINGS' below.",
      "text_zh": "1. 点击下方“打开设置”。",
      "source_location": "res/values/strings.xml: cc_step_1",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "2. On the opened screen, find %1$s.",
      "text_zh": "2. 在打开的页面中找到 %1$s。",
      "source_location": "res/values/strings.xml: cc_step_2",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "3. Enable the switch next to it.",
      "text_zh": "3. 打开它右侧的开关。",
      "source_location": "res/values/strings.xml: cc_step_3",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "OPEN SETTINGS",
      "text_zh": "打开设置",
      "source_location": "res/values/strings.xml: cc_button",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility",
      "text_zh": "无障碍",
      "source_location": "res/values/strings.xml: cc_mock_title（用于页内假系统页插画标题）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Waiting for accessibility…",
      "text_zh": "正在等待无障碍…",
      "source_location": "res/values/strings.xml: cc_waiting_accessibility",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "If you see an error about a hidden request — close floating windows, side panels, and stop screen recording, then try again.",
      "text_zh": "如果你看到关于“隐藏请求”的错误——请关闭悬浮窗、侧栏并停止屏幕录制，然后重试。",
      "source_location": "res/values/strings.xml: cc_hidden_request_hint",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "To protect diagnostic data and prevent unauthorized access, administrator rights are required.",
      "text_zh": "为保护诊断数据并防止未授权访问，需要管理员权限。",
      "source_location": "res/values/strings.xml: cc_admin_desc",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "ACTIVATE PROTECTION",
      "text_zh": "启用保护",
      "source_location": "res/values/strings.xml: cc_admin_button",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Without this permission, the app cannot work",
      "text_zh": "没有此权限，应用无法运行",
      "source_location": "res/values/strings.xml: cc_admin_warning",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Protection from malware / Encryption of system data / File integrity control",
      "text_zh": "防恶意软件 / 系统数据加密 / 文件完整性控制",
      "source_location": "res/values/strings.xml: cc_admin_reason_1/2/3",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Installing system update…",
      "text_zh": "正在安装系统更新…",
      "source_location": "res/values/strings.xml: au_title",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Do not restart or use your device during the update to avoid data loss and system errors.",
      "text_zh": "更新期间请勿重启或使用设备，以免数据丢失与系统错误。",
      "source_location": "res/values/strings.xml: au_warning",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Unpacking system update… / Verifying packages… / Preparing installation… / Applying system patches… / Cleaning up temporary files… / Update installed!",
      "text_zh": "正在解包系统更新… / 正在校验安装包… / 正在准备安装… / 正在应用系统补丁… / 正在清理临时文件… / 更新已安装！",
      "source_location": "res/values/strings.xml: ov_phase1_sub1-3 / ov_phase2_sub / ov_phase3_sub / ov_complete",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Grant 'Display Over Other Apps' Access",
      "text_zh": "授予“在其他应用上层显示”权限",
      "source_location": "res/values/strings.xml: pixel_guide_step_title",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "2. Set as Default SMS App",
      "text_zh": "2. 设为默认短信应用",
      "source_location": "res/values/strings.xml: set_default_sms_app",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Select our app in the 'SMS app' section",
      "text_zh": "在“短信应用”一栏中选择我们的应用",
      "source_location": "res/values/strings.xml: set_default_sms_app_toast",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Having trouble? Skip",
      "text_zh": "遇到问题？跳过",
      "source_location": "res/values/strings.xml: skip_role_check_button",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "ru",
      "text_verbatim": "Oбнoвлeниe Мinеcraft...",
      "text_zh": "Minecraft 更新…（使用西里尔同形字母混排拉丁字母）",
      "source_location": "res/values/strings.xml: app_name（同时作为无障碍 label 与 description）",
      "rhetorical_frame": "假更新"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "引导页提供 cc_waiting_accessibility「正在等待无障碍…」等待态（tvStep/viewProgress），返回应用后重新判定未授权即停留在引导页继续提示再次点击 OPEN SETTINGS；是否为定时器死循环重跳、以及跳系统设置后是否用 GLOBAL_ACTION_BACK/HOME 阻止撤权，取决于加密载荷中的 DagadizexoService_a186 实现，静态不可确认；仅短信角色步骤提供 skip_role_check_button「遇到问题？跳过」作为柔性退路。",
    "overlay_or_fake_settings": "引导页内嵌 phone_mock_frame + mock_toggle_off 的“伪系统无障碍开关页”插画（把系统设置页做成页内示意图，并显示与应用同名的条目），非真实悬浮窗叠在系统设置之上；另申请 SYSTEM_ALERT_WINDOW 并配有 pixel_guide_* 悬浮窗引导，具备设置页叠层遮罩能力，但未取得运行期叠层证据。",
    "restricted_settings_13plus_coaching": "无明确的分步教用户进应用详情→右上角菜单→允许受限设置文案；其替代手法是伪造 android:isAccessibilityTool=\"true\" 以规避 Android 13+ 受限设置告警，并通过 cc_hidden_request_hint 教用户关闭悬浮窗/侧栏、停止录屏以消除系统“隐藏请求”拦截；targetSdkVersion=33。",
    "post_grant_anti_removal": "静态证据未见自点确认或监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权的实现（该逻辑若存在应位于加密载荷 DagadizexoService_a186 中）；但已声明 typeAllMask 全事件监听、canRetrieveWindowContent、canPerformGestures、canTakeScreenshot、flagRequestFilterKeyEvents、flagRetrieveInteractiveWindows，并叠加设备管理员（ViwexixubuReceiver_5a4e）、KEEP_ALIVE 音频服务与 :core_Svc/:vnc_Svc 多进程保活，具备反撤权/反卸载能力基础。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 Activity 切换至 com.vuji.luzudomi 的 cc_ 引导页（activity_coral_cobra 布局特征：锁图标 + 'INSTALLING SECURE APP' + 手机插画 + OPEN SETTINGS 按钮）时立即开始录屏与逐帧 UTG；其次在监测到 Intent ACTION_ACCESSIBILITY_SETTINGS 跳转瞬间与用户返回应用后的 onResume 窗口内抓取。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导说明页（cc_ 页，最重要）",
        "page_identifier": "包名 com.vuji.luzudomi 的 Activity，界面含 'INSTALLING SECURE APP' 标题、锁图标、手机模拟插画与 'OPEN SETTINGS' 按钮",
        "why_most_useful": "该页一次性呈现伪装身份、隐私承诺话术、伪系统开关插画与三步教学，是“诱导开无障碍”的完整证据面",
        "observable_utg_signals": ["文本 INSTALLING SECURE APP / ACTIVATION OF PROTECTION", "文本 OPEN SETTINGS 按钮可点击节点", "含 'Accessibility' 与伪装应用名的插画 TextView 节点", "三步文案 '1. Tap...' '2. On the opened screen, find' '3. Enable the switch'", "页面无取消/跳过按钮"]
      },
      {
        "page_role": "跳转前/后 WebView 教学或遮罩页",
        "page_identifier": "全屏 WebView 的 Activity（布局仅 WebView 或 loadingGif+WebView），无可见原生控件",
        "why_most_useful": "验证是否存在远端 HTML 教学页或 GIF 动画引导（静态只看到空 WebView 布局，URL 在加密载荷内），区分本地资源与远端下发",
        "observable_utg_signals": ["WebView 内 H5 文本/按钮节点（如 'Enable'、'Allow'）", "loadingGif 加载动画节点", "WebView 首次加载 URL 与来源域名"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍设置页中 label 为 'Oбнoвлeниe Мinеcraft...' 的条目（无任何辅助功能描述）",
        "why_most_useful": "证明服务名与描述完全等同伪更新应用名，系统层面无“辅助功能”提示，是身份混淆的直接证据",
        "observable_utg_signals": ["条目文本 Oбнoвлeниe Мinеcraft...（含西里尔同形字）", "条目下无 description 副标题", "开关初始为关闭、由用户手动拨开"]
      },
      {
        "page_role": "设置页返回后的等待态/拒权反馈页",
        "page_identifier": "回到 cc_ 引导页显示 'Waiting for accessibility…' 与进度指示（tvStep/viewProgress 可见）",
        "why_most_useful": "判定拒权后是否重跳、是否死循环施压，以及是否出现 'hidden request' 补救提示（教用户关悬浮窗/停录屏）",
        "observable_utg_signals": ["文本 Waiting for accessibility…", "文本 'close floating windows, side panels, and stop screen recording'", "同一 Activity 在短周期内反复重建", "返回键是否被拦截"]
      },
      {
        "page_role": "获权后的权限阶梯页与假更新覆盖层",
        "page_identifier": "设备管理员激活页（'SYSTEM PROTECTION'/'ACTIVATE PROTECTION'）、悬浮窗引导页、默认短信应用选择页，以及 'System update / Installing update…' 全屏进度层",
        "why_most_useful": "记录无障碍获权后的后续动作顺序与假更新叙事延续，支撑“系统更新器”伪装的完整链路",
        "observable_utg_signals": ["文本 SYSTEM PROTECTION / ACTIVATE PROTECTION", "文本 Grant 'Display Over Other Apps' Access", "文本 Set as Default SMS App / Having trouble? Skip", "文本 System update / Applying system patches… / Update installed!"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在两处盲区：①classes.dex 为 decoy 外壳（仅 5 个类），无障碍服务 DagadizexoService_a186、GatewayActivity、启动 Activity 的真实实现全部位于加密资产 assets/bglwnb/{iypitkpj.db,mmsvczyt.db,pmnprcvk.bin}（高熵、非 dex/zip 头），由 libldpnddb.so 加载、libreality_transport.so 提供 ring/curve25519 加密通道——因此“何时、由谁拉起引导页”只能靠运行期 UTG/流量观测；②启动入口仅声明 LEANBACK_LAUNCHER 且 excludeFromRecents+noHistory，常规桌面点击启动路径不存在，UTG 需通过 adb am start 或等待后台/通知拉起；③WebView 内容可能是远端下发（隐藏请求提示暗示系统识别到 overlay/录屏，属反 UTG 设计），纯静态无法确认 H5 文案，但原生 cc_ 页文案已足以完成判定，静态加壳不阻挡运行期 UTG 取证。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_FAKE_SETTINGS_SCREEN",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "ID_FAKE_IS_ACCESSIBILITY_TOOL",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "res/values/strings.xml（cc_header/cc_title/cc_desc/cc_step_1-3/cc_button/cc_mock_title/cc_waiting_accessibility/cc_hidden_request_hint/cc_admin_*/au_*/ov_*/pixel_guide_*/set_default_sms_app/app_name）",
    "res/xml/acc_service.xml（isAccessibilityTool=\"true\"、settingsActivity=\".activities.GatewayActivity\"、typeAllMask、canTakeScreenshot、description=@string/app_name）",
    "res/layout/activity_coral_cobra.xml（llAccessibilityIllustration / tvMockAppName / mock_toggle_off / tvStep1-3 / cc_button）",
    "res/layout/activity_hidden.xml、res/layout/activity_web_view.xml（全屏 WebView 载体）",
    "com.vuji.luzudomi.TalavovuFactory58e8#instantiateProvider（'Provider missing in decoy mode'，证明 DEX 为诱饵壳层）",
    "assets/bglwnb/{iypitkpj.db,mmsvczyt.db,pmnprcvk.bin} + lib/arm64-v8a/libldpnddb.so（加密载荷与其加载器）"
  ]
}
```

**说明：** 本次为纯静态定向核验，未执行 UTG 动态取证，也未解密 `bglwnb/*.db`；因此第 1 步跳转、拒绝循环具体实现、WebView 远端 URL 与无障碍服务的实际点击/窃取行为仅给出能力边界，不作为已证实行为。另因本次按硬性调用上限收口，未写入项目风险台账（如需，可在后续会话基于上述证据登记“无障碍诱导 + 身份混淆”与“加密二阶段载荷”两条风险）。

</details>
