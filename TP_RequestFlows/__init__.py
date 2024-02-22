from TP_Requests.http import TP_HTTP_REQUEST
from TP_HTTP_Request_Response_Parser import *
import json_duplicate_keys as jdks
import glob
import os

Flows = dict()

def kwvars(environments, vars=dict()):
	vars = dict()

	for importLib in environments["libs"]:
		exec(importLib)

	for name in environments["vars"]:
		if environments["vars"][name]["runCode"]:
			try:
				vars[name] = eval(environments["vars"][name]["value"])
			except Exception as e:
				vars[name] = None
		else:
			vars[name] = environments["vars"][name]["value"]

	return vars


def run_flows(FlowFolders, injectObj=dict(), separator="||", parse_index="$", dupSign_start="{{{", dupSign_end="}}}", ordered_dict=False, update_content_length=True, proxy_server=None):

	RequestRules = jdks.load(os.path.join(FlowFolders, "rules.json"))

	for i in range(len(glob.glob1(FlowFolders, "*.req"))):
		Flows[str(i+1)] = {
			"rawRequest": open(os.path.join(FlowFolders, "raw-{}.req".format(i+1)), "rb").read().decode("utf-8"),
			"rawResponse": None
		}

	try:
		for reqNum in Flows:
			req = TP_HTTP_REQUEST(Flows[reqNum]["rawRequest"], separator=separator, parse_index=parse_index, dupSign_start=dupSign_start, dupSign_end=dupSign_end, ordered_dict=ordered_dict)

			if "PathParams" in RequestRules.get("flows")[reqNum]:
				PathParams = RequestRules.get("flows")[reqNum]["PathParams"]
				if type(PathParams) == dict:
					for name in PathParams:
						req.update_path_param(name, PathParams[name].format(**kwvars(RequestRules.get("environments"))))

			if "QueryParams" in RequestRules.get("flows")[reqNum]:
				QueryParams = RequestRules.get("flows")[reqNum]["QueryParams"]
				if type(QueryParams) == dict:
					for name in QueryParams:
						req.update_query_param(name, QueryParams[name].format(**kwvars(RequestRules.get("environments"))))

			if "HTTPHeaders" in RequestRules.get("flows")[reqNum]:
				HTTPHeaders = RequestRules.get("flows")[reqNum]["HTTPHeaders"]
				if type(HTTPHeaders) == dict:
					for name in HTTPHeaders:
						req.update_http_header(name, HTTPHeaders[name].format(**kwvars(RequestRules.get("environments"))))

			if "HTTPCookies" in RequestRules.get("flows")[reqNum]:
				HTTPCookies = RequestRules.get("flows")[reqNum]["HTTPCookies"]
				if type(HTTPCookies) == dict:
					for name in HTTPCookies:
						req.update_http_cookie(name, HTTPCookies[name].format(**kwvars(RequestRules.get("environments"))))

			if "RequestBody" in RequestRules.get("flows")[reqNum]:
				RequestBody = RequestRules.get("flows")[reqNum]["RequestBody"]
				if type(RequestBody) == dict:
					for name in RequestBody:
						try:
							datetype_ori = type(req.get_request_body_param(name))
							datatype_new = type(eval(RequestBody[name].format(**kwvars(RequestRules.get("environments")))))

							if datetype_ori == datatype_new or datetype_ori in [int, float] and datatype_new in [int, float]:
								req.update_request_body_param(name, eval(RequestBody[name].format(**kwvars(RequestRules.get("environments")))))
						except Exception as e:
							req.update_request_body_param(name, RequestBody[name].format(**kwvars(RequestRules.get("environments"))))


			injectObj_reqNum = {}
			if reqNum in injectObj and type(injectObj[reqNum]) == dict:
				injectObj_reqNum = injectObj[reqNum]


			Scheme = RequestRules.get("flows")[reqNum]["Scheme"]
			Host = RequestRules.get("flows")[reqNum]["Host"]
			Port = RequestRules.get("flows")[reqNum]["Port"]

			Flows[reqNum] = req.sendRequest(Host, Port, Scheme, injectObj=injectObj_reqNum, update_content_length=update_content_length, proxy_server=proxy_server)
	except Exception as e:
		print(e)

	return Flows