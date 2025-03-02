locals {
  task_name        = "${var.workspace}-${var.task_name}"
  cloudwatch_group = "/${var.workspace}/ecs/${var.app_name}/${var.task_name}"
  env_vars = length(var.envs) > 0 ? [for env in split(",", var.envs) : {
    name  = split("=", env)[0]
    value = split("=", env)[1]
  }] : []
}
