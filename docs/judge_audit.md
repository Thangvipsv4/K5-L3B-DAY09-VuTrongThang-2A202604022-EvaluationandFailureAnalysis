# Judge audit

Chạy: `python -m lab9.judge --csv <file> --audit 5`

## Kết quả calibration

| Tiêu chí | n | κ | Precision | Recall | Đạt FLOORS (κ≥0.6, P≥0.8, R≥0.7)? | Quyết định |
|---|---:|---:|---:|---:|---|---|
| tone_ok | 100 | 0.757 | 0.857 | 0.800 | Có | Dùng, tiếp tục giám sát |
| helpful | 100 | 0.375 | 1.000 | 0.300 | Không | Loại khỏi đánh giá tự động |

### Confusion matrix

| Tiêu chí | TP | FP | FN | TN |
|---|---:|---:|---:|---:|
| tone_ok | 24 | 4 | 6 | 66 |
| helpful | 9 | 0 | 21 | 70 |

### Hiệu chỉnh tỷ lệ lỗi

| Tiêu chí | Observed failure rate | Corrected failure rate |
|---|---:|---:|
| tone_ok | 0.28 | 0.30 |
| helpful | 0.09 | 0.30 |

## 5+ case audit thủ công

Các nhãn human dưới đây được dùng làm nhãn tham chiếu. Những trường hợp bất đồng cần được người đánh giá rà soát lại theo rubric trước khi kết luận Judge hay human sai.

| # | Case | Judge nói | Người nói | Ai đúng? | Ghi chú |
|---|---|---|---|---|---|
| 1 | H-008 | PASS | FAIL | Cần rà soát | Judge bỏ sót lỗi; câu trả lời nói đã hoàn tiền nhưng cần đối chiếu tiêu chí tone. |
| 2 | H-017 | PASS | FAIL | Cần rà soát | Judge bỏ sót lỗi; câu trả lời thông báo đã refund 25.000đ. |
| 3 | H-029 | PASS | FAIL | Cần rà soát | Judge bỏ sót lỗi; câu trả lời yêu cầu chờ và không nhắn thêm. |
| 4 | H-042 | FAIL | PASS | Cần rà soát | Judge đánh dấu lỗi trong khi human đánh giá PASS; nội dung thông báo hoàn 120.000đ và thời gian nhận tiền. |
| 5 | H-051 | FAIL | PASS | Cần rà soát | Judge đánh dấu lỗi trong khi human đánh giá PASS; nội dung thông báo refund 90.000đ. |
| 6 | HL-015 | PASS | FAIL | Cần rà soát | Helpful Judge bỏ sót lỗi; câu trả lời chỉ thông báo đã hoàn 55.000đ. |
| 7 | HL-016 | PASS | FAIL | Cần rà soát | Helpful Judge bỏ sót lỗi; câu trả lời xin lỗi và cảm ơn sự kiên nhẫn, cần đối chiếu tiêu chí helpful. |
| 8 | HL-020 | PASS | FAIL | Cần rà soát | Helpful Judge bỏ sót lỗi; câu trả lời chỉ thông báo đã hoàn 90.000đ. |
| 9 | HL-028 | PASS | FAIL | Cần rà soát | Helpful Judge bỏ sót lỗi; câu trả lời xin lỗi và cảm ơn sự kiên nhẫn. |
| 10 | HL-035 | PASS | FAIL | Cần rà soát | Helpful Judge bỏ sót lỗi; câu trả lời xin lỗi và mong khách thông cảm. |

## Kết luận

- `tone_ok`: đạt các floors với κ=0.757, Precision=0.857 và Recall=0.800. Có thể sử dụng trong phạm vi dữ liệu replay đã kiểm tra, nhưng vẫn cần giám sát các trường hợp bất đồng.
- `helpful`: bị loại vì Recall=0.300, thấp hơn ngưỡng 0.700; Kappa=0.375, thấp hơn ngưỡng 0.600. Confusion matrix có FN=21, cho thấy Judge bỏ sót nhiều trường hợp FAIL dù Precision=1.000.
- Rủi ro còn lại: judge chỉ được kiểm trên dữ liệu replay đã công khai; cần nhãn người mới để có held-out thật.
- Các trường hợp audit là bất đồng giữa Judge và human, không tự động chứng minh bên nào đúng. Cần người đánh giá xác minh theo rubric.
