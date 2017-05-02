# -*- coding: utf-8 -*-
# ===================================
# ScriptName : main.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-04-20 17:07
# ===================================
from collections import defaultdict
rule = {}
"""
存储格式为：{
    rule_id : [
        {
            'action':'permit',
            'src-zone':'trust',
            'dst-zone':'untrust',
            'src-ip':'Any'
            'dst-ip':'Any'
            'service ':['Any']
        },
        {
            'action':'permit',
            'src-zone':'trust',
            'dst-zone':'untrust',
            'src-ip':'Any'
            'dst-ip':'Any'
            'service ':['Any']
        },
    ]
}
"""

one_rule = defaultdict(lambda :'', action='NoAction', src_zone='NoSourceZone',
                               dst_zone='NoDestinationZone', src_ip='NoSourceIP', dst_ip='NoDestinationIP')
rule_id = None
def main(filename):
    with file(filename) as f:
        [parse_line(line.strip()) for line in f if all(line.strip())]
    output_format()



def parse_line(line):
    global rule_id
    global one_rule
    global rule
    if line.startswith('rule id'):
        if len(one_rule)> 4:
            if rule.has_key(rule_id):
                rule[rule_id].append(one_rule)
            else:
                rule[rule_id]= [one_rule]
        rule_id = line.split(' ')[2]
        one_rule = defaultdict(lambda :'', action='NoAction', src_zone='NoSourceZone',
                               dst_zone='NoDestinationZone', src_ip='NoSourceIP', dst_ip='NoDestinationIP')
    else:
        parse_rule(line, one_rule)



def parse_rule(line, one_rule):
    if line.startswith('action'):
        action = line.split(' ')[1]
        one_rule['action'] = action
    elif line.startswith('src-zone'):
        src_zone = line.split(' ')[1]
        one_rule['src_zone'] = src_zone.strip('"')
    elif line.startswith('dst-zone'):
        dst_zone = line.split(' ')[1]
        one_rule['dst_zone'] = dst_zone.strip('"')
    elif line.startswith('src-ip'):
        src_ip = line.split(' ')[1]
        one_rule['src_ip'] = src_ip
    elif line.startswith('dst-ip'):
        dst_ip = line.split(' ')[1]
        one_rule['dst_ip'] = dst_ip
    elif line.startswith('service'):
        service = line.split(' ')[1]
        if one_rule.has_key('service'):
            one_rule['service'].add(service.strip('"'))
        else:
            one_rule['service'] = set([service.strip('"')])


def output_format():
    with open('result.txt', 'w+') as f:
        f.writelines("%-16r%-16s%-18s%-22s%-26s%-26s%-28r\n"%('rule id', 'action', 'src-zone', 'dst-zone', 'src-ip', 'dst-ip', 'service'))
        global rule
        for k, vs in rule.items():
            first_print = None
            for v in vs:
                if not first_print:
                    f.writelines("%-16r%-16s%-18s%-22s%-26s%-26s%-28r\n"%(str(k), v['action'], v['src_zone'], v['dst_zone'], v['src_ip'], v['dst_ip'], list(v['service'])))
                else:
                    f.writelines("%-16r%-16s%-18s%-22s%-26s%-26s%-28r\n"%('', v['action'], v['src_zone'], v['dst_zone'], v['src_ip'], v['dst_ip'], list(v['service'])))


if __name__ == '__main__':
    main('rule.txt')
    