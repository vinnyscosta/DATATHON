resource "aws_ecs_task_definition" "service" {
  family                   = local.task_name
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.cpu
  memory                   = var.memory
  #task_role_arn            = data.aws_iam_role.app_role.arn
  task_role_arn      = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${var.role_name}"
  execution_role_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${var.role_name}"
  container_definitions = templatefile("${path.module}/templates/container-definition.json.tpl", {
    task_name        = local.task_name
    image            = var.image
    cpu              = var.cpu
    memory           = var.memory
    region           = var.region
    env_vars         = jsonencode(local.env_vars)
    cloudwatch_group = aws_cloudwatch_log_group.log_group.name
  })
}
