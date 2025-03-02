variable "environment" {
  type        = string
  default     = null
  description = "The environment to deploy"
}

variable "workspace" {
  type        = string
  default     = ""
  description = "Inform the name of your workspace"
}

variable "app_name" {
  type        = string
  default     = null
  description = "Inform the name"
}

variable "role_name" {
  type        = string
  description = "Inform the name of Iam role"
}

variable "task_name" {
  type        = string
  default     = null
  description = "Inform the name of container definition"
}

variable "region" {
  type        = string
  description = "AWS Region"
  default     = "sa-east-1"
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
