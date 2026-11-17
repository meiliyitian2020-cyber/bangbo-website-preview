# 验证结果 · 2026-11-17

- 母版：Ola v19，提交 f8026d91802eb907a54d9f84c349aa306ef098cd；原文件 SHA256 5a79698af859992878ad6febd33991ab814c252d432356617ab20a5d22435be5，构建前后未变。
- CSS：对颜色词法替换归一后，全部 style 块与母版一致；没有修改布局、字号、比例、断点。文案使用原文本测量槽位保留高度/宽度。
- 首页：1440×900 / 390×844 × en、zh、hi、id 共 8 组，主要控件矩形差异 0（阈值 1.1px），无文字溢出报告、脚本异常或失败资源请求。
- 内页：About / Help / Contact / Safety × 四语言 × 两屏宽，共 32 组，主要容器、页脚和表单矩形均无超阈值差异，无文字溢出。
- 路由：每组覆盖 about、help、contact、safety、terms、privacy、children、community、bullying、cookies、law-enforcement。
- 功能：6 个首页槽位、5 个功能占位，切换场景；FAQ 搜索/无结果；表单空值不通过及完整填写校验；更多下载；Cookie 偏好保存；未知充值反馈。
- 补充：实际语言下拉切换；全部 7 个下载渠道按钮；仅 Google Play 调用本产品官方 URL，未确认渠道均反馈；手机菜单；刷新后 Cookie 持久化；file:// 离线直接打开、Logo 和首屏占位加载。
- 素材：官网 Logo 重新下载字节完全一致；商店图标重新下载后逐像素一致；展示图全部为本地占位，无人物宣传素材或视频。
- 发布输出 `dist/index.html` 未残留 Ola/Infriends、旧公司/邮箱/地址。template 与 baseline 配置保留结构来源；原始参考文本编码存储仅用于不可见尺寸测量。

机器结果：tests/review-results.json、pages-layout-results.json、extra-results.json。截图：tests/bangbo-1440-* 与 bangbo-390-*。

在线匿名访问的最终结果另记 DEPLOYMENT.md 与 tests/public-access.json。
