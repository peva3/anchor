# Skill 42: Infrastructure as Code

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.

## 42. Infrastructure as Code

Infrastructure must be defined in code, not configured manually through a web console. Every project that deploys to cloud infrastructure requires IaC.

### 42.1 Tool Selection

| Tool | Language | When to Use |
|------|----------|-------------|
| **Terraform** | HCL | Enterprise, multi-cloud, large teams, existing HCL ecosystem |
| **OpenTofu** | HCL | Terraform-compatible, open-source fork (preferred for new projects) |
| **Pulumi** | TypeScript/Python/Go | Developer-friendly, type-safe, application teams |
| **Crossplane** | YAML (K8s CRDs) | Kubernetes-native, GitOps control loops |

### 42.2 Terraform/OpenTofu Project Structure

```
terraform/
├── main.tf              # Provider configuration, remote state backend
├── variables.tf         # Input variables with types and descriptions
├── outputs.tf            # Output values (connection strings, endpoints, ARNs)
├── versions.tf           # Provider version constraints
├── terraform.tfvars      # Variable values (non-sensitive)
├── network.tf            # VPC, subnets, security groups, NAT gateways
├── compute.tf            # Compute instances, Kubernetes cluster, load balancers
├── database.tf           # RDS/Cloud SQL, backups, parameter groups
├── cache.tf              # Redis/ElastiCache configuration
├── secrets.tf            # Secrets Manager / Vault references
├── monitoring.tf         # Alerts, dashboards, log groups
├── iam.tf                # Service accounts, roles, policies
└── environments/
    ├── dev.tfvars
    ├── staging.tfvars
    └── prod.tfvars
```

### 42.3 Core Configuration Template

**`versions.tf`:**
```hcl
terraform {
  required_version = ">= 1.8.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.50"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }

  backend "s3" {
    bucket         = "mycompany-terraform-state"
    key            = "myproject/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

**`variables.tf`:**
```hcl
variable "environment" {
  description = "Deployment environment (dev, staging, prod)"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "instance_count" {
  description = "Number of compute instances"
  type        = number
  default     = 3
}

variable "database_password" {
  description = "Master database password"
  type        = string
  sensitive   = true
}

variable "enable_deletion_protection" {
  description = "Prevent accidental deletion of resources"
  type        = bool
  default     = true
}
```

**`outputs.tf`:**
```hcl
output "database_endpoint" {
  description = "Database connection endpoint"
  value       = aws_db_instance.main.endpoint
  sensitive   = true
}

output "load_balancer_dns" {
  description = "Load balancer DNS name"
  value       = aws_lb.main.dns_name
}

output "service_url" {
  description = "Public URL of the deployed service"
  value       = "https://${var.environment}.example.com"
}
```

### 42.4 Multi-Environment Pattern

```bash
# Initialize (one-time per environment)
terraform init -backend-config="environments/dev.backend.tfvars"

# Plan changes
terraform plan -var-file="environments/dev.tfvars" -out=dev.plan

# Apply changes
terraform apply dev.plan

# Destroy (caution!) — only for ephemeral environments
terraform destroy -var-file="environments/dev.tfvars"
```

### 42.5 State Management Rules

| Rule | Detail |
|------|--------|
| **Remote state REQUIRED** | Never store state locally — use S3, GCS, Azure Blob, or Terraform Cloud |
| **State locking REQUIRED** | Use DynamoDB (AWS), Cloud Storage lock (GCP), or equivalent |
| **Never edit state manually** | Use `terraform state mv/rm/import` commands only |
| **State encryption at rest** | Enable server-side encryption on state bucket |
| **State backup** | Enable versioning on state bucket, retain at least 30 days |
| **Workspace per environment** | Separate state per environment (dev/staging/prod) — never share state |

### 42.6 Pre-Deploy Checklist

Before `terraform apply`:
- [ ] `terraform fmt --recursive` passes (standardized formatting)
- [ ] `terraform validate` passes (syntax and reference validation)
- [ ] `terraform plan` reviewed — no unexpected destroy/replace operations
- [ ] Sensitive outputs are marked `sensitive = true`
- [ ] Deletion protection is enabled on stateful resources (databases, storage)
- [ ] Terraform plan output is saved to version control for audit

---

