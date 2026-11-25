# MR_049__fe1e6cff49｜Wotby — Settings

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：85.8s

## 1. 一句话核心结论

- **核心申请方式**：冒充 com.android.settings 系统设置的加壳样本，无障碍引导与诱导文案全部藏在运行期解密并通过 BaseDexClassLoader 注入的二阶段 dex 中，静态无法还原其引导流程。
- **静态可见性说明**：一阶段 DEX 仅含 Loader（com.sek.dap.a~e），用 Base64 常量+MD5 解密 / .err8.log 并经 BaseDexClassLoader/pathList 反射注入 / .e9.jar、/ .e9.dex，再反射调用 com.sek.apps.AppsDataApplication.initData()；该类不在包内，所有无障碍诱导弹窗/Activity/WebView 文案与触发逻辑均位于该运行期解密载荷，静态不可还原。Manifest、资源与 AOSP Settings 框架代码完整可见。
- **命中的行为模式标签**：`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `fe1e6cff49e218e2eab8f96ef92817f217127fbf21d4a010092597986874b2ed` |
| 包名 / 年份 | `com.android.settings` / 2020 |
| 家族 / 品类 | **Wotby**（同池样本数：1） |
| 原始来源标识 | https://blog.malwarebytes.com/android/2020/07/we-found-yet-another-phone-with-pre-installed-malware-via-the-lifeline-assistance-program/ |
| 桌面显示名 | Settings |
| 引导页宣称品牌/身份 | Android 系统「设置」（com.android.settings，sharedUserId=android.uid.system，coreApp=true，versionName 7.1.1） |
| 系统无障碍列表服务名 | 无（Manifest 未声明任何 AccessibilityService，运行期是否注册由二阶段载荷决定） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：①包名/图标/标签/theme 全量复用系统设置，activity-alias 名为 Settings 抢占 LAUNCHER 与 android.settings.SETTINGS；②声明 sharedUserId=android.uid.system、coreApp=true、original-package、requiredForAllUsers，伪装系统级特权应用；③Application 类替换为 com.sek.dap.Apps（非 AOSP 类）作为加载入口；④载荷类名单字母混淆（com.sek.dap.a~e）；⑤加密资产伪装成 assets/ti.ttf、assets/wiz.txt 与 /.err8.log、small.ttf；⑥dex/jar 落地后反射注入 BaseDexClassLoader |
| 无障碍服务类名 | `二阶段/嵌包或无直接声明` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, PACKAGE_USAGE_STATS, READ_CONTACTS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.sek.dap.Apps（Application）→ com.sek.dap.a 解密落盘 → Class.forName("com.sek.apps.AppsDataApplication").initData(Context) | Application.onCreate() 进程启动即执行 | 不可静态还原 | **原文**：无（该阶段无任何界面，仅 Log.e("Test", "--ERR3 AppsDataApplication: ~111/222") 调试日志）<br>**译注**：启动阶段不呈现任何界面文字，仅完成解密与二阶段类加载 | 无 | `com.sek.dap.Apps.onCreate / com.sek.dap.Apps.init / com.sek.dap.a.a(Context)` |
| 2 | 获权后动作 | 二阶段载荷 com.sek.apps.AppsDataApplication（未包含于包内 DEX） | initData() 被反射调用后由二阶段自行注册 Activity/服务并展示引导 | 不可静态还原 | **原文**：无（静态不可达）<br>**译注**：无法静态确认；诱导弹窗、跳转 ACTION_ACCESSIBILITY_SETTINGS 的时机与文案均在解密载荷内 | 无法静态确认（是否有取消/跳过按钮不可知） | `com.sek.apps.AppsDataApplication.initData(Context)（仅字符串引用，类体缺失）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 静态可确认：无任何无障碍引导文案载体——Manifest 未声明 AccessibilityService，故不存在系统无障碍列表中的 android:description 说明文字
- 静态可确认：包内 resources.arsc/strings 中的 accessibility_* 字符串与 res/xml/accessibility_settings*.xml、res/layout/enable_accessibility_service_dialog_content.xml 均属被搬运的 AOSP Settings 原生设置界面，非本样本自定义诱导页
- 疑似（不可静态确认）：二阶段解密 dex 内的自定义 Activity/Dialog/WebView/悬浮窗，以及跳转 ACTION_ACCESSIBILITY_SETTINGS 前的说明页，全部位于 /.e9.jar、/.e9.dex 运行期载荷

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Settings | 设置 | `resources.arsc @7F0E027F（application/android:label，被 activity-alias Settings 复用）` | 未知 |
| en | Pairing grants access to your contacts and call history when connected. | 配对连接后即授予对您的联系人和通话记录的访问权限。 | `resources.arsc（AOSP Settings 蓝牙配对提示原始字符串，非诱导文案）` | 良性透明说明 |
| en | This speech synthesis engine may be able to collect all the text that will be spoken, including personal data like passwords and credit card | 该语音合成引擎可能收集所有将被朗读的文本，包括密码和信用卡等个人数据。 | `resources.arsc（AOSP Settings TTS 引擎隐私提示原始字符串，非诱导文案）` | 良性透明说明 |
| en | Enable developer options | 启用开发者选项 | `resources.arsc（AOSP Settings 原始字符串）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：静态不可确认；引导逻辑在二阶段解密载荷 com.sek.apps.AppsDataApplication 内，需运行期观测 onResume 是否重跳无障碍设置
- **遮罩叠层 / 高仿系统设置页**：静态不可确认；无静态悬浮窗/遮罩布局证据，二阶段是否叠层未知
- **Android 13+ 受限设置（Restricted Settings）应对**：静态不可确认；包内无 SESSION_INSTALLER 静态实现，教学逻辑若存在只能位于二阶段载荷
- **获权后即时行为与防撤权机制**：静态不可确认；预筛 WATCH_SETTINGS 线索的实现在二阶段载荷内
- **良性降级 / 替代方案**：无（本样本为伪装系统设置的加壳恶意样本，未见任何降级路径）

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动冒充的 Settings 图标后立即开始 UTG 采样；重点挂钩两类瞬间：①应用自身 Activity 获得焦点且界面元素与 AOSP 设置不一致时；②监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 的跳转前 1~2 帧
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：一阶段为纯 Loader（com.sek.dap.a~e），诱导无障碍的弹窗、WebView、遮罩与文案全部位于运行期解密并经 BaseDexClassLoader 注入的 /.e9.dex、/.e9.jar，纯静态分析完全不可达；此外包内 assets/ti.ttf、assets/wiz.txt 与 /.err8.log 为加密资产，静态加载虽不阻挡运行期 UTG，但会阻碍事前文本预筛。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动首屏（伪装系统设置入口）** | 包名 com.android.settings 的 Settings activity-alias 首屏，标题为 Settings 但内容与 AOSP 设置不符或直接弹窗 | 确认是否为一次性冷启动阻塞式引导（TRIG_COLD_START_BLOCK），区分诱导时机 | 首屏是否出现非 AOSP 的权限/无障碍说明弹窗；弹窗是否无取消/返回按钮；首屏 Activity 类名与 com.android.settings.Settings 是否一致 |
| **跳转前说明页/教学页** | 跳转 ACTION_ACCESSIBILITY_SETTINGS 之前压栈的 Activity 或 Dialog | 该页承载诱导文案与身份宣称，是判定伪装身份与话术框架的关键证据 | 文案原文（含空白/换行挤出的超长服务名）；是否存在 WebView 控件；是否有倒计时或不可取消标识 |
| **系统无障碍服务列表项** | 系统 Settings 无障碍列表中新出现的服务条目及其说明文字 | 确认二阶段实际注册的服务名（静态 Manifest 无声明，只能运行期看到） | 服务显示名与描述原文；是否与 com.android.settings 系统项混淆同名；开关是否被自动点击开启 |
| **返回设置页后的遮罩/重跳页** | 从无障碍设置返回应用时立刻出现的悬浮窗或再次弹窗 | 判定拒绝/返回后的循环拉起与叠层引导（COERCE_REFUSAL_LOOP_RELAUNCH / COERCE_OVERLAY_STACK_ON_SETTINGS） | 返回后 500~1000ms 内是否再次跳转无障碍设置；是否存在覆盖系统设置页的半透明层；是否出现 GLOBAL_ACTION_BACK/HOME 导致无法退出 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.sek.dap.Apps.init(Application) —— 反射调用 com.sek.apps.AppsDataApplication.initData(Context)`
- `com.sek.dap.a.a(Context) / com.sek.dap.a.<init>(Context) —— 解密 /.err8.log 与 /.08.log 比对落盘`
- `com.sek.dap.c.<clinit> —— Base64 常量解码出 /.e9.jar,/.e9.dex,dexElements,dalvik.system.BaseDexClassLoader,pathList 注入清单`
- `com.sek.dap.d.a / com.sek.dap.b.a —— MessageDigest 解密与写盘`
- `AndroidManifest.xml: android:name="com.sek.dap.Apps"、sharedUserId="android.uid.system"、activity-alias name="Settings"`
- `assets/ti.ttf、assets/wiz.txt —— 伪装为字体/文本的加密资产`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，14 次工具调用内收口）

