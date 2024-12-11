import os

def count_total_lines_in_txt_files_MC(directory):
    total_lines = 0
    # 디렉토리 내 모든 파일을 순회
    for filename in os.listdir(directory):
        if filename.endswith("*MC*.txt"):  # .txt 파일만 선택
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    total_lines += len(lines)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    
    print(f"Total number of lines in all .txt files: {total_lines}")

def count_total_lines_in_txt_files(directory):
    total_lines = 0
    # 디렉토리 내 모든 파일을 순회
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):  # .txt 파일만 선택
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    total_lines += len(lines)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    
    print(f"Total number of lines in all .txt files: {total_lines}")

# 사용 예시
directory_path = "data"  # 디렉토리 경로 수정
count_total_lines_in_txt_files(directory_path)
count_total_lines_in_txt_files_MC(directory_path)
