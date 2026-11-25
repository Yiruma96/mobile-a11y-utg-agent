# MB_044__1495da4ff4｜SpyNote — олях

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：196.5s

## 1. 一句话核心结论

- **核心申请方式**：应用在完全无 UI、无任何说明文字的情况下，凭硬编码开关位 gp="11111" 于冷启动与每次 onResume 直接静默跳转系统无障碍设置页，服务名伪装为 systeminformation.android.app，获权后立即禁用自身桌面图标。
- **静态可见性说明**：无障碍诱导全部逻辑（C7.c、C7$1.run、C1.onServiceConnected、C7.a）与开关位 res/values/strings.xml#gp 均以明文静态可见，无加壳、无加密字符串、无远端 HTML 或 WebView。仅 res/raw/google.apk 为 0 字节占位（二阶段投放槽为空），不影响本链条判定。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `1495da4ff455fceb8fc73f38b75d65be3435c649b2aaf014124e9c58da930c37` |
| 包名 / 年份 | `cmf0.c3b5bm90zq.patch` / 2026 |
| 家族 / 品类 | **SpyNote**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | олях |
| 引导页宣称品牌/身份 | systeminformation.android.app（伪造的“系统信息”包名，用于冒充系统组件） |
| 系统无障碍列表服务名 | systeminformation.android.app |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务 android:label 使用 @string/s = "systeminformation.android.app" 而非真实应用名 олях；服务未配置 android:description（无任何授权说明）；应用主题为 Theme.Translucent.NoTitleBar 且启动 Activity 不加载任何布局，运行期无任何界面文字可被用户或 OCR 读取；启动器 Activity C7 在获权后通过 setComponentEnabledSetting 设为 DISABLED 自隐藏；无多 activity-alias、无同形字、无伪造 isAccessibilityTool。 |
| 无障碍服务类名 | `cmf0.c3b5bm90zq.patch.C1` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | cmf0.c3b5bm90zq.patch.C7（LAUNCHER Activity，主题 @android:style/Theme.Translucent.NoTitleBar） | onCreate() → 直接调用 c()；无 setContentView | 原生Activity | 无 | 无提示，用户仅看到图标被点击后系统设置页被拉起 | `cmf0.c3b5bm90zq.patch.C7.onCreate / C7.c` |
| 2 | 业务功能触发 | cmf0.c3b5bm90zq.patch.C7.c() 读取 res/values/strings.xml#gp | Resources.getString(0x7f0c0021) 取得 gp="11111"，逐字符判定 charAt(1)/(3)/(4)/(0) | 不可静态还原 | **原文**：11111<br>**译注**：硬编码开关串：第0位=隐藏图标 第1位=跳无障碍 第2位=图标采集 第3位=设备管理器 第4位=root检测 | 无 | `cmf0.c3b5bm90zq.patch.C7.c / res/values/strings.xml#gp` |
| 3 | 跳受限设置 | 系统设备管理器激活页（Intent android.app.action.ADD_DEVICE_ADMIN） | C7$1.run 中 gp.charAt(3)=='1' 且 c.a()==false → startActivityForResult(intent, 100) | 系统无障碍页 | **原文**：intent.putExtra("android.app.extra.ADD_EXPLANATION", "")<br>**译注**：设备管理器激活说明文本被显式置为空字符串，系统页仅显示应用名与系统默认模板，无任何业务理由 | 系统页要求点击“激活”，应用侧无取消/跳过提示 | `cmf0.c3b5bm90zq.patch.C7$1.run / res/xml/device_admin.xml（wipe-data、reset-password、force-lock、disable-camera 等全部策略）` |
| 4 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | C7$1.run 中 gp.charAt(1)=='1' 且 !C11.j → new Intent().setFlags(FLAG_ACTIVITY_NEW_TASK).setAction("android.settings.ACCESSIBILITY_SETTINGS"); startActivity | 系统无障碍页 | **原文**：无（应用未提供任何前置说明页、Dialog、WebView 或 HTML）<br>**译注**：直接跳到系统无障碍设置根页面，不指定具体服务详情，需用户自行在列表中寻找 | 要求用户在系统无障碍列表中手动找到并开启名为 systeminformation.android.app 的服务；无取消/跳过按钮 | `cmf0.c3b5bm90zq.patch.C7$1.run` |
| 5 | 引导说明页（缺失环节） | 系统无障碍列表项：label=@string/s，无 android:description | 服务在无障碍列表中呈现 | 系统无障碍页 | **原文**：systeminformation.android.app<br>**译注**：用户在系统列表里看到的服务名是一个伪造的“系统信息”包名字符串，与桌面应用名 олях 完全无关，也没有任何功能说明 | 开启开关 | `AndroidManifest.xml 中 service cmf0.c3b5bm90zq.patch.C1（android:label="@string/s"）/ res/values/strings.xml#s` |
| 6 | 拒权反馈循环 | C7.onResume → c() → new Thread(C7$1).start() | 用户从设置页返回（未开启服务）→ onResume 触发，C11.j 仍为 false | 原生Activity | 无 | 用户需反复按返回或强行结束进程才能脱离；无降级路径 | `cmf0.c3b5bm90zq.patch.C7.onResume / C7.c / C7$1.run` |
| 7 | 获权后动作 | cmf0.c3b5bm90zq.patch.C1.onServiceConnected / C7.a() | 服务连接成功 → 置 C11.j=true；gp.charAt(0)=='1' → setComponentEnabledSetting(C7, COMPONENT_ENABLED_STATE_DISABLED) | 不可静态还原 | **原文**：accessibilityServiceInfo.flags = 89; eventTypes = -1; feedbackType = 16<br>**译注**：开启全量事件监听并禁用自身桌面图标，使应用从启动器消失 | 无；用户此后难以再次找到该应用入口 | `cmf0.c3b5bm90zq.patch.C1.onServiceConnected / C7.a` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 应用侧：无任何位置。C7 未调用 setContentView，未使用 Dialog/Fragment/WebView，工程内无 assets 目录、无自定义 layout（res/layout 仅含 appcompat 的 abc_* 与 C6 的 chat.xml）
- 系统无障碍列表：仅显示 android:label="@string/s" 解析出的 systeminformation.android.app；未配置 android:description，故说明栏为空
- 桌面图标名：@string/app_name = олях（与无障碍服务名不一致）
- 系统设备管理器激活页：ADD_EXPLANATION 被显式传入空字符串 ""
- res/values/strings.xml 中仅存的业务相关字面量：gp=11111、h=justin-subcategories.with.playit.plus、p=28098、v=0.09.2021、MER=..
- C6 聊天界面内硬编码多语种提示 “Write a message / 鍵入消息 / Bir mesaj yaz” 等，属远控会话界面，与无障碍引导无关

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| ru | олях | олях（无实义字符串，用作桌面图标名） | `res/values/strings.xml key=app_name / key=n` | 未知 |
| en | systeminformation.android.app | systeminformation.android.app（伪造的“系统信息”应用包名） | `res/values/strings.xml key=s（用于 android:label 与无障碍服务名）` | 假反诈安全 |
| en | 11111 | 11111（硬编码开关串，全开：隐藏图标、跳无障碍、采集图标、请求设备管理器、root 检测） | `res/values/strings.xml key=gp（代码 0x7f0c0021）` | 未知 |
| en | android.settings.ACCESSIBILITY_SETTINGS | 系统无障碍设置页动作（无附带说明文字） | `cmf0.c3b5bm90zq.patch.C7$1.run 硬编码 Intent action` | 教唆忽视警告 |
| en | android.app.action.ADD_DEVICE_ADMIN / android.app.extra.ADD_EXPLANATION = "" | 设备管理器激活请求，激活说明为空字符串 | `cmf0.c3b5bm90zq.patch.C7$1.run 硬编码` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：C7.onResume 无条件再次调用 c()；c() 内部以 new Thread(C7$1) 重新评估 gp.charAt(1)=='1' && !C11.j，用户从系统设置返回而未开启时立即再次 startActivity(ACCESSIBILITY_SETTINGS)，形成无提示的重跳循环；仅当服务真正连接（C11.j=true）或进程被杀才终止
- **遮罩叠层 / 高仿系统设置页**：无。未申请使用 SYSTEM_ALERT_WINDOW 绘制引导遮罩（权限虽声明但该链路未使用），未构造高仿系统开关页，也未在设置页上叠加浮层；因此不存在可截图识别的伪造界面，只有系统原生设置页
- **Android 13+ 受限设置（Restricted Settings）应对**：无。targetSdkVersion=22，代码中未出现 ACTION_APPLICATION_DETAILS_SETTINGS、未出现“允许受限设置”分步教学、未使用 Session 安装器绕过
- **获权后即时行为与防撤权机制**：获权后不监听设置页撤权动作，但立即执行 setComponentEnabledSetting(C7, COMPONENT_ENABLED_STATE_DISABLED) 禁用自身启动图标使应用从桌面消失；同时以空说明请求设备管理器（wipe-data/reset-password/force-lock/disable-camera）增加卸载阻力
- **良性降级 / 替代方案**：无。没有任何替代路径、手动模式或安全降级分支；条件不满足时仅 finish() 或反复重跳

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以 Intent action 为准：Hook/监测 startActivity 的 action 等于 android.settings.ACCESSIBILITY_SETTINGS 或 android.app.action.ADD_DEVICE_ADMIN 的瞬间即拉起 UTG 抓取（冷启动后 1 秒内即发生，不要等界面文字，因为本应用运行期界面全空）
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无纯图诱导盲区（本就无图、无文本、无 HTML）。真正的盲区是“零 UI”形态：常规基于引导弹窗文本/OCR 的检测在此完全失效，必须依赖 Intent action 与组件名 hook；另外 res/raw/google.apk 为 0 字节占位，本样本二阶段投放未落地，若换用带真实载荷的变体需另行核对 base.apk 释放与安装链。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动瞬间的应用侧页面（空白 Translucent Activity）** | cmf0.c3b5bm90zq.patch.C7，主题 Theme.Translucent.NoTitleBar，无任何子 View | 证明应用侧零说明文字、零 UI，与正常应用“先解释后跳转”的合规路径形成直接对比 | Activity 名 cmf0.c3b5bm90zq.patch.C7；层级树中无 TextView/ImageView 等任何可见节点；主题为 Translucent 且无标题栏 |
| **跳转后的系统无障碍服务列表项** | 设置 → 无障碍 → 已下载/已安装的服务，列表项文本为 systeminformation.android.app | 直接固定身份伪装证据：服务名与桌面应用名 олях 不一致，且说明栏为空 | 列表项文本 systeminformation.android.app；该项下方无 description 文本；开关初始为关闭状态 |
| **设备管理器激活页（空说明）** | 系统设备管理器激活对话框，说明文本区域为空 | 证明以空说明请求高风险设备管理策略，属同一静默提权链 | 页面标题含“设备管理”/Device admin；说明文本为空字符串；策略提示含擦除数据、重置密码等 |
| **返回后的重跳循环页** | 从设置页返回后 500ms 内再次出现的系统无障碍设置页 | 证明拒权后无降级、强制重跳的胁迫行为 | 同一 Activity 在返回后短时间内被再次拉起；应用侧无任何提示文本；重复次数≥2 |
| **获权后桌面状态** | 启动器中原图标 олях 消失 | 证明获权后自隐藏，阻碍用户自查与撤权 | 桌面图标数量减少；包 cmf0.c3b5bm90zq.patch 在启动器中不可见 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `cmf0.c3b5bm90zq.patch.C7.c`
- `cmf0.c3b5bm90zq.patch.C7$1.run`
- `cmf0.c3b5bm90zq.patch.C7.onResume`
- `cmf0.c3b5bm90zq.patch.C1.onServiceConnected`
- `cmf0.c3b5bm90zq.patch.C7.a()`
- `res/values/strings.xml（gp / s / app_name / h / p）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

分析已完成：应用没有加壳，核心逻辑可完整静态还原。以下为结论要点。

**核心机制（与常规“引导页教学”完全相反）**
- 启动 Activity [C7](<resource-unit:#1.dex1 code:cmf0.c3b5bm90zq.patch.C7>) 没有 `setContentView`，也没有布局或弹窗；其 `onCreate` 与 `onResume` 都直接调用 [C7.c()](<resource-unit:#1.dex1 code:cmf0.c3b5bm90zq.patch.C7#c>)，因此**界面上不会显示任何文字**。
- 代码读取 [strings.xml](<resource-unit:#1 file:res/values/strings.xml#L36-L41>) 中 `gp="11111"` 的字符位，以此作为硬编码开关；在 [C7$1.run()](<resource-unit:#1.dex1 code:cmf0.c3b5bm90zq.patch.C7$1#run>) 中，第 2 位 `'1'` 会在 `C11.j==false` 时直接 `startActivity(ACTION_ACCESSIBILITY_SETTINGS)`；第 4 位 `'1'` 会以 `ADD_EXPLANATION=""`（空说明）弹出设备管理器授权；第 1 位 `'1'` 会在获权后调用 `setComponentEnabledSetting(C7, DISABLED)` 隐藏桌面图标。
- **服务名伪装**：无障碍服务 `C1` 的 `android:label="@string/s"`，而 `s=systeminformation.android.app`，桌面名是 `олях`。用户在系统无障碍列表中看到的是一个伪造的包名，而不是真实应用名；该服务也没有配置 `android:description`，因此没有授权理由说明。
- **拒绝授权后的循环**：返回时 `onResume → c() → new Thread(C7$1).run()` 会再次判断并重新拉起无障碍设置页，直到 `C11.j` 为 true。
- 获权后，[C1.onServiceConnected()](<resource-unit:#1.dex1 code:cmf0.c3b5bm90zq.patch.C1#onServiceConnected>) 设置 `eventTypes=-1`、`flags=89`；[onAccessibilityEvent()](<resource-unit:#1.dex1 code:cmf0.c3b5bm90zq.patch.C1#onAccessibilityEvent>) 收集全量界面文本并写入 `/sdcard/<s>/config<date>.log`，同时上报 `h=justin-subcategories.with.playit.plus`、`p=28098`。
- 二阶段：`C7$2.run()` 把 `res/raw/google.apk` 复制为 `base.apk` 并触发安装；本样本中该资源为 **0 字节占位**，没有实际载荷。

**可见性判定**：`clear`。逻辑没有加密或远端 HTML，全部在 DEX 与明文 strings 中。唯一不可静态还原的是空的 raw 载荷槽。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍诱导全部逻辑（C7.c、C7$1.run、C1.onServiceConnected、C7.a）与开关位 res/values/strings.xml#gp 均以明文静态可见，无加壳、无加密字符串、无远端 HTML 或 WebView。仅 res/raw/google.apk 为 0 字节占位（二阶段投放槽为空），不影响本链条判定。",
  "summary_one_liner": "应用在完全无 UI、无任何说明文字的情况下，凭硬编码开关位 gp=\"11111\" 于冷启动与每次 onResume 直接静默跳转系统无障碍设置页，服务名伪装为 systeminformation.android.app，获权后立即禁用自身桌面图标。",
  "disguise_identity": {
    "app_display_name": "олях",
    "claimed_brand_or_persona": "systeminformation.android.app（伪造的“系统信息”包名，用于冒充系统组件）",
    "a11y_service_label": "systeminformation.android.app",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务 android:label 使用 @string/s = \"systeminformation.android.app\" 而非真实应用名 олях；服务未配置 android:description（无任何授权说明）；应用主题为 Theme.Translucent.NoTitleBar 且启动 Activity 不加载任何布局，运行期无任何界面文字可被用户或 OCR 读取；启动器 Activity C7 在获权后通过 setComponentEnabledSetting 设为 DISABLED 自隐藏；无多 activity-alias、无同形字、无伪造 isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "cmf0.c3b5bm90zq.patch.C7（LAUNCHER Activity，主题 @android:style/Theme.Translucent.NoTitleBar）",
      "trigger_event": "onCreate() → 直接调用 c()；无 setContentView",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无任何界面元素，Activity 仅执行权限条件判断后结束",
      "user_action_requested": "无提示，用户仅看到图标被点击后系统设置页被拉起",
      "code_anchor": "cmf0.c3b5bm90zq.patch.C7.onCreate / C7.c"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "cmf0.c3b5bm90zq.patch.C7.c() 读取 res/values/strings.xml#gp",
      "trigger_event": "Resources.getString(0x7f0c0021) 取得 gp=\"11111\"，逐字符判定 charAt(1)/(3)/(4)/(0)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "11111",
      "shown_text_zh": "硬编码开关串：第0位=隐藏图标 第1位=跳无障碍 第2位=图标采集 第3位=设备管理器 第4位=root检测",
      "user_action_requested": "无",
      "code_anchor": "cmf0.c3b5bm90zq.patch.C7.c / res/values/strings.xml#gp"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "系统设备管理器激活页（Intent android.app.action.ADD_DEVICE_ADMIN）",
      "trigger_event": "C7$1.run 中 gp.charAt(3)=='1' 且 c.a()==false → startActivityForResult(intent, 100)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "intent.putExtra(\"android.app.extra.ADD_EXPLANATION\", \"\")",
      "shown_text_zh": "设备管理器激活说明文本被显式置为空字符串，系统页仅显示应用名与系统默认模板，无任何业务理由",
      "user_action_requested": "系统页要求点击“激活”，应用侧无取消/跳过提示",
      "code_anchor": "cmf0.c3b5bm90zq.patch.C7$1.run / res/xml/device_admin.xml（wipe-data、reset-password、force-lock、disable-camera 等全部策略）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "C7$1.run 中 gp.charAt(1)=='1' 且 !C11.j → new Intent().setFlags(FLAG_ACTIVITY_NEW_TASK).setAction(\"android.settings.ACCESSIBILITY_SETTINGS\"); startActivity",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用未提供任何前置说明页、Dialog、WebView 或 HTML）",
      "shown_text_zh": "直接跳到系统无障碍设置根页面，不指定具体服务详情，需用户自行在列表中寻找",
      "user_action_requested": "要求用户在系统无障碍列表中手动找到并开启名为 systeminformation.android.app 的服务；无取消/跳过按钮",
      "code_anchor": "cmf0.c3b5bm90zq.patch.C7$1.run"
    },
    {
      "step": 5,
      "stage": "引导说明页（缺失环节）",
      "screen_or_component": "系统无障碍列表项：label=@string/s，无 android:description",
      "trigger_event": "服务在无障碍列表中呈现",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "systeminformation.android.app",
      "shown_text_zh": "用户在系统列表里看到的服务名是一个伪造的“系统信息”包名字符串，与桌面应用名 олях 完全无关，也没有任何功能说明",
      "user_action_requested": "开启开关",
      "code_anchor": "AndroidManifest.xml 中 service cmf0.c3b5bm90zq.patch.C1（android:label=\"@string/s\"）/ res/values/strings.xml#s"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "C7.onResume → c() → new Thread(C7$1).start()",
      "trigger_event": "用户从设置页返回（未开启服务）→ onResume 触发，C11.j 仍为 false",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "不显示任何提示，再次静默拉起无障碍设置页",
      "user_action_requested": "用户需反复按返回或强行结束进程才能脱离；无降级路径",
      "code_anchor": "cmf0.c3b5bm90zq.patch.C7.onResume / C7.c / C7$1.run"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "cmf0.c3b5bm90zq.patch.C1.onServiceConnected / C7.a()",
      "trigger_event": "服务连接成功 → 置 C11.j=true；gp.charAt(0)=='1' → setComponentEnabledSetting(C7, COMPONENT_ENABLED_STATE_DISABLED)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "accessibilityServiceInfo.flags = 89; eventTypes = -1; feedbackType = 16",
      "shown_text_zh": "开启全量事件监听并禁用自身桌面图标，使应用从启动器消失",
      "user_action_requested": "无；用户此后难以再次找到该应用入口",
      "code_anchor": "cmf0.c3b5bm90zq.patch.C1.onServiceConnected / C7.a"
    }
  ],
  "text_presentation_locations": [
    "应用侧：无任何位置。C7 未调用 setContentView，未使用 Dialog/Fragment/WebView，工程内无 assets 目录、无自定义 layout（res/layout 仅含 appcompat 的 abc_* 与 C6 的 chat.xml）",
    "系统无障碍列表：仅显示 android:label=\"@string/s\" 解析出的 systeminformation.android.app；未配置 android:description，故说明栏为空",
    "桌面图标名：@string/app_name = олях（与无障碍服务名不一致）",
    "系统设备管理器激活页：ADD_EXPLANATION 被显式传入空字符串 \"\"",
    "res/values/strings.xml 中仅存的业务相关字面量：gp=11111、h=justin-subcategories.with.playit.plus、p=28098、v=0.09.2021、MER=..",
    "C6 聊天界面内硬编码多语种提示 “Write a message / 鍵入消息 / Bir mesaj yaz” 等，属远控会话界面，与无障碍引导无关"
  ],
  "verbatim_texts": [
    {
      "lang": "ru",
      "text_verbatim": "олях",
      "text_zh": "олях（无实义字符串，用作桌面图标名）",
      "source_location": "res/values/strings.xml key=app_name / key=n",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "systeminformation.android.app",
      "text_zh": "systeminformation.android.app（伪造的“系统信息”应用包名）",
      "source_location": "res/values/strings.xml key=s（用于 android:label 与无障碍服务名）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "11111",
      "text_zh": "11111（硬编码开关串，全开：隐藏图标、跳无障碍、采集图标、请求设备管理器、root 检测）",
      "source_location": "res/values/strings.xml key=gp（代码 0x7f0c0021）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "android.settings.ACCESSIBILITY_SETTINGS",
      "text_zh": "系统无障碍设置页动作（无附带说明文字）",
      "source_location": "cmf0.c3b5bm90zq.patch.C7$1.run 硬编码 Intent action",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "android.app.action.ADD_DEVICE_ADMIN / android.app.extra.ADD_EXPLANATION = \"\"",
      "text_zh": "设备管理器激活请求，激活说明为空字符串",
      "source_location": "cmf0.c3b5bm90zq.patch.C7$1.run 硬编码",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "C7.onResume 无条件再次调用 c()；c() 内部以 new Thread(C7$1) 重新评估 gp.charAt(1)=='1' && !C11.j，用户从系统设置返回而未开启时立即再次 startActivity(ACCESSIBILITY_SETTINGS)，形成无提示的重跳循环；仅当服务真正连接（C11.j=true）或进程被杀才终止",
    "overlay_or_fake_settings": "无。未申请使用 SYSTEM_ALERT_WINDOW 绘制引导遮罩（权限虽声明但该链路未使用），未构造高仿系统开关页，也未在设置页上叠加浮层；因此不存在可截图识别的伪造界面，只有系统原生设置页",
    "restricted_settings_13plus_coaching": "无。targetSdkVersion=22，代码中未出现 ACTION_APPLICATION_DETAILS_SETTINGS、未出现“允许受限设置”分步教学、未使用 Session 安装器绕过",
    "post_grant_anti_removal": "获权后不监听设置页撤权动作，但立即执行 setComponentEnabledSetting(C7, COMPONENT_ENABLED_STATE_DISABLED) 禁用自身启动图标使应用从桌面消失；同时以空说明请求设备管理器（wipe-data/reset-password/force-lock/disable-camera）增加卸载阻力",
    "benign_graceful_degradation": "无。没有任何替代路径、手动模式或安全降级分支；条件不满足时仅 finish() 或反复重跳"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以 Intent action 为准：Hook/监测 startActivity 的 action 等于 android.settings.ACCESSIBILITY_SETTINGS 或 android.app.action.ADD_DEVICE_ADMIN 的瞬间即拉起 UTG 抓取（冷启动后 1 秒内即发生，不要等界面文字，因为本应用运行期界面全空）",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动瞬间的应用侧页面（空白 Translucent Activity）",
        "page_identifier": "cmf0.c3b5bm90zq.patch.C7，主题 Theme.Translucent.NoTitleBar，无任何子 View",
        "why_most_useful": "证明应用侧零说明文字、零 UI，与正常应用“先解释后跳转”的合规路径形成直接对比",
        "observable_utg_signals": ["Activity 名 cmf0.c3b5bm90zq.patch.C7", "层级树中无 TextView/ImageView 等任何可见节点", "主题为 Translucent 且无标题栏"]
      },
      {
        "page_role": "跳转后的系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已下载/已安装的服务，列表项文本为 systeminformation.android.app",
        "why_most_useful": "直接固定身份伪装证据：服务名与桌面应用名 олях 不一致，且说明栏为空",
        "observable_utg_signals": ["列表项文本 systeminformation.android.app", "该项下方无 description 文本", "开关初始为关闭状态"]
      },
      {
        "page_role": "设备管理器激活页（空说明）",
        "page_identifier": "系统设备管理器激活对话框，说明文本区域为空",
        "why_most_useful": "证明以空说明请求高风险设备管理策略，属同一静默提权链",
        "observable_utg_signals": ["页面标题含“设备管理”/Device admin", "说明文本为空字符串", "策略提示含擦除数据、重置密码等"]
      },
      {
        "page_role": "返回后的重跳循环页",
        "page_identifier": "从设置页返回后 500ms 内再次出现的系统无障碍设置页",
        "why_most_useful": "证明拒权后无降级、强制重跳的胁迫行为",
        "observable_utg_signals": ["同一 Activity 在返回后短时间内被再次拉起", "应用侧无任何提示文本", "重复次数≥2"]
      },
      {
        "page_role": "获权后桌面状态",
        "page_identifier": "启动器中原图标 олях 消失",
        "why_most_useful": "证明获权后自隐藏，阻碍用户自查与撤权",
        "observable_utg_signals": ["桌面图标数量减少", "包 cmf0.c3b5bm90zq.patch 在启动器中不可见"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无纯图诱导盲区（本就无图、无文本、无 HTML）。真正的盲区是“零 UI”形态：常规基于引导弹窗文本/OCR 的检测在此完全失效，必须依赖 Intent action 与组件名 hook；另外 res/raw/google.apk 为 0 字节占位，本样本二阶段投放未落地，若换用带真实载荷的变体需另行核对 base.apk 释放与安装链。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED"
  ],
  "code_anchors": [
    "cmf0.c3b5bm90zq.patch.C7.c",
    "cmf0.c3b5bm90zq.patch.C7$1.run",
    "cmf0.c3b5bm90zq.patch.C7.onResume",
    "cmf0.c3b5bm90zq.patch.C1.onServiceConnected",
    "cmf0.c3b5bm90zq.patch.C7.a()",
    "res/values/strings.xml（gp / s / app_name / h / p）"
  ]
}
```

**补充说明与边界**
- 已登记风险 `R-001`（autonomous_audit / high / malware_trojan），命题限定为“无说明静默跳转 + 服务名伪装 + 获权自隐藏”。
- 同一链条中的**空说明设备管理器提权**与 `C7$2` 的 `base.apk` 释放安装能力已在正文说明，但未单列风险条目（受 14 次工具调用上限约束）；如需独立命题可追加登记。
- 未使用动态分析：静态证据已完整闭合，且无在线设备需求。
- 覆盖边界：`res/raw/google.apk` 为 0 字节，二阶段真实载荷内容不可评估。

</details>
