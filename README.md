# Extract Content Facebook Posts

Script Python để trích xuất nội dung các bài viết từ file JSON Facebook.

## Files trong project

- `Content-fb-TuanLe.json`: File JSON chứa dữ liệu Facebook posts (122MB)
- `extract_posts.py`: Script chính với nhiều tùy chọn
- `simple_extract.py`: Script đơn giản chỉ trích xuất nội dung text

## Cách sử dụng

### 1. Script đơn giản (Khuyến nghị cho lần đầu)

```bash
python simple_extract.py
```

Sẽ tạo file `facebook_posts_content.txt` chứa tất cả nội dung bài viết.

### 2. Script đầy đủ

#### Tạo 1 file duy nhất:
```bash
python extract_posts.py --mode single
```

#### Chia thành nhiều file nhỏ (100 bài/file):
```bash
python extract_posts.py --mode chunks --posts-per-file 100
```

#### Tùy chỉnh đường dẫn:
```bash
python extract_posts.py --input Content-fb-TuanLe.json --output my_output --mode chunks
```

## Tùy chọn dòng lệnh

- `--input, -i`: File JSON input (mặc định: Content-fb-TuanLe.json)
- `--output, -o`: Thư mục output (mặc định: extracted_posts)
- `--mode, -m`: Chế độ single hoặc chunks (mặc định: single)
- `--posts-per-file, -p`: Số bài viết mỗi file khi dùng chunks (mặc định: 100)

## Kết quả

- **Mode single**: Tạo 1 file `all_posts.txt` chứa tất cả bài viết
- **Mode chunks**: Tạo nhiều file `posts_part_001.txt`, `posts_part_002.txt`, ...
- **Simple extract**: Tạo file `facebook_posts_content.txt` với định dạng đơn giản

## Thông tin dữ liệu

- Fanpage: Tuan Le (baonam.kimchi)
- Tổng số posts: 1,349 bài
- Chủ đề chính: Khởi nghiệp, kinh doanh, chia sẻ kinh nghiệm
- Thời gian: Tháng 6/2025
