# Bangbo website review

独立评审项目。结构与交互以 Ola 第 19 版提交 `f8026d91802eb907a54d9f84c349aa306ef098cd` 为准；原项目未修改。

## 本地构建与预览

- Python 3.12 + Pillow：`python -m pip install -r requirements.txt`
- 构建：`python build-aligned.py`
- 预览：`python -m http.server 8768 --bind 127.0.0.1`，打开 `http://127.0.0.1:8768/dist/?lang=zh`
- 离线：直接打开 `dist/index.html`；所有字体、徽章、标识和占位资源均为本地文件。
- 校验：`npm ci`，分别在本目录与母版 dist 启动 8768、8769 HTTP 服务，再执行 `npm test`。测试使用本机 Chrome；可按运行环境调整 executablePath。

## 可编辑内容

- `product-copy.json`：中、英、印地、印尼四语言产品文案。
- `build-aligned.py`：链接、主体、正式协议、占位映射与构建逻辑。
- `brand-paint.py`：颜色和不占布局空间的书页/书签装饰。
- `brand/`：真实官方 Logo 与 App 图标。
- `dist/assets/placeholder-*`：首屏 1600×900 / 900×1600；五功能 720×1280。首页没有人物或宣传图片，没有视频。
- `template/`：本地固定母版及通用资源；这是结构溯源文件，保留原始品牌文本用于校验，不用于展示。构建不依赖 Infriends 或其他项目路径。
- `alignment-slots.js`：在固定母版文字槽位内保留高度，不改变字号或移动按钮。中性历史场景 ID 和埋点标识保持原样。

`prepare-project.py` 校验独立模板与文案，不覆盖配置。日常运行 `build-aligned.py` 构建。

## 部署

独立 GitHub 仓库和 GitHub Pages；`.github/workflows/pages.yml` 发布已验证的 `dist`。无需服务端运行时。详情见 `DEPLOYMENT.md`。

来源、冲突和未接入项分别见 `SOURCES.md`、`HANDOFF.md`。截图与机器检查报告位于 `tests/`。
