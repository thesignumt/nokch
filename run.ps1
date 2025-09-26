
# Import the PSToml module
Import-Module PSToml

# Path to your TOML file
$tomlFile = "./pyproject.toml"

# Function to upload files using twine
function Upload-TomlFiles
{
  try
  {
    # Read and parse the TOML file
    $tomlContent = Get-Content $tomlFile -Raw -ErrorAction Stop | ConvertFrom-Toml

    # Extract the version from the [project] section
    $version = $tomlContent.project.version
    if (-not $version)
    {
      Write-Output "Error: Version not found in [project] section"
      return
    }

    # Create toUpload variable with files containing the version
    $toUpload = Get-ChildItem -Path "dist/" -File | Where-Object { $_.Name -like "*$version*" } | ForEach-Object { $_.FullName }

    if ($toUpload.Count -eq 0)
    {
      Write-Output "No files found with version $version in dist/"
      return
    }

    # Check if twine is an executable command
    if (Get-Command twine -ErrorAction SilentlyContinue)
    {
      # Upload each file using twine with quoted paths
      foreach ($file in $toUpload)
      {
        $quotedFile = "`"$file`""
        Write-Output "Uploading: $file"
        Invoke-Expression "twine upload $quotedFile"
      }
    } else
    {
      Write-Output "Error: twine is not installed or not found in PATH"
    }
  } catch
  {
    Write-Output "Error: $_"
  }
}

python -m build

Upload-TomlFiles
