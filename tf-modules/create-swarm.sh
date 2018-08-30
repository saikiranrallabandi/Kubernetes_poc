ANSIBLE_ROOT_LOC=$1
ANSIBLE_SWARM_INV_LOC=$2
#ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -b -i ${SWARM_INV_LOC}/swarm-inventory swarm.yml
ansible-playbook -b -i ${ANSIBLE_SWARM_INV_LOC}/swarm-inventory ${ANSIBLE_ROOT_LOC}/swarm.yml --private-key ~/.ssh/sigmaex2KeyPair.pem
