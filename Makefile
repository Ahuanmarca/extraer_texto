run:
	python3 main.py 2025_01A
	python3 main.py 2025_02A
	python3 main.py 2025_03A
	python3 main.py 2025_04A
	python3 main.py 2025_05A

clean:
	@echo "Limpiando archivos en output..."
	find carpeta_trabajo/output/010-steps -type f ! -name "*.py" ! -name ".gitkeep" -delete
	find carpeta_trabajo/output/020-output -type f ! -name "*.py" ! -name ".gitkeep" -delete
	find carpeta_trabajo/output/030-logs -type f ! -name "*.py" ! -name ".gitkeep" -delete
	find carpeta_trabajo/output/040-export-js -type f ! -name "*.py" ! -name ".gitkeep" -delete
