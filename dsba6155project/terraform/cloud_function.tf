
resource "null_resource" "creating_function_code_zip" {
  provisioner "local-exec" {
    command = "Compress-Archive cloud_function/* cloud_func.zip -Force"
    interpreter = ["PowerShell", "-Command"]
  }
}


//https://us-east1-dsba6155p.cloudfunctions.net/data_pull_cloud_func?query=hinduism&bucket=dsba6155pdatabucket&folder=download
resource "google_storage_bucket_object" "cloud_function_zip" {
  name   = "data_pull_cloud_func"
  source = "${path.root}/cloud_func.zip"
  bucket = google_storage_bucket.data_bucket.name
  depends_on = [null_resource.creating_function_code_zip]
}


resource "google_cloudfunctions_function" "data_pull_cloud_func" {
  name        = "data_pull_cloud_func"
  description = "Pulls data from Project Gutenberg"
  runtime     = "python37"
  project = data.google_project.kbs_project.project_id

  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.data_bucket.name
  source_archive_object = google_storage_bucket_object.cloud_function_zip.name
  trigger_http          = true
  entry_point           = "getbooks"
}

# IAM entry for all users to invoke the function
resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = google_cloudfunctions_function.data_pull_cloud_func.project
  region         = google_cloudfunctions_function.data_pull_cloud_func.region
  cloud_function = google_cloudfunctions_function.data_pull_cloud_func.name

  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"
}
