from elasticsearch import Elasticsearch
import warnings
from datetime import datetime
import time

# Tắt cảnh báo đỏ
warnings.filterwarnings("ignore")

# Kết nối
es = Elasticsearch(['http://localhost:9200'])

print(f"--- BẮT ĐẦU QUÉT LÚC {datetime.now().strftime('%H:%M:%S')} ---")

def scan():
    # Quét log trong 1 tiếng qua để chắc chắn bắt được dữ liệu cũ của bạn
    query = {
        "query": {
            "bool": {
                "must": [
                    # thay đổi event.code để quét các loại log khác nếu cần
                    {"match": {"event.code": 4625}}, 
                    {"range": {"@timestamp": {"gte": "now-1h"}}} 
                ]
            }
        }
    }

    try:
        res = es.search(index="winlogbeat-*", body=query, size=500)
        hits = res['hits']['hits']
        total_logs = len(hits)

        if total_logs > 0:
            print("\n" + "="*45)
            print(f"!!! CẢNH BÁO: PHÁT HIỆN {total_logs} LẦN ĐĂNG NHẬP SAI !!!")
            
            # Lấy log mới nhất để phân tích kỹ
            latest_log = hits[0]['_source']
            
            # --- PHẦN SỬA ĐỔI ĐỂ LẤY TÊN USER ---
            user = latest_log.get('winlog', {}).get('event_data', {}).get('TargetUserName')
            
            if not user:
                user = latest_log.get('user', {}).get('name')
                
            if not user:
                user = latest_log.get('related', {}).get('user')
                
            if not user:
                user = "Unknown (Không xác định)"
            # ------------------------------------

            ip = latest_log.get('source', {}).get('ip', 'Localhost/Unknown')
            timestamp = latest_log.get('@timestamp')
            
            print(f"- Thời gian: {timestamp}")
            print(f"- Tài khoản bị tấn công: {user}")
            print(f"- IP nguồn tấn công: {ip}")
            print("="*45 + "\n")
            return True
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Chưa phát hiện thêm log mới...", end='\r')
            return False

    except Exception as e:
        print(f"Lỗi: {e}")
        return False

# Chạy vòng lặp
while True:
    found = scan()
    if found:
        print("\nĐã lấy được đầy đủ thông tin!")
        input("Nhấn Enter để thoát chương trình...")
        break
    time.sleep(5)