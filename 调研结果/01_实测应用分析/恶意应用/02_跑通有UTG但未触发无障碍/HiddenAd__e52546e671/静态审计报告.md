# MR_105__e52546e671｜HiddenAd — Fire in the Desert

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：161.5s

## 1. 一句话核心结论

- **核心申请方式**：该样本不具备无障碍引导链，实为 Unity 游戏外壳包裹的隐藏保活+静默广告家族样本（1×1 透明 Activity 与多前台服务互拉，配合全量广告 SDK）。
- **静态可见性说明**：Manifest 与 4 个主 DEX 完整可见且可确认：无任何 BIND_ACCESSIBILITY_SERVICE 无障碍服务声明、无 android.settings.ACCESSIBILITY_SETTINGS 跳转、无 android:description 无障碍说明，故无障碍引导链本身静态不可见（不存在）。应用字符串经 StringFog 变体 ALLATORIxDEMO 加密、业务主逻辑下沉至 libil2cpp.so，且大量广告/保活组件的行为参数可能由远端下发；本轮未对 libil2cpp.so 做符号级还原，故原生层是否在运行期拼装引导文案未完全排除。
- **命中的行为模式标签**：`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `e52546e671f096ea99041dd1a867df40b1098b676d804dc9c33652de69f20a9c` |
| 包名 / 年份 | `com.fire.the.desert.in` / 2020 |
| 家族 / 品类 | **HiddenAd**（同池样本数：12） |
| 原始来源标识 | https://gbhackers.com/21-malicious-apps/ |
| 桌面显示名 | Fire in the Desert |
| 引导页宣称品牌/身份 | Fire in the Desert（Unity 休闲游戏，android:isGame=true，banner 与 Unity 启动主题） |
| 系统无障碍列表服务名 | 无（Manifest 未声明任何 AccessibilityService，系统无障碍列表中不会出现该应用条目） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：入口 com.firedesert.StartActivity 使用 Theme.Translucent 作为启动透明壳；com.firedesert.aa.KoAct 以 setGravity(51)+1x1 像素窗口实现不可见 Activity；亮屏即 finish、onDestroy 立即 startForegroundService 形成互拉保活；字符串使用 StringFog 风格 ALLATORIxDEMO 解密；业务逻辑迁至 libil2cpp.so 与 nativeinit JNI 桥；Manifest 无 a11y 相关伪造项 |
| 无障碍服务类名 | `二阶段/嵌包或无直接声明` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `无` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.firedesert.StartActivity（android:theme=Theme.Translucent，MAIN/LAUNCHER） | 用户点击桌面图标（ACTION_MAIN + CATEGORY_LAUNCHER） | 原生Activity | 无 | 无（无任何弹窗、无取消/跳过按钮，直接过渡） | `#1 manifest:basic_info` |
| 2 | 业务功能触发 | com.unity3d.player.UnityPlayerActivity（android:label=@string/app_name，screenOrientation=sensorPortrait） | StartActivity 拉起 Unity 播放器 Activity，Unity 引擎初始化 | 原生Activity | **原文**：Fire in the Desert<br>**译注**：显示名仅为游戏名，未见任何权限申请或安全提示文案 | 无 | `#1 manifest:basic_info` |
| 3 | 获权后动作 | com.firedesert.MainActivity（setContentView(2131165184) 后调用 u.ALLATORIxDEMO） | onCreate(Bundle) | 原生Activity | 无 | 无 | `com.firedesert.MainActivity#onCreate` |
| 4 | 获权后动作 | com.firedesert.aa.KoAct（singleInstance、excludeFromRecents、finishOnTaskLaunch=false） | onCreate 设置 1x1 窗口；onResume 检测 PowerManager.isInteractive() 为真时 finish() | 原生Activity | 无 | 无（用户完全无感） | `com.firedesert.aa.KoAct#onCreate / com.firedesert.aa.KoAct#onResume` |
| 5 | 获权后动作 | com.firedesert.aa.DoService（前台服务）及 Ga1Service/Ga2Service/HeService/PService/SjobService/SimService/UABServiceOne~Four | KoAct.onDestroy() 中 ContextCompat.startForegroundService(this, new Intent(this, DoService.class)) | 通知栏 | 无 | 无 | `com.firedesert.aa.KoAct#onDestroy` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 无任何无障碍引导/说明文字呈现位置：Manifest 中无 AccessibilityService 声明，故系统无障碍列表内不会出现该应用的 android:description 条目
- 4 个主 DEX 与 assets/audience_network.dex 均未检索到 android.settings.ACCESSIBILITY_SETTINGS / ACTION_ACCESSIBILITY_SETTINGS 常量，不存在跳转前教学页或设置页遮罩的代码锚点
- res/values/ids.xml 中的 accessibility_* 条目全部为 androidx 无障碍兼容框架的通用 id 资源，与应用自身引导无关
- 唯一与“设置页”相关的常量为 android.settings.APPLICATION_DETAILS_SETTINGS（classes.dex / classes3.dex），归属广告 SDK 的跳应用详情能力，非无障碍引导
- res/values/strings.xml 中预筛命中的 Facebook/Google Play services 文案（Continue with Facebook、Enable Google Play services 等）为 Facebook SDK 与 Google Play services 可用性提示，与无障碍无关

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Enable Google Play services | 启用 Google Play 服务 | `res/values/strings.xml（Google Play services 可用性提示，SDK 资源）` | 良性透明说明 |
| en | %1$s won't run without Google Play services, which are missing from your device. | %1$s 在缺少 Google Play 服务的设备上无法运行。 | `res/values/strings.xml（SDK 资源）` | 良性透明说明 |
| en | Continue with Facebook | 使用 Facebook 继续 | `res/values/strings.xml（Facebook SDK 登录按钮文案）` | 良性透明说明 |
| en | WebView login requires INTERNET permission | WebView 登录需要 INTERNET 权限 | `res/values/strings.xml（SDK 资源）` | 良性透明说明 |
| en | Fire in the Desert | 沙漠之火 | `res/values/strings.xml: app_name（Manifest android:label / UnityPlayerActivity android:label）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不存在无障碍拒权反馈循环；应用从不读取 getEnabledAccessibilityServiceList/getInstalledAccessibilityServiceList 用于引导判断（仅 androidx 兼容库内出现该符号）。实际存在的“循环”是保活闭环：KoAct.onResume 在亮屏时 finish()，onDestroy 立刻 startForegroundService(DoService)，服务侧再拉起 KoAct。
- **遮罩叠层 / 高仿系统设置页**：无。Manifest 未申请 SYSTEM_ALERT_WINDOW，也未声明无障碍服务，无法叠放引导遮罩或伪造系统无障碍开关页；唯一近似行为是 1×1 像素的不可见 Activity 窗口（KoAct），其目的为常驻而非引导。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未检索到 ACTION_MANAGE_UNKNOWN_APP_SOURCES / REQUEST_INSTALL_PACKAGES 引导链；DEX 线索中的 SESSION_INSTALLER 未在 Manifest 中体现为安装器绕过逻辑。
- **获权后即时行为与防撤权机制**：无（无无障碍权限可撤，故不存在自授权或 GLOBAL_ACTION_BACK/HOME 阻止撤权）。但存在进程级反清理能力：GuardLive$ScRec$SreenBroadcastReceiver 屏幕状态监听、多进程服务、JobService 与开机 RECEIVE_BOOT_COMPLETED 自启。
- **良性降级 / 替代方案**：无（不适用：应用本身不申请无障碍，也未提供手动/ADB 替代路径说明）

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：不应围绕 ACCESSIBILITY_SETTINGS 设钩。建议在冷启动后持续监测两类页面事件：(1) 出现 package=com.fire.the.desert.in 且 activity=com.firedesert.aa.KoAct 的 1×1 不可见窗口；(2) 出现 com.firedesert.aa.DoService 前台服务通知与 KoAct/DoService 交替出现的 activity 切换序列。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在两处盲区：(1) 业务主逻辑位于 libil2cpp.so 且字符串经 ALLATORIxDEMO 加密，本轮未做原生层符号级还原，无法完全排除运行期由远端下发的引导文案；(2) 若远端下发的是纯图片/全屏 WebView 广告，UTG 文本信号可能为空，需结合网络流量与截图复核。另需注意：静态“加壳”判定为 False 且本样本不属于加壳样本，其静态不可见性来自 il2cpp + StringFog，而非 VMP。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动透明壳入口页** | com.firedesert.StartActivity（Theme.Translucent，无任何可见控件） | 确认入口与展示名 Fire in the Desert 的强绑定，且证明启动阶段不存在任何权限引导弹窗 | activity 名称为 StartActivity 但可见节点树为空；无任何文本/按钮节点的全透明窗口 |
| **1×1 隐藏保活 Activity 页** | com.firedesert.aa.KoAct（singleInstance / excludeFromRecents） | 这是该样本最独特的可观测恶意特征，可据此把样本归入隐藏保活型而非无障碍引导型 | 窗口边界为 1×1 像素且位于屏幕左上角；页面不可见却频繁 onCreate/onResume/onDestroy 切换；伴随 DoService 前台服务通知同时出现 |
| **Unity 游戏主界面** | com.unity3d.player.UnityPlayerActivity（label=Fire in the Desert，sensorPortrait） | 作为“良性游戏外壳”的对照页，用于区分正常玩法与后台静默广告/保活行为 | Unity 引擎渲染层节点；无权限申请弹窗出现 |
| **系统应用详情页（若被广告 SDK 拉起）** | Settings 的 com.android.settings.applications.InstalledAppDetails（APPLICATION_DETAILS_SETTINGS） | 用于核实跳转归属：若确实出现，应归因广告 SDK 而非应用自建无障碍教学 | 当前前台包为 com.android.settings 且携带应用包名；本应用处于后台、无对应引导文案 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.firedesert.aa.KoAct#onCreate`
- `com.firedesert.aa.KoAct#onResume`
- `com.firedesert.aa.KoAct#onDestroy`
- `com.firedesert.MainActivity#onCreate`
- `#1 manifest:components`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（围绕“无障碍引导”这一主线，结论为负向，并附对真实行为的修正）

