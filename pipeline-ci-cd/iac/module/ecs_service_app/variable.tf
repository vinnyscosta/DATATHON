variable "cluster_id" {
  description = "Id do cluster ECS"
  type        = string
}

variable "task_definition" {
  description = "Nome do task_definition ECS"
  type        = string
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

variable "container_name" {
  description = "Nome do container dentro da Task Definition"
  type        = string
}

variable "container_port" {
  description = "Porta do container"
  type        = number
  default     = 8080
}
