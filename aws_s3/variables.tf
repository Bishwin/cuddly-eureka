variable "service_name" {
  type        = string
  description = "name to assign all resources created for this service"
}

variable "function_filename" {
  type        = string
  description = ""
}

variable "runtime" {
  type        = string
  default     = "python3.8"
  description = ""
}
