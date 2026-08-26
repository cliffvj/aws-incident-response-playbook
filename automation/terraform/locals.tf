locals {
  common_tags = merge(
    {
      Project     = var.project_name
      ManagedBy   = "Terraform"
      Purpose     = "IncidentResponseLab"
      Environment = var.deployment_environment
    },
    var.tags,
  )
}
