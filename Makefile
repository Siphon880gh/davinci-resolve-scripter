# Makefile for renaming folders/files

# Define the rename map
RENAME_MAP := \
    console_drop_scripts 0console_drop_scripts \
    generate-otio.py 1generate-otio.py \
    console_input_scripts 2console_input_scripts

# Default target: show available options
.DEFAULT_GOAL := help

help:
	@echo "Available options:"
	@echo "  make hint   - Rename folders/files as to names that hint the sequence of scripts to run to automate DaVinci Resolve videos"
	@echo "  make clean  - Restore folders/files to original names removing the number prefixes"

# Target to rename folders/files according to the map
hint:
	@echo "Renaming folders/files..."
	$(foreach orig, $(filter-out 0% 1% 2%, $(RENAME_MAP)), \
		$(if $(wildcard $(orig)), \
			mv $(orig) $(word 2, $(RENAME_MAP)); \
			echo "Hint filled name of $(orig) to $(word 2, $(RENAME_MAP))";, \
			echo "File/Folder $(orig) not found, not appropriate option at this time or may have been named already, or you manually renamed it.";) \
		$(eval RENAME_MAP := $(wordlist 3, $(words $(RENAME_MAP)), $(RENAME_MAP))) \
	)

# Target to undo the renaming (restore original names)
clean:
	@echo "Restoring folders/files..."
	$(foreach new, $(filter 0% 1% 2%, $(RENAME_MAP)), \
		$(if $(wildcard $(new)), \
			mv $(new) $(word 1, $(RENAME_MAP)); \
			echo "Cleaned name of $(new) to $(word 1, $(RENAME_MAP))";, \
			echo "File/Folder $(new) not found, not appropriate option at this time or may have been named already, or you manually renamed it.";) \
		$(eval RENAME_MAP := $(wordlist 3, $(words $(RENAME_MAP)), $(RENAME_MAP))) \
	)
