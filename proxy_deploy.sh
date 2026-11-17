#!/bin/bash
# 触发 action proxy 部署 fitsaga（ops-runner/proxy.yml）
# 前置：PROXY_KEYS_JSON secret 已含 fitsaga key（见 PROXY_SETUP.md）
# 用法: bash proxy_deploy.sh preview  或  bash proxy_deploy.sh prod
set -e
ENV_NAME="${1:-preview}"
case "$ENV_NAME" in
  preview|prod) ;;
  *) echo "用法: $0 preview|prod"; exit 1 ;;
esac
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
gh workflow run "deploy proxy" --repo greatyingzi/ops-runner -f site=fitsaga -f env="$ENV_NAME"
echo "已触发 proxy 部署 fitsaga env=$ENV_NAME"
echo "查看: https://github.com/greatyingzi/ops-runner/actions/workflows/proxy.yml"
