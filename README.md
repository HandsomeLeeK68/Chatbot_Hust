# 🎓 Chatbot HUST - Trợ lý Hỏi đáp Quy chế

Một chatbot Trợ lý AI, được xây dựng để giúp sinh viên Đại học Bách khoa Hà Nội (HUST) tra cứu nhanh chóng và chính xác các thông tin về quy chế, quy định, học vụ, và học bổng của nhà trường.

## 🌟 Giới thiệu

Sinh viên HUST thường xuyên cần tra cứu thông tin trong một khối lượng lớn các văn bản quy chế, cẩm nang sinh viên, và thông báo từ các phòng ban. Việc tìm kiếm thủ công tốn nhiều thời gian và không phải lúc nào cũng ra được kết quả mong muốn.

Dự án này xây dựng một Trợ lý AI (Chatbot) sử dụng mô hình RAG (Retrieval-Augmented Generation) để cung cấp câu trả lời bằng ngôn ngữ tự nhiên cho các câu hỏi của sinh viên. Thay vì tự "nghĩ" ra câu trả lời (dễ dẫn đến "ảo giác" thông tin), chatbot sẽ *truy xuất* các thông tin liên quan trực tiếp từ kho văn bản quy chế của trường và *tổng hợp* lại để tạo ra câu trả lời chính xác, đáng tin cậy.

Sinh viên có thể hỏi về mọi thứ, từ:
* Điều kiện xét học bổng khuyến khích học tập.
* Quy định về cảnh cáo học vụ, buộc thôi học.
* Số tín chỉ tối thiểu/tối đa mỗi kỳ.
* Thủ tục tốt nghiệp, làm đồ án.
* Và bất kỳ quy định nào khác.

## 📸 Demo
![Demo Giao diện Chatbot](https://github.com/user-attachments/assets/542e4ff0-8389-4656-8b44-18c7184861e6)

## ✨ Tính năng chính

* *Hỏi đáp Ngôn ngữ Tự nhiên:* Đặt câu hỏi như đang trò chuyện với một người tư vấn.
* *Chính xác & Tin cậy:* Câu trả lời được tạo ra dựa trên nguồn tài liệu chính thống của HUST, hạn chế tối đa việc bịa đặt thông tin.
* *Nhanh chóng:* Cung cấp câu trả lời tức thì, tiết kiệm thời gian tìm kiếm.
* *Giao diện Thân thiện:* Giao diện chat đơn giản, trực quan được xây dựng bằng Streamlit.
* *Chế độ Sáng/Tối:* Tích hợp nút chuyển đổi giao diện Light/Dark mode.

## 🛠️ Kiến trúc & Công nghệ sử dụng

Dự án này áp dụng kiến trúc *RAG (Retrieval-Augmented Generation)*.

1.  *Giao diện người dùng (Frontend):*
    * *[Streamlit](https://streamlit.io/):* Được sử dụng để xây dựng giao diện web-app chatbot một cách nhanh chóng.

2.  *Hệ thống lõi (Backend):*
    * *[LangChain](https://www.langchain.com/):* Framework chính để kết nối các thành phần của hệ thống RAG.
    * *[CTransformers](https://github.com/marella/ctransformers):* Thư viện để chạy các mô hình LLM (định dạng GGUF) cục bộ trên CPU/GPU.
    * *Mô hình Ngôn ngữ (LLM):* Sử dụng vinallama-7b-chat_q5_0.gguf (hoặc một mô hình tương tự) để sinh câu trả lời.
    * *Cơ sở dữ liệu Vector (Vector DB):*
        * *[FAISS](https://faiss.ai/):* Thư viện của Facebook để tìm kiếm tương đồng (similarity search) siêu nhanh.
        * *[HuggingFace Embeddings](https://huggingface.co/models?pipeline_tag=sentence-similarity):* Sử dụng một mô hình (ví dụ: GPT4AllBgeEmbeddings) để vector hóa văn bản.

### Luồng hoạt động

1.  *(Offline) Xử lý Dữ liệu:* Các văn bản quy chế (.pdf, .txt, .docx) được thu thập, cắt thành các đoạn nhỏ (chunks), vector hóa và lưu trữ trong một cơ sở dữ liệu vector FAISS (tại vectorstores/db_faiss).
2.  *(Online) Truy vấn:*
    * Người dùng nhập câu hỏi qua giao diện Streamlit.
    * Câu hỏi được vector hóa.
    * Hệ thống RetrievalQA của LangChain sử dụng FAISS để tìm *3* đoạn văn bản (k=3) trong kho tài liệu có nội dung liên quan nhất đến câu hỏi.
3.  *(Online) Sinh câu trả lời:*
    * Các đoạn văn bản liên quan (context) và câu hỏi (question) được đưa vào một *Prompt Template* (khuôn mẫu câu lệnh).
    * Prompt này được gửi đến mô hình vinallama-7b-chat.
    * Mô hình LLM sẽ tổng hợp thông tin chỉ từ context được cung cấp để tạo ra câu trả lời cuối cùng.

## 🚀 Cài đặt & Chạy dự án

Bạn có thể chạy dự án này hoàn toàn trên máy cục bộ (offline).

### 1. Yêu cầu hệ thống

* [Python 3.9+](https://www.python.org/)
* [Git](https://git-scm.com/)

### 2. Các bước cài đặt

*Bước 1: Clone kho lưu trữ*
```bash
git clone [https://github.com/ten-cua-ban/ten-du-an.git](https://github.com/ten-cua-ban/ten-du-an.git)
cd ten-du-an
