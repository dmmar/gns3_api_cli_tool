#!/usr/bin/env python
import requests
from prettytable import PrettyTable
import time
import argparse


def gns3_create_new_project():

    t_show_projects = gns3_show_projects()
    print(t_show_projects)

    print('To create a new GNS3 project, please type a project name, for example: lab7')
    project_name = input('GNS3 project name: ')

    payload_create_project = '{"name": "' + str(project_name) + '"}'

    create_project = requests.post(gns3_server + '/v2/projects', data=payload_create_project)

    if create_project:
        create_project_dict = create_project.json()
        new_project_id = create_project_dict['project_id']
        print('#' * 100)
        print('Project', '[' + project_name + ']', 'is created. Project ID:', new_project_id)
        print('#' * 100)
        return new_project_id
    else:
        print('Project', '[' + project_name + ']', 'is not created because something went wrong.')
        print('Maybe that project is already existed or project name is empty.')
        return


def gns3_show_projects():

    show_projects = requests.get(gns3_server + '/v2/projects')

    if show_projects:
        show_projects_dict = show_projects.json()
        projects_count = 0
        t_projects = PrettyTable(['Number', 'Name', 'Project ID', 'Project status'])

        for dictionary in show_projects_dict:
            projects_count += 1
            project_name = dictionary['name']
            project_id = dictionary['project_id']
            project_status = dictionary['status']
            t_projects.add_row([projects_count, project_name, project_id, project_status])
        return t_projects
    else:
        print(show_projects)
        print('Can not show GNS3 projects because something went wrong.')
        exit()


def gns3_select_project():

    show_projects = requests.get(gns3_server + '/v2/projects')
    show_projects_dict = show_projects.json()

    projects_count = 0
    t_projects = PrettyTable(['Number', 'Name', 'Project ID', 'Project status'])

    for project in show_projects_dict:
        projects_count += 1
        project_name = project['name']
        project_id = project['project_id']
        project_status = project['status']
        t_projects.add_row([projects_count, project_name, project_id, project_status])
    print(t_projects)
    input_prj_name = input('Please, write GNS3 project name: ')
    for prj_name in show_projects_dict:
        if input_prj_name == prj_name['name']:
            project_status = prj_name['status']
            if project_status == 'opened':
                prj_id = prj_name['project_id']
                print('#' * 100)
                print('Project', '[' + input_prj_name + ']', 'is chosen. Project ID:', prj_id)
                print('#' * 100)
                return prj_id
            else:
                print('Can not choose a GNS3 project', '[' + input_prj_name + ']', 'because something went wrong.')
                print('Maybe project is closed, please look at "Project status". If so, you need to open it.')
                exit()
    print('[' + input_prj_name + ']', 'does not exist in the GNS3. Please, try again.')
    main()


def gns3_show_links(project_id):

    r_get_nodes = requests.get(gns3_server + '/v2/projects/' + str(project_id) + '/nodes')
    r_get_nodes_dict = r_get_nodes.json()

    r_get_links = requests.get(gns3_server + '/v2/projects/' + str(project_id) + '/links')
    r_get_links_dict = r_get_links.json()

    number_links = 0

    print('Existing links are:')

    for dictionary in r_get_links_dict:

        link_id = dictionary['link_id']
        link_type = dictionary['link_type']

        loop = dictionary['nodes']
        number_links += 1
        print('#' * 100)

        for index, item in enumerate(loop):
            for node in r_get_nodes_dict:
                device_id = node['node_id']
                a = item
                node_id = a['node_id']
                if node_id == device_id:
                    name = node['name']
                    for key, value in a.items():
                        if key == 'adapter_number':
                            print(number_links, '|', name, '|', key, value, '|', 'Link-ID:', link_id, '|',
                                  'Link-type:', link_type)


