# Script of topics I want to cover in the group meeting

## Avoid having to type your password accessing della by ssh or vscode

- Show ssh login from my local to della
  - Maybe also mention using alias in local bashrc
- Show vscode remote accessing della
- Mention Jon Halverson's repository for tips and tricks

## Mental model of Della compute and file-systems

- Show a figure of laptop, login-node, vis-node,
  mydella, compute nodes etc. RC already has a pretty nice figure
- Time how long copy within /projects and /scratch and between
- Show that you can ssh into a compute job iff you have a
  job running on it (like ssh rb3242@della-r3c4n16)
- Compute nodes do NOT have internet access

## Della job monitoring

- qstat alias to view more columns
- Jobstats of a running job
- seff of a finished job (also sent in emails)
- reportseff for an array of jobs
- Show starting an interactive job (sinteractive)
- Job start estimate with `squeue --start $JOBID`
- Della queues are based on job time and memory and 
  has different limits (qos | vi -) or on della help-page

## Della quota and storage management

- checkquota (and where it is on mydella website)
- akey_quotas alias (and jupyter notebook?)

## Tmux

- always be tmuxing! share a link to a help page
- can get lots of value using just a few commands 
- cd into the examples/tmux and go through the notes



