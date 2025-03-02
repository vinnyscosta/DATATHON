locals {
  env_vars = length(var.envs) > 0 ? [for env in split(",", var.envs) : {
    name  = split("=", env)[0]
    value = split("=", env)[1]
  }] : []
}