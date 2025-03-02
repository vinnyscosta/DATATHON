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

variable "region" {
  type        = string
  description = "AWS Region"
  default     = "sa-east-1"
}
