SHELL := powershell.exe
.SHELLFLAGS := -NoProfile -Command

VENV := venv
PYTHON := $(VENV)\Scripts\python
PYTHON_EXE := $(VENV)\Scripts\python.exe
UV := uv
FORMAT := docx

.PHONY: help init clean convert

help:
	@Write-Host "Available targets:"
	@Write-Host "  init    : Create virtual environment and install dependencies (uv)"
	@Write-Host "  convert : Convert between Markdown, DOCX, and PDF (auto-detects direction)"
	@Write-Host "            MD to DOCX:  make convert INPUT=doc.md"
	@Write-Host "            MD to PDF:   make convert INPUT=doc.md FORMAT=pdf"
	@Write-Host "            DOCX to MD:  make convert INPUT=doc.docx"
	@Write-Host "            With output: make convert INPUT=doc.md OUTPUT=out.docx"
	@Write-Host "  clean   : Remove virtual environment"

init:
	@if (-not (Get-Command $(UV) -ErrorAction SilentlyContinue)) { throw "uv is required. Install it from https://docs.astral.sh/uv/getting-started/installation/" }
	$(UV) venv $(VENV) --clear
	@$(UV) pip install --native-tls --python "$(PYTHON_EXE)" -r requirements.txt; if ($$LASTEXITCODE -ne 0) { Write-Warning "uv pip install failed in this network; falling back to ensurepip + pip."; & "$(PYTHON_EXE)" -m ensurepip --upgrade; & "$(PYTHON_EXE)" -m pip install -r requirements.txt }

convert:
	& "$(PYTHON)" convert.py "$(INPUT)" "$(OUTPUT)" -f $(FORMAT)

clean:
	if (Test-Path $(VENV)) { Remove-Item -Recurse -Force $(VENV) }
