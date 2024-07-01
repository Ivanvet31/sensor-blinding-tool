import requests

def send_trigger_requests():
    targets = ['109.71.242.119']
    ports = ['80', '443']


    payloads = [
        'JOIN ',                              # ET MALWARE Psyb0t joining an IRC Channel
        'Subject: SC-KeyLog Logs',            # ET MALWARE SC-KeyLog Keylogger Installed - Sending Initial Email Report
        'From: SC-KeyLog',                    # ET MALWARE SC-KeyLog Keylogger Installed - Sending Log Email Report
        'uv+LRCQID7dIDFEECggDSLm9df8C/zSNK',  # ET MALWARE Bugbear@MM virus via SMTP
        '54 00 42 00 4c 00 5',                # ET MALWARE Outbound AVISOSVB MSSQL Request
        'C2 E5 E5 E5 9E DD A4 A3 D4 A6 D4 D3', # ET MALWARE Arucer Command Execution
        'C2 E5 E5 E5 9E D5 D4 D2 D1 A1 D7 A3', # ET MALWARE Arucer DIR Listing
        'C2 E5 E5 E5 9E DC DD A1 DC D0 DD A', # ET MALWARE Arucer WRITE FILE command
        'C2 E5 E5 E5 9E A3 D3 A6 D1 D6 A0 D4',# ET MALWARE Arucer READ FILE Command
        'C2 E5 E5 E5 9E D2 DD D6 A0 A4 A6 A7',# ET MALWARE Arucer NOP Command
        'C2 E5 E5 E5 9E A0 A4 D2 A4 D7 A0 A7',# ET MALWARE Arucer FIND FILE Command
        'C2 E5 E5 E5 9E A0 D7 A4 A6 D0 D5 DD DC C8' # ET MALWARE Arucer YES Command
    ]

    for target in targets:
        for port in ports:
            url = f'http://{target}:{port}/'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

            for payload in payloads:
                response = requests.get(url, headers=headers, params={'key': payload})
                print(f'Status Code (GET): {response.status_code}')

if __name__ == '__main__':
    send_trigger_requests()
