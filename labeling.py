import pandas as pd
import os

def convert_to_yolo_format(coordinates_str, img_w, img_h, class_id):
    if pd.isna(coordinates_str):
        return ""
    pairs = coordinates_str.split(';')
    coordinates = [list(map(float, pair.split(','))) for pair in pairs]
    
    #TODO: sol aşşa, sol üst, sağ üst , sağ aşşa şeklinde sırala
    coordinates = sorted(coordinates, key=lambda x: (x[0], x[1]))
    bottom_left = coordinates[0]
    top_left = coordinates[1] if coordinates[1][1] > bottom_left[1] else coordinates[2]
    top_right = coordinates[2] if coordinates[2][1] > bottom_left[1] else coordinates[1]
    bottom_right = coordinates[3]
    
    aw = (bottom_right[0] - bottom_left[0]) / img_w
    ah = (top_left[1] - bottom_left[1]) / img_h
    
    aox = 0.5 + (((coordinates[0][0] + coordinates[2][0]) / 2) / img_w)
    aoy = 0.5 + (((coordinates[0][1] + coordinates[1][1]) / 2) / img_h)
    
    yolo_format = f"{class_id} {aox:.6f} {aoy:.6f} {aw:.6f} {ah:.6f}"
    print(yolo_format)
    return yolo_format

def process_folders(base_folder, df):
    print(df.head())
    class_ids = ["Normal", "Kitle", "Kalsifikasyon"]
    try:
        for index, row in df.iterrows():
            if pd.isna(row['ETIKETKOORDINATLARI']):  
                print("Column 'ETIKETKOORDINATLARI' is NaN, skipping...")
                continue
            
            main_folder = os.path.join(base_folder, row['KATEGORI'][:9])
            sub_folder = os.path.join(main_folder, str(row['HASTAID']))  

            if not os.path.exists(sub_folder):
                print(f"Subfolder {sub_folder} does not exist, skipping...")
                continue

            yolo_format = convert_to_yolo_format(row['ETIKETKOORDINATLARI'], 2364, 2964, class_ids.index(row['ETIKETADI']))
            file_name = f"{row['DOSYAADI'].split('.')[0]}.txt"
            file_path = os.path.join(sub_folder, file_name)

            with open(file_path, 'a') as f:
                f.write(yolo_format + '\n')
    except Exception as e:
        print(f"An error occurred: {e}")


csv_path = r"C:\Users\bedir\OneDrive\Masaüstü\YMIR\TEKNOFEST\DATASETS\veribilgisi.csv"
df = pd.read_csv(csv_path, sep=';', on_bad_lines='skip')

print("Column names:", df.columns)

base_folder = r"C:\Users\bedir\OneDrive\Masaüstü\YMIR\TEKNOFEST\DATASETS\dataset"

process_folders(base_folder, df)
