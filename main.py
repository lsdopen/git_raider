import yaml, json
import subprocess
from rich.console import Console
from rich.table import Column, Table

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
