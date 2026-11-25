# MR_115__89f6e2ecfb｜Hqwar — PayLife Kartensicherheit

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：145.1s

## 1. 一句话核心结论

- **核心申请方式**：无障碍服务仅在 Manifest 中以 PayLife 名义声明，实现类与全部引导/跳转逻辑缺失于包内 DEX，由 Application 启动时的字节数组解密与反射装载二阶段载荷后运行期生成。
- **静态可见性说明**：Manifest 完整可见（无障碍服务 com.pagkijxim.tycdlm.KexhDHREsoSY、启动 Activity com.pagkijxim.tycdlm.zxlqunay.zbpMvA 等数十组件），但 classes.dex 中不含任何 com.pagkijxim.* 类，也无 AccessibilityService/onAccessibilityEvent 定义；引导页面、跳转 Intent、提示文案全部由 com.pvbitn.ireurvi.IZTjtACHVQ 的字节数组解密+反射在运行期构造，strings.xml 仅有 actTest 一条、无 assets/HTML，故 UTG 页面流转不可静态还原。
- **命中的行为模式标签**：`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `89f6e2ecfbd60f4edbdcb457313efd824379a9ea316a078995ac1eaf35fef270` |
| 包名 / 年份 | `com.pagkijxim.tycdlm` / 2019 |
| 家族 / 品类 | **Hqwar**（同池样本数：4） |
| 原始来源标识 | https://blog.zimperium.com/how-zimperiums-z9-detected-unknown-mobile-malware-overlooked-by-the-av-industry/ |
| 桌面显示名 | PayLife Kartensicherheit |
| 引导页宣称品牌/身份 | PayLife（银行卡/支付安全工具） |
| 系统无障碍列表服务名 | PayLife |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务未声明 android:description，系统无障碍列表只显示品牌名 PayLife 而无功能说明；十余个引导类 Activity 全部 android:label="" 且共用图标 @drawable/gnovtvwmsveg，多数叠加 excludeFromRecents/singleTask 使入口名不可见；类名与字段名为随机化乱码（SCoGtet、IZTjtACHVQ、KexhDHREsoSY），字符串以交错乱码与字节数组加密双重混淆。 |
| 无障碍服务类名 | `com.pagkijxim.tycdlm.KexhDHREsoSY` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, PACKAGE_USAGE_STATS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.pvbitn.ireurvi.SCoGtet (Application) → com.pagkijxim.tycdlm.zxlqunay.zbpMvA (LAUNCHER Activity，无字节码) | 进程启动时 Application.onCreate() | 不可静态还原 | **原文**：无（strings.xml 仅 pnulgtuvw=actTest）<br>**译注**：静态不可见任何冷启动界面文案 | 不可静态判定 | `com.pvbitn.ireurvi.SCoGtet.onCreate / res/values/strings.xml` |
| 2 | 获权后动作 | 运行期解密与反射装载的二阶段载荷（目标类名不可静态确定） | SCoGtet.onCreate → IZTjtACHVQ.tUsoDabT(Application) 解密 byte[] 字符串并反射取类、实例化 bnvSACy | 不可静态还原 | **原文**：无（解密前为 byte[]{-11,-102,100,-75,105,-44,...} 等字节数组）<br>**译注**：载荷装载阶段的字符串全部加密，明文与界面内容静态不可得 | 不可静态判定 | `com.pvbitn.ireurvi.IZTjtACHVQ.tUsoDabT(android.app.Application) / IZTjtACHVQ.tUsoDabT(byte[])` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：由 Manifest service android:label="PayLife" 提供，无 android:description（配置 meta-data 指向 @xml/mxbawx）
- 桌面图标名称：application android:label="PayLife Kartensicherheit"
- res/values/strings.xml：仅 1 条 pnulgtuvw=actTest，无引导文案
- 包内无 assets/ 目录，故不存在本地 HTML 引导页
- 其余引导文字（弹窗/Activity/WebView/悬浮窗）均无静态载体，须待运行期解密载荷生成

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | PayLife Kartensicherheit | PayLife 银行卡安全 | `AndroidManifest.xml application android:label` | 假反诈安全 |
| en | PayLife | PayLife | `AndroidManifest.xml service com.pagkijxim.tycdlm.KexhDHREsoSY android:label` | 假反诈安全 |
| en | actTest | actTest（疑似残留测试串，非用户可见文案） | `res/values/strings.xml key=pnulgtuvw` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态判定：实现无障碍引导的类未包含在 classes.dex 中，无 onResume/Timer 重跳代码可核验
- **遮罩叠层 / 高仿系统设置页**：不可静态判定：无 SYSTEM_ALERT_WINDOW 使用点可定位（权限已声明），res/layout 无引导布局证据
- **Android 13+ 受限设置（Restricted Settings）应对**：无（未发现 ACTION_APPLICATION_DETAILS_SETTINGS 或受限设置相关字符串，targetSdkVersion=27 亦不涉及 Android 13 受限设置机制）
- **获权后即时行为与防撤权机制**：不可静态判定：无 GLOBAL_ACTION_BACK/HOME 相关代码可核验
- **良性降级 / 替代方案**：无（未见任何降级或替代路径代码）

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以 Application 启动为起点：在 SCoGtet.onCreate 返回后即开始录屏/UTG 采样，并在监测到 Activity 切换到 com.pagkijxim.tycdlm.zxlqunay.* 或系统页 com.android.settings/.Settings$AccessibilitySettings 的瞬间抓取快照；若二阶段载荷为远端下发，需配合网络 Hook 在下载完成后立即开启 UTG。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：包内不含无障碍服务与启动 Activity 的字节码，引导文案与跳转逻辑全部由运行期字节数组解密+反射生成（一阶段 Dropper 结构），纯静态 UTG 规则无法预判页面文本与跳转时机；若二阶段载荷经远端下发且采用图片化引导，则需 OCR 辅助。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后首个可见界面（启动 Activity zxlqunay.zbpMvA 或二阶段动态创建的 Activity）** | TaskRecord 顶层 Activity 属于 com.pagkijxim.tycdlm 且 label 为空、图标为 @drawable/gnovtvwmsveg | 该类 Activity 无字节码，是唯一能确认载荷是否成功装载并呈现诱导界面的观测点 | 界面是否以 PayLife 品牌出现；是否出现无障碍/安全授权相关按钮文本；是否存在不可取消的弹窗层级（dialog 节点无取消控件） |
| **跳转系统无障碍设置前的引导页** | 当前 Activity 后紧接 com.android.settings AccessibilitySettings 的 Intent 跳转 | 决定诱导方式属原生说明页、WebView 还是悬浮遮罩，是区分诱导形态的关键帧 | 页面根节点为 WebView 还是原生布局；WebView URL 是本地 assets 还是远端域名；是否存在逐步骤教学文本 |
| **系统无障碍服务列表项** | com.android.settings/.accessibility.AccessibilitySettings 中 label=PayLife 的条目 | 核验列表项是否仅有品牌名而无 description，评估用户可获得的真实信息量 | 条目 text 与 contentDescription；是否存在副标题说明（预期缺失） |
| **从设置页返回后的压栈遮罩页** | 从 AccessibilitySettings 返回后 0.5–2 秒内新出现的顶层窗口/悬浮窗 | 判定是否存在拒绝循环重跳或遮罩叠层引导 | 返回后是否立刻再次跳转设置页；是否出现 TYPE_APPLICATION_OVERLAY 类窗口节点；是否出现指向开关位置的引导箭头/高亮 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.pvbitn.ireurvi.SCoGtet.onCreate`
- `com.pvbitn.ireurvi.IZTjtACHVQ.tUsoDabT(android.app.Application)`
- `com.pvbitn.ireurvi.IZTjtACHVQ.tUsoDabT(byte[])`
- `com.pvbitn.ireurvi.IZTjtACHVQ.tUsoDabT()`
- `res/values/strings.xml`
- `AndroidManifest.xml (service com.pagkijxim.tycdlm.KexhDHREsoSY, meta-data @xml/mxbawx)`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，已收口）

