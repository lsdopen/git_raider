import yaml, json
import subprocess
from datetime import datetime
from rich.console import Console
from rich.table import Column, Table
from jinja2 import Template

config = yaml.safe_load(open('raider.yaml'))

seen = json.load(open('seen.json'))
current = []

for org in config['organizations']:
    subprocess.run(['./util/yar', '-C', 'util/yarconfig.json', '--noise', '10', '--include-members', '--skip-duplicates', '--save', 'tmp.json', '--no-cache', '--org', org], stdout=subprocess.DEVNULL)
    if this_run_secrets := json.load(open('tmp.json')):
        current += this_run_secrets

for user in config['users']:
    subprocess.run(['./util/yar', '-C', 'util/yarconfig.json', '--noise', '10', '--include-members', '--skip-duplicates', '--save', 'tmp.json', '--no-cache', '--user', user], stdout=subprocess.DEVNULL)
    if this_run_secrets := json.load(open('tmp.json')):
        current += this_run_secrets

for repo in config['repos']:
    subprocess.run(['./util/yar', '-C', 'util/yarconfig.json', '--noise', '10', '--include-members', '--skip-duplicates', '--save', 'tmp.json', '--no-cache', '--repo', repo], stdout=subprocess.DEVNULL)
    if this_run_secrets := json.load(open('tmp.json')):
        current += this_run_secrets

new = [secret for secret in current if secret not in seen]

seen = seen + current

with open('seen.json', 'w') as f:
    json.dump(seen, f)

# print a table with new entries
console = Console()
table = Table(show_header=True)
table.add_column("Commiter")
table.add_column("Reason")
table.add_column("Source")
table.add_column("Secret")

for secret in new:
    table.add_row(secret['Commiter'], 
                  secret["Reason"],
                  secret["Source"],
                  secret["Secret"]
                  )

console.print(table)

html_template = Template("""
                         <h1>{{date}}</h1>
                         <table style="width:100%">
                         <tr>
                             <th>Commiter</th>
                             <th>Reason</th>
                             <th>Repo</th>
                             <th>File</th>
                             <th>Commit</th>
                             <th>Secret</th>
                        </tr>
                        {% for secret in secrets %}
                        <tr>
                            <td>{{secret['Commiter']}}</td>
                            <td>{{secret['Reason']}}</td>
                            <td><a href="{{secret['RepoName']}}">{{secret['RepoName']}}</a></td>
                            <td>{{secret['Filepath']}}</td>
                            <td><a href="{{secret['Source']}}">{{secret['CommitHash']}}</a></td>
                            <td>{{secret['Secret']}}</td>
                        </tr>
                        {% endfor %}
                        </table>
                         """)

html_out = html_template.render(secrets=new, date=datetime.now().strftime("%F"))

with open("log.html", "a") as f:
    f.write(html_out)