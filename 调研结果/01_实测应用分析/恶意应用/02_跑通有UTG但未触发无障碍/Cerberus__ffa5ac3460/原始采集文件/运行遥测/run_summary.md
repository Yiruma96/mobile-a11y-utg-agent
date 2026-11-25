# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:05:37
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.mwmnfwt.arhkrgajn`（静态标签：`malicious` / `Cerberus` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`success`（共执行 1 步，UTG 唯一节点 `1` 个，有向边 `0` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.mwmnfwt.arhkrgajn` / `AzdwTPqtXIfh` | `-` | 1 | 0 / 是 | `terminate` → App launched and navigated to System Accessibility Sett | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.mwmnfwt.arhkrgajn/AzdwTPqtXIfh`)**: (空文本)

## 中文逐页引导链路解读

> **全链路总结**：该应用启动后直接进入系统无障碍设置页，疑似借“Flash Player服务”名称诱导用户开启高风险无障碍授权；页面无应用内可见文案，仅见系统备份通知，最终探针终止且授权未测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “你的数据未备份”（系统通知横幅，step_01）
- 英文 -> “立即添加备份账户”（系统通知横幅，step_01）
- 英文 -> “Flash Player Serv…”（系统无障碍设置页，step_01）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: AzdwTPqtXIfh** | 系统无障碍设置页，随机标题；通知横幅意译“数据未备份/立即添加备份账户”，疑似以“Flash Player服务”诱导开启授权，无遮罩，探针终止。 | `step_01_action.png` |
