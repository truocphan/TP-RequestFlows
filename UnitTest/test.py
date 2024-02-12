import sys
sys.path.insert(0, "..")
import TP_RequestFlows

TP_RequestFlows.run_flows(r".\TestData\OWASP_Juice_Shop", proxy_server={"host":"127.0.0.1", "port":8080})