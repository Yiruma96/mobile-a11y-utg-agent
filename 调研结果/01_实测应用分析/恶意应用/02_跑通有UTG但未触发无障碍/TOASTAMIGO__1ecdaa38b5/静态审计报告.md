# MR_159__1ecdaa38b5｜TOASTAMIGO — Smart AppLocker

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：132.2s

## 1. 一句话核心结论

- **核心申请方式**：加壳应用在系统无障碍列表中用“Smart AppLocker / 轻松锁定应用”的弱化描述申请全量窗口读取与按键过滤能力，并以“设置→无障碍→App Locker→打开”的硬编码文字教学引导用户手动开启，具体引导弹窗与拒绝重跳逻辑藏于 360 加固加密载荷。
- **静态可见性说明**：classes.dex 仅含 360 加固壳 com.qihoo.util 的 7 个类（StubApp1555239919/QHDialog/QhJobService 等），应用自身 com.goami.applocker.* 与 com.luna.powersaver.gp.* 类全部缺失；真实业务代码以 7.0MB 加密载荷 assets/slogan.gpt 存放，由 assets/libjiagu.so、libjiagu_a64.so、libjiagu_ls.so、libjiagu_x64.so、libjiagu_x86.so 在运行期解密加载。因此无障碍引导的点击回调、弹窗文案、是否死循环重跳等纯运行期细节不可静态还原；仅 Manifest、res/xml/phone_accessibility.xml 与 res/values/strings.xml 中的声明与教学文案静态可见。
- **命中的行为模式标签**：`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `1ecdaa38b5bb203cc7684b4bb74f46a4433b778c58d0e7d581e10164f9b71298` |
| 包名 / 年份 | `com.goami.applocker` / 2017 |
| 家族 / 品类 | **TOASTAMIGO**（同池样本数：44） |
| 原始来源标识 | https://www.trendmicro.com/en_us/research/17/k/toast-overlay-weaponized-install-android-malware-single-attack-chain.html |
| 桌面显示名 | Smart AppLocker |
| 引导页宣称品牌/身份 | Smart AppLocker（通用应用锁工具，宣称用于锁定应用） |
| 系统无障碍列表服务名 | Smart AppLocker（服务未设置 android:label，回退至应用名；描述为 The service for the purpose of Android 4.0.3 and above to lock apps easily.） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 使用 360 加固壳（com.qihoo.util.StubApp1555239919 为 application 入口，配套 LsActivity/SoService/libjiagu 系列）使真实类全部隐藏；2) 多 Activity 别名混淆：LAUNCHER 指向 com.qihoo.util.StartActivity（noHistory、excludeFromRecents），MAIN 指向 ApplicationListActivity，另有壳内 CommonActivity/CommonService(exported=true)/CommonProvider(exported=true)；3) 无障碍服务未设 android:label，系统列表只显示应用名，配合弱化 description 降低用户警惕；4) 导出服务 com.luna.powersaver.gp.service.GuardService 与 CPlusReceiver 构成与主界面无关的旁路拉起通道；5) 未发现伪造 isAccessibilityTool、空白/同形字或换行挤出警告的证据。 |
| 无障碍服务类名 | `com.goami.applocker.AppLocker.MyAccessibilityServiceTmp` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：com.miui.home,com.umiplus.screenlock,com.android.vending,com.android.settings,com.android.packageinstaller,com.google.android.packageinstaller,com.sec.android.app.launcher,com.bbk.launcher2,com.oppo.launcher |
| 共现高危权限 | `CAMERA, PACKAGE_USAGE_STATS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | The service for the purpose of Android 4.0.3 and above to lock apps easily. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.qihoo.util.StartActivity（LAUNCHER，noHistory=true）→ com.goami.applocker.AppLocker.ApplicationListActivity（MAIN，singleInstance） | 用户点击桌面图标启动；壳类 StubApp1555239919 先完成 slogan.gpt 解密与类加载后跳转 | 原生Activity | **原文**：Smart AppLocker<br>**译注**：桌面/任务栏显示名“Smart AppLocker”（应用锁工具） | 无（自动进入主界面，后续引导逻辑在加密载荷内） | `AndroidManifest.xml: com.qihoo.util.StartActivity / com.goami.applocker.AppLocker.ApplicationListActivity；com.qihoo.util.StubApp1555239919` |
| 2 | 引导说明页 | 主流程内的原生弹窗/提示（具体载体不可静态还原），文案资源 alp_42447968_cmd_android_m_above | 检测到无障碍服务未启用（触发点位于加密载荷，静态不可见） | 不可静态还原 | **原文**：This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it.<br>**译注**：本设备版本高于 Android 4.0.3。请进入 设置->无障碍服务->App Locker 并将其打开。 | 要求用户自行进入系统设置逐级找到无障碍服务并开启 App Locker；资源中未见对应的取消/跳过文案 | `res/values/strings.xml: alp_42447968_cmd_android_m_above（L85）` |
| 3 | 跳无障碍设置 | 系统无障碍服务列表页（android.settings.ACCESSIBILITY_SETTINGS），列表项为 Smart AppLocker | 用户按引导点击跳转（Intent 构造点位于加密载荷内，静态不可见） | 系统无障碍页 | **原文**：The service for the purpose of Android 4.0.3 and above to lock apps easily.<br>**译注**：本服务用于在 Android 4.0.3 及以上版本轻松锁定应用。 | 在系统无障碍列表中把 Smart AppLocker 开关拨到开启（系统标准页，用户可随时返回/关闭） | `res/xml/phone_accessibility.xml android:description → res/values/strings.xml: accessibility_service_description（L83）` |
| 4 | 拒权反馈循环 | Toast 提示（alp_42447968_cmd_android_m_above_toast）或重复弹窗 | 用户未开启即从系统设置返回（onResume 类回调，实现位于加密载荷，不可静态确认） | 不可静态还原 | **原文**：Find Setting->AccessibilityService->App Locker and Open it.<br>**译注**：找到 设置->无障碍服务->App Locker 并将其打开。 | 再次要求用户前往设置开启；是否形成强制重跳循环、是否存在取消按钮无法静态确认 | `res/values/strings.xml: alp_42447968_cmd_android_m_above_toast（L235）` |
| 5 | 获权后动作 | MyAccessibilityServiceTmp（typeAllMask / canRetrieveWindowContent / canRequestFilterKeyEvents）及旁路服务 GuardService | 系统绑定无障碍服务后回调（实现位于加密载荷，不可静态确认） | 不可静态还原 | 无 | 无 | `AndroidManifest.xml: com.goami.applocker.AppLocker.MyAccessibilityServiceTmp；com.luna.powersaver.gp.service.GuardService` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：服务未设 android:label，回退显示应用名 Smart AppLocker，描述来自 res/values/strings.xml accessibility_service_description（L83）
- res/values/strings.xml L85 alp_42447968_cmd_android_m_above：设置→无障碍服务→App Locker 的分步文字教学（载体弹窗位于加密载荷，静态不可见）
- res/values/strings.xml L235 alp_42447968_cmd_android_m_above_toast：同内容的 Toast 版教学提示
- res/values/strings.xml L136/L137 powersaver_title_accessibility_text(_2) = Accessibility、L111 powersaver_accessibility_observe_text = observe：com.luna.powersaver.gp 模块的无障碍引导标题文本
- 应用桌面/最近任务显示名 Smart AppLocker（app_name，Manifest 双启动别名共用 label）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | The service for the purpose of Android 4.0.3 and above to lock apps easily. | 本服务用于在 Android 4.0.3 及以上版本轻松锁定应用。 | `res/values/strings.xml: accessibility_service_description（L83），被 res/xml/phone_accessibility.xml 引用` | 隐私承诺 |
| en | This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it. | 本设备版本高于 Android 4.0.3。请进入 设置->无障碍服务->App Locker 并将其打开。 | `res/values/strings.xml: alp_42447968_cmd_android_m_above（L85）` | 受限设置分步教学 |
| en | Find Setting->AccessibilityService->App Locker and Open it. | 找到 设置->无障碍服务->App Locker 并将其打开。 | `res/values/strings.xml: alp_42447968_cmd_android_m_above_toast（L235）` | 受限设置分步教学 |
| en | Accessibility | 无障碍 | `res/values/strings.xml: powersaver_title_accessibility_text / powersaver_title_accessibility_text_2（L136-L137）` | 未知 |
| en | observe | 观察/监听 | `res/values/strings.xml: powersaver_accessibility_observe_text（L111）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：资源中存在“设置→无障碍→App Locker→打开”的弹窗文案与 Toast 文案两套，暗示未开启时会被反复提示；是否 onResume 死循环重跳、定时器拉起等具体实现位于 assets/slogan.gpt 解密后的 DEX，静态不可确认。
- **遮罩叠层 / 高仿系统设置页**：静态不可确认。Manifest 声明了 SYSTEM_ALERT_WINDOW（悬浮窗）与 Theme.Translucent.NoTitleBar 的 InstallRecommandActivity/InterstitalActivity，具备叠加遮罩或浮层的技术条件，但无代码级证据表明用于无障碍设置页遮罩。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。targetSdkVersion=24（2017 年样本），资源中不存在 Android 13 受限设置（应用详情右上角菜单允许受限设置）或 Session 安装器相关文案。
- **获权后即时行为与防撤权机制**：静态不可确认。未见 anti-removal 相关权限/文案证据（初筛 anti_removal 为空），是否监听设置页以 GLOBAL_ACTION_BACK/HOME 阻止撤权需运行期验证。
- **良性降级 / 替代方案**：无。未见手动模式/ADB/仅观看等替代路径文案；教学文案仅有“去设置打开”一条路径。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：两条并抓：①冷启动 com.qihoo.util.StartActivity → ApplicationListActivity 后首屏稳定时立即开始 UTG 采样（覆盖解密加载后的首个引导弹窗）；②监测到跳转 android.settings.ACCESSIBILITY_SETTINGS（或 APP_DETAILS_SETTINGS）时在跳转前后各 800ms 连续截图，并在用户从系统设置返回的 onResume 时刻再采样一轮，用于捕获拒绝重跳与压栈遮罩。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在两处盲区：1) 静态加壳（360 jiagu，载荷 assets/slogan.gpt 加密）本身不阻挡运行期 UTG，但会使代码级触发条件、是否死循环、获权后行为无法静态预判，需完全依赖运行期观测；2) 若引导页以纯图片或 WebView 远端 HTML 呈现（组件具备 WebView/网络权限条件），UTG 文本可能为空，此时需开启 OCR 并对 WebView 加载 URL 做流量侧核对。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动/首屏引导弹窗页** | ApplicationListActivity 之上的 Dialog 或透明 Activity，含“Setting->AccessibilityService->App Locker”类文本 | 该页是用户第一次被要求开启无障碍的位置，可直接读出文案、按钮集合（是否存在取消/跳过）以及是否不可关闭 | 文本节点包含 Setting / AccessibilityService / App Locker；按钮数量与文本（仅“OK/Go”还是存在 Cancel/Skip）；Dialog 是否 setCancelable(false)（返回键无效、无外部点击消失） |
| **跳转前说明页/中间页** | com.goami.applocker.accessibility.activity.InstallRecommandActivity 或 InterstitalActivity（Theme.Translucent.NoTitleBar） | 这两个透明 Activity 是壳内代码可能插入的教学/广告/推荐页载体，判断引导是否夹带安装推荐或广告是区分诱导性质的关键 | Activity 类名与 theme 为 Translucent；页面是否含安装/推荐/下载按钮；是否存在 WebView 节点或图片引导 |
| **系统无障碍服务列表项** | 设置→无障碍 中“Smart AppLocker”条目及其描述文本 | 核对系统实际呈现的名称与描述是否与申请的 typeAllMask/canRetrieveWindowContent 能力严重不匹配，是“弱化描述换取全量权限”的直接证据 | 条目文本 Smart AppLocker；描述文本 The service for the purpose of Android 4.0.3 and above to lock apps easily.；开关初始状态 |
| **从设置返回后的反馈/重跳页** | 返回应用瞬间的 Toast、重复 Dialog 或全屏遮罩 | 决定是否存在拒绝反馈循环与叠层逼迫，是判定强制性的核心观测点 | 返回后 1-3 秒内再次出现同类引导文本；Toast 文本 Find Setting->AccessibilityService->App Locker and Open it.；当前顶层窗口包名/类名是否被非系统悬浮层覆盖 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.goami.applocker.AppLocker.MyAccessibilityServiceTmp（AndroidManifest.xml service 声明，绑定 BIND_ACCESSIBILITY_SERVICE，配置 @xml/phone_accessibility）`
- `res/xml/phone_accessibility.xml（typeAllMask / canRetrieveWindowContent=true / canRequestFilterKeyEvents=true / description=@string/accessibility_service_description）`
- `res/values/strings.xml: accessibility_service_description、alp_42447968_cmd_android_m_above、alp_42447968_cmd_android_m_above_toast`
- `com.qihoo.util.StubApp1555239919 与 assets/slogan.gpt（360 加固壳入口与加密代码载荷）`
- `com.goami.applocker.accessibility.activity.InstallRecommandActivity / InterstitalActivity（Theme.Translucent.NoTitleBar 引导或推荐页载体）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点

**静态可见度：** DEX 层只有 360 加固壳。`classes.dex` 实际仅含 `com.qihoo.util` 的 7 个类（[StubApp1555239919](<resource-unit:#1.dex1 code:com.qihoo.util.StubApp1555239919>)、`QHDialog`、`QhJobService` 等），应用自身的 `com.goami.applocker.*` 类**全部不在 DEX 中**；真实代码以 7.0 MB 加密载荷 [assets/slogan.gpt](<resource-unit:#1 file:assets/slogan.gpt>) 的形式存在，由 `assets/libjiagu*.so` 在运行时解密并加载。因此“引导页面流转”的代码级细节（点击回调、`startActivity(ACTION_ACCESSIBILITY_SETTINGS)`、弹窗按钮、是否死循环重跳）**无法静态还原**。

**但可静态确认的事实链（Manifest + 资源层）足以刻画其引导设计：**

1. **入口是双启动别名**：LAUNCHER 指向 `com.qihoo.util.StartActivity`（`noHistory`、壳入口），MAIN 指向 `com.goami.applocker.AppLocker.ApplicationListActivity`；两者 `label` 均为 `@string/app_name` = **Smart AppLocker**。
2. **无障碍服务声明**：[service MyAccessibilityServiceTmp](<resource-unit:#1 manifest:components>) 受 `BIND_ACCESSIBILITY_SERVICE` 保护，配置指向 [res/xml/phone_accessibility.xml](<resource-unit:#1 file:res/xml/phone_accessibility.xml#L2>)：`typeAllMask` + `canRetrieveWindowContent="true"` + `canRequestFilterKeyEvents="true"`——即申请**读取全部窗口内容与过滤按键**的全量能力，而 `android:description` 仅写“lock apps easily”。
3. **系统列表显示名与描述**：服务未设 `android:label`，系统无障碍列表回退到应用名 **Smart AppLocker**；描述为 [strings.xml L83](<resource-unit:#1 file:res/values/strings.xml#L83>) “The service for the purpose of Android 4.0.3 and above to lock apps easily.”——把“全量窗口读取/按键过滤”弱化为“轻松锁定应用”。
4. **分步教学文本（硬编码在 strings 资源）**：
   - [L85 `alp_42447968_cmd_android_m_above`](<resource-unit:#1 file:res/values/strings.xml#L85>)：“This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it.”
   - [L235 `alp_42447968_cmd_android_m_above_toast`](<resource-unit:#1 file:res/values/strings.xml#L235>)：“Find Setting->AccessibilityService->App Locker and Open it.”
   两条均为**纯文字路径教学**（设置→无障碍→App Locker→打开），无“取消/跳过”语义字符串。
5. **辅助投放组件**：`com.goami.applocker.accessibility.activity` 包下另有 `InstallRecommandActivity`、`InterstitalActivity`（`Theme.Translucent.NoTitleBar`，`excludeFromRecents`），以及导出服务 `com.luna.powersaver.gp.service.GuardService` 与 `CPlusReceiver`（监听 `BOOT_COMPLETED`、`CONNECTIVITY_CHANGE`、`USB_STATE`、自定义 `com.luna.powersaver.gp.ACTION_CLOCK/ACTION_OPEN_RECORD`），配套字符串 `powersaver_title_accessibility_text`=“Accessibility”。说明除应用主流程外，还存在一条**独立于主界面、可在开机/网络/定时事件下被唤起的旁路拉起通道**，其用途被壳内代码隐藏。
6. **高敏感权限组合**：`SYSTEM_ALERT_WINDOW` + `PACKAGE_USAGE_STATS` + `WRITE_SETTINGS` + `GET_TASKS/REAL_GET_TASKS` + `CAMERA` + `READ_PHONE_STATE`，与 TOASTAMIGO 家族的“遮罩/任务监听/静默改设置”能力面吻合，但具体调用点在加密载荷内，未获代码级证据。

**未决与覆盖边界：** 引导弹窗的文案、按钮、拒绝后的重跳逻辑、是否叠遮罩、是否教用户开启受限设置，均位于 `slogan.gpt` 解密后的 DEX 中，本次未做脱壳还原，故不作定性断言；UTG 运行期取证是补齐该链的最优路径。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "classes.dex 仅含 360 加固壳 com.qihoo.util 的 7 个类（StubApp1555239919/QHDialog/QhJobService 等），应用自身 com.goami.applocker.* 与 com.luna.powersaver.gp.* 类全部缺失；真实业务代码以 7.0MB 加密载荷 assets/slogan.gpt 存放，由 assets/libjiagu.so、libjiagu_a64.so、libjiagu_ls.so、libjiagu_x64.so、libjiagu_x86.so 在运行期解密加载。因此无障碍引导的点击回调、弹窗文案、是否死循环重跳等纯运行期细节不可静态还原；仅 Manifest、res/xml/phone_accessibility.xml 与 res/values/strings.xml 中的声明与教学文案静态可见。",
  "summary_one_liner": "加壳应用在系统无障碍列表中用“Smart AppLocker / 轻松锁定应用”的弱化描述申请全量窗口读取与按键过滤能力，并以“设置→无障碍→App Locker→打开”的硬编码文字教学引导用户手动开启，具体引导弹窗与拒绝重跳逻辑藏于 360 加固加密载荷。",
  "disguise_identity": {
    "app_display_name": "Smart AppLocker",
    "claimed_brand_or_persona": "Smart AppLocker（通用应用锁工具，宣称用于锁定应用）",
    "a11y_service_label": "Smart AppLocker（服务未设置 android:label，回退至应用名；描述为 The service for the purpose of Android 4.0.3 and above to lock apps easily.）",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 使用 360 加固壳（com.qihoo.util.StubApp1555239919 为 application 入口，配套 LsActivity/SoService/libjiagu 系列）使真实类全部隐藏；2) 多 Activity 别名混淆：LAUNCHER 指向 com.qihoo.util.StartActivity（noHistory、excludeFromRecents），MAIN 指向 ApplicationListActivity，另有壳内 CommonActivity/CommonService(exported=true)/CommonProvider(exported=true)；3) 无障碍服务未设 android:label，系统列表只显示应用名，配合弱化 description 降低用户警惕；4) 导出服务 com.luna.powersaver.gp.service.GuardService 与 CPlusReceiver 构成与主界面无关的旁路拉起通道；5) 未发现伪造 isAccessibilityTool、空白/同形字或换行挤出警告的证据。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.qihoo.util.StartActivity（LAUNCHER，noHistory=true）→ com.goami.applocker.AppLocker.ApplicationListActivity（MAIN，singleInstance）",
      "trigger_event": "用户点击桌面图标启动；壳类 StubApp1555239919 先完成 slogan.gpt 解密与类加载后跳转",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Smart AppLocker",
      "shown_text_zh": "桌面/任务栏显示名“Smart AppLocker”（应用锁工具）",
      "user_action_requested": "无（自动进入主界面，后续引导逻辑在加密载荷内）",
      "code_anchor": "AndroidManifest.xml: com.qihoo.util.StartActivity / com.goami.applocker.AppLocker.ApplicationListActivity；com.qihoo.util.StubApp1555239919"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "主流程内的原生弹窗/提示（具体载体不可静态还原），文案资源 alp_42447968_cmd_android_m_above",
      "trigger_event": "检测到无障碍服务未启用（触发点位于加密载荷，静态不可见）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it.",
      "shown_text_zh": "本设备版本高于 Android 4.0.3。请进入 设置->无障碍服务->App Locker 并将其打开。",
      "user_action_requested": "要求用户自行进入系统设置逐级找到无障碍服务并开启 App Locker；资源中未见对应的取消/跳过文案",
      "code_anchor": "res/values/strings.xml: alp_42447968_cmd_android_m_above（L85）"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍服务列表页（android.settings.ACCESSIBILITY_SETTINGS），列表项为 Smart AppLocker",
      "trigger_event": "用户按引导点击跳转（Intent 构造点位于加密载荷内，静态不可见）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "The service for the purpose of Android 4.0.3 and above to lock apps easily.",
      "shown_text_zh": "本服务用于在 Android 4.0.3 及以上版本轻松锁定应用。",
      "user_action_requested": "在系统无障碍列表中把 Smart AppLocker 开关拨到开启（系统标准页，用户可随时返回/关闭）",
      "code_anchor": "res/xml/phone_accessibility.xml android:description → res/values/strings.xml: accessibility_service_description（L83）"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "Toast 提示（alp_42447968_cmd_android_m_above_toast）或重复弹窗",
      "trigger_event": "用户未开启即从系统设置返回（onResume 类回调，实现位于加密载荷，不可静态确认）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Find Setting->AccessibilityService->App Locker and Open it.",
      "shown_text_zh": "找到 设置->无障碍服务->App Locker 并将其打开。",
      "user_action_requested": "再次要求用户前往设置开启；是否形成强制重跳循环、是否存在取消按钮无法静态确认",
      "code_anchor": "res/values/strings.xml: alp_42447968_cmd_android_m_above_toast（L235）"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "MyAccessibilityServiceTmp（typeAllMask / canRetrieveWindowContent / canRequestFilterKeyEvents）及旁路服务 GuardService",
      "trigger_event": "系统绑定无障碍服务后回调（实现位于加密载荷，不可静态确认）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无（获权后的实际行为不可静态见，Manifest 层面可见 SYSTEM_ALERT_WINDOW / PACKAGE_USAGE_STATS / GET_TASKS / WRITE_SETTINGS 能力面）",
      "user_action_requested": "无",
      "code_anchor": "AndroidManifest.xml: com.goami.applocker.AppLocker.MyAccessibilityServiceTmp；com.luna.powersaver.gp.service.GuardService"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：服务未设 android:label，回退显示应用名 Smart AppLocker，描述来自 res/values/strings.xml accessibility_service_description（L83）",
    "res/values/strings.xml L85 alp_42447968_cmd_android_m_above：设置→无障碍服务→App Locker 的分步文字教学（载体弹窗位于加密载荷，静态不可见）",
    "res/values/strings.xml L235 alp_42447968_cmd_android_m_above_toast：同内容的 Toast 版教学提示",
    "res/values/strings.xml L136/L137 powersaver_title_accessibility_text(_2) = Accessibility、L111 powersaver_accessibility_observe_text = observe：com.luna.powersaver.gp 模块的无障碍引导标题文本",
    "应用桌面/最近任务显示名 Smart AppLocker（app_name，Manifest 双启动别名共用 label）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "The service for the purpose of Android 4.0.3 and above to lock apps easily.",
      "text_zh": "本服务用于在 Android 4.0.3 及以上版本轻松锁定应用。",
      "source_location": "res/values/strings.xml: accessibility_service_description（L83），被 res/xml/phone_accessibility.xml 引用",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it.",
      "text_zh": "本设备版本高于 Android 4.0.3。请进入 设置->无障碍服务->App Locker 并将其打开。",
      "source_location": "res/values/strings.xml: alp_42447968_cmd_android_m_above（L85）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Find Setting->AccessibilityService->App Locker and Open it.",
      "text_zh": "找到 设置->无障碍服务->App Locker 并将其打开。",
      "source_location": "res/values/strings.xml: alp_42447968_cmd_android_m_above_toast（L235）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility",
      "text_zh": "无障碍",
      "source_location": "res/values/strings.xml: powersaver_title_accessibility_text / powersaver_title_accessibility_text_2（L136-L137）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "observe",
      "text_zh": "观察/监听",
      "source_location": "res/values/strings.xml: powersaver_accessibility_observe_text（L111）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "资源中存在“设置→无障碍→App Locker→打开”的弹窗文案与 Toast 文案两套，暗示未开启时会被反复提示；是否 onResume 死循环重跳、定时器拉起等具体实现位于 assets/slogan.gpt 解密后的 DEX，静态不可确认。",
    "overlay_or_fake_settings": "静态不可确认。Manifest 声明了 SYSTEM_ALERT_WINDOW（悬浮窗）与 Theme.Translucent.NoTitleBar 的 InstallRecommandActivity/InterstitalActivity，具备叠加遮罩或浮层的技术条件，但无代码级证据表明用于无障碍设置页遮罩。",
    "restricted_settings_13plus_coaching": "无。targetSdkVersion=24（2017 年样本），资源中不存在 Android 13 受限设置（应用详情右上角菜单允许受限设置）或 Session 安装器相关文案。",
    "post_grant_anti_removal": "静态不可确认。未见 anti-removal 相关权限/文案证据（初筛 anti_removal 为空），是否监听设置页以 GLOBAL_ACTION_BACK/HOME 阻止撤权需运行期验证。",
    "benign_graceful_degradation": "无。未见手动模式/ADB/仅观看等替代路径文案；教学文案仅有“去设置打开”一条路径。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "两条并抓：①冷启动 com.qihoo.util.StartActivity → ApplicationListActivity 后首屏稳定时立即开始 UTG 采样（覆盖解密加载后的首个引导弹窗）；②监测到跳转 android.settings.ACCESSIBILITY_SETTINGS（或 APP_DETAILS_SETTINGS）时在跳转前后各 800ms 连续截图，并在用户从系统设置返回的 onResume 时刻再采样一轮，用于捕获拒绝重跳与压栈遮罩。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动/首屏引导弹窗页",
        "page_identifier": "ApplicationListActivity 之上的 Dialog 或透明 Activity，含“Setting->AccessibilityService->App Locker”类文本",
        "why_most_useful": "该页是用户第一次被要求开启无障碍的位置，可直接读出文案、按钮集合（是否存在取消/跳过）以及是否不可关闭",
        "observable_utg_signals": ["文本节点包含 Setting / AccessibilityService / App Locker", "按钮数量与文本（仅“OK/Go”还是存在 Cancel/Skip）", "Dialog 是否 setCancelable(false)（返回键无效、无外部点击消失）"]
      },
      {
        "page_role": "跳转前说明页/中间页",
        "page_identifier": "com.goami.applocker.accessibility.activity.InstallRecommandActivity 或 InterstitalActivity（Theme.Translucent.NoTitleBar）",
        "why_most_useful": "这两个透明 Activity 是壳内代码可能插入的教学/广告/推荐页载体，判断引导是否夹带安装推荐或广告是区分诱导性质的关键",
        "observable_utg_signals": ["Activity 类名与 theme 为 Translucent", "页面是否含安装/推荐/下载按钮", "是否存在 WebView 节点或图片引导"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置→无障碍 中“Smart AppLocker”条目及其描述文本",
        "why_most_useful": "核对系统实际呈现的名称与描述是否与申请的 typeAllMask/canRetrieveWindowContent 能力严重不匹配，是“弱化描述换取全量权限”的直接证据",
        "observable_utg_signals": ["条目文本 Smart AppLocker", "描述文本 The service for the purpose of Android 4.0.3 and above to lock apps easily.", "开关初始状态"]
      },
      {
        "page_role": "从设置返回后的反馈/重跳页",
        "page_identifier": "返回应用瞬间的 Toast、重复 Dialog 或全屏遮罩",
        "why_most_useful": "决定是否存在拒绝反馈循环与叠层逼迫，是判定强制性的核心观测点",
        "observable_utg_signals": ["返回后 1-3 秒内再次出现同类引导文本", "Toast 文本 Find Setting->AccessibilityService->App Locker and Open it.", "当前顶层窗口包名/类名是否被非系统悬浮层覆盖"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在两处盲区：1) 静态加壳（360 jiagu，载荷 assets/slogan.gpt 加密）本身不阻挡运行期 UTG，但会使代码级触发条件、是否死循环、获权后行为无法静态预判，需完全依赖运行期观测；2) 若引导页以纯图片或 WebView 远端 HTML 呈现（组件具备 WebView/网络权限条件），UTG 文本可能为空，此时需开启 OCR 并对 WebView 加载 URL 做流量侧核对。"
  },
  "behavior_pattern_tags": [
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.goami.applocker.AppLocker.MyAccessibilityServiceTmp（AndroidManifest.xml service 声明，绑定 BIND_ACCESSIBILITY_SERVICE，配置 @xml/phone_accessibility）",
    "res/xml/phone_accessibility.xml（typeAllMask / canRetrieveWindowContent=true / canRequestFilterKeyEvents=true / description=@string/accessibility_service_description）",
    "res/values/strings.xml: accessibility_service_description、alp_42447968_cmd_android_m_above、alp_42447968_cmd_android_m_above_toast",
    "com.qihoo.util.StubApp1555239919 与 assets/slogan.gpt（360 加固壳入口与加密代码载荷）",
    "com.goami.applocker.accessibility.activity.InstallRecommandActivity / InterstitalActivity（Theme.Translucent.NoTitleBar 引导或推荐页载体）"
  ]
}
```

**风险台账说明：** 本轮未写入 `record_risk`。当前可证实的仅为 Manifest 声明与资源文案（弱化描述 + 分步教学），而“诱导/强制/拒绝循环”等定性要件位于加密载荷内、缺代码级闭合证据，按“证据未闭合不提交”的要求留作未决项，待脱壳还原或 UTG 运行期取证后再判定。

</details>
