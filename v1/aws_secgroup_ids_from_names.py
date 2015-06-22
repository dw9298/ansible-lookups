# (c) 2015, Jon Hadfield <jon@lessknown.co.uk>
"""
Description: This lookup takes an AWS region and a list of one or more
security Group Names and returns a list of matching security Group IDs. 

Example Usage:
{{ lookup('aws_secgroup_ids_from_names', ('eu-west-1', ['nginx_group', 'mysql_group'])) }}
"""
from ansible import errors
try:
    import boto.ec2
except ImportError:
    raise errors.AnsibleError("aws_secgroup_ids_from_names lookup cannot be run without boto installed")

class LookupModule(object):
    def __init__(self, basedir=None, **kwargs):
	            self.basedir = basedir

    def run(self, terms, variables=None, **kwargs):
        if isinstance(terms, basestring):
            terms = [terms]
        sg_list = []
        region = terms[0]
        group_names = terms[1]
        conn = boto.ec2.connect_to_region(region)
        for group_name in group_names:
            filters = {'group_name': group_name}
            sg = conn.get_all_security_groups(filters=filters)
            if sg and sg[0]:
                sg_list.append(sg[0].id)
        return sg_list