**1. 无障碍服务的声明是完整且明确的，但实现代码不存在于包内 DEX**
- Manifest 第 109–114 行声明了无障碍服务 `com.pagkijxim.tycdlm.KexhDHREsoSY`，其 `android:label="PayLife"`、`android:permission="android.permission.BIND_ACCESSIBILITY_SERVICE"`，并带有 `AccessibilityService` 的 intent-filter 与 `meta-data android:accessibilityservice → @xml/mxbawx`。
- 但 `classes.dex` 中**不存在任何 `com.pagkijxim.*` 类**，也不存在 `AccessibilityService`、`onAccessibilityEvent` 的定义。全部 38 个类只分布在 `com.pvbitn.ireurvi.*`（33 个）与 `com.qiyjhshnbpht.*`（5 个）中。声明与实际代码严重脱节。

**2. 跳转点与引导文案无法静态定位**
- 以 `ACCESSIBILITY_SETTINGS`、`APPLICATION_DETAILS_SETTINGS`、`isAccessibilityTool`、`action_settings` 等关键词搜索整个应用的代码与资源，**没有命中任何结果**；以 `Settings` 搜索，也只命中 `android.support.qiyjhshnbpht` 包中的 `Settings$Secure.getString` 调用，这说明该调用是三方库在读取系统设置，而不是在跳转设置页。
- `res/values/strings.xml` 仅有 1 条：`pnulgtuvw = actTest`。包内**没有 `assets/` 目录**，因此不存在本地 HTML 引导页；`res/layout` 下也没有引导布局的证据。界面文案没有静态载体。

