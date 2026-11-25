# MB_154__e907e2a4dc｜Vultur — Piccolo Filemanager

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：120.5s

## 1. 一句话核心结论

- **核心申请方式**：以「Piccolo Filemanager」文件管理器外壳和「Antivirus Protection」无障碍服务名伪装，通过开机自启的前台服务在后台无限循环拉起透明 WebView 意语安全话术页并反复跳转系统无障碍设置，用户返回即重跳，直到开启无障碍为止。
- **静态可见性说明**：Activity/Service 跳转链、循环逻辑、通知构造与设置 Intent 全部静态可读；但 WebView 实际展示的 HTML 与多项字符串键经 AES/ECB(PKCS5) 硬编码密钥解密后取自 SharedPreferences，可由 FCM MessagingService 与远端配置改写，最终文案不可完全静态还原；未发现加壳/VMP/二阶段 dex。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `e907e2a4dc7455d068b1f5a28fbda8ea8abdb30e0c19a6200083ad2fb607961d` |
| 包名 / 年份 | `com.trouba.terrasse` / 2023 |
| 家族 / 品类 | **Vultur**（同池样本数：2） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Piccolo Filemanager |
| 引导页宣称品牌/身份 | Antivirus Protection（虚构的杀毒/安全防护服务，冒充系统级安全组件） |
| 系统无障碍列表服务名 | Antivirus Protection |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍说明用 === ENG / === IT / === NL / === FR 多语种分段堆叠填充 android:description，把真实能力（typeAllMask 全事件、canRetrieveWindowContent、canPerformGestures）完全掩盖；accessibility_service_summary 留空；界面文案以 AES/ECB 解密形式存放于 SharedPreferences 而非 strings 资源；引导页使用 Theme.Translucent.NoTitleBar 全屏透明 Activity 叠加在系统设置之上，用户难以辨识来源应用。 |
| 无障碍服务类名 | `com.trouba.terrasse.services.AcService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `QUERY_ALL_PACKAGES, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | === ENG<br>We are very sensitive for your safety, this service check your phone parameters from third party changes<br>=== IT<br>Siamo molto sensibili per la tua sicurezza, questo servizio controlla i parametri del tuo telefono da modifiche di terze parti<br>=== NL<br>We zijn erg gevoelig voor uw veiligheid, deze service controleert de parameters van uw telefoon tegen wijzigingen van derden<br>=== FR<br>Nous sommes très sensibles pour votre sécurité, ce service vérifie les paramètres de votre téléphone contre les changements de tiers |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.trouba.terrasse.BootReceiver → com.trouba.terrasse.WebViewService（前台服务）；另 MainActivity.onCreate 亦触发 p70.a 检测 | android.intent.action.BOOT_COMPLETED / QUICKBOOT_POWEROFF 广播，或用户点击图标启动 MainActivity | 通知栏 | **原文**：Action required<br>**译注**：需要您操作（通知标题） | 无直接操作；通知点击后被引导至系统无障碍设置页，无忽略/关闭选项设计 | `com.trouba.terrasse.BootReceiver#onReceive；com.trouba.terrasse.WebViewService#a` |
| 2 | 业务功能触发 | com.trouba.terrasse.WebViewService 后台线程循环 while(!p70.a(this)) | onStartCommand → new Thread(x60).start()，随后 WebViewService.a() 取得 WakeLock 并循环检测无障碍是否已启用 | 原生Activity | **原文**：Action required<br>**译注**：持续显示「需要您操作」通知并保持前台服务存活 | 无；等待配置间隔（默认 30 秒，SharedPreferences 可调）后自动弹出下一步引导页 | `com.trouba.terrasse.WebViewService#a；c.p70#a(android.content.Context)` |
| 3 | 引导说明页 | com.trouba.terrasse.activity.WebViewActivity（android:theme=Theme.Translucent.NoTitleBar 全屏透明 Activity 内嵌 WebView） | WebViewService.a() 中 SDK<29 分支调用 WebViewActivity.a(Context)，以 FLAG_ACTIVITY_NEW_TASK 直接弹出；WebViewActivity#a 解密 HTML 后 loadData | 本地HTML WebView | **原文**：Grazie per averci scelto. Per motivi di sicurezza è necessario attivare il servizio Protezione antivirus. Toccare Servizi installati, quindi attivare il menu Protezione antivirus<br>**译注**：感谢您选择我们。出于安全原因，必须启用「病毒防护」服务。请点击「已安装的服务」，然后启用「病毒防护」菜单。 | 按指引进入已安装服务列表并启用「Protezione antivirus」；页面无取消、跳过或关闭按钮，点击屏幕任意位置即 finish() 并跳转系统设置 | `com.trouba.terrasse.activity.WebViewActivity#a()；res/values/strings.xml#L62 html_text_start` |
| 4 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | WebViewActivity.onPause() → b() 立即 startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS").setFlags(1887436800)) | 系统无障碍页 | **原文**：无（系统页面）<br>**译注**：系统无障碍设置列表，其中含名为「Antivirus Protection」的条目 | 要求用户在列表中找到并开启「Antivirus Protection」；本应用不提供任何退出该流程的入口 | `com.trouba.terrasse.activity.WebViewActivity#onPause；com.trouba.terrasse.activity.WebViewActivity#b` |
| 5 | 遮罩叠层指引 | com.trouba.terrasse.activity.HelpActivity（透明全屏 Activity + WebView，由 AccessibilityRequestService.a() 以 HelpActivity.i 动作拉起） | AccessibilityRequestService.a() 循环中 i3%(i2*2)==0 时调用 HelpActivity.a(this, HelpActivity.i)；用户从系统设置返回后 HelpActivity.onStop 在 i 动作下 sleep 1s 再以 j 动作重新拉起自身 | 悬浮窗Overlay | **原文**：Oh ah, hai dimenticato di attivare il servizio di protezione antivirus. Fallo ora<br>**译注**：哎呀，你忘了启用病毒防护服务。现在就去开启。 | 再次被要求前往设置开启服务；j 动作页面点击后 finish()，但 onStop 会再次重拉，形成返回即叠层 | `com.trouba.terrasse.activity.HelpActivity#a()；com.trouba.terrasse.activity.HelpActivity#onStop；res/values/strings.xml#L60 html_text_a11y` |
| 6 | 拒权反馈循环 | com.trouba.terrasse.AccessibilityRequestService 循环线程 + 常驻通知 | 用户未开启无障碍或按返回键离开设置页：p70.a() 返回 false，循环继续；每 30 次迭代重跳 ACCESSIBILITY_SETTINGS，每 2×配置值 次改拉 HelpActivity | 通知栏 | **原文**：For security reason you need to turn on %1$s by %2$s<br>**译注**：出于安全原因，您需要通过 %2$s 开启 %1$s。 | 无有效拒绝路径；通知 contentIntent 直接指向无障碍设置页，进程由 WakeLock + FOREGROUND_SERVICE 维持不被回收 | `com.trouba.terrasse.AccessibilityRequestService#a()；com.trouba.terrasse.AccessibilityRequestService#d()；res/values/strings.xml#L4 a11_request_message` |
| 7 | 获权后动作 | com.trouba.terrasse.services.AcService 无障碍服务激活；各引导 Activity 与通知回收 | p70.a(Context) 通过 AccessibilityManager.getEnabledAccessibilityServiceList 检测到本包服务已启用 → 循环 break，b80.a(this) 撤销通知，WebViewService.b=false | 系统无障碍页 | 无 | 无；未发现获权后自点确认或阻止用户撤权的逻辑 | `com.trouba.terrasse.AccessibilityRequestService#a()；c.p70#a(android.content.Context)；res/xml/ac_config.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- WebViewActivity 全屏透明 Activity 内的 WebView（loadData 注入 AES 解密后的 HTML，意大利语 html_text_start 指引文案）
- HelpActivity 透明 Activity 内的 WebView 叠层（html_text_a11y：『Oh ah, hai dimenticato di attivare il servizio di protezione antivirus. Fallo ora』）
- 系统无障碍设置列表中的服务条目：label=Antivirus Protection，description 为 ENG/IT/NL/FR 四语安全话术（res/values/strings.xml L33-L41）
- 常驻前台通知：标题 res/values/strings.xml#L64 notification_title『Action required』、正文 a11_request_message / html_text_notification，点击直达 ACCESSIBILITY_SETTINGS
- 应用关闭对话框：close_dialog_title_9『Attention!』+ close_dialog_message_9『This update is incompatible with the current version of the Play Store and will be removed』（CloseAppDialogActivity，假更新话术）
- res/values/strings.xml 中预留但本链未直接引用的通用诱导串：a11_request_title『Action required』、a11_request_button『Open settings』、please_enable_service『Please enable %1$s service』

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| it | Grazie per averci scelto. Per motivi di sicurezza è necessario attivare il servizio Protezione antivirus. Toccare Servizi installati, quindi attivare il menu Protezione antivirus | 感谢您选择我们。出于安全原因，必须启用「病毒防护」服务。请点击「已安装的服务」，然后启用「病毒防护」菜单。 | `res/values/strings.xml key=html_text_start（经 WebViewActivity#a 解密注入 WebView）` | 假反诈安全 |
| it | Oh ah, hai dimenticato di attivare il servizio di protezione antivirus. Fallo ora | 哎呀，你忘了启用病毒防护服务。现在就去开启。 | `res/values/strings.xml key=html_text_a11y（HelpActivity 叠层 WebView）` | 假反诈安全 |
| it | Abilita la protezione antivirus per la tua sicurezza | 为了您的安全，请启用病毒防护。 | `res/values/strings.xml key=html_text_notification` | 假反诈安全 |
| en | For security reason you need to turn on %1$s by %2$s | 出于安全原因，您需要通过 %2$s 开启 %1$s。 | `res/values/strings.xml key=a11_request_message` | 假反诈安全 |
| en | === ENG We are very sensitive for your safety, this service check your phone parameters from third party changes === IT Siamo molto sensibili per la tua sicurezza, questo servizio controlla i parametri del tuo telefono da modifiche di terze parti === NL We zijn erg gevoelig voor uw veiligheid, deze service controleert de parameters van uw telefoon tegen wijzigingen van derden === FR Nous sommes très sensibles pour votre sécurité, ce service vérifie les paramètres de votre téléphone contre les changements de tiers | 【英】我们对您的安全非常敏感，本服务检查您手机的参数是否被第三方更改【意】【荷】【法】同义重复 | `res/values/strings.xml key=accessibility_service_description（系统无障碍列表说明，ac_config.xml 引用）` | 假反诈安全 |
| en | Antivirus Protection | 病毒防护（无障碍服务名，与桌面名 Piccolo Filemanager 不符） | `res/values/strings.xml key=accessibility_service_label` | 清理工具伪装 |
| en | This update is incompatible with the current version of the Play Store and will be removed | 此更新与当前版本的 Play 商店不兼容，将被移除。 | `res/values/strings.xml key=close_dialog_message_9（CloseAppDialogActivity）` | 假更新 |
| en | Action required | 需要您操作 | `res/values/strings.xml key=notification_title / a11_request_title` | 故障恐吓 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`background_relaunch`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：三层循环叠加：①WebViewService#a 在 while(!p70.a()) 中按配置间隔反复拉起 WebViewActivity；②AccessibilityRequestService#a 每 30 次迭代（约 15 秒）无条件重跳 android.settings.ACCESSIBILITY_SETTINGS，每 2×配置值 次改拉 HelpActivity 叠层；③HelpActivity#onStop 在 i 动作下 Thread.sleep(1000) 后立即以 j 动作重新 startActivity 自身，用户从系统设置返回即被再次覆盖。全程由 WakeLock 与 FOREGROUND_SERVICE 维持进程存活，无次数上限。
- **遮罩叠层 / 高仿系统设置页**：使用 Theme.Translucent.NoTitleBar 的全屏透明 Activity（WebViewActivity / HelpActivity）+ WebView 叠放在系统无障碍设置之上作为引导遮罩；未伪造系统开关控件，但透明叠层使用户难以判断内容来源。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间（由 WebViewActivity#onPause 或 AccessibilityRequestService#a 触发）立即截图，可稳定捕获前置透明 WebView 引导页；另在 BOOT_COMPLETED 广播后 10-40 秒窗口内周期性截图，可捕获冷启动自动弹出的 WebViewActivity。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：WebView 内容由 AES/ECB 解密自 SharedPreferences 且可由 FCM 远端改写，若下发的 HTML 为纯图片或无文本 DOM，则 UTG 文本节点提取会失效，需回退到截图 OCR；此外该应用使用透明 Activity 而非真正的 WindowManager 悬浮窗，部分仅检测 TYPE_APPLICATION_OVERLAY 的方案会漏检。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动/后台自动弹出的引导说明页（WebViewActivity）** | 透明无标题全屏 Activity，背景色透明（setBackgroundColor(0)）叠加在桌面之上，内部为 WebView 渲染的意大利语文本，窗口动画为 0 | 这是用户首次接触的诱导界面，可直接证明应用在用户未做任何操作时自动弹出安全话术并要求开启服务，是强制引导链的起点 | Activity 名 com.trouba.terrasse.activity.WebViewActivity 且主题为透明；界面文本含『Protezione antivirus』『Servizi installati』；无任何取消/关闭按钮控件节点；弹出时机无对应点击事件 |
| **系统无障碍服务列表项（Antivirus Protection）** | 系统 Settings 无障碍页内服务条目，标签为 Antivirus Protection，说明区为 ENG/IT/NL/FR 四段重复文本 | 证明伪装身份与真实能力不匹配：条目名冒充杀毒服务，而应用桌面名为文件管理器 | 服务名 Antivirus Protection 与已安装应用名 Piccolo Filemanager 不一致；description 含 === ENG / === IT 分段标记；summary 为空 |
| **从系统设置返回后的叠层再引导页（HelpActivity）** | 另一透明全屏 Activity，文本为『Oh ah, hai dimenticato di attivare il servizio di protezione antivirus. Fallo ora』 | 证明拒绝/返回后的循环重跳行为，是判定『强制不可取消』的核心运行期证据 | HelpActivity 在用户按返回键后 1 秒内再次出现在前台；界面文本含『Fallo ora』催促语；同一引导界面在短时间窗口内重复出现多次 |
| **常驻通知（Action required）** | 通知栏条目，标题 Action required，正文为安全提示，点击直接进入无障碍设置 | 证明诱导不依赖用户主动打开应用，由前台服务常驻推送 | 通知标题 Action required；通知来源为 com.trouba.terrasse 前台服务；点击后落点为 android.settings.ACCESSIBILITY_SETTINGS |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.trouba.terrasse.activity.WebViewActivity#onPause`
- `com.trouba.terrasse.activity.WebViewActivity#a()`
- `com.trouba.terrasse.AccessibilityRequestService#a()`
- `com.trouba.terrasse.activity.HelpActivity#onStop`
- `com.trouba.terrasse.WebViewService#a`
- `res/values/strings.xml#L41 accessibility_service_label / res/xml/ac_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点

**身份伪装（静态确认）**
- 桌面名 `Piccolo Filemanager`（文件管理器），无障碍服务标签却为 `Antivirus Protection`，见 [strings.xml (lines 41-44)](<resource-unit:#1 file:res/values/strings.xml#L41-L44>)。
- 无障碍说明用 ENG/IT/NL/FR 四语重复"我们非常重视您的安全…检查手机参数"，但 [ac_config.xml](<resource-unit:#1 file:res/xml/ac_config.xml>) 实际申请 `typeAllMask` + `canRetrieveWindowContent` + `canPerformGestures`，说明与能力严重不符。

**引导链（纯运行期流转）**
1. **冷启动/开机**：[BootReceiver.onReceive()](<resource-unit:#1.dex1 code:com.trouba.terrasse.BootReceiver#onReceive>) 或 MainActivity 拉起 [WebViewService](<resource-unit:#1.dex1 code:com.trouba.terrasse.WebViewService#onStartCommand>) 前台服务。
2. **后台轮询**：[WebViewService.a()](<resource-unit:#1.dex1 code:com.trouba.terrasse.WebViewService#a>) 内 `while(!p70.a(this))` 循环，先弹 `Action required` 通知并持有 WakeLock。
3. **全屏透明 WebView 引导页**：[WebViewActivity.a()](<resource-unit:#1.dex1 code:com.trouba.terrasse.activity.WebViewActivity#a>) 用 AES/ECB 硬编码密钥（[c.v90.a](<resource-unit:#1.dex1 code:c.v90#a>)）解密 SharedPreferences 中的 HTML，替换占位后 `loadData`；文案为意大利语"Grazie per averci scelto… attivare il servizio Protezione antivirus"。
4. **失焦即跳设置**：[WebViewActivity.onPause()](<resource-unit:#1.dex1 code:com.trouba.terrasse.activity.WebViewActivity#onPause>) → [b()](<resource-unit:#1.dex1 code:com.trouba.terrasse.activity.WebViewActivity#b>) 直接 `startActivity("android.settings.ACCESSIBILITY_SETTINGS")`；点屏幕任意处即 `finish()`，无取消/跳过。
5. **返回即重跳 + 叠层**：[AccessibilityRequestService.a()](<resource-unit:#1.dex1 code:com.trouba.terrasse.AccessibilityRequestService#a>) 每 30 次迭代（约 15s）重跳无障碍设置，每 `2×配置值` 次改由 [HelpActivity.a(Context, String)](<resource-unit:#1.dex1 code:com.trouba.terrasse.activity.HelpActivity#a>) 叠加透明 WebView 引导层；[HelpActivity.onStop()](<resource-unit:#1.dex1 code:com.trouba.terrasse.activity.HelpActivity#onStop>) 在 `i` 动作下 sleep 1s 后以 `j` 动作重新拉起自身。
6. **通知二次诱导**：[AccessibilityRequestService.d()](<resource-unit:#1.dex1 code:com.trouba.terrasse.AccessibilityRequestService#d>) 常驻通知 `Action required`，`contentIntent` 直指无障碍设置页。
7. **获权后**：`p70.a()` 返回 true → 各循环退出、通知撤销、服务释放（无撤权自保逻辑）。

**关键判断**：无 `ACTION_APPLICATION_DETAILS_SETTINGS`、无 restricted settings 教学（targetSdk 28）、无假开关页；核心手段是**后台无限重跳 + 透明叠层 WebView 话术**，属"假反诈/杀毒安全"恐吓式强制授权。

**静态可见性**：控制流完全可见；但界面最终 HTML 文案与部分键值经 AES 解密且可由 FCM/远端配置改写，故为 `partial_dynamic_or_remote`。

已登记风险：**R-001**（high / deceptive_behavior）。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "Activity/Service 跳转链、循环逻辑、通知构造与设置 Intent 全部静态可读；但 WebView 实际展示的 HTML 与多项字符串键经 AES/ECB(PKCS5) 硬编码密钥解密后取自 SharedPreferences，可由 FCM MessagingService 与远端配置改写，最终文案不可完全静态还原；未发现加壳/VMP/二阶段 dex。",
  "summary_one_liner": "以「Piccolo Filemanager」文件管理器外壳和「Antivirus Protection」无障碍服务名伪装，通过开机自启的前台服务在后台无限循环拉起透明 WebView 意语安全话术页并反复跳转系统无障碍设置，用户返回即重跳，直到开启无障碍为止。",
  "disguise_identity": {
    "app_display_name": "Piccolo Filemanager",
    "claimed_brand_or_persona": "Antivirus Protection（虚构的杀毒/安全防护服务，冒充系统级安全组件）",
    "a11y_service_label": "Antivirus Protection",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍说明用 === ENG / === IT / === NL / === FR 多语种分段堆叠填充 android:description，把真实能力（typeAllMask 全事件、canRetrieveWindowContent、canPerformGestures）完全掩盖；accessibility_service_summary 留空；界面文案以 AES/ECB 解密形式存放于 SharedPreferences 而非 strings 资源；引导页使用 Theme.Translucent.NoTitleBar 全屏透明 Activity 叠加在系统设置之上，用户难以辨识来源应用。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.trouba.terrasse.BootReceiver → com.trouba.terrasse.WebViewService（前台服务）；另 MainActivity.onCreate 亦触发 p70.a 检测",
      "trigger_event": "android.intent.action.BOOT_COMPLETED / QUICKBOOT_POWEROFF 广播，或用户点击图标启动 MainActivity",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "Action required",
      "shown_text_zh": "需要您操作（通知标题）",
      "user_action_requested": "无直接操作；通知点击后被引导至系统无障碍设置页，无忽略/关闭选项设计",
      "code_anchor": "com.trouba.terrasse.BootReceiver#onReceive；com.trouba.terrasse.WebViewService#a"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.trouba.terrasse.WebViewService 后台线程循环 while(!p70.a(this))",
      "trigger_event": "onStartCommand → new Thread(x60).start()，随后 WebViewService.a() 取得 WakeLock 并循环检测无障碍是否已启用",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Action required",
      "shown_text_zh": "持续显示「需要您操作」通知并保持前台服务存活",
      "user_action_requested": "无；等待配置间隔（默认 30 秒，SharedPreferences 可调）后自动弹出下一步引导页",
      "code_anchor": "com.trouba.terrasse.WebViewService#a；c.p70#a(android.content.Context)"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "com.trouba.terrasse.activity.WebViewActivity（android:theme=Theme.Translucent.NoTitleBar 全屏透明 Activity 内嵌 WebView）",
      "trigger_event": "WebViewService.a() 中 SDK<29 分支调用 WebViewActivity.a(Context)，以 FLAG_ACTIVITY_NEW_TASK 直接弹出；WebViewActivity#a 解密 HTML 后 loadData",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Grazie per averci scelto. Per motivi di sicurezza è necessario attivare il servizio Protezione antivirus. Toccare Servizi installati, quindi attivare il menu Protezione antivirus",
      "shown_text_zh": "感谢您选择我们。出于安全原因，必须启用「病毒防护」服务。请点击「已安装的服务」，然后启用「病毒防护」菜单。",
      "user_action_requested": "按指引进入已安装服务列表并启用「Protezione antivirus」；页面无取消、跳过或关闭按钮，点击屏幕任意位置即 finish() 并跳转系统设置",
      "code_anchor": "com.trouba.terrasse.activity.WebViewActivity#a()；res/values/strings.xml#L62 html_text_start"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "WebViewActivity.onPause() → b() 立即 startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\").setFlags(1887436800))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（系统页面）",
      "shown_text_zh": "系统无障碍设置列表，其中含名为「Antivirus Protection」的条目",
      "user_action_requested": "要求用户在列表中找到并开启「Antivirus Protection」；本应用不提供任何退出该流程的入口",
      "code_anchor": "com.trouba.terrasse.activity.WebViewActivity#onPause；com.trouba.terrasse.activity.WebViewActivity#b"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.trouba.terrasse.activity.HelpActivity（透明全屏 Activity + WebView，由 AccessibilityRequestService.a() 以 HelpActivity.i 动作拉起）",
      "trigger_event": "AccessibilityRequestService.a() 循环中 i3%(i2*2)==0 时调用 HelpActivity.a(this, HelpActivity.i)；用户从系统设置返回后 HelpActivity.onStop 在 i 动作下 sleep 1s 再以 j 动作重新拉起自身",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Oh ah, hai dimenticato di attivare il servizio di protezione antivirus. Fallo ora",
      "shown_text_zh": "哎呀，你忘了启用病毒防护服务。现在就去开启。",
      "user_action_requested": "再次被要求前往设置开启服务；j 动作页面点击后 finish()，但 onStop 会再次重拉，形成返回即叠层",
      "code_anchor": "com.trouba.terrasse.activity.HelpActivity#a()；com.trouba.terrasse.activity.HelpActivity#onStop；res/values/strings.xml#L60 html_text_a11y"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "com.trouba.terrasse.AccessibilityRequestService 循环线程 + 常驻通知",
      "trigger_event": "用户未开启无障碍或按返回键离开设置页：p70.a() 返回 false，循环继续；每 30 次迭代重跳 ACCESSIBILITY_SETTINGS，每 2×配置值 次改拉 HelpActivity",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "For security reason you need to turn on %1$s by %2$s",
      "shown_text_zh": "出于安全原因，您需要通过 %2$s 开启 %1$s。",
      "user_action_requested": "无有效拒绝路径；通知 contentIntent 直接指向无障碍设置页，进程由 WakeLock + FOREGROUND_SERVICE 维持不被回收",
      "code_anchor": "com.trouba.terrasse.AccessibilityRequestService#a()；com.trouba.terrasse.AccessibilityRequestService#d()；res/values/strings.xml#L4 a11_request_message"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "com.trouba.terrasse.services.AcService 无障碍服务激活；各引导 Activity 与通知回收",
      "trigger_event": "p70.a(Context) 通过 AccessibilityManager.getEnabledAccessibilityServiceList 检测到本包服务已启用 → 循环 break，b80.a(this) 撤销通知，WebViewService.b=false",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "引导层与通知消失，AcService 开始以 typeAllMask 全事件监听与手势注入能力运行",
      "user_action_requested": "无；未发现获权后自点确认或阻止用户撤权的逻辑",
      "code_anchor": "com.trouba.terrasse.AccessibilityRequestService#a()；c.p70#a(android.content.Context)；res/xml/ac_config.xml"
    }
  ],
  "text_presentation_locations": [
    "WebViewActivity 全屏透明 Activity 内的 WebView（loadData 注入 AES 解密后的 HTML，意大利语 html_text_start 指引文案）",
    "HelpActivity 透明 Activity 内的 WebView 叠层（html_text_a11y：『Oh ah, hai dimenticato di attivare il servizio di protezione antivirus. Fallo ora』）",
    "系统无障碍设置列表中的服务条目：label=Antivirus Protection，description 为 ENG/IT/NL/FR 四语安全话术（res/values/strings.xml L33-L41）",
    "常驻前台通知：标题 res/values/strings.xml#L64 notification_title『Action required』、正文 a11_request_message / html_text_notification，点击直达 ACCESSIBILITY_SETTINGS",
    "应用关闭对话框：close_dialog_title_9『Attention!』+ close_dialog_message_9『This update is incompatible with the current version of the Play Store and will be removed』（CloseAppDialogActivity，假更新话术）",
    "res/values/strings.xml 中预留但本链未直接引用的通用诱导串：a11_request_title『Action required』、a11_request_button『Open settings』、please_enable_service『Please enable %1$s service』"
  ],
  "verbatim_texts": [
    {
      "lang": "it",
      "text_verbatim": "Grazie per averci scelto. Per motivi di sicurezza è necessario attivare il servizio Protezione antivirus. Toccare Servizi installati, quindi attivare il menu Protezione antivirus",
      "text_zh": "感谢您选择我们。出于安全原因，必须启用「病毒防护」服务。请点击「已安装的服务」，然后启用「病毒防护」菜单。",
      "source_location": "res/values/strings.xml key=html_text_start（经 WebViewActivity#a 解密注入 WebView）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "it",
      "text_verbatim": "Oh ah, hai dimenticato di attivare il servizio di protezione antivirus. Fallo ora",
      "text_zh": "哎呀，你忘了启用病毒防护服务。现在就去开启。",
      "source_location": "res/values/strings.xml key=html_text_a11y（HelpActivity 叠层 WebView）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "it",
      "text_verbatim": "Abilita la protezione antivirus per la tua sicurezza",
      "text_zh": "为了您的安全，请启用病毒防护。",
      "source_location": "res/values/strings.xml key=html_text_notification",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "For security reason you need to turn on %1$s by %2$s",
      "text_zh": "出于安全原因，您需要通过 %2$s 开启 %1$s。",
      "source_location": "res/values/strings.xml key=a11_request_message",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "=== ENG We are very sensitive for your safety, this service check your phone parameters from third party changes === IT Siamo molto sensibili per la tua sicurezza, questo servizio controlla i parametri del tuo telefono da modifiche di terze parti === NL We zijn erg gevoelig voor uw veiligheid, deze service controleert de parameters van uw telefoon tegen wijzigingen van derden === FR Nous sommes très sensibles pour votre sécurité, ce service vérifie les paramètres de votre téléphone contre les changements de tiers",
      "text_zh": "【英】我们对您的安全非常敏感，本服务检查您手机的参数是否被第三方更改【意】【荷】【法】同义重复",
      "source_location": "res/values/strings.xml key=accessibility_service_description（系统无障碍列表说明，ac_config.xml 引用）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Antivirus Protection",
      "text_zh": "病毒防护（无障碍服务名，与桌面名 Piccolo Filemanager 不符）",
      "source_location": "res/values/strings.xml key=accessibility_service_label",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "This update is incompatible with the current version of the Play Store and will be removed",
      "text_zh": "此更新与当前版本的 Play 商店不兼容，将被移除。",
      "source_location": "res/values/strings.xml key=close_dialog_message_9（CloseAppDialogActivity）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Action required",
      "text_zh": "需要您操作",
      "source_location": "res/values/strings.xml key=notification_title / a11_request_title",
      "rhetorical_frame": "故障恐吓"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "background_relaunch",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "三层循环叠加：①WebViewService#a 在 while(!p70.a()) 中按配置间隔反复拉起 WebViewActivity；②AccessibilityRequestService#a 每 30 次迭代（约 15 秒）无条件重跳 android.settings.ACCESSIBILITY_SETTINGS，每 2×配置值 次改拉 HelpActivity 叠层；③HelpActivity#onStop 在 i 动作下 Thread.sleep(1000) 后立即以 j 动作重新 startActivity 自身，用户从系统设置返回即被再次覆盖。全程由 WakeLock 与 FOREGROUND_SERVICE 维持进程存活，无次数上限。",
    "overlay_or_fake_settings": "使用 Theme.Translucent.NoTitleBar 的全屏透明 Activity（WebViewActivity / HelpActivity）+ WebView 叠放在系统无障碍设置之上作为引导遮罩；未伪造系统开关控件，但透明叠层使用户难以判断内容来源。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间（由 WebViewActivity#onPause 或 AccessibilityRequestService#a 触发）立即截图，可稳定捕获前置透明 WebView 引导页；另在 BOOT_COMPLETED 广播后 10-40 秒窗口内周期性截图，可捕获冷启动自动弹出的 WebViewActivity。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动/后台自动弹出的引导说明页（WebViewActivity）",
        "page_identifier": "透明无标题全屏 Activity，背景色透明（setBackgroundColor(0)）叠加在桌面之上，内部为 WebView 渲染的意大利语文本，窗口动画为 0",
        "why_most_useful": "这是用户首次接触的诱导界面，可直接证明应用在用户未做任何操作时自动弹出安全话术并要求开启服务，是强制引导链的起点",
        "observable_utg_signals": ["Activity 名 com.trouba.terrasse.activity.WebViewActivity 且主题为透明", "界面文本含『Protezione antivirus』『Servizi installati』", "无任何取消/关闭按钮控件节点", "弹出时机无对应点击事件"]
      },
      {
        "page_role": "系统无障碍服务列表项（Antivirus Protection）",
        "page_identifier": "系统 Settings 无障碍页内服务条目，标签为 Antivirus Protection，说明区为 ENG/IT/NL/FR 四段重复文本",
        "why_most_useful": "证明伪装身份与真实能力不匹配：条目名冒充杀毒服务，而应用桌面名为文件管理器",
        "observable_utg_signals": ["服务名 Antivirus Protection 与已安装应用名 Piccolo Filemanager 不一致", "description 含 === ENG / === IT 分段标记", "summary 为空"]
      },
      {
        "page_role": "从系统设置返回后的叠层再引导页（HelpActivity）",
        "page_identifier": "另一透明全屏 Activity，文本为『Oh ah, hai dimenticato di attivare il servizio di protezione antivirus. Fallo ora』",
        "why_most_useful": "证明拒绝/返回后的循环重跳行为，是判定『强制不可取消』的核心运行期证据",
        "observable_utg_signals": ["HelpActivity 在用户按返回键后 1 秒内再次出现在前台", "界面文本含『Fallo ora』催促语", "同一引导界面在短时间窗口内重复出现多次"]
      },
      {
        "page_role": "常驻通知（Action required）",
        "page_identifier": "通知栏条目，标题 Action required，正文为安全提示，点击直接进入无障碍设置",
        "why_most_useful": "证明诱导不依赖用户主动打开应用，由前台服务常驻推送",
        "observable_utg_signals": ["通知标题 Action required", "通知来源为 com.trouba.terrasse 前台服务", "点击后落点为 android.settings.ACCESSIBILITY_SETTINGS"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "WebView 内容由 AES/ECB 解密自 SharedPreferences 且可由 FCM 远端改写，若下发的 HTML 为纯图片或无文本 DOM，则 UTG 文本节点提取会失效，需回退到截图 OCR；此外该应用使用透明 Activity 而非真正的 WindowManager 悬浮窗，部分仅检测 TYPE_APPLICATION_OVERLAY 的方案会漏检。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.trouba.terrasse.activity.WebViewActivity#onPause",
    "com.trouba.terrasse.activity.WebViewActivity#a()",
    "com.trouba.terrasse.AccessibilityRequestService#a()",
    "com.trouba.terrasse.activity.HelpActivity#onStop",
    "com.trouba.terrasse.WebViewService#a",
    "res/values/strings.xml#L41 accessibility_service_label / res/xml/ac_config.xml"
  ]
}
```

</details>
