terraform {
  required_providers {
    vercel = {
      source  = "vercel/vercel"
      version = "~> 1.0"
    }
  }
}

provider "vercel" {
  api_token = var.vercel_api_token
}

resource "vercel_project" "terra_web_app" {
  name      = "food-traffic-web-app"        # Name of the Vercel project
  framework = null                  # (Omit or set to a known framework; null means “Other”)
  git_repository = {
    type              = "github"
    repo              = "ManikandanREC/foot_traffic"
    ref = "main"
  }

  
}
