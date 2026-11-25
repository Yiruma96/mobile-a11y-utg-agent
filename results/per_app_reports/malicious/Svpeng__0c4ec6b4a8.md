# MR_062__0c4ec6b4a8｜Svpeng — Авито

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：157.0s

## 1. 一句话核心结论

- **核心申请方式**：启动后由权限向导 Activity 先判定无障碍未开启，弹出伪装成「Google Play」的俄语安全承诺 Toast 并直接 startActivityForResult 跳转 android.settings.ACCESSIBILITY_SETTINGS，用户返回仍未开启则立刻重弹重跳形成死循环，且无任何取消或跳过入口。
- **静态可见性说明**：全部引导逻辑与文案均在 DEX 内静态可见；文案虽经 AES/CBC/NoPadding 加密，但密钥、IV 以明文常量内联在调用点（如 fp1r4smginu.esdtrci 的参数），已成功解密还原，无远端 HTML、无加壳、无二阶段载荷参与无障碍引导链路。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `0c4ec6b4a8e9674bf7af120b767477fdc460753eda860a73b270d08ff9b0c841` |
| 包名 / 年份 | `com.seoadvice.swentoday` / 2019 |
| 家族 / 品类 | **Svpeng**（同池样本数：20） |
| 原始来源标识 | https://blog.zimperium.com/how-zimperiums-z9-detected-unknown-mobile-malware-overlooked-by-the-av-industry/ |
| 桌面显示名 | Авито |
| 引导页宣称品牌/身份 | Google Play（系统无障碍服务列表中显示为 Google Play，文案宣称其为应用运行所必需组件并已通过安全检查） |
| 系统无障碍列表服务名 | Google Play |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务 label 直接冒用 Google Play（strings.xml 键 yvndrmuf），应用 label 冒用 Авито；服务配置 res/xml/bgjsraok.xml 不写 android:description，系统列表中不出现任何能力说明与警告文字；文案经 AES/CBC 加密以规避静态字符串检测；类名/包名全部随机化（如 com.idoing.linefirefree.cqnj67u8hc1、bubbleshooter.orig.jlncg46bksq）；settingsActivity 指向不存在的 com.example.root.myapplication.MainActivity。 |
| 无障碍服务类名 | `com.idoing.linefirefree.cqnj67u8hc1` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `READ_CONTACTS, READ_SMS, RECEIVE_SMS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | pine.game.skydancer.snsl81auntd（LAUNCHER Activity，excludeFromRecents=true） | onCreate → cvwltsjb → byzcvsif → ngturvfj → bnlgmwjo → hnzscqak → yzfplqne | 原生Activity | 无 | 无（用户只看到桌面图标「Авито」被点击） | `pine.game.skydancer.snsl81auntd.yzfplqne / onCreate` |
| 2 | 引导说明页（无障碍为第一道门） | bubbleshooter.orig.jlncg46bksq（权限向导 Activity） | esanfvgp(Bundle) 中第一项判定 n0m2ouh1fnl.hgyetujraz(context) 为 false | 原生Activity | **原文**：无（该步仅做条件判定，界面在下一步 Toast 中呈现）<br>**译注**：检测到无障碍服务未开启，进入无障碍引导分支并 return，短信/设备管理员/悬浮窗三步被顺延 | 无 | `bubbleshooter.orig.jlncg46bksq.esanfvgp` |
| 3 | 拒权反馈循环（首次诱导文案） | Toast（由 jlncg46bksq$1 CountDownTimer 维持 10 秒） | gizjsbfmvx() 被 esanfvgp 调用 | 原生Dialog | **原文**：Для работы приложения требуется включенный: Google Play найдите его в этом меню и включите!<br>**译注**：应用运行需要开启：Google Play，请在此菜单中找到并开启它！ | 在随后弹出的系统无障碍设置页中找到名为「Google Play」的服务并打开；Toast 无任何按钮，无取消或跳过选项 | `bubbleshooter.orig.jlncg46bksq.gizjsbfmvx（AES 解密 com.fungames.battletanksbeta.fp1r4smginu.esdtrci + getString(R.string.yvndrmuf)）` |
| 4 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | gizjsbfmvx() 内 startActivityForResult(intent, 125) | 系统无障碍页 | **原文**：Google Play<br>**译注**：系统无障碍服务列表中出现一项名为「Google Play」的服务，无任何功能描述与风险提示 | 手动点开「Google Play」开关并确认系统弹窗 | `bubbleshooter.orig.jlncg46bksq.gizjsbfmvx（hfmyxeosur_nuelwsmcoy_yqndveucbh_arjdklonic = 125）` |
| 5 | 拒权反馈循环 | onActivityResult → vkfqelgp → knrjpwqb → oadkzhln | 用户从设置页返回且 requestCode==125 时 hgyetujraz() 仍为 false | 原生Activity | **原文**：Для работы приложения требуется включенный: Google Play найдите его в этом меню и включите!<br>**译注**：再次弹出同一俄语 Toast 并再次跳转无障碍设置页，无限循环，用户无法停留在应用内或退出流程 | 被迫重复开启，或强制结束应用 | `bubbleshooter.orig.jlncg46bksq.oadkzhln` |
| 6 | 获权后动作 | com.idoing.linefirefree.cqnj67u8hc1（AccessibilityService）+ com.kongregate.mobile.fly.google.x4pg21rvqaw（广播接收器） | 无障碍开启后 esanfvgp 继续走到下一项判定；oadkzhln 末尾 sendBroadcast(x4pg21rvqaw, svkandcljr_bernhfmnui_vwmjrsbpti_zpysrbagud) 并 finish() | 不可静态还原 | 无 | 无 | `com.idoing.linefirefree.cqnj67u8hc1.onServiceConnected / pcnwrmzt` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 无障碍引导文案以 Toast 形式呈现（bubbleshooter.orig.jlncg46bksq.gizjsbfmvx，AES 解密后拼接 R.string.yvndrmuf），由 jlncg46bksq$1 CountDownTimer 每 1 秒刷新、总计 10 秒挂住，无按钮、不可取消、不可跳过
- 系统无障碍服务列表中该服务的显示名为 strings.xml 键 yvndrmuf = 「Google Play」；应用在系统设置应用列表中的显示名为键 zscgtqby = 「Авито」
- res/xml/bgjsraok.xml 未配置 android:description，因此系统无障碍列表项下无任何能力说明或风险警示文字
- 设备管理器附加说明文案（非无障碍，同一向导后续步骤）：AES 解密的「Приложение проверено и является полностью безопасным! Выполнить запуск?」以 ADD_EXPLANATION extra 传给系统设备管理员确认页
- 全包未发现本地/远端 HTML 教学页、未发现自定义引导弹窗布局、未发现覆盖在系统设置页之上的半透明遮罩（无 TYPE_SYSTEM_ALERT/TYPE_APPLICATION_OVERLAY 与该流程关联；hbax72vnotp 的 TYPE=2010 悬浮窗属另一 Activity 的远端页面加载器）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| ru | Для работы приложения требуется включенный: | 应用运行需要开启： | `bubbleshooter.orig.jlncg46bksq.gizjsbfmvx 内 AES 密文（Hex + AES/CBC/NoPadding，key=262b7c89081a7a4d5d3f43ee9561bf0c，iv=54c7890fd32ea16b）` | 假更新 |
| ru | найдите его в этом меню и включите! | 请在此菜单中找到它并开启！ | `bubbleshooter.orig.jlncg46bksq.gizjsbfmvx 内 AES 密文（key=f427af129de0bb6578c6a19d05383ec4，iv=e473fa86c902b15d）` | 受限设置分步教学 |
| en | Google Play | Google Play（系统无障碍服务列表中的服务名，被拼接进上述俄语句子作为「必须开启的组件」） | `res/values/strings.xml key yvndrmuf（同时用作 android:label）` | 假反诈安全 |
| ru | Приложение проверено и является полностью безопасным! Выполнить запуск? | 应用已通过检查，完全安全！是否执行启动？ | `bubbleshooter.orig.jlncg46bksq.zhemraysg 中 AES 密文，作为 ADD_DEVICE_ADMIN 的 ADD_EXPLANATION（key=75640f7d22bae3318c09c1de859bf4a6，iv=6804315f7d29caeb）` | 隐私承诺 |
| ru | Авито | Авито（俄罗斯二手交易平台品牌名，用作桌面应用显示名） | `res/values/strings.xml key zscgtqby` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：onActivityResult(requestCode=125) 经 vkfqelgp→knrjpwqb→oadkzhln 判定无障碍仍未开启时，立即再次调用 gizjsbfmvx() 重弹 10 秒 Toast 并再次 startActivityForResult 跳转 ACCESSIBILITY_SETTINGS，无任何计数上限或退出条件，用户只能强制结束应用
- **遮罩叠层 / 高仿系统设置页**：无。未发现悬浮窗遮罩、全屏引导层或高仿系统无障碍开关页；诱导完全依赖系统原生 Toast + 直接跳转系统真实设置页
- **Android 13+ 受限设置（Restricted Settings）应对**：无。全包未出现 ACTION_APPLICATION_DETAILS_SETTINGS 或「允许受限设置」分步教学，也无 Session 安装器绕过路径（targetSdkVersion=19，本身不涉及 Android 13 受限设置机制）
- **获权后即时行为与防撤权机制**：无。未发现 GLOBAL_ACTION_BACK / GLOBAL_ACTION_HOME 调用，也未发现监听设置页阻止撤权的代码
- **良性降级 / 替代方案**：无。向导在无障碍未开启时不提供任何替代模式或降级路径，且不 finish，形成闭环强制

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在应用进程内 Hook AccessibilityManager/AccessibilityService 状态查询（n0m2ouh1fnl.hgyetujraz → lmtsdozn → mandybxz 链）或直接监测 startActivityForResult 携带 action=android.settings.ACCESSIBILITY_SETTINGS、requestCode=125 的瞬间，以及紧邻其前的 Toast.show() 调用；亦可由冷启动后 3 秒内出现 ACCESSIBILITY_SETTINGS 跳转作为触发点
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：引导载体是系统 Toast，部分 UTG 抓取框架默认不采集 Toast 窗口节点（WindowManager.LayoutParams.type=TOAST），需显式开启 Toast/系统窗口采集，否则会误判为「无任何说明文字」；此外无障碍服务自身的读屏与注入逻辑位于 cqnj67u8hc1.pcnwrmzt（1724 条指令）与启动插件 snsl81auntd.yzfplqne（900 条指令）中，本轮未逐行还原，若需刻画获权后的实际危害需另行深挖。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转前诱导 Toast 页** | 系统 Toast 文本「Для работы приложения требуется включенный: Google Play найдите его в этом меню и включите!」，与权限向导 Activity 同屏 | 该文案同时给出「必须开启」的强制理由与冒用品牌名，是判定诱导与身份冒用的决定性证据 | Toast 文本节点中的「Google Play」与俄语强制措辞；Toast 无任何按钮/取消控件，且持续约 10 秒不消失；同屏 Activity 类名与桌面图标名「Авито」不一致 |
| **系统无障碍服务列表项** | android.settings.ACCESSIBILITY_SETTINGS 页面中名为「Google Play」的服务条目 | 验证服务名冒用且无功能描述，直接暴露系统层面的身份欺骗 | 服务条目文本恰为「Google Play」；条目下无 summary/description 文案（对应 bgjsraok.xml 缺 android:description）；条目数量与已安装应用列表不匹配（不存在真正的 Google Play 无障碍服务） |
| **拒权返回后重跳页** | 从设置页返回后 1 秒内再次出现 ACCESSIBILITY_SETTINGS 页面 | 证明 onActivityResult 死循环重跳，是判定非自愿/剥夺拒绝权的关键运行证据 | 同一 Activity 反复回到栈顶且 finish 未被调用；两次 ACCESSIBILITY_SETTINGS 页面出现间隔恒定（受 Toast 时长约束）；用户按返回键无法离开应用主流程 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `bubbleshooter.orig.jlncg46bksq.gizjsbfmvx`
- `bubbleshooter.orig.jlncg46bksq.esanfvgp`
- `bubbleshooter.orig.jlncg46bksq.oadkzhln`
- `com.seoadvice.swentoday.n0m2ouh1fnl.hgyetujraz`
- `res/values/strings.xml（yvndrmuf=Google Play、zscgtqby=Авито）`
- `res/xml/bgjsraok.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验）

