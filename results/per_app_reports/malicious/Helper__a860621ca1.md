# MR_039__a860621ca1｜Helper — firewey

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：469.1s

## 1. 一句话核心结论

- **核心申请方式**：以透明无界面 Activity 静默启动，通过加密模块下发原生权限引导弹窗，把「无障碍服务」包装成清理后台卡慢应用并直接在系统无障碍说明里教用户点右上角开关，同时声明不收集任何个人数据。
- **静态可见性说明**：Manifest 声明、无障碍服务类壳、res/xml/sa__detection_service_config.xml、全部权限引导与无障碍说明文案在解包资源中完整静态可见；但真正执行 ACTION_ACCESSIBILITY_SETTINGS 跳转、引导弹窗展示与获权后事件处理的 cleanmaster 模块实现不在主 dex 内（AccessibilityDetectService 仅转发 getIndex()=10 / getModulePackageName()="com.superman.cleanmaster"），模块代码位于 assets/firehelper.jar（XOR 0x37 加密，运行时解密后 DexClassLoader 加载），主 dex 与模块 dex 转储均无 android.settings.ACTION_ACCESSIBILITY_SETTINGS 字面量，跳转与拒权循环逻辑需动态 UTG 或模块逆向确认。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `a860621ca11cd660118a4127c12e91b64f3dca7caea137b2a15b39001184b203` |
| 包名 / 年份 | `com.mufc.fireymn` / 2020 |
| 家族 / 品类 | **Helper**（同池样本数：2） |
| 原始来源标识 | https://securelist.com/unkillable-xhelper-and-a-trojan-matryoshka/96487/ |
| 桌面显示名 | firewey |
| 引导页宣称品牌/身份 | Clean Master（清理大师 / 内存加速工具） |
| 系统无障碍列表服务名 | firewey（无障碍服务 android:label=@string/app_name，与桌面名一致） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务名在中文资源中被改写为「开启辅助权限」（sa__permission_open_accessibility）以弱化「无障碍」敏感词；服务类名伪装为 cleanmaster.AccessibilityDetectService（探测/检测语义）；实际承载逻辑的模块入口名为 ModuleConstants.AccessibilityDetectService=10 索引常量，类本身为空壳；sa__detection_service_des 用「点右上角开关」把系统开关位置写成说明正文，属把系统警告挤出视野的教学式措辞；包名 com.mufc.fireymn / 显示名 firewey 与宣称品牌 Clean Master 不一致。 |
| 无障碍服务类名 | `com.superman.moduleshell.cleanmaster.AccessibilityDetectService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, PACKAGE_USAGE_STATS, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Please turn on the button in the top-right corner. <br><br>Powerful clean the background apps that use memory.<br><br>Notice: We will NOT collect any personal data. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.mufc.fireymn.MainActivity（android:theme=@android:style/Theme.Translucent.NoTitleBar，excludeFromRecents=true，exported=true） | 桌面图标点击 / BOOT_COMPLETED 拉起 / 其他应用 exported 启动 → onCreate | 原生Activity | 无 | 无需用户操作，用户看不到任何清理界面 | `com.mufc.fireymn.MainActivity；AndroidManifest.xml activity 声明` |
| 2 | 业务功能触发 | 模块化框架加载：ModuleManager → ModuleConstants.CM="com.superman.cleanmaster"；AccessibilityDetectService.getIndex()=10 | 主进程启动后 ModuleManager 反射分发 cleanmaster 模块（模块代码由 assets/firehelper.jar 解密后 DexClassLoader 载入） | 不可静态还原 | 无 | 无 | `com.superman.moduleshell.cleanmaster.AccessibilityDetectService#getModulePackageName / #getIndex；com.superman.module.ModuleConstants#CM` |
| 3 | 引导说明页 | cleanmaster 模块权限引导界面（Dialog/Activity，模块内实现） | 模块检测到无障碍服务未启用（AccessibilityManager 查询）后拉起引导 | 原生Dialog | **原文**：Please turn on permission / Granting permissions / Enable Accessibility / Grant Floating Window permission / Floating Window<br>**译注**：请开启权限 / 正在授予权限 / 开启无障碍（辅助）权限 / 开启悬浮窗权限 / 悬浮窗 | 点击「Enable Accessibility」进入系统无障碍设置；点击「Grant Floating Window permission」进入悬浮窗授权；是否提供取消/跳过按钮需动态确认（静态未见关闭逻辑） | `res/values/strings.xml：sa__permission_title、sa__grant_permissions_title、sa__permission_open_accessibility、sa__permission_float_window、sa__permission_show_float_window` |
| 4 | 跳受限设置 | 系统悬浮窗/应用详情设置页（Settings.ACTION_MANAGE_OVERLAY_PERMISSION / ACTION_APPLICATION_DETAILS_SETTINGS） | 引导页点击悬浮窗项 | 不可静态还原 | 无 | 用户手动打开「显示在其他应用上层」开关 | `cleanmaster 模块（assets/firehelper.jar 解密后 classes.dex），静态不可定位` |
| 5 | 跳无障碍设置 | 系统设置 Settings.ACTION_ACCESSIBILITY_SETTINGS → 无障碍服务列表中的「firewey」条目 | 引导页点击「Enable Accessibility」项 | 系统无障碍页 | **原文**：firewey — Please turn on the button in the top-right corner. Powerful clean the background apps that use memory. Notice: We will NOT collect any personal data.<br>**译注**：firewey — 请打开右上角的开关。强大的清理占用内存的后台应用。注意：我们不会收集任何个人数据。 | 用户在系统无障碍页找到 firewey 并打开右上角开关 | `res/xml/sa__detection_service_config.xml（android:description=@string/sa__detection_service_des）；AndroidManifest.xml service android:label=@string/app_name` |
| 6 | 遮罩叠层指引 | 获权前/后的悬浮窗引导层（SYSTEM_ALERT_WINDOW 已声明） | 悬浮窗权限授予后由模块弹出引导层 | 悬浮窗Overlay | **原文**：Click here to clean up the background apps / Found a lot of junk files in the phone,<font color=#ff0606>Clean up now! </font><br>**译注**：点击此处清理后台应用 / 发现手机中存在大量垃圾文件，立即清理！ | 点击悬浮窗清理入口 | `res/values/strings.xml：sa__boost_phone_slow_description、sa__boost_phone_slow_title（您的手机异常卡慢）；模块内 Overlay 实现` |
| 7 | 获权后动作 | com.superman.moduleshell.cleanmaster.AccessibilityDetectService（RTemplateAccessibilityService 实现 onAccessibilityEvent） | 系统无障碍事件回调：typeWindowStateChanged / typeWindowContentChanged / typeViewScrolled / typeNotificationStateChanged | 不可静态还原 | 无 | 无 | `com.superman.moduleshell.cleanmaster.AccessibilityDetectService（转发至 RTemplateAccessibilityService）；res/xml/sa__detection_service_config.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：android:label=@string/app_name（firewey）+ android:description=@string/sa__detection_service_des（res/xml/sa__detection_service_config.xml 引用）
- 应用内权限引导界面（模块内 Dialog/Activity）：sa__permission_title「Please turn on permission」+ 列表项 sa__permission_open_accessibility「Enable Accessibility」、sa__permission_float_window「Grant Floating Window permission」、sa__permission_show_float_window「Floating Window」，顶部标题 sa__grant_permissions_title「Granting permissions」（res/values/strings.xml 及其 values-zh-rCN 对应项）
- 悬浮窗/叠层引导文案：sa__boost_phone_slow_title「您的手机异常卡慢」、sa__boost_phone_slow_description「Click here to clean up the background apps」、含 <font color=#ff0606> 红色 HTML 的「Found a lot of junk files in the phone,Clean up now!」
- 无障碍服务自述承诺句位于 sa__detection_service_des 正文：「Notice: We will NOT collect any personal data.」——只出现在系统无障碍说明里，不出现在应用自身可交互界面（应用无可交互界面）
- 中文资源将无障碍入口改写为「开启辅助权限」，与英文「Enable Accessibility」并存

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Please turn on the button in the top-right corner. Powerful clean the background apps that use memory. Notice: We will NOT collect any personal data. | 请打开右上角的开关。强大的清理占用内存的后台应用。注意：我们不会收集任何个人数据。 | `res/values/strings.xml key=sa__detection_service_des（经 res/xml/sa__detection_service_config.xml 作为 android:description 呈现）` | 受限设置分步教学 |
| zh | 打开右上角的开关。 | 打开右上角的开关。 | `res/values-zh-rCN/strings.xml key=sa__detection_service_des` | 受限设置分步教学 |
| en | Enable Accessibility | 开启无障碍（辅助）权限 | `res/values/strings.xml key=sa__permission_open_accessibility` | 清理工具伪装 |
| zh | 开启辅助权限 | 开启辅助权限 | `res/values-zh-rCN/strings.xml key=sa__permission_open_accessibility` | 清理工具伪装 |
| en | Please turn on permission | 请开启权限 | `res/values/strings.xml key=sa__permission_title` | 清理工具伪装 |
| en | Grant Floating Window permission | 开启悬浮窗权限 | `res/values/strings.xml key=sa__permission_float_window` | 受限设置分步教学 |
| en | Granting permissions | 正在授予权限 | `res/values/strings.xml key=sa__grant_permissions_title` | 清理工具伪装 |
| zh | 您的手机异常卡慢 | 您的手机异常卡慢 | `res/values-zh-rCN/strings.xml key=sa__boost_phone_slow_title` | 故障恐吓 |
| en | Found a lot of junk files in the phone,<font color=#ff0606>Clean up now! </font> | 发现手机中存在大量垃圾文件，立即清理！ | `res/values/strings.xml（HTML 富文本，红色高亮）` | 故障恐吓 |
| en | Click here to clean up the background apps | 点击此处清理后台应用 | `res/values/strings.xml key=sa__boost_phone_slow_description` | 清理工具伪装 |
| en | Notice: We will NOT collect any personal data. | 注意：我们不会收集任何个人数据。 | `res/values/strings.xml key=sa__detection_service_des（正文末句）` | 隐私承诺 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：静态不可完整确认。可确认部分：MainActivity 为透明主题、excludeFromRecents=true，onCreate 即 finish 并 moveTaskToBack(true)，应用本身不提供可停留的清理界面；未获权时用户返回系统设置只能重新从桌面/后台服务再次被拉起引导。是否存在 onResume 定时重跳或 Timer 每 N 秒拉起，代码位于 XOR 加密的 firehelper.jar 模块内，需动态 UTG 观测。
- **遮罩叠层 / 高仿系统设置页**：未见高仿系统无障碍开关页；但已声明 SYSTEM_ALERT_WINDOW 并在资源中备有悬浮窗权限引导与叠层清理提示文案（sa__permission_float_window、sa__permission_show_float_window、sa__boost_phone_slow_*），可叠放半透明引导层；是否在系统无障碍页之上压栈遮罩需动态确认。
- **Android 13+ 受限设置（Restricted Settings）应对**：无障碍场景下的教学已确认存在且写在系统无障碍说明里：「Please turn on the button in the top-right corner.」（请打开右上角的开关）。针对 Android 13+ 应用详情页右上角菜单「允许受限设置」的独立教学文案未在资源中检索到，但 REQUEST_INSTALL_PACKAGES 已声明且模块框架具备安装代理 Activity（RiInstallProxyActivity、TipInstallActivity），是否走 Session 安装器绕过需动态确认。
- **获权后即时行为与防撤权机制**：静态未见监听无障碍设置页并用 GLOBAL_ACTION_BACK/HOME 阻止撤权的代码（该类逻辑若存在应位于加密模块内）；可确认的是服务开启 canRetrieveWindowContent 与 flagRequestFilterKeyEvents，具备在设置页上读取控件与拦截按键的能力基础，需动态验证。
- **良性降级 / 替代方案**：无。应用不存在可用的手动清理模式或仅观看模式；未授权时无任何降级功能路径，MainActivity 透明即退出。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动 com.mufc.fireymn.MainActivity 后立即开始录屏/UTG 采样（该 Activity 透明且 onCreate 即 finish，是模块拉起权限引导的确定起点）；同时在监测到顶层窗口变为 com.android.settings 无障碍页（AccessibilitySettings）或应用详情页时立即抓取整屏节点树。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在盲区：无障碍服务类为纯转发空壳，全部跳转与拒权循环逻辑位于 XOR 0x37 加密的 assets/firehelper.jar 模块内（运行时解密 + DexClassLoader），静态无法定位 ACTION_ACCESSIBILITY_SETTINGS 调用点；若模块进一步由 https://pgmd.leostat.com/leoads/api/m-p-upgrade 远端下发替换，则引导 UI 形态可随时变化，UTG 需在联网与断网两种条件下各采一轮。此外应用无可见主界面（透明 Activity + excludeFromRecents），UTG 需从进程启动时刻即开始采样，否则会漏掉第一帧引导页。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后弹出的权限引导页（模块 Dialog/Activity）** | 顶层窗口为 com.mufc.fireymn 进程内的 Dialog 或 com.superman.* 模块 Activity，文本包含 "Please turn on permission" / "Granting permissions" / "Enable Accessibility" | 这是用户第一次被告知要开无障碍的界面，直接决定判定为「清理工具伪装引导」还是「良性说明」，并能确认是否提供取消/跳过按钮 | 是否存在关闭/取消/跳过按钮节点；引导文案是否把无障碍说成清理功能；是否出现悬浮窗授权按钮并紧随其后跳系统设置 |
| **系统无障碍服务列表中的 firewey 条目** | com.android.settings 无障碍页，节点文本含 firewey 与 "Please turn on the button in the top-right corner" | 验证应用是否把自己的功能说明伪装成清理工具、并把系统开关位置写进 description 完成分步教学；这是纯 UTG 可 100% 提取的关键判别证据 | 服务标签与桌面名是否一致；description 是否含点右上角开关的教学句；是否含"不会收集任何个人数据"隐私承诺；开关初始状态 |
| **跳转设置页后叠放的引导遮罩/悬浮窗** | type=TYPE_APPLICATION_OVERLAY 窗口或覆盖在 com.android.settings 之上的应用窗口 | 区分是否采用压栈遮罩逼迫用户点开关（恶意）还是仅跳转后留在本页（相对温和） | 无障碍设置页之上是否存在应用自有窗口；遮罩文本是否指向开关位置；遮罩是否不可关闭 |
| **拒权返回后的反馈页** | 从无障碍设置返回后 0~3 秒内的顶层窗口序列 | 确认是否构成 onResume 死循环重跳/定时拉起，判定强制程度 | 返回后是否立即再次出现同一引导页；重跳间隔与次数；是否出现辱骂/恐吓型挽留文案 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.superman.moduleshell.cleanmaster.AccessibilityDetectService#getModulePackageName / #getIndex`
- `com.superman.module.ModuleConstants#CM`
- `res/xml/sa__detection_service_config.xml`
- `res/values/strings.xml#sa__detection_service_des`
- `res/values/strings.xml#sa__permission_open_accessibility`
- `AndroidManifest.xml（service AccessibilityDetectService / activity com.mufc.fireymn.MainActivity）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点

**说明：** 指定的 `input.apk` 路径在运行期已不存在。我改用同包名 `com.mufc.fireymn` 的既有解包缓存（`APKAudit_baseline\...\05_xHelper\a860621c….apk.arkaudit_cache`，含 jadx 反编译与 `firehelper` 解密产物）完成核验。以下结论均基于该缓存，包名、资源与 Manifest 一致。

- **无障碍服务声明完全静态可见**：`com.superman.moduleshell.cleanmaster.AccessibilityDetectService` 以 `android:label="@string/app_name"`（即 `firewey`）注册，配置 `res/xml/sa__detection_service_config.xml` 中 `canRetrieveWindowContent="true"`、`flagRequestFilterKeyEvents`、`flagRequestEnhancedWebAccessibility`，并监听 `typeWindowStateChanged/typeWindowContentChanged/typeViewScrolled/typeNotificationStateChanged`——这是可读取任意界面内容与按键事件的高权限配置，与“清理后台应用”的说法严重不成比例。
- **服务类是空壳转发器**：该类只覆写 `getIndex()→10` 与 `getModulePackageName()→ModuleConstants.CM`（`"com.superman.cleanmaster"`），真实 `onAccessibilityEvent` 逻辑在模块化框架 `com.superman.module.api.template.RTemplateAccessibilityService` 与远端/加密模块中，主 dex 不含实现。
- **权限引导文案在资源中完整可见**：`sa__permission_title`（请开启权限）、`sa__permission_open_accessibility`（Enable Accessibility / 开启辅助权限）、`sa__permission_float_window`（Grant Floating Window permission）、`sa__grant_permissions_title`（Granting permissions）、`sa__permission_show_float_window`（Floating Window）。
- **无障碍列表说明本身就是分步教学 + 隐私承诺**：`sa__detection_service_des` = “Please turn on the button in the top-right corner. Powerful clean the background apps that use memory. Notice: We will NOT collect any personal data.”（中文版“打开右上角的开关。…”）。中文 `sa__permission_open_accessibility` 被改称为“开启辅助权限”，弱化“无障碍”敏感度。
- **入口无可见界面**：`com.mufc.fireymn.MainActivity` 为 `Theme.Translucent.NoTitleBar` + `excludeFromRecents="true"` + `exported="true"`，配合已验证的 onCreate 即 finish / moveTaskToBack 行为，用户看不到任何可交互的清理界面，只能被动进入权限引导。
- **静态缺口**：主 dex 与模块 dex 转储中均搜不到 `ACTION_ACCESSIBILITY_SETTINGS` / `ACTION_APPLICATION_DETAILS_SETTINGS` 字面量，跳转代码位于 XOR(0x37) 加密的 `assets/firehelper.jar`（运行时解密后 DexClassLoader 加载）所承载的 cleanmaster 模块内，需动态 UTG 或模块逆向补齐。

---

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "Manifest 声明、无障碍服务类壳、res/xml/sa__detection_service_config.xml、全部权限引导与无障碍说明文案在解包资源中完整静态可见；但真正执行 ACTION_ACCESSIBILITY_SETTINGS 跳转、引导弹窗展示与获权后事件处理的 cleanmaster 模块实现不在主 dex 内（AccessibilityDetectService 仅转发 getIndex()=10 / getModulePackageName()=\"com.superman.cleanmaster\"），模块代码位于 assets/firehelper.jar（XOR 0x37 加密，运行时解密后 DexClassLoader 加载），主 dex 与模块 dex 转储均无 android.settings.ACTION_ACCESSIBILITY_SETTINGS 字面量，跳转与拒权循环逻辑需动态 UTG 或模块逆向确认。",
  "summary_one_liner": "以透明无界面 Activity 静默启动，通过加密模块下发原生权限引导弹窗，把「无障碍服务」包装成清理后台卡慢应用并直接在系统无障碍说明里教用户点右上角开关，同时声明不收集任何个人数据。",
  "disguise_identity": {
    "app_display_name": "firewey",
    "claimed_brand_or_persona": "Clean Master（清理大师 / 内存加速工具）",
    "a11y_service_label": "firewey（无障碍服务 android:label=@string/app_name，与桌面名一致）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务名在中文资源中被改写为「开启辅助权限」（sa__permission_open_accessibility）以弱化「无障碍」敏感词；服务类名伪装为 cleanmaster.AccessibilityDetectService（探测/检测语义）；实际承载逻辑的模块入口名为 ModuleConstants.AccessibilityDetectService=10 索引常量，类本身为空壳；sa__detection_service_des 用「点右上角开关」把系统开关位置写成说明正文，属把系统警告挤出视野的教学式措辞；包名 com.mufc.fireymn / 显示名 firewey 与宣称品牌 Clean Master 不一致。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.mufc.fireymn.MainActivity（android:theme=@android:style/Theme.Translucent.NoTitleBar，excludeFromRecents=true，exported=true）",
      "trigger_event": "桌面图标点击 / BOOT_COMPLETED 拉起 / 其他应用 exported 启动 → onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无可见界面：透明主题，onCreate 即 finish、onStart 调 moveTaskToBack(true)，不进入最近任务列表",
      "user_action_requested": "无需用户操作，用户看不到任何清理界面",
      "code_anchor": "com.mufc.fireymn.MainActivity；AndroidManifest.xml activity 声明"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "模块化框架加载：ModuleManager → ModuleConstants.CM=\"com.superman.cleanmaster\"；AccessibilityDetectService.getIndex()=10",
      "trigger_event": "主进程启动后 ModuleManager 反射分发 cleanmaster 模块（模块代码由 assets/firehelper.jar 解密后 DexClassLoader 载入）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面；此步完成模块注册与权限检测调度，具体判定条件位于加密模块内",
      "user_action_requested": "无",
      "code_anchor": "com.superman.moduleshell.cleanmaster.AccessibilityDetectService#getModulePackageName / #getIndex；com.superman.module.ModuleConstants#CM"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "cleanmaster 模块权限引导界面（Dialog/Activity，模块内实现）",
      "trigger_event": "模块检测到无障碍服务未启用（AccessibilityManager 查询）后拉起引导",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Please turn on permission / Granting permissions / Enable Accessibility / Grant Floating Window permission / Floating Window",
      "shown_text_zh": "请开启权限 / 正在授予权限 / 开启无障碍（辅助）权限 / 开启悬浮窗权限 / 悬浮窗",
      "user_action_requested": "点击「Enable Accessibility」进入系统无障碍设置；点击「Grant Floating Window permission」进入悬浮窗授权；是否提供取消/跳过按钮需动态确认（静态未见关闭逻辑）",
      "code_anchor": "res/values/strings.xml：sa__permission_title、sa__grant_permissions_title、sa__permission_open_accessibility、sa__permission_float_window、sa__permission_show_float_window"
    },
    {
      "step": 4,
      "stage": "跳受限设置",
      "screen_or_component": "系统悬浮窗/应用详情设置页（Settings.ACTION_MANAGE_OVERLAY_PERMISSION / ACTION_APPLICATION_DETAILS_SETTINGS）",
      "trigger_event": "引导页点击悬浮窗项",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "跳转系统悬浮窗权限页；跳转 Intent 构造代码位于加密模块，主 dex 无 android.settings.* 相关字面量",
      "user_action_requested": "用户手动打开「显示在其他应用上层」开关",
      "code_anchor": "cleanmaster 模块（assets/firehelper.jar 解密后 classes.dex），静态不可定位"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 Settings.ACTION_ACCESSIBILITY_SETTINGS → 无障碍服务列表中的「firewey」条目",
      "trigger_event": "引导页点击「Enable Accessibility」项",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "firewey — Please turn on the button in the top-right corner. Powerful clean the background apps that use memory. Notice: We will NOT collect any personal data.",
      "shown_text_zh": "firewey — 请打开右上角的开关。强大的清理占用内存的后台应用。注意：我们不会收集任何个人数据。",
      "user_action_requested": "用户在系统无障碍页找到 firewey 并打开右上角开关",
      "code_anchor": "res/xml/sa__detection_service_config.xml（android:description=@string/sa__detection_service_des）；AndroidManifest.xml service android:label=@string/app_name"
    },
    {
      "step": 6,
      "stage": "遮罩叠层指引",
      "screen_or_component": "获权前/后的悬浮窗引导层（SYSTEM_ALERT_WINDOW 已声明）",
      "trigger_event": "悬浮窗权限授予后由模块弹出引导层",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Click here to clean up the background apps / Found a lot of junk files in the phone,<font color=#ff0606>Clean up now! </font>",
      "shown_text_zh": "点击此处清理后台应用 / 发现手机中存在大量垃圾文件，立即清理！",
      "user_action_requested": "点击悬浮窗清理入口",
      "code_anchor": "res/values/strings.xml：sa__boost_phone_slow_description、sa__boost_phone_slow_title（您的手机异常卡慢）；模块内 Overlay 实现"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "com.superman.moduleshell.cleanmaster.AccessibilityDetectService（RTemplateAccessibilityService 实现 onAccessibilityEvent）",
      "trigger_event": "系统无障碍事件回调：typeWindowStateChanged / typeWindowContentChanged / typeViewScrolled / typeNotificationStateChanged",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面；服务以 canRetrieveWindowContent=true、flagRequestFilterKeyEvents 读取前台窗口内容与按键事件，具体行为（清理判定、广告展示或保活）在加密模块内",
      "user_action_requested": "无",
      "code_anchor": "com.superman.moduleshell.cleanmaster.AccessibilityDetectService（转发至 RTemplateAccessibilityService）；res/xml/sa__detection_service_config.xml"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：android:label=@string/app_name（firewey）+ android:description=@string/sa__detection_service_des（res/xml/sa__detection_service_config.xml 引用）",
    "应用内权限引导界面（模块内 Dialog/Activity）：sa__permission_title「Please turn on permission」+ 列表项 sa__permission_open_accessibility「Enable Accessibility」、sa__permission_float_window「Grant Floating Window permission」、sa__permission_show_float_window「Floating Window」，顶部标题 sa__grant_permissions_title「Granting permissions」（res/values/strings.xml 及其 values-zh-rCN 对应项）",
    "悬浮窗/叠层引导文案：sa__boost_phone_slow_title「您的手机异常卡慢」、sa__boost_phone_slow_description「Click here to clean up the background apps」、含 <font color=#ff0606> 红色 HTML 的「Found a lot of junk files in the phone,Clean up now!」",
    "无障碍服务自述承诺句位于 sa__detection_service_des 正文：「Notice: We will NOT collect any personal data.」——只出现在系统无障碍说明里，不出现在应用自身可交互界面（应用无可交互界面）",
    "中文资源将无障碍入口改写为「开启辅助权限」，与英文「Enable Accessibility」并存"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Please turn on the button in the top-right corner. Powerful clean the background apps that use memory. Notice: We will NOT collect any personal data.",
      "text_zh": "请打开右上角的开关。强大的清理占用内存的后台应用。注意：我们不会收集任何个人数据。",
      "source_location": "res/values/strings.xml key=sa__detection_service_des（经 res/xml/sa__detection_service_config.xml 作为 android:description 呈现）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "zh",
      "text_verbatim": "打开右上角的开关。",
      "text_zh": "打开右上角的开关。",
      "source_location": "res/values-zh-rCN/strings.xml key=sa__detection_service_des",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Accessibility",
      "text_zh": "开启无障碍（辅助）权限",
      "source_location": "res/values/strings.xml key=sa__permission_open_accessibility",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "zh",
      "text_verbatim": "开启辅助权限",
      "text_zh": "开启辅助权限",
      "source_location": "res/values-zh-rCN/strings.xml key=sa__permission_open_accessibility",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Please turn on permission",
      "text_zh": "请开启权限",
      "source_location": "res/values/strings.xml key=sa__permission_title",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Grant Floating Window permission",
      "text_zh": "开启悬浮窗权限",
      "source_location": "res/values/strings.xml key=sa__permission_float_window",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Granting permissions",
      "text_zh": "正在授予权限",
      "source_location": "res/values/strings.xml key=sa__grant_permissions_title",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "zh",
      "text_verbatim": "您的手机异常卡慢",
      "text_zh": "您的手机异常卡慢",
      "source_location": "res/values-zh-rCN/strings.xml key=sa__boost_phone_slow_title",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Found a lot of junk files in the phone,<font color=#ff0606>Clean up now! </font>",
      "text_zh": "发现手机中存在大量垃圾文件，立即清理！",
      "source_location": "res/values/strings.xml（HTML 富文本，红色高亮）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Click here to clean up the background apps",
      "text_zh": "点击此处清理后台应用",
      "source_location": "res/values/strings.xml key=sa__boost_phone_slow_description",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Notice: We will NOT collect any personal data.",
      "text_zh": "注意：我们不会收集任何个人数据。",
      "source_location": "res/values/strings.xml key=sa__detection_service_des（正文末句）",
      "rhetorical_frame": "隐私承诺"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "静态不可完整确认。可确认部分：MainActivity 为透明主题、excludeFromRecents=true，onCreate 即 finish 并 moveTaskToBack(true)，应用本身不提供可停留的清理界面；未获权时用户返回系统设置只能重新从桌面/后台服务再次被拉起引导。是否存在 onResume 定时重跳或 Timer 每 N 秒拉起，代码位于 XOR 加密的 firehelper.jar 模块内，需动态 UTG 观测。",
    "overlay_or_fake_settings": "未见高仿系统无障碍开关页；但已声明 SYSTEM_ALERT_WINDOW 并在资源中备有悬浮窗权限引导与叠层清理提示文案（sa__permission_float_window、sa__permission_show_float_window、sa__boost_phone_slow_*），可叠放半透明引导层；是否在系统无障碍页之上压栈遮罩需动态确认。",
    "restricted_settings_13plus_coaching": "无障碍场景下的教学已确认存在且写在系统无障碍说明里：「Please turn on the button in the top-right corner.」（请打开右上角的开关）。针对 Android 13+ 应用详情页右上角菜单「允许受限设置」的独立教学文案未在资源中检索到，但 REQUEST_INSTALL_PACKAGES 已声明且模块框架具备安装代理 Activity（RiInstallProxyActivity、TipInstallActivity），是否走 Session 安装器绕过需动态确认。",
    "post_grant_anti_removal": "静态未见监听无障碍设置页并用 GLOBAL_ACTION_BACK/HOME 阻止撤权的代码（该类逻辑若存在应位于加密模块内）；可确认的是服务开启 canRetrieveWindowContent 与 flagRequestFilterKeyEvents，具备在设置页上读取控件与拦截按键的能力基础，需动态验证。",
    "benign_graceful_degradation": "无。应用不存在可用的手动清理模式或仅观看模式；未授权时无任何降级功能路径，MainActivity 透明即退出。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动 com.mufc.fireymn.MainActivity 后立即开始录屏/UTG 采样（该 Activity 透明且 onCreate 即 finish，是模块拉起权限引导的确定起点）；同时在监测到顶层窗口变为 com.android.settings 无障碍页（AccessibilitySettings）或应用详情页时立即抓取整屏节点树。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后弹出的权限引导页（模块 Dialog/Activity）",
        "page_identifier": "顶层窗口为 com.mufc.fireymn 进程内的 Dialog 或 com.superman.* 模块 Activity，文本包含 \"Please turn on permission\" / \"Granting permissions\" / \"Enable Accessibility\"",
        "why_most_useful": "这是用户第一次被告知要开无障碍的界面，直接决定判定为「清理工具伪装引导」还是「良性说明」，并能确认是否提供取消/跳过按钮",
        "observable_utg_signals": ["是否存在关闭/取消/跳过按钮节点", "引导文案是否把无障碍说成清理功能", "是否出现悬浮窗授权按钮并紧随其后跳系统设置"]
      },
      {
        "page_role": "系统无障碍服务列表中的 firewey 条目",
        "page_identifier": "com.android.settings 无障碍页，节点文本含 firewey 与 \"Please turn on the button in the top-right corner\"",
        "why_most_useful": "验证应用是否把自己的功能说明伪装成清理工具、并把系统开关位置写进 description 完成分步教学；这是纯 UTG 可 100% 提取的关键判别证据",
        "observable_utg_signals": ["服务标签与桌面名是否一致", "description 是否含点右上角开关的教学句", "是否含\"不会收集任何个人数据\"隐私承诺", "开关初始状态"]
      },
      {
        "page_role": "跳转设置页后叠放的引导遮罩/悬浮窗",
        "page_identifier": "type=TYPE_APPLICATION_OVERLAY 窗口或覆盖在 com.android.settings 之上的应用窗口",
        "why_most_useful": "区分是否采用压栈遮罩逼迫用户点开关（恶意）还是仅跳转后留在本页（相对温和）",
        "observable_utg_signals": ["无障碍设置页之上是否存在应用自有窗口", "遮罩文本是否指向开关位置", "遮罩是否不可关闭"]
      },
      {
        "page_role": "拒权返回后的反馈页",
        "page_identifier": "从无障碍设置返回后 0~3 秒内的顶层窗口序列",
        "why_most_useful": "确认是否构成 onResume 死循环重跳/定时拉起，判定强制程度",
        "observable_utg_signals": ["返回后是否立即再次出现同一引导页", "重跳间隔与次数", "是否出现辱骂/恐吓型挽留文案"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在盲区：无障碍服务类为纯转发空壳，全部跳转与拒权循环逻辑位于 XOR 0x37 加密的 assets/firehelper.jar 模块内（运行时解密 + DexClassLoader），静态无法定位 ACTION_ACCESSIBILITY_SETTINGS 调用点；若模块进一步由 https://pgmd.leostat.com/leoads/api/m-p-upgrade 远端下发替换，则引导 UI 形态可随时变化，UTG 需在联网与断网两种条件下各采一轮。此外应用无可见主界面（透明 Activity + excludeFromRecents），UTG 需从进程启动时刻即开始采样，否则会漏掉第一帧引导页。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "COERCE_NO_SKIP_NON_CANCELABLE"
  ],
  "code_anchors": [
    "com.superman.moduleshell.cleanmaster.AccessibilityDetectService#getModulePackageName / #getIndex",
    "com.superman.module.ModuleConstants#CM",
    "res/xml/sa__detection_service_config.xml",
    "res/values/strings.xml#sa__detection_service_des",
    "res/values/strings.xml#sa__permission_open_accessibility",
    "AndroidManifest.xml（service AccessibilityDetectService / activity com.mufc.fireymn.MainActivity）"
  ]
}
```

</details>
