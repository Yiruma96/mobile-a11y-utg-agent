# MB_051__33ece83956｜Coper — Chrome

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：174.5s

## 1. 一句话核心结论

- **核心申请方式**：一阶段加载器 APK 以「Chrome」为显示名和无障碍服务名、以土耳其语「启用无障碍服务」作为无障碍描述，冷启动即在 attachBaseContext 解密 assets/yYnsu.json 注入二阶段 dex，由隐藏载荷完成引导用户开启高权限无障碍服务的流程。
- **静态可见性说明**：明文 classes.dex 仅含 Application 加载器（com.wreck.chef.Haveragestep + Qfrostwild 反射注入 dexElements）与第三方 SDK；全部无障碍引导逻辑位于 assets/yYnsu.json（156869 字节，已加密/编码）经 roomreview() 解密后写入 getDir("onion") 并由 carcorn() 反射注入系统 ClassLoader 的二阶段 dex 中，静态无法还原；主 DEX 中不存在 ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS / isAccessibilityServiceEnabled 的调用点。可静态确认的仅有 Manifest 声明、无障碍配置 XML 与 strings.xml 诱饵文本。
- **命中的行为模式标签**：`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `33ece8395604682f2c428a5b7a11e562b836f44f7b6fbb0caaa84bfa80d0c8ff` |
| 包名 / 年份 | `com.wreck.chef` / 2026 |
| 家族 / 品类 | **Coper**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Chrome |
| 引导页宣称品牌/身份 | Google Chrome 浏览器（com.wreck.chef 包名、com.elevator.* 混淆类名与之毫无关系） |
| 系统无障碍列表服务名 | Chrome |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务 label 与桌面图标名共用 @string/a="Chrome"，直接冒用系统浏览器品牌；strings.xml 全包仅两条字符串（WIPEAYSSVi/a），资源面被极端裁剪以隐藏意图；应用类全部为 com.elevator 下 1-4 字符混淆名；6 个随机名无属性 Activity（ycpsttrsga、tdwjlrqtqhhauqf、zreuctkootj、qwwhvefvya、tzmjlgjfdqhfc、gxmctqsouzqgleg）作为隐藏载体；APK 内 100 个 ZIP 条目被置加密标志位（含 yYnsu.json），阻断 apktool/apkid 常规解包；Application 中大量算术噪声语句干扰反编译；未发现伪造 isAccessibilityTool 属性（该属性在配置 XML 中未出现）。 |
| 无障碍服务类名 | `com.elevator.p024l` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | android.app.Application: com.wreck.chef.Haveragestep（manifest android:name） | 进程启动 → attachBaseContext(Context) 回调，在 super.attachBaseContext 之后立即执行 | 不可静态还原 | 无 | 无（用户无感知） | `com.wreck.chef.Haveragestep#attachBaseContext / #roomreview；字段 Awindowbunker="yYnsu.json"、Ainmatenetwork="onion"` |
| 2 | 冷启动入口 | ClassLoader 注入：Qfrostwild.carcorn(ClassLoader, File dexDir, List<File>) → pathList.makePathElements/makeDexElements → relieforgan(obj,"dexElements",...) | attachBaseContext 内 roomreview() 返回 true（载荷解密落盘成功）后调用 | 不可静态还原 | 无 | 无 | `com.wreck.chef.Qfrostwild#carcorn` |
| 3 | 业务功能触发 | com.elevator.p045l（LAUNCHER，label=@string/a="Chrome"，excludeFromRecents=true，screenOrientation=10，透明主题 Theme.AppCompat.Transparent.NoActionBar） | 用户点击桌面「Chrome」图标 → MAIN/LAUNCHER | 不可静态还原 | **原文**：无（明文代码中无该 Activity 的任何实现，仅在二阶段载荷内）<br>**译注**：启动器首屏，实际渲染内容由加密载荷决定 | 不可静态还原 | `AndroidManifest.xml <activity android:name="com.elevator.p045l"> + res/values/styles.xml Theme.AppCompat.Transparent.NoActionBar` |
| 4 | 跳无障碍设置 | 二阶段载荷内的引导页 → 系统设置 android.settings.ACCESSIBILITY_SETTINGS | 不可静态还原（主 DEX 中无 ACCESSIBILITY_SETTINGS 字符串与 startActivity 调用点） | 不可静态还原 | **原文**：不可静态还原<br>**译注**：预计为土耳其语引导文案，需 UTG 抓取 | 不可静态还原 | `assets/yYnsu.json（加密二阶段载荷）` |
| 5 | 遮罩叠层指引 | 系统无障碍服务列表项：com.elevator.p024l（label="Chrome"，description="Erişebilirlik Servisileri Etkinleştirme"） | 用户进入设置后，系统渲染该服务的名称与说明；应用侧可配合透明浮动 Activity 叠层 | 系统无障碍页 | **原文**：Chrome / Erişebilirlik Servisileri Etkinleştirme<br>**译注**：Chrome / 启用无障碍服务 | 用户在该列表中点击「Chrome」并开启开关 | `AndroidManifest.xml <service android:name="com.elevator.p024l" android:label="@7F030001"> + xml/dyruxlcc.xml + res/values/strings.xml` |
| 6 | 获权后动作 | com.elevator.p024l (AccessibilityService)：accessibilityEventTypes=0xFFFFFFFF、canRetrieveWindowContent=true、canPerformGestures=true、accessibilityFlags=0x53 | 服务被系统绑定后 onServiceConnected / onAccessibilityEvent（实现体在加密载荷内） | 不可静态还原 | **原文**：不可静态还原<br>**译注**：全事件监听 + 读屏 + 手势代点，具备自动点击与界面劫持能力 | 不可静态还原 | `xml/dyruxlcc.xml（无障碍能力声明）+ assets/yYnsu.json（服务实现）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统「设置 → 无障碍 → 已下载的服务」列表项：服务名 "Chrome"（@string/a），下方说明文字 "Erişebilirlik Servisileri Etkinleştirme"（@7F030000 = strings.xml WIPEAYSSVi）——这是唯一可静态确认的引导文本落点
- 桌面图标名："Chrome"（@string/a，同时用于 activity label 与 device-admin receiver label）
- 冷启动后的引导页/弹窗：位于加密二阶段 dex（assets/yYnsu.json 解密产物），明文资源中不存在任何引导文案、HTML 或 layout
- 透明浮动 Activity（Theme.AppCompat.Transparent.NoActionBar，windowIsFloating/Translucent、backgroundDimEnabled=false）为潜在的叠层遮挡载体，但具体承载文本在载荷内
- 无本地 assets/*.html 引导页、无 res/layout 引导布局、无 WebView 加载说明页（assets 目录仅有 Unity/广告 SDK 资源与图片）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| tr | Erişebilirlik Servisileri Etkinleştirme | 启用无障碍服务 | `res/values/strings.xml key=WIPEAYSSVi（被无障碍服务 meta-data android:description=@7F030000 引用）` | 良性透明说明 |
| en | Chrome | Chrome（谷歌浏览器） | `res/values/strings.xml key=a（用于 application android:label、无障碍服务 android:label、device-admin receiver label 及启动 Activity label）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：明文代码中无 onResume 重跳、无 Timer、无 Settings 结果回调（无 startActivityForResult/isAccessibilityServiceEnabled），拒权循环逻辑位于加密二阶段 dex；仅可确认 BOOT_COMPLETED/USER_PRESENT/SCREEN_ON/PACKAGE_ADDED 等 13 个动作的高优先级（priority=999）广播接收器 com.elevator.p060d 为后台反复拉起提供通路。
- **遮罩叠层 / 高仿系统设置页**：未发现高仿系统无障碍开关页资源（无对应 layout/xml）；但存在透明浮动、无边框、无变暗的 Activity 主题与多个随机名无属性 Activity，为叠层遮挡/半透明引导窗预留了载体，实际叠层行为在载荷内不可静态还原。
- **Android 13+ 受限设置（Restricted Settings）应对**：不可静态还原（minSdkVersion=26，若载荷内含 Android 13+ 受限设置教学文本，只存在于 yYnsu.json 解密产物中）
- **获权后即时行为与防撤权机制**：不可静态还原；已确认配套反移除能力：BIND_DEVICE_ADMIN 接收器 com.elevator.p078p（USES_POLICY_FORCE_LOCK）、无障碍配置 accessibilityFlags=0x53 与 canPerformGestures=true（可模拟 GLOBAL_ACTION_BACK/HOME 及代点），但具体阻止撤权代码在载荷内。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以「进程启动即 hook Application.attachBaseContext 完成后的首个 Activity 上屏」为第一锚点，并以「Activity 启动 Intent 命中 android.settings.ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS」为第二锚点；由于跳转代码在二阶段 dex，需在 carcorn() 注入完成后（或直接在系统 settings 包被拉起瞬间）开始抓取。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区为一阶段 Dropper 结构：APK 自身不含任何引导 UI，仅 Application 解密注入；若 UTG 在 carcorn 完成前采样或二阶段 dex 解密失败（设备 API/目录条件不满足），将只能看到空白/闪退，看不到引导页。此外 100 个 ZIP 条目被置加密标志位，静态工具易误判为「加密包」而放弃，实际数据明文可解。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **系统无障碍服务列表项（诱饵本体）** | Settings$AccessibilitySettings 列表中 label 为「Chrome」、summary 为「Erişebilirlik Servisileri Etkinleştirme」的条目 | 这是唯一可静态确认、且必然出现的诱导落点；服务名与品牌冒充、土耳其语说明在此同时暴露，可与 Manifest 声明一一对应 | 服务名文本 = Chrome；说明文本 = Erişebilirlik Servisileri Etkinleştirme；条目开关初始为关闭；所在页包名 com.android.settings |
| **冷启动首屏 / 引导说明页（载荷内）** | com.elevator.p045l 启动后的首个全屏窗口（无标题栏、非近期任务显示），或其后的透明浮动窗口 | 捕获载荷解密后的真实引导文案与按钮集合，用于判断是否有取消/跳过、是否为恐吓或假更新话术 | 可见文本节点全量（土耳其语/英语）；是否存在可点击的「取消/跳过/稍后」节点；窗口是否 isFloating/半透明叠层；是否存在 WebView 节点 |
| **跳设置后压栈遮罩页 / 拒权返回页** | 从 settings 返回后 800ms 内重新出现的 Activity 或悬浮窗 | 判定是否为 onResume 死循环重跳、是否叠加遮罩指引用户点击哪个位置 | 返回后 0-2s 内 Activity 栈变化次数；是否存在覆盖在 settings 之上的半透明窗口；是否有指向开关位置的箭头/高亮节点 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.wreck.chef.Haveragestep#attachBaseContext`
- `com.wreck.chef.Haveragestep#roomreview`
- `com.wreck.chef.Qfrostwild#carcorn`
- `assets/yYnsu.json`
- `xml/dyruxlcc.xml`
- `res/values/strings.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（静态可见部分）

**一、静态可见性判定：核心引导流程不在明文代码中，位于加密的二阶段 dex 载荷内。**

- 应用清单本身高度混淆，应用类全部为 `com.elevator.*` 短名；主 DEX 仅 1624 个类，除 `com.unity3d`、`com.adswizz` 等第三方库外，**自身代码只有 2 个类**：`com.wreck.chef.Haveragestep`（自定义 Application）与 `com.wreck.chef.Qfrostwild`（反射注入工具）。
- [Haveragestep.attachBaseContext()](<resource-unit:#1.dex1 code:com.wreck.chef.Haveragestep#attachBaseContext>) 在 `super.attachBaseContext()` 之后立即：
  - `File dir = context.getDir("onion", 0)`；
  - 定位 `new File(assetsDir, "yYnsu.json")`（`Awindowbunker = "yYnsu.json"`，`roomreview()` 中 `context.getAssets().open(...)` 读取）；
  - 调用 [Qfrostwild.carcorn()](<resource-unit:#1.dex1 code:com.wreck.chef.Qfrostwild#carcorn>)，用反射取 `pathList` → `makePathElements`/`makeDexElements` → `relieforgan(obj,"dexElements", …)` **把解密后的 dex 元素注入系统 ClassLoader**。
- 因此该 APK 是**一阶段加载器（Dropper）**：真正的无障碍引导 UI、`ACTION_ACCESSIBILITY_SETTINGS` 跳转、遮罩层、拒权循环逻辑全部在 `assets/yYnsu.json`（156,869 字节，压缩后反而更大 → 已加密/编码）解密出的二阶段 dex 中，**静态不可还原**。主 DEX 中不存在 `ACCESSIBILITY_SETTINGS`、`APPLICATION_DETAILS_SETTINGS`、`isAccessibilityServiceEnabled`、`startActivityForResult` 的任何调用点（已定向搜索，全部 no_matches）。

**二、可静态确认的身份伪装与无障碍声明（这部分证据确凿）**

- 应用显示名 `@string/a` = **`Chrome`**，无障碍服务 `com.elevator.p024l` 的 `android:label` 同样是 `@string/a` = **`Chrome`** —— 在系统无障碍服务列表中会显示为「Chrome」。
- 无障碍服务 `android:description` = `@7F030000` = `WIPEAYSSVi` = **`Erişebilirlik Servisileri Etkinleştirme`**（土耳其语，意为「启用无障碍服务」），指向土耳其语受害群体（与 Coper 家族目标一致）。`strings.xml` 全应用仅两条字符串，全部服务于这套伪装。
- 无障碍配置（`xml/dyruxlcc.xml`）：`accessibilityEventTypes=0xFFFFFFFF`（监听全部事件）、`canRetrieveWindowContent=true`、`canPerformGestures=true`、`accessibilityFlags=0x53`（含 FLAG_RETRIEVE_INTERACTIVE_WINDOWS / FLAG_REQUEST_FILTER_KEY_EVENTS 类能力）—— 即完整的读屏＋手势代点＋按键拦截能力，是后续「自动点击确认/自动开启」的技术前提。
- 配套清单能力齐全：`READ_SMS`/`RECEIVE_SMS`/`SEND_SMS`（`priority=999` 的 `SMS_RECEIVED` 与 `SMS_DELIVER` 双接收器）、`CALL_PHONE`、`QUERY_ALL_PACKAGES`、`WRITE_SETTINGS`、`REQUEST_IGNORE_BATTERY_OPTIMIZATIONS`、`BIND_DEVICE_ADMIN`（`com.elevator.p078p`）、`NotificationListenerService`（`com.elevator.p092o`）、`SYSTEM_ALERT_WINDOW` 未声明但主题为透明浮动窗口（`Theme.AppCompat.Transparent.NoActionBar`，`windowIsFloating/Translucent/backgroundDimEnabled=false`）—— 典型无边框悬浮 Activity 载体，用于叠层遮挡/引导。
- 反分析手法：APK 内 **100 个 ZIP 条目被置上「加密」标志位**（含 `assets/yYnsu.json`、`classes.dex` 相关条目），使 `apktool`/`zipfile`/`apkid` 直接解包报 `password required`，需先清除通用标志位才能读取；此外清单中有 6 个随机名 Activity（`ycpsttrsga`、`tdwjlrqtqhhauqf`、`zreuctkootj`、`qwwhvefvya`、`tzmjlgjfdqhfc`、`gxmctqsouzqgleg`…）无任何声明属性，作为载荷内可动态启动的隐藏载体。

**三、运行期引导流程的推定边界**

可静态确认的骨架：冷启动 → `Haveragestep.attachBaseContext` 解密 `yYnsu.json` → 注入二阶段 dex → 启动 `com.elevator.p045l`（`excludeFromRecents=true`、`screenOrientation=10` 全向、透明主题）。二阶段内部的具体弹窗文案、是否 `onResume` 死循环重跳设置、是否自点开关、是否有取消按钮，**无法从明文代码给出逐字证据**，需 UTG 抓取。

> 说明：本轮受 14 次工具调用硬约束，已超预算即收口，未执行 `record_risk` 登记（证据已足以支撑「二阶段加密载荷 + 无障碍冒充 Chrome + 土耳其语诱饵」命题，建议后续单独登记为 `malware_trojan` / `review_evasion_mutation`）。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "明文 classes.dex 仅含 Application 加载器（com.wreck.chef.Haveragestep + Qfrostwild 反射注入 dexElements）与第三方 SDK；全部无障碍引导逻辑位于 assets/yYnsu.json（156869 字节，已加密/编码）经 roomreview() 解密后写入 getDir(\"onion\") 并由 carcorn() 反射注入系统 ClassLoader 的二阶段 dex 中，静态无法还原；主 DEX 中不存在 ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS / isAccessibilityServiceEnabled 的调用点。可静态确认的仅有 Manifest 声明、无障碍配置 XML 与 strings.xml 诱饵文本。",
  "summary_one_liner": "一阶段加载器 APK 以「Chrome」为显示名和无障碍服务名、以土耳其语「启用无障碍服务」作为无障碍描述，冷启动即在 attachBaseContext 解密 assets/yYnsu.json 注入二阶段 dex，由隐藏载荷完成引导用户开启高权限无障碍服务的流程。",
  "disguise_identity": {
    "app_display_name": "Chrome",
    "claimed_brand_or_persona": "Google Chrome 浏览器（com.wreck.chef 包名、com.elevator.* 混淆类名与之毫无关系）",
    "a11y_service_label": "Chrome",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务 label 与桌面图标名共用 @string/a=\"Chrome\"，直接冒用系统浏览器品牌；strings.xml 全包仅两条字符串（WIPEAYSSVi/a），资源面被极端裁剪以隐藏意图；应用类全部为 com.elevator 下 1-4 字符混淆名；6 个随机名无属性 Activity（ycpsttrsga、tdwjlrqtqhhauqf、zreuctkootj、qwwhvefvya、tzmjlgjfdqhfc、gxmctqsouzqgleg）作为隐藏载体；APK 内 100 个 ZIP 条目被置加密标志位（含 yYnsu.json），阻断 apktool/apkid 常规解包；Application 中大量算术噪声语句干扰反编译；未发现伪造 isAccessibilityTool 属性（该属性在配置 XML 中未出现）。",
    "obfuscation_evidence": "xml/dyruxlcc.xml 仅有 description/eventTypes/feedbackType/flags/canRetrieveWindowContent/canPerformGestures 六项，无 isAccessibilityTool"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "android.app.Application: com.wreck.chef.Haveragestep（manifest android:name）",
      "trigger_event": "进程启动 → attachBaseContext(Context) 回调，在 super.attachBaseContext 之后立即执行",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面，仅解密与注入",
      "user_action_requested": "无（用户无感知）",
      "code_anchor": "com.wreck.chef.Haveragestep#attachBaseContext / #roomreview；字段 Awindowbunker=\"yYnsu.json\"、Ainmatenetwork=\"onion\""
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "ClassLoader 注入：Qfrostwild.carcorn(ClassLoader, File dexDir, List<File>) → pathList.makePathElements/makeDexElements → relieforgan(obj,\"dexElements\",...)",
      "trigger_event": "attachBaseContext 内 roomreview() 返回 true（载荷解密落盘成功）后调用",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "把解密后的二阶段 dex 注入 dexElements，使后续所有 com.elevator.* 业务类可被加载",
      "user_action_requested": "无",
      "code_anchor": "com.wreck.chef.Qfrostwild#carcorn"
    },
    {
      "step": 3,
      "stage": "业务功能触发",
      "screen_or_component": "com.elevator.p045l（LAUNCHER，label=@string/a=\"Chrome\"，excludeFromRecents=true，screenOrientation=10，透明主题 Theme.AppCompat.Transparent.NoActionBar）",
      "trigger_event": "用户点击桌面「Chrome」图标 → MAIN/LAUNCHER",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（明文代码中无该 Activity 的任何实现，仅在二阶段载荷内）",
      "shown_text_zh": "启动器首屏，实际渲染内容由加密载荷决定",
      "user_action_requested": "不可静态还原",
      "code_anchor": "AndroidManifest.xml <activity android:name=\"com.elevator.p045l\"> + res/values/styles.xml Theme.AppCompat.Transparent.NoActionBar"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "二阶段载荷内的引导页 → 系统设置 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "不可静态还原（主 DEX 中无 ACCESSIBILITY_SETTINGS 字符串与 startActivity 调用点）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "不可静态还原",
      "shown_text_zh": "预计为土耳其语引导文案，需 UTG 抓取",
      "user_action_requested": "不可静态还原",
      "code_anchor": "assets/yYnsu.json（加密二阶段载荷）"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "系统无障碍服务列表项：com.elevator.p024l（label=\"Chrome\"，description=\"Erişebilirlik Servisileri Etkinleştirme\"）",
      "trigger_event": "用户进入设置后，系统渲染该服务的名称与说明；应用侧可配合透明浮动 Activity 叠层",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Chrome / Erişebilirlik Servisileri Etkinleştirme",
      "shown_text_zh": "Chrome / 启用无障碍服务",
      "user_action_requested": "用户在该列表中点击「Chrome」并开启开关",
      "code_anchor": "AndroidManifest.xml <service android:name=\"com.elevator.p024l\" android:label=\"@7F030001\"> + xml/dyruxlcc.xml + res/values/strings.xml"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.elevator.p024l (AccessibilityService)：accessibilityEventTypes=0xFFFFFFFF、canRetrieveWindowContent=true、canPerformGestures=true、accessibilityFlags=0x53",
      "trigger_event": "服务被系统绑定后 onServiceConnected / onAccessibilityEvent（实现体在加密载荷内）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "不可静态还原",
      "shown_text_zh": "全事件监听 + 读屏 + 手势代点，具备自动点击与界面劫持能力",
      "user_action_requested": "不可静态还原",
      "code_anchor": "xml/dyruxlcc.xml（无障碍能力声明）+ assets/yYnsu.json（服务实现）"
    }
  ],
  "text_presentation_locations": [
    "系统「设置 → 无障碍 → 已下载的服务」列表项：服务名 \"Chrome\"（@string/a），下方说明文字 \"Erişebilirlik Servisileri Etkinleştirme\"（@7F030000 = strings.xml WIPEAYSSVi）——这是唯一可静态确认的引导文本落点",
    "桌面图标名：\"Chrome\"（@string/a，同时用于 activity label 与 device-admin receiver label）",
    "冷启动后的引导页/弹窗：位于加密二阶段 dex（assets/yYnsu.json 解密产物），明文资源中不存在任何引导文案、HTML 或 layout",
    "透明浮动 Activity（Theme.AppCompat.Transparent.NoActionBar，windowIsFloating/Translucent、backgroundDimEnabled=false）为潜在的叠层遮挡载体，但具体承载文本在载荷内",
    "无本地 assets/*.html 引导页、无 res/layout 引导布局、无 WebView 加载说明页（assets 目录仅有 Unity/广告 SDK 资源与图片）"
  ],
  "verbatim_texts": [
    {
      "lang": "tr",
      "text_verbatim": "Erişebilirlik Servisileri Etkinleştirme",
      "text_zh": "启用无障碍服务",
      "source_location": "res/values/strings.xml key=WIPEAYSSVi（被无障碍服务 meta-data android:description=@7F030000 引用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Chrome",
      "text_zh": "Chrome（谷歌浏览器）",
      "source_location": "res/values/strings.xml key=a（用于 application android:label、无障碍服务 android:label、device-admin receiver label 及启动 Activity label）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：明文代码中无 onResume 重跳、无 Timer、无 Settings 结果回调（无 startActivityForResult/isAccessibilityServiceEnabled），拒权循环逻辑位于加密二阶段 dex；仅可确认 BOOT_COMPLETED/USER_PRESENT/SCREEN_ON/PACKAGE_ADDED 等 13 个动作的高优先级（priority=999）广播接收器 com.elevator.p060d 为后台反复拉起提供通路。",
    "overlay_or_fake_settings": "未发现高仿系统无障碍开关页资源（无对应 layout/xml）；但存在透明浮动、无边框、无变暗的 Activity 主题与多个随机名无属性 Activity，为叠层遮挡/半透明引导窗预留了载体，实际叠层行为在载荷内不可静态还原。",
    "restricted_settings_13plus_coaching": "不可静态还原（minSdkVersion=26，若载荷内含 Android 13+ 受限设置教学文本，只存在于 yYnsu.json 解密产物中）",
    "post_grant_anti_removal": "不可静态还原；已确认配套反移除能力：BIND_DEVICE_ADMIN 接收器 com.elevator.p078p（USES_POLICY_FORCE_LOCK）、无障碍配置 accessibilityFlags=0x53 与 canPerformGestures=true（可模拟 GLOBAL_ACTION_BACK/HOME 及代点），但具体阻止撤权代码在载荷内。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以「进程启动即 hook Application.attachBaseContext 完成后的首个 Activity 上屏」为第一锚点，并以「Activity 启动 Intent 命中 android.settings.ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS」为第二锚点；由于跳转代码在二阶段 dex，需在 carcorn() 注入完成后（或直接在系统 settings 包被拉起瞬间）开始抓取。",
    "key_pages_to_capture": [
      {
        "page_role": "系统无障碍服务列表项（诱饵本体）",
        "page_identifier": "Settings$AccessibilitySettings 列表中 label 为「Chrome」、summary 为「Erişebilirlik Servisileri Etkinleştirme」的条目",
        "why_most_useful": "这是唯一可静态确认、且必然出现的诱导落点；服务名与品牌冒充、土耳其语说明在此同时暴露，可与 Manifest 声明一一对应",
        "observable_utg_signals": ["服务名文本 = Chrome", "说明文本 = Erişebilirlik Servisileri Etkinleştirme", "条目开关初始为关闭", "所在页包名 com.android.settings"]
      },
      {
        "page_role": "冷启动首屏 / 引导说明页（载荷内）",
        "page_identifier": "com.elevator.p045l 启动后的首个全屏窗口（无标题栏、非近期任务显示），或其后的透明浮动窗口",
        "why_most_useful": "捕获载荷解密后的真实引导文案与按钮集合，用于判断是否有取消/跳过、是否为恐吓或假更新话术",
        "observable_utg_signals": ["可见文本节点全量（土耳其语/英语）", "是否存在可点击的「取消/跳过/稍后」节点", "窗口是否 isFloating/半透明叠层", "是否存在 WebView 节点"]
      },
      {
        "page_role": "跳设置后压栈遮罩页 / 拒权返回页",
        "page_identifier": "从 settings 返回后 800ms 内重新出现的 Activity 或悬浮窗",
        "why_most_useful": "判定是否为 onResume 死循环重跳、是否叠加遮罩指引用户点击哪个位置",
        "observable_utg_signals": ["返回后 0-2s 内 Activity 栈变化次数", "是否存在覆盖在 settings 之上的半透明窗口", "是否有指向开关位置的箭头/高亮节点"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区为一阶段 Dropper 结构：APK 自身不含任何引导 UI，仅 Application 解密注入；若 UTG 在 carcorn 完成前采样或二阶段 dex 解密失败（设备 API/目录条件不满足），将只能看到空白/闪退，看不到引导页。此外 100 个 ZIP 条目被置加密标志位，静态工具易误判为「加密包」而放弃，实际数据明文可解。"
  },
  "behavior_pattern_tags": [
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH"
  ],
  "code_anchors": [
    "com.wreck.chef.Haveragestep#attachBaseContext",
    "com.wreck.chef.Haveragestep#roomreview",
    "com.wreck.chef.Qfrostwild#carcorn",
    "assets/yYnsu.json",
    "xml/dyruxlcc.xml",
    "res/values/strings.xml"
  ]
}
```

</details>
