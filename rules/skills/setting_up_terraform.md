## 元数据

- **类型**: Workflow
- **分类**: Infrastructure & DevOps
- **适用场景**: Set up Terraform infrastructure-as-code for cloud resources, including provider configuration, modules, state management, and CI integration.
- **上游来源**: [setting-up-terraform](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/setting-up-terraform)
- **user-invocable**: —
- **导入日期**: 2026-06-26

---

# Setup Terraform

Use this skill when the user asks to set up Terraform, infrastructure as code, cloud provisioning, or IaC.

## Steps

1. **Initialize the project structure**

   ```
   infra/
   ├── main.tf
   ├── variables.tf
   ├── outputs.tf
   ├── terraform.tfvars      # (gitignored)
   ├── providers.tf
   └── modules/
   ```

2. **Configure the provider** — in `providers.tf`:

   ```hcl
   terraform {
     required_version = ">= 1.5"
     required_providers {
       aws = {
         source  = "hashicorp/aws"
         version = "~> 5.0"
       }
     }
     backend "s3" {
       bucket = "my-terraform-state"
       key    = "prod/terraform.tfstate"
       region = "us-east-1"
     }
   }

   provider "aws" {
     region = var.aws_region
   }
   ```

   Adapt the provider for the user's cloud (AWS, GCP, Azure).

3. **Define variables** — in `variables.tf`, define inputs with types, descriptions, and defaults:

   ```hcl
   variable "aws_region" {
     type        = string
     default     = "us-east-1"
     description = "AWS region for resources"
   }

   variable "environment" {
     type        = string
     description = "Deployment environment (dev, staging, prod)"
   }
   ```

4. **Create resources** — in `main.tf`, define the infrastructure the user needs (VPC, RDS, ECS, S3, Lambda, etc.). Extract reusable patterns into modules under `modules/`.

5. **Configure remote state** — use an S3 bucket (AWS), GCS bucket (GCP), or Azure Storage for state. Enable state locking with DynamoDB (AWS).

6. **Add to `.gitignore`**

   ```
   *.tfstate
   *.tfstate.*
   .terraform/
   terraform.tfvars
   *.tfvars
   ```

7. **Add CI pipeline** — create a GitHub Actions workflow that runs `terraform fmt -check`, `terraform validate`, and `terraform plan` on PRs, with `terraform apply` on merge to main (with approval gate).

## Notes

- Never commit state files or `.tfvars` with secrets.
- Use workspaces or separate state files for dev/staging/prod.
- Pin provider versions to avoid breaking changes.
- Run `terraform fmt` before committing.
