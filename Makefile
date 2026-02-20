SHELL := powershell.exe
.SHELLFLAGS := -NoProfile -Command

VENV := venv
PYTHON := $(VENV)\Scripts\python
PIP := $(VENV)\Scripts\pip

.PHONY: help init clean convert

help:
	@Write-Host "Available targets:"
	@Write-Host "  init    : Create virtual environment and install dependencies"
	@Write-Host "  convert : Convert between Markdown and DOCX (auto-detects direction)"
	@Write-Host "            MD to DOCX:  make convert INPUT=doc.md"
	@Write-Host "            DOCX to MD:  make convert INPUT=doc.docx"
	@Write-Host "            With output: make convert INPUT=doc.md OUTPUT=out.docx"
	@Write-Host "  clean   : Remove virtual environment"

init:
	python -m venv $(VENV) --without-pip
	& "$(PYTHON)" -m ensurepip
	& "$(PYTHON)" -m pip install -r requirements.txt

convert:
	& "$(PYTHON)" convert.py "$(INPUT)" "$(OUTPUT)"

clean:
	if (Test-Path $(VENV)) { Remove-Item -Recurse -Force $(VENV) }
