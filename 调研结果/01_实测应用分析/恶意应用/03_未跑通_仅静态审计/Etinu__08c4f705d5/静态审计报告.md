# MR_078__08c4f705d5｜Etinu — Keyboard Wallpaper

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：159.6s

## 1. 一句话核心结论

- **核心申请方式**：该应用并未申请或引导开启无障碍权限：仅有一个首次启动的 Start 按钮加隐私政策文本的引导页，点 Start 后进入 Keyboard/Wallpaper 页签浏览页并加载 MoPub 插屏广告，包内无无障碍服务、无 ACTION_ACCESSIBILITY_SETTINGS 跳转、无遮罩或假设置页
- **静态可见性说明**：全部 DEX 逻辑静态可读；仅类名混淆与字符串 AES/CBC 常量加密，密钥与 IV 硬编码为 pbpGvOQnXZVOGKsD（p06b6b360#maa960f88），已离线全部还原，未发现远端下发、二阶段载荷或加壳；Manifest 与代码中均无任何无障碍服务声明或无障碍设置跳转，故无障碍引导结论为静态可证实的不存在

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `08c4f705d5a7c9dc7c05edee3fcad12f345a6ee6832d54b758e57394292ba651` |
| 包名 / 年份 | `com.studio.keypaper2021` / 2021 |
| 家族 / 品类 | **Etinu**（同池样本数：4） |
| 原始来源标识 | https://www.mcafee.com/blogs/other-blogs/mcafee-labs/clever-billing-fraud-applications-on-google-play-etinu/ |
| 桌面显示名 | Keyboard Wallpaper |
| 引导页宣称品牌/身份 | Keyboard Wallpaper（真实名称，未冒充品牌） |
| 系统无障碍列表服务名 | 无（Manifest 中不存在任何 BIND_ACCESSIBILITY_SERVICE 服务，系统无障碍列表不会出现本应用条目） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无身份混淆技巧；仅存在常规代码混淆（包名混淆为 p2002e610.p588368a5.p84796801.*、类名混淆为 p19de3d12/p8ed94dc5）与字符串 AES 常量加密（p06b6b360#maa960f88，密钥硬编码），以及 Manifest 中大量随机名 meta-data 干扰项，不涉及空白/换行挤出警告、同形字、多 activity-alias 或伪造 isAccessibilityTool |
| 无障碍服务类名 | `二阶段/嵌包或无直接声明` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `无` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | p2002e610.p588368a5.p84796801.p2ecabb75.p19de3d12（LAUNCHER Activity，同时声明 app://com.studio.keypaper2021 深链） | onCreate → i()；读取 SharedPreferences 中 app_first_launch | 原生Activity | **原文**：Keyboard Wallpaper（app_name）/ 按钮与文本由 layout 绑定，按钮标识 btn_start、文本标识 tv_privacy_policy（均为运行期解密所得视图键名）<br>**译注**：应用名“Keyboard Wallpaper”；首次启动展示开始按钮与隐私政策文本 | 点击 Start 按钮继续；无系统权限弹窗、无无障碍申请 | `p2002e610.p588368a5.p84796801.p2ecabb75.p19de3d12#i` |
| 2 | 引导说明页 | 同一 Activity 内的 tv_privacy_policy 文本项（点击回调 p19de3d12$pbdda8066） | 用户点击隐私政策文本 | 原生Activity | **原文**：tv_privacy_policy<br>**译注**：隐私政策入口文本（良性说明性质，非恐吓或假更新） | 可选点击查看隐私政策，不影响继续使用 | `p2002e610.p588368a5.p84796801.p2ecabb75.p19de3d12#i` |
| 3 | 业务功能触发 | p2002e610.p588368a5.p84796801.p2ecabb75.p8ed94dc5（ViewPager2 + TabLayout 主浏览页） | Start 点击后 p19de3d12$p0bb1ec1e#onClick 将 app_first_launch 置 false 并调用 p19de3d12#m() 以显式 ComponentName 启动该 Activity；非首次启动时冷启动直接经 m() 进入 | 原生Activity | **原文**：Keyboard / Wallpaper（页签标题，运行期 AES 解密后设置）<br>**译注**：“键盘”“壁纸”两个页签 | 浏览键盘与壁纸素材，无任何权限申请步骤 | `p2002e610.p588368a5.p84796801.p2ecabb75.p8ed94dc5#i` |
| 4 | 获权后动作 | MoPub 插屏广告（com.mopub.mobileads.MoPubInterstitial，ad unit 4216e45946e54a3baa7492d9cdc9629d） | p8ed94dc5#j() 中 MoPub.initializeSdk 回调后 load()；p19de3d12#i() 中 MoPub.initializeSdk | 原生Activity | **原文**：无（广告素材由远端广告位下发，包内无固定文案）<br>**译注**：进入主页后加载并展示插屏广告 | 无；广告展示与无障碍权限无关联 | `p2002e610.p588368a5.p84796801.p2ecabb75.p8ed94dc5#j` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 首次启动 Activity p19de3d12 内的 btn_start 按钮与 tv_privacy_policy 文本（原生布局，非 Dialog，可跳过——非首次启动直接进入主页）
- 主页 p8ed94dc5 的 TabLayout 页签文本 Keyboard / Wallpaper（运行期 AES 解密后写入）
- res/values/strings.xml 中 app_name = Keyboard Wallpaper（桌面显示名）
- 不存在：assets 下无任何 HTML（**/*.html 检索为空），无 WebView 教学页、无悬浮窗遮罩、无系统无障碍 description 文案、无无障碍设置页跳转后叠层指引

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Keyboard Wallpaper | 键盘壁纸 | `res/values/strings.xml key=app_name（运行期亦由 p06b6b360#maa960f88 解密出 Keyboard / Wallpaper 作为页签标题）` | 良性透明说明 |
| en | btn_start | 开始按钮（视图键名，界面呈现为开始/进入按钮） | `p2002e610.p588368a5.p84796801.p2ecabb75.p19de3d12#i 中 findViewById(pf3702ff2.f881c889a) 经 p06b6b360#maa960f88 解密` | 良性透明说明 |
| en | tv_privacy_policy | 隐私政策文本项 | `p2002e610.p588368a5.p84796801.p2ecabb75.p19de3d12#i 中 findViewById(pf3702ff2.fe8147a19) 经 p06b6b360#maa960f88 解密` | 良性透明说明 |
| en | app_first_launch | 首次启动标记（SharedPreferences 键，控制是否显示引导按钮） | `p2002e610.p588368a5.p84796801.p2ecabb75.p19de3d12#i / p19de3d12$p0bb1ec1e#onClick，经 p06b6b360#maa960f88 解密` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无。该应用不申请无障碍权限，因此不存在拒绝后的重跳循环；首次启动的引导页在点击 Start 后即写入 app_first_launch=false，后续冷启动直接进入主页，属良性降级/跳过逻辑
- **遮罩叠层 / 高仿系统设置页**：无。代码中无 SYSTEM_ALERT_WINDOW 权限申请，无全屏或半透明遮罩 Activity，也无高仿系统无障碍开关页（无任何自定义 a11y 开关 UI 布局）
- **Android 13+ 受限设置（Restricted Settings）应对**：无。全文检索 'allow restricted settings'、'special app access' 均无命中；APPLICATION_DETAILS_SETTINGS 跳转仅存在于 Facebook SDK（i.f.b.c.d.l.v#b），不承载受限设置教学文案
- **获权后即时行为与防撤权机制**：无。未声明无障碍服务，不存在获权后自点确认、GLOBAL_ACTION_BACK/HOME 阻止撤权或监听设置页的行为
- **良性降级 / 替代方案**：有：引导页可被跳过（非首次启动直接进入主页），且未申请任何无障碍权限，键盘/壁纸功能不依赖无障碍授权

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：无需以无障碍跳转为触发点——本包不存在 ACCESSIBILITY_SETTINGS 跳转。若需核验该样本运行期形态，应在冷启动首次拉起 p19de3d12（LAUNCHER）时即开始录制，观察 btn_start 引导页与随后进入的 Keyboard/Wallpaper 页签主页，并对 MoPub 插屏展示时刻补截一帧
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：本样本不涉及无障碍诱导，主要盲区在广告素材与远端广告位配置（MoPub ad unit 4216e45946e54a3baa7492d9cdc9629d 的素材由服务端下发，包内无固定文案，纯 UTG 文本可能为空）；另类名混淆与字符串 AES 常量加密不影响运行期 UTG 观测

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导页（Start 按钮 + 隐私政策文本）** | p2002e610.p588368a5.p84796801.p2ecabb75.p19de3d12，标题栏显示 Keyboard Wallpaper，含一个主按钮与一行文本链 | 这是该样本唯一的用户引导界面，可直接确认其引导诉求是“进入内容”而非“开无障碍” | 页面内不存在系统无障碍开关控件或 'Accessibility' 字样；仅一个主按钮 + 一行隐私政策文本，无恐吓/假更新文案；点击主按钮后直接进入内容页而非系统设置 |
| **主浏览页（Keyboard / Wallpaper 页签）** | p2002e610.p588368a5.p84796801.p2ecabb75.p8ed94dc5，TabLayout 两页签 + ViewPager2 | 确认获“引导”后落点是素材浏览与广告，而非无障碍授权后动作 | 页签文本为 Keyboard 与 Wallpaper；无悬浮窗叠层、无假设置页；进入后出现 MoPub 插屏广告 |
| **系统无障碍服务列表项（预期缺失项）** | 系统设置 → 无障碍 → 已下载的服务列表 | 反向核验：列表内不应出现 com.studio.keypaper2021 条目，可实证否定无障碍诱导路径 | 列表中无 Keyboard Wallpaper 条目；本应用从未跳转该页面 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `p2002e610.p588368a5.p84796801.p2ecabb75.p19de3d12#i`
- `p2002e610.p588368a5.p84796801.p2ecabb75.p19de3d12#m`
- `p2002e610.p588368a5.p84796801.p2ecabb75.p19de3d12$p0bb1ec1e#onClick`
- `p2002e610.p588368a5.p84796801.p2ecabb75.p8ed94dc5#i`
- `p06b6b360#maa960f88`
- `i.c.a.e.d0#<init>`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 核验结论（无障碍引导视角）

- **Manifest 层无任何无障碍服务**：全量声明中没有 `android.permission.BIND_ACCESSIBILITY_SERVICE`，也没有 `android.accessibilityservice.AccessibilityService` 的 `<service>` 声明；`android:description` 形式的无障碍说明同样不存在。对完整 Manifest 转储执行 grep `ccessibilit`，结果为零命中。
- **代码中不存在跳转到无障碍设置的动作**：`#1.dex1` 全文检索 `ACCESSIBILITY_SETTINGS`、`Settings.ACTION_ACCESSIBILITY`、`AccessibilityServiceInfo`、`allow restricted settings` 均为 `no_matches`。唯一出现的 `ACCESSIBILITY` 相关系统设置 Intent 是 [i.f.b.c.d.l.v#b()](<resource-unit:#1.dex1 code:i.f.b.c.d.l.v#b>)，它构造的是 `android.settings.APPLICATION_DETAILS_SETTINGS`，调用方只有 Facebook SDK 内部的 `i.f.b.c.d.d.a`，用于应用详情页跳转，并非无障碍引导，且没有与之配套的“受限设置”教学文案。
- **“SpeechToTextAccessibilityService”只是设备指纹采集时用的匹配标记**：[i.c.a.e.d0#<init>](<resource-unit:#1.dex1 code:i.c.a.e.d0#<init>>) 读取 `Settings.Secure.enabled_accessibility_services`，用 `AccessibilityMenuService`、`SelectToSpeechService`、`SoundAmplifierService`、`SpeechToTextAccessibilityService`、`SwitchAccessService` 等字符串做 `contains()` 判断，再按位写入统计字段 `v`。这是统计 SDK 的设备画像，并非本应用申请或开启无障碍，也没有任何提示界面。
- **实际的运行期引导流程是“启动页 + 广告”**：桌面入口 [p2002e610.p588368a5.p84796801.p2ecabb75.p19de3d12](<resource-unit:#1.dex1 code:p2002e610.p588368a5.p84796801.p2ecabb75.p19de3d12>) 在 [i()](<resource-unit:#1.dex1 code:p2002e610.p588368a5.p84796801.p2ecabb75.p19de3d12#i>) 中绑定 `btn_start` 按钮与 `tv_privacy_policy` 文本；仅当 SharedPreferences 中 `app_first_launch` 为 `true` 时才显示这两者，否则直接经 [m()](<resource-unit:#1.dex1 code:p2002e610.p588368a5.p84796801.p2ecabb75.p19de3d12#m>) 跳到主浏览页。点击 Start 时，[p19de3d12$p0bb1ec1e#onClick](<resource-unit:#1.dex1 code:p2002e610.p588368a5.p84796801.p2ecabb75.p19de3d12$p0bb1ec1e#onClick>) 把 `app_first_launch` 置为 `false` 后调用 `m()`；主页面 [p8ed94dc5#i](<resource-unit:#1.dex1 code:p2002e610.p588368a5.p84796801.p2ecabb75.p8ed94dc5#i>) 用 ViewPager2+TabLayout 承载 “Keyboard / Wallpaper” 两个页签，随后初始化 MoPub 插屏广告（硬编码 ad unit `4216e45946e54a3baa7492d9cdc9629d`）。
- **字符串以 AES 静态加密但密钥硬编码**：[p06b6b360#maa960f88](<resource-unit:#1.dex1 code:p06b6b360#maa960f88>) 使用 `AES/CBC/PKCS5Padding`，密钥和 IV 均为 `pbpGvOQnXZVOGKsD`；我离线还原了全部关键常量（`btn_start`、`tv_privacy_policy`、`app_first_launch`、`Keyboard`、`Wallpaper`、`callback`、广告位 ID），**不存在运行时远端下发或二阶段载荷**。
- **可见性判定**：`static_visibility = clear`。虽然类名被混淆，并且字符串常量采用 AES 加密，但密钥在包内、逻辑完整可还原，因此无障碍相关结论“不存在”是静态可证实的，不需要 UTG 补证。
- 覆盖边界：无障碍引导专题在包内**不成立**；包内其他可疑能力（自定义输入法 `p18e10fd7.p11037c49`、`enabled_accessibility_services` 指纹采集、MoPub 插屏广告）不在本轮专题结论范围内，未展开定性。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部 DEX 逻辑静态可读；仅类名混淆与字符串 AES/CBC 常量加密，密钥与 IV 硬编码为 pbpGvOQnXZVOGKsD（p06b6b360#maa960f88），已离线全部还原，未发现远端下发、二阶段载荷或加壳；Manifest 与代码中均无任何无障碍服务声明或无障碍设置跳转，故无障碍引导结论为静态可证实的不存在",
  "summary_one_liner": "该应用并未申请或引导开启无障碍权限：仅有一个首次启动的 Start 按钮加隐私政策文本的引导页，点 Start 后进入 Keyboard/Wallpaper 页签浏览页并加载 MoPub 插屏广告，包内无无障碍服务、无 ACTION_ACCESSIBILITY_SETTINGS 跳转、无遮罩或假设置页",
  "disguise_identity": {
    "app_display_name": "Keyboard Wallpaper",
    "claimed_brand_or_persona": "Keyboard Wallpaper（真实名称，未冒充品牌）",
    "a11y_service_label": "无（Manifest 中不存在任何 BIND_ACCESSIBILITY_SERVICE 服务，系统无障碍列表不会出现本应用条目）",
    "identity_mismatch": false,
    "obfuscation_tricks": "无身份混淆技巧；仅存在常规代码混淆（包名混淆为 p2002e610.p588368a5.p84796801.*、类名混淆为 p19de3d12/p8ed94dc5）与字符串 AES 常量加密（p06b6b360#maa960f88，密钥硬编码），以及 Manifest 中大量随机名 meta-data 干扰项，不涉及空白/换行挤出警告、同形字、多 activity-alias 或伪造 isAccessibilityTool"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "p2002e610.p588368a5.p84796801.p2ecabb75.p19de3d12（LAUNCHER Activity，同时声明 app://com.studio.keypaper2021 深链）",
      "trigger_event": "onCreate → i()；读取 SharedPreferences 中 app_first_launch",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Keyboard Wallpaper（app_name）/ 按钮与文本由 layout 绑定，按钮标识 btn_start、文本标识 tv_privacy_policy（均为运行期解密所得视图键名）",
      "shown_text_zh": "应用名“Keyboard Wallpaper”；首次启动展示开始按钮与隐私政策文本",
      "user_action_requested": "点击 Start 按钮继续；无系统权限弹窗、无无障碍申请",
      "code_anchor": "p2002e610.p588368a5.p84796801.p2ecabb75.p19de3d12#i"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "同一 Activity 内的 tv_privacy_policy 文本项（点击回调 p19de3d12$pbdda8066）",
      "trigger_event": "用户点击隐私政策文本",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "tv_privacy_policy",
      "shown_text_zh": "隐私政策入口文本（良性说明性质，非恐吓或假更新）",
      "user_action_requested": "可选点击查看隐私政策，不影响继续使用",
      "code_anchor": "p2002e610.p588368a5.p84796801.p2ecabb75.p19de3d12#i"
    },
    {
      "step": 3,
      "stage": "业务功能触发",
      "screen_or_component": "p2002e610.p588368a5.p84796801.p2ecabb75.p8ed94dc5（ViewPager2 + TabLayout 主浏览页）",
      "trigger_event": "Start 点击后 p19de3d12$p0bb1ec1e#onClick 将 app_first_launch 置 false 并调用 p19de3d12#m() 以显式 ComponentName 启动该 Activity；非首次启动时冷启动直接经 m() 进入",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Keyboard / Wallpaper（页签标题，运行期 AES 解密后设置）",
      "shown_text_zh": "“键盘”“壁纸”两个页签",
      "user_action_requested": "浏览键盘与壁纸素材，无任何权限申请步骤",
      "code_anchor": "p2002e610.p588368a5.p84796801.p2ecabb75.p8ed94dc5#i"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "MoPub 插屏广告（com.mopub.mobileads.MoPubInterstitial，ad unit 4216e45946e54a3baa7492d9cdc9629d）",
      "trigger_event": "p8ed94dc5#j() 中 MoPub.initializeSdk 回调后 load()；p19de3d12#i() 中 MoPub.initializeSdk",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（广告素材由远端广告位下发，包内无固定文案）",
      "shown_text_zh": "进入主页后加载并展示插屏广告",
      "user_action_requested": "无；广告展示与无障碍权限无关联",
      "code_anchor": "p2002e610.p588368a5.p84796801.p2ecabb75.p8ed94dc5#j"
    }
  ],
  "text_presentation_locations": [
    "首次启动 Activity p19de3d12 内的 btn_start 按钮与 tv_privacy_policy 文本（原生布局，非 Dialog，可跳过——非首次启动直接进入主页）",
    "主页 p8ed94dc5 的 TabLayout 页签文本 Keyboard / Wallpaper（运行期 AES 解密后写入）",
    "res/values/strings.xml 中 app_name = Keyboard Wallpaper（桌面显示名）",
    "不存在：assets 下无任何 HTML（**/*.html 检索为空），无 WebView 教学页、无悬浮窗遮罩、无系统无障碍 description 文案、无无障碍设置页跳转后叠层指引"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Keyboard Wallpaper",
      "text_zh": "键盘壁纸",
      "source_location": "res/values/strings.xml key=app_name（运行期亦由 p06b6b360#maa960f88 解密出 Keyboard / Wallpaper 作为页签标题）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "btn_start",
      "text_zh": "开始按钮（视图键名，界面呈现为开始/进入按钮）",
      "source_location": "p2002e610.p588368a5.p84796801.p2ecabb75.p19de3d12#i 中 findViewById(pf3702ff2.f881c889a) 经 p06b6b360#maa960f88 解密",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "tv_privacy_policy",
      "text_zh": "隐私政策文本项",
      "source_location": "p2002e610.p588368a5.p84796801.p2ecabb75.p19de3d12#i 中 findViewById(pf3702ff2.fe8147a19) 经 p06b6b360#maa960f88 解密",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "app_first_launch",
      "text_zh": "首次启动标记（SharedPreferences 键，控制是否显示引导按钮）",
      "source_location": "p2002e610.p588368a5.p84796801.p2ecabb75.p19de3d12#i / p19de3d12$p0bb1ec1e#onClick，经 p06b6b360#maa960f88 解密",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无。该应用不申请无障碍权限，因此不存在拒绝后的重跳循环；首次启动的引导页在点击 Start 后即写入 app_first_launch=false，后续冷启动直接进入主页，属良性降级/跳过逻辑",
    "overlay_or_fake_settings": "无。代码中无 SYSTEM_ALERT_WINDOW 权限申请，无全屏或半透明遮罩 Activity，也无高仿系统无障碍开关页（无任何自定义 a11y 开关 UI 布局）",
    "restricted_settings_13plus_coaching": "无。全文检索 'allow restricted settings'、'special app access' 均无命中；APPLICATION_DETAILS_SETTINGS 跳转仅存在于 Facebook SDK（i.f.b.c.d.l.v#b），不承载受限设置教学文案",
    "post_grant_anti_removal": "无。未声明无障碍服务，不存在获权后自点确认、GLOBAL_ACTION_BACK/HOME 阻止撤权或监听设置页的行为",
    "benign_graceful_degradation": "有：引导页可被跳过（非首次启动直接进入主页），且未申请任何无障碍权限，键盘/壁纸功能不依赖无障碍授权"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "无需以无障碍跳转为触发点——本包不存在 ACCESSIBILITY_SETTINGS 跳转。若需核验该样本运行期形态，应在冷启动首次拉起 p19de3d12（LAUNCHER）时即开始录制，观察 btn_start 引导页与随后进入的 Keyboard/Wallpaper 页签主页，并对 MoPub 插屏展示时刻补截一帧",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导页（Start 按钮 + 隐私政策文本）",
        "page_identifier": "p2002e610.p588368a5.p84796801.p2ecabb75.p19de3d12，标题栏显示 Keyboard Wallpaper，含一个主按钮与一行文本链",
        "why_most_useful": "这是该样本唯一的用户引导界面，可直接确认其引导诉求是“进入内容”而非“开无障碍”",
        "observable_utg_signals": ["页面内不存在系统无障碍开关控件或 'Accessibility' 字样", "仅一个主按钮 + 一行隐私政策文本，无恐吓/假更新文案", "点击主按钮后直接进入内容页而非系统设置"]
      },
      {
        "page_role": "主浏览页（Keyboard / Wallpaper 页签）",
        "page_identifier": "p2002e610.p588368a5.p84796801.p2ecabb75.p8ed94dc5，TabLayout 两页签 + ViewPager2",
        "why_most_useful": "确认获“引导”后落点是素材浏览与广告，而非无障碍授权后动作",
        "observable_utg_signals": ["页签文本为 Keyboard 与 Wallpaper", "无悬浮窗叠层、无假设置页", "进入后出现 MoPub 插屏广告"]
      },
      {
        "page_role": "系统无障碍服务列表项（预期缺失项）",
        "page_identifier": "系统设置 → 无障碍 → 已下载的服务列表",
        "why_most_useful": "反向核验：列表内不应出现 com.studio.keypaper2021 条目，可实证否定无障碍诱导路径",
        "observable_utg_signals": ["列表中无 Keyboard Wallpaper 条目", "本应用从未跳转该页面"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "本样本不涉及无障碍诱导，主要盲区在广告素材与远端广告位配置（MoPub ad unit 4216e45946e54a3baa7492d9cdc9629d 的素材由服务端下发，包内无固定文案，纯 UTG 文本可能为空）；另类名混淆与字符串 AES 常量加密不影响运行期 UTG 观测"
  },
  "behavior_pattern_tags": [],
  "code_anchors": [
    "p2002e610.p588368a5.p84796801.p2ecabb75.p19de3d12#i",
    "p2002e610.p588368a5.p84796801.p2ecabb75.p19de3d12#m",
    "p2002e610.p588368a5.p84796801.p2ecabb75.p19de3d12$p0bb1ec1e#onClick",
    "p2002e610.p588368a5.p84796801.p2ecabb75.p8ed94dc5#i",
    "p06b6b360#maa960f88",
    "i.c.a.e.d0#<init>"
  ]
}
```

</details>
