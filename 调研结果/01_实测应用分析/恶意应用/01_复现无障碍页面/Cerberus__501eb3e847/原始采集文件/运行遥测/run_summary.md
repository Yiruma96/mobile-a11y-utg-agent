# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:47:09
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.wood.area`（静态标签：`malicious` / `Cerberus` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `6` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / Messages / Chrome / Search`
- **Back 后 +5.5s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / Messages / Chrome / Search`
- **Back 后 +10.5s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / Messages / Chrome / Search`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.wood.area` / `mjpzwvrpys` | `-` | 1 | 0 / 是 | `click` → [540, 1637] | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.wood.area` / `mjpzwvrpys` | `-` | 7 | 281 / 否 | `click` → [5] View id=btn (click) center=(540,1503) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 219 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.wood.area/mjpzwvrpys`)**: (空文本)
- **Step 2 (`com.wood.area/mjpzwvrpys`)**: `Accessibility` | `android-flat` | `Android Güncelleme` | `Bir sonraki ekranda erişilebilirlik izni vermeniz gerek` | `white-tick-png-8` | `Devam Et`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Lütfen izin veriniz.` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用启动后在 WebView 中用土耳其语伪装成“Android 更新”，以“不更新手机就会暴露于所有攻击”的恐吓话术，诱导用户进入系统无障碍设置，并开启名为“Lütfen izin veriniz.（请授予权限）”的服务。用户点击 Deny 拒绝授权后，应用静默回到桌面，没有异常，也没有二次弹窗，链路以 GRACEFUL_STAY_OR_DEGRADE 结束。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 土耳其语 -> “Devam Et”（继续）（WebView 首屏与更新页按钮）：用中性按钮文案降低用户戒心，推动进入下一屏授权。
- 土耳其语 -> “Android Güncelleme”（Android 更新）（step_02 标题）：把恶意页面伪装成系统更新组件。
- 土耳其语 -> “Bir sonraki ekranda erişilebilirlik izni vermeniz gerekmektedir. Yüklü servisler menüsünde veya Android Güncelleme'ye tıklayabilirsiniz. Telefonunuzu güncellemediğiniz takdirde tüm saldırılara açık hale gelecektir.”（下一屏需要授予无障碍权限，可在已安装服务菜单中或点击 Android 更新；若不更新手机，将对所有攻击敞开）（step_02 正文）：用安全恐吓话术边制造恐慌，边直接指路授权入口。
- 土耳其语 -> “Lütfen izin veriniz.”（请授予权限）（无障碍列表页条目与服务详情页服务名）：把恶意无障碍服务命名为看似系统提示的名称，以骗取用户授予权限。
- 英语（系统高危弹窗）-> “Allow Lütfen izin veriniz. to have full control of your device?”（允许其完全控制你的设备？），并列出 “View and control screen / View and perform actions”：系统会随之明示“读取全屏内容、代替用户操作”的权限，这是该攻击真正想取得的权限。

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: mjpzwvrpys** | 应用内 WebView 首屏，无可见文案，标题为随机串 mjpzwvrpys；点击坐标命中土耳其语“Devam Et（继续）”按钮，促使页面推进到无障碍授权环节；通知栏还一直挂着 Google 未备份提示。 | `step_01_action.png` |
| 2 | **Step 2: mjpzwvrpys** | WebView 伪装“Android Güncelleme（Android 更新）”页，谎称不更新手机就会暴露于所有攻击，并要求在下一屏授予无障碍权限；点击“Devam Et”后跳转到系统设置。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 系统无障碍设置列表，已出现“Lütfen izin veriniz.（请授予权限）”条目且开关关闭；探针捕获 HOOK_A11Y_SETTINGS 后自动终止页面，没有遮罩。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转后 0.8 秒仍停在无障碍列表页，overlays=0，无新增文本或浮层：应用已把用户直接带到系统授权入口，等待用户自行点击服务项。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后 2.0 秒仍在无障碍列表页，overlays=0，未见任何诱导弹窗覆盖：说明诱导全部在 WebView 阶段完成，系统页只负责落点。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | 无障碍服务详情页，服务名被设为土耳其语“Lütfen izin veriniz.（请授予权限）”，描述为“未提供”，开关关闭；这是用伪装名称骗取授权的典型做法。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 系统高危授权确认框，说明该服务可读取全屏内容并代替用户操作；本步选择“Deny（拒绝）”，未授予无障碍权限。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 拒绝授权后 2 秒已回到系统桌面，应用未崩溃、未再次拉起授权页，呈现 GRACEFUL_STAY_OR_DEGRADE 的静默降级。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒绝授权后 10.5 秒仍停在桌面，无覆盖层、无二次诱导弹窗；应用保持静默，处于降级驻留状态，等待后续触发。 | `step_03_refusal_10500ms_screen.png` |