def gns3_create_links(project_id):

    gns3_show_available_nodes(project_id)
    print()
    gns3_show_links(project_id)
    print()
    print('A table contains examples of adapter numbers and its interface names for specific appliances:')
    t_adapter_numbers = PrettyTable(['number', 'IOSvL2 Int.', 'IOSv Int.', 'vASA Int.'])
    t_adapter_numbers.add_row(['[0]', 'Gi0/0', 'Gi0/0', 'Mgmt0/0'])
    t_adapter_numbers.add_row(['[1]', 'Gi0/1', 'Gi0/1', 'Gi0/0'])
    t_adapter_numbers.add_row(['[2]', 'Gi0/2', 'Gi0/2', 'Gi0/1'])
    t_adapter_numbers.add_row(['[3]', 'Gi0/3', 'Gi0/3', 'Gi0/2'])
    t_adapter_numbers.add_row(['[4]', 'Gi1/0', '-', 'Gi0/3'])
    t_adapter_numbers.add_row(['[5]', 'Gi1/1', '-', 'Gi0/4'])
    t_adapter_numbers.add_row(['[6]', 'Gi1/2', '-', 'Gi0/5'])
    t_adapter_numbers.add_row(['[7]', 'Gi1/3', '-', 'Gi0/6'])
    t_adapter_numbers.add_row(['[8]', 'Gi2/0', '-', '-'])
    t_adapter_numbers.add_row(['[9]', 'Gi2/1', '-', '-'])
    t_adapter_numbers.add_row(['[10]', 'Gi2/2', '-', '-'])
    t_adapter_numbers.add_row(['[11]', 'Gi2/3', '-', '-'])
    t_adapter_numbers.add_row(['[12]', 'Gi3/0', '-', '-'])
    t_adapter_numbers.add_row(['[13]', 'Gi3/1', '-', '-'])
    t_adapter_numbers.add_row(['[14]', 'Gi3/2', '-', '-'])
    t_adapter_numbers.add_row(['[15]', 'Gi3/3', '-', '-'])
    print(t_adapter_numbers)

    print('To create a link pair between two devices, use the following, for example: R1 0 vSW3 4')
    try:
        node1, node1_link, node2, node2_link = input('Node1_Name, Node1_Link, Node2_Name, Node2_Link: ').split()
        print()
    except Exception as e:
        print(e)
        print('that is not working, please try again.')
        return
    else:
        r_get_nodes = requests.get(gns3_server + '/v2/projects/' + str(project_id) + '/nodes')
        r_get_nodes_dict = r_get_nodes.json()

        adapter_number_1 = node1_link
        adapter_number_2 = node2_link

        for dictionary_node1 in r_get_nodes_dict:
            node1_name = dictionary_node1['name']
            if node1 == node1_name:
                print(node1, 'that device is existed in GNS3 project.')
                node1 = dictionary_node1['node_id']
                break

        for dictionary_node2 in r_get_nodes_dict:
            node2_name = dictionary_node2['name']
            if node2 == node2_name:
                print(node2_name, 'that device is existed in GNS3 project.')
                node2 = dictionary_node2['node_id']
                break

        node_id_1 = '"' + node1 + '"'
        node_id_2 = '"' + node2 + '"'

        payload_create_link_pair = '{"nodes": [{"adapter_number": ' + str(adapter_number_1) + ', "node_id": '\
                                   + str(node_id_1) + ', "port_number": 0}, {"adapter_number": ' + str(adapter_number_2)\
                                   + ', "node_id": ' + str(node_id_2) + ', "port_number": 0}]}'

        r_create_link_pair = requests.post(gns3_server + '/v2/projects/' + project_id + '/links',
                                           data=payload_create_link_pair)

        if r_create_link_pair:
            r_create_link_pair_dict = r_create_link_pair.json()
            print()
            print('#' * 50)
            print('New Link-ID:', r_create_link_pair_dict['link_id'])
            print('#' * 50)
            print()
            ask1 = input('Do you want to create one more? [y/n] : ')
            if ask1 == 'n':
                return
            elif ask1 == 'y':
                gns3_create_links(project_id)
        else:
            print(r_create_link_pair)
            print('that is not working, please try again.')
            ask2 = input('Do you want to try again? [y/n] : ')
            if ask2 == 'n':
                return
            elif ask2 == 'y':
                gns3_create_links(project_id)


