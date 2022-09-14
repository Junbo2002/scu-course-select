# -*- coding: UTF-8 -*-

from func import *
import requests


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def head_print():
    print(
        """        
     __            ___.                                            
    |__|__ __  ____\_ |__   ____   __  _  _______    ____    ____  
    |  |  |  \/    \| __ \ /  _ \  \ \/ \/ /\__  \  /    \  / ___\ 
    |  |  |  /   |  \ \_\ (  <_> )  \     /  / __ \|   |  \/ /_/  >
/\__|  |____/|___|  /___  /\____/    \/\_/  (____  /___|  /\___  / 
\______|          \/    \/                       \/     \//_____/  

        """
    )
    print(f"{bcolors.HEADER} SCU 抢课脚本: 使用该软件造成的后果与作者无关 {bcolors.ENDC}")

    print(f"{bcolors.HEADER} 项目github地址: https://github.com/Junbo-Jabari/scu-course-select {bcolors.ENDC}")


session = requests.session()
if __name__ == '__main__':
    head_print()
    main(session)
    input('\nPress <Enter>')

