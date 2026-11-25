# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:50:20
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`melt.pull.leg`（静态标签：`malicious` / `BankBot` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`success`（共执行 1 步，UTG 唯一节点 `1` 个，有向边 `0` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `melt.pull.leg` / `nwv` | `-` | 26 | 234 / 否 | `terminate` → App (BankBot, disguised as 'Asistan') launched a Cordov | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`melt.pull.leg/nwv`)**: `Erişilebilirlik` | `Accessibility Service` | `DOWNLOADED SERVICES` | `Select to speak` | `OFF` | `Aktif Ediniz` | `Switch Access` | `TalkBack` | `SCREEN READERS` | `Text-to-speech output`

## 中文逐页引导链路解读

> **全链路总结**：该应用伪装为“Asistan/助手”，通过 Cordova WebView 静默跳转至系统无障碍设置页，借土语“Aktif Ediniz”诱导用户为恶意服务开启无障碍权限；本次未出现通知或遮罩，动态探针在该授权页终止，拒权结果未测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 土耳其语 -> “请激活/启用”（Step 1 系统无障碍设置页的 Aktif Ediniz 提示）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: nwv** | 系统无障碍设置页，土语“Aktif Ediniz”即“请激活”，以开启无障碍服务诱导授权；无通知/遮罩，页面终止。 | `step_01_action.png` |
