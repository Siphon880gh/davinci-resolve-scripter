# Makefile for renaming folders/files into names that hint the sequence of scripts to run to automate DaVinci Resolve videos

# Define the rename pairs
RENAME_PAIRS := \
	letterbox 01_letterbox \
	unassemble__drop_scripts 02_unassemble__drop_scripts \
	generate_otio 03_generate_otio \
	motion__input_scripts 04_motion__input_scripts \
	subtitle_from_audio 05_subtitle_from_audio \
	luts 06_luts

# Default target: show available options
.DEFAULT_GOAL := help

help:
	@echo "Available options:"
	@echo "  make hint   - Rename folders/files to names that hint the sequence of scripts to run to automate DaVinci Resolve videos"
	@echo "  make clean  - Restore folders/files to original names, removing the number prefixes"

# Target to rename folders/files according to the map
hint:
	@echo "Renaming folders/files..."
	@set -e; \
	set -- $(RENAME_PAIRS); \
	while [ "$$#" -gt 0 ]; do \
		orig="$$1"; \
		new="$$2"; \
		if [ -e "$$orig" ]; then \
			mv "$$orig" "$$new"; \
			echo "Renamed $$orig to $$new"; \
		else \
			echo "File/Folder $$orig not found."; \
		fi; \
		shift 2; \
	done

# Target to undo the renaming (restore original names)
clean:
	@echo "Restoring folders/files..."
	@set -e; \
	set -- $(RENAME_PAIRS); \
	while [ "$$#" -gt 0 ]; do \
		orig="$$1"; \
		new="$$2"; \
		if [ -e "$$new" ]; then \
			mv "$$new" "$$orig"; \
			echo "Restored $$new to $$orig"; \
		else \
			echo "File/Folder $$new not found."; \
		fi; \
		shift 2; \
	done
