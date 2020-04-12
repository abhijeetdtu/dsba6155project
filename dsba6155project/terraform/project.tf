# Error: error creating project dsba6155p (KBS Project):
# googleapi: Error 403: The caller does not have permission, forbidden. If you received a 403 error, make sure you have the `roles/resourcemanager.projectCreator` permission
# Doesnt work as we need to create organization
# resource "google_project" "kbs_project" {
#   name       = "KBS Project"
#   project_id = "dsba6155p"
#   org_id = "0"
# }


# instead use data source


data "google_project" "kbs_project" {
  project_id = "dsba6155p"
}
