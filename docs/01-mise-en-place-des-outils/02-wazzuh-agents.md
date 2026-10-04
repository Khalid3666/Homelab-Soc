# Wazzuh Agents :

Maintenant que Wazzuh est bien fonctionnel sur notre unité principale,
il est temps de commencer à deployer des agents sur les endpoints qu’on
souhaite protéger. Un agent wazzuh a pour rôle de communiquer entre
l’endpoint et le manager wazzuh manager à qui il va transmettre des
données à travers un canal crypté et authentifié. Cette fonctionnalité a
été conçu avec comme objectif de permettre le monitoring de plusieurs
endpoints sans impacter leurs performances.

Un agent wazzuh possède des fonctionnalités clés qui sont :

- Log collector

- Command execution

- File integrity monitoring (FIM)

- Security configuration assessment (SCA)

- System inventory

- Malware detection

- Active Response

- Container security

- Cloud security

Avant de continuer, il est nécessaire de faire des ajustements sur les
configurations réseaux des machines virtuelles. Actuellement, j’utilise
une deuxième machine ubuntu qui servira de premier endpoint de test pour
essayer de deployer un agent dessus. Cependant pour que cela fonctionne,
il faut que les deux machines soient sous le même sous-réseau pour
permettre à l’agent de communiquer avec le wazzuh manager. Pour cela, la
configuration réseau des deux machines est définie à “Réseau Interne”.
Pour la navigation sur internet, l’objectif est de se servir de la
machine hébergeant le firewall OPNsense comme gateway principale.

<img src="../media/image6.png" style="width:6.26772in;height:2.95833in" />

*Machine Main Wazuh*

<img src="../media/image26.png" style="width:6.26772in;height:2.04167in" />

*Machine Endpoint*

Désormais, le Wazuh dashboard sera deployé sur l’adresse 192.168.115.4
sur le port 443. Depuis le dashboard, il est possible de déployer un
agent. Il faut spécifier l’OS ciblé, l’adresse du serveur, le nom de
l’agent et son groupe. Ensuite wazzuh nous génére une commande à
exécuter sur l’endpoint pour installer l’agent. Contrairement à
l’installation de Wazzuh, il est nécessaire de créer un service pour
lancer l’agent à chaque démarrage.

<img src="../media/image31.png" style="width:6.26772in;height:4.95833in" />

*sudo curl -o wazuh-agent-4.14.4-1.x86_64.rpm
https://packages.wazuh.com/4.x/yum/wazuh-agent-4.14.4-1.x86_64.rpm &&
sudo WAZUH_MANAGER='192.168.115.4' WAZUH_AGENT_GROUP='default'
WAZUH_AGENT_NAME='EndPoint_Test' rpm -ihv
wazuh-agent-4.14.4-1.x86_64.rpm*

<img src="../media/image10.png" style="width:6.26772in;height:2.875in" />

Après l’exécution de cette commande, l’installation de l’agent semble
être terminée et l’agent est bien ajouté en tant que service. En
revenant sur la liste des agents, on peut voir notre agent
“EndPoint_test” apparaître avec un statut actif. En y accédant, on
retrouve un dashboard très détaillé sur différents aspects de sécurité
liés à la machine. Notre agent est donc bien fonctionnel et prêt à
l’emploi.

<img src="../media/image4.png" style="width:6.26772in;height:2.06944in" />

<img src="../media/image15.png" style="width:6.26772in;height:3.20833in" />

<img src="../media/image34.png" style="width:6.26772in;height:3.20833in" />

<img src="../media/image32.png" style="width:6.26772in;height:2.05556in" />
