param(
    [string]$BaseBranch = "feature/poc-parallel-agents",
    [string]$Agent1Branch = "feature/agent-1",
    [string]$Agent2Branch = "feature/agent-2",
    [string]$Model = "gpt-5.3-codex",
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

function Test-CommandExists {
    param([Parameter(Mandatory = $true)][string]$Name)
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

function Invoke-Checked {
    param([Parameter(Mandatory = $true)][string]$Command)

    Write-Host "> $Command" -ForegroundColor DarkCyan
    if (-not $DryRun) {
        Invoke-Expression $Command
        if ($LASTEXITCODE -ne 0) {
            throw "Fallo el comando: $Command"
        }
    }
}

function Invoke-QualityChecks {
    if ($DryRun) {
        Write-Host "> flake8 main.py test" -ForegroundColor DarkCyan
        Write-Host "> vulture main.py test --min-confidence 80" -ForegroundColor DarkCyan
        Write-Host "> pytest -q" -ForegroundColor DarkCyan
        Write-Host "> bandit -r main.py test" -ForegroundColor DarkCyan
        return
    }

    if (-not (Test-Path "test")) {
        throw "No existe la carpeta 'test'. Debes tener tests en 'test' antes de integrar."
    }

    Invoke-Checked "flake8 main.py test"
    Invoke-Checked "vulture main.py test --min-confidence 80"
    Invoke-Checked "pytest -q"
    Invoke-Checked "bandit -r main.py test"
}

function Invoke-CopilotFixQuality {
    param([string]$Branch)
    $fixTask = @"
Estoy en la rama $Branch. Los checks de calidad (flake8, vulture, pytest o bandit) han fallado.
Tu mision:
1. Ejecuta flake8 main.py test para ver los errores exactos.
2. Corrige SOLO los archivos necesarios para que flake8, vulture, pytest y bandit pasen sin errores.
   - Arregla problemas de estilo (W391 trailing newline, E501 line too long, etc.).
   - No cambies la logica de negocio ni los tests existentes.
3. Una vez corregido, ejecuta git add -u y git commit --amend --no-edit para incluir las correcciones en el ultimo commit.
4. No hagas push.
5. Confirma cuando todos los checks pasen en verde.
"@
    Write-Host "> copilot -p <auto-fix-quality-prompt> --model $Model --allow-all-tools --allow-all-paths --no-ask-user" -ForegroundColor Yellow
    if (-not $DryRun) {
        & copilot -p $fixTask --model $Model --allow-all-tools --allow-all-paths --no-ask-user
        if ($LASTEXITCODE -ne 0) {
            throw "Copilot no pudo corregir los problemas de calidad en $Branch"
        }
    }
}

function Invoke-QualityChecksWithAutoFix {
    param([string]$Branch)
    if ($DryRun) {
        Invoke-QualityChecks
        return
    }
    try {
        Invoke-QualityChecks
    } catch {
        Write-Warning "Quality checks fallaron en $Branch. Lanzando Copilot para corregir automaticamente."
        Invoke-CopilotFixQuality -Branch $Branch
        Write-Host "Re-ejecutando quality checks tras la correccion automatica..." -ForegroundColor DarkCyan
        Invoke-QualityChecks
    }
}

function Get-WorktreePath {
    param([string]$Branch)
    $raw = git worktree list --porcelain 2>$null
    if (-not $raw) { return $null }
    $entries = ($raw -join "`n") -split "`n`n"
    foreach ($entry in $entries) {
        if ($entry -match "branch refs/heads/$([regex]::Escape($Branch))") {
            if ($entry -match "(?m)^worktree (.+)") {
                return $Matches[1].Trim()
            }
        }
    }
    return $null
}

function Invoke-CopilotResolveMerge {
    $mergeTask = "Resuelve los conflictos de merge actuales manteniendo ambas funcionalidades, valida calidad con flake8, vulture, pytest y bandit, y finaliza el commit de merge sin hacer push."
    Write-Host "> copilot -p <merge-resolution-prompt> --model $Model --allow-all-tools --allow-all-paths --no-ask-user" -ForegroundColor DarkCyan

    if (-not $DryRun) {
        & copilot -p $mergeTask --model $Model --allow-all-tools --allow-all-paths --no-ask-user
        if ($LASTEXITCODE -ne 0) {
            throw "Fallo la resolucion automatica de conflicto con Copilot"
        }
    }
}

if (-not (Test-CommandExists -Name "git")) {
    throw "git no esta disponible en PATH."
}
if (-not (Test-CommandExists -Name "copilot")) {
    throw "copilot no esta disponible en PATH."
}

if (-not $DryRun) {
    if (-not (Test-CommandExists -Name "flake8")) { throw "flake8 no esta disponible." }
    if (-not (Test-CommandExists -Name "vulture")) { throw "vulture no esta disponible." }
    if (-not (Test-CommandExists -Name "pytest")) { throw "pytest no esta disponible." }
    if (-not (Test-CommandExists -Name "bandit")) { throw "bandit no esta disponible." }
}

$repoRoot = git rev-parse --show-toplevel 2>$null
if (-not $repoRoot) {
    throw "Este script debe ejecutarse dentro de un repositorio Git."
}

# Trabajamos desde el directorio del script (poc-parallel-agents) para que
# los quality checks encuentren main.py y test/. Los comandos git funcionan
# desde cualquier subdirectorio del repositorio.
Set-Location $PSScriptRoot

$dirty = git status --porcelain
if ($dirty) {
    Write-Warning "Hay cambios sin commit en el working tree."
}

if ((git branch --list $BaseBranch) -eq "") {
    throw "No existe la rama base '$BaseBranch'."
}
if ((git branch --list $Agent1Branch) -eq "") {
    throw "No existe la rama '$Agent1Branch'."
}
if ((git branch --list $Agent2Branch) -eq "") {
    throw "No existe la rama '$Agent2Branch'."
}

# Validate each agent branch before integration
# Si la rama ya está abierta en un worktree, se ejecutan los checks allí
# sin intentar cambiar de rama en el worktree principal.
$scriptSubdir = Split-Path $PSScriptRoot -Leaf

$wt1 = Get-WorktreePath -Branch $Agent1Branch
if ($wt1) {
    Write-Host "Usando worktree para $Agent1Branch : $wt1" -ForegroundColor DarkCyan
    Push-Location (Join-Path $wt1 $scriptSubdir)
    Invoke-QualityChecksWithAutoFix -Branch $Agent1Branch
    Pop-Location
} else {
    Invoke-Checked "git checkout $Agent1Branch"
    Push-Location $PSScriptRoot
    Invoke-QualityChecksWithAutoFix -Branch $Agent1Branch
    Pop-Location
}

$wt2 = Get-WorktreePath -Branch $Agent2Branch
if ($wt2) {
    Write-Host "Usando worktree para $Agent2Branch : $wt2" -ForegroundColor DarkCyan
    Push-Location (Join-Path $wt2 $scriptSubdir)
    Invoke-QualityChecksWithAutoFix -Branch $Agent2Branch
    Pop-Location
} else {
    Invoke-Checked "git checkout $Agent2Branch"
    Push-Location $PSScriptRoot
    Invoke-QualityChecksWithAutoFix -Branch $Agent2Branch
    Pop-Location
}

# Merge flow into base
Invoke-Checked "git checkout $BaseBranch"

if ($DryRun) {
    Invoke-Checked ('git merge --no-ff {0} -m "merge: integrate {0} into {1}"' -f $Agent1Branch, $BaseBranch)
    Invoke-Checked ('git merge --no-ff {0} -m "merge: integrate {0} into {1}"' -f $Agent2Branch, $BaseBranch)
} else {
    try {
        Invoke-Checked ('git merge --no-ff {0} -m "merge: integrate {0} into {1}"' -f $Agent1Branch, $BaseBranch)
    } catch {
        Write-Warning "Conflicto al fusionar $Agent1Branch. Lanzando Copilot para resolver."
        Invoke-CopilotResolveMerge
    }

    Invoke-QualityChecksWithAutoFix -Branch $BaseBranch

    try {
        Invoke-Checked ('git merge --no-ff {0} -m "merge: integrate {0} into {1}"' -f $Agent2Branch, $BaseBranch)
    } catch {
        Write-Warning "Conflicto al fusionar $Agent2Branch. Lanzando Copilot para resolver."
        Invoke-CopilotResolveMerge
    }
}

Invoke-QualityChecksWithAutoFix -Branch $BaseBranch
Invoke-Checked "git log --graph --oneline --all -n 12"

Write-Host "Integracion completada: $Agent1Branch y $Agent2Branch fusionadas en $BaseBranch con validaciones en verde." -ForegroundColor Green
