@echo off
REM README Updater for Windows - A script to automatically update README.md after git pushes

setlocal enabledelayedexpansion

if "%1"=="init" (
    call :init_repo
    call :create_readme
    call :setup_git_hooks
    echo Repository initialized with README.md and git hooks.
    goto :eof
)

if "%1"=="update" (
    call :update_readme
    goto :eof
)

echo Usage: %0 {init^|update}
echo   init   - Initialize repository with README.md and git hooks
echo   update - Update README.md with latest commit information
goto :eof

:init_repo
if not exist .git (
    echo Initializing git repository...
    git init
    echo Git repository created.
) else (
    echo Git repository already exists.
)
goto :eof

:create_readme
if not exist README.md (
    echo Creating initial README.md...
    (
        echo # Project Documentation
        echo.
        echo ## Overview
        echo This is the main documentation for the project.
        echo.
        echo ## Recent Updates
        echo ^| Date ^| Description ^|
        echo ^|------^|-------------^|
        echo.
        echo ## Getting Started
        echo Instructions for getting started with the project.
        echo.
        echo ## Features
        echo Key features of the project.
    ) > README.md
    echo README.md created.
) else (
    echo README.md already exists.
)
goto :eof

:update_readme
echo Updating README.md with latest commit info...

REM Get the latest commit message and date
for /f "tokens=*" %%a in ('git log -1 --pretty^=format:"%%h"') do set LATEST_COMMIT=%%a
for /f "tokens=*" %%a in ('git log -1 --pretty^=format:"%%ad" --date^=short') do set COMMIT_DATE=%%a
for /f "tokens=*" %%a in ('git log -1 --pretty^=format:"%%s"') do set COMMIT_MSG=%%a

REM Create a temporary file
type README.md > temp_readme.md

REM Find the line number after the Recent Updates table header
set LINE_NUM=0
set FOUND_HEADER=0
for /f "tokens=1,* delims=:" %%a in ('findstr /n "^" temp_readme.md') do (
    if "!FOUND_HEADER!"=="1" (
        set /a LINE_NUM=%%a
        set FOUND_HEADER=2
        goto :break_loop
    )
    if "%%b"=="|------|-------------|" set FOUND_HEADER=1
)
:break_loop

if !LINE_NUM! GTR 0 (
    REM Create a new file with the update inserted
    set /a INSERT_LINE=!LINE_NUM!
    set COUNTER=0
    (
        for /f "tokens=1,* delims=:" %%a in ('findstr /n "^" temp_readme.md') do (
            set /a COUNTER+=1
            if !COUNTER!==!INSERT_LINE! (
                echo ^| !COMMIT_DATE! ^| !COMMIT_MSG! (!LATEST_COMMIT!^) ^|
            )
            echo %%b
        )
    ) > new_readme.md
    move /y new_readme.md README.md > nul
    echo README.md updated with latest commit information.
) else (
    echo Could not find the table header in README.md.
)

del temp_readme.md
goto :eof

:setup_git_hooks
echo Setting up git hooks...

if not exist .git\hooks mkdir .git\hooks

(
    echo #!/bin/sh
    echo # Post-commit hook to update README.md
    echo.
    echo # Run the README updater script
    echo cmd /c readme_updater.bat update
) > .git\hooks\post-commit

echo Git hooks configured.
goto :eof

endlocal