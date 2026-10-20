
$ErrorActionPreference = "Stop"

# Move to the project directory
Set-Location "D:\DeepDerma-LabOps"

# Configure the Python import path used by this project
$env:PYTHONPATH = "D:\Lib\site-packages"

# Request the SQL password without displaying it
$securePassword = Read-Host "Enter your DeepDermaAppLogin SQL password" -AsSecureString
$env:DEEPDERMA_DB_PASSWORD = [System.Net.NetworkCredential]::new("", $securePassword).Password

try {
    # Start the DeepDerma application
    python -m streamlit run app/app.py
}
finally {
    # Clear the password from this PowerShell process when Streamlit exits
    Remove-Item Env:DEEPDERMA_DB_PASSWORD -ErrorAction SilentlyContinue
    Remove-Variable securePassword -ErrorAction SilentlyContinue
}
