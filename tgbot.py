import re
import datetime
import random
import time

def parse_suricata_rules(input_file, output_file):
    current_time = datetime.datetime.now().strftime('%m/%d/%Y-%H:%M:%S.%f')[:-3]
    with open(input_file, 'r') as f_in:
        rules = f_in.readlines()

    while True:
        for rule in rules:
            delay = random.uniform(0.01, 3.0)
            time.sleep(delay)

            match = re.match(r'^(\d{2}/\d{2}/\d{4}-\d{2}:\d{2}:\d{2}\.\d{6}) \[\*\*\] \[(\d+:\d+:\d+)\] (.+) \[\*\*\] \[Classification: (.+)\] \[Priority: (\d+)\] \{(\w+)\} (\d+\.\d+\.\d+\.\d+):(\d+) -> (\d+\.\d+\.\d+\.\d+):(\d+)$')
            print(match)
            if match:
                proto = match.group(1)
                ext_net = match.group(2)
                home_net = match.group(3)
                port = match.group(4)
                msg = match.group(5)
                flow = match.group(6)
                classtype = match.group(8)
                priority = match.group(9)
                
                src_ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
                
                log_entry = f"{current_time}  [**] [1:{priority}:3] {msg} [**] [Classification: Potentially Bad Traffic] [Priority: 2] {{{proto}}} {src_ip}:55442 -> 10.129.0.20:{port}\n"
                
                with open(output_file, 'a') as f_out:
                    f_out.write(log_entry)
                    print(log_entry)

parse_suricata_rules('/var/lib/suricata/rules/suricata.rules', '/var/log/suricata/fast.log')
