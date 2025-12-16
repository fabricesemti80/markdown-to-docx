SHELL := powershell.exe
.SHELLFLAGS := -NoProfile -Command

VENV := venv
PYTHON := $(VENV)\Scripts\python
PIP := $(VENV)\Scripts\pip

.PHONY: help setup clean convert

help:
	@Write-Host "Available targets:"
	@Write-Host "  setup   : Create virtual environment and install dependencies"
	@Write-Host "  convert : Convert Markdown to DOCX (requires INPUT and OUTPUT variables)"
	@Write-Host "            Example: make convert INPUT=test.md OUTPUT=test.docx"
	@Write-Host "  clean   : Remove virtual environment"

setup:
	python -m venv $(VENV) --without-pip
	& "$(PYTHON)" -m ensurepip
	& "$(PYTHON)" -m pip install -r requirements.txt

convert:
	& "$(PYTHON)" convert.py "$(INPUT)" "$(OUTPUT)"

clean:
	if (Test-Path $(VENV)) { Remove-Item -Recurse -Force $(VENV) }