**核心事实：本样本对无障碍引导的静态可见性为「不可静态还原」——载荷被加密并延迟加载。**

1. **包名与身份伪装**：Manifest 声明 `package="com.android.settings"`、`sharedUserId="android.uid.system"`、`coreApp="true"`、`original-package`、`versionName 7.1.1`、`targetSdk 25`，桌面入口由 `activity-alias name="Settings"`（MAIN/LAUNCHER）指向 `Settings` Activity，标签复用系统设置字符串 `@7F0E027F`，即完整冒充 Android 系统「设置」。但 `<application android:name="com.sek.dap.Apps">` 并非 AOSP Settings 的 Application 类——真实 AOSP 设置不会有该入口。
2. **无障碍服务声明**：全包**未声明任何 `AccessibilityService`**，无 `BIND_ACCESSIBILITY_SERVICE` 权限、无 `android:description`、无服务标签（与预筛一致）。Manifest 中 32 处 `accessibility` 命中全部是 AOSP Settings 自身的 `Settings$AccessibilitySettingsActivity` 等系统设置页与 `android.support.*` 兼容库，属于被整体搬运的良性框架代码，不是恶意服务。
3. **真实恶意逻辑在运行期解密载荷中**：[com.sek.dap.Apps.onCreate()](<resource-unit:#1.dex1 code:com.sek.dap.Apps#onCreate>) → [init()](<resource-unit:#1.dex1 code:com.sek.dap.Apps#init>) 先调用 [com.sek.dap.a.a(Context)](<resource-unit:#1.dex1 code:com.sek.dap.a#a>) 完成解密落盘，随后 `Class.forName("com.sek.apps.AppsDataApplication").getDeclaredMethod("initData", Context.class).invoke(...)` 反射调用——**该类在 DEX 中不存在**，即一阶段 Loader 只负责拉起二阶段。
4. **加载链细节**：[com.sek.dap.a.<init>()](<resource-unit:#1.dex1 code:com.sek.dap.a#<init>>) 读取 `/.err8.log`（密文）→ 与 `/.08.log` 比对后经 `com.sek.dap.d`（`MessageDigest`）解密 → `com.sek.dap.b.a()` 写入。而 [com.sek.dap.c](<resource-unit:#1.dex1 code:com.sek.dap.c>) 的 `<clinit>`（1667 条指令）内置 Base64 常量，解码后为逗号分隔清单：`/.err8.log,/.e9.jar,/.e9.dex,com.android.content.Context,dexElements,dalvik.system.BaseDexClassLoader,pathList,lib2,libc,/.o.jar,small.ttf` —— 典型的 **jar/dex 落地 + BaseDexClassLoader/pathList 反射注入**（`assets/ti.ttf`、`assets/wiz.txt` 为配套加密资产）。
5. **对本次问题的直接回答**：因诱导无障碍的弹窗/Activity/HTML 文案均在二阶段 `com.sek.apps.AppsDataApplication` 内（未包含于 DEX，需设备侧解密），**无法静态给出逐步引导流程、原文文案与遮罩组件**。可确认的只有：没有任何 `android:description` 型无障碍说明载体，恶意引导不可能依赖系统无障碍列表文案；且本样本无 `SESSION_INSTALLER` 静态实现，13+ 受限设置教学逻辑同样只能存在于二阶段。

**未决与边界**：二阶段明文（`/.e9.dex`、`small.ttf`）依赖运行期解密与设备，纯静态不可达；动态分析未启动（本会话未验证设备在线）。以下 JSON 如实标注 `packed_or_encrypted`，并给出运行期 UTG 抓取建议。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "一阶段 DEX 仅含 Loader（com.sek.dap.a~e），用 Base64 常量+MD5 解密 / .err8.log 并经 BaseDexClassLoader/pathList 反射注入 / .e9.jar、/ .e9.dex，再反射调用 com.sek.apps.AppsDataApplication.initData()；该类不在包内，所有无障碍诱导弹窗/Activity/WebView 文案与触发逻辑均位于该运行期解密载荷，静态不可还原。Manifest、资源与 AOSP Settings 框架代码完整可见。",
  "summary_one_liner": "冒充 com.android.settings 系统设置的加壳样本，无障碍引导与诱导文案全部藏在运行期解密并通过 BaseDexClassLoader 注入的二阶段 dex 中，静态无法还原其引导流程。",
  "disguise_identity": {
    "app_display_name": "Settings",
    "claimed_brand_or_persona": "Android 系统「设置」（com.android.settings，sharedUserId=android.uid.system，coreApp=true，versionName 7.1.1）",
    "a11y_service_label": "无（Manifest 未声明任何 AccessibilityService，运行期是否注册由二阶段载荷决定）",
    "identity_mismatch": true,
    "obfuscation_tricks": "①包名/图标/标签/theme 全量复用系统设置，activity-alias 名为 Settings 抢占 LAUNCHER 与 android.settings.SETTINGS；②声明 sharedUserId=android.uid.system、coreApp=true、original-package、requiredForAllUsers，伪装系统级特权应用；③Application 类替换为 com.sek.dap.Apps（非 AOSP 类）作为加载入口；④载荷类名单字母混淆（com.sek.dap.a~e）；⑤加密资产伪装成 assets/ti.ttf、assets/wiz.txt 与 /.err8.log、small.ttf；⑥dex/jar 落地后反射注入 BaseDexClassLoader"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.sek.dap.Apps（Application）→ com.sek.dap.a 解密落盘 → Class.forName(\"com.sek.apps.AppsDataApplication\").initData(Context)",
      "trigger_event": "Application.onCreate() 进程启动即执行",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（该阶段无任何界面，仅 Log.e(\"Test\", \"--ERR3 AppsDataApplication: ~111/222\") 调试日志）",
      "shown_text_zh": "启动阶段不呈现任何界面文字，仅完成解密与二阶段类加载",
      "user_action_requested": "无",
      "code_anchor": "com.sek.dap.Apps.onCreate / com.sek.dap.Apps.init / com.sek.dap.a.a(Context)"
    },
    {
      "step": 2,
      "stage": "获权后动作",
      "screen_or_component": "二阶段载荷 com.sek.apps.AppsDataApplication（未包含于包内 DEX）",
      "trigger_event": "initData() 被反射调用后由二阶段自行注册 Activity/服务并展示引导",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（静态不可达）",
      "shown_text_zh": "无法静态确认；诱导弹窗、跳转 ACTION_ACCESSIBILITY_SETTINGS 的时机与文案均在解密载荷内",
      "user_action_requested": "无法静态确认（是否有取消/跳过按钮不可知）",
      "code_anchor": "com.sek.apps.AppsDataApplication.initData(Context)（仅字符串引用，类体缺失）"
    }
  ],
  "text_presentation_locations": [
    "静态可确认：无任何无障碍引导文案载体——Manifest 未声明 AccessibilityService，故不存在系统无障碍列表中的 android:description 说明文字",
    "静态可确认：包内 resources.arsc/strings 中的 accessibility_* 字符串与 res/xml/accessibility_settings*.xml、res/layout/enable_accessibility_service_dialog_content.xml 均属被搬运的 AOSP Settings 原生设置界面，非本样本自定义诱导页",
    "疑似（不可静态确认）：二阶段解密 dex 内的自定义 Activity/Dialog/WebView/悬浮窗，以及跳转 ACTION_ACCESSIBILITY_SETTINGS 前的说明页，全部位于 /.e9.jar、/.e9.dex 运行期载荷"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Settings",
      "text_zh": "设置",
      "source_location": "resources.arsc @7F0E027F（application/android:label，被 activity-alias Settings 复用）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Pairing grants access to your contacts and call history when connected.",
      "text_zh": "配对连接后即授予对您的联系人和通话记录的访问权限。",
      "source_location": "resources.arsc（AOSP Settings 蓝牙配对提示原始字符串，非诱导文案）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "This speech synthesis engine may be able to collect all the text that will be spoken, including personal data like passwords and credit card",
      "text_zh": "该语音合成引擎可能收集所有将被朗读的文本，包括密码和信用卡等个人数据。",
      "source_location": "resources.arsc（AOSP Settings TTS 引擎隐私提示原始字符串，非诱导文案）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable developer options",
      "text_zh": "启用开发者选项",
      "source_location": "resources.arsc（AOSP Settings 原始字符串）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "静态不可确认；引导逻辑在二阶段解密载荷 com.sek.apps.AppsDataApplication 内，需运行期观测 onResume 是否重跳无障碍设置",
    "overlay_or_fake_settings": "静态不可确认；无静态悬浮窗/遮罩布局证据，二阶段是否叠层未知",
    "restricted_settings_13plus_coaching": "静态不可确认；包内无 SESSION_INSTALLER 静态实现，教学逻辑若存在只能位于二阶段载荷",
    "post_grant_anti_removal": "静态不可确认；预筛 WATCH_SETTINGS 线索的实现在二阶段载荷内",
    "benign_graceful_degradation": "无（本样本为伪装系统设置的加壳恶意样本，未见任何降级路径）"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动冒充的 Settings 图标后立即开始 UTG 采样；重点挂钩两类瞬间：①应用自身 Activity 获得焦点且界面元素与 AOSP 设置不一致时；②监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 的跳转前 1~2 帧",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动首屏（伪装系统设置入口）",
        "page_identifier": "包名 com.android.settings 的 Settings activity-alias 首屏，标题为 Settings 但内容与 AOSP 设置不符或直接弹窗",
        "why_most_useful": "确认是否为一次性冷启动阻塞式引导（TRIG_COLD_START_BLOCK），区分诱导时机",
        "observable_utg_signals": ["首屏是否出现非 AOSP 的权限/无障碍说明弹窗", "弹窗是否无取消/返回按钮", "首屏 Activity 类名与 com.android.settings.Settings 是否一致"]
      },
      {
        "page_role": "跳转前说明页/教学页",
        "page_identifier": "跳转 ACTION_ACCESSIBILITY_SETTINGS 之前压栈的 Activity 或 Dialog",
        "why_most_useful": "该页承载诱导文案与身份宣称，是判定伪装身份与话术框架的关键证据",
        "observable_utg_signals": ["文案原文（含空白/换行挤出的超长服务名）", "是否存在 WebView 控件", "是否有倒计时或不可取消标识"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统 Settings 无障碍列表中新出现的服务条目及其说明文字",
        "why_most_useful": "确认二阶段实际注册的服务名（静态 Manifest 无声明，只能运行期看到）",
        "observable_utg_signals": ["服务显示名与描述原文", "是否与 com.android.settings 系统项混淆同名", "开关是否被自动点击开启"]
      },
      {
        "page_role": "返回设置页后的遮罩/重跳页",
        "page_identifier": "从无障碍设置返回应用时立刻出现的悬浮窗或再次弹窗",
        "why_most_useful": "判定拒绝/返回后的循环拉起与叠层引导（COERCE_REFUSAL_LOOP_RELAUNCH / COERCE_OVERLAY_STACK_ON_SETTINGS）",
        "observable_utg_signals": ["返回后 500~1000ms 内是否再次跳转无障碍设置", "是否存在覆盖系统设置页的半透明层", "是否出现 GLOBAL_ACTION_BACK/HOME 导致无法退出"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在显著盲区：一阶段为纯 Loader（com.sek.dap.a~e），诱导无障碍的弹窗、WebView、遮罩与文案全部位于运行期解密并经 BaseDexClassLoader 注入的 /.e9.dex、/.e9.jar，纯静态分析完全不可达；此外包内 assets/ti.ttf、assets/wiz.txt 与 /.err8.log 为加密资产，静态加载虽不阻挡运行期 UTG，但会阻碍事前文本预筛。"
  },
  "behavior_pattern_tags": [
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE"
  ],
  "code_anchors": [
    "com.sek.dap.Apps.init(Application) —— 反射调用 com.sek.apps.AppsDataApplication.initData(Context)",
    "com.sek.dap.a.a(Context) / com.sek.dap.a.<init>(Context) —— 解密 /.err8.log 与 /.08.log 比对落盘",
    "com.sek.dap.c.<clinit> —— Base64 常量解码出 /.e9.jar,/.e9.dex,dexElements,dalvik.system.BaseDexClassLoader,pathList 注入清单",
    "com.sek.dap.d.a / com.sek.dap.b.a —— MessageDigest 解密与写盘",
    "AndroidManifest.xml: android:name=\"com.sek.dap.Apps\"、sharedUserId=\"android.uid.system\"、activity-alias name=\"Settings\"",
    "assets/ti.ttf、assets/wiz.txt —— 伪装为字体/文本的加密资产"
  ]
}
```

</details>
