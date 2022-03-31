import pexpect
from pexpect.popen_spawn import PopenSpawn
import re
import time

class pxpowershell(object):
    def __init__(self, *args, **kwargs):
        self.cmd = "powershell.exe"
        self.unique_prompt = "XYZPYEXPECTZYX"
        self.orig_prompt = ""
        self.process = ""
        
    def start_process(self):
        self.process =  pexpect.popen_spawn.PopenSpawn(self.cmd)
        time.sleep(2)
        init_banner = self.process.read_nonblocking(4096, 2)
        try:
            prompt = re.findall(b'PS [A-Z]:', init_banner, re.MULTILINE)[0]
        except Exception as e:
            raise (
                Exception("Unable to determine powershell prompt. {0}".format(e))
            ) from e

        self.process.sendline("Get-Content function:\prompt")
        self.process.expect(prompt)
        self.orig_prompt = self.process.before[32:]
        self.process.sendline('Function prompt{{"{0}"}}'.format(self.unique_prompt))
        self.process.expect(self.unique_prompt)
        self.process.expect(self.unique_prompt)
        
    def restore_prompt(self):
        self.process.sendline('Function prompt{{"{0}"}}'.format(self.orig_prompt))
    
    def run(self,pscommand):
        self.process.sendline(pscommand)
        self.process.expect(self.unique_prompt)
        print(self.process.before)
        return self.process.before[len(pscommand)+2:]
    
    def stop_process(self):
        self.process.kill(9)
        

def create_connection(ps, server_name, database_name = None):
    ps.run(f'$serverName = "{server_name}";')
    ps.run(f'$databaseName = "{database_name}";')
    ps.run('$svr = new-Object Microsoft.AnalysisServices.Tabular.Server')
    ps.run('$svr.Connect($serverName)')
    ps.run('$database = $svr.databases')
    if database_name:
        ps.run('$database = $database.GetByName({$databaseName})')
    else:
        db_name = ps.run("$svr.databases[0].name").decode('utf-8').strip()
        ps.run(f'$db = $database.GetByName("{db_name}")')
        
        
def create_measure(ps, name, expression, table, folder = None):
    ps.run(f'$table = $db.Model.Tables.Item("{table}")')
    ps.run('$measure = new-Object Microsoft.AnalysisServices.Tabular.Measure')
    ps.run(f'$measure.Name = "{name}"')
    ps.run(f'$measure.Expression = "{expression}"')
    if folder:
        ps.run(f'$measure.DisplayFolder = "{folder}"')
    ps.run('$table.Measures.Add($measure)')

server_name = "localhost:YOUR_PORT_HERE"

x = pxpowershell()
x.start_process()
x.run('[System.Reflection.Assembly]::LoadWithPartialName("Microsoft.AnalysisServices.Tabular")')
create_connection(x, server_name)
create_measure(x, "TestMeasure", "1+1", "Table Measures","TestFolder")
x.run("$db.Model.SaveChanges()")
x.stop_process()