# MB_149__c585e17bdd｜SpyMax — Void PubgHack

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：210.5s

## 1. 一句话核心结论

- **核心申请方式**：伪装为 PUBG 外挂 Void PubgHack，无任何无障碍引导页与用途说明，靠用户自行在系统设置开启唯一无描述的无障碍服务，获权后由 C2 sabanjm2.ddns.net:7771 下发指令开启全量界面文本读屏外发并可远程启动摄像头。
- **静态可见性说明**：DEX 无加壳、无二次加密载荷，无障碍服务声明、C2 地址、指令分发与读屏回传逻辑全部静态可见；唯一不可静态还原的是远端下发的指令文本（cmn[] 指令表由服务器回传的制表符分隔串填充），但指令分支与本地执行行为均已在代码中确认。
- **命中的行为模式标签**：`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `c585e17bddd707a7fbc777cf539b6fa748f3c0eaf6a765879a22744d876b9fc4` |
| 包名 / 年份 | `package.name.suffix` / 2022 |
| 家族 / 品类 | **SpyMax**（同池样本数：4） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Void PubgHack |
| 引导页宣称品牌/身份 | PUBG（com.tencent.ig）作弊/外挂工具 |
| 系统无障碍列表服务名 | Void PubgHack |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务未配置 android:description，系统列表无任何用途说明；服务类名/包名全为随机小写串（package.name.xfcsmhyqynpchfebulknuveqofbxhosbp10872）；字符串资源名亦随机化；冷启动后用 setComponentEnabledSetting(...,2) 禁用自身 Launcher 组件隐藏图标；WebView 加载非 URL 字符串 com.tencent.ig 必然出错，再以黑底白字错误页顶替真实界面 |
| 无障碍服务类名 | `package.name.xfcsmhyqynpchfebulknuveqofbxhosbp10872` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, READ_CONTACTS, READ_SMS, RECORD_AUDIO, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | package.name.oxkoxccxyloozajerukgvqgjumuxqfhwnjiiuxghguaupxvjsfzrikdyqaukhfhsesapsbjtnczbqmtwqlelgpndgkstcwza1094（唯一 LAUNCHER Activity，Theme.Translucent.NoTitleBar） | onCreate：requestWindowFeature + 按字符串第 0/2/3 位字符与常量 c1 比较的静态开关决定分支 | 本地HTML WebView | **原文**：b<html><head><style type="text/css">body{color: #fff; background-color: #000;}</style></head><body>  …  </body></html><br>**译注**：黑底白字的空白/错误页模板，页面内容仅填充 WebView 的 onReceivedError 错误描述字符串 | 无任何提示或按钮；页面无引导文案，用户唯一可做的是自行退出应用 | `oxkoxccxyloozajerukgvqgjumuxqfhwnjiiuxghguaupxvjsfzrikdyqaukhfhsesapsbjtnczbqmtwqlelgpndgkstcwza1094.onCreate / res/layout/webllpyzpuepg1117.xml / tzscqcwccfxkseexigrkkibpevvhjedrcasfodkgotlhzjsffimzcoolycyvgosxbgislziewlwrxupvcqbbseonmhhmfoazb1089.gh` |
| 2 | 获权后动作 | 系统设置 → 无障碍 → 服务项 "Void PubgHack"（用户自行进入，应用不跳转） | 用户在系统无障碍列表中手动开启该服务（应用内无 startActivity 跳转，静态未找到 ACTION_ACCESSIBILITY_SETTINGS） | 系统无障碍页 | **原文**：Void PubgHack<br>**译注**：系统无障碍列表仅显示服务名 Void PubgHack，无 android:description 说明文字 | 用户需自行开关该服务；应用未提供取消/跳过逻辑，因为根本没有前置提示 | `#1 manifest:components / res/values/strings.xml czdxykqsnnousufr1104` |
| 3 | 获权后动作 | package.name.xfcsmhyqynpchfebulknuveqofbxhosbp10872（AccessibilityService） | onServiceConnected → setServiceInfo(eventTypes=-1, flags=89, feedbackType=16) | 不可静态还原 | 无 | 无 | `xfcsmhyqynpchfebulknuveqofbxhosbp10872.onServiceConnected` |
| 4 | 获权后动作 | xfcsmhyqynpchfebulknuveqofbxhosbp10871$ta（后台指令循环）+ mtrjephavfwonygfsqzjlbamehgbikvnnxtlkkguguz1088（Socket 通道） | 常驻服务 onCreate 启动 AsyncTask 循环，从 sabanjm2.ddns.net:7771 接收制表符分隔指令；命中 cmn[11] 分支时调用 acc() 读取 enabled_accessibility_services 判定是否已获权并置 k=true | 不可静态还原 | **原文**：sabanjm2.ddns.net<br>**译注**：远端 C2 域名；指令内容为服务器下发的分隔字符串，本地仅见分支索引 | 无 | `xfcsmhyqynpchfebulknuveqofbxhosbp10871$ta.doInBackground / tzscqcwccfxkseexigrkkibpevvhjedrcasfodkgotlhzjsffimzcoolycyvgosxbgislziewlwrxupvcqbbseonmhhmfoazb1089.acc` |
| 5 | 获权后动作 | xfcsmhyqynpchfebulknuveqofbxhosbp10872.onAccessibilityEvent → s() → Socket 外发 | k 为真时，对 TYPE_VIEW_CLICKED/TEXT_CHANGED/WINDOW_STATE_CHANGED 等事件逐条采集 | 不可静态还原 | **原文**：无（界面侧无提示）<br>**译注**：无提示；后台将「应用名 + 界面文本 + 事件类型」写入 C2 连接 | 无 | `xfcsmhyqynpchfebulknuveqofbxhosbp10872.onAccessibilityEvent / xfcsmhyqynpchfebulknuveqofbxhosbp10872.s` |
| 6 | 获权后动作 | package.name.wtarloxwlakgbgtnhhgxdfqyhpnhtertunmifdezflkglbcjxvjlmrrrdckvbpcgjrlotkhedhsrujnf1092（摄像头远控服务）+ 1x1 透明 SurfaceView（type 2006） | C2 下发启动摄像头指令 → onStartCommand 以 WindowManager.addView 挂 1×1 透明窗口并 Camera.open() | 悬浮窗Overlay | 无 | 无 | `wtarloxwlakgbgtnhhgxdfqyhpnhtertunmifdezflkglbcjxvjlmrrrdckvbpcgjrlotkhedhsrujnf1092.onStartCommand / ck()` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 无障碍服务标签：res/values/strings.xml 的 czdxykqsnnousufr1104 = "Void PubgHack"，经 Manifest 中 android:label 显示于系统「设置 → 无障碍」列表项
- 无障碍服务说明：完全缺失（Manifest 未设置 android:description，系统设置页该服务无用途描述）
- 主界面：res/layout/webllpyzpuepg1117.xml 的全屏 WebView，加载非 URL 字符串 com.tencent.ig，出错后由 tzscqcwccfxkseexigrkkibpevvhjedrcasfodkgotlhzjsffimzcoolycyvgosxbgislziewlwrxupvcqbbseonmhhmfoazb1089.gh() 拼成黑底白字 HTML 显示错误串（无引导文案）
- 前台通知：res/layout/gnvidyyaqckkc1118.xml 为 0×0、背景 #01ffffff 的透明 LinearLayout，作为 RemoteViews 承载通知，通知标题与正文均被 setContentTitle(null)/setContentText(null) 置空，视觉上无任何提示
- 不存在任何引导弹窗、悬浮遮罩、GIF/图片教学、本地或远端 HTML 教学页（assets 目录为空，res/raw/gmplhmgdibkialoaglp1114 为 0 字节占位）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Void PubgHack | Void 版 PUBG 外挂 | `res/values/strings.xml key czdxykqsnnousufr1104（同时为 android:label 与无障碍服务 label）` | 清理工具伪装 |
| en | <html><head><style type="text/css">body{color: #fff; background-color: #000;}</style></head><body> | 黑底白字的空白页模板（正文仅填 WebView 错误描述） | `tzscqcwccfxkseexigrkkibpevvhjedrcasfodkgotlhzjsffimzcoolycyvgosxbgislziewlwrxupvcqbbseonmhhmfoazb1089.gh() 硬编码` | 未知 |
| en | sabanjm2.ddns.net | （C2 服务器域名，非面向用户文本） | `res/values/strings.xml key dutqenukqobvkpzbyde1101` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：无拒绝循环：应用不做任何跳转，因此不存在 onResume 重跳或定时器拉起；也完全没有降级路径。仅在用户自行开启后，C2 指令分支通过 acc() 读取 enabled_accessibility_services 确认状态并回传 1/0
- **遮罩叠层 / 高仿系统设置页**：无引导遮罩、无高仿系统无障碍页；唯一悬浮窗是摄像头服务使用的 1×1 全透明 SurfaceView（type 2006），属隐蔽取帧而非引导
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无 GLOBAL_ACTION_BACK/HOME 阻止撤权逻辑；但具备反卸载辅助能力：Boot 广播接收器（priority 999）自启、前台透明通知保活、exi() 中以 Process.killProcess 重启，且 onCreate 会禁用自身 Launcher 组件隐藏图标
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：本样本没有跳转设置页的瞬间，UTG 应在冷启动时立即拉起（Activity onCreate 后约 500ms 内截取首屏），并在用户手动开启无障碍服务后（服务 onServiceConnected 触发时刻）再次拉起，观察后台 Socket 外连与 1×1 透明窗口
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在两点盲区：一是全程无引导文本，纯靠用户自发动机（想开挂）去系统设置开启，UTG 若只按「弹窗/教学页」特征匹配会漏判，需改为「无障碍服务存在但无 description + 冷启动无真实功能界面」组合判定；二是 C2 指令表（cmn[]）为远端下发的分隔字符串，静态不可还原，读屏开关与摄像头指令的真实下发时机需动态抓包确认。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动外壳页（WebView 错误页）** | Activity 为 package.name.oxkoxccxyloozajerukgvqgjumuxqfhwnjiiuxghguaupxvjsfzrikdyqaukhfhsesapsbjtnczbqmtwqlelgpndgkstcwza1094，全屏单 WebView（id=web），内容为黑底白字、仅一行错误描述 | 确认应用没有任何真实功能与引导文案，宣称的「PUBG 外挂」实际为空壳，是判定伪装身份与 static_hidden 获权方式的关键 | 页面文本极短且为 WebView 错误串（ERR_UNKNOWN_URL_SCHEME 等）；无按钮、无输入框、无任何「开启/授权/允许」节点；状态栏/标题为空（Theme.Translucent.NoTitleBar + requestWindowFeature） |
| **系统无障碍服务列表项** | Settings 无障碍列表中出现 label 为 Void PubgHack、副标题为空的条目 | 证明该服务无 android:description、以外部挂名示人，用户无法得知真实读屏用途 | 列表项文本仅 "Void PubgHack"，无描述行；开关状态变化即为获权时刻（可对齐后续流量爆发） |
| **获权后后台行为观测点（无界面）** | 无障碍服务启用后 30s 内：外连 sabanjm2.ddns.net:7771 的 TCP 会话 + 1×1 全透明 WindowManager 窗口（type 2006） | 把「系统设置开关」与「读屏数据外发/摄像头取帧」绑定，是恶意性质的直接证据 | DNS 解析/连接到 sabanjm2.ddns.net 的流量；窗口层级中出现 1×1 透明 overlay；前台通知标题与正文为空（RemoteViews 0×0） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `package.name.xfcsmhyqynpchfebulknuveqofbxhosbp10872.onServiceConnected`
- `package.name.xfcsmhyqynpchfebulknuveqofbxhosbp10872.onAccessibilityEvent`
- `package.name.xfcsmhyqynpchfebulknuveqofbxhosbp10871$ta.doInBackground`
- `package.name.tzscqcwccfxkseexigrkkibpevvhjedrcasfodkgotlhzjsffimzcoolycyvgosxbgislziewlwrxupvcqbbseonmhhmfoazb1089.acc`
- `package.name.oxkoxccxyloozajerukgvqgjumuxqfhwnjiiuxghguaupxvjsfzrikdyqaukhfhsesapsbjtnczbqmtwqlelgpndgkstcwza1094.onCreate`
- `res/values/strings.xml (czdxykqsnnousufr1104 / dutqenukqobvkpzbyde1101) / res/layout/webllpyzpuepg1117.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（无障碍引导视角）

**核心结论：该样本没有“引导链”，属 `static_hidden`（静态隐藏式）获权。**

- **无任何引导 UI**：全 DEX 中不存在 `ACTION_ACCESSIBILITY_SETTINGS`、`ACTION_APPLICATION_DETAILS_SETTINGS` 跳转，没有 Dialog、Overlay、GIF 或教学 WebView，也没有任何“开启辅助功能”的文案或字符串资源（`strings.xml` 仅 13 条，全是配置项：域名 `sabanjm2.ddns.net`、端口 `7771`、版本、目标包名 `com.tencent.ig` 等）。
- **伪装外壳仅一屏**：唯一 Launcher Activity 只是把布局 `webllpyzpuepg1117` 的 WebView 加载为 `com.tencent.ig`（非 URL），必然触发 `onReceivedError`，再用 `gh()` 拼出黑底白字的错误页 —— 用户看到的是“加载失败/空白”的外壳，随后被 finish 或留在错误页；同时 `onCreate` 里通过 `setComponentEnabledSetting(..., 2)` 把自身图标禁用隐藏。
- **无障碍项无说明**：Manifest 中无障碍服务 `package.name.xfcsmhyqynpchfebulknuveqofbxhosbp10872` 只设 `android:label=@string/czdxykqsnnousufr1104`（`Void PubgHack`），**没有 `android:description`**，系统列表里用户只看到一个与 PUBG 外挂同名的服务名，无用途说明、无隐私承诺，靠“想开挂就得给权限”这一用户自发动机完成获权。
- **获权后才激活**：`onServiceConnected` 直接设 `eventTypes = -1`（全事件）、`flags = 89`、`feedbackType = 16`；但 `onAccessibilityEvent` 受静态开关 `k` 控制，`k` 只由 C2 指令分支（`cmn[11]`）调用 `acc()` 读 `enabled_accessibility_services` 确认“已开启”后置真 —— 即**服务是否真正开始读屏由远端指令决定**。
- **读屏内容外发**：`s()` 把「应用名 + 界面文本 + 事件类型」经 `se()` 用 Socket 发往硬编码 C2 `sabanjm2.ddns.net:7771`，覆盖短信、聊天、输入框等全部界面文本。
- **同通道联动远控**：指令循环还可下发启动摄像头服务，以 1×1 透明 `SurfaceView`（type 2006）挂窗并 `Camera.open()`，实现后台拍照/取帧。

即：**没有“一步步引导”，只有“伪装外挂 → 用户自行去系统设置开启唯一无说明的无障碍项 → 远端按需开启全屏读屏与摄像头远控”**。UTG 检测应重点抓“冷启动即空白/错误页外壳 + 系统无障碍列表项文本 + 获权瞬间后台 Socket 外连”，而非弹窗教学页。

**已登记风险**：R-001（privacy_spyware / high）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "DEX 无加壳、无二次加密载荷，无障碍服务声明、C2 地址、指令分发与读屏回传逻辑全部静态可见；唯一不可静态还原的是远端下发的指令文本（cmn[] 指令表由服务器回传的制表符分隔串填充），但指令分支与本地执行行为均已在代码中确认。",
  "summary_one_liner": "伪装为 PUBG 外挂 Void PubgHack，无任何无障碍引导页与用途说明，靠用户自行在系统设置开启唯一无描述的无障碍服务，获权后由 C2 sabanjm2.ddns.net:7771 下发指令开启全量界面文本读屏外发并可远程启动摄像头。",
  "disguise_identity": {
    "app_display_name": "Void PubgHack",
    "claimed_brand_or_persona": "PUBG（com.tencent.ig）作弊/外挂工具",
    "a11y_service_label": "Void PubgHack",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务未配置 android:description，系统列表无任何用途说明；服务类名/包名全为随机小写串（package.name.xfcsmhyqynpchfebulknuveqofbxhosbp10872）；字符串资源名亦随机化；冷启动后用 setComponentEnabledSetting(...,2) 禁用自身 Launcher 组件隐藏图标；WebView 加载非 URL 字符串 com.tencent.ig 必然出错，再以黑底白字错误页顶替真实界面"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "package.name.oxkoxccxyloozajerukgvqgjumuxqfhwnjiiuxghguaupxvjsfzrikdyqaukhfhsesapsbjtnczbqmtwqlelgpndgkstcwza1094（唯一 LAUNCHER Activity，Theme.Translucent.NoTitleBar）",
      "trigger_event": "onCreate：requestWindowFeature + 按字符串第 0/2/3 位字符与常量 c1 比较的静态开关决定分支",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "b<html><head><style type=\"text/css\">body{color: #fff; background-color: #000;}</style></head><body>  …  </body></html>",
      "shown_text_zh": "黑底白字的空白/错误页模板，页面内容仅填充 WebView 的 onReceivedError 错误描述字符串",
      "user_action_requested": "无任何提示或按钮；页面无引导文案，用户唯一可做的是自行退出应用",
      "code_anchor": "oxkoxccxyloozajerukgvqgjumuxqfhwnjiiuxghguaupxvjsfzrikdyqaukhfhsesapsbjtnczbqmtwqlelgpndgkstcwza1094.onCreate / res/layout/webllpyzpuepg1117.xml / tzscqcwccfxkseexigrkkibpevvhjedrcasfodkgotlhzjsffimzcoolycyvgosxbgislziewlwrxupvcqbbseonmhhmfoazb1089.gh"
    },
    {
      "step": 2,
      "stage": "获权后动作",
      "screen_or_component": "系统设置 → 无障碍 → 服务项 \"Void PubgHack\"（用户自行进入，应用不跳转）",
      "trigger_event": "用户在系统无障碍列表中手动开启该服务（应用内无 startActivity 跳转，静态未找到 ACTION_ACCESSIBILITY_SETTINGS）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Void PubgHack",
      "shown_text_zh": "系统无障碍列表仅显示服务名 Void PubgHack，无 android:description 说明文字",
      "user_action_requested": "用户需自行开关该服务；应用未提供取消/跳过逻辑，因为根本没有前置提示",
      "code_anchor": "#1 manifest:components / res/values/strings.xml czdxykqsnnousufr1104"
    },
    {
      "step": 3,
      "stage": "获权后动作",
      "screen_or_component": "package.name.xfcsmhyqynpchfebulknuveqofbxhosbp10872（AccessibilityService）",
      "trigger_event": "onServiceConnected → setServiceInfo(eventTypes=-1, flags=89, feedbackType=16)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面；静默把监听范围扩大到全部无障碍事件类型",
      "user_action_requested": "无",
      "code_anchor": "xfcsmhyqynpchfebulknuveqofbxhosbp10872.onServiceConnected"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "xfcsmhyqynpchfebulknuveqofbxhosbp10871$ta（后台指令循环）+ mtrjephavfwonygfsqzjlbamehgbikvnnxtlkkguguz1088（Socket 通道）",
      "trigger_event": "常驻服务 onCreate 启动 AsyncTask 循环，从 sabanjm2.ddns.net:7771 接收制表符分隔指令；命中 cmn[11] 分支时调用 acc() 读取 enabled_accessibility_services 判定是否已获权并置 k=true",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "sabanjm2.ddns.net",
      "shown_text_zh": "远端 C2 域名；指令内容为服务器下发的分隔字符串，本地仅见分支索引",
      "user_action_requested": "无",
      "code_anchor": "xfcsmhyqynpchfebulknuveqofbxhosbp10871$ta.doInBackground / tzscqcwccfxkseexigrkkibpevvhjedrcasfodkgotlhzjsffimzcoolycyvgosxbgislziewlwrxupvcqbbseonmhhmfoazb1089.acc"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "xfcsmhyqynpchfebulknuveqofbxhosbp10872.onAccessibilityEvent → s() → Socket 外发",
      "trigger_event": "k 为真时，对 TYPE_VIEW_CLICKED/TEXT_CHANGED/WINDOW_STATE_CHANGED 等事件逐条采集",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（界面侧无提示）",
      "shown_text_zh": "无提示；后台将「应用名 + 界面文本 + 事件类型」写入 C2 连接",
      "user_action_requested": "无",
      "code_anchor": "xfcsmhyqynpchfebulknuveqofbxhosbp10872.onAccessibilityEvent / xfcsmhyqynpchfebulknuveqofbxhosbp10872.s"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "package.name.wtarloxwlakgbgtnhhgxdfqyhpnhtertunmifdezflkglbcjxvjlmrrrdckvbpcgjrlotkhedhsrujnf1092（摄像头远控服务）+ 1x1 透明 SurfaceView（type 2006）",
      "trigger_event": "C2 下发启动摄像头指令 → onStartCommand 以 WindowManager.addView 挂 1×1 透明窗口并 Camera.open()",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无可见内容；1×1 全透明悬浮窗，用户无感知",
      "user_action_requested": "无",
      "code_anchor": "wtarloxwlakgbgtnhhgxdfqyhpnhtertunmifdezflkglbcjxvjlmrrrdckvbpcgjrlotkhedhsrujnf1092.onStartCommand / ck()"
    }
  ],
  "text_presentation_locations": [
    "无障碍服务标签：res/values/strings.xml 的 czdxykqsnnousufr1104 = \"Void PubgHack\"，经 Manifest 中 android:label 显示于系统「设置 → 无障碍」列表项",
    "无障碍服务说明：完全缺失（Manifest 未设置 android:description，系统设置页该服务无用途描述）",
    "主界面：res/layout/webllpyzpuepg1117.xml 的全屏 WebView，加载非 URL 字符串 com.tencent.ig，出错后由 tzscqcwccfxkseexigrkkibpevvhjedrcasfodkgotlhzjsffimzcoolycyvgosxbgislziewlwrxupvcqbbseonmhhmfoazb1089.gh() 拼成黑底白字 HTML 显示错误串（无引导文案）",
    "前台通知：res/layout/gnvidyyaqckkc1118.xml 为 0×0、背景 #01ffffff 的透明 LinearLayout，作为 RemoteViews 承载通知，通知标题与正文均被 setContentTitle(null)/setContentText(null) 置空，视觉上无任何提示",
    "不存在任何引导弹窗、悬浮遮罩、GIF/图片教学、本地或远端 HTML 教学页（assets 目录为空，res/raw/gmplhmgdibkialoaglp1114 为 0 字节占位）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Void PubgHack",
      "text_zh": "Void 版 PUBG 外挂",
      "source_location": "res/values/strings.xml key czdxykqsnnousufr1104（同时为 android:label 与无障碍服务 label）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "<html><head><style type=\"text/css\">body{color: #fff; background-color: #000;}</style></head><body>",
      "text_zh": "黑底白字的空白页模板（正文仅填 WebView 错误描述）",
      "source_location": "tzscqcwccfxkseexigrkkibpevvhjedrcasfodkgotlhzjsffimzcoolycyvgosxbgislziewlwrxupvcqbbseonmhhmfoazb1089.gh() 硬编码",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "sabanjm2.ddns.net",
      "text_zh": "（C2 服务器域名，非面向用户文本）",
      "source_location": "res/values/strings.xml key dutqenukqobvkpzbyde1101",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "无拒绝循环：应用不做任何跳转，因此不存在 onResume 重跳或定时器拉起；也完全没有降级路径。仅在用户自行开启后，C2 指令分支通过 acc() 读取 enabled_accessibility_services 确认状态并回传 1/0",
    "overlay_or_fake_settings": "无引导遮罩、无高仿系统无障碍页；唯一悬浮窗是摄像头服务使用的 1×1 全透明 SurfaceView（type 2006），属隐蔽取帧而非引导",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无 GLOBAL_ACTION_BACK/HOME 阻止撤权逻辑；但具备反卸载辅助能力：Boot 广播接收器（priority 999）自启、前台透明通知保活、exi() 中以 Process.killProcess 重启，且 onCreate 会禁用自身 Launcher 组件隐藏图标",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "本样本没有跳转设置页的瞬间，UTG 应在冷启动时立即拉起（Activity onCreate 后约 500ms 内截取首屏），并在用户手动开启无障碍服务后（服务 onServiceConnected 触发时刻）再次拉起，观察后台 Socket 外连与 1×1 透明窗口",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动外壳页（WebView 错误页）",
        "page_identifier": "Activity 为 package.name.oxkoxccxyloozajerukgvqgjumuxqfhwnjiiuxghguaupxvjsfzrikdyqaukhfhsesapsbjtnczbqmtwqlelgpndgkstcwza1094，全屏单 WebView（id=web），内容为黑底白字、仅一行错误描述",
        "why_most_useful": "确认应用没有任何真实功能与引导文案，宣称的「PUBG 外挂」实际为空壳，是判定伪装身份与 static_hidden 获权方式的关键",
        "observable_utg_signals": [
          "页面文本极短且为 WebView 错误串（ERR_UNKNOWN_URL_SCHEME 等）",
          "无按钮、无输入框、无任何「开启/授权/允许」节点",
          "状态栏/标题为空（Theme.Translucent.NoTitleBar + requestWindowFeature）"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍列表中出现 label 为 Void PubgHack、副标题为空的条目",
        "why_most_useful": "证明该服务无 android:description、以外部挂名示人，用户无法得知真实读屏用途",
        "observable_utg_signals": [
          "列表项文本仅 \"Void PubgHack\"，无描述行",
          "开关状态变化即为获权时刻（可对齐后续流量爆发）"
        ]
      },
      {
        "page_role": "获权后后台行为观测点（无界面）",
        "page_identifier": "无障碍服务启用后 30s 内：外连 sabanjm2.ddns.net:7771 的 TCP 会话 + 1×1 全透明 WindowManager 窗口（type 2006）",
        "why_most_useful": "把「系统设置开关」与「读屏数据外发/摄像头取帧」绑定，是恶意性质的直接证据",
        "observable_utg_signals": [
          "DNS 解析/连接到 sabanjm2.ddns.net 的流量",
          "窗口层级中出现 1×1 透明 overlay",
          "前台通知标题与正文为空（RemoteViews 0×0）"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在两点盲区：一是全程无引导文本，纯靠用户自发动机（想开挂）去系统设置开启，UTG 若只按「弹窗/教学页」特征匹配会漏判，需改为「无障碍服务存在但无 description + 冷启动无真实功能界面」组合判定；二是 C2 指令表（cmn[]）为远端下发的分隔字符串，静态不可还原，读屏开关与摄像头指令的真实下发时机需动态抓包确认。"
  },
  "behavior_pattern_tags": [
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "TRIG_COLD_START_BLOCK"
  ],
  "code_anchors": [
    "package.name.xfcsmhyqynpchfebulknuveqofbxhosbp10872.onServiceConnected",
    "package.name.xfcsmhyqynpchfebulknuveqofbxhosbp10872.onAccessibilityEvent",
    "package.name.xfcsmhyqynpchfebulknuveqofbxhosbp10871$ta.doInBackground",
    "package.name.tzscqcwccfxkseexigrkkibpevvhjedrcasfodkgotlhzjsffimzcoolycyvgosxbgislziewlwrxupvcqbbseonmhhmfoazb1089.acc",
    "package.name.oxkoxccxyloozajerukgvqgjumuxqfhwnjiiuxghguaupxvjsfzrikdyqaukhfhsesapsbjtnczbqmtwqlelgpndgkstcwza1094.onCreate",
    "res/values/strings.xml (czdxykqsnnousufr1104 / dutqenukqobvkpzbyde1101) / res/layout/webllpyzpuepg1117.xml"
  ]
}
```

</details>
