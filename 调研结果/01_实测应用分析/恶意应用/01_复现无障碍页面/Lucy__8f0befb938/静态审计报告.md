# MR_155__8f0befb938｜Lucy — Video Player

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：272.8s

## 1. 一句话核心结论

- **核心申请方式**：伪装成开源视频播放器的恶意应用，冷启动即禁用自身启动图标并由 JobScheduler 拉起 ReqPerm 活动，用不可取消的 AlertDialog 以『必须开启 SVO 视频优化才能看视频』为由反复跳转系统无障碍设置，获权后由无障碍服务自动点击 ALLOW/OK/DONE 完成悬浮窗自授权与清空最近任务。
- **静态可见性说明**：DEX 未加壳、无加密载荷，引导链（Launcher 自禁用 → JobScheduler 5s → ReqPerm 不可取消弹窗 → ACCESSIBILITY_SETTINGS 跳转 → onActivityResult 回跳循环 → 无障碍服务自点击授权）全部可从 classes.dex 与 res/values/strings.xml 静态还原；未发现远端 HTML 或 AES 二阶段载荷参与无障碍引导。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `8f0befb9381f9b0b1253a07487456b585a2352bdbdd0e3cc2e17b29b489a8376` |
| 包名 / 年份 | `uuctvbgtlb.nkoqrtdctt.unootbawgh` / 2020 |
| 家族 / 品类 | **Lucy**（同池样本数：81） |
| 原始来源标识 | https://research.checkpoint.com/2020/lucys-back-ransomware-goes-mobile/ |
| 桌面显示名 | Video Player |
| 引导页宣称品牌/身份 | 开源视频播放器 / Streaming Video Optimization (SVO) 视频优化服务 |
| 系统无障碍列表服务名 | Streaming Video Optimization (SVO) |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务标签 @string/fake_label 在名称后塞入约 40 个换行加一个句点，把系统无障碍列表中紧随其后的能力警告/描述挤出可视区；android:description 用『开源播放器免许可费、补丁与漏洞修复更及时』的长篇话术掩盖 canRetrieveWindowContent 等真实能力；启动器组件在首次 onCreate 中用 setComponentEnabledSetting(COMPONENT_ENABLED_STATE_DISABLED) 自我禁用，桌面图标消失；包名/类名全随机化（uuctvbgtlb.nkoqrtdctt.unootbawgh.*）；服务 android:label 与 activity label（Word service / ReqPerm）互不一致。 |
| 无障碍服务类名 | `uuctvbgtlb.nkoqrtdctt.unootbawgh.bpnbunmqon` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Android Optimization must be enable, for play video in your phone.<br> Video player offer some advantages over players developed with proprietary software. Many businesses and individual users prefer to go the open source route as it does away with the procurement barrier. <br> Video players built with proprietary software use private source code and is offered via licensing where users need to pay for and agree to the different terms and conditions before being able to use the player. <br> Given the vastly improved scrutiny around security, the availability of patches and bug fixes, open source video players are free to use without licensing fees and cumbersome, contracts. Some additional benefits include |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | uuctvbgtlb.nkoqrtdctt.unootbawgh.lrplugqbfs（LAUNCHER Activity） | onCreate()：setContentView 后立即调用私有方法 a() 禁用自身组件，并调用 i.a(getApplicationContext()) 注册 5 秒延迟的 JobScheduler 任务 | 原生Activity | 无 | 无需用户操作（页面随即消失） | `uuctvbgtlb.nkoqrtdctt.unootbawgh.lrplugqbfs.onCreate / .a / uuctvbgtlb.nkoqrtdctt.unootbawgh.i.a` |
| 2 | 引导说明页 | uuctvbgtlb.nkoqrtdctt.unootbawgh.nzpdotxvtw（label=ReqPerm）内的 AlertDialog | nzpdotxvtw.onCreate() → a()；条件 bpnbunmqon.b == false（无障碍服务未连接） | 原生Dialog | **原文**：Attention! / To continue watching the video on your phone, you must enable Streaming Video Optimization (SVO), select line in the menu and turn it on!<br>**译注**：注意！/ 要在手机上继续观看视频，您必须启用流媒体视频优化（SVO），在菜单中选择该行并打开它！ | 仅有一个确定按钮（R$string.ok），setCancelable(false) 不可取消、无跳过；SDK<23 时以 WindowManager 类型 2010 悬浮窗形式弹出 | `uuctvbgtlb.nkoqrtdctt.unootbawgh.nzpdotxvtw.a(Context,String,Intent)；strings: Attention / Activate_Access` |
| 3 | 跳无障碍设置 | 系统设置页 Settings.ACTION_ACCESSIBILITY_SETTINGS（无障碍服务列表） | AlertDialog 确定按钮回调 nzpdotxvtw$1.onClick() → startActivityForResult(intent, 0) | 系统无障碍页 | 无 | 在系统无障碍列表中点击 SVO 服务开关并确认系统警告对话框 | `uuctvbgtlb.nkoqrtdctt.unootbawgh.nzpdotxvtw#a：new Intent("android.settings.ACCESSIBILITY_SETTINGS").addFlags(8388608)` |
| 4 | 拒权反馈循环 | nzpdotxvtw.onActivityResult → 再次弹出同一不可取消 AlertDialog | 用户从系统设置返回触发 onActivityResult，无条件调用 a() 重新判断 bpnbunmqon.b | 原生Dialog | **原文**：Attention! / To continue watching the video on your phone, you must enable Streaming Video Optimization (SVO), select line in the menu and turn it on!<br>**译注**：未开启则原样重弹同一提示，形成返回即重跳的死循环；只有按 HOME 或最近任务键才会临时关闭 | 无取消按钮；唯一逃逸路径是按 HOME/最近任务（被 CLOSE_SYSTEM_DIALOGS 广播监听后 dismiss 并置 bpnbunmqon.a=false、nzpdotxvtw.a=false） | `uuctvbgtlb.nkoqrtdctt.unootbawgh.nzpdotxvtw.onActivityResult / nzpdotxvtw$a.onReceive` |
| 5 | 获权后动作 | uuctvbgtlb.nkoqrtdctt.unootbawgh.bpnbunmqon（AccessibilityService）onServiceConnected / onAccessibilityEvent | 用户开启服务后 onServiceConnected()：置 b=true，startActivity(nzpdotxvtw, exit=true) 收掉残留弹窗，setServiceInfo(flags=19, eventTypes=-1, notificationTimeout=100)；随后每个无障碍事件里 findAccessibilityNodeInfosByText 并用 dispatchGesture 点击 | 不可静态还原 | **原文**：Allow display over other apps / Permit drawing over other apps / If you don’t want / DONE / CLEAR ALL / ALLOW / OK<br>**译注**：由无障碍服务自动点击系统「允许在其他应用上层显示」按钮、确认对话框与「清除全部」最近任务，用户无需再手动操作 | 无（全部由 dispatchGesture 自动点击完成），并伴随 2 秒延迟的 postDelayed 重复点击 | `uuctvbgtlb.nkoqrtdctt.unootbawgh.bpnbunmqon#onServiceConnected / #onAccessibilityEvent / #a(AccessibilityEvent,String)` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- nzpdotxvtw（ReqPerm）内不可取消 AlertDialog：标题 @string/Attention（Attention!），正文 @string/Activate_Access（Activate_Access）
- 系统无障碍列表服务条目：android:label=@string/fake_label（Streaming Video Optimization (SVO) 后接大量换行与句点）
- 系统无障碍服务详情/描述：android:description=@string/accessibility_service_description（大段开源播放器免许可费话术），由 res/xml/bqpgvctoin.xml 引用
- 应用列表/桌面名称：@string/app_name = Video Player
- manifest 中 service android:label="Word service"（JobService dtpqopbpon）与 activity android:label=@string/title_activity_req_perm（ReqPerm），均不向用户说明真实用途
- res/values/strings.xml 中 @string/Text（伪造 FBI 执法勒索 HTML 文案）与 @string/titleWhere / @string/CardHint / @string/textSend（OneVanilla $500 购卡页文案），供后续诈骗流程使用，不属本次无障碍引导页
- 无本地 HTML/WebView 引导页：本应用 assets 中未使用 HTML 承载无障碍引导文案，全部为原生字符串与代码硬编码

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Attention! | 注意！ | `res/values/strings.xml key=Attention（用于 nzpdotxvtw 弹窗标题）` | 故障恐吓 |
| en | To continue watching the video on your phone, you must enable Streaming Video Optimization (SVO), select line in the menu and turn it on! | 要在手机上继续观看视频，您必须启用流媒体视频优化（SVO），在菜单中选择该行并打开它！ | `res/values/strings.xml key=Activate_Access（nzpdotxvtw.a 弹窗正文，setCancelable(false)）` | 假更新 |
| en | Android Optimization must be enable, for play video in your phone. | 必须开启安卓优化，才能在您的手机上播放视频。 | `res/values/strings.xml key=accessibility_service_description（res/xml/bqpgvctoin.xml android:description）` | 故障恐吓 |
| en | Video player offer some advantages over players developed with proprietary software. Many businesses and individual users prefer to go the open source route as it does away with the procurement barrier. Video players built with proprietary software use private source code and is offered via licensing where users need to pay for and agree to the different terms and conditions before being able to use the player. Given the vastly improved scrutiny around security, the availability of patches and bug fixes, open source video players are free to use without licensing fees and cumbersome, contracts. Some additional benefits include | 视频播放器相比专有软件开发的播放器有一些优势。许多企业和个人用户更青睐开源路线，因为它消除了采购门槛。专有软件构建的视频播放器使用私有源码并通过许可方式提供，用户需付费并同意各种条款后才能使用。鉴于安全审查大幅改善、补丁与错误修复可得，开源视频播放器可免费使用，无需许可费与繁琐合同。其他额外好处包括…… | `res/values/strings.xml key=accessibility_service_description（系统无障碍服务描述，正文在句末被截断为 include）` | 隐私承诺 |
| en | Streaming Video Optimization (SVO)<br><br><br><br><br><br><br><br><br> <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>. | 流媒体视频优化（SVO）+ 大量空行 + 句点（用于把系统无障碍列表中的警告文字挤出屏幕可视区域） | `res/values/strings.xml key=fake_label（manifest service android:label）` | 清理工具伪装 |
| en | Allow display over other apps | 允许在其他应用上层显示 | `uuctvbgtlb.nkoqrtdctt.unootbawgh.bpnbunmqon.onAccessibilityEvent 中硬编码，用于自动点击系统悬浮窗授权按钮` | 受限设置分步教学 |
| en | Permit drawing over other apps | 允许绘制在其他应用之上 | `uuctvbgtlb.nkoqrtdctt.unootbawgh.bpnbunmqon.onAccessibilityEvent 中硬编码，用于自动点击系统悬浮窗授权按钮` | 受限设置分步教学 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：用户从系统无障碍设置返回后 onActivityResult 无条件调用 a()，若 bpnbunmqon.b 仍为 false 则原样重弹同一个 setCancelable(false) 的 AlertDialog，形成「返回即重跳」的无限循环；无障碍服务自身在未获权时也会 startActivity(nzpdotxvtw) 反复后台拉起。唯一临时逃逸是按 HOME 或最近任务键（监听 CLOSE_SYSTEM_DIALOGS 的 homekey/recentapps 后 dismiss 并置 bpnbunmqon.a=false、nzpdotxvtw.a=false）。
- **遮罩叠层 / 高仿系统设置页**：弹窗在 SDK<23 时通过 getWindow().setType(2010) 以悬浮窗层级显示；未发现伪造的高仿系统无障碍开关页或覆盖在设置页之上的半透明引导遮罩。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion 26，未涉及 Android 13+ 受限设置教学或 Session 安装器绕过）
- **获权后即时行为与防撤权机制**：有自授权行为：onServiceConnected 后服务持续在无障碍事件中按文本查找并用 dispatchGesture 自动点击 ALLOW / Permit drawing over other apps（自动授予 SYSTEM_ALERT_WINDOW）、OK、DONE 以及 CLEAR ALL（自动清空最近任务以隐藏自身痕迹）；未发现用 GLOBAL_ACTION_BACK/HOME 阻止用户撤权的逻辑。此外首次启动即以 setComponentEnabledSetting 禁用自身 LAUNCHER 组件，用户失去再次进入/管理入口。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以监测到 Intent 目标为 android.settings.ACCESSIBILITY_SETTINGS（含 FLAG_ACTIVITY_NEW_TASK）的 startActivityForResult 为最佳瞬间拉起 UTG；若设备在冷启动后 5 秒内即出现 ReqPerm（nzpdotxvtw）弹窗，也可直接以该 Activity onCreate 为触发点。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：全部引导文案均为原生字符串与代码硬编码，纯文本可由 UTG 直接提取。需注意两点运行期盲区：一是首次启动即自我禁用 LAUNCHER 组件，之后无法通过桌面图标复现引导，需在首次安装后立即抓取；二是真正的恶意业务（伪造 FBI 勒索页 @string/Text、OneVanilla $500 购卡页）在无障碍获权后才由后台服务触发，纯 UTG 若只观察无障碍引导阶段会漏掉该部分。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页** | uuctvbgtlb.nkoqrtdctt.unootbawgh.nzpdotxvtw（ReqPerm）上的 AlertDialog，标题 Attention!，正文含 Streaming Video Optimization (SVO) | 该页是引导链唯一面向用户的说明载体，且明确 setCancelable(false)、无取消/跳过，可直接判定强迫性诱导 | 弹窗无任何取消/跳过控件，仅一个确定按钮；正文出现『必须启用 SVO 才能看视频』的虚假功能前置要求；弹窗出现时无障碍服务尚未开启（开关关闭）；对话框不可通过返回键关闭 |
| **设置页后压栈遮罩/重复弹窗页** | 从 ACCESSIBILITY_SETTINGS 返回后 0~1 秒内再次出现的同一 ReqPerm 弹窗 | 证明拒权后存在回跳循环（onActivityResult → a() 重弹），是区分恶意强迫与良性一次性引导的决定性证据 | 同一 Activity 在设置返回后再次出现相同文本；无降级路径、无『稍后再说』入口；按 HOME 后弹窗消失、再次进入又出现 |
| **系统无障碍服务列表项** | 系统设置无障碍列表中 label 为 Streaming Video Optimization (SVO) 的条目，其后带大段空白 | 可直观验证换行填充挤出警告、标签与包名/应用名（Video Player）身份不一致 | 服务名称后存在异常长空白/换行，警告文字被推离可视区；服务描述出现『开源播放器免许可费』等与无障碍无关话术；列表项文本与桌面应用名 Video Player 不一致 |
| **获权瞬间的系统悬浮窗授权页** | 系统『允许在其他应用上层显示』对话框，按钮文本 Allow display over other apps / Permit drawing over other apps 被自动点击 | 捕捉无障碍服务 dispatchGesture 自动授权 SYSTEM_ALERT_WINDOW 的自点击行为，证明获权后自动化越权 | 无用户触摸事件而授权对话框被点击关闭；两次同义授权文案（Allow / Permit）先后被点击；随后出现 CLEAR ALL 使最近任务被清空 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `uuctvbgtlb.nkoqrtdctt.unootbawgh.lrplugqbfs#onCreate / #a（自我禁用 LAUNCHER 组件 + 投递 5s JobScheduler）`
- `uuctvbgtlb.nkoqrtdctt.unootbawgh.nzpdotxvtw#a(Context,String,Intent)（setCancelable(false) 的 Attention! 弹窗）`
- `uuctvbgtlb.nkoqrtdctt.unootbawgh.nzpdotxvtw$1#onClick（startActivityForResult 跳 android.settings.ACCESSIBILITY_SETTINGS）`
- `uuctvbgtlb.nkoqrtdctt.unootbawgh.nzpdotxvtw#onActivityResult（拒权回跳循环）`
- `uuctvbgtlb.nkoqrtdctt.unootbawgh.bpnbunmqon#onServiceConnected / #onAccessibilityEvent（dispatchGesture 自动点击 ALLOW/OK/DONE/CLEAR ALL）`
- `res/values/strings.xml（Activate_Access / Attention / fake_label / accessibility_service_description）与 res/xml/bqpgvctoin.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（纯运行期 UTG 视角）

**静态可见性：clear**（DEX 明文、无壳、无加密载荷，引导链完整可读）

**引导链（4 步闭环，非良性）**

1. **冷启动入口**：[lrplugqbfs.onCreate()](<resource-unit:#1.dex1 code:uuctvbgtlb.nkoqrtdctt.unootbawgh.lrplugqbfs#onCreate>) 只做两件事——先用 `setComponentEnabledSetting(..., 2, 1)` 把**自己的启动器组件禁用**（桌面图标消失，用户无法再次进入/卸载引导），再通过 `i.a()` 挂 5 秒 `JobScheduler` 定时任务，随后直接 finish。真正的前台引导由后续组件拉起，冷启动 0 步不可见。
2. **引导说明页（不可取消）**：[nzpdotxvtw.onCreate()](<resource-unit:#1.dex1 code:uuctvbgtlb.nkoqrtdctt.unootbawgh.nzpdotxvtw#onCreate>) → [a()](<resource-unit:#1.dex1 code:uuctvbgtlb.nkoqrtdctt.unootbawgh.nzpdotxvtw#a>)：若无障碍未连接（`bpnbunmqon.b == false`），弹 `AlertDialog`（`setCancelable(false)`，SDK<23 时 `setType(2010)` 走悬浮窗层级），标题 `Attention!`，正文 `To continue watching the video on your phone, you must enable Streaming Video Optimization (SVO), select line in the menu and turn it on!`，仅一个「确定」按钮，**无取消/跳过**。
3. **跳系统无障碍设置**：按钮回调 [nzpdotxvtw$1.onClick()](<resource-unit:#1.dex1 code:uuctvbgtlb.nkoqrtdctt.unootbawgh.nzpdotxvtw$1#onClick>) → `startActivityForResult(new Intent("android.settings.ACCESSIBILITY_SETTINGS").addFlags(0x800000), 0)`，直接落在系统无障碍列表，未做受限设置（Android 13+）分步教学（targetSdk 26，不需要）。
4. **拒权反馈循环**：`onActivityResult` 无条件回调 `a()`，用户从设置页返回若仍未开启则**再次弹出同一个不可取消对话框**（无限重试）；仅当用户按 HOME/最近任务（监听 `CLOSE_SYSTEM_DIALOGS` 的 `homekey`/`recentapps`，见 [nzpdotxvtw$a.onReceive()](<resource-unit:#1.dex1 code:uuctvbgtlb.nkoqrtdctt.unootbawgh.nzpdotxvtw$a#onReceive>)）才临时 dismiss 并置 `bpnbunmqon.a=false` 放行。

**获权后动作（自授权，替代人工点击）**：[bpnbunmqon.onServiceConnected()](<resource-unit:#1.dex1 code:uuctvbgtlb.nkoqrtdctt.unootbawgh.bpnbunmqon#onServiceConnected>) 置 `b=true`，`startActivity(nzpdotxvtw, exit=true)` 收掉残留弹窗，然后 `setServiceInfo(flags=19, eventTypes=-1)` 全事件监听；[onAccessibilityEvent()](<resource-unit:#1.dex1 code:uuctvbgtlb.nkoqrtdctt.unootbawgh.bpnbunmqon#onAccessibilityEvent>) 持续按文本查找并**用 `dispatchGesture` 自动点击** `ALLOW` / `Permit drawing over other apps` / `OK` / `DONE` / `CLEAR ALL` / `If you don’t want`——即自动授予 `SYSTEM_ALERT_WINDOW`、自动确认系统弹窗、自动清空最近任务（隐蔽化）。服务 [a()](<resource-unit:#1.dex1 code:uuctvbgtlb.nkoqrtdctt.unootbawgh.bpnbunmqon#a>) 还会在无障碍未开启时反复 `startActivity(nzpdotxvtw)` 后台重拉引导（`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`）。

**身份伪装**：桌面名 `Video Player`，无障碍服务名 `Streaming Video Optimization (SVO)` 后跟 **数十个换行 + 一个句点**（`@string/fake_label`），把系统列表中的警告/描述挤出可视区；`android:description` 用大段「开源播放器免许可费」话术掩盖无障碍能力。真正的恶意载荷另有 FBI 勒索页（`@string/Text`）与 OneVanilla $500 购卡页（`@string/titleWhere`），与本引导链共享同一无障碍自点击能力。

**UTG 采集建议**：以「检测到 `ACCESSIBILITY_SETTINGS` 跳转 Intent」或「ReqPerm 对话框出现」为触发点抓取；关键页为不可取消 `Attention!` 弹窗页、从设置返回后重复弹出的同一弹窗、以及获权瞬间无障碍服务自点 `ALLOW` 时的系统浮窗授权页。无纯图/OCR 盲区，文本全部在 strings 与代码硬编码中。

```json
{
  "static_visibility": "clear",
  "visibility_note": "DEX 未加壳、无加密载荷，引导链（Launcher 自禁用 → JobScheduler 5s → ReqPerm 不可取消弹窗 → ACCESSIBILITY_SETTINGS 跳转 → onActivityResult 回跳循环 → 无障碍服务自点击授权）全部可从 classes.dex 与 res/values/strings.xml 静态还原；未发现远端 HTML 或 AES 二阶段载荷参与无障碍引导。",
  "summary_one_liner": "伪装成开源视频播放器的恶意应用，冷启动即禁用自身启动图标并由 JobScheduler 拉起 ReqPerm 活动，用不可取消的 AlertDialog 以『必须开启 SVO 视频优化才能看视频』为由反复跳转系统无障碍设置，获权后由无障碍服务自动点击 ALLOW/OK/DONE 完成悬浮窗自授权与清空最近任务。",
  "disguise_identity": {
    "app_display_name": "Video Player",
    "claimed_brand_or_persona": "开源视频播放器 / Streaming Video Optimization (SVO) 视频优化服务",
    "a11y_service_label": "Streaming Video Optimization (SVO)",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务标签 @string/fake_label 在名称后塞入约 40 个换行加一个句点，把系统无障碍列表中紧随其后的能力警告/描述挤出可视区；android:description 用『开源播放器免许可费、补丁与漏洞修复更及时』的长篇话术掩盖 canRetrieveWindowContent 等真实能力；启动器组件在首次 onCreate 中用 setComponentEnabledSetting(COMPONENT_ENABLED_STATE_DISABLED) 自我禁用，桌面图标消失；包名/类名全随机化（uuctvbgtlb.nkoqrtdctt.unootbawgh.*）；服务 android:label 与 activity label（Word service / ReqPerm）互不一致。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "uuctvbgtlb.nkoqrtdctt.unootbawgh.lrplugqbfs（LAUNCHER Activity）",
      "trigger_event": "onCreate()：setContentView 后立即调用私有方法 a() 禁用自身组件，并调用 i.a(getApplicationContext()) 注册 5 秒延迟的 JobScheduler 任务",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "该页无可见引导文字，仅作一次性跳板：禁用桌面图标并投递 5 秒后的 Job 任务后 finish",
      "user_action_requested": "无需用户操作（页面随即消失）",
      "code_anchor": "uuctvbgtlb.nkoqrtdctt.unootbawgh.lrplugqbfs.onCreate / .a / uuctvbgtlb.nkoqrtdctt.unootbawgh.i.a"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "uuctvbgtlb.nkoqrtdctt.unootbawgh.nzpdotxvtw（label=ReqPerm）内的 AlertDialog",
      "trigger_event": "nzpdotxvtw.onCreate() → a()；条件 bpnbunmqon.b == false（无障碍服务未连接）",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Attention! / To continue watching the video on your phone, you must enable Streaming Video Optimization (SVO), select line in the menu and turn it on!",
      "shown_text_zh": "注意！/ 要在手机上继续观看视频，您必须启用流媒体视频优化（SVO），在菜单中选择该行并打开它！",
      "user_action_requested": "仅有一个确定按钮（R$string.ok），setCancelable(false) 不可取消、无跳过；SDK<23 时以 WindowManager 类型 2010 悬浮窗形式弹出",
      "code_anchor": "uuctvbgtlb.nkoqrtdctt.unootbawgh.nzpdotxvtw.a(Context,String,Intent)；strings: Attention / Activate_Access"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 Settings.ACTION_ACCESSIBILITY_SETTINGS（无障碍服务列表）",
      "trigger_event": "AlertDialog 确定按钮回调 nzpdotxvtw$1.onClick() → startActivityForResult(intent, 0)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "直接跳转到系统无障碍服务列表，由用户在其中找到并开启「Streaming Video Optimization (SVO)」",
      "user_action_requested": "在系统无障碍列表中点击 SVO 服务开关并确认系统警告对话框",
      "code_anchor": "uuctvbgtlb.nkoqrtdctt.unootbawgh.nzpdotxvtw#a：new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\").addFlags(8388608)"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "nzpdotxvtw.onActivityResult → 再次弹出同一不可取消 AlertDialog",
      "trigger_event": "用户从系统设置返回触发 onActivityResult，无条件调用 a() 重新判断 bpnbunmqon.b",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Attention! / To continue watching the video on your phone, you must enable Streaming Video Optimization (SVO), select line in the menu and turn it on!",
      "shown_text_zh": "未开启则原样重弹同一提示，形成返回即重跳的死循环；只有按 HOME 或最近任务键才会临时关闭",
      "user_action_requested": "无取消按钮；唯一逃逸路径是按 HOME/最近任务（被 CLOSE_SYSTEM_DIALOGS 广播监听后 dismiss 并置 bpnbunmqon.a=false、nzpdotxvtw.a=false）",
      "code_anchor": "uuctvbgtlb.nkoqrtdctt.unootbawgh.nzpdotxvtw.onActivityResult / nzpdotxvtw$a.onReceive"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "uuctvbgtlb.nkoqrtdctt.unootbawgh.bpnbunmqon（AccessibilityService）onServiceConnected / onAccessibilityEvent",
      "trigger_event": "用户开启服务后 onServiceConnected()：置 b=true，startActivity(nzpdotxvtw, exit=true) 收掉残留弹窗，setServiceInfo(flags=19, eventTypes=-1, notificationTimeout=100)；随后每个无障碍事件里 findAccessibilityNodeInfosByText 并用 dispatchGesture 点击",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Allow display over other apps / Permit drawing over other apps / If you don’t want / DONE / CLEAR ALL / ALLOW / OK",
      "shown_text_zh": "由无障碍服务自动点击系统「允许在其他应用上层显示」按钮、确认对话框与「清除全部」最近任务，用户无需再手动操作",
      "user_action_requested": "无（全部由 dispatchGesture 自动点击完成），并伴随 2 秒延迟的 postDelayed 重复点击",
      "code_anchor": "uuctvbgtlb.nkoqrtdctt.unootbawgh.bpnbunmqon#onServiceConnected / #onAccessibilityEvent / #a(AccessibilityEvent,String)"
    }
  ],
  "text_presentation_locations": [
    "nzpdotxvtw（ReqPerm）内不可取消 AlertDialog：标题 @string/Attention（Attention!），正文 @string/Activate_Access（Activate_Access）",
    "系统无障碍列表服务条目：android:label=@string/fake_label（Streaming Video Optimization (SVO) 后接大量换行与句点）",
    "系统无障碍服务详情/描述：android:description=@string/accessibility_service_description（大段开源播放器免许可费话术），由 res/xml/bqpgvctoin.xml 引用",
    "应用列表/桌面名称：@string/app_name = Video Player",
    "manifest 中 service android:label=\"Word service\"（JobService dtpqopbpon）与 activity android:label=@string/title_activity_req_perm（ReqPerm），均不向用户说明真实用途",
    "res/values/strings.xml 中 @string/Text（伪造 FBI 执法勒索 HTML 文案）与 @string/titleWhere / @string/CardHint / @string/textSend（OneVanilla $500 购卡页文案），供后续诈骗流程使用，不属本次无障碍引导页",
    "无本地 HTML/WebView 引导页：本应用 assets 中未使用 HTML 承载无障碍引导文案，全部为原生字符串与代码硬编码"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Attention!",
      "text_zh": "注意！",
      "source_location": "res/values/strings.xml key=Attention（用于 nzpdotxvtw 弹窗标题）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "To continue watching the video on your phone, you must enable Streaming Video Optimization (SVO), select line in the menu and turn it on!",
      "text_zh": "要在手机上继续观看视频，您必须启用流媒体视频优化（SVO），在菜单中选择该行并打开它！",
      "source_location": "res/values/strings.xml key=Activate_Access（nzpdotxvtw.a 弹窗正文，setCancelable(false)）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Android Optimization must be enable, for play video in your phone.",
      "text_zh": "必须开启安卓优化，才能在您的手机上播放视频。",
      "source_location": "res/values/strings.xml key=accessibility_service_description（res/xml/bqpgvctoin.xml android:description）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": " Video player offer some advantages over players developed with proprietary software. Many businesses and individual users prefer to go the open source route as it does away with the procurement barrier. Video players built with proprietary software use private source code and is offered via licensing where users need to pay for and agree to the different terms and conditions before being able to use the player. Given the vastly improved scrutiny around security, the availability of patches and bug fixes, open source video players are free to use without licensing fees and cumbersome, contracts. Some additional benefits include",
      "text_zh": "视频播放器相比专有软件开发的播放器有一些优势。许多企业和个人用户更青睐开源路线，因为它消除了采购门槛。专有软件构建的视频播放器使用私有源码并通过许可方式提供，用户需付费并同意各种条款后才能使用。鉴于安全审查大幅改善、补丁与错误修复可得，开源视频播放器可免费使用，无需许可费与繁琐合同。其他额外好处包括……",
      "source_location": "res/values/strings.xml key=accessibility_service_description（系统无障碍服务描述，正文在句末被截断为 include）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Streaming Video Optimization (SVO)\n\n\n\n\n\n\n\n\n \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n.",
      "text_zh": "流媒体视频优化（SVO）+ 大量空行 + 句点（用于把系统无障碍列表中的警告文字挤出屏幕可视区域）",
      "source_location": "res/values/strings.xml key=fake_label（manifest service android:label）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Allow display over other apps",
      "text_zh": "允许在其他应用上层显示",
      "source_location": "uuctvbgtlb.nkoqrtdctt.unootbawgh.bpnbunmqon.onAccessibilityEvent 中硬编码，用于自动点击系统悬浮窗授权按钮",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Permit drawing over other apps",
      "text_zh": "允许绘制在其他应用之上",
      "source_location": "uuctvbgtlb.nkoqrtdctt.unootbawgh.bpnbunmqon.onAccessibilityEvent 中硬编码，用于自动点击系统悬浮窗授权按钮",
      "rhetorical_frame": "受限设置分步教学"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "用户从系统无障碍设置返回后 onActivityResult 无条件调用 a()，若 bpnbunmqon.b 仍为 false 则原样重弹同一个 setCancelable(false) 的 AlertDialog，形成「返回即重跳」的无限循环；无障碍服务自身在未获权时也会 startActivity(nzpdotxvtw) 反复后台拉起。唯一临时逃逸是按 HOME 或最近任务键（监听 CLOSE_SYSTEM_DIALOGS 的 homekey/recentapps 后 dismiss 并置 bpnbunmqon.a=false、nzpdotxvtw.a=false）。",
    "overlay_or_fake_settings": "弹窗在 SDK<23 时通过 getWindow().setType(2010) 以悬浮窗层级显示；未发现伪造的高仿系统无障碍开关页或覆盖在设置页之上的半透明引导遮罩。",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion 26，未涉及 Android 13+ 受限设置教学或 Session 安装器绕过）",
    "post_grant_anti_removal": "有自授权行为：onServiceConnected 后服务持续在无障碍事件中按文本查找并用 dispatchGesture 自动点击 ALLOW / Permit drawing over other apps（自动授予 SYSTEM_ALERT_WINDOW）、OK、DONE 以及 CLEAR ALL（自动清空最近任务以隐藏自身痕迹）；未发现用 GLOBAL_ACTION_BACK/HOME 阻止用户撤权的逻辑。此外首次启动即以 setComponentEnabledSetting 禁用自身 LAUNCHER 组件，用户失去再次进入/管理入口。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以监测到 Intent 目标为 android.settings.ACCESSIBILITY_SETTINGS（含 FLAG_ACTIVITY_NEW_TASK）的 startActivityForResult 为最佳瞬间拉起 UTG；若设备在冷启动后 5 秒内即出现 ReqPerm（nzpdotxvtw）弹窗，也可直接以该 Activity onCreate 为触发点。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页",
        "page_identifier": "uuctvbgtlb.nkoqrtdctt.unootbawgh.nzpdotxvtw（ReqPerm）上的 AlertDialog，标题 Attention!，正文含 Streaming Video Optimization (SVO)",
        "why_most_useful": "该页是引导链唯一面向用户的说明载体，且明确 setCancelable(false)、无取消/跳过，可直接判定强迫性诱导",
        "observable_utg_signals": ["弹窗无任何取消/跳过控件，仅一个确定按钮", "正文出现『必须启用 SVO 才能看视频』的虚假功能前置要求", "弹窗出现时无障碍服务尚未开启（开关关闭）", "对话框不可通过返回键关闭"]
      },
      {
        "page_role": "设置页后压栈遮罩/重复弹窗页",
        "page_identifier": "从 ACCESSIBILITY_SETTINGS 返回后 0~1 秒内再次出现的同一 ReqPerm 弹窗",
        "why_most_useful": "证明拒权后存在回跳循环（onActivityResult → a() 重弹），是区分恶意强迫与良性一次性引导的决定性证据",
        "observable_utg_signals": ["同一 Activity 在设置返回后再次出现相同文本", "无降级路径、无『稍后再说』入口", "按 HOME 后弹窗消失、再次进入又出现"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统设置无障碍列表中 label 为 Streaming Video Optimization (SVO) 的条目，其后带大段空白",
        "why_most_useful": "可直观验证换行填充挤出警告、标签与包名/应用名（Video Player）身份不一致",
        "observable_utg_signals": ["服务名称后存在异常长空白/换行，警告文字被推离可视区", "服务描述出现『开源播放器免许可费』等与无障碍无关话术", "列表项文本与桌面应用名 Video Player 不一致"]
      },
      {
        "page_role": "获权瞬间的系统悬浮窗授权页",
        "page_identifier": "系统『允许在其他应用上层显示』对话框，按钮文本 Allow display over other apps / Permit drawing over other apps 被自动点击",
        "why_most_useful": "捕捉无障碍服务 dispatchGesture 自动授权 SYSTEM_ALERT_WINDOW 的自点击行为，证明获权后自动化越权",
        "observable_utg_signals": ["无用户触摸事件而授权对话框被点击关闭", "两次同义授权文案（Allow / Permit）先后被点击", "随后出现 CLEAR ALL 使最近任务被清空"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：全部引导文案均为原生字符串与代码硬编码，纯文本可由 UTG 直接提取。需注意两点运行期盲区：一是首次启动即自我禁用 LAUNCHER 组件，之后无法通过桌面图标复现引导，需在首次安装后立即抓取；二是真正的恶意业务（伪造 FBI 勒索页 @string/Text、OneVanilla $500 购卡页）在无障碍获权后才由后台服务触发，纯 UTG 若只观察无障碍引导阶段会漏掉该部分。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "uuctvbgtlb.nkoqrtdctt.unootbawgh.lrplugqbfs#onCreate / #a（自我禁用 LAUNCHER 组件 + 投递 5s JobScheduler）",
    "uuctvbgtlb.nkoqrtdctt.unootbawgh.nzpdotxvtw#a(Context,String,Intent)（setCancelable(false) 的 Attention! 弹窗）",
    "uuctvbgtlb.nkoqrtdctt.unootbawgh.nzpdotxvtw$1#onClick（startActivityForResult 跳 android.settings.ACCESSIBILITY_SETTINGS）",
    "uuctvbgtlb.nkoqrtdctt.unootbawgh.nzpdotxvtw#onActivityResult（拒权回跳循环）",
    "uuctvbgtlb.nkoqrtdctt.unootbawgh.bpnbunmqon#onServiceConnected / #onAccessibilityEvent（dispatchGesture 自动点击 ALLOW/OK/DONE/CLEAR ALL）",
    "res/values/strings.xml（Activate_Access / Attention / fake_label / accessibility_service_description）与 res/xml/bqpgvctoin.xml"
  ]
}
```

</details>
