import requests
from bs4 import BeautifulSoup
import os
import argparse

def extract_links_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTP hata durumlarını kontrol et
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tüm bağlantıları bul
        links = set()
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Sadece http veya https ile başlayan bağlantıları ekle
            if href.startswith('http://') or href.startswith('https://'):
                links.add(href)
        
        return links
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return set()

def main(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Giriş dosyası {input_file} bulunamadı.")
        return

    all_links = set()
    
    # URL'leri oku
    with open(input_file, 'r') as file:
        urls = file.readlines()

    # Her URL için bağlantıları çıkar
    for url in urls:
        url = url.strip()  # Satır sonu boşluklarını temizle
        if url:
            print(f"{url} adresinden bağlantılar çıkarılıyor...")
            links = extract_links_from_url(url)
            all_links.update(links)
    
    # Çıkarılan bağlantıları yaz
    with open(output_file, 'w') as file:
        for link in all_links:
            file.write(link + '\n')

    print(f"Çıkarılan bağlantılar {output_file} dosyasına kaydedildi.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web sitesi URL'lerinden bağlantıları çıkar.")
    parser.add_argument('-f', '--file', type=str, required=True, help='Giriş dosyasının adı (örn: url.txt)')
    parser.add_argument('-o', '--output', type=str, required=True, help='Çıkış dosyasının adı (örn: output.txt)')

    args = parser.parse_args()

    main(args.file, args.output)