**3. 启动链呈现典型的“一阶段装载器”结构**
- 唯一的 Application [SCoGtet.onCreate()](<resource-unit:#1.dex1 code:com.pvbitn.ireurvi.SCoGtet#onCreate>) 会立即调用 [IZTjtACHVQ.tUsoDabT(Application)](<resource-unit:#1.dex1 code:com.pvbitn.ireurvi.IZTjtACHVQ#tUsoDabT(android.app.Application)>)。后者大量使用 `tUsoDabT(byte[])` 解密硬编码字节数组（例如 `{-11,-102,100,-75,...}`），再把解密结果作为 URL 或动作串传入；同时通过 [tUsoDabT()](<resource-unit:#1.dex1 code:com.pvbitn.ireurvi.IZTjtACHVQ#tUsoDabT()>) 通过反射取类，并实例化 `bnvSACy` 执行后续动作。字段初值全是交错乱码串（如 `"cblnpspdrcsoesdeaeopsrof s"`），属于字符串加密与名字混淆。
- 另外，包内存在非标准资源 `unknown/image/fullsize`（233,766 字节）和 `image/picloadlistorderbysizeoffile.prop`，其性质在本次预算内未还原。

**4. 身份伪装线索已确认**
- 桌面名是 `PayLife Kartensicherheit`（“银行卡安全”语义），无障碍列表项标签是 `PayLife`，**并且该 service 没有 `android:description`**。这会导致系统无障碍列表只显示品牌名，而不显示功能说明。
- 十余个 Activity 使用 `android:label=""`，并共用图标 `@drawable/gnovtvwmsveg`，其中多数带有 `excludeFromRecents` 和 `singleTask`。这些 Activity 的入口名称与用途对用户不可见。

**5. 结论边界**
纯运行期 UTG 视角的“逐步骤页面流转”在当前包内**无法静态还原**：无障碍服务实现、启动 Activity `zxlqunay.zbpMvA` 与全部引导 Activity 均无字节码，文案与跳转 Intent 只能在二阶段解密载荷或远端下发后出现。已登记风险 [R-001](<resource-unit:#1 manifest:components>)，定性为运行期解密加载；建议以动态脱壳加 UTG 抓取补齐流转细节。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "Manifest 完整可见（无障碍服务 com.pagkijxim.tycdlm.KexhDHREsoSY、启动 Activity com.pagkijxim.tycdlm.zxlqunay.zbpMvA 等数十组件），但 classes.dex 中不含任何 com.pagkijxim.* 类，也无 AccessibilityService/onAccessibilityEvent 定义；引导页面、跳转 Intent、提示文案全部由 com.pvbitn.ireurvi.IZTjtACHVQ 的字节数组解密+反射在运行期构造，strings.xml 仅有 actTest 一条、无 assets/HTML，故 UTG 页面流转不可静态还原。",
  "summary_one_liner": "无障碍服务仅在 Manifest 中以 PayLife 名义声明，实现类与全部引导/跳转逻辑缺失于包内 DEX，由 Application 启动时的字节数组解密与反射装载二阶段载荷后运行期生成。",
  "disguise_identity": {
    "app_display_name": "PayLife Kartensicherheit",
    "claimed_brand_or_persona": "PayLife（银行卡/支付安全工具）",
    "a11y_service_label": "PayLife",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务未声明 android:description，系统无障碍列表只显示品牌名 PayLife 而无功能说明；十余个引导类 Activity 全部 android:label=\"\" 且共用图标 @drawable/gnovtvwmsveg，多数叠加 excludeFromRecents/singleTask 使入口名不可见；类名与字段名为随机化乱码（SCoGtet、IZTjtACHVQ、KexhDHREsoSY），字符串以交错乱码与字节数组加密双重混淆。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.pvbitn.ireurvi.SCoGtet (Application) → com.pagkijxim.tycdlm.zxlqunay.zbpMvA (LAUNCHER Activity，无字节码)",
      "trigger_event": "进程启动时 Application.onCreate()",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（strings.xml 仅 pnulgtuvw=actTest）",
      "shown_text_zh": "静态不可见任何冷启动界面文案",
      "user_action_requested": "不可静态判定",
      "code_anchor": "com.pvbitn.ireurvi.SCoGtet.onCreate / res/values/strings.xml"
    },
    {
      "step": 2,
      "stage": "获权后动作",
      "screen_or_component": "运行期解密与反射装载的二阶段载荷（目标类名不可静态确定）",
      "trigger_event": "SCoGtet.onCreate → IZTjtACHVQ.tUsoDabT(Application) 解密 byte[] 字符串并反射取类、实例化 bnvSACy",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（解密前为 byte[]{-11,-102,100,-75,105,-44,...} 等字节数组）",
      "shown_text_zh": "载荷装载阶段的字符串全部加密，明文与界面内容静态不可得",
      "user_action_requested": "不可静态判定",
      "code_anchor": "com.pvbitn.ireurvi.IZTjtACHVQ.tUsoDabT(android.app.Application) / IZTjtACHVQ.tUsoDabT(byte[])"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：由 Manifest service android:label=\"PayLife\" 提供，无 android:description（配置 meta-data 指向 @xml/mxbawx）",
    "桌面图标名称：application android:label=\"PayLife Kartensicherheit\"",
    "res/values/strings.xml：仅 1 条 pnulgtuvw=actTest，无引导文案",
    "包内无 assets/ 目录，故不存在本地 HTML 引导页",
    "其余引导文字（弹窗/Activity/WebView/悬浮窗）均无静态载体，须待运行期解密载荷生成"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "PayLife Kartensicherheit",
      "text_zh": "PayLife 银行卡安全",
      "source_location": "AndroidManifest.xml application android:label",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "PayLife",
      "text_zh": "PayLife",
      "source_location": "AndroidManifest.xml service com.pagkijxim.tycdlm.KexhDHREsoSY android:label",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "actTest",
      "text_zh": "actTest（疑似残留测试串，非用户可见文案）",
      "source_location": "res/values/strings.xml key=pnulgtuvw",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态判定：实现无障碍引导的类未包含在 classes.dex 中，无 onResume/Timer 重跳代码可核验",
    "overlay_or_fake_settings": "不可静态判定：无 SYSTEM_ALERT_WINDOW 使用点可定位（权限已声明），res/layout 无引导布局证据",
    "restricted_settings_13plus_coaching": "无（未发现 ACTION_APPLICATION_DETAILS_SETTINGS 或受限设置相关字符串，targetSdkVersion=27 亦不涉及 Android 13 受限设置机制）",
    "post_grant_anti_removal": "不可静态判定：无 GLOBAL_ACTION_BACK/HOME 相关代码可核验",
    "benign_graceful_degradation": "无（未见任何降级或替代路径代码）"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以 Application 启动为起点：在 SCoGtet.onCreate 返回后即开始录屏/UTG 采样，并在监测到 Activity 切换到 com.pagkijxim.tycdlm.zxlqunay.* 或系统页 com.android.settings/.Settings$AccessibilitySettings 的瞬间抓取快照；若二阶段载荷为远端下发，需配合网络 Hook 在下载完成后立即开启 UTG。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后首个可见界面（启动 Activity zxlqunay.zbpMvA 或二阶段动态创建的 Activity）",
        "page_identifier": "TaskRecord 顶层 Activity 属于 com.pagkijxim.tycdlm 且 label 为空、图标为 @drawable/gnovtvwmsveg",
        "why_most_useful": "该类 Activity 无字节码，是唯一能确认载荷是否成功装载并呈现诱导界面的观测点",
        "observable_utg_signals": ["界面是否以 PayLife 品牌出现", "是否出现无障碍/安全授权相关按钮文本", "是否存在不可取消的弹窗层级（dialog 节点无取消控件）"]
      },
      {
        "page_role": "跳转系统无障碍设置前的引导页",
        "page_identifier": "当前 Activity 后紧接 com.android.settings AccessibilitySettings 的 Intent 跳转",
        "why_most_useful": "决定诱导方式属原生说明页、WebView 还是悬浮遮罩，是区分诱导形态的关键帧",
        "observable_utg_signals": ["页面根节点为 WebView 还是原生布局", "WebView URL 是本地 assets 还是远端域名", "是否存在逐步骤教学文本"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings/.accessibility.AccessibilitySettings 中 label=PayLife 的条目",
        "why_most_useful": "核验列表项是否仅有品牌名而无 description，评估用户可获得的真实信息量",
        "observable_utg_signals": ["条目 text 与 contentDescription", "是否存在副标题说明（预期缺失）"]
      },
      {
        "page_role": "从设置页返回后的压栈遮罩页",
        "page_identifier": "从 AccessibilitySettings 返回后 0.5–2 秒内新出现的顶层窗口/悬浮窗",
        "why_most_useful": "判定是否存在拒绝循环重跳或遮罩叠层引导",
        "observable_utg_signals": ["返回后是否立刻再次跳转设置页", "是否出现 TYPE_APPLICATION_OVERLAY 类窗口节点", "是否出现指向开关位置的引导箭头/高亮"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在显著盲区：包内不含无障碍服务与启动 Activity 的字节码，引导文案与跳转逻辑全部由运行期字节数组解密+反射生成（一阶段 Dropper 结构），纯静态 UTG 规则无法预判页面文本与跳转时机；若二阶段载荷经远端下发且采用图片化引导，则需 OCR 辅助。"
  },
  "behavior_pattern_tags": [
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "ID_MULTI_ALIAS_CAMOUFLAGE"
  ],
  "code_anchors": [
    "com.pvbitn.ireurvi.SCoGtet.onCreate",
    "com.pvbitn.ireurvi.IZTjtACHVQ.tUsoDabT(android.app.Application)",
    "com.pvbitn.ireurvi.IZTjtACHVQ.tUsoDabT(byte[])",
    "com.pvbitn.ireurvi.IZTjtACHVQ.tUsoDabT()",
    "res/values/strings.xml",
    "AndroidManifest.xml (service com.pagkijxim.tycdlm.KexhDHREsoSY, meta-data @xml/mxbawx)"
  ]
}
```

</details>
