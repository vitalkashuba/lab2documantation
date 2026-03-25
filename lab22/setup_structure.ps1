# Запусти цей скрипт в папці де хочеш створити проект
# Наприклад: cd "C:\Users\vital_o30\OneDrive\Desktop\Нова папка (2)\lab2_python"
# Потім: .\setup_structure.ps1

$files = @(
    "main.py",
    "requirements.txt",
    ".gitignore",
    "src/__init__.py",
    "src/domain/__init__.py",
    "src/domain/entities/__init__.py",
    "src/domain/entities/models.py",
    "src/domain/enums/__init__.py",
    "src/domain/enums/review_status.py",
    "src/dal/__init__.py",
    "src/dal/data_source.py",
    "src/dal/interfaces/__init__.py",
    "src/dal/interfaces/i_csv_reader.py",
    "src/dal/interfaces/i_repositories.py",
    "src/dal/repositories/__init__.py",
    "src/dal/repositories/csv_reader.py",
    "src/dal/repositories/repositories.py",
    "src/bll/__init__.py",
    "src/bll/interfaces/__init__.py",
    "src/bll/interfaces/i_data_import_service.py",
    "src/bll/services/__init__.py",
    "src/bll/services/data_import_service.py",
    "src/config/__init__.py",
    "src/config/container.py",
    "src/presentation/__init__.py",
    "src/presentation/interfaces/__init__.py",
    "src/presentation/interfaces/i_controllers.py",
    "src/utils/__init__.py",
    "src/utils/csv_generator.py"
)

foreach ($file in $files) {
    $dir = Split-Path $file
    if ($dir -and !(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    if (!(Test-Path $file)) {
        New-Item -ItemType File -Path $file -Force | Out-Null
    }
    Write-Host "OK $file"
}

# .gitignore вміст
Set-Content .gitignore @"
__pycache__/
*.pyc
*.sqlite
data/
.env
"@

Write-Host ""
Write-Host "Структура створена! Тепер скопіюй вміст файлів з архіву lab2_python_sqlalchemy.zip"
