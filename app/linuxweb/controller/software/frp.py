from app.linuxweb.common import *
dar=config.path['linux_install_path']+"frp/frp0.30"
# pkill frps && cd /usr/local/frp/frp0.30 && ./frps -c frps_full.ini &
def get_server():
    server={
        'conf':file_get_content(dar+"/frps_full.ini"),
        'base':json_decode(file_get_content(dar+"/frps_full.conf"))
    }
    return returnjson(server)
def run_status():
    "获取运行状态"
    data={"frpc":0,"frps":0}
    if get_process_id('frps'):
        data['frps']=1
    if get_process_id('frpc'):
        data['frpc']=1
    return returnjson(data)
def restart(types='frps'):
    "重启"
    if types=='frps':
        os.system("pkill frps")
        time.sleep(1)
        os.system("cd "+dar +" && ./frps -c frps_full.ini &")
        time.sleep(1)
        if not get_process_id('frps'):
            return returnjson(code=1,msg="启动失败，请检查配置")
    elif types=='frpc':
        os.system("pkill frpc")
        time.sleep(1)
        os.system("cd "+dar +" && ./frpc -c frpc.ini &")
        time.sleep(1)
        if not get_process_id('frpc'):
            return returnjson(code=1,msg="启动失败，请检查配置")
    return returnjson()
def stop(types='frps'):
    "停止"
    if types=='frps':
        os.system("pkill frps")
    elif types=='frpc':
        os.system("pkill frpc")
    return returnjson()
def upd_server(types='ini'):
    server=request.get_json()
    if types=='ini':
        file_set_content(dar+"/frps_full.ini",server['conf'])
    elif types=='base':
        base=server['base']
        f = open(dar+"/frps_full.ini")
        con=''
        while True:
            line = f.readline()
            if not line:
                break
            elif 'bind_addr = ' in line:
                line="bind_addr = "+base['bind_addr']+"\n"
            elif 'bind_port = ' in line:
                line="bind_port = "+base['bind_port']+"\n"
            elif 'bind_udp_port = ' in line:
                line="bind_udp_port = "+base['bind_udp_port']+"\n"
            elif 'kcp_bind_port = ' in line:
                line="kcp_bind_port = "+base['kcp_bind_port']+"\n"
            elif 'vhost_http_port = ' in line:
                line="vhost_http_port = "+base['vhost_http_port']+"\n"
            elif 'vhost_https_port = ' in line:
                line="vhost_https_port = "+base['vhost_https_port']+"\n"
            elif 'dashboard_addr = ' in line:
                line="dashboard_addr = "+base['dashboard_addr']+"\n"
            elif 'dashboard_port = ' in line:
                line="dashboard_port = "+base['dashboard_port']+"\n"
            elif 'dashboard_user = ' in line:
                line="dashboard_user = "+base['dashboard_user']+"\n"
            elif 'dashboard_pwd = ' in line:
                line="dashboard_pwd = "+base['dashboard_pwd']+"\n"
            elif 'log_level = ' in line:
                line="log_level = "+base['log_level']+"\n"
            elif 'log_max_days = ' in line:
                line="log_max_days = "+base['log_max_days']+"\n"
            elif 'disable_log_color = ' in line:
                line="disable_log_color = "+base['disable_log_color']+"\n"
            elif 'token = ' in line:
                line="token = "+base['token']+"\n"
            elif 'allow_ports = ' in line:
                line="allow_ports = "+base['allow_ports']+"\n"
            elif 'max_pool_count = ' in line:
                line="max_pool_count = "+base['max_pool_count']+"\n"
            elif 'max_ports_per_client = ' in line:
                line="max_ports_per_client = "+base['max_ports_per_client']+"\n"
            elif 'subdomain_host = ' in line:
                line="subdomain_host = "+base['subdomain_host']+"\n"
            elif 'tcp_mux = ' in line:
                line="tcp_mux = "+base['tcp_mux']+"\n"
            con=con+line
        f.close()
        file_set_content(dar+"/frps_full.ini",con)
        file_set_content(dar+"/frps_full.conf",json_encode(base))
    os.system("pkill frps")
    time.sleep(1)
    os.system("cd "+dar +" && ./frps -c frps_full.ini &")
    time.sleep(1)
    if not get_process_id('frps'):
        return returnjson(code=1,msg="启动失败，请检查配置")
    return returnjson()
def get_client():
    client={
        'conf':file_get_content(dar+"/frpc.ini"),
        'base':json_decode(file_get_content(dar+"/frpc.conf"))
    }
    return returnjson(client)
def upd_client(type='ini'):
    server=request.get_json()
    file_set_content(dar+"/frpc.ini",server['conf'])
    os.system("pkill frpc")
    time.sleep(1)
    os.system("cd "+dar +" && ./frpc -c frpc.ini &")
    time.sleep(1)
    if not get_process_id('frpc'):
        return returnjson(code=1,msg="启动失败，请检查配置")
    return returnjson()