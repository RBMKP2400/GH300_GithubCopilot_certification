param(
    [string]$BaseBranch = "feature/poc-parallel-agents",
    [string]$Agent1Branch = "feature/agent-1",
    [string]$Agent2Branch = "feature/agent-2",
    [string]$Agent1Path = ".worktrees\agent-1",
    [string]$Agent2Path = ".worktrees\agent-2",
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

function Resolve-ProjectPath {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$ProjectRoot
    )

    if ([System.IO.Path]::IsPathRooted($Path)) {
        return [System.IO.Path]::GetFullPath($Path)
    }

    return [System.IO.Path]::GetFullPath((Join-Path $ProjectRoot $Path))
}

function Invoke-Checked {
    param(
        [Parameter(Mandatory = $true)][string]$Exe,
        [string[]]$Args = @()
    )

    Write-Host ("> $Exe $($Args -join ' ')") -ForegroundColor DarkCyan
    if (-not $DryRun) {
        & $Exe @Args
        if ($LASTEXITCODE -ne 0) {
            throw "Fallo el comando: $Exe $($Args -join ' ')"
        }
    }
}

function Add-AgentWorktree {
    param(
        [Parameter(Mandatory = $true)][string]$Branch,
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Base
    )

    $parent = Split-Path -Parent $Path
    if ($parent -and -not (Test-Path $parent)) {
        if ($DryRun) {
            Write-Host "> mkdir -p $parent" -ForegroundColor DarkCyan
        } else {
            New-Item -ItemType Directory -Path $parent -Force | Out-Null
        }
    }

    if ((Test-Path $Path) -and ((Get-ChildItem -Force $Path | Measure-Object).Count -gt 0)) {
        throw "La ruta $Path ya existe y no esta vacia. Usa otra ruta o elimina ese directorio."
    }

    $exists = (-not $DryRun) -and [bool](git branch --list $Branch)
    if ($exists) {
        Invoke-Checked "git" @("worktree", "add", $Path, $Branch)
    } else {
        Invoke-Checked "git" @("worktree", "add", $Path, "-b", $Branch, $Base)
    }
}

$repoRoot = (git rev-parse --show-toplevel 2>$null)
if (-not $repoRoot) {
    throw "Este script debe ejecutarse dentro de un repositorio Git."
}

$projectRoot = Split-Path -Parent $PSCommandPath
if (-not $projectRoot) {
    $projectRoot = (Get-Location).Path
}

$agent1ResolvedPath = Resolve-ProjectPath -Path $Agent1Path -ProjectRoot $projectRoot
$agent2ResolvedPath = Resolve-ProjectPath -Path $Agent2Path -ProjectRoot $projectRoot

Set-Location $repoRoot.Trim()

Invoke-Checked "git" @("checkout", $BaseBranch)
Add-AgentWorktree -Branch $Agent1Branch -Path $agent1ResolvedPath -Base $BaseBranch
Add-AgentWorktree -Branch $Agent2Branch -Path $agent2ResolvedPath -Base $BaseBranch

Write-Host "Worktrees listos." -ForegroundColor Green
Write-Host "Agent 1: $agent1ResolvedPath ($Agent1Branch)"
Write-Host "Agent 2: $agent2ResolvedPath ($Agent2Branch)"
Write-Host "Siguiente paso: abre dos terminales y ejecuta copilot en cada carpeta aislada."