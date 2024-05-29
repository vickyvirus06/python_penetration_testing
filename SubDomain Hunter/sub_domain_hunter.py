import requests
import time

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
    basic_scan(domain_name.strip())
else:
    print("\nInvalid Domain name")