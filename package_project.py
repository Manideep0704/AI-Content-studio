from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

root = Path(__file__).parent / 'image-ai'
with ZipFile(root.parent / 'image-ai-completed.zip', 'w', ZIP_DEFLATED) as archive:
    for path in root.rglob('*'):
        relative = path.relative_to(root)
        if any(part in {'.venv', 'node_modules', '__pycache__', '.git', 'generated_images'} for part in relative.parts):
            continue
        if not path.is_file() or path.name == '.env' or path.suffix in {'.db', '.pyc'} or path.name in {'test_hf_out.png', 'test_pollinations.py', 'test_api.py'}:
            continue
        archive.write(path, Path('image-ai') / relative)
print('Created image-ai-completed.zip')
