# MB_060__9dcd3f15b7｜GoldDigger — Identitas Kependudukan Digital

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：132.0s

## 1. 一句话核心结论

- **核心申请方式**：该样本以印尼官方政务身份应用「Identitas Kependudukan Digital」为外壳，用壳+加密资产隐藏真实代码，无障碍服务同样冒用该品牌名并自声明 isAccessibilityTool=true，配合 Splash→CheckPermission→TransplentPermission→Activation 的假激活流程诱导用户开启无障碍，随后由录屏/录音/摄像头/LiveKit 服务链回传数据。
- **静态可见性说明**：classes.dex 仅为 DPT/nashsiqiu 壳（6 个类：ProxyApplication/JniBridge/ProxyComponentFactory），真实业务代码以自定义加密资产 assets/OoooooOooo（2.5MB，魔数 01 00 02 00）配合 libdpt.so 运行期解密；ACCESSIBILITY_SETTINGS/APPLICATION_DETAILS_SETTINGS/FocusService 在壳 DEX 中零命中。无障碍引导的弹窗文案、WebView/HTML、悬浮遮罩与页面流转均位于加密二阶段载荷内，仅 Manifest 组件声明、无障碍标签/描述、无障碍配置属性与字符串资源名静态可证。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`ID_FAKE_IS_ACCESSIBILITY_TOOL`（伪造android:isAccessibilityTool="true"）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `9dcd3f15b7212de5b1163404fee57ea292abd0bb5992c7ba2b054fe384a2b93b` |
| 包名 / 年份 | `com.udadwn.dnfenu.jjmck.dismo` / 2025 |
| 家族 / 品类 | **GoldDigger**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Identitas Kependudukan Digital |
| 引导页宣称品牌/身份 | 印尼政府数字人口身份应用 Identitas Kependudukan Digital（官方电子身份证/IKD） |
| 系统无障碍列表服务名 | Identitas Kependudukan Digital |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名 com.udadwn.dnfenu.jjmck.dismo 与品牌完全无关；类名/包名混淆为三串 32 位十六进制（cb310a0d…、c67f205d…、c015e644…）；AndroidManifest 中无障碍配置显式声明 isAccessibilityTool=true 以伪装成合规无障碍工具并压制系统敏感数据访问警告；多个 activity-alias（AliasActivity/AliasGoogleActivity/AliasTmpActivity）用于入口与图标伪装；assets/app_acf 伪造 androidx.core.app.CoreComponentFactory 劫持组件工厂 |
| 无障碍服务类名 | `cb310a0da268140999ff21e12d8f2afef.c67f205dae8ec47999791d07a0b0def2d.c015e6446b3c348d695474a9ef074f2c6.service.FocusService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=True` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Identitas Kependudukan Digital |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | cb310a0d…c6.ui.SplashActivity（壳 ProxyApplication 先加载 assets/OoooooOooo 解密二阶段） | launcher 启动 / Application.onCreate 触发壳解密装载 | 原生Activity | 无 | 无（自动进入下一步） | `AndroidManifest.xml 组件声明 SplashActivity；com.nashsiqiu.shell.ProxyApplication` |
| 2 | 引导说明页 | cb310a0d…c6.ui.CheckPermissionActivity | SplashActivity 完成后跳转（预期在 onCreate/onResume 检查权限状态） | 不可静态还原 | **原文**：无（载荷加密，文案不可静态读取）<br>**译注**：权限引导/检查页，用于逐项要求通讯录、短信、相机、录音、悬浮窗、无障碍等权限 | 不可静态还原（组件名表明为权限检查驱动，未见取消按钮证据） | `cb310a0da268140999ff21e12d8f2afef.c67f205dae8ec47999791d07a0b0def2d.c015e6446b3c348d695474a9ef074f2c6.ui.CheckPermissionActivity` |
| 3 | 跳无障碍设置 | 系统设置页 Settings.ACTION_ACCESSIBILITY_SETTINGS（由加密载荷内代码发起） | 用户点击“激活/开启服务”类按钮后 startActivity(ACTION_ACCESSIBILITY_SETTINGS) | 系统无障碍页 | **原文**：Accessibility service description / Identitas Kependudukan Digital<br>**译注**：系统无障碍列表中显示的服务名与说明均为「Identitas Kependudukan Digital」，用户需在该列表中找到并打开同名开关 | 在系统无障碍列表中手动找到并开启同名服务开关 | `res/values/arrays.xml/touch_accessibility_service_config.xml（description/label 资源）；跳转代码位于加密载荷` |
| 4 | 遮罩叠层指引 | cb310a0d…c6.ui.TransplentPermissionActivity（透明权限 Activity，配合 SYSTEM_ALERT_WINDOW） | 从系统无障碍设置返回后重新拉起（预期 onResume 或悬浮窗按钮） | 悬浮窗Overlay | **原文**：无（载荷加密，不可静态读取）<br>**译注**：半透明/透明页覆盖在设置界面之上，提供“点这里开启”式叠层指引，需动态采集才能获得原文 | 不可静态还原 | `cb310a0d…c6.ui.TransplentPermissionActivity；权限 android.permission.SYSTEM_ALERT_WINDOW / SYSTEM_OVERLAY_WINDOW` |
| 5 | 获权后动作 | ActivationActivity → WaitCheckActivity → LoginActivity / FaceActivity / UploadIDPhotosActivity / SettingSafePwdActivity；FocusService + record.CameraService/AudioService/ScreenRecordService/LiveKitService | 检测到无障碍服务已启用后进入“激活”流程 | 不可静态还原 | **原文**：无（载荷加密）<br>**译注**：以“等待审核/人脸核验/上传身份证照片/设置安全密码”的假政务流程继续索取身份与生物特征，同时后台具备录屏、录音、摄像头与 LiveKit 实时回传能力 | 上传身份证照片、进行人脸采集、设置查询与安全密码 | `cb310a0d…c6.ui.ActivationActivity / WaitCheckActivity / FaceActivity / UploadIDPhotosActivity / SettingSafePwdActivity；cb310a0d…c6.record.ScreenRecordService / CameraService / AudioService / LiveKitService` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍列表项：android:label 与 android:description 均为「Identitas Kependudukan Digital」（resources.arsc 中可确证）
- 无障碍服务配置 res/values/arrays.xml/touch_accessibility_service_config.xml：description 指向上述字符串，并声明 isAccessibilityTool=true / canRetrieveWindowContent / canPerformGestures
- 应用内引导弹窗与说明文字：位于加密资产 assets/OoooooOooo 解密后的二阶段代码（含 CheckPermissionActivity / TransplentPermissionActivity），静态不可见
- 预筛命中的权限失败文案（如「获取权限失败，继续保存图片」「获取系统相机权限被拒绝」「获取系统录音权限被拒绝」）位于加密载荷或壳内资源，本次静态未能定位到明文载体
- 可能存在的远端 WebView 引导页：未获静态证据，需运行期抓包确认

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| id | Identitas Kependudukan Digital | 数字人口身份（印尼官方电子身份证应用名） | `resources.arsc 中 android:label / android:description（无障碍服务 FocusService）` | 假反诈安全 |
| en | Accessibility service description | 无障碍服务说明 | `resources.arsc（无障碍服务描述默认串）` | 未知 |
| zh | 获取权限失败，继续保存图片 | 获取权限失败，继续保存图片 | `预筛字符串（静态未定位到明文载体，疑在加密载荷/壳资源）` | 未知 |
| zh | 获取系统相机权限被拒绝 | 获取系统相机权限被拒绝 | `预筛字符串（静态未定位到明文载体）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：壳+加密载荷隐藏跳转与回调逻辑；Manifest 中存在 TransplentPermissionActivity（透明页）与 WaitCheckActivity，配合 onResume 重拉/悬浮窗按钮的死循环重跳高度可疑，需动态验证
- **遮罩叠层 / 高仿系统设置页**：存在叠层条件：声明 SYSTEM_ALERT_WINDOW 与 SYSTEM_OVERLAY_WINDOW 权限，并含 TransplentPermissionActivity（透明 Activity），具备在系统设置页上叠加半透明指引层的能力；是否为高仿无障碍开关页需动态确认
- **Android 13+ 受限设置（Restricted Settings）应对**：不可静态还原（Android 13+ 受限设置/应用详情页教学文案位于加密载荷内，未获静态证据）
- **获权后即时行为与防撤权机制**：不可静态还原：存在 asd.kkalive.com.daemon.* 守护进程、OnePxActivity 与多个 JobService，具备反撤权/保活基础能力，但未见 GLOBAL_ACTION_BACK/HOME 阻止撤权的静态证据
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 CheckPermissionActivity 或 TransplentPermissionActivity 启动、或窗口出现 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 跳转的瞬间立即拉起 UTG；另在从系统无障碍页返回前台后 800ms 内再次抓取，捕捉重新压栈的引导页或遮罩层
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：显著盲区：核心引导逻辑与全部引导文案封装在加密资产 assets/OoooooOooo（自定义魔数，配合 libdpt.so 运行期解密）中，静态只能确认无障碍服务声明、品牌冒用标签与 isAccessibilityTool=true；若运行期引导采用纯图片/纯视频（无文本节点）或仅通过远端 WebView 下发 HTML，则 UTG 文本抽取会失效，需 OCR 与流量抓包补证。注意静态加壳不阻挡运行期 UTG 采集。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页 / 权限检查页** | 包名 com.udadwn.dnfenu.jjmck.dismo 下 CheckPermissionActivity 窗口，含权限清单与“激活/开启”主按钮 | 该页是引导链起点，可直接读到诱导文案原文与是否存在取消/跳过入口 | 窗口类名含 CheckPermissionActivity；权限条目文本（通讯录/短信/相机/录音/无障碍）；是否存在“取消/稍后/跳过”可点击节点；主按钮文案（激活/立即开启） |
| **跳转前无障碍教学页 / 叠层指引** | TransplentPermissionActivity 透明窗口或 TYPE_APPLICATION_OVERLAY 悬浮窗，覆盖在系统设置之上 | 区分“良性说明”与“遮罩式诱导开启”最关键，且能捕获伪造开关页/手指指引图 | 窗口是否透明/半透明且覆盖 Settings；是否出现仿系统开关控件或手指引导图；文案是否含“点这里开启/必须开启”强制语；是否遮挡真实系统开关导致误点 |
| **系统无障碍服务列表项** | com.android.settings 无障碍页中 label 为 Identitas Kependudukan Digital 的条目 | 核对服务名冒用与 Android 13+ 是否因 isAccessibilityTool=true 而未显示敏感数据警告 | 条目名称 Identitas Kependudukan Digital；是否出现“可查看敏感数据/可执行手势”警告文本；开关状态变化时间点 |
| **获权后假政务流程页** | ActivationActivity / WaitCheckActivity / UploadIDPhotosActivity / FaceActivity | 确认获权后立即转入身份与生物特征采集，佐证无障碍权限的真实目的 | “等待审核/激活”文案；身份证上传与人脸采集界面元素；设置查询密码/安全密码输入框 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `cb310a0da268140999ff21e12d8f2afef.c67f205dae8ec47999791d07a0b0def2d.c015e6446b3c348d695474a9ef074f2c6.service.FocusService`
- `cb310a0da268140999ff21e12d8f2afef.c67f205dae8ec47999791d07a0b0def2d.c015e6446b3c348d695474a9ef074f2c6.ui.CheckPermissionActivity`
- `cb310a0da268140999ff21e12d8f2afef.c67f205dae8ec47999791d07a0b0def2d.c015e6446b3c348d695474a9ef074f2c6.ui.TransplentPermissionActivity`
- `res/values/arrays.xml/touch_accessibility_service_config.xml`
- `com.nashsiqiu.shell.ProxyApplication / assets/OoooooOooo（加密二阶段载荷）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（要点）