def gns3_start_nodes(project_id):

    r_get_nodes = requests.get(gns3_server + '/v2/projects/' + str(project_id) + '/nodes')
    r_get_nodes_dict = r_get_nodes.json()

    for dictionary_node in r_get_nodes_dict:
        if dictionary_node['status'] == 'stopped':
            # For Juniper vSRX, starting time 10 min (600 sec).
            if dictionary_node['port_name_format'] == 'ge-0/0/{0}':
                print('#' * 100)
                print(dictionary_node['name'], 'is starting', ', node-id:', dictionary_node['node_id'])
                node_id = dictionary_node['node_id']
                url_start_node = gns3_server + '/v2/projects/' + str(project_id) + '/nodes/' + node_id + '/start'
                requests.post(url=url_start_node)
                print(time.ctime())
                time.sleep(600)
                print(dictionary_node['name'], 'is loaded', time.ctime())
                print('#' * 100)
            # For other GNS3 appliances, starting time 1 min.
            else:
                print('#' * 100)
                print(dictionary_node['name'], 'is starting', ', node-id:', dictionary_node['node_id'])
                node_id = dictionary_node['node_id']
                url_start_node = gns3_server + '/v2/projects/' + str(project_id) + '/nodes/' + node_id + '/start'
                requests.post(url=url_start_node)
                print(time.ctime())
                time.sleep(60)
                print(dictionary_node['name'], 'is loaded', time.ctime())
                print('#' * 100)
        else:
            print(dictionary_node['name'], 'is working,', 'console port:',
                  dictionary_node['console'], ', node-id:', dictionary_node['node_id'])


def gns3_show_available_nodes(project_id):

    r_get_nodes = requests.get(gns3_server + '/v2/projects/' + str(project_id) + '/nodes')
    r_get_nodes_dict = r_get_nodes.json()
    count_nodes = 0
    table_available_nodes = PrettyTable(['Number', 'Name', 'Node ID', 'Status', 'Console Port'])
    print()
    print('Available nodes are:')
    print('#' * 100)
    for dictionary in r_get_nodes_dict:
        avaiable_node_name = dictionary['name']
        avaiable_node_id = dictionary['node_id']
        avaiable_node_status = dictionary['status']
        avaiable_node_console = dictionary['console']
        count_nodes += 1
        table_available_nodes.add_row([count_nodes, avaiable_node_name,
                                       avaiable_node_id, avaiable_node_status, avaiable_node_console])
    print(table_available_nodes)


def gns3_delete_node(project_id):

    gns3_show_available_nodes(project_id)

    print('#' * 100)
    print('To delete a specific node, please write a node name.')
    print('For example: vSW4')
    print('#' * 100)

    ask_node_name_to_del = input('Node Name: ')
    node_name_to_del = ask_node_name_to_del

    r_get_nodes = requests.get(gns3_server + '/v2/projects/' + str(project_id) + '/nodes')
    r_get_nodes_dict = r_get_nodes.json()

    for dictionary_node in r_get_nodes_dict:
        node_name_to_del = dictionary_node['name']
        if ask_node_name_to_del == node_name_to_del:
            print(ask_node_name_to_del, 'that device is existed in GNS3 project.')
            ask_node_name_to_del = dictionary_node['node_id']
            break

    r_get_deleted_node_id = requests.get(gns3_server + '/v2/projects/' + str(project_id) + '/nodes/'
                                         + str(ask_node_name_to_del))

    if r_get_deleted_node_id:

        requests.delete(gns3_server + '/v2/projects/' + project_id + '/nodes/' + str(ask_node_name_to_del))
        print()
        print(node_name_to_del, 'is deleted.')
        print()
        ask = input('Do you want to delete one more? [y/n] : ')
        if ask == 'y':
            gns3_delete_node(project_id)
        elif ask == 'n':
            return
    else:
        print(r_get_deleted_node_id)
        print('that is not working, please try again.')
        return


def gns3_delete_a_link_pair(project_id):

    gns3_show_links(project_id)

    print('#' * 100)
    print('To delete a specific link pair, please copy and paste a link ID from the table.')
    print('For example: 9d8e7cf2-12c8-436c-9d76-901baf562589')
    print('#' * 100)

    ask_link_id_to_del = input('A link pair ID to delete: ')

    r_check_link_pair_id = requests.get(gns3_server + '/v2/projects/' + str(project_id) + '/links/'
                                        + str(ask_link_id_to_del))

    if r_check_link_pair_id:

        requests.delete(gns3_server + '/v2/projects/' + project_id + '/links/' + str(ask_link_id_to_del))
        print(ask_link_id_to_del, 'is deleted.')

        ask = input('Do you want to delete one more? [y/n] : ')
        if ask == 'y':
            gns3_delete_a_link_pair(project_id)
        elif ask == 'n':
            return
    else:
        print(r_check_link_pair_id)
        print('that is not working, please try again.')
        return


