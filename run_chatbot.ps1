# Function to check if Python is installed
function Test-PythonInstalled {
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python 3") {
            return $true
        }
        return $false
    }
    catch {
        return $false
    }
}

# Function to check if winget is available
function Test-WingetInstalled {
    try {
        winget --version | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# Function to install Python
function Install-Python {
    Write-Host "Installing Python 3.12..."
    
    if (Test-WingetInstalled) {
        Write-Host "Installing Python using winget..."
        winget install -e --id Python.Python.3.12
    }
    else {
        Write-Host "Downloading Python installer..."
        $pythonUrl = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
        $installerPath = "$env:TEMP\python-installer.exe"
        
        # Download Python installer
        Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath
        
        # Install Python with required options
        Write-Host "Running Python installer..."
        Start-Process -FilePath $installerPath -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1" -Wait
        
        # Clean up
        Remove-Item -Path $installerPath -Force
    }
    
    # Refresh environment variables
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
    
    Write-Host "Python installation completed. Verifying installation..."
    if (Test-PythonInstalled) {
        Write-Host "Python was successfully installed!"
    }
    else {
        Write-Host "Python installation may have failed. Please try installing Python manually."
        Exit 1
    }
}

# Function to check if virtual environment exists
function Test-VenvExists {
    return Test-Path ".\venv"
}

# Function to activate virtual environment
function Activate-Venv {
    # Dot-source the activation script so its environment changes persist in the current session.
    . .\venv\Scripts\Activate.ps1
}

# Function to read environment variables from .env file
function Read-EnvFile {
    if (Test-Path ".env") {
        Get-Content ".env" | ForEach-Object {
            if ($_ -match '^\s*([^#][^=]+)=(.*)$') {
                $key = $matches[1].Trim()
                $value = $matches[2].Trim()
                Set-Variable -Name $key -Value $value -Scope Script
            }
        }
        return $true
    }
    return $false
}

# Function to save environment variables to .env file
function Save-EnvFile {
    param (
        [Parameter(Mandatory = $true)]
        [System.Collections.IDictionary]$Credentials
    )
    
    @"
OPENAI_API_KEY=$($Credentials.ApiKey)
OPENAI_MODEL_NAME=$($Credentials.ModelName)
"@ | Set-Content ".env"
    Write-Host "Credentials saved to .env file`n"
}

# Function to get OpenAI credentials
function Get-OpenAICredentials {
    param (
        [switch]$AllowOverride = $true
    )
    
    # Initialize from .env if it exists
    $script:OPENAI_API_KEY = $null
    $script:OPENAI_MODEL_NAME = $null
    $null = Read-EnvFile   # Discard any output from Read-EnvFile
    
    $apiKey = $null
    while ([string]::IsNullOrWhiteSpace($apiKey)) {
        if ([string]::IsNullOrWhiteSpace($script:OPENAI_API_KEY) -or $AllowOverride) {
            if ($script:OPENAI_API_KEY) {
                Write-Host "Current OpenAI API key exists. Press Enter to keep it, or enter a new key to override:"
                $input = Read-Host -Prompt "OpenAI API key"
                
                if ([string]::IsNullOrWhiteSpace($input)) {
                    Write-Host "Keeping existing API key."
                    $apiKey = $script:OPENAI_API_KEY
                    break
                }
                else {
                    Write-Host "Using new API key."
                    $apiKey = $input
                }
            }
            else {
                Write-Host "OpenAI API key is required to run the chatbot."
                $input = Read-Host -Prompt "Please enter your OpenAI API key"
                
                if (-not [string]::IsNullOrWhiteSpace($input)) {
                    $apiKey = $input
                }
                else {
                    Write-Host "Error: OpenAI API key is required. Please try again or press Ctrl+C to exit."
                }
            }
        }
        else {
            Write-Host "Using existing OpenAI API key from .env file."
            $apiKey = $script:OPENAI_API_KEY
            break
        }
    }
    
    $modelName = $null
    if ([string]::IsNullOrWhiteSpace($script:OPENAI_MODEL_NAME) -or $AllowOverride) {
        if ($script:OPENAI_MODEL_NAME) {
            Write-Host "Current model is '$script:OPENAI_MODEL_NAME'. Press Enter to keep it, or enter a new model name:"
            $input = Read-Host -Prompt "Model name"
            
            if ([string]::IsNullOrWhiteSpace($input)) {
                Write-Host "Keeping existing model '$script:OPENAI_MODEL_NAME'."
                $modelName = $script:OPENAI_MODEL_NAME
            }
            else {
                Write-Host "Using new model '$input'."
                $modelName = $input
            }
        }
        else {
            $modelName = Read-Host -Prompt "Enter the OpenAI model to use (default: gpt-3.5-turbo)"
            if ([string]::IsNullOrWhiteSpace($modelName)) {
                $modelName = "gpt-3.5-turbo"
                Write-Host "Using default model 'gpt-3.5-turbo'."
            }
            else {
                Write-Host "Using model '$modelName'."
            }
        }
    }
    else {
        Write-Host "Using existing model '$script:OPENAI_MODEL_NAME' from .env file."
        $modelName = $script:OPENAI_MODEL_NAME
    }
    
    return [ordered]@{
        ApiKey = $apiKey
        ModelName = $modelName
    }
}

# Function to get server configuration from Python config file
function Get-ServerConfig {
    $configContent = Get-Content "chatbot-ui/config.py" -Raw
    $config = @{}
    
    # Parse CHATBOT_SERVER configuration
    if ($configContent -match 'CHATBOT_SERVER\s*=\s*{[^}]*"url":\s*"([^"]+)"[^}]*"port":\s*(\d+)[^}]*}') {
        $config.ChatbotUrl = $matches[1]
        $config.ChatbotPort = [int]$matches[2]
    }
    
    # Parse CHATUI_SERVER configuration
    if ($configContent -match 'CHATUI_SERVER\s*=\s*{[^}]*"url":\s*"([^"]+)"[^}]*"port":\s*(\d+)[^}]*"debug":\s*(True|False)[^}]*}') {
        $config.ChatUiUrl = $matches[1]
        $config.ChatUiPort = [int]$matches[2]
        $config.ChatUiDebug = $matches[3] -eq "True"
    }
    
    return $config
}

# Check if Python is installed; if not, install it
if (-not (Test-PythonInstalled)) {
    Write-Host "Python is not installed. Installing Python 3.12..."
    Install-Python
}

# Create and setup virtual environment if it doesn't exist
if (-not (Test-VenvExists)) {
    Write-Host "Setting up virtual environment..."
    python -m venv venv
    Activate-Venv
    python -m pip install --upgrade pip
    pip install -r requirements.txt
}
else {
    Write-Host "Virtual environment already exists."
    Activate-Venv
}

# Load existing environment variables from .env file
$envFileExists = Read-EnvFile

# Get OpenAI credentials and save to .env file
$credentials = Get-OpenAICredentials
Save-EnvFile -Credentials $credentials

Write-Host "Environment setup completed.`n"

# Get server configuration from config.py
$config = Get-ServerConfig
Write-Host "Server configuration loaded from config.py"

# Fallback defaults for Chat UI if not set in config file
if (-not $config.ChatUiUrl) { $config.ChatUiUrl = "http://127.0.0.1" }
if (-not $config.ChatUiPort) { $config.ChatUiPort = 5500 }
if (-not $config.ChatUiDebug) { $config.ChatUiDebug = $false }

Write-Host "FastAPI server running at $($config.ChatbotUrl):$($config.ChatbotPort)"
Write-Host "Dash UI running at $($config.ChatUiUrl):$($config.ChatUiPort)"
Write-Host "Press Ctrl+C to stop the servers"

# Function to start the FastAPI server as a background job
$fastapi_job = Start-Job -ScriptBlock {
    param($url, $port)
    Set-Location $using:PWD
    . .\venv\Scripts\Activate.ps1
    uvicorn chatbot.server:app --host $url --port $port --reload
} -ArgumentList ($config.ChatbotUrl.Replace("http://", "")), $config.ChatbotPort

# Function to start the Dash Chat UI as a background job
$dash_job = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    . .\venv\Scripts\Activate.ps1
    python chatbot-ui/dash-chat-ui.py

} -ArgumentList ($config.ChatUiUrl.Replace("http://", "")), $config.ChatUiPort


# Open the browser to the Chat UI server link
$chatUiFullUrl = "$($config.ChatUiUrl):$($config.ChatUiPort)"
Start-Process $chatUiFullUrl


# Wait indefinitely until the user presses Ctrl+C.
try {
    while ($true) {
        $jobs = @($fastapi_job, $dash_job) | Where-Object { $_ -ne $null }
        if ($jobs.Count -gt 0) {
            Receive-Job -Job $jobs | Where-Object { $_ -ne $null } | Out-Null
        }
        Start-Sleep -Seconds 1
    }
}
catch {
    # When Ctrl+C is pressed, the loop will exit and we continue to the finally block.
}
finally {
    Write-Host "`nStopping servers..."
    if ($fastapi_job) { Stop-Job -Job $fastapi_job -Force }
    if ($dash_job) { Stop-Job -Job $dash_job -Force }
    Remove-Job -Job ($fastapi_job, $dash_job) -Force
    Write-Host "Servers stopped."
    Write-Host "`nChatbot application stopped."
}
