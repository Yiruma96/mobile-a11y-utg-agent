# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:01:44
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.nnawozvvi.pamwhbawm`（静态标签：`malicious` / `Teabot` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`success`（共执行 1 步，UTG 唯一节点 `1` 个，有向边 `0` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.nnawozvvi.pamwhbawm` / `InioawndOIADNwaiond` | `-` | 2 | 23 / 是 | `terminate` → App flowed from launch to the System Accessibility Sett | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.nnawozvvi.pamwhbawm/InioawndOIADNwaiond`)**: `QR Code Scanner: Add-On`

## 中文逐页引导链路解读

> **全链路总结**：应用启动后以“QR Code Scanner: Add-On”附加组件外观进入，随即转向系统无障碍设置页索取启用无障碍权限；探针未做拒权测试，最终以终止结束。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “二维码扫描器：附加组件”（启动页，伪装为工具类附加功能）
- 英文 -> “You need ……”（系统无障碍设置页，截断的启用无障碍引导文案）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: InioawndOIADNwaiond** | 启动页显示“QR Code Scanner: Add-On（二维码扫描器：附加组件）”，无通知横幅与遮罩；探针记录其跳转系统无障碍设置后终止。 | `step_01_action.png` |
