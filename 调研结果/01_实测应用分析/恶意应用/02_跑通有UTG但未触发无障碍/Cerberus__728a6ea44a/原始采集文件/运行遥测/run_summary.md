# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:02:55
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.uxlgtsvfdc.zipvwntdy`（静态标签：`malicious` / `Cerberus` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`success`（共执行 2 步，UTG 唯一节点 `1` 个，有向边 `1` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.uxlgtsvfdc.zipvwntdy` / `HerwEHxXO` | `-` | 1 | 0 / 是 | `wait` | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.uxlgtsvfdc.zipvwntdy` / `HerwEHxXO` | `-` | 1 | 0 / 是 | `terminate` → Launched Flash Player-branded app (com.uxlgtsvfdc.zipvw | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.uxlgtsvfdc.zipvwntdy/HerwEHxXO`)**: (空文本)
- **Step 2 (`com.uxlgtsvfdc.zipvwntdy/HerwEHxXO`)**: (空文本)

## 中文逐页引导链路解读

> **全链路总结**：应用启动后进入隐藏 Activity HerwEHxXO，页面无可见应用内 UI，仅伴随 Google 系统备份通知；等待刷新未显示无障碍授权弹窗，随后在疑似无障碍服务提示/隐藏 Activity 触发点终止，呈现隐藏入口与授权诱导痕迹。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “您的数据尚未备份”（系统通知横幅，Step 1/2）
- 英文 -> “立即添加备份账户”（系统通知横幅，Step 1/2）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: HerwEHxXO** | 进入 HerwEHxXO 空白页，无应用内文字；仅见系统通知“数据未备份/添加备份账户”，等待刷新仍未出现授权提示。 | `step_01_action.png` |
| 2 | **Step 2: HerwEHxXO** | 仍为同一空白 Activity；未见应用内遮罩，探针在疑似无障碍服务授权节点终止，并记录隐藏 Activity 触发。 | `step_02_action.png` |
