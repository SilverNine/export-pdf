# os: 파일 및 디렉터리 경로 작업에 사용
import os
# PyPDF2: PDF 파일을 읽고 쓰는 데 사용
from PyPDF2 import PdfReader, PdfWriter
# datetime: 타임스탬프 생성을 위해 사용.
from datetime import datetime

# pdf_folder: 원본 PDF 파일들이 있는 디렉터리
# output_folder: 처리된 PDF 파일을 저장할 디렉터리
# log_folder: 로그 파일을 저장할 디렉터리
def save_pdf(pdf_folder, output_folder, log_folder):
    # 센터별로 이미 처리된 사람 이름을 저장하는 딕셔너리
    processed = {}  
    # 처리된 조합 로그 파일 경로
    log_file_path = os.path.join(log_folder, "processed_combinations_log.txt")  
    # 처리된 파일 수 카운터
    count = 0  
    
    # os.walk: 지정된 디렉터리의 파일들을 재귀적으로 탐색
    for root, _, files in os.walk(pdf_folder):
        for filename in files:
            if filename.endswith('.pdf'):
                parts = filename.split('_')
                # 파일명이 예상된 형식을 따르는지 확인 ( "_" 가 포함되어 있어야 처리 대상에 포함 )
                if len(parts) > 2:  
                    # 센터 이름
                    center_name = parts[1]  
                    # 중간 이름
                    person_name = parts[2]  
                    
                    # "센터별"로 이미 처리된 사람 이름인지 확인
                    if center_name not in processed:
                        processed[center_name] = set()

                    # 이미 중간 이름이 있으면 패스
                    if person_name in processed[center_name]:
                        print(f"File already processed for {person_name} in center: {center_name}, skipping: {filename}")
                        continue
                    # 처음 처리한 사람이면 담아놓자
                    else:
                        processed[center_name].add(person_name)
                
                pdf_path = os.path.join(root, filename)
                try:
                    # PDF를 읽어서
                    reader = PdfReader(pdf_path)
                    # PDF 페이지 수가 7인 경우
                    if len(reader.pages) == 7:
                        writer = PdfWriter()
                        # 7번째 페이지 추출
                        writer.add_page(reader.pages[6])
                        # 타임스팸프를 파일명에 포함
                        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                        # PDF로 저장, 이미지로 저장하면 처리시간 대폭 증가
                        output_pdf_filename = f"{os.path.splitext(filename)[0]}_{timestamp}.pdf"
                        output_pdf_path = os.path.join(output_folder, output_pdf_filename)
                        # with open은 파일을 열고 작업한 후 자동으로 닫아준다.
                        with open(output_pdf_path, 'wb') as output_pdf_file:
                            writer.write(output_pdf_file)
                        # 저장된 파일 수 카운트
                        count += 1  
                except Exception as e:
                    continue

    # 로그 파일에 처리된 조합 저장
    with open(log_file_path, 'w') as log_file:
        log_file.write(f"Total processed files: {count}\n")
        combo_counter = 1
        for center, people in processed.items():
            for person in people:
                log_file.write(f"{combo_counter}. {person} in center: {center}\n")
                combo_counter += 1
    print(f"Processed combinations log saved to {log_file_path}")

source_folder = '/Users/SilverNine/Downloads/pdfs'
output_folder = '/Users/SilverNine/Downloads/export'
log_folder = '/Users/SilverNine/Downloads/logs'
save_pdf(source_folder, output_folder, log_folder)