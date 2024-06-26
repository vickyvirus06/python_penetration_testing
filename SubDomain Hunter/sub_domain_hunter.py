import requests
import time

def deep_scan(domain_name):
    found_subdomain_list = []
    with open("subdomains.txt", "r") as subdomain_list:
        print("\nSubdomain found :  \n\n")
        pointer = 0;
        #subdomain_list.seek(0)  # Reset file pointer to the beginning for iteration
        for subdomain in subdomain_list:
            pointer = pointer +1;
            for inner_subdomain in subdomain_list:
                if subdomain != inner_subdomain:
                    print(subdomain.strip() + "." + inner_subdomain.strip() + "." + domain_name)
                    sub_domain_url = "http://" + subdomain.strip() + "." + inner_subdomain.strip() + "." + domain_name
                    try:
                        response = requests.get(sub_domain_url, timeout=5)
                        if response.status_code == 200:
                            print(subdomain.strip() + "." + inner_subdomain.strip() + "." + domain_name)
                            found_subdomain_list.append(subdomain.strip() + "." + inner_subdomain.strip() + "." + domain_name)
                    except:
                        pass
            subdomain_list.seek(pointer)
    return found_subdomain_list

def basic_scan(domain_name):
    found_subdomain_list = []
    with open("subdomains.txt", "r") as subdomain_list:
        total_subdomains = len(subdomain_list.readlines())  # Counting total lines
        print("")
        print("*" * 50)
        print("Total subdomains to be tested:", total_subdomains)
        print("*" * 50)
        print("\nSubdomain found :  \n\n")
        subdomain_list.seek(0)  # Reset file pointer to the beginning for iteration
        for subdomain in subdomain_list:
            sub_domain_url = "http://" + subdomain.strip() + "." + domain_name
            try:
                response = requests.get(sub_domain_url, timeout=5)
                if response.status_code == 200:
                    print(subdomain.strip() + "." + domain_name)
                    found_subdomain_list.append(subdomain.strip() + "." + domain_name)
            except:
                pass
        
    return found_subdomain_list               

print("-" * 100)
print("""
     ____        _     ____                        _       
\t███████╗██╗   ██╗██████╗ ██████╗  ██████╗ ███╗   ███╗ █████╗ ██╗███╗   ██╗
\t██╔════╝██║   ██║██╔══██╗██╔══██╗██╔═══██╗████╗ ████║██╔══██╗██║████╗  ██║
\t███████╗██║   ██║██████╔╝██║  ██║██║   ██║██╔████╔██║███████║██║██╔██╗ ██║
\t╚════██║██║   ██║██╔══██╗██║  ██║██║   ██║██║╚██╔╝██║██╔══██║██║██║╚██╗██║
\t███████║╚██████╔╝██████╔╝██████╔╝╚██████╔╝██║ ╚═╝ ██║██║  ██║██║██║ ╚████║
\t╚══════╝ ╚═════╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝
                                                                          
\t    ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗                   
\t    ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗                  
\t    ███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝                  
\t    ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗                  
\t    ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║                  
\t    ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝ \n""")


print("\033[1mProgram Made by vickyvirus\033[0m")
print("-" * 100)

domain_name = input("\nPlease Enter the domain name to scan: ")

if domain_name.strip() and ".com" in domain_name:
    print("\n\033[1m1) Basic Scan \033[0m")
    print("\033[1m2) Deep Scan \033[0m")
    scan_type = input("\nEnter your choice : ")
    if int(scan_type) == 1:
        found_subdomain_list = basic_scan(domain_name.strip())
    elif int(scan_type) == 2:
        found_subdomain_list = deep_scan(domain_name.strip())
else:
    print("\nInvalid Domain name")