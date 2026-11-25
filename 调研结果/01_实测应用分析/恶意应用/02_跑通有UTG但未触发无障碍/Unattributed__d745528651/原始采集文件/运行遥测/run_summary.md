# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:17:29
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.sec.android.app.sysupdate`（静态标签：`malicious` / `Unattributed` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.sec.android.app.sysupdate` / `LauncherAlias` | `-` | 18 | 15 / 否 | `click` → [5] Button text="1" (click) center=(346,1262) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.sec.android.app.sysupdate` / `LauncherAlias` | `-` | 18 | 16 / 否 | `click` → [6] Button text="2" (click) center=(539,1262) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.sec.android.app.sysupdate` / `LauncherAlias` | `-` | 18 | 17 / 否 | `click` → [7] Button text="3" (click) center=(732,1262) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.sec.android.app.sysupdate` / `LauncherAlias` | `-` | 18 | 18 / 否 | `click` → [8] Button text="4" (click) center=(346,1428) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.sec.android.app.sysupdate` / `LauncherAlias` | `-` | 18 | 19 / 否 | `click` → [18] ImageButton id=ok (click) center=(732,1954) | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.sec.android.app.sysupdate` / `LauncherAlias` | `-` | 18 | 15 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.sec.android.app.sysupdate` / `LauncherAlias` | `-` | 18 | 15 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.sec.android.app.sysupdate` / `LauncherAlias` | `-` | 18 | 15 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.sec.android.app.sysupdate/LauncherAlias`)**: `A` | `B` | `C` | `1` | `2` | `3` | `4` | `5` | `6` | `7`
- **Step 2 (`com.sec.android.app.sysupdate/LauncherAlias`)**: `•` | `A` | `B` | `C` | `1` | `2` | `3` | `4` | `5` | `6`
- **Step 3 (`com.sec.android.app.sysupdate/LauncherAlias`)**: `••` | `A` | `B` | `C` | `1` | `2` | `3` | `4` | `5` | `6`
- **Step 4 (`com.sec.android.app.sysupdate/LauncherAlias`)**: `•••` | `A` | `B` | `C` | `1` | `2` | `3` | `4` | `5` | `6`
- **Step 5 (`com.sec.android.app.sysupdate/LauncherAlias`)**: `••••` | `A` | `B` | `C` | `1` | `2` | `3` | `4` | `5` | `6`
- **Step 6 (`com.sec.android.app.sysupdate/LauncherAlias`)**: `A` | `B` | `C` | `1` | `2` | `3` | `4` | `5` | `6` | `7`
- **Step 7 (`com.sec.android.app.sysupdate/LauncherAlias`)**: `A` | `B` | `C` | `1` | `2` | `3` | `4` | `5` | `6` | `7`
- **Step 8 (`com.sec.android.app.sysupdate/LauncherAlias`)**: `A` | `B` | `C` | `1` | `2` | `3` | `4` | `5` | `6` | `7`

## 中文逐页引导链路解读

> **全链路总结**：应用以“系统更新”包名 com.sec.android.app.sysupdate 和 LauncherAlias 入口伪装系统组件，首屏为四位 PIN 门禁；连续输入 1234 并点 OK 后，探针跳转 .a.M、.AliasSettings、.AliasChrome 均未展示真实设置/授权页，仍停留于同一 PIN 键盘，具有别名规避与门禁诱导特征，授权/拒权未测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 你的数据未备份（各步骤 GMS 通知横幅）
- 英文 -> 立即添加备份账户（各步骤 GMS 通知横幅）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: LauncherAlias** | 首屏为四位PIN门禁键盘，含字母A/B/C与数字键；顶部1个圆点，无取消键；点击“1”，通知横幅称数据未备份。 | `step_01_action.png` |
| 2 | **Step 2: LauncherAlias** | PIN键盘页，顶部进度为2个圆点；本步点击“2”，无取消或返回入口；GMS通知仍称数据未备份、建议添加备份账户。 | `step_02_action.png` |
| 3 | **Step 3: LauncherAlias** | PIN键盘页，顶部进度为3个圆点；本步点击“3”，界面无取消键；通知横幅持续显示“数据未备份，立即添加备份账户”。 | `step_03_action.png` |
| 4 | **Step 4: LauncherAlias** | PIN键盘页，顶部进度为4个圆点；本步点击“4”完成四位PIN；界面仍无取消/返回；通知横幅提示数据未备份。 | `step_04_action.png` |
| 5 | **Step 5: LauncherAlias** | PIN键盘页显示4个圆点，本步点击勾选OK确认PIN；未进入真实系统设置，仍为门禁页；通知横幅称数据未备份。 | `step_05_action.png` |
| 6 | **Step 6: LauncherAlias** | 静态跳转探针指向.a.M，但界面仍为同一PIN键盘，数字与字母键未变；无新页面内容，通知横幅仍提示数据未备份。 | `step_06_screen.png` |
| 7 | **Step 7: LauncherAlias** | 静态跳转探针指向.AliasSettings，界面仍停留在PIN键盘，无设置项或授权弹窗；通知横幅继续称数据未备份。 | `step_07_screen.png` |
| 8 | **Step 8: LauncherAlias** | 静态跳转探针指向.AliasChrome，仍显示PIN键盘且无新界面；未见授权/拒权结果；通知横幅称数据未备份。 | `step_08_screen.png` |
