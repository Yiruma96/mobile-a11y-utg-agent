# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:29:02
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.infosoft.docutain`（静态标签：`malicious` / `GodFather` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `3` 个，有向边 `4` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_A11Y_SETTINGS`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | hooks=`['HOOK_A11Y_SETTINGS']` | overlays=`0` | texts=`Back / Accessibility / Search settings / DOWNLOADED APPS / Android Protect`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.infosoft.docutain` / `datamediaGrenadian` | `-` | 9 | 266 / 否 | `click` → [4] Button text="Scan" id=scan (click) center=(540,886) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 214 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.infosoft.docutain/datamediaGrenadian`)**: `Android Protect` | `No harmful apps found` | `Android protect hasn't scanned yet` | `Scan` | `Recently scanned apps` | `+20 more` | `Apps have not been scanned yet` | `Android Protect regularly checks your apps and device f` | `Learn more`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Android Protect` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用先以假冒“Android Protect”安全扫描页显示未发现有害应用并诱导点击Scan，随后跳转系统无障碍设置引导开启“Android Protect”服务；服务详情页展示开关与快捷方式，拒权后自动重新拉起无障碍设置，体现社工诱导与反复施压。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English -> 安卓保护（假冒安全品牌，Step1/通知/无障碍页）
- English -> 未发现有害应用（Step1）
- English -> Android Protect 尚未扫描（Step1）
- English -> 扫描（Step1）
- English -> 最近扫描的应用（Step1）
- English -> 还有20项（Step1）
- English -> 应用尚未被扫描（Step1）
- English -> Android Protect定期检查应用与设备的有害行为，发现风险会通知你（Step1）
- English -> 了解更多（Step1）
- English -> 手机正受Android Protect保护（通知横幅）
- English -> 请激活以使更新生效（通知/无障碍页）
- English -> 使用Android Protect（服务详情页）
- English -> Android Protect快捷方式（服务详情页）
- English -> 未提供描述（服务详情页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: datamediaGrenadian** | 假冒安全扫描页：英文称未发现有害应用、尚未扫描，含Scan按钮；点击Scan，顶部有手机受保护等通知，无遮罩。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 系统无障碍列表：DOWNLOADED APPS下Android Protect为Off，通知催促请激活；捕获无障碍钩子/探针后终止，无遮罩。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍停在无障碍设置页且文本为空；应用继续推送请激活及空正文通知，遮罩为0。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳转后2.0秒探针：页面仍为无障碍设置、无界面文本；请激活与空正文通知持续存在，遮罩为0，未发生点击。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 无障碍服务详情页：标题Android Protect，Use开关为Off、快捷方式Off、未提供描述；本步查看详情，遮罩0。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 服务详情页/警告检查：仍见Android Protect与Use开关Off、快捷方式Off；未捕获系统警告弹窗，遮罩0，通知仍催促激活。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒权后返回无障碍列表：Android Protect仍为Off，通知继续请激活；Back_refuse触发RELAUNCHED_A11Y_SETTINGS，自动重拉设置页。 | `step_02_refusal_2000ms_screen.png` |
