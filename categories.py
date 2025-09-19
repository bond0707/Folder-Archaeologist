import os
from datetime import datetime as dt

def categorize_files():
    same_species = {}       # dict[str, list] -> Grouped by extension.
    large_fossils = []      # All files larger than 500 MB
    ancient_artifacts = []  # All files older than 1 year

    for (path, folders, files) in os.walk("C:\\Me\\Photos\\Wallpapers"):
        for file in files:
            fossil = os.path.join(path, file)
            fossil_type = os.path.basename(fossil).split(".")[-1]
            
            if fossil_type in same_species.keys():
                same_species[fossil_type].append(fossil)
            else:
                same_species[fossil_type] = [fossil]

            if (age := dt.now().timestamp() - os.path.getmtime(fossil)) > 31557600: # 1 year in seconds
                ancient_artifacts.append((fossil, age))
            
            if os.path.getsize(fossil) > 524288000: # 500 MB in bytes 
                # Dividing by 1 GB in bytes (1024 * 1024 * 1024)
                large_fossils.append((fossil, os.path.getsize(fossil)))
                # (fossil, f"{(os.path.getsize(fossil) / (1073741824)):.3}")
                
    large_fossils.sort(key=lambda x : x[1], reverse=True)
    ancient_artifacts.sort(key=lambda x : x[1], reverse=True)
    
    return (same_species, large_fossils, ancient_artifacts)
    
if __name__ == "__main__":
    pass