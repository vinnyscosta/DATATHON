resource "aws_cloudwatch_dashboard" "mlops_dashboard" {
  dashboard_name = "API-MLOps-Dashboard"

  dashboard_body = jsonencode({
    widgets = [
      # USO DE CPU
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/ECS", "CPUUtilization", "ClusterName", var.ecs_cluster_name, "ServiceName", var.ecs_service_name]
          ]
          title  = "Uso de CPU (%)"
          view   = "timeSeries"
          region = var.aws_region
          stat   = "Average"
          period = 60
        }
      },
      # USO DE MEMÓRIA
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/ECS", "MemoryUtilization", "ClusterName", var.ecs_cluster_name, "ServiceName", var.ecs_service_name]
          ]
          title  = "Uso de Memória (%)"
          view   = "timeSeries"
          region = var.aws_region
          stat   = "Average"
          period = 60
        }
      },
      # TOTAL DE REQUISIÇÕES NO ALB
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/ApplicationELB", "RequestCount", "LoadBalancer", var.alb_arn_suffix]
          ]
          title  = "Total de Requisições no ALB"
          view   = "timeSeries"
          region = var.aws_region
          stat   = "Sum"
          period = 60
        }
      },
      # ERROS 5XX NO ALB
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/ApplicationELB", "HTTPCode_Target_5XX_Count", "LoadBalancer", var.alb_arn_suffix]
          ]
          title  = "Erros 5XX no ALB"
          view   = "timeSeries"
          region = var.aws_region
          stat   = "Sum"
          period = 60
        }
      },
      # LATÊNCIA DA API (P95)
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/ApplicationELB", "TargetResponseTime", "LoadBalancer", var.alb_arn_suffix]
          ]
          title  = "Latência da API (P95)"
          view   = "timeSeries"
          region = var.aws_region
          stat   = "p95"
          period = 60
        }
      },
      # LATÊNCIA DA API (MÉDIA)
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/ApplicationELB", "TargetResponseTime", "LoadBalancer", var.alb_arn_suffix]
          ]
          title  = "Latência Média da API"
          view   = "timeSeries"
          region = var.aws_region
          stat   = "Average"
          period = 60
        }
      }
    ]
  })
}