**静态可见性：加壳/加密，核心引导逻辑无法静态还原**

- `classes.dex`（5.2 MB）经核实只是**壳**，仅 6 个类：`com.nashsiqiu.shell.ProxyApplication`、`JniBridge`、`ProxyComponentFactory`，另有 `a.a`、`b.a` 与 `com.nash.dpt.MainActivity` 桩。真实业务代码（含 `...service.FocusService` 无障碍服务、引导弹窗/WebView）不在其中，`ACCESSIBILITY_SETTINGS`、`APPLICATION_DETAILS_SETTINGS`、`isAccessibilityTool`、`FocusService` 在该 DEX 中**零命中**。
- 真实载荷位于 `assets/OoooooOooo`（2.5 MB，自定义魔数 `01 00 02 00`，字符串区高熵、无明文），配合 `assets/vwwwwwvwww/{arm,arm64,x86,x86_64}/libdpt.so`（DPT 壳 native）在运行期解密；`assets/app_name` 给出动态应用类名 `cb310a0d….App`，`assets/app_acf` 给出伪造的 `CoreComponentFactory`，均属典型二阶段装载。
- 因此“用户如何一步步被引导开启无障碍”的**页面流转、弹窗文案、WebView/悬浮窗载体**全部位于加密载荷内，静态不可见；以下仅为 Manifest/资源层可确证的部分。

