import subprocess

checkout_branch('develop', 'ezleague')

run_script('cd ezleague/client && npm install --legacy-peer-deps && npm run build')











