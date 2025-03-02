variable "aws_region" {
  description = "Região AWS"
  default     = "us-east-1"
}

variable "ecs_cluster_name" {
  description = "Nome do cluster ECS"
}

variable "ecs_service_name" {
  description = "Nome do serviço ECS"
}

variable "alb_arn_suffix" {
  description = "ARN Sufixo do Application Load Balancer"
}
