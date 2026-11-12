# 在 GitHub 发布副本

推荐仓库名：`grill-my-research-skill`。内部 skill 名称一致，调用方式为
`$grill-my-research-skill`。把本文件夹的**内容**作为仓库根目录，使 `SKILL.md`
和 `README.md` 直接出现在仓库首页，不再额外套一层目录。

## GitHub Desktop

用 GitHub Desktop 将当前文件夹创建为本地仓库；核对待提交文件，提交后发布到你的
账户。如果此目录已经有 Git 配置，先沿用并确认原配置，不重复初始化。界面按钮可能
随版本变化，关键顺序是本地建仓库、核对内容、提交、发布。

## Git 命令方式

先在 GitHub 创建同名空仓库，选择 **Public**。创建时不额外生成 README、许可证和 `.gitignore`，因为
这些文件已经在本地提供。进入本目录，逐条执行：

```text
git init -b main
git add .
git status --short
git commit -m "Add Grill My Research skill"
git remote add origin https://github.com/YOUR_USERNAME/grill-my-research-skill.git
git push -u origin main
```

将 `YOUR_USERNAME` 替换成你的账户名；按提示完成身份验证。上述命令假定当前没有
已有仓库或 `origin`，已有配置则核对后沿用。若 Git 要求身份信息，设置你希望显示在
提交记录中的姓名和邮箱。不要把访问 Token 写进仓库或说明文件。

## 建议的仓库信息

- Description: `Adaptive research questioning, evidence-weighted feedback, and a coherent question-to-decision project plan.`
- Topics: `agent-skills`, `codex-skill`, `research-design`, `critical-thinking`, `socratic-method`, `research-workflow`
- License: MIT（已提供 `LICENSE`）

推送后，检查仓库首页是否显示 **Public** 和 **MIT license**，确认 `SKILL.md` 在根目录，
并在 **Actions** 查看本次提交的检查结果。

## 包含与排除

保留隐藏的 `.github/`、`.gitignore`、`.gitattributes`。`work/`、`private/`、
`inputs/`、`outputs/`、本地环境、缓存和生成 ZIP 不应上传。Git 会使用 `.gitignore`，
网页手动上传则需你自行核对。不要把真实未公开课题放进公开示例或 Issue。

需要干净源码 ZIP 时，在安装开发依赖后执行：

```text
python -m pip install -r requirements-dev.txt
python scripts/validate_repository.py
python -m unittest discover -s tests -v
python scripts/package_skill.py --output dist/grill-my-research-skill.zip
```

ZIP 内只有一个 `grill-my-research-skill/` 顶层目录。上传时使用其解压后的内容，
不要只将 ZIP 当作整个源码仓库。上传后查看 Actions 中真实的自动检查结果。

元数据与打包测试通过不代表 AI 科研判断通过；行为评估方法见
[../evals/README.md](../evals/README.md)。
