
# Python Docker GitHub Actions Demo

## (日本語説明)

### 🚀 プロジェクト概要

このプロジェクトには2つの独立したPythonアプリケーションが含まれています。一つはBaidu（百度）のホットサーチランキングをスクレイピングするWebクローラー(`app.py`)で、もう一つはOpenAI APIと対話するコマンドラインチャットボット(`chat.py`)です。このプロジェクトの核心は、GitHub Actionsを利用してCI/CDプロセスを自動化し、アプリケーションをDockerイメージとしてビルドし、Docker Hubにプッシュする方法を示すことです。

### 🛠️ 技術スタック

  * **プログラミング言語**: Python
  * **依存関係管理**: `requirements.txt`
  * **コンテナ化**: Docker
  * **CI/CD**: GitHub Actions

### ⚙️ CI/CD 自動化フロー

このプロジェクトのCI/CDフローは `.github/workflows/main.yml` ファイルで定義されています。詳細は以下の通りです。

  * **トリガー条件**:

      * `main` ブランチにコードがプッシュされた時に自動的にトリガーされます。
      * GitHub Actionsのページで手動でトリガーすることも可能です (`workflow_dispatch`)。

  * **実行環境**:

      * ジョブは `ubuntu-latest` の仮想マシン上で実行されます。

  * **主要なステップと使用されているAction**:

    1.  **コードのチェックアウト (Checkout)**: 公式の `actions/checkout@v4` Action を使用して、最新のコードを取得します。
    2.  **Docker Buildxのセットアップ (Set up Docker Buildx)**: `docker/setup-buildx-action@v3` を使用して、マルチプラットフォームイメージのビルドなど、高度なビルド機能を設定します。
    3.  **Docker Hubへのログイン (Login to Docker Hub)**: `docker/login-action@v3` Action を使用します。このActionは、事前にGitHubリポジトリに設定された `DOCKERHUB_USERNAME` と `DOCKERHUB_TOKEN` という名前のSecretsを読み込み、安全にログインします。
    4.  **イメージのビルドとプッシュ (Build and push Docker image)**: `docker/build-push-action@v5` Action を使用して、以下の操作を実行します。
          * プロジェクトのルートディレクトリにある `Dockerfile` に基づいてDockerイメージをビルドします。
          * ビルドしたイメージをDocker Hubにプッシュします。
          * イメージに `your-username/my-hello-world-app:latest` のようなタグを付けます。

### ✅ 設定と利用方法

1.  **このリポジトリを** あなたのGitHubアカウントにフォークします。
2.  あなたのリポジトリで、`Settings` \> `Secrets and variables` \> `Actions` に移動します。
3.  以下の2つのリポジトリシークレット（Repository secrets）を追加します:
      * `DOCKERHUB_USERNAME`: あなたのDocker Hubユーザー名。
      * `DOCKERHUB_TOKEN`: あなたのDocker Hubアクセストークン。
4.  `.github/workflows/main.yml` ファイル内のイメージタグを編集し、`your-username` をあなたのDocker Hubユーザー名に置き換えます。
5.  `main` ブランチに任意のコミットをプッシュするか、ワークフローを手動でトリガーすると、自動ビルドとプッシュが開始されます。


-----

## (中文说明)

### 🚀 项目简介

本项目包含两个独立的Python应用：一个用于爬取百度热搜榜的网络爬虫 (`app.py`)，以及一个与OpenAI API交互的命令行聊天机器人 (`chat.py`)。项目核心在于演示如何通过 GitHub Actions 实现自动化 CI/CD 流程，将应用打包成 Docker 镜像并推送到 Docker Hub。

### 🛠️ 技术栈

  * **编程语言**: Python
  * **依赖管理**: `requirements.txt`
  * **容器化**: Docker
  * **CI/CD**: GitHub Actions

### ⚙️ CI/CD 自动化流程

本项目的 CI/CD 流程由 `.github/workflows/main.yml` 文件定义，具体如下：

  * **触发条件**:

      * 当有代码推送到 `main` 分支时自动触发。
      * 允许在 GitHub Actions 页面手动触发 (`workflow_dispatch`)。

  * **执行环境**:

      * 作业运行在 `ubuntu-latest` 虚拟机上。

  * **核心步骤与使用的 Actions**:

    1.  **检出代码 (Checkout)**: 使用官方的 `actions/checkout@v4` Action 来获取最新的代码。
    2.  **设置 Docker Buildx (Set up Docker Buildx)**: 使用 `docker/setup-buildx-action@v3` 来配置更高级的构建功能，例如构建多平台镜像。
    3.  **登录到 Docker Hub (Login to Docker Hub)**: 使用 `docker/login-action@v3` Action，它会读取预先在 GitHub 仓库中配置好的 `DOCKERHUB_USERNAME` 和 `DOCKERHUB_TOKEN` 秘密（Secrets）来进行安全登录。
    4.  **构建并推送镜像 (Build and push Docker image)**: 使用 `docker/build-push-action@v5` Action 来执行以下操作：
          * 根据项目根目录下的 `Dockerfile` 文件构建 Docker 镜像。
          * 将构建好的镜像推送到 Docker Hub。
          * 为镜像打上标签，例如 `your-username/my-hello-world-app:latest`。

### ✅ 如何配置和使用

1.  **Fork 本仓库** 到你的 GitHub 账户。
2.  在你的仓库中，进入 `Settings` \> `Secrets and variables` \> `Actions`。
3.  添加以下两个仓库秘密（Repository secrets）:
      * `DOCKERHUB_USERNAME`: 你的 Docker Hub 用户名。
      * `DOCKERHUB_TOKEN`: 你的 Docker Hub 访问令牌（Access Token）。
4.  修改 `.github/workflows/main.yml` 文件中的镜像标签，将 `your-username` 替换为你的 Docker Hub 用户名。
5.  向 `main` 分支推送任何提交 (commit)，或者手动触发 workflow，即可开始自动化构建和推送。
