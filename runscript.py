import subprocess



def run_script(script):
    subprocess.call(script, shell=True)


run_script('cd ezleague/client && npm install --legacy-peer-deps && npm run build')