**一、核心事实：静态可见范围内不存在任何无障碍引导链**

- 在完整的 [AndroidManifest 组件清单](<resource-unit:#1 manifest:components>) 中，**没有任何** `android:permission="android.permission.BIND_ACCESSIBILITY_SERVICE"` 的 `AccessibilityService` 子类声明，也没有 `android.accessibilityservice.*` 元数据或 `android:description` 无障碍说明。预筛给出的 `a11y_service_label=[]` 与 `A11Y_OVERLAY` 标签在该样本上属于启发式误报。
- 对 4 个主 DEX 和 `assets/audience_network.dex` 做原生字符串检索后，只命中 `android.settings.APPLICATION_DETAILS_SETTINGS`（classes.dex、classes3.dex），**未命中** `android.settings.ACCESSIBILITY_SETTINGS` 或 `ACTION_ACCESSIBILITY_SETTINGS`；`AccessibilityService` 相关符号全部来自 `androidx.core` 兼容库和 `SpeechToTextAccessibilityService` 这类库内类，并非应用自身实现。
- 因此，从冷启动到获权的整条 UTG 页面流转链（引导弹窗 → 跳设置 → 遮罩 → 拒权循环）在本样本中**不存在可核验的代码实体**。

**二、实际定位到的真实（恶意）行为骨架：Unity 外壳 + 隐藏保活 + 静默广告**

- 桌面入口 [com.firedesert.StartActivity](<resource-unit:#1 manifest:basic_info>)（`Theme.Translucent`，即透明壳）先启动，实际承载界面的则是 `com.unity3d.player.UnityPlayerActivity`（`isGame=true`，显示名 `Fire in the Desert`），这是典型的“游戏外壳”。
- [MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.firedesert.MainActivity#onCreate>) 仅调用 `setContentView`，随后转入 `u.ALLATORIxDEMO(this)`；该类还声明 `native void nativeinit()`（JNI 桥接），说明业务主逻辑位于 il2cpp 原生层，并由 StringFog 风格的 `ALLATORIxDEMO` 方法负责解密字符串。
- [KoAct.onCreate()](<resource-unit:#1.dex1 code:com.firedesert.aa.KoAct#onCreate>) 把窗口 `setGravity(51)`，并将尺寸强制设为 **1×1 像素**，使其成为一个不可见的透明 Activity；[KoAct.onResume()](<resource-unit:#1.dex1 code:com.firedesert.aa.KoAct#onResume>) 在屏幕点亮（`PowerManager.isInteractive()` 返回真）时立即调用 `finish()`，即“亮屏即自毁、灭屏才存活”；[KoAct.onDestroy()](<resource-unit:#1.dex1 code:com.firedesert.aa.KoAct#onDestroy>) 立刻用 `ContextCompat.startForegroundService` 拉起 `DoService`，形成**隐藏 Activity 与前台服务互相拉起**的保活闭环。
- 配套还有 `com.firedesert.aa.{DoService,Ga1Service,Ga2Service,HeService,PService,SjobService}`、`com.firedesert.radio.{SimService,UABServiceOne~Four}`、`com.handy.custom.DoService`、`GuardLive$ScRec$SreenBroadcastReceiver`（屏幕录制相关接收器）等十余个可疑服务与接收器，以及 AppLovin、Unity Ads、Fyber、IronSource、InMobi、Tapjoy、MoPub、Facebook Audience Network 全量广告 SDK 与 `BILLING` 权限。

**三、UTG 视角的可用信号（用于后续动态复核）**

- 最有效的触发锚点不是无障碍设置页，而是 **1×1 透明 Activity `com.firedesert.aa.KoAct`** 与**前台服务 `DoService`** 的反复出现：UTG 中出现“无界面、1×1、不可见窗口”的活动页，可直接判定其隐藏保活属性。
- 若后续观察到 `APPLICATION_DETAILS_SETTINGS` 跳转，应归因到广告 SDK 的“打开应用详情”能力，而不是应用自建的无障碍引导。

**四、覆盖边界与未决项**

- 字符串经 `ALLATORIxDEMO`（StringFog 变体）加密，Unity 业务逻辑位于 `libil2cpp.so`；本次未在 `libil2cpp.so` 内展开符号级检索，因此**不能排除**原生层存在运行期下发的无障碍/悬浮引导（可能性低：Manifest 无 a11y 服务与 `SYSTEM_ALERT_WINDOW` 权限，系统侧无法真正生效）。
- 受 14 次调用上限约束，未对 `com.firedesert.aa` 其余 20 余个类做逐一反编译，也未记录风险台账；本轮结论仅覆盖“无障碍引导”这一命题。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "Manifest 与 4 个主 DEX 完整可见且可确认：无任何 BIND_ACCESSIBILITY_SERVICE 无障碍服务声明、无 android.settings.ACCESSIBILITY_SETTINGS 跳转、无 android:description 无障碍说明，故无障碍引导链本身静态不可见（不存在）。应用字符串经 StringFog 变体 ALLATORIxDEMO 加密、业务主逻辑下沉至 libil2cpp.so，且大量广告/保活组件的行为参数可能由远端下发；本轮未对 libil2cpp.so 做符号级还原，故原生层是否在运行期拼装引导文案未完全排除。",
  "summary_one_liner": "该样本不具备无障碍引导链，实为 Unity 游戏外壳包裹的隐藏保活+静默广告家族样本（1×1 透明 Activity 与多前台服务互拉，配合全量广告 SDK）。",
  "disguise_identity": {
    "app_display_name": "Fire in the Desert",
    "claimed_brand_or_persona": "Fire in the Desert（Unity 休闲游戏，android:isGame=true，banner 与 Unity 启动主题）",
    "a11y_service_label": "无（Manifest 未声明任何 AccessibilityService，系统无障碍列表中不会出现该应用条目）",
    "identity_mismatch": true,
    "obfuscation_tricks": "入口 com.firedesert.StartActivity 使用 Theme.Translucent 作为启动透明壳；com.firedesert.aa.KoAct 以 setGravity(51)+1x1 像素窗口实现不可见 Activity；亮屏即 finish、onDestroy 立即 startForegroundService 形成互拉保活；字符串使用 StringFog 风格 ALLATORIxDEMO 解密；业务逻辑迁至 libil2cpp.so 与 nativeinit JNI 桥；Manifest 无 a11y 相关伪造项"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.firedesert.StartActivity（android:theme=Theme.Translucent，MAIN/LAUNCHER）",
      "trigger_event": "用户点击桌面图标（ACTION_MAIN + CATEGORY_LAUNCHER）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "全透明壳入口，无可见界面与文案",
      "user_action_requested": "无（无任何弹窗、无取消/跳过按钮，直接过渡）",
      "code_anchor": "#1 manifest:basic_info"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.unity3d.player.UnityPlayerActivity（android:label=@string/app_name，screenOrientation=sensorPortrait）",
      "trigger_event": "StartActivity 拉起 Unity 播放器 Activity，Unity 引擎初始化",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Fire in the Desert",
      "shown_text_zh": "显示名仅为游戏名，未见任何权限申请或安全提示文案",
      "user_action_requested": "无",
      "code_anchor": "#1 manifest:basic_info"
    },
    {
      "step": 3,
      "stage": "获权后动作",
      "screen_or_component": "com.firedesert.MainActivity（setContentView(2131165184) 后调用 u.ALLATORIxDEMO）",
      "trigger_event": "onCreate(Bundle)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "仅装载布局并转入混淆调度器，无引导性文案；同声明 native void nativeinit() 交由 il2cpp 处理",
      "user_action_requested": "无",
      "code_anchor": "com.firedesert.MainActivity#onCreate"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "com.firedesert.aa.KoAct（singleInstance、excludeFromRecents、finishOnTaskLaunch=false）",
      "trigger_event": "onCreate 设置 1x1 窗口；onResume 检测 PowerManager.isInteractive() 为真时 finish()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "不可见保活页：1×1 像素、左上角定位、亮屏即自毁",
      "user_action_requested": "无（用户完全无感）",
      "code_anchor": "com.firedesert.aa.KoAct#onCreate / com.firedesert.aa.KoAct#onResume"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "com.firedesert.aa.DoService（前台服务）及 Ga1Service/Ga2Service/HeService/PService/SjobService/SimService/UABServiceOne~Four",
      "trigger_event": "KoAct.onDestroy() 中 ContextCompat.startForegroundService(this, new Intent(this, DoService.class))",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "无",
      "shown_text_zh": "前台服务拉起以维持进程常驻，配合多进程（:PService/:SimService/:serviceOne~:serviceFour/:dService）分散存活",
      "user_action_requested": "无",
      "code_anchor": "com.firedesert.aa.KoAct#onDestroy"
    }
  ],
  "text_presentation_locations": [
    "无任何无障碍引导/说明文字呈现位置：Manifest 中无 AccessibilityService 声明，故系统无障碍列表内不会出现该应用的 android:description 条目",
    "4 个主 DEX 与 assets/audience_network.dex 均未检索到 android.settings.ACCESSIBILITY_SETTINGS / ACTION_ACCESSIBILITY_SETTINGS 常量，不存在跳转前教学页或设置页遮罩的代码锚点",
    "res/values/ids.xml 中的 accessibility_* 条目全部为 androidx 无障碍兼容框架的通用 id 资源，与应用自身引导无关",
    "唯一与“设置页”相关的常量为 android.settings.APPLICATION_DETAILS_SETTINGS（classes.dex / classes3.dex），归属广告 SDK 的跳应用详情能力，非无障碍引导",
    "res/values/strings.xml 中预筛命中的 Facebook/Google Play services 文案（Continue with Facebook、Enable Google Play services 等）为 Facebook SDK 与 Google Play services 可用性提示，与无障碍无关"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Enable Google Play services",
      "text_zh": "启用 Google Play 服务",
      "source_location": "res/values/strings.xml（Google Play services 可用性提示，SDK 资源）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "%1$s won't run without Google Play services, which are missing from your device.",
      "text_zh": "%1$s 在缺少 Google Play 服务的设备上无法运行。",
      "source_location": "res/values/strings.xml（SDK 资源）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Continue with Facebook",
      "text_zh": "使用 Facebook 继续",
      "source_location": "res/values/strings.xml（Facebook SDK 登录按钮文案）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "WebView login requires INTERNET permission",
      "text_zh": "WebView 登录需要 INTERNET 权限",
      "source_location": "res/values/strings.xml（SDK 资源）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Fire in the Desert",
      "text_zh": "沙漠之火",
      "source_location": "res/values/strings.xml: app_name（Manifest android:label / UnityPlayerActivity android:label）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不存在无障碍拒权反馈循环；应用从不读取 getEnabledAccessibilityServiceList/getInstalledAccessibilityServiceList 用于引导判断（仅 androidx 兼容库内出现该符号）。实际存在的“循环”是保活闭环：KoAct.onResume 在亮屏时 finish()，onDestroy 立刻 startForegroundService(DoService)，服务侧再拉起 KoAct。",
    "overlay_or_fake_settings": "无。Manifest 未申请 SYSTEM_ALERT_WINDOW，也未声明无障碍服务，无法叠放引导遮罩或伪造系统无障碍开关页；唯一近似行为是 1×1 像素的不可见 Activity 窗口（KoAct），其目的为常驻而非引导。",
    "restricted_settings_13plus_coaching": "无。未检索到 ACTION_MANAGE_UNKNOWN_APP_SOURCES / REQUEST_INSTALL_PACKAGES 引导链；DEX 线索中的 SESSION_INSTALLER 未在 Manifest 中体现为安装器绕过逻辑。",
    "post_grant_anti_removal": "无（无无障碍权限可撤，故不存在自授权或 GLOBAL_ACTION_BACK/HOME 阻止撤权）。但存在进程级反清理能力：GuardLive$ScRec$SreenBroadcastReceiver 屏幕状态监听、多进程服务、JobService 与开机 RECEIVE_BOOT_COMPLETED 自启。",
    "benign_graceful_degradation": "无（不适用：应用本身不申请无障碍，也未提供手动/ADB 替代路径说明）"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "不应围绕 ACCESSIBILITY_SETTINGS 设钩。建议在冷启动后持续监测两类页面事件：(1) 出现 package=com.fire.the.desert.in 且 activity=com.firedesert.aa.KoAct 的 1×1 不可见窗口；(2) 出现 com.firedesert.aa.DoService 前台服务通知与 KoAct/DoService 交替出现的 activity 切换序列。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动透明壳入口页",
        "page_identifier": "com.firedesert.StartActivity（Theme.Translucent，无任何可见控件）",
        "why_most_useful": "确认入口与展示名 Fire in the Desert 的强绑定，且证明启动阶段不存在任何权限引导弹窗",
        "observable_utg_signals": ["activity 名称为 StartActivity 但可见节点树为空", "无任何文本/按钮节点的全透明窗口"]
      },
      {
        "page_role": "1×1 隐藏保活 Activity 页",
        "page_identifier": "com.firedesert.aa.KoAct（singleInstance / excludeFromRecents）",
        "why_most_useful": "这是该样本最独特的可观测恶意特征，可据此把样本归入隐藏保活型而非无障碍引导型",
        "observable_utg_signals": ["窗口边界为 1×1 像素且位于屏幕左上角", "页面不可见却频繁 onCreate/onResume/onDestroy 切换", "伴随 DoService 前台服务通知同时出现"]
      },
      {
        "page_role": "Unity 游戏主界面",
        "page_identifier": "com.unity3d.player.UnityPlayerActivity（label=Fire in the Desert，sensorPortrait）",
        "why_most_useful": "作为“良性游戏外壳”的对照页，用于区分正常玩法与后台静默广告/保活行为",
        "observable_utg_signals": ["Unity 引擎渲染层节点", "无权限申请弹窗出现"]
      },
      {
        "page_role": "系统应用详情页（若被广告 SDK 拉起）",
        "page_identifier": "Settings 的 com.android.settings.applications.InstalledAppDetails（APPLICATION_DETAILS_SETTINGS）",
        "why_most_useful": "用于核实跳转归属：若确实出现，应归因广告 SDK 而非应用自建无障碍教学",
        "observable_utg_signals": ["当前前台包为 com.android.settings 且携带应用包名", "本应用处于后台、无对应引导文案"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在两处盲区：(1) 业务主逻辑位于 libil2cpp.so 且字符串经 ALLATORIxDEMO 加密，本轮未做原生层符号级还原，无法完全排除运行期由远端下发的引导文案；(2) 若远端下发的是纯图片/全屏 WebView 广告，UTG 文本信号可能为空，需结合网络流量与截图复核。另需注意：静态“加壳”判定为 False 且本样本不属于加壳样本，其静态不可见性来自 il2cpp + StringFog，而非 VMP。"
  },
  "behavior_pattern_tags": [
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED"
  ],
  "code_anchors": [
    "com.firedesert.aa.KoAct#onCreate",
    "com.firedesert.aa.KoAct#onResume",
    "com.firedesert.aa.KoAct#onDestroy",
    "com.firedesert.MainActivity#onCreate",
    "#1 manifest:components"
  ]
}
```

</details>
