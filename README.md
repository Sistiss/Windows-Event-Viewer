# Hệ Thống Cảnh Báo Sớm Tấn Công Dựa Trên Windows Event Viewer

## Giới thiệu

Dự án xây dựng hệ thống cảnh báo sớm các hành vi tấn công mạng thông qua việc phân tích log từ Windows Event Viewer. Hệ thống sử dụng ELK Stack để thu thập, lưu trữ và trực quan hóa dữ liệu log, kết hợp giữa phương pháp phát hiện dựa trên luật (Rule-based) và học máy (Machine Learning) nhằm phát hiện các hành vi bất thường và gửi cảnh báo theo thời gian thực.

## Mục tiêu

* Thu thập và phân tích log từ Windows Event Viewer.
* Phát hiện các hành vi tấn công phổ biến như Brute Force, Persistence,...
* Ứng dụng thuật toán Isolation Forest để phát hiện bất thường.
* Xây dựng Dashboard giám sát trực quan trên Kibana.
* Gửi cảnh báo tự động qua Telegram.

## Công nghệ sử dụng

* Python
* Elasticsearch
* Kibana
* Winlogbeat
* Docker
* Scikit-learn
* Pandas
* Telegram Bot API

## Chức năng chính

### Phát hiện dựa trên luật (Rule-Based)

* Phát hiện Brute Force thông qua Event ID 4625.
* Phát hiện tạo Scheduled Task bất thường.
* Giám sát các sự kiện liên quan đến thay đổi tài khoản và đặc quyền.

### Phát hiện bất thường bằng Machine Learning

Sử dụng thuật toán **Isolation Forest** để phát hiện:

* Tần suất đăng nhập bất thường.
* Hoạt động ngoài giờ hành chính.
* Hành vi khác biệt so với dữ liệu nền đã học.

## Các Event ID quan trọng

| Event ID | Mô tả                        |
| -------- | ---------------------------- |
| 4624     | Đăng nhập thành công         |
| 4625     | Đăng nhập thất bại           |
| 4672     | Đăng nhập với quyền đặc biệt |
| 4688     | Tạo tiến trình mới           |
| 4698     | Tạo Scheduled Task           |
| 4720     | Tạo tài khoản mới            |
| 4740     | Tài khoản bị khóa            |
| 1102     | Xóa log hệ thống             |


## Kết quả đạt được

* Thu thập và quản lý log tập trung bằng ELK Stack.
* Phát hiện hiệu quả các cuộc tấn công Brute Force.
* Nhận diện hành vi bất thường bằng Machine Learning.
* Trực quan hóa dữ liệu trên Kibana Dashboard.
* Gửi cảnh báo tức thời qua Telegram.

## Hướng phát triển

* Tích hợp Sysmon để thu thập log chi tiết hơn.
* Phân tích PowerShell Script Block Logging.
* Kết hợp log từ Firewall, IDS/IPS.
* Nâng cấp mô hình phát hiện bằng Deep Learning (LSTM).
* Tích hợp Threat Intelligence (VirusTotal, OTX).
* Tự động phản ứng khi phát hiện tấn công (SOAR).
* Triển khai kiến trúc phân tán với Kafka.

