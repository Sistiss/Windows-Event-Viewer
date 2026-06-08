import time
import requests
import warnings
from elasticsearch import Elasticsearch, ElasticsearchWarning
from datetime import datetime, timedelta

# --- CẤU HÌNH TELEGRAM  ---
TELEGRAM_TOKEN = ""
TELEGRAM_CHAT_ID = ""

# Tắt cảnh báo SSL 
warnings.filterwarnings('ignore', category=ElasticsearchWarning)

# Kết nối Elasticsearch
es = Elasticsearch(['http://localhost:9200'])

def send_telegram_alert(message):
    """Gửi tin nhắn cảnh báo về Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown" 
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print(">>> Đã gửi cảnh báo Telegram thành công!")
        else:
            print(f"!!! Lỗi gửi Telegram: {response.text}")
    except Exception as e:
        print(f"!!! Không kết nối được Telegram: {e}")



def check_persistence():
    # Lấy thời gian 1 giờ
    minutes=60
    
    # Query tìm Event 4625
    query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"winlog.event_id": 4625}},
                    {"range": {"@timestamp": {"gte": minutes}}}
                ]
            }
        }
    }
    
    try:
        # Tìm kiếm log
        res = es.search(index="winlogbeat-*", body=query, size=100)
        
        # Nếu tìm thấy ít nhất 1 sự kiện
        if res['hits']['total']['value'] > 0:
            print(">>> PHÁT HIỆN HÀNH VI FAILED LOGIN!")
            
            # Lấy chi tiết tên Task để báo cáo
            log_detail = res['hits']['hits'][0]['_source']
            task_name = log_detail['winlog']['event_data']['TaskName']
            
            msg_content = (
                f"🚨 **CẢNH BÁO BẢO MẬT (Kịch bản 2)** 🚨\n"
                f"--------------------------\n"
                f"Phát hiện hành vi tạo Scheduled Task đáng ngờ!\n"
                f"📂 Tên Task: **{task_name}**\n"
                f"🆔 Event ID: **4625**\n"
                f"⚠️ Loại hành vi: **Failed Login Attempts**"
            )
            
            send_telegram_alert(msg_content)
            
    except Exception as e:
        print(f"Lỗi truy vấn persistence: {e}")

# Cập nhật vòng lặp chính
if __name__ == "__main__":
    print("--- BẮT ĐẦU GIÁM SÁT HỆ THỐNG ---")
    while True:
        check_persistence() 
        time.sleep(10)