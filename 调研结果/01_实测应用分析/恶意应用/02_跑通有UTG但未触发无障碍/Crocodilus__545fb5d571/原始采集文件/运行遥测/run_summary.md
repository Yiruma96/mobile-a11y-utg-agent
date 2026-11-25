# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:24:42
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`stinky.massive`（静态标签：`malicious` / `Crocodilus` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `6` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.packageinstaller` / `PackageInstallerActivity` | `-` | 4 | 106 / 否 | `click` → [4] Button text="Settings" id=button1 (click) center=(8 | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$ManageAppExternalSourcesActivity` | `-` | 10 | 294 / 否 | `click` → [9] Switch id=switch_widget (unchecked) center=(972,707 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$ManageAppExternalSourcesActivity` | `-` | 10 | 294 / 否 | `system_button` → Back | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.packageinstaller` / `PackageInstallerActivity` | `-` | 4 | 59 / 否 | `click` → [4] Button text="Install" id=button1 (click) center=(88 | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `wait` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `sizing.catsup.thriving` / `WjsaScCKITSBsc` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `sizing.catsup.thriving` / `WjsaScCKITSBsc` | `-` | 6 | 247 / 否 | `click` → [5] Button text="Erişilebilirliği Etkinleştir" (click)  | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.packageinstaller/PackageInstallerActivity`)**: `Chrome` | `For your security, your phone is not allowed to install` | `Cancel` | `Settings`
- **Step 2 (`com.android.settings/Settings$ManageAppExternalSourcesActivity`)**: `Back` | `Install unknown apps` | `Search settings` | `Chrome` | `1.0` | `Allow from this source` | `Your phone and personal data are more vulnerable to att`
- **Step 3 (`com.android.settings/Settings$ManageAppExternalSourcesActivity`)**: `Back` | `Install unknown apps` | `Search settings` | `Chrome` | `1.0` | `Allow from this source` | `Your phone and personal data are more vulnerable to att`
- **Step 4 (`com.google.android.packageinstaller/PackageInstallerActivity`)**: `Chrome` | `Do you want to install this application?` | `Cancel` | `Install`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 7 (`sizing.catsup.thriving/WjsaScCKITSBsc`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 8 (`sizing.catsup.thriving/WjsaScCKITSBsc`)**: `Erişilebilirlik İzni` | `Chrome Icon` | `Erişilebilirlik İzni Gerekli` | `Uygulamanın çalışabilmesi için erişilebilirlik izni ver` | `Erişilebilirliği Etkinleştir` | `Erişilebilirlik ayarları, yüklü uygulamalar altında vey`

## 中文逐页引导链路解读

> **全链路总结**：应用先借 Chrome 触发系统安装器，诱导用户放行未知来源并确认安装内嵌 APK，随后回到桌面并通过静态跳转拉起新包。最终以土耳其语“无障碍权限必需”页面诱导开启无障碍服务，呈现典型投放器与权限滥用链路。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> 出于安全，你的手机不允许此来源安装未知应用（Step 1 系统安装器拦截页）
- 英语 -> 未知应用更易攻击手机和个人数据，安装即自担风险（Step 2 系统设置授权页）
- 英语 -> 是否安装此应用？（Step 4 系统安装确认页）
- 土耳其语 -> 需要无障碍权限（Step 8 无障碍诱导页标题）
- 土耳其语 -> 应用要运行，你必须授予无障碍权限（Step 8 无障碍诱导页说明）
- 土耳其语 -> 启用无障碍（Step 8 无障碍诱导页按钮）
- 土耳其语 -> 无障碍设置可在已安装应用或无障碍栏目中找到（Step 8 设置指引）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: PackageInstallerActivity** | 系统安装器拦截页：提示出于安全不允许Chrome安装未知应用，含取消/设置；本步点击“设置”转去授权，无通知与遮罩。 | `step_01_action.png` |
| 2 | **Step 2: Settings$ManageAppExternal** | 系统设置“安装未知应用”页：为Chrome开启“Allow from this source”；页面警告未知应用风险。本步勾选开关，无通知与遮罩。 | `step_02_action.png` |
| 3 | **Step 3: Settings$ManageAppExternal** | 同一授权页：Chrome的“允许此来源”开关已打开，页面仍显示安全风险说明；本步按返回键回到投放器，无通知与遮罩。 | `step_03_action.png` |
| 4 | **Step 4: PackageInstallerActivity** | 系统安装确认页：询问是否安装该应用，含取消/安装；本步点击“安装”确认装入内嵌APK，无通知与遮罩。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 回到桌面启动器：显示应用列表、日期、信息/Chrome/搜索等；安装完成后等待观察是否出现新图标，无通知与遮罩。 | `step_05_action.png` |
| 6 | **Step 6: NexusLauncherActivity** | 仍在桌面启动器，界面无变化；探针以静态活动跳转尝试拉起目标组件，未出现通知或遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: WjsaScCKITSBsc** | 跳转至新包sizing.catsup.thriving的空白活动，界面仍残留桌面元素；无可见诱导文案，随后继续静态跳转，无通知与遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: WjsaScCKITSBsc** | 土耳其语无障碍诱导页：称应用运行必须授予无障碍权限，并指引到设置；本步点击“启用无障碍”按钮，无通知与遮罩。 | `step_08_action.png` |