def gns3_get_appliances_names_and_id():

    gns3_appliances_dict = {}

    show_appliances = requests.get(gns3_server + '/v2/appliances')

    if show_appliances:
        show_appliances_dict = show_appliances.json()
        for appliance in show_appliances_dict:

            gns3_get_appliance_name = appliance['name']
            gns3_get_appliance_id = appliance['appliance_id']

            gns3_show_appliances = gns3_get_appliance_name, gns3_get_appliance_id

            gns3_appliance_name = gns3_show_appliances[0]
            gns3_appliance_id = gns3_show_appliances[1]

            gns3_appliances_dict.update({gns3_appliance_name: gns3_appliance_id})
    return gns3_appliances_dict


def gns3_create_node(project_id):

    gns3_show_available_nodes(project_id)

    gns3_appliances = gns3_get_appliances_names_and_id()
    t_available_appliances = PrettyTable(['Appliance Name', 'ID'])

    for key, value in gns3_appliances.items():
        t_available_appliances.add_row([key, value])

    print('Available appliances are:')
    print('#' * 100)
    print(t_available_appliances)
    print('To create a new node, please use the following, for example: ')
    print()
    print('Appliance Name: Cisco IOSv 15.6(2)T')
    print('Node Name: vR1')
    print()

    gns3_input_appliance = input('Appliance Name: ')
    gns3_input_appliance_name = input('Node Name: ')

    payload_coordinates = '{"x": 0, "y": 0}'
    payload_node_name = '{"name": "' + gns3_input_appliance_name + '"}'

    for key, value in gns3_appliances.items():
        if gns3_input_appliance == key:
            # Built in GNS3
            if gns3_input_appliance == 'Cloud':
                cloud_payload = '{"name": "' + gns3_input_appliance_name + \
                                '", "node_type": "cloud", "compute_id": "local"}'
                cloud_r = requests.post(gns3_server + '/v2/projects/' + project_id + '/nodes', data=cloud_payload)
                if cloud_r:
                    cloud_r_dict = cloud_r.json()
                    cloud_new_id = cloud_r_dict['node_id']
                    print()
                    print(gns3_input_appliance_name, 'is created.', cloud_new_id)
                    print()
                    ask = input('Do you want to create one more? [y/n] : ')
                    if ask == 'n':
                        return
                    elif ask == 'y':
                        gns3_create_node(project_id)
                else:
                    print(cloud_r)
                    print('that is not working, please try again.')
                    return
            elif gns3_input_appliance == 'VPCS':
                vpcs_payload = '{"name": "' + gns3_input_appliance_name + \
                               '", "node_type": "vpcs", "compute_id": "local"}'
                vpcs_r = requests.post(gns3_server + '/v2/projects/' + project_id + '/nodes', data=vpcs_payload)
                if vpcs_r:
                    vpcs_r_dict = vpcs_r.json()
                    vpcs_new_id = vpcs_r_dict['node_id']
                    print()
                    print(gns3_input_appliance_name, 'is created.', vpcs_new_id)
                    print()
                    ask = input('Do you want to create one more? [y/n] : ')
                    if ask == 'n':
                        return
                    elif ask == 'y':
                        gns3_create_node(project_id)
                else:
                    print(vpcs_r)
                    print('that is not working, please try again.')
                    return
            elif gns3_input_appliance == 'NAT':
                nat_payload = '{"name": "' + gns3_input_appliance_name + \
                               '", "node_type": "nat", "compute_id": "local"}'
                nat_r = requests.post(gns3_server + '/v2/projects/' + project_id + '/nodes', data=nat_payload)
                if nat_r:
                    nat_r_dict = nat_r.json()
                    nat_new_id = nat_r_dict['node_id']
                    print()
                    print(gns3_input_appliance_name, 'is created.', nat_new_id)
                    print()
                    ask = input('Do you want to create one more? [y/n] : ')
                    if ask == 'n':
                        return
                    elif ask == 'y':
                        gns3_create_node(project_id)
                else:
                    print(nat_r)
                    print('that is not working, please try again.')
                    return
            elif gns3_input_appliance == 'Frame Relay switch':
                fr_sw_payload = '{"name": "' + gns3_input_appliance_name + \
                               '", "node_type": "frame_relay_switch", "compute_id": "local"}'
                fr_sw_r = requests.post(gns3_server + '/v2/projects/' + project_id + '/nodes', data=fr_sw_payload)
                if fr_sw_r:
                    fr_sw_r_dict = fr_sw_r.json()
                    fr_sw_new_id = fr_sw_r_dict['node_id']
                    print()
                    print(gns3_input_appliance_name, 'is created.', fr_sw_new_id)
                    print()
                    ask = input('Do you want to create one more? [y/n] : ')
                    if ask == 'n':
                        return
                    elif ask == 'y':
                        gns3_create_node(project_id)
                else:
                    print(fr_sw_r)
                    print('that is not working, please try again.')
                    return
            elif gns3_input_appliance == 'Ethernet hub':
                eth_hub_payload = '{"name": "' + gns3_input_appliance_name + \
                               '", "node_type": "ethernet_hub", "compute_id": "local"}'
                eth_hub_r = requests.post(gns3_server + '/v2/projects/' + project_id + '/nodes', data=eth_hub_payload)
                if eth_hub_r:
                    eth_hub_r_dict = eth_hub_r.json()
                    eth_hub_new_id = eth_hub_r_dict['node_id']
                    print()
                    print(gns3_input_appliance_name, 'is created.', eth_hub_new_id)
                    print()
                    ask = input('Do you want to create one more? [y/n] : ')
                    if ask == 'n':
                        return
                    elif ask == 'y':
                        gns3_create_node(project_id)
                else:
                    print(eth_hub_r)
                    print('that is not working, please try again.')
                    return
            elif gns3_input_appliance == 'Ethernet switch':
                eth_sw_payload = '{"name": "' + gns3_input_appliance_name + \
                               '", "node_type": "ethernet_switch", "compute_id": "local"}'
                eth_sw_r = requests.post(gns3_server + '/v2/projects/' + project_id + '/nodes', data=eth_sw_payload)
                if eth_sw_r:
                    eth_sw_r_dict = eth_sw_r.json()
                    eth_sw_new_id = eth_sw_r_dict['node_id']
                    print()
                    print(gns3_input_appliance_name, 'is created.', eth_sw_new_id)
                    print()
                    ask = input('Do you want to create one more? [y/n] : ')
                    if ask == 'n':
                        return
                    elif ask == 'y':
                        gns3_create_node(project_id)
                else:
                    print(eth_sw_r)
                    print('that is not working, please try again.')
                    return
            # Added manually
            else:
                appliance_id = value
                r_create_node = requests.post(gns3_server + '/v2/projects/' + project_id + '/appliances/'
                                              + appliance_id, data=payload_coordinates)
                if r_create_node:
                    r_create_node_dict = r_create_node.json()
                    new_node_id = r_create_node_dict['node_id']
                    requests.put(gns3_server + '/v2/projects/' + project_id + '/nodes/' + new_node_id,
                                 data=payload_node_name)
                    print()
                    print(gns3_input_appliance_name, 'is created.', new_node_id)
                    print()
                    ask = input('Do you want to create one more? [y/n] : ')
                    if ask == 'n':
                        return
                    elif ask == 'y':
                        gns3_create_node(project_id)
                else:
                    print(r_create_node)
                    print('that is not working, please try again.')
                    return


