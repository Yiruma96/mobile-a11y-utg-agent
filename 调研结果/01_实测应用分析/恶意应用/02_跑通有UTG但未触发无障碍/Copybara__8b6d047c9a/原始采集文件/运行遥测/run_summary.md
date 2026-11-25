# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:07:02
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.orijucaroma.newicon`（静态标签：`malicious` / `Copybara` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `3` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.orijucaroma.newicon` / `main` | `-` | 1 | 0 / 是 | `click` → [540, 1560] | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.orijucaroma.newicon` / `main` | `-` | 3 | 63 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,121 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.orijucaroma.newicon` / `main` | `-` | 10 | 326 / 否 | `click` → [10] Button text="Continue" (click) center=(540,1752) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.orijucaroma.newicon` / `main` | `-` | 3 | 63 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,121 | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.orijucaroma.newicon` / `main` | `-` | 3 | 63 / 否 | `system_button` → Back | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.orijucaroma.newicon` / `main` | `-` | 10 | 326 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.orijucaroma.newicon` / `main` | `-` | 10 | 326 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.orijucaroma.newicon` / `main` | `-` | 10 | 326 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.orijucaroma.newicon/main`)**: (空文本)
- **Step 2 (`com.orijucaroma.newicon/main`)**: `No internet` | `Please make sure you are connected to the internet` | `OK`
- **Step 3 (`com.orijucaroma.newicon/main`)**: `Pv3qrDFdzRl0fhmsf83FqGZJFDou2N6d85cNOu+Uu9tMB76riKoncSS` | `Certificato HYPE` | `Update your Certificato HYPE.` | `Click the "Continue" button and follow the installation` | `1 Open settings` | `2 In Accessibility, open the "Downloaded Services" or "` | `3 Activate the "Certificato HYPE" option.` | `Continue`
- **Step 4 (`com.orijucaroma.newicon/main`)**: `No internet` | `Please make sure you are connected to the internet` | `OK`
- **Step 5 (`com.orijucaroma.newicon/main`)**: `No internet` | `Please make sure you are connected to the internet` | `OK`
- **Step 6 (`com.orijucaroma.newicon/main`)**: `Pv3qrDFdzRl0fhmsf83FqGZJFDou2N6d85cNOu+Uu9tMB76riKoncSS` | `Certificato HYPE` | `Update your Certificato HYPE.` | `Click the "Continue" button and follow the installation` | `1 Open settings` | `2 In Accessibility, open the "Downloaded Services" or "` | `3 Activate the "Certificato HYPE" option.` | `Continue`
- **Step 7 (`com.orijucaroma.newicon/main`)**: `Pv3qrDFdzRl0fhmsf83FqGZJFDou2N6d85cNOu+Uu9tMB76riKoncSS` | `Certificato HYPE` | `Update your Certificato HYPE.` | `Click the "Continue" button and follow the installation` | `1 Open settings` | `2 In Accessibility, open the "Downloaded Services" or "` | `3 Activate the "Certificato HYPE" option.` | `Continue`
- **Step 8 (`com.orijucaroma.newicon/main`)**: `Pv3qrDFdzRl0fhmsf83FqGZJFDou2N6d85cNOu+Uu9tMB76riKoncSS` | `Certificato HYPE` | `Update your Certificato HYPE.` | `Click the "Continue" button and follow the installation` | `1 Open settings` | `2 In Accessibility, open the "Downloaded Services" or "` | `3 Activate the "Certificato HYPE" option.` | `Continue`

## 中文逐页引导链路解读

> **全链路总结**：该应用从伪造的“Certificato HYPE”证书更新页与无障碍启用引导入口开始，反复以英文“No internet”弹窗阻断并诱导用户点击继续，随后通过静态回退依次跳转Common.StartActivity、service2_BR与AdminReceiver2，指向无障碍/设备管理授权链；拒权结果未测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 意大利语/英语 -> “HYPE证书；更新您的HYPE证书。点击‘Continue’并按照安装步骤操作”（伪造HYPE证书页）
- 英语 -> “打开设置；在无障碍中进入‘Downloaded Services’或‘Installed Services’；启用‘Certificato HYPE’选项”（伪造HYPE证书页）
- 英语 -> “无网络；请确认已连接互联网；确定”（No internet错误弹窗，step_02/04/05）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: main** | 当前为未采集文本的伪造HYPE证书页，点击Continue尝试开始安装引导，未出现通知或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: main** | 弹出英文“No internet/请确认联网/OK”错误框；点击OK关闭后重试继续，未出现通知或遮罩。 | `step_02_action.png` |
| 3 | **Step 3: main** | 伪造HYPE证书页展示更新证书及无障碍启用三步说明；点击Continue继续，未出现通知或遮罩。 | `step_03_action.png` |
| 4 | **Step 4: main** | 再次弹出英文无网络提示与OK按钮；点击OK后计划返回查看原生备用指南，弹窗仍是阻断点。 | `step_04_action.png` |
| 5 | **Step 5: main** | 同一“No internet/请联网/OK”弹窗持续阻断；改用系统返回键关闭，仍未进入系统无障碍设置，无通知遮罩。 | `step_05_action.png` |
| 6 | **Step 6: main** | 仍停留伪造HYPE证书页；静态回退触发跳转Common.StartActivity，绕过页面交互继续安装链路。 | `step_06_screen.png` |
| 7 | **Step 7: main** | 证书页未变，静态回退跳至service2$service2_BR服务组件，疑似转入后台启用流程，无通知遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: main** | 证书页仍显示；静态回退跳至AdminReceiver2设备管理接收器，疑似请求设备管理权限，未现通知遮罩。 | `step_08_screen.png` |
