# MB_016__545fb5d571｜Crocodilus — Chrome

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：152.8s

## 1. 一句话核心结论

- **核心申请方式**：以 "Chrome" 为名的两阶段 Dropper：外层把内嵌的 sizing.catsup.thriving APK 写入 cache 并安装拉起，内层再以同样冒名 "Chrome" 的无障碍服务（可读取窗口内容、可执行手势）获取无障碍权限；具体引导页面藏于加密 dex，静态不可见。
- **静态可见性说明**：外层 APK（stinky.massive）的 Manifest 与 classes.dex 明文可见，但只是 3 个类的安装器 Dropper；真正的无障碍业务位于内嵌 assets/SvhpjVWZH.apk（sizing.catsup.thriving），其 classes.dex 同样只含安装器，核心逻辑在 assets/classes1.dex、assets/classes2.dex（无 dex 魔数、首块熵约1.6、加密）以及 ZIP 加密条目 dvook.png 中；外层 assets/classes1-9.enc 亦为加密载荷。因此引导弹窗、说明页、跳转无障碍设置的代码与文案均不可静态还原，仅 Manifest 声明、服务名、无障碍配置属性与 Dropper 行为可见。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `545fb5d571cab5d861d1259d4c31cd292795189aee79041821c9d9221c570e9c` |
| 包名 / 年份 | `stinky.massive` / 2025 |
| 家族 / 品类 | **Crocodilus**（同池样本数：6） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Chrome |
| 引导页宣称品牌/身份 | Google Chrome（冒充） |
| 系统无障碍列表服务名 | Chrome（android:label="Chrome"，服务类 sizing.catsup.thriving.eWmumTIktlkbl.QcFhDbuhroJFiB） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名 stinky.massive / sizing.catsup.thriving 与 Chrome 毫无关系；多 activity-alias 伪装（sizing.catsup.thriving.StandUpAlias，enabled=false、icon=@drawable/bfqstlpws、label=Chrome、targetActivity=nvSdeTFYxKzo，可在运行期切换图标与入口）；Activity label 使用占位符 ==AppName==；application theme=Theme.Translucent.NoTitleBar 且 launcher Activity 为 NoDisplay，桌面无可见界面；核心 dex 以 .enc 与伪 dex（无 dex 魔数、低熵）加密，ZIP 内 dvook.png 采用密码加密条目抗静态提取 |
| 无障碍服务类名 | `二阶段/嵌包或无直接声明` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `QUERY_ALL_PACKAGES, REQUEST_INSTALL_PACKAGES` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | stinky.massive.NWqrdTFTiwRe（外层唯一 Activity，Theme 无标题透明） | 用户点击桌面 "Chrome" 图标触发 onCreate | 原生Activity | 无 | 仅需点击桌面图标；无任何取消或跳过选项 | `stinky.massive.NWqrdTFTiwRe#onCreate / #b` |
| 2 | 冷启动入口 | cacheDir 中的 SvhpjVWZH.apk 安装流程 + 内层包拉起 | onCreate 中 b() 解包 assets/SvhpjVWZH.apk 到 cacheDir，随后 c(file, pkg) 安装、a() 调 getLaunchIntentForPackage + startActivity | 原生Activity | 无 | 若系统弹出安装确认，用户需允许安装来源不明的内层 APK；外层自身不提供取消 | `stinky.massive.NWqrdTFTiwRe#onCreate / #b / #c / #a` |
| 3 | 引导说明页 | 内层 sizing.catsup.thriving 启动入口（nvSdeTFYxKzo / GprNYLKvls 或 alias StandUpAlias） | 内层被 startActivity 拉起后进入其主界面（具体分支逻辑不可静态还原） | 不可静态还原 | **原文**：无（代码位于加密的 assets/classes1.dex、assets/classes2.dex）<br>**译注**：无法静态取得；从家族行为推断为冒名 Chrome 的更新/安全类说明页，但本样本未取得可引用原文 | 不可静态确认 | `assets/SvhpjVWZH.apk → AndroidManifest.xml（activity nvSdeTFYxKzo / GprNYLKvls / alias StandUpAlias）` |
| 4 | 跳无障碍设置 | 系统设置 → 无障碍 → 已安装服务（目标项显示名 Chrome） | 不可静态还原的 Intent 跳转（代码在加密 dex 中；内层已具备 ACCESSIBILITY_SETTINGS 所需的全部声明） | 系统无障碍页 | **原文**：Chrome<br>**译注**：无障碍服务列表中出现一项名为 "Chrome" 的服务，与真实 Google Chrome 无法在列表中区分 | 用户需在系统无障碍列表中手动开启该服务并确认授权弹窗 | `assets/SvhpjVWZH.apk → AndroidManifest.xml: service sizing.catsup.thriving.eWmumTIktlkbl.QcFhDbuhroJFiB / res/xml/yngxsft.xml` |
| 5 | 获权后动作 | sizing.catsup.thriving.eWmumTIktlkbl.QcFhDbuhroJFiB（AccessibilityService，canRetrieveWindowContent=true、canPerformGestures=true） | 服务被系统绑定后开始接收无障碍事件 | 不可静态还原 | 无 | 无（用户已完成授权） | `assets/SvhpjVWZH.apk → res/xml/yngxsft.xml；receiver sizing.catsup.thriving.oeusiUpMlxQd.pJdLbJtNjxpq（BIND_DEVICE_ADMIN）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 桌面/启动器图标名称：AndroidManifest.xml 中 application android:label="Chrome"（外层 stinky.massive 与内层 sizing.catsup.thriving 均为 Chrome）
- 系统无障碍服务列表项：内层 service sizing.catsup.thriving.eWmumTIktlkbl.QcFhDbuhroJFiB 的 android:label="Chrome"
- 系统应用信息/权限页：Activity label 占位符 ==AppName==（sizing.catsup.thriving.oeusiUpMlxQd.cnYjxppCVL，Theme.Translucent.NoTitleBar），以及 activity-alias StandUpAlias 的 label="Chrome"、icon=@drawable/bfqstlpws
- 引导弹窗/说明页文本：无静态可读来源——内层 resources.arsc 未发现任何自定义引导字符串，外层 assets/*.js 均为加密二进制，内层 assets/classes1.dex、classes2.dex 为加密伪 dex，dvook.png 为 ZIP 加密条目；此类文案只能在运行期 UTG/截屏取得

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Chrome | Chrome（谷歌浏览器） | `外层与内层 AndroidManifest.xml application/@android:label；无障碍 service QcFhDbuhroJFiB/@android:label；activity-alias StandUpAlias/@android:label` | 假更新 |
| en | ==AppName== | 未替换的占位符，说明该 Activity 标题本应由运行期或远端填充品牌名 | `内层 AndroidManifest.xml: activity sizing.catsup.thriving.oeusiUpMlxQd.cnYjxppCVL/@android:label` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原（内层引导与重试逻辑在加密 dex 中）；但外层已确认声明 BOOT_COMPLETED、USER_PRESENT、SCREEN_OFF、MY_PACKAGE_REPLACED、PACKAGE_ADDED 广播接收器（sizing.catsup.thriving.uNQDQRFBIaiBPw.AicSXtjrggzso），具备开机/亮屏/包变更后重新拉起引导的持续施压条件。
- **遮罩叠层 / 高仿系统设置页**：不可静态确认是否存在半透明遮罩或高仿设置页；但无障碍配置 res/xml/yngxsft.xml 同时开启 canRetrieveWindowContent 与 canPerformGestures，具备在系统设置页之上叠加遮罩并代替用户点击开关的能力基础。
- **Android 13+ 受限设置（Restricted Settings）应对**：静态线索 restricted=['SESSION_INSTALLER'] 指向内层使用 PackageInstaller Session 方式完成安装，与本样本外层「解包到 cacheDir 后安装内层 APK」的路径一致；是否再教用户进入应用详情允许「受限设置」的文案无法静态还原。
- **获权后即时行为与防撤权机制**：未取得静态确认；但内层已声明 BIND_DEVICE_ADMIN 设备管理器接收器（sizing.catsup.thriving.oeusiUpMlxQd.pJdLbJtNjxpq）与前台服务、媒体投影等，通常用于增加卸载与撤权阻力。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以「内层包 sizing.catsup.thriving 安装完成并被 startActivity 拉起」为首要钩子，并在其后 0~3 秒内监测任意 intent 指向 android.settings.ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 的时刻立即抓取；外层 stinky.massive 的冷启动瞬间（Theme.Translucent.NoTitleBar、无 UI）只用于确认 Dropper 阶段，不适合作为诱导证据页。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在明显盲区：(1) 本样本为两阶段 Dropper，若只在安装后监测被启动的包，会漏掉外层安装器阶段，需按包名链 stinky.massive → sizing.catsup.thriving 跟踪；(2) 内层核心逻辑与全部引导文案位于加密的 assets/classes1.dex、classes2.dex 及 ZIP 加密条目 dvook.png，外层 assets/*.js 亦为加密二进制，静态无法给出文案，必须依赖运行期 UTG/截屏；(3) 引导页可能以纯图或 WebView 远端页面呈现（当前无本地 HTML 资源，若远端下发则文本为空，需配合 OCR 与网络流量）。注意静态加壳本身不阻挡运行期 UTG 取证。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **外层 Dropper 静默安装阶段（确认二阶段结构）** | 前台应用 stinky.massive，屏幕无可见界面（透明/NoDisplay Activity），随后系统安装器或 PackageInstaller 会话出现 | 区分「一阶段安装器」与「二阶段诱导器」，避免把安装弹窗误判为诱导弹窗 | 前台包名 stinky.massive 且无任何可见节点文本；随后出现系统安装确认或 Session 安装进度；紧接着前台包名切换为 sizing.catsup.thriving |
| **内层冒名 Chrome 的引导说明页（最关键的诱导页）** | 前台包名 sizing.catsup.thriving，界面标题/正文含 Chrome 或更新、安全类措辞，且无明确关闭按钮 | 这是唯一能把「冒名身份」与「要求开启无障碍」直接关联起来的页面，静态完全不可见 | 界面文本含 Chrome / 更新 / 安全 等字样；存在指向设置的按钮节点文本；是否存在返回键失效或弹窗无取消按钮 |
| **跳转后的系统无障碍服务列表项** | 系统设置包 com.android.settings，列表中出现名为 Chrome 的无障碍服务项 | 验证用户被引导的落点确实是本应用服务，且服务显示名与真实 Chrome 无法区分 | 设置页无障碍列表项文本为 Chrome；该项对应服务摘要/应用信息指向 sizing.catsup.thriving；开关初始状态为关闭 |
| **获权后叠加遮罩/自动操作阶段** | 系统设置页之上出现非系统绘制的覆盖层，或开关被自动打开后自动返回 | 判断是否存在代点开关、GLOBAL_ACTION_BACK 强制返回等反撤权与代授权行为 | 设置页上方出现悬浮窗层级的节点；开关状态在无用户输入情况下变化；授权后界面立即被返回或跳走 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `stinky.massive.NWqrdTFTiwRe#onCreate`
- `stinky.massive.NWqrdTFTiwRe#b`
- `stinky.massive.NWqrdTFTiwRe#a`
- `assets/SvhpjVWZH.apk!AndroidManifest.xml: service sizing.catsup.thriving.eWmumTIktlkbl.QcFhDbuhroJFiB`
- `assets/SvhpjVWZH.apk!res/xml/yngxsft.xml`
- `assets/classes1.dex / assets/classes2.dex（加密载荷，不可静态还原）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点

**两阶段 Dropper 结构（已静态确认）**

- 外层包 `stinky.massive`（显示名 `Chrome`）的 `classes.dex` 只有 3 个类，不包含任何无障碍相关代码。其唯一实质行为是[NWqrdTFTiwRe#onCreate](<resource-unit:#1.dex1 code:stinky.massive.NWqrdTFTiwRe#onCreate>)：调用 `b()` 把 `assets/SvhpjVWZH.apk` 写入 `cacheDir`，再通过 `getPackageArchiveInfo` 读取包名、调用 `c(file, pkg)` 安装，然后用 `a()` 调用 `getLaunchIntentForPackage` 和 `startActivity` 拉起内层。
- 内层 [assets/SvhpjVWZH.apk](<resource-unit:<local_path> file:all>) 的真实包名为 `sizing.catsup.thriving`，同样声明 `android:label="Chrome"`，并**确实声明了无障碍服务** `sizing.catsup.thriving.eWmumTIktlkbl.QcFhDbuhroJFiB`（`label="Chrome"`、`permission=BIND_ACCESSIBILITY_SERVICE`、`meta-data @xml/yngxsft`）。该服务的配置包含 `canRetrieveWindowContent` 与 `canPerformGestures`，也就是能读取窗口内容并执行手势。
- **引导流程本体不可静态还原**：内层 `classes.dex`（24KB）不含任何 `accessibility`、`Settings`、`WebView` 字符串；真正业务代码在 `assets/classes1.dex`、`assets/classes2.dex` 中，这两个文件没有 `dex` 魔数、首块熵约 1.6（加密或伪装），另外 `dvook.png` 是 ZIP 加密条目；外层 `assets/classes1-9.enc` 同样是加密载荷。因此，冷启动后“弹窗、说明页、跳设置”的具体文案与跳转点均无法静态取得。
- 伪装细节：包名与 Chrome 完全无关；存在 `activity-alias` `sizing.catsup.thriving.StandUpAlias`（`enabled=false`、`icon=@drawable/bfqstlpws`、`label="Chrome"`），用于更换图标或名称；还有一个 Activity 的 label 使用占位符 `==AppName==`；同时声明 `BIND_DEVICE_ADMIN` 设备管理器、`BOOT_COMPLETED`、`USER_PRESENT`、`PACKAGE_ADDED` 接收器，具备后台重拉与增加卸载阻力的能力。

**UTG 视角的取舍**：纯运行期检测应把钩子挂在“内层包安装完成并被 `startActivity` 拉起”以及“任何指向 `ACCESSIBILITY_SETTINGS` 的 Intent”这两个瞬间，因为此时才进入真正的引导界面；外层 `Theme.Translucent.NoTitleBar` 没有可见 UI，冷启动瞬间抓不到诱导文本。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "外层 APK（stinky.massive）的 Manifest 与 classes.dex 明文可见，但只是 3 个类的安装器 Dropper；真正的无障碍业务位于内嵌 assets/SvhpjVWZH.apk（sizing.catsup.thriving），其 classes.dex 同样只含安装器，核心逻辑在 assets/classes1.dex、assets/classes2.dex（无 dex 魔数、首块熵约1.6、加密）以及 ZIP 加密条目 dvook.png 中；外层 assets/classes1-9.enc 亦为加密载荷。因此引导弹窗、说明页、跳转无障碍设置的代码与文案均不可静态还原，仅 Manifest 声明、服务名、无障碍配置属性与 Dropper 行为可见。",
  "summary_one_liner": "以 \"Chrome\" 为名的两阶段 Dropper：外层把内嵌的 sizing.catsup.thriving APK 写入 cache 并安装拉起，内层再以同样冒名 \"Chrome\" 的无障碍服务（可读取窗口内容、可执行手势）获取无障碍权限；具体引导页面藏于加密 dex，静态不可见。",
  "disguise_identity": {
    "app_display_name": "Chrome",
    "claimed_brand_or_persona": "Google Chrome（冒充）",
    "a11y_service_label": "Chrome（android:label=\"Chrome\"，服务类 sizing.catsup.thriving.eWmumTIktlkbl.QcFhDbuhroJFiB）",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名 stinky.massive / sizing.catsup.thriving 与 Chrome 毫无关系；多 activity-alias 伪装（sizing.catsup.thriving.StandUpAlias，enabled=false、icon=@drawable/bfqstlpws、label=Chrome、targetActivity=nvSdeTFYxKzo，可在运行期切换图标与入口）；Activity label 使用占位符 ==AppName==；application theme=Theme.Translucent.NoTitleBar 且 launcher Activity 为 NoDisplay，桌面无可见界面；核心 dex 以 .enc 与伪 dex（无 dex 魔数、低熵）加密，ZIP 内 dvook.png 采用密码加密条目抗静态提取"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "stinky.massive.NWqrdTFTiwRe（外层唯一 Activity，Theme 无标题透明）",
      "trigger_event": "用户点击桌面 \"Chrome\" 图标触发 onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无可见界面，静默执行",
      "user_action_requested": "仅需点击桌面图标；无任何取消或跳过选项",
      "code_anchor": "stinky.massive.NWqrdTFTiwRe#onCreate / #b"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "cacheDir 中的 SvhpjVWZH.apk 安装流程 + 内层包拉起",
      "trigger_event": "onCreate 中 b() 解包 assets/SvhpjVWZH.apk 到 cacheDir，随后 c(file, pkg) 安装、a() 调 getLaunchIntentForPackage + startActivity",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "先读取内嵌包名并尝试 getPackageInfo 判断是否已安装，未安装则写入 cacheDir 并安装，再直接拉起内层 sizing.catsup.thriving 的启动入口，外层 finish()",
      "user_action_requested": "若系统弹出安装确认，用户需允许安装来源不明的内层 APK；外层自身不提供取消",
      "code_anchor": "stinky.massive.NWqrdTFTiwRe#onCreate / #b / #c / #a"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "内层 sizing.catsup.thriving 启动入口（nvSdeTFYxKzo / GprNYLKvls 或 alias StandUpAlias）",
      "trigger_event": "内层被 startActivity 拉起后进入其主界面（具体分支逻辑不可静态还原）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（代码位于加密的 assets/classes1.dex、assets/classes2.dex）",
      "shown_text_zh": "无法静态取得；从家族行为推断为冒名 Chrome 的更新/安全类说明页，但本样本未取得可引用原文",
      "user_action_requested": "不可静态确认",
      "code_anchor": "assets/SvhpjVWZH.apk → AndroidManifest.xml（activity nvSdeTFYxKzo / GprNYLKvls / alias StandUpAlias）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已安装服务（目标项显示名 Chrome）",
      "trigger_event": "不可静态还原的 Intent 跳转（代码在加密 dex 中；内层已具备 ACCESSIBILITY_SETTINGS 所需的全部声明）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Chrome",
      "shown_text_zh": "无障碍服务列表中出现一项名为 \"Chrome\" 的服务，与真实 Google Chrome 无法在列表中区分",
      "user_action_requested": "用户需在系统无障碍列表中手动开启该服务并确认授权弹窗",
      "code_anchor": "assets/SvhpjVWZH.apk → AndroidManifest.xml: service sizing.catsup.thriving.eWmumTIktlkbl.QcFhDbuhroJFiB / res/xml/yngxsft.xml"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "sizing.catsup.thriving.eWmumTIktlkbl.QcFhDbuhroJFiB（AccessibilityService，canRetrieveWindowContent=true、canPerformGestures=true）",
      "trigger_event": "服务被系统绑定后开始接收无障碍事件",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务侧行为代码位于加密 dex，无法静态确认其读取/点击/转账操作细节；同时存在 BIND_DEVICE_ADMIN 设备管理器与 SMS 读写、媒体投影（mediaProjection）等配套能力",
      "user_action_requested": "无（用户已完成授权）",
      "code_anchor": "assets/SvhpjVWZH.apk → res/xml/yngxsft.xml；receiver sizing.catsup.thriving.oeusiUpMlxQd.pJdLbJtNjxpq（BIND_DEVICE_ADMIN）"
    }
  ],
  "text_presentation_locations": [
    "桌面/启动器图标名称：AndroidManifest.xml 中 application android:label=\"Chrome\"（外层 stinky.massive 与内层 sizing.catsup.thriving 均为 Chrome）",
    "系统无障碍服务列表项：内层 service sizing.catsup.thriving.eWmumTIktlkbl.QcFhDbuhroJFiB 的 android:label=\"Chrome\"",
    "系统应用信息/权限页：Activity label 占位符 ==AppName==（sizing.catsup.thriving.oeusiUpMlxQd.cnYjxppCVL，Theme.Translucent.NoTitleBar），以及 activity-alias StandUpAlias 的 label=\"Chrome\"、icon=@drawable/bfqstlpws",
    "引导弹窗/说明页文本：无静态可读来源——内层 resources.arsc 未发现任何自定义引导字符串，外层 assets/*.js 均为加密二进制，内层 assets/classes1.dex、classes2.dex 为加密伪 dex，dvook.png 为 ZIP 加密条目；此类文案只能在运行期 UTG/截屏取得"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Chrome",
      "text_zh": "Chrome（谷歌浏览器）",
      "source_location": "外层与内层 AndroidManifest.xml application/@android:label；无障碍 service QcFhDbuhroJFiB/@android:label；activity-alias StandUpAlias/@android:label",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "==AppName==",
      "text_zh": "未替换的占位符，说明该 Activity 标题本应由运行期或远端填充品牌名",
      "source_location": "内层 AndroidManifest.xml: activity sizing.catsup.thriving.oeusiUpMlxQd.cnYjxppCVL/@android:label",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原（内层引导与重试逻辑在加密 dex 中）；但外层已确认声明 BOOT_COMPLETED、USER_PRESENT、SCREEN_OFF、MY_PACKAGE_REPLACED、PACKAGE_ADDED 广播接收器（sizing.catsup.thriving.uNQDQRFBIaiBPw.AicSXtjrggzso），具备开机/亮屏/包变更后重新拉起引导的持续施压条件。",
    "overlay_or_fake_settings": "不可静态确认是否存在半透明遮罩或高仿设置页；但无障碍配置 res/xml/yngxsft.xml 同时开启 canRetrieveWindowContent 与 canPerformGestures，具备在系统设置页之上叠加遮罩并代替用户点击开关的能力基础。",
    "restricted_settings_13plus_coaching": "静态线索 restricted=['SESSION_INSTALLER'] 指向内层使用 PackageInstaller Session 方式完成安装，与本样本外层「解包到 cacheDir 后安装内层 APK」的路径一致；是否再教用户进入应用详情允许「受限设置」的文案无法静态还原。",
    "post_grant_anti_removal": "未取得静态确认；但内层已声明 BIND_DEVICE_ADMIN 设备管理器接收器（sizing.catsup.thriving.oeusiUpMlxQd.pJdLbJtNjxpq）与前台服务、媒体投影等，通常用于增加卸载与撤权阻力。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以「内层包 sizing.catsup.thriving 安装完成并被 startActivity 拉起」为首要钩子，并在其后 0~3 秒内监测任意 intent 指向 android.settings.ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 的时刻立即抓取；外层 stinky.massive 的冷启动瞬间（Theme.Translucent.NoTitleBar、无 UI）只用于确认 Dropper 阶段，不适合作为诱导证据页。",
    "key_pages_to_capture": [
      {
        "page_role": "外层 Dropper 静默安装阶段（确认二阶段结构）",
        "page_identifier": "前台应用 stinky.massive，屏幕无可见界面（透明/NoDisplay Activity），随后系统安装器或 PackageInstaller 会话出现",
        "why_most_useful": "区分「一阶段安装器」与「二阶段诱导器」，避免把安装弹窗误判为诱导弹窗",
        "observable_utg_signals": ["前台包名 stinky.massive 且无任何可见节点文本", "随后出现系统安装确认或 Session 安装进度", "紧接着前台包名切换为 sizing.catsup.thriving"]
      },
      {
        "page_role": "内层冒名 Chrome 的引导说明页（最关键的诱导页）",
        "page_identifier": "前台包名 sizing.catsup.thriving，界面标题/正文含 Chrome 或更新、安全类措辞，且无明确关闭按钮",
        "why_most_useful": "这是唯一能把「冒名身份」与「要求开启无障碍」直接关联起来的页面，静态完全不可见",
        "observable_utg_signals": ["界面文本含 Chrome / 更新 / 安全 等字样", "存在指向设置的按钮节点文本", "是否存在返回键失效或弹窗无取消按钮"]
      },
      {
        "page_role": "跳转后的系统无障碍服务列表项",
        "page_identifier": "系统设置包 com.android.settings，列表中出现名为 Chrome 的无障碍服务项",
        "why_most_useful": "验证用户被引导的落点确实是本应用服务，且服务显示名与真实 Chrome 无法区分",
        "observable_utg_signals": ["设置页无障碍列表项文本为 Chrome", "该项对应服务摘要/应用信息指向 sizing.catsup.thriving", "开关初始状态为关闭"]
      },
      {
        "page_role": "获权后叠加遮罩/自动操作阶段",
        "page_identifier": "系统设置页之上出现非系统绘制的覆盖层，或开关被自动打开后自动返回",
        "why_most_useful": "判断是否存在代点开关、GLOBAL_ACTION_BACK 强制返回等反撤权与代授权行为",
        "observable_utg_signals": ["设置页上方出现悬浮窗层级的节点", "开关状态在无用户输入情况下变化", "授权后界面立即被返回或跳走"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在明显盲区：(1) 本样本为两阶段 Dropper，若只在安装后监测被启动的包，会漏掉外层安装器阶段，需按包名链 stinky.massive → sizing.catsup.thriving 跟踪；(2) 内层核心逻辑与全部引导文案位于加密的 assets/classes1.dex、classes2.dex 及 ZIP 加密条目 dvook.png，外层 assets/*.js 亦为加密二进制，静态无法给出文案，必须依赖运行期 UTG/截屏；(3) 引导页可能以纯图或 WebView 远端页面呈现（当前无本地 HTML 资源，若远端下发则文本为空，需配合 OCR 与网络流量）。注意静态加壳本身不阻挡运行期 UTG 取证。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "stinky.massive.NWqrdTFTiwRe#onCreate",
    "stinky.massive.NWqrdTFTiwRe#b",
    "stinky.massive.NWqrdTFTiwRe#a",
    "assets/SvhpjVWZH.apk!AndroidManifest.xml: service sizing.catsup.thriving.eWmumTIktlkbl.QcFhDbuhroJFiB",
    "assets/SvhpjVWZH.apk!res/xml/yngxsft.xml",
    "assets/classes1.dex / assets/classes2.dex（加密载荷，不可静态还原）"
  ]
}
```

**覆盖边界说明**：内层引导页文案、跳转 Intent 构造与拒权循环逻辑均位于加密 dex 与加密 ZIP 条目内，本轮未做脱壳还原，因此 `step_by_step_flow` 的第 3、5 步与 `how_user_is_guided_to_enable` 中多项字段标注为不可静态确认，需以运行期 UTG/截屏补充；已确认部分（两阶段 Dropper、冒名 Chrome 的无障碍服务声明、服务能力配置、多别名伪装）均有 Manifest 与 dex 直接证据。

</details>
