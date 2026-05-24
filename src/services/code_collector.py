import os

class CodeCollectorService:
    def __init__(self, ignore_folders: set, ignore_relative_paths: set):
        self.ignore_folders = ignore_folders
        self.ignore_relative_paths = ignore_relative_paths

    def collect(self, base_path: str, extensions: list[str], custom_ignored_paths: list[str] = None) -> str:
        if not os.path.exists(base_path):
            raise FileNotFoundError(f"Directory not found: {base_path}")
        if not os.path.isdir(base_path):
            raise NotADirectoryError(f"Path is not a directory: {base_path}")

        all_code = []
        
        current_ignore_paths = set(self.ignore_relative_paths)
        if custom_ignored_paths:
            for cp in custom_ignored_paths:
                normalized = cp.replace("\\", "/").lower()
                if normalized:
                    current_ignore_paths.add(normalized)

        for root, dirs, files in os.walk(base_path):
            # Case-insensitive filtering for simple folder names
            dirs[:] = [d for d in dirs if d.lower() not in self.ignore_folders]

            # Filtering for relative paths
            valid_dirs = []
            for d in dirs:
                full_dir_path = os.path.join(root, d)
                relative_path = os.path.relpath(full_dir_path, base_path).replace("\\", "/").lower()
                
                if relative_path not in current_ignore_paths:
                    valid_dirs.append(d)
            
            dirs[:] = valid_dirs

            # File collection based on selected extensions
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                            all_code.append(f"// ==== {file_path} ====\n{content}\n")
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")

        return "\n".join(all_code)