import os
import time
import requests
from threading import Thread, Lock
from queue import Queue
import argparse

start_time = time.time() # Start measuring execution time

v = Queue()
list_lock = Lock()
discovered_domains = []

def scan_subdomains(domain):
    print(args.delay)
    time.sleep(args.delay)
    global v
    while True:
        # time.sleep(args.delay)
        subdomain = v.get() # get the subdomain from the queue
        url = f"http://{subdomain}.{domain}" # scan the subdomain
        try:
            requests.get(url)
        except requests.ConnectionError:
            pass
        else:
            print("[+] Discovered subdomain:", url) # add the subdomain to the global list
            with list_lock:
                discovered_domains.append(url) # time.sleep(args.delay)
                

        v.task_done()  # done with scanning that subdomain


def main(domain, n_threads, subdomains):
    global v

    for subdomain in subdomains: # fill the queue with all the subdomains
        v.put(subdomain)

    for t in range(n_threads):
        worker = Thread(target=scan_subdomains, args=(domain,)) # start all threads 
        worker.daemon = True # daemon thread means a thread that will end when the main thread ends
        worker.start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Subdomain Scanner")
    parser.add_argument("domain", help="Domain to scan for subdomains without (e.g without 'http://' or 'https://')")
    parser.add_argument("-w", "--wordlist", help="File that contains all subdomains to scan, line by line.",
                       )
    parser.add_argument("-t", "--num-threads", help="Number of threads to use to scan the domain. Default is 10", default=10, type=int)
    parser.add_argument("-o", "--output-file", help="Specify the output text file name to write discovered subdomains")
    parser.add_argument("-d", "--delay", type=int, default=0, help='Delay in seconds between requests (default: 0)')

    args = parser.parse_args()
    domain = args.domain
    wordlist = args.wordlist
    num_threads = args.num_threads
    output_file = args.output_file
    delay = args.delay

    main(domain=domain, n_threads=num_threads, subdomains=open(wordlist).read().splitlines())
    v.join()

    with open(output_file, "w") as f: # save the file
        for url in discovered_domains:
            print(url, file=f)

output_file_path = os.path.abspath(output_file) # Get the absolute path of the output file
print(f"Results saved in {output_file_path}") # Print the location of the output file

end_time = time.time() # End measuring execution time
elapsed_time = end_time - start_time
print(f"Execution time: {elapsed_time:.2f} seconds") # Print the execution time