def gns3_delete_project():

    t_show_projects = gns3_show_projects()
    print(t_show_projects)

    print('#' * 100)
    print('To delete a specific project, please write a project name.')
    print('For example: test1')
    print('#' * 100)

    ask_project_name_to_del = input('Project Name: ')
    if ask_project_name_to_del:
        project_name_to_del = ask_project_name_to_del

        r_get_projects = requests.get(gns3_server + '/v2/projects')
        r_get_projects_dict = r_get_projects.json()

        for dictionary_project in r_get_projects_dict:
            project_name_to_del = dictionary_project['name']
            if ask_project_name_to_del == project_name_to_del:
                print(ask_project_name_to_del, 'that project is existed in GNS3.')
                ask_project_name_to_del = dictionary_project['project_id']
                break
        r_to_delete_project = requests.delete(gns3_server + '/v2/projects/' + ask_project_name_to_del)
        if r_to_delete_project:
            print()
            print(project_name_to_del, 'is deleted.', ask_project_name_to_del)
            print()
            ask = input('Do you want to delete one more? [y/n] : ')
            if ask == 'y':
                gns3_delete_project()
            elif ask == 'n':
                return
        else:
            print(r_to_delete_project)
            print('The project does not exist.')
            return
    else:
        print('Project name is empty. Please, try again.')
        return


