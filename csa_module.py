import xml.etree.ElementTree as ET
import copy

# from oslo.config import cfg
# from oslo_log import log as logging
# from nova import utils

# LOG = logging.getLogger(__name__)
# CONF = cfg.CONF

def make_input_xml(rt_vms, ifile, ofile):
#   out = utils.execute('pwd')
#   LOG.debug("output of pwd: %s", out);
 
#   tree = ET.parse('/var/run/nova/openstack_multilevel_EDF.xml')
#   root = tree.getroot()
#   LOG.debug("after tree.getroot()");

# # the XML template has the following structure
# # root    : <system > ... </system>
# # root[0] : <component name="comp1" scheduler="EDF" min_period="15" max_period="15">
# # root[0][0] : <task name="t1" p="300" d="300" e="100" cs="0"> </task>

# #
# # Here component corresponds to VM, and VM has only one task
# #  To add a component, use the following commands:
# #    t = copy.deepcopy(root[0])
# #    root.append(t)
# #  To change the 'name' of the new task
# #    root[1][0].attrib['name'] = 'new name'
# # 

  rt_vms = { 
   "uuid1": [["budget1", "budget2"],["period1", "period2"], ["deadline1", "deadline2"]],
   "uuid2": [["budget1", "budget2"],["period1", "period2"], ["deadline1", "deadline2"]]
  }
  if (len(rt_vms) > 1):
    ref_component = copy.deepcopy(root[0])
  # LOG.debug("make_input_xml: len(rt_vms) = %s\n", len(rt_vms))
  # LOG.debug("make_input_xml: rt_vms = %s\n", rt_vms)
  index = -1
  for uuid, value in rt_vms.iteritems(): # for each VM
    # LOG.debug("make_input_xml: VM: %s\n", uuid)
    # LOG.debug("make_input_xml: VM: %s\n", value)
    index = index + 1
    component = root[0]
    if (index > 0):
      component = copy.deepcopy(ref_component)
      root.append(component)
    component.attrib['name'] = uuid
    task = component[0]
    budget = value[0]
    period = value[1]
    deadline = value[2]
    for i, item in enumerate(budget):
      if (i > 0):
        task = copy.deepcopy(component[0])
        component.append(task)
      task.attrib['p'] = str(period[i])
      task.attrib['d'] = str(deadline[i])
      task.attrib['e'] = str(budget[i])
  ET.dump(root)

  tree.write(ifile)
# call CARTS
  # LOG.debug("call java")
  # out = utils.execute('java', '-jar', '/var/run/nova/Carts.jar', ifile, 'MPR', ofile)
  # # LOG.debug("output of Java: %s", out)

def read_output_xml(ofile):
  tree = ET.parse(ofile)
  root = tree.getroot()

# the XML template has the following structure
# root       : <component name="system" > ... </component>
# root[0]    : <resource> 
# root[0][0]   <model cpus="3" execution_time="3" period="1"> </model> 
#              ... </resource>
# root[1]    : <processed_task> ... </processed_task>
# root[2]    : <component > </component> 
# root[3]    : <component > </component> 

  total_num_cpus = int(root[0][0].attrib['cpus'])
  rt_vms = {}
  _t_num_cpus = 0
  LOG.debug("read_output_xml")
  for index, outer_item in enumerate(root):
    # outer_item 0: <Element 'resource'
    # outer_item 1: <Element 'processed_task'
    if (index < 2): continue
    # outer_item 2: component
    LOG.debug(" output xml - Component : %s", str(outer_item))
    LOG.debug(" output xml - resource: %s", str(outer_item[0]))
    my_rt_vm = {}
    my_rt_vm['name']   = outer_item.attrib['name']
    my_rt_vm['vcpus']   = int(outer_item[0][0].attrib['cpus'])
    _t_num_cpus = _t_num_cpus + my_rt_vm['vcpus']
    LOG.debug(" output xml - processed_task : %s", str(outer_item[1]))
    vcpu_list = outer_item[1] # processed_task
    if (my_rt_vm['vcpus'] != len(vcpu_list)):
      LOG.debug("vcpu # mismatch (%d) != (%d)", my_rt_vm['vcpus'], len(vcpu_list))
    period_list = []
    budget_list = []
    deadline_list = []
    for i, item in enumerate(vcpu_list):
      LOG.debug(" read_output_xml - i(%d), item(%s)", i, str(item))
      period_list.append(int(item.attrib['period']))
      budget_list.append(int(item.attrib['execution_time']))
      deadline_list.append(int(item.attrib['deadline']))
    my_rt_vm['rt_period'] = period_list 
    my_rt_vm['rt_budget'] = budget_list 
    my_rt_vm['rt_deadline'] = deadline_list 

    rt_vms[outer_item.attrib['name']] = my_rt_vm

  if (total_num_cpus != _t_num_cpus):
    LOG.debug(" WARNING: read_output_xml: total number of vcpus mismatch (%d) != (%d)", \
      total_num_cpus, _t_num_cpus) 
    LOG.debug(" WARNING: For now, we return the sum of vcpus (%d)", _t_num_cpus)
  LOG.debug(" read_output_xml - rt_vms : %s", str(rt_vms))
  return (_t_num_cpus, rt_vms)

#def get_vm_properties_xml2list(uuid, vms):
#  if uuid == 'all':
#     return True
#  for i, item in enumerate (vms):
#    if item['name'] == uuid:
    

# (1, 2, 3) --> [1, 2, 3]
#

def scheduler_hints_to_list (scheduler_hint_field):
  LOG.debug('H: scheduler_hint_field = %s', scheduler_hint_field)
  tmp = scheduler_hint_field.replace(" ", "").strip('"')
  r_list = map(str, tmp.strip("()").split(','))
  LOG.debug('H: to list = %s', str(r_list))
  return r_list

def rt_sanity_check(period_list, budget_list, deadline_list):
  # TODO
  return True
def hi():
  print 'sup'

hi()
rt_vms = { 
 "uuid1": [["budget1", "budget2"],["period1", "period2"], ["deadline1", "deadline2"]],
 "uuid2": [["budget1", "budget2"],["period1", "period2"], ["deadline1", "deadline2"]]
}

make_input_xml(rt_vms,'s','s')