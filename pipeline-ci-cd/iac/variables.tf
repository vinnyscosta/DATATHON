variable "environment" {
  type        = string
  default     = null
  description = "Environment name"
}

variable "account_id" {
  type        = string
  description = "account_id"
}


variable "region" {
  type        = string
  description = "AWS Region"
  default     = "sa-east-1"
}

variable "app_name" {
  type        = string
  default     = null
  description = ""
}

variable "iam_role_name" {
  type        = string
  description = "Iam Role Name"
}

variable "iam_role_policy" {
  type        = string
  description = "Iam Role Policy"
}

variable "project_name" {
  type        = string
  default     = null
  description = "Project Name"
}

variable "account" {
  type        = string
  default     = null
  description = "Account Slug"
}

variable "workspace" {
  type        = string
  default     = null
  description = "workspace Slug"
}

variable "username" {
  type        = string
  default     = null
  description = ""
}

variable "task_name" {
  type        = string
  default     = null
  description = ""
}

variable "image" {
  type        = string
  description = ""
  default     = ""
}

variable "cpu" {
  type        = string
  description = ""
  default     = ""
}

variable "memory" {
  type        = string
  description = ""
  default     = ""
}

variable "envs" {
  type        = string
  description = ""
  default     = ""
}


variable "tags" {
  description = "(Optional) A mapping of tags to assign to the kms key."
  type        = map(string)
}




variable "service_name" {
  description = "Nome do serviço ECS"
  type        = string
}

variable "desired_count" {
  description = "Número de instâncias do container"
  type        = number
  default     = 1
}

variable "vpc_id" {
  description = "ID da VPC onde o ECS e o Load Balancer serão criados"
  type        = string
}


variable "subnets" {
  description = "Lista de subnets para rodar o ECS"
  type        = list(string)
}

variable "security_groups" {
  description = "Lista de Security Groups para o ECS"
  type        = list(string)
}


variable "route53_zone_id" {
  description = "ID da Hosted Zone do Route 53"
  type        = string
}

