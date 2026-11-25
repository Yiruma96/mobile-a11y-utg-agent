# MB_158__b4bd65520d｜Anubis — Android Update

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：216.7s

## 1. 一句话核心结论

- **核心申请方式**：启动即由 Application 解密 image/mediumcrop 并反射加载二阶段 DEX，无障碍服务与全部引导页面均在加密载荷内运行期构建，明文包内仅留伪装名 Android Update 与无说明的 Active Secure Service。
- **静态可见性说明**：APK 未使用商业壳，但采用一阶段 Dropper + 加密二阶段载荷：唯一 classes.dex 仅含 41 个混淆类（com.hatsdi.tiscpme / com.jegeqkhn.jegeqkhn），Manifest 声明的全部 com.kcyhit.tjdedz.* 组件（含无障碍服务 OgPmKURFy、LAUNCHER Activity VazLacq、短信/开机 receiver bdmZLEASRteL）在 DEX 中完全缺失；真实逻辑存于 APK 内 image/mediumcrop（188565 字节高熵密文，由 image/firstlist.txt 索引、4 个短随机串作配置分片），由 Application.onCreate 调用 izEMFNpwhrNV 解密并反射取 Class 加载。布局资源全为空壳、strings.xml 仅 actTest，故无障碍引导 UI 与跳转逻辑无法静态还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `b4bd65520d764bea63e2956f63cfe1e79109aa63efc39f3fd938e29df77cf0fd` |
| 包名 / 年份 | `com.kcyhit.tjdedz` / 2024 |
| 家族 / 品类 | **Anubis**（同池样本数：2） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Android Update |
| 引导页宣称品牌/身份 | 伪装为系统「Android 更新」组件；无障碍服务对外宣称「Active Secure Service」（安全服务），settingsActivity 仍残留模板值 com.example.root.myapplication.MainActivity |
| 系统无障碍列表服务名 | Active Secure Service |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：显示名为系统更新（Android Update）却无任何更新功能，包名 com.kcyhit.tjdedz 与真实 Application 类 com.hatsdi.tiscpme.rkAOtE 不一致；无障碍配置 android:description 完全缺失（系统列表无用途说明）；settingsActivity 指向不存在的 com.example.root.myapplication.MainActivity 模板类；组件名全随机化（OgPmKURFy/vfxtsmnymfkv/ukviwoxpegs 等），多 Activity 使用空 label + 69 字节 1x1 占位图标 luixbfsajat.png 隐藏于最近任务；主逻辑置于加密载荷以规避静态检测 |
| 无障碍服务类名 | `com.kcyhit.tjdedz.OgPmKURFy` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, PACKAGE_USAGE_STATS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.kcyhit.tjdedz.vfxtsmnymfkv.VazLacq（LAUNCHER Activity，类不在明文 DEX 中） | 用户点击桌面图标启动；进程启动时先执行 Application com.hatsdi.tiscpme.rkAOtE.onCreate | 不可静态还原 | 无 | 点击桌面「Android Update」图标 | `#1 manifest:components（activity vfxtsmnymfkv.VazLacq + MAIN/LAUNCHER）；res/values/strings.xml` |
| 2 | 冷启动入口 | com.hatsdi.tiscpme.rkAOtE（Application）→ com.hatsdi.tiscpme.izEMFNpwhrNV | Application.onCreate 无条件执行，构造 izEMFNpwhrNV 并调用 qxACAmGXDfo(Application)，再 qxACAmGXDfo() 取得 Class 进入初始化分支 | 不可静态还原 | 无 | 无（用户无感知） | `com.hatsdi.tiscpme.rkAOtE#onCreate → com.hatsdi.tiscpme.izEMFNpwhrNV#qxACAmGXDfo(android.app.Application)` |
| 3 | 业务功能触发 | 加密载荷 image/mediumcrop 解密后注册的全部 com.kcyhit.tjdedz.* 组件 | 由 image/firstlist.txt 索引 mediumcrop，经 qxACAmGXDfo(byte[]) 解密、qxACAmGXDfo() 反射加载类；随后 LAUNCHER Activity、开机/亮屏/PACKAGE_ADDED/SMS_RECEIVED 广播 receiver 生效 | 不可静态还原 | 无 | 不可静态还原 | `#1 file:unknown/image/firstlist.txt；#1 file:unknown/image/mediumcrop；com.hatsdi.tiscpme.izEMFNpwhrNV#qxACAmGXDfo(byte[])` |
| 4 | 跳无障碍设置 | 系统无障碍服务列表项「Active Secure Service」（com.kcyhit.tjdedz.OgPmKURFy） | 二阶段载荷内的引导逻辑（跳转点不可静态还原） | 系统无障碍页 | **原文**：Active Secure Service<br>**译注**：「活动安全服务」——仅此服务名，android:description 未设置，系统列表不显示任何用途说明 | 在系统无障碍列表中手动开启该服务（预期） | `#1 manifest:components（service OgPmKURFy，permission BIND_ACCESSIBILITY_SERVICE）；#1 file:res/xml/pjmjvpvbevy.xml` |
| 5 | 获权后动作 | 无障碍服务 OgPmKURFy（canRetrieveWindowContent=true、typeWindowContentChanged\|typeWindowStateChanged、flagIncludeNotImportantViews\|flagReportViewIds） | 服务被系统绑定后由 onAccessibilityEvent 接收窗口内容变化事件（实现体在加密载荷内） | 不可静态还原 | 无 | 无 | `#1 file:res/xml/pjmjvpvbevy.xml；#1 manifest:permissions` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表：服务名「Active Secure Service」（android:label，硬编码在 Manifest），无 android:description，因此无任何用途说明文字
- 桌面启动器：应用名「Android Update」（Manifest application android:label）
- 明文包内无任何引导文本载体：res/values/strings.xml 仅 1 条 actTest，15 个 res/layout/*.xml 均为 104 字节空壳，res/drawable/ndtmprlsq.jpg 为 0 字节
- 真正的引导弹窗/说明页/WebView/悬浮遮罩文案应位于 image/mediumcrop 解密后的二阶段载荷中，静态不可见（需动态脱壳）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Android Update | 安卓更新 | `AndroidManifest.xml application android:label（= 桌面显示名）` | 假更新 |
| en | Active Secure Service | 活动安全服务 | `AndroidManifest.xml service com.kcyhit.tjdedz.OgPmKURFy android:label` | 假反诈安全 |
| en | actTest | actTest（无意义占位字符串，仅为填充资源表） | `res/values/strings.xml <string name="opasxqflt">` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：拒绝/返回后的重跳逻辑（onResume 死循环、Timer 拉起或悬浮遮罩）位于 image/mediumcrop 解密后的二阶段载荷，明文 DEX 无 ACTION_ACCESSIBILITY_SETTINGS 调用点
- **遮罩叠层 / 高仿系统设置页**：不可静态还原：已具备 SYSTEM_ALERT_WINDOW 权限与 flagIncludeNotImportantViews 无障碍标志，具备叠加引导遮罩/高仿设置页的能力，但具体实现位于加密载荷内，静态无证据
- **Android 13+ 受限设置（Restricted Settings）应对**：无静态证据（targetSdkVersion=27，二阶段载荷内是否含 Android 13 受限设置教学无法确认）
- **获权后即时行为与防撤权机制**：不可静态还原；已具备 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 与 15 项广播（含 SCREEN_ON/USER_PRESENT）的自启常驻条件，撤权对抗实现不在明文包内
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在进程启动即拉起（Application.onCreate 触发载荷解密），因此最稳妥的 UTG 起抓时机是「点击桌面 Android Update 图标后 0–3 秒」，并在同一会话中持续抓取；同时监控 Intent 跳转 android.settings.ACCESSIBILITY_SETTINGS、android.settings.APPLICATION_DETAILS_SETTINGS、android.settings.action.MANAGE_OVERLAY_PERMISSION、ACTION_USAGE_ACCESS_SETTINGS，任一出现即立即 UTG 快照并连拍。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：主要盲区：一阶段 Dropper 明文包内无任何引导文本与设置跳转代码，全部话术与跳转点藏于 image/mediumcrop 加密载荷（需运行期脱壳才能静态取证）；若样本在检测环境判断为分析环境（模拟器/无 SIM/无目标银行 App），可能长时间不弹引导页，UTG 会看到空白或立即退出；另 res/drawable/ndtmprlsq.jpg 为 0 字节占位，图片诱饵须运行期由载荷下发，需 OCR 兜底。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗/说明页（载荷动态构建）** | 包名 com.kcyhit.tjdedz 下任意 Activity（LAUNCHER 为 vfxtsmnymfkv.VazLacq），theme 常为 Theme.Translucent.NoTitleBar / Theme.NoDisplay，文本由二阶段 DEX 动态生成 | 这是判断是否为恶意诱导的唯一入口：明文包无任何引导文案，全部话术只在运行期出现 | 弹窗/页面内是否存在「更新」「安全」「故障」等诱导词；是否存在取消/跳过按钮（无取消即强制型）；是否出现「无障碍」「辅助功能」「授权」等关键词；Activity 类名是否为随机混淆串（vfxtsmnymfkv.*） |
| **跳转前教学/说明页（Dialog 或 WebView）** | 覆盖全屏的 Dialog 或 WebView，内容含步骤 1/2/3 图文指引 | 该页直接给出「打开设置→无障碍→Active Secure Service→开启」的教唆文本，是诱导链最核心证据 | 是否出现「设置」「无障碍」「辅助功能」「开启」等分步指引文本；是否含图片/GIF 指引（needs_ocr）；WebView 加载的是 file:///android_asset 本地页还是远端 URL（看地址栏/网络流量） |
| **系统无障碍服务列表项** | com.android.settings 的 AccessibilitySettings 页面，列表项文本 Active Secure Service | 核对伪装名与无说明状态，并观察是否被自动点击/被遮罩覆盖 | 列表项名称 Active Secure Service；该项下方无任何用途说明文字；是否有悬浮窗覆盖在系统页之上；开关是否被无障碍自身点击自动打开 |
| **设置页返回后的反馈页** | 回到应用 Activity 或悬浮遮罩，常见重跳系统设置或提示「未开启」 | 用于确认拒绝循环机制与遮罩压栈行为（静态不可见） | 返回后是否在 1–3 秒内再次跳转设置；是否出现半透明遮罩+手指指引动画；是否出现倒计时/强制按钮 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.hatsdi.tiscpme.rkAOtE#onCreate`
- `com.hatsdi.tiscpme.izEMFNpwhrNV#qxACAmGXDfo(android.app.Application)`
- `com.hatsdi.tiscpme.izEMFNpwhrNV#qxACAmGXDfo(byte[])`
- `com.hatsdi.tiscpme.izEMFNpwhrNV#qxACAmGXDfo()`
- `#1 file:unknown/image/firstlist.txt`
- `#1 file:res/xml/pjmjvpvbevy.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，14 次工具调用收口）

**核心发现：无障碍引导流程在静态层面不可还原，属于“加密二阶段载荷”结构，而不是加壳。**

1. **Manifest 与 DEX 严重不匹配**：Manifest 声明 30 余个 `com.kcyhit.tjdedz.*` 组件（含无障碍服务 `com.kcyhit.tjdedz.OgPmKURFy`，label `Active Secure Service`、`settingsActivity` 指向模板残留 `com.example.root.myapplication.MainActivity`、**无 `android:description`**），但唯一 `classes.dex` 只有 41 个混淆类（`com.hatsdi.tiscpme` / `com.jegeqkhn.jegeqkhn`），`strings` 中检索不到任何 `kcyhit`、`OgPmKURFy`、`vfxtsmnymfkv` 符号。
2. **Application 启动即解密加载**：[rkAOtE.onCreate()](<resource-unit:#1.dex1 code:com.hatsdi.tiscpme.rkAOtE#onCreate>) 立即调用 `izEMFNpwhrNV.qxACAmGXDfo(Application)`，随后 `qxACAmGXDfo()` 返回 `Class` 并进入后续初始化 —— 即“一阶段 Dropper 反射加载二阶段 DEX”。
3. **加密载荷确证**：APK 内 `image/firstlist.txt` 仅一行 `image/mediumcrop`；`mediumcrop` 为 188565 字节高熵数据（首字节 `91 e0 02 00`，无任何可读字符串）；另 4 个 36–43 字节随机字母串文件为密钥/配置分片。解密与读取链为 `qxACAmGXDfo(byte[])`、`qxACAmGXDfo(InputStream, boolean)`，方法体经控制流平坦化，并伪造 API 名（`flushdata`、`enumElements`）。
4. **UI 全部由载荷动态构建**：`res/layout/*.xml` 全为 104 字节空壳，`strings.xml` 仅 `actTest` 一条，`drawable/ndtmprlsq.jpg` 为 0 字节 —— 引导弹窗、说明页、WebView 与跳转 `ACTION_ACCESSIBILITY_SETTINGS` 的代码点均不在明文包内。
5. **可确认的触发入口**：LAUNCHER Activity `vfxtsmnymfkv.VazLacq` 与 15 个广播的 receiver `ukviwoxpegs.bdmZLEASRteL`（`BOOT_COMPLETED`/`USER_PRESENT`/`SCREEN_ON`/`PACKAGE_ADDED`/`SMS_RECEIVED`）都落在缺失类集合内，由载荷运行期注册；无障碍能力与短信投递接管（`SMS_DELIVER`/`WAP_PUSH_DELIVER`）、`PACKAGE_USAGE_STATS`、`SYSTEM_ALERT_WINDOW`、`REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` 共同构成 Anubis 家族典型的银行木马高危能力面。

已登记风险 [R-001](<resource-unit:#1 manifest:components>)（malware_trojan / high），证据边界为：`mediumcrop` 解密算法与二阶段 DEX 的引导文案、跳转点、拒绝循环、遮罩层未还原。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "APK 未使用商业壳，但采用一阶段 Dropper + 加密二阶段载荷：唯一 classes.dex 仅含 41 个混淆类（com.hatsdi.tiscpme / com.jegeqkhn.jegeqkhn），Manifest 声明的全部 com.kcyhit.tjdedz.* 组件（含无障碍服务 OgPmKURFy、LAUNCHER Activity VazLacq、短信/开机 receiver bdmZLEASRteL）在 DEX 中完全缺失；真实逻辑存于 APK 内 image/mediumcrop（188565 字节高熵密文，由 image/firstlist.txt 索引、4 个短随机串作配置分片），由 Application.onCreate 调用 izEMFNpwhrNV 解密并反射取 Class 加载。布局资源全为空壳、strings.xml 仅 actTest，故无障碍引导 UI 与跳转逻辑无法静态还原。",
  "summary_one_liner": "启动即由 Application 解密 image/mediumcrop 并反射加载二阶段 DEX，无障碍服务与全部引导页面均在加密载荷内运行期构建，明文包内仅留伪装名 Android Update 与无说明的 Active Secure Service。",
  "disguise_identity": {
    "app_display_name": "Android Update",
    "claimed_brand_or_persona": "伪装为系统「Android 更新」组件；无障碍服务对外宣称「Active Secure Service」（安全服务），settingsActivity 仍残留模板值 com.example.root.myapplication.MainActivity",
    "a11y_service_label": "Active Secure Service",
    "identity_mismatch": true,
    "obfuscation_tricks": "显示名为系统更新（Android Update）却无任何更新功能，包名 com.kcyhit.tjdedz 与真实 Application 类 com.hatsdi.tiscpme.rkAOtE 不一致；无障碍配置 android:description 完全缺失（系统列表无用途说明）；settingsActivity 指向不存在的 com.example.root.myapplication.MainActivity 模板类；组件名全随机化（OgPmKURFy/vfxtsmnymfkv/ukviwoxpegs 等），多 Activity 使用空 label + 69 字节 1x1 占位图标 luixbfsajat.png 隐藏于最近任务；主逻辑置于加密载荷以规避静态检测"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.kcyhit.tjdedz.vfxtsmnymfkv.VazLacq（LAUNCHER Activity，类不在明文 DEX 中）",
      "trigger_event": "用户点击桌面图标启动；进程启动时先执行 Application com.hatsdi.tiscpme.rkAOtE.onCreate",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "明文包内无该 Activity 的任何布局或文案；res/layout 全部为 104 字节空壳，strings.xml 仅 actTest",
      "user_action_requested": "点击桌面「Android Update」图标",
      "code_anchor": "#1 manifest:components（activity vfxtsmnymfkv.VazLacq + MAIN/LAUNCHER）；res/values/strings.xml"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "com.hatsdi.tiscpme.rkAOtE（Application）→ com.hatsdi.tiscpme.izEMFNpwhrNV",
      "trigger_event": "Application.onCreate 无条件执行，构造 izEMFNpwhrNV 并调用 qxACAmGXDfo(Application)，再 qxACAmGXDfo() 取得 Class 进入初始化分支",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面；此步为载荷解密装载，程序启动即完成二阶段注入",
      "user_action_requested": "无（用户无感知）",
      "code_anchor": "com.hatsdi.tiscpme.rkAOtE#onCreate → com.hatsdi.tiscpme.izEMFNpwhrNV#qxACAmGXDfo(android.app.Application)"
    },
    {
      "step": 3,
      "stage": "业务功能触发",
      "screen_or_component": "加密载荷 image/mediumcrop 解密后注册的全部 com.kcyhit.tjdedz.* 组件",
      "trigger_event": "由 image/firstlist.txt 索引 mediumcrop，经 qxACAmGXDfo(byte[]) 解密、qxACAmGXDfo() 反射加载类；随后 LAUNCHER Activity、开机/亮屏/PACKAGE_ADDED/SMS_RECEIVED 广播 receiver 生效",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "二阶段 DEX 未还原，其界面与文案未知",
      "user_action_requested": "不可静态还原",
      "code_anchor": "#1 file:unknown/image/firstlist.txt；#1 file:unknown/image/mediumcrop；com.hatsdi.tiscpme.izEMFNpwhrNV#qxACAmGXDfo(byte[])"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍服务列表项「Active Secure Service」（com.kcyhit.tjdedz.OgPmKURFy）",
      "trigger_event": "二阶段载荷内的引导逻辑（跳转点不可静态还原）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Active Secure Service",
      "shown_text_zh": "「活动安全服务」——仅此服务名，android:description 未设置，系统列表不显示任何用途说明",
      "user_action_requested": "在系统无障碍列表中手动开启该服务（预期）",
      "code_anchor": "#1 manifest:components（service OgPmKURFy，permission BIND_ACCESSIBILITY_SERVICE）；#1 file:res/xml/pjmjvpvbevy.xml"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "无障碍服务 OgPmKURFy（canRetrieveWindowContent=true、typeWindowContentChanged|typeWindowStateChanged、flagIncludeNotImportantViews|flagReportViewIds）",
      "trigger_event": "服务被系统绑定后由 onAccessibilityEvent 接收窗口内容变化事件（实现体在加密载荷内）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "可读取全部窗口内容与控件 ID，配合短信投递接管、悬浮窗与用量统计构成窃取/远控能力",
      "user_action_requested": "无",
      "code_anchor": "#1 file:res/xml/pjmjvpvbevy.xml；#1 manifest:permissions"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表：服务名「Active Secure Service」（android:label，硬编码在 Manifest），无 android:description，因此无任何用途说明文字",
    "桌面启动器：应用名「Android Update」（Manifest application android:label）",
    "明文包内无任何引导文本载体：res/values/strings.xml 仅 1 条 actTest，15 个 res/layout/*.xml 均为 104 字节空壳，res/drawable/ndtmprlsq.jpg 为 0 字节",
    "真正的引导弹窗/说明页/WebView/悬浮遮罩文案应位于 image/mediumcrop 解密后的二阶段载荷中，静态不可见（需动态脱壳）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Android Update",
      "text_zh": "安卓更新",
      "source_location": "AndroidManifest.xml application android:label（= 桌面显示名）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Active Secure Service",
      "text_zh": "活动安全服务",
      "source_location": "AndroidManifest.xml service com.kcyhit.tjdedz.OgPmKURFy android:label",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "actTest",
      "text_zh": "actTest（无意义占位字符串，仅为填充资源表）",
      "source_location": "res/values/strings.xml <string name=\"opasxqflt\">",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：拒绝/返回后的重跳逻辑（onResume 死循环、Timer 拉起或悬浮遮罩）位于 image/mediumcrop 解密后的二阶段载荷，明文 DEX 无 ACTION_ACCESSIBILITY_SETTINGS 调用点",
    "overlay_or_fake_settings": "不可静态还原：已具备 SYSTEM_ALERT_WINDOW 权限与 flagIncludeNotImportantViews 无障碍标志，具备叠加引导遮罩/高仿设置页的能力，但具体实现位于加密载荷内，静态无证据",
    "restricted_settings_13plus_coaching": "无静态证据（targetSdkVersion=27，二阶段载荷内是否含 Android 13 受限设置教学无法确认）",
    "post_grant_anti_removal": "不可静态还原；已具备 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 与 15 项广播（含 SCREEN_ON/USER_PRESENT）的自启常驻条件，撤权对抗实现不在明文包内",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在进程启动即拉起（Application.onCreate 触发载荷解密），因此最稳妥的 UTG 起抓时机是「点击桌面 Android Update 图标后 0–3 秒」，并在同一会话中持续抓取；同时监控 Intent 跳转 android.settings.ACCESSIBILITY_SETTINGS、android.settings.APPLICATION_DETAILS_SETTINGS、android.settings.action.MANAGE_OVERLAY_PERMISSION、ACTION_USAGE_ACCESS_SETTINGS，任一出现即立即 UTG 快照并连拍。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗/说明页（载荷动态构建）",
        "page_identifier": "包名 com.kcyhit.tjdedz 下任意 Activity（LAUNCHER 为 vfxtsmnymfkv.VazLacq），theme 常为 Theme.Translucent.NoTitleBar / Theme.NoDisplay，文本由二阶段 DEX 动态生成",
        "why_most_useful": "这是判断是否为恶意诱导的唯一入口：明文包无任何引导文案，全部话术只在运行期出现",
        "observable_utg_signals": ["弹窗/页面内是否存在「更新」「安全」「故障」等诱导词", "是否存在取消/跳过按钮（无取消即强制型）", "是否出现「无障碍」「辅助功能」「授权」等关键词", "Activity 类名是否为随机混淆串（vfxtsmnymfkv.*）"]
      },
      {
        "page_role": "跳转前教学/说明页（Dialog 或 WebView）",
        "page_identifier": "覆盖全屏的 Dialog 或 WebView，内容含步骤 1/2/3 图文指引",
        "why_most_useful": "该页直接给出「打开设置→无障碍→Active Secure Service→开启」的教唆文本，是诱导链最核心证据",
        "observable_utg_signals": ["是否出现「设置」「无障碍」「辅助功能」「开启」等分步指引文本", "是否含图片/GIF 指引（needs_ocr）", "WebView 加载的是 file:///android_asset 本地页还是远端 URL（看地址栏/网络流量）"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 的 AccessibilitySettings 页面，列表项文本 Active Secure Service",
        "why_most_useful": "核对伪装名与无说明状态，并观察是否被自动点击/被遮罩覆盖",
        "observable_utg_signals": ["列表项名称 Active Secure Service", "该项下方无任何用途说明文字", "是否有悬浮窗覆盖在系统页之上", "开关是否被无障碍自身点击自动打开"]
      },
      {
        "page_role": "设置页返回后的反馈页",
        "page_identifier": "回到应用 Activity 或悬浮遮罩，常见重跳系统设置或提示「未开启」",
        "why_most_useful": "用于确认拒绝循环机制与遮罩压栈行为（静态不可见）",
        "observable_utg_signals": ["返回后是否在 1–3 秒内再次跳转设置", "是否出现半透明遮罩+手指指引动画", "是否出现倒计时/强制按钮"]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "主要盲区：一阶段 Dropper 明文包内无任何引导文本与设置跳转代码，全部话术与跳转点藏于 image/mediumcrop 加密载荷（需运行期脱壳才能静态取证）；若样本在检测环境判断为分析环境（模拟器/无 SIM/无目标银行 App），可能长时间不弹引导页，UTG 会看到空白或立即退出；另 res/drawable/ndtmprlsq.jpg 为 0 字节占位，图片诱饵须运行期由载荷下发，需 OCR 兜底。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.hatsdi.tiscpme.rkAOtE#onCreate",
    "com.hatsdi.tiscpme.izEMFNpwhrNV#qxACAmGXDfo(android.app.Application)",
    "com.hatsdi.tiscpme.izEMFNpwhrNV#qxACAmGXDfo(byte[])",
    "com.hatsdi.tiscpme.izEMFNpwhrNV#qxACAmGXDfo()",
    "#1 file:unknown/image/firstlist.txt",
    "#1 file:res/xml/pjmjvpvbevy.xml"
  ]
}
```

</details>