**静态可见性：清晰可还原**。虽然字符串用 AES/CBC 加密，但密钥与 IV 均以明文常量内联，已成功解密；无障碍引导流程完整可见。

**核心链路（纯运行期 UTG 视角）**

1. **冷启动入口**：Launcher 是 `pine.game.skydancer.snsl81auntd`，其 `onCreate` 会转入 `yzfplqne`，完成插件初始化与后台服务拉起后 `finish()`，不在前台停留。
2. **权限向导（无障碍为第一道门）**：[esanfvgp()](<resource-unit:#1.dex1 code:bubbleshooter.orig.jlncg46bksq#esanfvgp>) 依次校验四类条件，第一项 `hgyetujraz()` 判定无障碍服务是否已开启，未开启即调用 `gizjsbfmvx()` 并 `return`（后续短信默认应用、设备管理器、悬浮窗三步被顺延）。
3. **诱导载体是 Toast，不是弹窗**：[gizjsbfmvx()](<resource-unit:#1.dex1 code:bubbleshooter.orig.jlncg46bksq#gizjsbfmvx>) 用 AES 解密俄语前缀/后缀，中间拼接 `R.string.yvndrmuf`（=`Google Play`），组成“应用运行需要开启：Google Play，请在此菜单中找到并开启它！”，并以 10 秒 CountDownTimer 挂住 Toast。
4. **直接跳系统无障碍页**：同方法 `new Intent("android.settings.ACCESSIBILITY_SETTINGS")` + `startActivityForResult(..., 125)`。全包无 `APPLICATION_DETAILS_SETTINGS`、无 `ACTION_SETTINGS`、无 `GLOBAL_ACTION_BACK`，**不含 Android 13 受限设置分步教学，也没有获权后阻止撤权**。
5. **拒权循环**：[oadkzhln()](<resource-unit:#1.dex1 code:bubbleshooter.orig.jlncg46bksq#oadkzhln>)（由 `onActivityResult` → `vkfqelgp` → `knrjpwqb` 链到达）在 `requestCode==125 && !hgyetujraz()` 时再次 `gizjsbfmvx()`，即返回后无条件重弹并重跳，无取消/跳过。

**身份冒用**：应用名 `Авито`（俄语二手交易平台），无障碍服务 label `Google Play`；服务配置 [res/xml/bgjsraok.xml](<resource-unit:#1 file:res/xml/bgjsraok.xml>) 无 `android:description`、无 `isAccessibilityTool`，系统列表中就是一个名为 “Google Play” 的服务；该服务 `typeAllMask` + `canRetrieveWindowContent` + `flagIncludeNotImportantViews`，全量读屏。

**未覆盖边界**：`cqnj67u8hc1.pcnwrmzt`（1724 条指令）与 `snsl81auntd.yzfplqne`（900 条指令）的具体读屏/注入逻辑未逐行展开；`hbax72vnotp` 存在 `TYPE=2010`（`TYPE_SYSTEM_ALERT`）悬浮窗 `addView` 与 WebView，属远端页面加载器，本轮未深入。已登记风险 R-001（high，deceptive_behavior）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部引导逻辑与文案均在 DEX 内静态可见；文案虽经 AES/CBC/NoPadding 加密，但密钥、IV 以明文常量内联在调用点（如 fp1r4smginu.esdtrci 的参数），已成功解密还原，无远端 HTML、无加壳、无二阶段载荷参与无障碍引导链路。",
  "summary_one_liner": "启动后由权限向导 Activity 先判定无障碍未开启，弹出伪装成「Google Play」的俄语安全承诺 Toast 并直接 startActivityForResult 跳转 android.settings.ACCESSIBILITY_SETTINGS，用户返回仍未开启则立刻重弹重跳形成死循环，且无任何取消或跳过入口。",
  "disguise_identity": {
    "app_display_name": "Авито",
    "claimed_brand_or_persona": "Google Play（系统无障碍服务列表中显示为 Google Play，文案宣称其为应用运行所必需组件并已通过安全检查）",
    "a11y_service_label": "Google Play",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务 label 直接冒用 Google Play（strings.xml 键 yvndrmuf），应用 label 冒用 Авито；服务配置 res/xml/bgjsraok.xml 不写 android:description，系统列表中不出现任何能力说明与警告文字；文案经 AES/CBC 加密以规避静态字符串检测；类名/包名全部随机化（如 com.idoing.linefirefree.cqnj67u8hc1、bubbleshooter.orig.jlncg46bksq）；settingsActivity 指向不存在的 com.example.root.myapplication.MainActivity。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "pine.game.skydancer.snsl81auntd（LAUNCHER Activity，excludeFromRecents=true）",
      "trigger_event": "onCreate → cvwltsjb → byzcvsif → ngturvfj → bnlgmwjo → hnzscqak → yzfplqne",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无可见界面，仅初始化插件（qiy26987c3n）并拉起服务 acl3yjngf9o，随后 finish()",
      "user_action_requested": "无（用户只看到桌面图标「Авито」被点击）",
      "code_anchor": "pine.game.skydancer.snsl81auntd.yzfplqne / onCreate"
    },
    {
      "step": 2,
      "stage": "引导说明页（无障碍为第一道门）",
      "screen_or_component": "bubbleshooter.orig.jlncg46bksq（权限向导 Activity）",
      "trigger_event": "esanfvgp(Bundle) 中第一项判定 n0m2ouh1fnl.hgyetujraz(context) 为 false",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（该步仅做条件判定，界面在下一步 Toast 中呈现）",
      "shown_text_zh": "检测到无障碍服务未开启，进入无障碍引导分支并 return，短信/设备管理员/悬浮窗三步被顺延",
      "user_action_requested": "无",
      "code_anchor": "bubbleshooter.orig.jlncg46bksq.esanfvgp"
    },
    {
      "step": 3,
      "stage": "拒权反馈循环（首次诱导文案）",
      "screen_or_component": "Toast（由 jlncg46bksq$1 CountDownTimer 维持 10 秒）",
      "trigger_event": "gizjsbfmvx() 被 esanfvgp 调用",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Для работы приложения требуется включенный: Google Play найдите его в этом меню и включите!",
      "shown_text_zh": "应用运行需要开启：Google Play，请在此菜单中找到并开启它！",
      "user_action_requested": "在随后弹出的系统无障碍设置页中找到名为「Google Play」的服务并打开；Toast 无任何按钮，无取消或跳过选项",
      "code_anchor": "bubbleshooter.orig.jlncg46bksq.gizjsbfmvx（AES 解密 com.fungames.battletanksbeta.fp1r4smginu.esdtrci + getString(R.string.yvndrmuf)）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "gizjsbfmvx() 内 startActivityForResult(intent, 125)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Google Play",
      "shown_text_zh": "系统无障碍服务列表中出现一项名为「Google Play」的服务，无任何功能描述与风险提示",
      "user_action_requested": "手动点开「Google Play」开关并确认系统弹窗",
      "code_anchor": "bubbleshooter.orig.jlncg46bksq.gizjsbfmvx（hfmyxeosur_nuelwsmcoy_yqndveucbh_arjdklonic = 125）"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "onActivityResult → vkfqelgp → knrjpwqb → oadkzhln",
      "trigger_event": "用户从设置页返回且 requestCode==125 时 hgyetujraz() 仍为 false",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Для работы приложения требуется включенный: Google Play найдите его в этом меню и включите!",
      "shown_text_zh": "再次弹出同一俄语 Toast 并再次跳转无障碍设置页，无限循环，用户无法停留在应用内或退出流程",
      "user_action_requested": "被迫重复开启，或强制结束应用",
      "code_anchor": "bubbleshooter.orig.jlncg46bksq.oadkzhln"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.idoing.linefirefree.cqnj67u8hc1（AccessibilityService）+ com.kongregate.mobile.fly.google.x4pg21rvqaw（广播接收器）",
      "trigger_event": "无障碍开启后 esanfvgp 继续走到下一项判定；oadkzhln 末尾 sendBroadcast(x4pg21rvqaw, svkandcljr_bernhfmnui_vwmjrsbpti_zpysrbagud) 并 finish()",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "向导结束，读屏服务开始工作（typeAllMask、canRetrieveWindowContent=true、flagIncludeNotImportantViews）",
      "user_action_requested": "无",
      "code_anchor": "com.idoing.linefirefree.cqnj67u8hc1.onServiceConnected / pcnwrmzt"
    }
  ],
  "text_presentation_locations": [
    "无障碍引导文案以 Toast 形式呈现（bubbleshooter.orig.jlncg46bksq.gizjsbfmvx，AES 解密后拼接 R.string.yvndrmuf），由 jlncg46bksq$1 CountDownTimer 每 1 秒刷新、总计 10 秒挂住，无按钮、不可取消、不可跳过",
    "系统无障碍服务列表中该服务的显示名为 strings.xml 键 yvndrmuf = 「Google Play」；应用在系统设置应用列表中的显示名为键 zscgtqby = 「Авито」",
    "res/xml/bgjsraok.xml 未配置 android:description，因此系统无障碍列表项下无任何能力说明或风险警示文字",
    "设备管理器附加说明文案（非无障碍，同一向导后续步骤）：AES 解密的「Приложение проверено и является полностью безопасным! Выполнить запуск?」以 ADD_EXPLANATION extra 传给系统设备管理员确认页",
    "全包未发现本地/远端 HTML 教学页、未发现自定义引导弹窗布局、未发现覆盖在系统设置页之上的半透明遮罩（无 TYPE_SYSTEM_ALERT/TYPE_APPLICATION_OVERLAY 与该流程关联；hbax72vnotp 的 TYPE=2010 悬浮窗属另一 Activity 的远端页面加载器）"
  ],
  "verbatim_texts": [
    {
      "lang": "ru",
      "text_verbatim": "Для работы приложения требуется включенный: ",
      "text_zh": "应用运行需要开启：",
      "source_location": "bubbleshooter.orig.jlncg46bksq.gizjsbfmvx 内 AES 密文（Hex + AES/CBC/NoPadding，key=262b7c89081a7a4d5d3f43ee9561bf0c，iv=54c7890fd32ea16b）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "ru",
      "text_verbatim": " найдите его в этом меню и включите!",
      "text_zh": "请在此菜单中找到它并开启！",
      "source_location": "bubbleshooter.orig.jlncg46bksq.gizjsbfmvx 内 AES 密文（key=f427af129de0bb6578c6a19d05383ec4，iv=e473fa86c902b15d）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Google Play",
      "text_zh": "Google Play（系统无障碍服务列表中的服务名，被拼接进上述俄语句子作为「必须开启的组件」）",
      "source_location": "res/values/strings.xml key yvndrmuf（同时用作 android:label）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "ru",
      "text_verbatim": "Приложение проверено и является полностью безопасным! Выполнить запуск?",
      "text_zh": "应用已通过检查，完全安全！是否执行启动？",
      "source_location": "bubbleshooter.orig.jlncg46bksq.zhemraysg 中 AES 密文，作为 ADD_DEVICE_ADMIN 的 ADD_EXPLANATION（key=75640f7d22bae3318c09c1de859bf4a6，iv=6804315f7d29caeb）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "ru",
      "text_verbatim": "Авито",
      "text_zh": "Авито（俄罗斯二手交易平台品牌名，用作桌面应用显示名）",
      "source_location": "res/values/strings.xml key zscgtqby",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "onActivityResult(requestCode=125) 经 vkfqelgp→knrjpwqb→oadkzhln 判定无障碍仍未开启时，立即再次调用 gizjsbfmvx() 重弹 10 秒 Toast 并再次 startActivityForResult 跳转 ACCESSIBILITY_SETTINGS，无任何计数上限或退出条件，用户只能强制结束应用",
    "overlay_or_fake_settings": "无。未发现悬浮窗遮罩、全屏引导层或高仿系统无障碍开关页；诱导完全依赖系统原生 Toast + 直接跳转系统真实设置页",
    "restricted_settings_13plus_coaching": "无。全包未出现 ACTION_APPLICATION_DETAILS_SETTINGS 或「允许受限设置」分步教学，也无 Session 安装器绕过路径（targetSdkVersion=19，本身不涉及 Android 13 受限设置机制）",
    "post_grant_anti_removal": "无。未发现 GLOBAL_ACTION_BACK / GLOBAL_ACTION_HOME 调用，也未发现监听设置页阻止撤权的代码",
    "benign_graceful_degradation": "无。向导在无障碍未开启时不提供任何替代模式或降级路径，且不 finish，形成闭环强制"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在应用进程内 Hook AccessibilityManager/AccessibilityService 状态查询（n0m2ouh1fnl.hgyetujraz → lmtsdozn → mandybxz 链）或直接监测 startActivityForResult 携带 action=android.settings.ACCESSIBILITY_SETTINGS、requestCode=125 的瞬间，以及紧邻其前的 Toast.show() 调用；亦可由冷启动后 3 秒内出现 ACCESSIBILITY_SETTINGS 跳转作为触发点",
    "key_pages_to_capture": [
      {
        "page_role": "跳转前诱导 Toast 页",
        "page_identifier": "系统 Toast 文本「Для работы приложения требуется включенный: Google Play найдите его в этом меню и включите!」，与权限向导 Activity 同屏",
        "why_most_useful": "该文案同时给出「必须开启」的强制理由与冒用品牌名，是判定诱导与身份冒用的决定性证据",
        "observable_utg_signals": [
          "Toast 文本节点中的「Google Play」与俄语强制措辞",
          "Toast 无任何按钮/取消控件，且持续约 10 秒不消失",
          "同屏 Activity 类名与桌面图标名「Авито」不一致"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "android.settings.ACCESSIBILITY_SETTINGS 页面中名为「Google Play」的服务条目",
        "why_most_useful": "验证服务名冒用且无功能描述，直接暴露系统层面的身份欺骗",
        "observable_utg_signals": [
          "服务条目文本恰为「Google Play」",
          "条目下无 summary/description 文案（对应 bgjsraok.xml 缺 android:description）",
          "条目数量与已安装应用列表不匹配（不存在真正的 Google Play 无障碍服务）"
        ]
      },
      {
        "page_role": "拒权返回后重跳页",
        "page_identifier": "从设置页返回后 1 秒内再次出现 ACCESSIBILITY_SETTINGS 页面",
        "why_most_useful": "证明 onActivityResult 死循环重跳，是判定非自愿/剥夺拒绝权的关键运行证据",
        "observable_utg_signals": [
          "同一 Activity 反复回到栈顶且 finish 未被调用",
          "两次 ACCESSIBILITY_SETTINGS 页面出现间隔恒定（受 Toast 时长约束）",
          "用户按返回键无法离开应用主流程"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "引导载体是系统 Toast，部分 UTG 抓取框架默认不采集 Toast 窗口节点（WindowManager.LayoutParams.type=TOAST），需显式开启 Toast/系统窗口采集，否则会误判为「无任何说明文字」；此外无障碍服务自身的读屏与注入逻辑位于 cqnj67u8hc1.pcnwrmzt（1724 条指令）与启动插件 snsl81auntd.yzfplqne（900 条指令）中，本轮未逐行还原，若需刻画获权后的实际危害需另行深挖。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "bubbleshooter.orig.jlncg46bksq.gizjsbfmvx",
    "bubbleshooter.orig.jlncg46bksq.esanfvgp",
    "bubbleshooter.orig.jlncg46bksq.oadkzhln",
    "com.seoadvice.swentoday.n0m2ouh1fnl.hgyetujraz",
    "res/values/strings.xml（yvndrmuf=Google Play、zscgtqby=Авито）",
    "res/xml/bgjsraok.xml"
  ]
}
```

</details>
