# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:07:47
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.android.system.qspas10`（静态标签：`malicious` / `Unattributed` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`hook_captured`（共执行 6 步，UTG 唯一节点 `8` 个，有向边 `12` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 6 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_06_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`hesy.poexdt.lmqsoqy/hesy.poexdt.lmqsoqy.hydfxatsbb` | hooks=`[]` | overlays=`0` | texts=`Access Page / S.A.C ITAÚ / Este aplicativo requer permissão de acesso para funcionar. Por favor, permita para continuar. / 1 / Click on continue`
- **Back 后 +5.5s**：`hesy.poexdt.lmqsoqy/hesy.poexdt.lmqsoqy.hydfxatsbb` | hooks=`[]` | overlays=`0` | texts=`Access Page / S.A.C ITAÚ / Este aplicativo requer permissão de acesso para funcionar. Por favor, permita para continuar. / 1 / Click on continue`
- **Back 后 +10.5s**：`hesy.poexdt.lmqsoqy/hesy.poexdt.lmqsoqy.hydfxatsbb` | hooks=`[]` | overlays=`0` | texts=`Access Page / S.A.C ITAÚ / Este aplicativo requer permissão de acesso para funcionar. Por favor, permita para continuar. / 1 / Click on continue`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.vpndialogs` / `ConfirmDialog` | `-` | 4 | 207 / 否 | `click` → [4] Button text="OK" id=button1 (click) center=(887,137 | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$ManageAppExternalSourcesActivity` | `-` | 10 | 298 / 否 | `click` → [9] Switch id=switch_widget (unchecked) center=(972,707 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$ManageAppExternalSourcesActivity` | `-` | 10 | 298 / 否 | `click` → [1] ImageButton desc="Back" (click) center=(77,160) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.packageinstaller` / `PackageInstallerActivity` | `-` | 4 | 63 / 否 | `click` → [4] Button text="Install" id=button1 (click) center=(88 | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `hesy.poexdt.lmqsoqy` / `tlmaqgmrhnb` | `-` | 5 | 98 / 否 | `wait` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 11 | 217 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_06_layout.xml` + `step_06_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.vpndialogs/ConfirmDialog`)**: `Connection request` | `S.A.C ITAÚ wants to set up a VPN connection that allows` | `Cancel` | `OK`
- **Step 2 (`com.android.settings/Settings$ManageAppExternalSourcesActivity`)**: `Back` | `Install unknown apps` | `Search settings` | `S.A.C ITAÚ` | `1.0` | `Allow from this source` | `Your phone and personal data are more vulnerable to att`
- **Step 3 (`com.android.settings/Settings$ManageAppExternalSourcesActivity`)**: `Back` | `Install unknown apps` | `Search settings` | `S.A.C ITAÚ` | `1.0` | `Allow from this source` | `Your phone and personal data are more vulnerable to att`
- **Step 4 (`com.google.android.packageinstaller/PackageInstallerActivity`)**: `S.A.C ITAÚ` | `Do you want to install this application?` | `Cancel` | `Install`
- **Step 5 (`hesy.poexdt.lmqsoqy/tlmaqgmrhnb`)**: `S.A.C ITAÚ` | `Aguarde o procedimento...` | `Otimizando sistema` | `Installing...` | `✓ Google Play Protect verificado`
- **Step 6 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Access Page` | `S.A.C ITAÚ` | `Este aplicativo requer permissão de acesso para funcion` | `1` | `Click on continue` | `2` | `Find downloaded apps` | `3` | `Enable S.A.C ITAÚ` | `CONTINUAR`

## 中文逐页引导链路解读

> **全链路总结**：应用先骗取VPN和未知来源安装权限，安装伪装成S.A.C ITAÚ的恶意包，再用“安装中/已验证”和三步教程诱导开启无障碍；拒权后反复重拉同一诱导页。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> “S.A.C ITAÚ 希望建立 VPN 连接以监控网络流量，仅信任来源时接受”（step_01 VPN授权弹窗）
- 英语 -> “允许来自此来源”及未知应用风险警告（step_02/03 未知来源设置页）
- 葡萄牙语/英语 -> “请稍候…/正在优化系统”“正在安装…”“✓ Google Play Protect 已验证”（step_05 恶意安装页）
- 葡萄牙语 -> “此应用需要访问权限才能运行，请允许以继续”（step_06/refusal 无障碍引导页）
- 英语/葡语 -> “点击继续 / 查找已下载应用 / 启用 S.A.C ITAÚ”及“CONTINUAR”（step_06/refusal 无障碍引导页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ConfirmDialog** | VPN授权弹窗：英文称S.A.C ITAÚ请求监控网络流量，仅信任时接受；点击OK授予VPN，顶部有Google备份通知。 | `step_01_action.png` |
| 2 | **Step 2: Settings$ManageAppExternal** | 未知来源设置页：显示S.A.C ITAÚ 1.0，英文警告未知应用风险；勾选“允许来自此来源”开关以放行安装，顶部备份通知。 | `step_02_action.png` |
| 3 | **Step 3: Settings$ManageAppExternal** | 同一未知来源页：开关已开启，英文风险提示仍在；点击左上返回恶意应用继续诱导，全程无遮罩，通知横幅保留。 | `step_03_action.png` |
| 4 | **Step 4: PackageInstallerActivity** | 系统安装确认页：英文“是否安装此应用？”，显示S.A.C ITAÚ；点击Install继续安装恶意载荷，通知横幅仍在。 | `step_04_action.png` |
| 5 | **Step 5: tlmaqgmrhnb** | 恶意安装页：葡文“请稍候/优化系统”、英文“安装中”及“Play Protect已验证”伪装可信；等待后触发广播。 | `step_05_action.png` |
| 6 | **Step 6: [无障碍列表页]** | 无障碍引导页：葡文称需访问权限，英文三步“继续/找应用/启用S.A.C ITAÚ”；点CONTINUAR后捕获钩子即终止。 | `step_06_screen.png` |
| 7 | **跳后探针 +0.8s** | 跳后0.8秒探针：仍停在无障碍设置页，界面文本为空、遮罩0；S.A.C与Google备份通知仍在，无用户操作。 | `step_06_probe_800ms_screen.png` |
| 8 | **跳后探针 +2.0s** | 跳后2秒探针：无障碍设置页持续空白、无遮罩；恶意应用S.A.C与Google备份通知仍挂起，未见新弹窗。 | `step_06_probe_2000ms_screen.png` |
| 9 | **服务详情页** | 无障碍设置详情页：显示DOWNLOADED APPS下S.A.C ITAÚ为Off，另有屏幕阅读/显示项；仅巡检未授权，通知仍在。 | `step_06_service_detail_screen.png` |
| 10 | **系统警告弹窗(点Deny)** | 巡检时出现系统“深色主题”说明弹窗，含Got it；无权限授权动作，遮罩0，S.A.C与备份通知仍在。 | `step_06_system_warning_screen.png` |
| 11 | **拒权返回 +2.0s** | 拒权后2秒：恶意应用重拉葡语“访问页”，称需访问权限才能继续，含三步教程与CONTINUAR；记录为重启诱导弹窗。 | `step_06_refusal_2000ms_screen.png` |
| 12 | **拒权返回 +10.5s** | 拒权后10.5秒：同一葡语“访问页”与三步教程仍在，未见权限关闭/取消，动作仍记为重启诱导弹窗，通知横幅保留。 | `step_06_refusal_10500ms_screen.png` |
