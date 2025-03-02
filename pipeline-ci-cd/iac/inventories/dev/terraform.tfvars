environment     = "dev"
account_id      = "458807800524"
region          = "us-east-1"
app_name        = "ecs-cluster-datatlon"
iam_role_name   = "ecsTaskExecutionRole"
iam_role_policy = "ecsTaskExecutionPolicy"
project_name    = "project-datathon-mlops"
account         = "contaluizcarloos"
workspace       = "mlops"
username        = "luizcst"
task_name       = "api-mlops-datathon"
cpu             = "4096"
memory          = "8192"
envs            = "enviroment=dev"

service_name    = "mlops-datathon-service"
desired_count   = 1
vpc_id          = "vpc-9405d4e9"
subnets         = ["subnet-281b4f65", "subnet-52c10963", "subnet-e8c8b7e6"]
security_groups = ["sg-26ef0813"]
route53_zone_id = ""
tags = {
  environment = "dev"
  product     = "data-platform"
}


