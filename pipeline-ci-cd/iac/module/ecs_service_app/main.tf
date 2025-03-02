resource "aws_lb" "ecs_alb" {
  name               = "${var.service_name}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = var.security_groups
  subnets            = var.subnets
}

resource "aws_lb_target_group" "ecs_tg" {
  name        = "${var.service_name}-tg"
  port        = var.container_port
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip" # 🔴 Alterado de "instance" para "ip"


  health_check {
    path                = "/health"
    interval            = 15
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

resource "aws_lb_listener" "ecs_listener" {
  load_balancer_arn = aws_lb.ecs_alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.ecs_tg.arn
  }
}


resource "aws_ecs_service" "ecs_service" {
  name            = var.service_name
  cluster         = var.cluster_id      # Nome do cluster ECS
  task_definition = var.task_definition # ARN da Task Definition
  desired_count   = var.desired_count   # Número de instâncias desejadas
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.subnets
    security_groups  = var.security_groups
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.ecs_tg.arn # Target Group do ALB
    container_name   = var.container_name
    container_port   = var.container_port
  }

  depends_on = [aws_lb_listener.ecs_listener]
}


