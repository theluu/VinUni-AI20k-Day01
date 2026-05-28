# Ngày 1 — Bài Tập & Phản Ánh
## Nền Tảng LLM API | Phiếu Thực Hành

**Thời lượng:** 1:30 giờ  
**Cấu trúc:** Lập trình cốt lõi (60 phút) → Bài tập mở rộng (30 phút)

---

## Phần 1 — Lập Trình Cốt Lõi (0:00–1:00)

Chạy các ví dụ trong Google Colab tại: https://colab.research.google.com/drive/172zCiXpLr1FEXMRCAbmZoqTrKiSkUERm?usp=sharing

Triển khai tất cả TODO trong `template.py`. Chạy `pytest tests/` để kiểm tra tiến độ.

**Điểm kiểm tra:** Sau khi hoàn thành 4 nhiệm vụ, chạy:
```bash
python template.py
```
Bạn sẽ thấy output so sánh phản hồi của GPT-4o và GPT-4o-mini.

---

## Phần 2 — Bài Tập Mở Rộng (1:00–1:30)

### Bài tập 2.1 — Độ Nhạy Của Temperature
Gọi `call_openai` với các giá trị temperature 0.0, 0.5, 1.0 và 1.5 sử dụng prompt **"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> Ở temperature=0.0, mô hình cho ra câu trả lời nhất quán, cụ thể và ít biến đổi — thường lặp lại cùng một sự kiện lịch sử hoặc địa lý rõ ràng. Khi temperature tăng lên 1.0–1.5, các phản hồi trở nên đa dạng hơn, sử dụng từ ngữ phong phú hơn và đôi khi đề cập đến những góc độ bất ngờ hoặc ít phổ biến hơn về Việt Nam. Tuy nhiên ở temperature=1.5, câu văn đôi khi kém mạch lạc hoặc lạc đề so với yêu cầu ban đầu.

**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> Nên đặt temperature=0.2. Chatbot hỗ trợ khách hàng cần trả lời chính xác, nhất quán và đáng tin cậy — tránh đưa ra thông tin sai hoặc mơ hồ. Temperature thấp giúp mô hình bám sát thông tin thực tế, đồng thời vẫn đủ linh hoạt để diễn đạt tự nhiên hơn mức 0.0 hoàn toàn cứng nhắc.

---

### Bài tập 2.2 — Đánh Đổi Chi Phí
Xem xét kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người thực hiện 3 lần gọi API, mỗi lần trung bình ~350 token.

**Ước tính xem GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này:**
> Tổng token mỗi ngày = 10.000 × 3 × 350 = 10.500.000 tokens.  
> Chi phí GPT-4o = 10.500.000 / 1.000 × $0.010 = **$105/ngày**  
> Chi phí GPT-4o-mini = 10.500.000 / 1.000 × $0.0006 = **$6.30/ngày**  
> GPT-4o đắt hơn GPT-4o-mini khoảng **16.7 lần** cho workload này (~$3.150 so với $189 mỗi tháng).

**Mô tả một trường hợp mà chi phí cao hơn của GPT-4o là xứng đáng, và một trường hợp GPT-4o-mini là lựa chọn tốt hơn:**
> GPT-4o xứng đáng khi xây dựng công cụ phân tích hợp đồng pháp lý hoặc báo cáo tài chính — nơi độ chính xác, khả năng suy luận phức tạp và chất lượng đầu ra ảnh hưởng trực tiếp đến quyết định kinh doanh quan trọng. Ngược lại, GPT-4o-mini phù hợp hơn cho các tác vụ đơn giản như phân loại email, trả lời FAQ, hoặc tóm tắt nội dung ngắn — nơi tốc độ và chi phí quan trọng hơn độ tinh tế của câu trả lời.

---

### Bài tập 2.3 — Trải Nghiệm Người Dùng với Streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì non-streaming lại phù hợp hơn?** (1 đoạn văn)
> Streaming quan trọng nhất trong các ứng dụng chatbot hoặc trợ lý AI tương tác trực tiếp với người dùng, đặc biệt khi câu trả lời dài — thay vì chờ toàn bộ response (có thể mất 5–10 giây), người dùng thấy token xuất hiện ngay lập tức, tạo cảm giác hệ thống đang "suy nghĩ" và phản hồi nhanh, cải thiện đáng kể trải nghiệm. Ngược lại, non-streaming phù hợp hơn khi xử lý batch (phân tích hàng loạt tài liệu, sinh báo cáo tự động), khi kết quả cần hoàn chỉnh trước khi xử lý tiếp (ví dụ: parse JSON từ response), hoặc trong các pipeline backend nơi không có người dùng trực tiếp theo dõi output.


## Danh Sách Kiểm Tra Nộp Bài
- [ ] Tất cả tests pass: `pytest tests/ -v`
- [ ] `call_openai` đã triển khai và kiểm thử
- [ ] `call_openai_mini` đã triển khai và kiểm thử
- [ ] `compare_models` đã triển khai và kiểm thử
- [ ] `streaming_chatbot` đã triển khai và kiểm thử
- [ ] `retry_with_backoff` đã triển khai và kiểm thử
- [ ] `batch_compare` đã triển khai và kiểm thử
- [ ] `format_comparison_table` đã triển khai và kiểm thử
- [ ] `exercises.md` đã điền đầy đủ
- [ ] Sao chép bài làm vào folder `solution` và đặt tên theo quy định 
