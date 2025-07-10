#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script đơn giản để trích xuất chỉ nội dung text từ Facebook JSON
"""

import json
import os
from datetime import datetime

def simple_extract(input_file='Content-fb-TuanLe.json', output_file='facebook_posts_content.txt'):
    """
    Trích xuất đơn giản chỉ nội dung text của các bài viết
    """
    
    print(f"📖 Đang đọc file: {input_file}")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return
    
    posts = data.get('posts', [])
    print(f"📊 Tìm thấy {len(posts)} bài viết")
    
    content_count = 0
    
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write("NỘI DUNG CÁC BÀI VIẾT FACEBOOK\n")
        out.write("=" * 50 + "\n\n")
        
        for i, post in enumerate(posts, 1):
            message = post.get('message', {})
            if not message:
                continue
            
            text = message.get('text', '')
            if not text or text.strip() == '':
                continue
            
            content_count += 1
            
            # Lấy thời gian nếu có
            creation_time = post.get('creation_time')
            if creation_time:
                try:
                    time_str = datetime.fromtimestamp(creation_time).strftime("%Y-%m-%d %H:%M")
                except:
                    time_str = "Unknown"
            else:
                time_str = "Unknown"
            
            # Ghi nội dung
            out.write(f"[{content_count}] - {time_str}\n")
            out.write("-" * 30 + "\n")
            out.write(text.replace('\\/', '/') + "\n")
            out.write("\n" + "=" * 50 + "\n\n")
            
            if content_count % 50 == 0:
                print(f"⏳ Đã xử lý {content_count} bài viết...")
    
    print(f"✅ Hoàn thành!")
    print(f"📄 Đã trích xuất {content_count} bài viết có nội dung")
    print(f"💾 File đầu ra: {output_file}")
    print(f"📏 Kích thước: {os.path.getsize(output_file) / (1024*1024):.2f} MB")

if __name__ == "__main__":
    simple_extract()
