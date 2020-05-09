import ansible.
import json
runner = ansible.runner.Runner(
       module_name='ping',
       module_args='',
       pattern='all',
       forks=10
    )
datastructure = runner.run()
data = json.dumps(datastructure,indent=4)
print(data)