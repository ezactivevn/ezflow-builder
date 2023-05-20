import subprocess

def clone_repository(repo_url, destination_path):
    subprocess.run(['git', 'clone', repo_url, destination_path])

def checkout_branch(branch_name, repo_path):
    subprocess.run(['git', 'checkout', branch_name], cwd=repo_path)

def pull_repository(repo_path):
    subprocess.run(['git', 'pull'], cwd=repo_path)

def run_script(script_path):
    subprocess.run(script_path, shell=True)

clone_repository('http://github.com/ezactivevn/ezleague.git', 'ezleague')

checkout_branch('develop', 'ezleague')

run_script('cd ezleague/client && npm install --legacy-peer-deps && npm run build')