def gns3_show_available_appliances(gns3_server):
    gns3_appliances_dict = {}
    show_appliances = requests.get(gns3_server + '/v2/appliances')
    if show_appliances:
        show_appliances_dict = show_appliances.json()
        for appliance in show_appliances_dict:
            gns3_get_appliance_name = appliance['name']
            gns3_get_appliance_id = appliance['appliance_id']
            gns3_show_appliances = gns3_get_appliance_name, gns3_get_appliance_id
            gns3_appliance_name = gns3_show_appliances[0]
            gns3_appliance_id = gns3_show_appliances[1]
            gns3_appliances_dict.update({gns3_appliance_name: gns3_appliance_id})
        gns3_appliances = gns3_appliances_dict
        t_available_appliances = PrettyTable(['Appliance Name', 'ID'])
        for key, value in gns3_appliances.items():
            t_available_appliances.add_row([key, value])
        return t_available_appliances
    else:
        print(show_appliances)
        print('that is not working.')
        exit()


parser = argparse.ArgumentParser()
parser.add_argument('-s', action='store', dest='gns3_server', required=True,
                    help='GNS3 server, for example: http://172.16.1.1:3080')
args = parser.parse_args()
gns3_server = args.gns3_server


def main():
    def print_gns3_menu():
        print("""
##############################
#      CREATE MANUALLY       #
#      A GNS3 TOPOLOGY       #
#       STEP BY STEP         #
##############################
        """)
        print('[Menu]', 'Current GNS3 server is', gns3_server)
        print('#' * 50)
        print("1. To create a new project.")
        print("2. To create a new node.")
        print("3. To create a new link pair.")
        print("4. To start all stopped nodes.")
        print("#" * 50)
        print("5. To delete a node.")
        print("6. To delete a link pair.")
        print("7. To delete a project.")
        print('#' * 50)
        print("8. To show nodes in the project.")
        print("9. To show link pairs in the project.")
        print("10. To show GNS3 projects.")
        print("11. To show GNS3 available appliances.")
        print('#' * 50)
    while True:
        print_gns3_menu()
        print('If you would like to finish, type "exit".')
        choice = input("Enter your choice [1-11]: ")
        if choice == '1':
            gns3_create_new_project()
        elif choice == '2':
            project_id = gns3_select_project()
            gns3_create_node(project_id)
        elif choice == '3':
            project_id = gns3_select_project()
            gns3_create_links(project_id)
        elif choice == '4':
            project_id = gns3_select_project()
            gns3_start_nodes(project_id)
        elif choice == '5':
            project_id = gns3_select_project()
            gns3_delete_node(project_id)
        elif choice == '6':
            project_id = gns3_select_project()
            gns3_delete_a_link_pair(project_id)
        elif choice == '7':
            gns3_delete_project()
        elif choice == '8':
            project_id = gns3_select_project()
            gns3_show_available_nodes(project_id)
        elif choice == '9':
            project_id = gns3_select_project()
            gns3_show_links(project_id)
        elif choice == '10':
            t_show_projects = gns3_show_projects()
            print(t_show_projects)
        elif choice == '11':
            t_show_gns3_appliances = gns3_show_available_appliances(gns3_server)
            print(t_show_gns3_appliances)
        elif choice == 'exit':
            exit()
        else:
            input("Wrong menu selection. Enter any key to try again..")


if __name__ == '__main__':
    main()

