SHELL := powershell.exe
.SHELLFLAGS := -NoProfile -Command

VENV := .venv
PYTHON_EXE := $(VENV)\Scripts\python.exe
UV := uv

.PHONY: help init clean convert

help:
	@Write-Host "Available targets:"
	@Write-Host "  init    : Create .venv and sync dependencies from uv.lock (uv sync)"
	@Write-Host "  convert : Convert between Markdown, DOCX, and PDF (auto-detects direction)"
	@Write-Host "            MD to DOCX:  make convert INPUT=doc.md"
	@Write-Host "            MD to PDF:   make convert INPUT=doc.md FORMAT=pdf"
	@Write-Host "            Prompt fmt:  make convert INPUT=doc.md"
	@Write-Host "            DOCX to MD:  make convert INPUT=doc.docx"
	@Write-Host "            With output: make convert INPUT=doc.md OUTPUT=out.docx"
	@Write-Host "  clean   : Remove virtual environment"

init:
	@if (-not (Get-Command $(UV) -ErrorAction SilentlyContinue)) { throw "uv is required. Install it from https://docs.astral.sh/uv/getting-started/installation/" }
	@$(UV) sync --native-tls; if ($$LASTEXITCODE -ne 0) { Write-Warning "uv sync failed in this network; falling back to ensurepip + pip."; & "$(PYTHON_EXE)" -m ensurepip --upgrade; & "$(PYTHON_EXE)" -m pip install -r requirements.txt }

convert:
	$(UV) run --no-sync python convert.py "$(INPUT)" "$(OUTPUT)" $(if $(FORMAT),-f $(FORMAT),)

clean:
	if (Test-Path $(VENV)) { Remove-Item -Recurse -Force $(VENV) }
