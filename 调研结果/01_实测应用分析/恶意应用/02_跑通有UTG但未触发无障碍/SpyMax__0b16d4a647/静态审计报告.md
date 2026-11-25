# MR_061__0b16d4a647｜SpyMax — media player

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：119.8s

## 1. 一句话核心结论

- **核心申请方式**：以不可见透明 Activity 为桌面入口，冷启动即按字符串位掩码静默直跳系统无障碍设置、无任何说明文字与取消入口，返回即死循环重跳，获权后立刻静默安装内嵌载荷 APK。
- **静态可见性说明**：引导链路全部为明文 DEX 与本地资源可见：跳转点、开关位掩码（@string/gp）、服务启用标志 C11.j、内嵌 res/raw/google.apk 均可静态定位；未加壳、无 AES/远端 HTML 参与无障碍引导。二阶段载荷 google.apk 内部行为不在本次范围。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `0b16d4a647349dc1b67186b73b1f0f5937ccfc4c120f47ad37ec2ec80ca787d7` |
| 包名 / 年份 | `cmf0.c3b5bm90zq.patch` / 2020 |
| 家族 / 品类 | **SpyMax**（同池样本数：23） |
| 原始来源标识 | https://blog.lookout.com/commercial-surveillanceware-operators-latest-to-take-advantage-of-covid-19 |
| 桌面显示名 | media player |
| 引导页宣称品牌/身份 | media player（伪装为媒体播放器，实际为短信/联系人/通话/录音窃取与载荷投放的木马） |
| 系统无障碍列表服务名 | media player（服务 C1 未声明 android:label，系统列表回退应用名，且无 android:description） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 全部类名/字符串资源名混淆为 C1~C15、a/b/c、gp/MER/s；2) 启动 Activity 使用 Theme.Translucent.NoTitleBar + excludeFromRecents，桌面点击无可视界面；3) @string/gp="10010" 作为位掩码同时控制跳无障碍、请求设备管理员、禁用自身组件隐藏图标；4) 无障碍服务刻意不写 label/description，避免暴露权限用途；5) 服务名与功能无关联（service player）。 |
| 无障碍服务类名 | `cmf0.c3b5bm90zq.patch.C1` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | cmf0.c3b5bm90zq.patch.C7（LAUNCHER，Theme.Translucent.NoTitleBar，excludeFromRecents） | onCreate() → c()；onResume() → c() | 原生Activity | 无 | 无提示；用户仅感知“点了图标什么都没发生” | `cmf0.c3b5bm90zq.patch.C7#onCreate / #onResume / #c` |
| 2 | 业务功能触发 | C7.b() → 新线程 C7$1 | c() 中无条件调用 b() 启动线程 | 不可静态还原 | 无 | 无 | `cmf0.c3b5bm90zq.patch.C7#b ; cmf0.c3b5bm90zq.patch.C7$1#run` |
| 3 | 跳受限设置 | 系统“设备管理员”激活页（android.app.action.ADD_DEVICE_ADMIN） | C7$1.run 中 gp.charAt(3)=='1' 且设备管理员未激活 → startActivityForResult(intent,100)，ADD_EXPLANATION 传空串 | 系统无障碍页 | **原文**：android.app.extra.ADD_EXPLANATION = ""<br>**译注**：系统设备管理员激活页，说明字段被置空，用户看不到任何申请理由 | 点击“激活”按钮；无应用侧取消/跳过（仅系统返回） | `cmf0.c3b5bm90zq.patch.C7$1#run` |
| 4 | 跳无障碍设置 | 系统设置 → 无障碍 → 服务列表（android.settings.ACCESSIBILITY_SETTINGS） | C7$1.run 中 gp.charAt(1)=='1' 且静态标志 C11.j 为 false（服务未连接）→ startActivity(Intent(ACTION_ACCESSIBILITY_SETTINGS).setFlags(0x10000000)) | 系统无障碍页 | **原文**：无（应用不提供任何前置说明或弹窗）<br>**译注**：直接落在系统无障碍服务列表，列表项仅显示应用名 media player，无用途描述 | 手动找到“media player”并打开开关；应用未提供取消/跳过按钮 | `cmf0.c3b5bm90zq.patch.C7$1#run ; #1 manifest:components` |
| 5 | 拒权反馈循环 | C7.onResume → c() → b() → C7$1.run | 用户从系统设置页返回（未开启服务，C11.j 仍为 false）触发 onResume | 系统无障碍页 | 无 | 无法通过返回退出，只能开启无障碍服务（或强制结束进程） | `cmf0.c3b5bm90zq.patch.C7#onResume / #c` |
| 6 | 获权后动作 | C1（AccessibilityService）onServiceConnected + C7$2 载荷安装 | 服务被系统绑定 → setServiceInfo(eventTypes=-1, flags=89) → C11.j=true；随后 C7$1.run 判定 z&&z2 成立 → 复制 res/raw/google.apk 到 /sdcard/<MER>/base.apk 并启动安装（或 su pm install -r） | 系统无障碍页 | **原文**：无（安装界面由系统 PackageInstaller 呈现，应用未附任何说明）<br>**译注**：获权即全量监听界面事件，同时静默投放内嵌 APK 载荷；若 gp.charAt(0)=='1' 则再调用 setComponentEnabledSetting(C7, COMPONENT_DISABLED) 隐藏桌面图标 | 在系统安装页确认安装二阶段 APK | `cmf0.c3b5bm90zq.patch.C1#onServiceConnected ; cmf0.c3b5bm90zq.patch.C7$2#run ; cmf0.c3b5bm90zq.patch.C7#a` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 应用侧无任何引导/说明文字呈现位置：无 AlertDialog、无 WebView、assets 下仅有 google.apk（无 HTML/图片引导）、res/raw 仅有载荷 APK
- 系统无障碍服务列表项：仅显示应用名 media player（C1 服务未声明 android:label / android:description，无用途说明）
- 系统设备管理员激活页：android.app.extra.ADD_EXPLANATION 被硬编码为空字符串 ""，说明区为空
- 桌面图标：@string/app_name = "media player"；gp.charAt(0)=='1' 时通过 setComponentEnabledSetting(C7,2,1) 使入口消失
- 唯一自定义 UI（res/layout/chat.xml，C6 远程聊天窗“Write a message”）与无障碍引导无关，属远程控制会话界面

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | media player | 媒体播放器 | `res/values/strings.xml app_name；AndroidManifest 中 application/activity C7 的 android:label` | 清理工具伪装 |
| en | service player | 播放器服务 | `res/values/strings.xml key=s（C11/C5/C15 服务 android:label）` | 未知 |
| en | 10010 | 10010（位掩码：第0位隐藏图标=1、第1位跳无障碍=1、第2位监听文本=0、第3位设备管理员=1、第4位root截屏=0） | `res/values/strings.xml key=gp（0x7f0c0021），由 C7.c / C7$1.run / C1.b 逐位读取` | 教唆忽视警告 |
| en | .. | ..（占位符，表示未配置目标包名，此时不启动任何目标应用） | `res/values/strings.xml key=MER（0x7f0c0000）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：用户从系统设置页返回未开启服务时，C7.onResume 再次执行 c()→b()→C7$1.run，因 C11.j（仅由 C1.onServiceConnected 置 true）仍为 false，无条件重新 startActivity(ACTION_ACCESSIBILITY_SETTINGS)，形成返回-重跳循环；C7 自身无 UI 且不 finish，无退出路径。
- **遮罩叠层 / 高仿系统设置页**：无叠层引导遮罩、无高仿系统无障碍开关页；C5 通过 WindowManager.addView 添加 1×1 的 TYPE_SYSTEM_OVERLAY(2006) SurfaceView 属相机偷拍预览，不承载任何引导文字。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=22，未使用 ACTION_APPLICATION_DETAILS_SETTINGS，全包无该 action 字符串）
- **获权后即时行为与防撤权机制**：获权后通过 gp.charAt(0)=='1' 调用 PackageManager.setComponentEnabledSetting(C7, 2, 1) 禁用启动组件以隐藏桌面图标，降低用户发现与卸载概率；同时申请设备管理员（BIND_DEVICE_ADMIN，C2）提高卸载难度；未见监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权。
- **良性降级 / 替代方案**：无（未获权时不会降级为手动模式，而是持续强制重跳系统设置页）

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动 com.cmf0...C7 后立即出现 android.settings.ACCESSIBILITY_SETTINGS 页面切换（Activity 栈顶变为 com.android.settings 无障碍页且无任何应用侧前置界面）；或监测到 startActivity 携带 action=android.settings.ACCESSIBILITY_SETTINGS / android.app.action.ADD_DEVICE_ADMIN 时拉起 UTG 抓栈。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：应用侧完全不呈现任何文本（无弹窗/HTML/悬浮引导），若 UTG 仅在应用自身窗口内取文本将零信号；必须依赖“页面流转事件”（跳转系统无障碍页、返回后立即重跳）作为判别依据。另需注意 gp 位掩码可远程/本地改写，若 charAt(1) 被置为 '0'，则该样本在运行期完全不出现无障碍引导，纯文本/单次抓屏会漏检。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后第一屏（跳转前）** | 栈顶为 cmf0.c3b5bm90zq.patch.C7，透明无内容、无任何文字控件 | 证明应用在零解释、零前置说明情况下直接跳转，是“静默强跳”而非用户主动申请的关键证据 | 页面层级中无 TextView/按钮节点；无弹窗/对话框节点；Activity 名 C7 与桌面图标点击一一对应 |
| **系统无障碍服务列表项** | com.android.settings 无障碍页中包含文本 media player 的服务条目，条目下无描述行 | 核对系统展示给用户的服务身份与说明缺失（无 android:description），确认身份伪装与告知缺失 | 条目文本 media player；无副标题/描述文本；开关初始为关闭状态 |
| **从系统设置返回后的重跳页面** | 连续两次 capture 中出现相同的 com.android.settings 无障碍页，间隔仅一次返回操作 | 捕获 onResume 死循环重跳，是判定强制诱导/无退出路径的决定性运行证据 | 相同页面在 1~3 秒内重复出现；中间无应用侧页面；返回键无法离开该页面 |
| **获权后系统安装器页面** | 系统 PackageInstaller 界面，安装源路径为 /sdcard/<MER>/base.apk | 证明无障碍获权后立即触发二阶段载荷投递，说明引导目的并非无障碍功能本身 | 安装确认页出现时机紧跟无障碍开关打开；安装包来源为外部存储 base.apk；应用未提供任何安装说明文字 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `cmf0.c3b5bm90zq.patch.C7#onCreate / #onResume / #c`
- `cmf0.c3b5bm90zq.patch.C7$1#run`
- `cmf0.c3b5bm90zq.patch.C1#onServiceConnected`
- `cmf0.c3b5bm90zq.patch.C7$2#run`
- `res/values/strings.xml（app_name / s / gp / MER）`
- `AndroidManifest.xml service cmf0.c3b5bm90zq.patch.C1（BIND_ACCESSIBILITY_SERVICE，无 label/description）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点（无障碍引导流程 · 纯运行期视角）

- **完全没有引导文案**：全包无 `AlertDialog`、`WebView`、`assets` 内 HTML（`assets/` 只有 `google.apk`）、无 `res/raw` 引导页，唯一自定义布局是远程聊天窗 [chat.xml](<resource-unit:#1 file:res/layout/chat.xml>)。无障碍权限申请**不经过任何说明页/弹窗**，属于“零解释静默跳转”型。
- **冷启动即跳系统无障碍页**：桌面入口 [C7](<resource-unit:#1.dex1 code:cmf0.c3b5bm90zq.patch.C7>) 为 `Theme.Translucent.NoTitleBar` + `excludeFromRecents`（不可见“空壳”Activity），`onCreate()` 与 `onResume()` 均调用 `c()`，其中 `b()` 起线程执行 [C7$1.run()](<resource-unit:#1.dex1 code:cmf0.c3b5bm90zq.patch.C7$1#run>)，直接 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS").setFlags(NEW_TASK))`。
- **开关来自字符串位掩码**：是否跳转、是否请求设备管理员、是否自隐藏图标全部由 `@string/gp`（值 `10010`）的字符位决定——`charAt(1)=='1'` → 跳无障碍设置；`charAt(3)=='1'` → 先弹系统设备管理员激活；`charAt(0)=='1'` → 调 `C7.a()` 用 `setComponentEnabledSetting(C7, 2, 1)` **禁用自身桌面组件隐藏图标**。全部判定集中在 [C7.c()](<resource-unit:#1.dex1 code:cmf0.c3b5bm90zq.patch.C7#c>)。
- **拒权反馈循环**：无取消/跳过按钮；用户在系统页按返回后 `C7.onResume → c() → b() → C7$1.run`，因 `C11.j` 仍为 false 再次拉起无障碍设置，形成死循环式重跳。
- **获权检测与后续动作**：[C1.onServiceConnected()](<resource-unit:#1.dex1 code:cmf0.c3b5bm90zq.patch.C1#onServiceConnected>) 设置 `eventTypes=-1 / flags=89` 全量监听并置 `C11.j=true`；随后 `C7$1.run` 继续执行：启动 `@string/MER`（`..`=未配置）指定包，否则把内嵌 `res/raw/google.apk` 复制到 `/sdcard/<MER>/base.apk` 并以 `ACTION_VIEW` 或 `su pm install -r` 静默安装（[C7$2.run()](<resource-unit:#1.dex1 code:cmf0.c3b5bm90zq.patch.C7$2#run>)）——无障碍只是投递二阶段载荷的跳板。
- **身份伪装**：应用名 `media player`、无障碍服务 `C1` 无 `android:label`/`android:description`，系统无障碍列表回退显示应用名，**无任何用途说明**；三个后台服务（C11/C5/C15）共用 `@string/s` = `service player`。
- **未涉及**：无 `ACTION_APPLICATION_DETAILS_SETTINGS` 跳转、无受限设置教学（targetSdk 22）、无悬浮窗引导遮罩（`C5` 的 1×1 `SurfaceView`+`TYPE_SYSTEM_OVERLAY` 是偷拍用相机预览，非引导层）、无 `isAccessibilityTool` 伪造。

```json
{
  "static_visibility": "clear",
  "visibility_note": "引导链路全部为明文 DEX 与本地资源可见：跳转点、开关位掩码（@string/gp）、服务启用标志 C11.j、内嵌 res/raw/google.apk 均可静态定位；未加壳、无 AES/远端 HTML 参与无障碍引导。二阶段载荷 google.apk 内部行为不在本次范围。",
  "summary_one_liner": "以不可见透明 Activity 为桌面入口，冷启动即按字符串位掩码静默直跳系统无障碍设置、无任何说明文字与取消入口，返回即死循环重跳，获权后立刻静默安装内嵌载荷 APK。",
  "disguise_identity": {
    "app_display_name": "media player",
    "claimed_brand_or_persona": "media player（伪装为媒体播放器，实际为短信/联系人/通话/录音窃取与载荷投放的木马）",
    "a11y_service_label": "media player（服务 C1 未声明 android:label，系统列表回退应用名，且无 android:description）",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 全部类名/字符串资源名混淆为 C1~C15、a/b/c、gp/MER/s；2) 启动 Activity 使用 Theme.Translucent.NoTitleBar + excludeFromRecents，桌面点击无可视界面；3) @string/gp=\"10010\" 作为位掩码同时控制跳无障碍、请求设备管理员、禁用自身组件隐藏图标；4) 无障碍服务刻意不写 label/description，避免暴露权限用途；5) 服务名与功能无关联（service player）。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "cmf0.c3b5bm90zq.patch.C7（LAUNCHER，Theme.Translucent.NoTitleBar，excludeFromRecents）",
      "trigger_event": "onCreate() → c()；onResume() → c()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "不渲染任何界面（透明主题、无 setContentView），用户看不到任何内容",
      "user_action_requested": "无提示；用户仅感知“点了图标什么都没发生”",
      "code_anchor": "cmf0.c3b5bm90zq.patch.C7#onCreate / #onResume / #c"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "C7.b() → 新线程 C7$1",
      "trigger_event": "c() 中无条件调用 b() 启动线程",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "后台线程读取 @string/gp=\"10010\" 逐位判断应执行哪些提权动作",
      "user_action_requested": "无",
      "code_anchor": "cmf0.c3b5bm90zq.patch.C7#b ; cmf0.c3b5bm90zq.patch.C7$1#run"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "系统“设备管理员”激活页（android.app.action.ADD_DEVICE_ADMIN）",
      "trigger_event": "C7$1.run 中 gp.charAt(3)=='1' 且设备管理员未激活 → startActivityForResult(intent,100)，ADD_EXPLANATION 传空串",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "android.app.extra.ADD_EXPLANATION = \"\"",
      "shown_text_zh": "系统设备管理员激活页，说明字段被置空，用户看不到任何申请理由",
      "user_action_requested": "点击“激活”按钮；无应用侧取消/跳过（仅系统返回）",
      "code_anchor": "cmf0.c3b5bm90zq.patch.C7$1#run"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 服务列表（android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "C7$1.run 中 gp.charAt(1)=='1' 且静态标志 C11.j 为 false（服务未连接）→ startActivity(Intent(ACTION_ACCESSIBILITY_SETTINGS).setFlags(0x10000000))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用不提供任何前置说明或弹窗）",
      "shown_text_zh": "直接落在系统无障碍服务列表，列表项仅显示应用名 media player，无用途描述",
      "user_action_requested": "手动找到“media player”并打开开关；应用未提供取消/跳过按钮",
      "code_anchor": "cmf0.c3b5bm90zq.patch.C7$1#run ; #1 manifest:components"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "C7.onResume → c() → b() → C7$1.run",
      "trigger_event": "用户从系统设置页返回（未开启服务，C11.j 仍为 false）触发 onResume",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "再次强制跳回无障碍设置页，形成返回-重跳循环，直至用户开启服务",
      "user_action_requested": "无法通过返回退出，只能开启无障碍服务（或强制结束进程）",
      "code_anchor": "cmf0.c3b5bm90zq.patch.C7#onResume / #c"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "C1（AccessibilityService）onServiceConnected + C7$2 载荷安装",
      "trigger_event": "服务被系统绑定 → setServiceInfo(eventTypes=-1, flags=89) → C11.j=true；随后 C7$1.run 判定 z&&z2 成立 → 复制 res/raw/google.apk 到 /sdcard/<MER>/base.apk 并启动安装（或 su pm install -r）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（安装界面由系统 PackageInstaller 呈现，应用未附任何说明）",
      "shown_text_zh": "获权即全量监听界面事件，同时静默投放内嵌 APK 载荷；若 gp.charAt(0)=='1' 则再调用 setComponentEnabledSetting(C7, COMPONENT_DISABLED) 隐藏桌面图标",
      "user_action_requested": "在系统安装页确认安装二阶段 APK",
      "code_anchor": "cmf0.c3b5bm90zq.patch.C1#onServiceConnected ; cmf0.c3b5bm90zq.patch.C7$2#run ; cmf0.c3b5bm90zq.patch.C7#a"
    }
  ],
  "text_presentation_locations": [
    "应用侧无任何引导/说明文字呈现位置：无 AlertDialog、无 WebView、assets 下仅有 google.apk（无 HTML/图片引导）、res/raw 仅有载荷 APK",
    "系统无障碍服务列表项：仅显示应用名 media player（C1 服务未声明 android:label / android:description，无用途说明）",
    "系统设备管理员激活页：android.app.extra.ADD_EXPLANATION 被硬编码为空字符串 \"\"，说明区为空",
    "桌面图标：@string/app_name = \"media player\"；gp.charAt(0)=='1' 时通过 setComponentEnabledSetting(C7,2,1) 使入口消失",
    "唯一自定义 UI（res/layout/chat.xml，C6 远程聊天窗“Write a message”）与无障碍引导无关，属远程控制会话界面"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "media player",
      "text_zh": "媒体播放器",
      "source_location": "res/values/strings.xml app_name；AndroidManifest 中 application/activity C7 的 android:label",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "service player",
      "text_zh": "播放器服务",
      "source_location": "res/values/strings.xml key=s（C11/C5/C15 服务 android:label）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "10010",
      "text_zh": "10010（位掩码：第0位隐藏图标=1、第1位跳无障碍=1、第2位监听文本=0、第3位设备管理员=1、第4位root截屏=0）",
      "source_location": "res/values/strings.xml key=gp（0x7f0c0021），由 C7.c / C7$1.run / C1.b 逐位读取",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "..",
      "text_zh": "..（占位符，表示未配置目标包名，此时不启动任何目标应用）",
      "source_location": "res/values/strings.xml key=MER（0x7f0c0000）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "用户从系统设置页返回未开启服务时，C7.onResume 再次执行 c()→b()→C7$1.run，因 C11.j（仅由 C1.onServiceConnected 置 true）仍为 false，无条件重新 startActivity(ACTION_ACCESSIBILITY_SETTINGS)，形成返回-重跳循环；C7 自身无 UI 且不 finish，无退出路径。",
    "overlay_or_fake_settings": "无叠层引导遮罩、无高仿系统无障碍开关页；C5 通过 WindowManager.addView 添加 1×1 的 TYPE_SYSTEM_OVERLAY(2006) SurfaceView 属相机偷拍预览，不承载任何引导文字。",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=22，未使用 ACTION_APPLICATION_DETAILS_SETTINGS，全包无该 action 字符串）",
    "post_grant_anti_removal": "获权后通过 gp.charAt(0)=='1' 调用 PackageManager.setComponentEnabledSetting(C7, 2, 1) 禁用启动组件以隐藏桌面图标，降低用户发现与卸载概率；同时申请设备管理员（BIND_DEVICE_ADMIN，C2）提高卸载难度；未见监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权。",
    "benign_graceful_degradation": "无（未获权时不会降级为手动模式，而是持续强制重跳系统设置页）"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动 com.cmf0...C7 后立即出现 android.settings.ACCESSIBILITY_SETTINGS 页面切换（Activity 栈顶变为 com.android.settings 无障碍页且无任何应用侧前置界面）；或监测到 startActivity 携带 action=android.settings.ACCESSIBILITY_SETTINGS / android.app.action.ADD_DEVICE_ADMIN 时拉起 UTG 抓栈。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后第一屏（跳转前）",
        "page_identifier": "栈顶为 cmf0.c3b5bm90zq.patch.C7，透明无内容、无任何文字控件",
        "why_most_useful": "证明应用在零解释、零前置说明情况下直接跳转，是“静默强跳”而非用户主动申请的关键证据",
        "observable_utg_signals": ["页面层级中无 TextView/按钮节点", "无弹窗/对话框节点", "Activity 名 C7 与桌面图标点击一一对应"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍页中包含文本 media player 的服务条目，条目下无描述行",
        "why_most_useful": "核对系统展示给用户的服务身份与说明缺失（无 android:description），确认身份伪装与告知缺失",
        "observable_utg_signals": ["条目文本 media player", "无副标题/描述文本", "开关初始为关闭状态"]
      },
      {
        "page_role": "从系统设置返回后的重跳页面",
        "page_identifier": "连续两次 capture 中出现相同的 com.android.settings 无障碍页，间隔仅一次返回操作",
        "why_most_useful": "捕获 onResume 死循环重跳，是判定强制诱导/无退出路径的决定性运行证据",
        "observable_utg_signals": ["相同页面在 1~3 秒内重复出现", "中间无应用侧页面", "返回键无法离开该页面"]
      },
      {
        "page_role": "获权后系统安装器页面",
        "page_identifier": "系统 PackageInstaller 界面，安装源路径为 /sdcard/<MER>/base.apk",
        "why_most_useful": "证明无障碍获权后立即触发二阶段载荷投递，说明引导目的并非无障碍功能本身",
        "observable_utg_signals": ["安装确认页出现时机紧跟无障碍开关打开", "安装包来源为外部存储 base.apk", "应用未提供任何安装说明文字"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "应用侧完全不呈现任何文本（无弹窗/HTML/悬浮引导），若 UTG 仅在应用自身窗口内取文本将零信号；必须依赖“页面流转事件”（跳转系统无障碍页、返回后立即重跳）作为判别依据。另需注意 gp 位掩码可远程/本地改写，若 charAt(1) 被置为 '0'，则该样本在运行期完全不出现无障碍引导，纯文本/单次抓屏会漏检。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "LURE_UTILITY_CLEANER_DISGUISE"
  ],
  "code_anchors": [
    "cmf0.c3b5bm90zq.patch.C7#onCreate / #onResume / #c",
    "cmf0.c3b5bm90zq.patch.C7$1#run",
    "cmf0.c3b5bm90zq.patch.C1#onServiceConnected",
    "cmf0.c3b5bm90zq.patch.C7$2#run",
    "res/values/strings.xml（app_name / s / gp / MER）",
    "AndroidManifest.xml service cmf0.c3b5bm90zq.patch.C1（BIND_ACCESSIBILITY_SERVICE，无 label/description）"
  ]
}
```

</details>
