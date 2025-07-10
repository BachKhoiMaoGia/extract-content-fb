#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để trích xuất nội dung các bài viết từ file JSON Facebook
Author: GitHub Copilot
Date: July 10, 2025
"""

import json
import os
import sys
from datetime import datetime
import argparse

def convert_timestamp(timestamp):
    """Chuyển đổi Unix timestamp thành định dạng datetime readable"""
    try:
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    except:
        return "Unknown"

def clean_text(text):
    """Làm sạch và định dạng lại text content"""
    if not text:
        return ""
    
    # Giữ nguyên format xuống dòng và khoảng trắng
    # Chỉ loại bỏ các ký tự escape không cần thiết
    cleaned = text.replace('\\/', '/')
    return cleaned.strip()

def extract_posts_content(json_file_path, output_dir="extracted_posts"):
    """
    Trích xuất nội dung các bài viết từ file JSON
    
    Args:
        json_file_path: Đường dẫn đến file JSON
        output_dir: Thư mục đầu ra cho các file txt
    """
    
    print(f"🔄 Đang xử lý file: {json_file_path}")
    
    # Tạo thư mục output nếu chưa tồn tại
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 Đã tạo thư mục: {output_dir}")
    
    # Đọc file JSON
    try:
        print("📖 Đang đọc file JSON...")
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Lỗi khi đọc file JSON: {e}")
        return
    
    # Lấy thông tin metadata
    fanpage_id = data.get('fanpage_id', 'Unknown')
    scan_time = data.get('scan_start_time', 'Unknown')
    total_posts = data.get('total_posts_processed', 0)
    posts = data.get('posts', [])
    
    print(f"📊 Thông tin fanpage:")
    print(f"   - Fanpage ID: {fanpage_id}")
    print(f"   - Thời gian scan: {scan_time}")
    print(f"   - Tổng số posts được xử lý: {total_posts}")
    print(f"   - Số posts trong data: {len(posts)}")
    
    # Tạo file tổng hợp tất cả bài viết
    all_posts_file = os.path.join(output_dir, "all_posts.txt")
    posts_with_content = 0
    
    with open(all_posts_file, 'w', encoding='utf-8') as all_file:
        # Header cho file tổng hợp
        all_file.write("=" * 80 + "\n")
        all_file.write("TỔNG HỢP NỘI DUNG CÁC BÀI VIẾT FACEBOOK\n")
        all_file.write("=" * 80 + "\n")
        all_file.write(f"Fanpage ID: {fanpage_id}\n")
        all_file.write(f"Thời gian scan: {scan_time}\n")
        all_file.write(f"Tổng số posts: {total_posts}\n")
        all_file.write("=" * 80 + "\n\n")
        
        # Xử lý từng bài viết
        for idx, post in enumerate(posts, 1):
            try:
                # Lấy thông tin cơ bản
                post_id = post.get('post_id', f'post_{idx}')
                creation_time = post.get('creation_time')
                url = post.get('url', '')
                
                # Lấy nội dung message
                message = post.get('message', {})
                if not message:
                    continue
                    
                text_content = message.get('text', '')
                if not text_content or text_content.strip() == '':
                    continue
                
                # Lấy thông tin tác giả
                actors = post.get('actors', [])
                author_name = "Unknown"
                if actors:
                    author_name = actors[0].get('name', 'Unknown')
                
                # Làm sạch nội dung
                clean_content = clean_text(text_content)
                
                # Chuyển đổi timestamp
                formatted_time = convert_timestamp(creation_time) if creation_time else "Unknown"
                
                posts_with_content += 1
                
                # Ghi vào file tổng hợp
                all_file.write(f"BÀI VIẾT #{posts_with_content}\n")
                all_file.write("-" * 50 + "\n")
                all_file.write(f"Post ID: {post_id}\n")
                all_file.write(f"Tác giả: {author_name}\n")
                all_file.write(f"Thời gian: {formatted_time}\n")
                all_file.write(f"URL: {url}\n")
                all_file.write("-" * 50 + "\n")
                all_file.write(f"{clean_content}\n")
                all_file.write("\n" + "=" * 80 + "\n\n")
                
                # Tạo file riêng cho mỗi bài viết (tùy chọn)
                # individual_file = os.path.join(output_dir, f"post_{posts_with_content:04d}.txt")
                # with open(individual_file, 'w', encoding='utf-8') as individual:
                #     individual.write(f"Post ID: {post_id}\n")
                #     individual.write(f"Tác giả: {author_name}\n")
                #     individual.write(f"Thời gian: {formatted_time}\n")
                #     individual.write(f"URL: {url}\n")
                #     individual.write("-" * 50 + "\n")
                #     individual.write(f"{clean_content}\n")
                
                # In progress mỗi 100 bài
                if posts_with_content % 100 == 0:
                    print(f"⏳ Đã xử lý {posts_with_content} bài viết có nội dung...")
                    
            except Exception as e:
                print(f"⚠️  Lỗi khi xử lý bài viết #{idx}: {e}")
                continue
    
    print(f"✅ Hoàn thành!")
    print(f"📈 Kết quả:")
    print(f"   - Tổng số bài viết được xử lý: {len(posts)}")
    print(f"   - Số bài viết có nội dung: {posts_with_content}")
    print(f"   - File đầu ra: {all_posts_file}")
    print(f"   - Kích thước file đầu ra: {os.path.getsize(all_posts_file) / (1024*1024):.2f} MB")

def extract_posts_by_chunks(json_file_path, output_dir="extracted_posts", posts_per_file=100):
    """
    Trích xuất và chia nhỏ nội dung thành nhiều file
    
    Args:
        json_file_path: Đường dẫn đến file JSON
        output_dir: Thư mục đầu ra
        posts_per_file: Số bài viết mỗi file
    """
    
    print(f"🔄 Đang xử lý file và chia thành chunks: {json_file_path}")
    
    # Tạo thư mục output
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Đọc file JSON
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Lỗi khi đọc file JSON: {e}")
        return
    
    posts = data.get('posts', [])
    fanpage_id = data.get('fanpage_id', 'Unknown')
    
    current_file_num = 1
    posts_in_current_file = 0
    posts_with_content = 0
    current_file = None
    
    for idx, post in enumerate(posts, 1):
        try:
            # Lấy nội dung
            message = post.get('message', {})
            if not message:
                continue
                
            text_content = message.get('text', '')
            if not text_content or text_content.strip() == '':
                continue
            
            # Nếu cần tạo file mới
            if posts_in_current_file == 0:
                if current_file:
                    current_file.close()
                
                filename = os.path.join(output_dir, f"posts_part_{current_file_num:03d}.txt")
                current_file = open(filename, 'w', encoding='utf-8')
                
                # Header cho file chunk
                current_file.write(f"FACEBOOK POSTS - PART {current_file_num}\n")
                current_file.write("=" * 50 + "\n")
                current_file.write(f"Fanpage ID: {fanpage_id}\n")
                current_file.write("=" * 50 + "\n\n")
            
            # Xử lý bài viết
            post_id = post.get('post_id', f'post_{idx}')
            creation_time = post.get('creation_time')
            url = post.get('url', '')
            
            actors = post.get('actors', [])
            author_name = actors[0].get('name', 'Unknown') if actors else "Unknown"
            
            clean_content = clean_text(text_content)
            formatted_time = convert_timestamp(creation_time) if creation_time else "Unknown"
            
            posts_with_content += 1
            posts_in_current_file += 1
            
            # Ghi nội dung
            current_file.write(f"BÀI VIẾT #{posts_with_content}\n")
            current_file.write("-" * 30 + "\n")
            current_file.write(f"Post ID: {post_id}\n")
            current_file.write(f"Tác giả: {author_name}\n")
            current_file.write(f"Thời gian: {formatted_time}\n")
            current_file.write("-" * 30 + "\n")
            current_file.write(f"{clean_content}\n")
            current_file.write("\n" + "-" * 50 + "\n\n")
            
            # Kiểm tra xem có cần chuyển sang file mới không
            if posts_in_current_file >= posts_per_file:
                current_file.close()
                print(f"✅ Đã hoàn thành file part {current_file_num} với {posts_in_current_file} bài viết")
                current_file_num += 1
                posts_in_current_file = 0
                current_file = None
            
        except Exception as e:
            print(f"⚠️  Lỗi khi xử lý bài viết #{idx}: {e}")
            continue
    
    # Đóng file cuối cùng
    if current_file:
        current_file.close()
        print(f"✅ Đã hoàn thành file part {current_file_num} với {posts_in_current_file} bài viết")
    
    print(f"🎉 Hoàn thành toàn bộ!")
    print(f"📊 Tổng kết:")
    print(f"   - Số bài viết có nội dung: {posts_with_content}")
    print(f"   - Số file được tạo: {current_file_num}")
    print(f"   - Thư mục đầu ra: {output_dir}")

def main():
    parser = argparse.ArgumentParser(description='Trích xuất nội dung bài viết từ Facebook JSON')
    parser.add_argument('--input', '-i', default='Content-fb-TuanLe.json',
                       help='Đường dẫn file JSON input (default: Content-fb-TuanLe.json)')
    parser.add_argument('--output', '-o', default='extracted_posts',
                       help='Thư mục output (default: extracted_posts)')
    parser.add_argument('--mode', '-m', choices=['single', 'chunks'], default='single',
                       help='Chế độ: single (1 file) hoặc chunks (nhiều file)')
    parser.add_argument('--posts-per-file', '-p', type=int, default=100,
                       help='Số bài viết mỗi file khi dùng mode chunks (default: 100)')
    
    args = parser.parse_args()
    
    # Kiểm tra file input
    if not os.path.exists(args.input):
        print(f"❌ File không tồn tại: {args.input}")
        sys.exit(1)
    
    print("🚀 BẮT ĐẦU TRÍCH XUẤT NỘI DUNG FACEBOOK POSTS")
    print("-" * 60)
    
    if args.mode == 'single':
        extract_posts_content(args.input, args.output)
    else:
        extract_posts_by_chunks(args.input, args.output, args.posts_per_file)
    
    print("-" * 60)
    print("🎉 HOÀN THÀNH!")

if __name__ == "__main__":
    main()
