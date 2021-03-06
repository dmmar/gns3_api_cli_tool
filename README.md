# gns3_api_cli_tool

## Overview

   This repository contains a simple python3 script to communicate with GNS3 server via API. 
   
   For example, to create/delete/start nodes etc.
   
   This script is useful because you do not need to open GNS3 GUI to communicate with server.
   
   **Tested on GNS3 2.1.21. and 2.2.7 **
   
   *The script does not support GNS3 server authentication login/pass for now.*
   
   P.S. Author is not an expert, he is learning how to code. Errors can exist.
   
   **Screenshots:**
   
   ![main_menu_new](https://github.com/dmmar/gns3_api_cli_tool/blob/master/Screenshots/main_menu_new.png "main_menu_new.png")
   
   **Sample video:**
   (https://youtu.be/z2oXdC4Lfl0)

## Prerequisites

    * python3
    * pip3

## Getting Started

    # git clone https://github.com/dmmar/gns3_api_cli_tool.git
    # pip3 install -r requirements.txt
    
## Running the script 

    [GNS3 2.1.21]
    # python3 gns3_api_cli_tool_v1.py -s http://127.0.0.1:3080
    
    [GNS3 2.2.7]
    # python3 gns3_api_cli_tool_v1_1.py -s http://127.0.0.1:3080
    
## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/dmmar/gns3_api_cli_tool/blob/master/LICENSE.md) file for details.