**Manifest/资源层可确证事实**

1. 无障碍服务真实声明存在：[FocusService](<resource-unit:#1 manifest:components>)（`cb310a0d…c6.service.FocusService`，`BIND_ACCESSIBILITY_SERVICE`），系统无障碍列表标签与 `android:description` 均为 **`Identitas Kependudukan Digital`**（印尼官方“数字人口身份”应用品牌），属**政府/系统身份冒充**；`res/values/arrays.xml/touch_accessibility_service_config.xml` 中 `canRetrieveWindowContent`、`canPerformGestures`、`canRequestEnhancedWebAccessibility`、`isAccessibilityTool` 均置为开启——`isAccessibilityTool=true` 是常被恶意样本用来在 Android 13+ 无障碍列表中压制“此服务可查看敏感数据”警告的自我声明。
2. 引导链的 Activity 命名直接暴露流程骨架：`SplashActivity` → `CheckPermissionActivity` → `TransplentPermissionActivity`（透明权限页）→ `ActivationActivity` → `WaitCheckActivity` → `LoginActivity` / `FaceActivity` / `UploadIDPhotosActivity` / `SettingSafePwdActivity`（“激活—等待审核—人脸—上传身份证照片—设置密码”的完整假政务身份流程）。
3. 采集能力服务群：`record.AudioService`、`record.CameraService`、`record.ScreenRecordService`、`record.DisplayService`、`record.LiveKitService` —— 与 LiveKit 实时音视频组合，具备录屏/录音/摄像头实时回传条件（GoldDigger 家族典型特征）。
4. 反移除/保活：`asd.kkalive.com.daemon.*`（DaemonService、PowerService、OnePxActivity、ScheduledService）、`asd.fgh.component.*` 与多个 `activity-alias`（`AliasActivity`/`AliasGoogleActivity`/`AliasTmpActivity`）用于图标与入口伪装、进程守护。

**UTG 视角的落地建议**：在 `CheckPermissionActivity`/`TransplentPermissionActivity` 启动或检测到 `ACTION_ACCESSIBILITY_SETTINGS` 跳转的瞬间拉起 UTG，优先抓“跳转前引导页”和“返回后重新压栈的透明权限页/遮罩页”，这两类页面对区分“良性说明”与“诱导开启”最具判别力。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "classes.dex 仅为 DPT/nashsiqiu 壳（6 个类：ProxyApplication/JniBridge/ProxyComponentFactory），真实业务代码以自定义加密资产 assets/OoooooOooo（2.5MB，魔数 01 00 02 00）配合 libdpt.so 运行期解密；ACCESSIBILITY_SETTINGS/APPLICATION_DETAILS_SETTINGS/FocusService 在壳 DEX 中零命中。无障碍引导的弹窗文案、WebView/HTML、悬浮遮罩与页面流转均位于加密二阶段载荷内，仅 Manifest 组件声明、无障碍标签/描述、无障碍配置属性与字符串资源名静态可证。",
  "summary_one_liner": "该样本以印尼官方政务身份应用「Identitas Kependudukan Digital」为外壳，用壳+加密资产隐藏真实代码，无障碍服务同样冒用该品牌名并自声明 isAccessibilityTool=true，配合 Splash→CheckPermission→TransplentPermission→Activation 的假激活流程诱导用户开启无障碍，随后由录屏/录音/摄像头/LiveKit 服务链回传数据。",
  "disguise_identity": {
    "app_display_name": "Identitas Kependudukan Digital",
    "claimed_brand_or_persona": "印尼政府数字人口身份应用 Identitas Kependudukan Digital（官方电子身份证/IKD）",
    "a11y_service_label": "Identitas Kependudukan Digital",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名 com.udadwn.dnfenu.jjmck.dismo 与品牌完全无关；类名/包名混淆为三串 32 位十六进制（cb310a0d…、c67f205d…、c015e644…）；AndroidManifest 中无障碍配置显式声明 isAccessibilityTool=true 以伪装成合规无障碍工具并压制系统敏感数据访问警告；多个 activity-alias（AliasActivity/AliasGoogleActivity/AliasTmpActivity）用于入口与图标伪装；assets/app_acf 伪造 androidx.core.app.CoreComponentFactory 劫持组件工厂"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "cb310a0d…c6.ui.SplashActivity（壳 ProxyApplication 先加载 assets/OoooooOooo 解密二阶段）",
      "trigger_event": "launcher 启动 / Application.onCreate 触发壳解密装载",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "启动页，具体界面内容位于加密载荷内不可静态还原",
      "user_action_requested": "无（自动进入下一步）",
      "code_anchor": "AndroidManifest.xml 组件声明 SplashActivity；com.nashsiqiu.shell.ProxyApplication"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "cb310a0d…c6.ui.CheckPermissionActivity",
      "trigger_event": "SplashActivity 完成后跳转（预期在 onCreate/onResume 检查权限状态）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（载荷加密，文案不可静态读取）",
      "shown_text_zh": "权限引导/检查页，用于逐项要求通讯录、短信、相机、录音、悬浮窗、无障碍等权限",
      "user_action_requested": "不可静态还原（组件名表明为权限检查驱动，未见取消按钮证据）",
      "code_anchor": "cb310a0da268140999ff21e12d8f2afef.c67f205dae8ec47999791d07a0b0def2d.c015e6446b3c348d695474a9ef074f2c6.ui.CheckPermissionActivity"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 Settings.ACTION_ACCESSIBILITY_SETTINGS（由加密载荷内代码发起）",
      "trigger_event": "用户点击“激活/开启服务”类按钮后 startActivity(ACTION_ACCESSIBILITY_SETTINGS)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Accessibility service description / Identitas Kependudukan Digital",
      "shown_text_zh": "系统无障碍列表中显示的服务名与说明均为「Identitas Kependudukan Digital」，用户需在该列表中找到并打开同名开关",
      "user_action_requested": "在系统无障碍列表中手动找到并开启同名服务开关",
      "code_anchor": "res/values/arrays.xml/touch_accessibility_service_config.xml（description/label 资源）；跳转代码位于加密载荷"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "cb310a0d…c6.ui.TransplentPermissionActivity（透明权限 Activity，配合 SYSTEM_ALERT_WINDOW）",
      "trigger_event": "从系统无障碍设置返回后重新拉起（预期 onResume 或悬浮窗按钮）",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无（载荷加密，不可静态读取）",
      "shown_text_zh": "半透明/透明页覆盖在设置界面之上，提供“点这里开启”式叠层指引，需动态采集才能获得原文",
      "user_action_requested": "不可静态还原",
      "code_anchor": "cb310a0d…c6.ui.TransplentPermissionActivity；权限 android.permission.SYSTEM_ALERT_WINDOW / SYSTEM_OVERLAY_WINDOW"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "ActivationActivity → WaitCheckActivity → LoginActivity / FaceActivity / UploadIDPhotosActivity / SettingSafePwdActivity；FocusService + record.CameraService/AudioService/ScreenRecordService/LiveKitService",
      "trigger_event": "检测到无障碍服务已启用后进入“激活”流程",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（载荷加密）",
      "shown_text_zh": "以“等待审核/人脸核验/上传身份证照片/设置安全密码”的假政务流程继续索取身份与生物特征，同时后台具备录屏、录音、摄像头与 LiveKit 实时回传能力",
      "user_action_requested": "上传身份证照片、进行人脸采集、设置查询与安全密码",
      "code_anchor": "cb310a0d…c6.ui.ActivationActivity / WaitCheckActivity / FaceActivity / UploadIDPhotosActivity / SettingSafePwdActivity；cb310a0d…c6.record.ScreenRecordService / CameraService / AudioService / LiveKitService"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍列表项：android:label 与 android:description 均为「Identitas Kependudukan Digital」（resources.arsc 中可确证）",
    "无障碍服务配置 res/values/arrays.xml/touch_accessibility_service_config.xml：description 指向上述字符串，并声明 isAccessibilityTool=true / canRetrieveWindowContent / canPerformGestures",
    "应用内引导弹窗与说明文字：位于加密资产 assets/OoooooOooo 解密后的二阶段代码（含 CheckPermissionActivity / TransplentPermissionActivity），静态不可见",
    "预筛命中的权限失败文案（如「获取权限失败，继续保存图片」「获取系统相机权限被拒绝」「获取系统录音权限被拒绝」）位于加密载荷或壳内资源，本次静态未能定位到明文载体",
    "可能存在的远端 WebView 引导页：未获静态证据，需运行期抓包确认"
  ],
  "verbatim_texts": [
    {
      "lang": "id",
      "text_verbatim": "Identitas Kependudukan Digital",
      "text_zh": "数字人口身份（印尼官方电子身份证应用名）",
      "source_location": "resources.arsc 中 android:label / android:description（无障碍服务 FocusService）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility service description",
      "text_zh": "无障碍服务说明",
      "source_location": "resources.arsc（无障碍服务描述默认串）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "zh",
      "text_verbatim": "获取权限失败，继续保存图片",
      "text_zh": "获取权限失败，继续保存图片",
      "source_location": "预筛字符串（静态未定位到明文载体，疑在加密载荷/壳资源）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "zh",
      "text_verbatim": "获取系统相机权限被拒绝",
      "text_zh": "获取系统相机权限被拒绝",
      "source_location": "预筛字符串（静态未定位到明文载体）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：壳+加密载荷隐藏跳转与回调逻辑；Manifest 中存在 TransplentPermissionActivity（透明页）与 WaitCheckActivity，配合 onResume 重拉/悬浮窗按钮的死循环重跳高度可疑，需动态验证",
    "overlay_or_fake_settings": "存在叠层条件：声明 SYSTEM_ALERT_WINDOW 与 SYSTEM_OVERLAY_WINDOW 权限，并含 TransplentPermissionActivity（透明 Activity），具备在系统设置页上叠加半透明指引层的能力；是否为高仿无障碍开关页需动态确认",
    "restricted_settings_13plus_coaching": "不可静态还原（Android 13+ 受限设置/应用详情页教学文案位于加密载荷内，未获静态证据）",
    "post_grant_anti_removal": "不可静态还原：存在 asd.kkalive.com.daemon.* 守护进程、OnePxActivity 与多个 JobService，具备反撤权/保活基础能力，但未见 GLOBAL_ACTION_BACK/HOME 阻止撤权的静态证据",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 CheckPermissionActivity 或 TransplentPermissionActivity 启动、或窗口出现 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 跳转的瞬间立即拉起 UTG；另在从系统无障碍页返回前台后 800ms 内再次抓取，捕捉重新压栈的引导页或遮罩层",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页 / 权限检查页",
        "page_identifier": "包名 com.udadwn.dnfenu.jjmck.dismo 下 CheckPermissionActivity 窗口，含权限清单与“激活/开启”主按钮",
        "why_most_useful": "该页是引导链起点，可直接读到诱导文案原文与是否存在取消/跳过入口",
        "observable_utg_signals": ["窗口类名含 CheckPermissionActivity", "权限条目文本（通讯录/短信/相机/录音/无障碍）", "是否存在“取消/稍后/跳过”可点击节点", "主按钮文案（激活/立即开启）"]
      },
      {
        "page_role": "跳转前无障碍教学页 / 叠层指引",
        "page_identifier": "TransplentPermissionActivity 透明窗口或 TYPE_APPLICATION_OVERLAY 悬浮窗，覆盖在系统设置之上",
        "why_most_useful": "区分“良性说明”与“遮罩式诱导开启”最关键，且能捕获伪造开关页/手指指引图",
        "observable_utg_signals": ["窗口是否透明/半透明且覆盖 Settings", "是否出现仿系统开关控件或手指引导图", "文案是否含“点这里开启/必须开启”强制语", "是否遮挡真实系统开关导致误点"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍页中 label 为 Identitas Kependudukan Digital 的条目",
        "why_most_useful": "核对服务名冒用与 Android 13+ 是否因 isAccessibilityTool=true 而未显示敏感数据警告",
        "observable_utg_signals": ["条目名称 Identitas Kependudukan Digital", "是否出现“可查看敏感数据/可执行手势”警告文本", "开关状态变化时间点"]
      },
      {
        "page_role": "获权后假政务流程页",
        "page_identifier": "ActivationActivity / WaitCheckActivity / UploadIDPhotosActivity / FaceActivity",
        "why_most_useful": "确认获权后立即转入身份与生物特征采集，佐证无障碍权限的真实目的",
        "observable_utg_signals": ["“等待审核/激活”文案", "身份证上传与人脸采集界面元素", "设置查询密码/安全密码输入框"]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "显著盲区：核心引导逻辑与全部引导文案封装在加密资产 assets/OoooooOooo（自定义魔数，配合 libdpt.so 运行期解密）中，静态只能确认无障碍服务声明、品牌冒用标签与 isAccessibilityTool=true；若运行期引导采用纯图片/纯视频（无文本节点）或仅通过远端 WebView 下发 HTML，则 UTG 文本抽取会失效，需 OCR 与流量抓包补证。注意静态加壳不阻挡运行期 UTG 采集。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "ID_FAKE_IS_ACCESSIBILITY_TOOL",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "cb310a0da268140999ff21e12d8f2afef.c67f205dae8ec47999791d07a0b0def2d.c015e6446b3c348d695474a9ef074f2c6.service.FocusService",
    "cb310a0da268140999ff21e12d8f2afef.c67f205dae8ec47999791d07a0b0def2d.c015e6446b3c348d695474a9ef074f2c6.ui.CheckPermissionActivity",
    "cb310a0da268140999ff21e12d8f2afef.c67f205dae8ec47999791d07a0b0def2d.c015e6446b3c348d695474a9ef074f2c6.ui.TransplentPermissionActivity",
    "res/values/arrays.xml/touch_accessibility_service_config.xml",
    "com.nashsiqiu.shell.ProxyApplication / assets/OoooooOooo（加密二阶段载荷）"
  ]
}
```

**覆盖边界**：本次未展开 `libdpt.so` 与 `assets/OoooooOooo` 的解密逆向，也未启动动态采集；`ACTION_ACCESSIBILITY_SETTINGS` 跳转点、拒绝后重跳循环、是否伪造设置页等结论依赖运行期验证。若需闭环，下一步应对 `assets/OoooooOooo` 做算法还原或直接运行应用做 UTG+流量采集。

</details>
