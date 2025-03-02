terraform {
  backend "s3" {
  }
}

module "ecs_cluster" {
  source    = "./module/ecs_cluster"
  app_name  = var.app_name
  workspace = var.workspace
  region    = var.region
}

module "iam_role_task_definition" {
  source          = "./module/iam_role"
  iam_role_name   = var.iam_role_name
  iam_role_policy = var.iam_role_policy

}



module "ecs_container_definition" {
  source     = "./module/ecs_container_definition"
  app_name   = var.app_name
  role_name  = var.iam_role_name
  task_name  = var.task_name
  workspace  = var.workspace
  region     = var.region
  image      = var.image
  cpu        = var.cpu
  memory     = var.memory
  envs       = var.envs
  depends_on = [module.ecs_cluster, module.iam_role_task_definition]
}


module "ecs_service_app" {
  source          = "./module/ecs_service_app"
  cluster_id      = module.ecs_cluster.aws_ecs_cluster_id                    # Nome do cluster ECS
  task_definition = module.ecs_container_definition.aws_container_definition # ARN da Task Definition
  service_name    = var.service_name
  desired_count   = var.desired_count
  vpc_id          = var.vpc_id
  subnets         = var.subnets
  security_groups = var.security_groups
  container_name  = "${var.workspace}-${var.task_name}"
  depends_on      = [module.ecs_container_definition]

}

module "cloud_watch" {
  source           = "./module/cloud_watch"
  ecs_cluster_name = module.ecs_cluster.aws_ecs_cluster_name
  ecs_service_name = var.service_name
  alb_arn_suffix   = module.ecs_service_app.alb_arn_suffix

  depends_on = [module.ecs_service_app]

}
