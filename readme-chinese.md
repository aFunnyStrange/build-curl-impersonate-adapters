# 构建 curl-impersonate 适配层

> 状态：**draft-inactive（草稿，未激活）**。这个公开 Skill 只包含可复用的工作流约束、验证门禁和
> 通用示例；激活前仍需要一次独立前向使用和用户明确批准。

这个 Skill 用于从官方 curl-impersonate 源码重构建自定义 TLS/H2/H3 profile，并让生成的原生后端
可以被 curl_cffi 和可选的 scrapy_cffi 无缝使用。它重点处理源码锁、幂等 profile overlay、与
Python ABI 匹配的单一 wrapper/libcurl 多 profile 产物包、一个 native 目录内的请求级 profile
选择，以及能够识别“Python 看似成功、实际仍加载另一套 libcurl”的分层验证。

同一平台、架构和 Python ABI 下，所有兼容的 Chrome/浏览器 profile 必须一次编译进同一个原生
runtime，只打包一套 wrapper、runtime library 和共享 profile manifest。禁止按 Chrome 版本或
profile 分目录打包；curl_cffi 和 scrapy_cffi 只配置一个 native 目录，再由每个请求选择 profile。

“完整”必须相对于项目工作场景声明：导航、fetch/XHR、子资源、预检、表单和 WebSocket 握手不是
同一套通用请求头。Manifest 必须声明所需场景及其覆盖关系；连接池必须绑定一个确定的 native
transport/profile，避免后续请求复用到另一个 profile 已建立的 TLS 连接。

Skill 不保存抓包、TLS key log、Cookie、私有 URL、凭证、任务会话、本机绝对路径或原生二进制。
公开内容只记录可迁移流程、通用协议约束和故障恢复门禁。

## 安装到 Codex

草稿激活前不要安装。激活后，把完整源码目录链接到用户 Skill 目录，不要复制可编辑源码。

Windows PowerShell：

```powershell
$skillsRoot = Join-Path $HOME ".agents\skills"
$source = (Resolve-Path "<仓库根目录>\build-curl-impersonate-adapters").Path
$link = Join-Path $skillsRoot "build-curl-impersonate-adapters"
New-Item -ItemType Directory -Force -Path $skillsRoot | Out-Null
if (Test-Path -LiteralPath $link) { throw "目标已存在：$link" }
New-Item -ItemType Junction -Path $link -Target $source | Out-Null
```

macOS：

```bash
skills_root="$HOME/.agents/skills"
source_dir="$(cd "<仓库根目录>/build-curl-impersonate-adapters" && pwd)"
link_path="$skills_root/build-curl-impersonate-adapters"
mkdir -p "$skills_root"
if [ -e "$link_path" ] || [ -L "$link_path" ]; then echo "目标已存在：$link_path" >&2; exit 1; fi
ln -s "$source_dir" "$link_path"
```

激活后可通过 `$build-curl-impersonate-adapters` 调用。CC Switch v3.13 或更高版本可以导入已链接的
本地 Skill，但仍需检查目标 Agent 的格式、工具、权限和原生构建环境。

## 资源

- `SKILL.md`：源码、构建、适配、隐私和资格验证主流程。
- `references/`：源码 overlay、请求场景与连接池、抓包证据、原生打包、Python 适配、验证矩阵和
  通用故障恢复门禁。
- `assets/integration-manifest.example.json`：可迁移的产物与证据清单模板。
- `scripts/check_integration_readiness.py`：只读检查清单、路径、单一产物包基数、ABI 和 SHA-256。
