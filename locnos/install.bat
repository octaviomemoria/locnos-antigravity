@echo off
echo ========================================
echo   LOCNOS - Instalacao Automatica
echo ========================================
echo.

REM Verificar se estamos no diretorio correto
if not exist "backend\package.json" (
    echo ERRO: Execute este script da pasta 'locnos'
    echo.
    echo Caminho correto:
    echo   cd locnos
    echo   install.bat
    pause
    exit /b 1
)

echo [1/4] Instalando dependencias do backend...
cd backend
call npm install
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar dependencias
    pause
    exit /b 1
)

echo.
echo [2/4] Criando arquivo .env...
if not exist ".env" (
    copy .env.example .env
    echo Arquivo .env criado! Configure o MONGODB_URI antes de continuar.
) else (
    echo Arquivo .env ja existe.
)

echo.
echo [3/4] Deseja popular o banco de dados agora? (S/N)
set /p resposta=
if /i "%resposta%"=="S" (
    echo Populando banco de dados...
    call npm run seed
)

echo.
echo ========================================
echo   INSTALACAO CONCLUIDA!
echo ========================================
echo.
echo Proximos passos:
echo   1. Configure o arquivo backend\.env
echo   2. Execute: cd backend
echo   3. Execute: npm run dev
echo.
echo Credenciais de teste:
echo   Admin: admin@locnos.com.br / admin123
echo   Cliente: joao@email.com / senha123
echo.
pause
