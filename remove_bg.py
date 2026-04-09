from PIL import Image

def remove_bg(input_path):
    try:
        img = Image.open(input_path).convert("RGBA")
        width, height = img.size
        pixels = img.load()
        
        target_color = pixels[0, 0]
        
        def is_similar(c1, c2, tol=25):
            return abs(c1[0]-c2[0]) < tol and abs(c1[1]-c2[1]) < tol and abs(c1[2]-c2[2]) < tol

        visited = set()
        stack = [(0,0), (width-1, 0), (0, height-1), (width-1, height-1)]
        
        for start in stack:
            if start not in visited and is_similar(pixels[start], target_color):
                q = [start]
                while q:
                    x, y = q.pop()
                    if (x,y) in visited: continue
                    visited.add((x,y))
                    
                    # Also collect semi-transparent edge pixels for anti-aliasing simulation
                    pixels[x,y] = (255, 255, 255, 0)
                    
                    for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
                        nx, ny = x+dx, y+dy
                        if 0 <= nx < width and 0 <= ny < height:
                            if (nx, ny) not in visited and is_similar(pixels[nx, ny], target_color):
                                q.append((nx, ny))
                                
        img.save(input_path)
        print(f"Successfully removed background from {input_path}")
    except Exception as e:
        print(f"Failed to process {input_path}: {e}")

remove_bg("g:/マイドライブ/2nd-Brain/01_プロジェクト/fiore-site/images/poodle_white.png")
remove_bg("g:/マイドライブ/2nd-Brain/01_プロジェクト/fiore-site/images/poodle_black.png")
remove_bg("g:/マイドライブ/2nd-Brain/01_プロジェクト/fiore-site/images/poodle_brown.png")
