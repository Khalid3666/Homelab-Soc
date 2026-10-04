Homelabs / Learning Paths :

1.  Soc : SIEM, EDR, NDR + Offensive machine to improve my offensive
    skills

2.  Cloud Security : Aws ?

3.  DevSecOps : CI/CD, pipelines, SAST/SCA tools…

4.  Architecture

5.  AI security ?

6.  Offensive :

    1.  Rootme

    2.  HackTheBox ?

    3.  CTF

Cloud Security :
[<u>https://medium.com/@ihor.sasovets/learning-path-for-cloud-security-specialists-73a09bc1db3b</u>](https://medium.com/@ihor.sasovets/learning-path-for-cloud-security-specialists-73a09bc1db3b)

Proxmox ? Ce revient souvent chez les gens pour les home labs et la
virtualisation

Ce qui pourrait être sympa :

- Attaquer mon SOC avec ma machine offensive

- Essayer de corriger ou supprimer les vecteurs d’attaques par lesquels
  j’ai réussi à attaquer la machine

- Déployer par exemple un Active Directory et essayer de le sécuriser
  tout en l’attaquant

- Déployer un appli web sur la machine, l’attaquer et peut-être même
  mettre en place des choses en lien avec le devsecops.

- <span class="mark">HONEYPOTS</span>

\
=

# Mise en place des outils de sécurité

Cette partie va principalement couvrir la mise en place des différents
composants nécessaires pour un home lab orienté SOC. Mon objectif est
double :

- Manipuler et implémenter les différents outils que l’on peut retrouver
  dans un environnement SOC

- Réfléchir, concevoir et organiser l’architecture IT d’un environnement
  simulant un cas réel avec : plusieurs workstations (OS différents),
  des assets vulnérables, des vulnérabilités et failles multiples et
  intentionnelles à corriger.

L’architecture visée à ce stade là est la suivante (évoluera au fil du
temps). L’idée est de me familiariser tout d’abord avec les différents
outils importants d’un point de vue architecture cyber. Pour démarrer,
voici les composants que je souhaite implémenter :

- **SIEM** avec splunk (ou Wazuh)

- **EDR** avec **Wazuh**

- **IDS/IPS** avec **Suricata** (ou Snort)

- Suite **SysInternals**

- **WAF** avec une application vulnérable

- Chaine **CI/CD** (**DevSecOps**, **SAST/SCA**)

- Scanner de vulnérbailités **OpenVAS**.

- Environnement **Active Directory**

- HoneyPot (Pas d’outil open source et gratuit en tête)

> <img src="./media/image36.png"
> style="width:6.26772in;height:4.05556in" />
>
> *Figure 1 : Architecture Cyber de l’environnement virtuel*

L’idée est également de diversifier les différentes workstations
présentes dans cet environnement virtuels afin de mettre la main sur des
distributions et OS variés. Le schéma d'architecture décrit 4 machines
pour l’instant.

- L’Endpoint Ubuntu sera le principal asset Linux de l’environnement et
  simulera un poste de travail classique. Des outils de sécurité
  pourront être installés dessus comme un firewall (pfSense) et un
  IDS/IPS (Suricatta) en plus de l’agent Wazuh.

- De l’autre côté, une machine très vulnérable comme metasploitable3 est
  une excellente opportunité de tester au maximum les capacités de l’EDR
  au vu des nombreuses vulnérabilités exploitables sur cette machine.

- Similaire à l’endpoint Ubuntu, une troisième machine tournant sous
  Windows 11 cette fois simulera un poste de travail Windows classique.
  Aucune mise à jour ne sera faite une fois l’installation lancée et
  cela pourra servir à tester de nouvelles vulnérabilités ou exploits
  publics qui existent déjà ou qui seront découverts dans le futur. Je
  réfléchis également à la possibilité d’intégrer un Active Directory
  dans cette machine pour étudier l'administration d’un AD mais surtout
  de compléter mes connaissances sur l’aspect offensive sur un AD

- Enfin, une dernière machine simulera un serveur hébergeant une
  application web vulnérable. L’objectif est de tester et mettre en
  place une approche DevSecOps ainsi qu’un Web Application Firewall
  (WAF) pour sécuriser le déploiement de l’application et garantir sa
  sécurité à travers outils de scan SAST/SCA. Wazuh possède un module
  similaire mais je compte explorer d’autres outils.

Ces 4 machines seront au sein du même sous-réseau pour commencer, cela
facilitera les différentes actions offensives pour tester les outils.
Par la suite, je considère l’implémentation d’une potentielle
segmentation réseau (dans la mesure du possible) pour davantage de
sécurité réseau.

Une machine kali linux sera utilisée pour effectuer des simulation
offensives sur cet environnement. Cela permettra de suivre en direct les
différentes réponses des composants implémenté (SIEM, EDR, Firewall,
IDS/IPS)

## Wazzuh main components : 

Tout d'abord, j'ai besoin de savoir de quoi est composé un SOC, quels
outils sont utilisés et comment ils sont connectés entre eux. Avant de
commencer à construire un SOC, j'ai besoin de concevoir et de dessiner
son architecture pour y voir plus clair. J'ai également besoin de
déterminer les ressources nécessaires pour faire tourner tout cela. Pour
l'instant, je prévois de commencer avec VirtualBox, mais je ne sais pas
si mon PC dispose de la RAM nécessaire pour faire fonctionner
l'ensemble..

J’ai choisi de faire tourner mon point central sur une VM Ubuntu en y
allouant les ressources minimum spécifiées dans la documentation
officielle. D’après mes recherches, Ubuntu est un OS idéal pour cette
tâche grâce à sa fluidité et flexibilité.

Pour le choix du SIEM, je vais choisir Wazzuh. Il s’agit d’un outil open
source, gratuit et simple à mettre en place. L’installation sera
effectuée en suivant la documentation officielle
(<https://documentation.wazuh.com/current/installation-guide/index.html>)
.

Puisque c’est la première fois que j’utilise Wazzuh, je me contenterais
d’installer la version rapide (Pas d’installation manuelle ou
personnaliser). Cette méthode installera les 3 composants majeures pour
Wazzuh en même temps :

- Wazzuh Indexer

- Wazzuh Serveur

- Wazzuh Dashboard

La commande suivante permet d’installer le script d’installation de
Wazzuh et de l’exécuter. Après quelques minutes, l’installation se
termine et j’ai accès au Wazzuh dashboard sur mon adresse locale en y
accédant par le port 443. Il serait peut être judicieux de changer le
port par défaut.

L’installation semble avoir créé un service pour Wazzuh qui se lance à
chaque démarrage, il n’est pas nécessaire de le créer manuellement.

curl -sO https://packages.wazuh.com/4.14/wazuh-install.sh && sudo bash
./wazuh-install.sh -a

<img src="./media/image21.png"
style="width:6.26772in;height:1.20833in" />

<img src="./media/image35.png"
style="width:6.26772in;height:3.54167in" />

***<u>Remarque :</u>** L’installation a planté la première fois que je
l’ai lancé. Un message d’erreur apparaissant sur le terminal lors de
l’installation du Wazzuh Dashboard sans donner de détails
supplémentaires. Les fichiers de logs ne m’ont pas apporté
d’informations particulieres pour m’aider à trouver le problème.
Cependant, j’ai remarqué que juste* avant *l’échec, mon OS me notifiait
que mon espace disque était faible. Il était donc facile de faire le
lien avec l’erreur précédente. Il se trouve que j’avais alloué 25 Gb
d’espace pour mon disque. J’ai dû alors allouer 80 Gb et ajuster la
taille de la partition directement avec Gparted.*

\
-

## Wazzuh Agents : 

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

<img src="./media/image6.png"
style="width:6.26772in;height:2.95833in" />

*Machine Main Wazuh*

<img src="./media/image26.png"
style="width:6.26772in;height:2.04167in" />

*Machine Endpoint*

Désormais, le Wazuh dashboard sera deployé sur l’adresse 192.168.115.4
sur le port 443. Depuis le dashboard, il est possible de déployer un
agent. Il faut spécifier l’OS ciblé, l’adresse du serveur, le nom de
l’agent et son groupe. Ensuite wazzuh nous génére une commande à
exécuter sur l’endpoint pour installer l’agent. Contrairement à
l’installation de Wazzuh, il est nécessaire de créer un service pour
lancer l’agent à chaque démarrage.

<img src="./media/image31.png"
style="width:6.26772in;height:4.95833in" />

*sudo curl -o wazuh-agent-4.14.4-1.x86_64.rpm
https://packages.wazuh.com/4.x/yum/wazuh-agent-4.14.4-1.x86_64.rpm &&
sudo WAZUH_MANAGER='192.168.115.4' WAZUH_AGENT_GROUP='default'
WAZUH_AGENT_NAME='EndPoint_Test' rpm -ihv
wazuh-agent-4.14.4-1.x86_64.rpm*

<img src="./media/image10.png" style="width:6.26772in;height:2.875in" />

Après l’exécution de cette commande, l’installation de l’agent semble
être terminée et l’agent est bien ajouté en tant que service. En
revenant sur la liste des agents, on peut voir notre agent
“EndPoint_test” apparaître avec un statut actif. En y accédant, on
retrouve un dashboard très détaillé sur différents aspects de sécurité
liés à la machine. Notre agent est donc bien fonctionnel et prêt à
l’emploi.

<img src="./media/image4.png"
style="width:6.26772in;height:2.06944in" />

<img src="./media/image15.png"
style="width:6.26772in;height:3.20833in" />

<img src="./media/image34.png"
style="width:6.26772in;height:3.20833in" />

<img src="./media/image32.png"
style="width:6.26772in;height:2.05556in" />

## Wazuh Security Assessment configuration. 

Il est désormais temps d’en apprendre plus sur les différentes
fonctionnalités de Wazzuh, à commencer par le Security assessment
configuration. Ce module scan le système sur lequel l’agent est installé
pour s’assurer qu’il est conforme à un set de réglages prédéfinis
concernant la configuration/paramètres. Cela permet de repérer les
potentiels problèmes et faiblesses au niveau des configuration de
l’endpoint et d’ainsi réduire la surface d’attaque.

Le point fort de ce module est sa capacité à fournir des recommandations
si un test échoue. Prenant un exemple tiré d’un scan de mon endpoint
Ubuntu. L’agent va accéder à la configuration de l’endpoint et utiliser
des fichiers de policy qui contiennent les règles qui devront être
testées sur la configuration de l’endpoint. Cela peut être :

- Existence d’un fichier

- Existence d’un répertoire

- Existence d’une clé de registres

- Process en cours

- Test récursif pour trouver des fichiers au seins des répertoires.

<img src="./media/image24.png"
style="width:6.26772in;height:1.72222in" />

Dans mon cas, le scan a relevé un score de conformité de 48% avec 117
règles échouées. Le nom du benchmark appliqué est : CIS Ubuntu Linux
24.04 LTS Benchmark v1.0.0. Il s’agit d’un benchmark déjà embarqué par
défaut sur Wazuh (Tout les benchmark disponibles :
[<u>https://documentation.wazuh.com/current/user-manual/capabilities/sec-config-assessment/available-sca-policies.html</u>](https://documentation.wazuh.com/current/user-manual/capabilities/sec-config-assessment/available-sca-policies.html))
Allons plus loin en observant les informations fournies par Wazuh.

<img src="./media/image14.png"
style="width:6.26772in;height:2.84722in" />

Prenons le premier test écouhé avec l’ID 35509. La sortie se divise en 5
parties majeures :

- **<u>Rationale :</u>** Explication détaillée du problème ainsi que le
  danger apporté par sa présence.

- **<u>Remediation :</u>** Wazuh nous propose des actions de
  remediations pour corriger le problème de configuration

- Description :

- Checks

- Compliance

<img src="./media/image28.png"
style="width:6.26772in;height:2.47222in" />

<img src="./media/image5.png"
style="width:3.91667in;height:7.20833in" />

## Wazuh Active response : 

> <img src="./media/image8.png"
> style="width:6.26772in;height:6.06944in" />

Simulation de brute-force :

<img src="./media/image13.png"
style="width:6.26772in;height:2.29167in" />

<img src="./media/image42.png"
style="width:6.26772in;height:1.94444in" />

<img src="./media/image37.png"
style="width:6.26772in;height:3.93056in" />

Voyons voir la différence si on ajoute de l’active response. Est ce que
hydra va tt de même marcher ?

On ajoute la config suivante dans le fichier de config :

\<ossec_config\>

\<active-response\>

\<disabled\>no\</disabled\>

\<command\>firewall-drop\</command\>

\<location\>local\</location\>

\<rules_id\>60122\</rules_id\>

\<timeout\>90\</timeout\>

\</active-response\>

\</ossec_config\>

Ce que ca fait c’est que ca va chercher une régle avec son id et
lorsqu’elle sera detecté, l’adresse ip sera ajoutée avec une consigne
drop sur le firewall. Ici la régle que j’ai spécifié est lié aux alertes
que wazzuh a remonté lors des tentatives de brute-force avec hydra. On
restart le service Wazuh manager pour que ces nouvelles modifications
soient prises en compte.

<img src="./media/image22.png"
style="width:6.26772in;height:2.80556in" />

Malgré ca, je peux toujours essayer plusieurs mots de passes et la
policy ne s’active pas.

<img src="./media/image43.png"
style="width:6.26772in;height:2.22222in" />

En fouillant dans la documentation officiel, j’apprend que wazuh et
embarqué avec des actives responses par défaut. De mon côté, j’ai
utilise firewall-drop comme active response dans ma configuration sauf
qu’elle est marqué comme spécifique à Linux et macOs. Je dois donc la
modifier par l’active-reponse **netsh.exe**

Après une nouvelle tentative de brute-force en ayant changé l’active
responses, les événements de sécurité montrent que l’active-response a
bien été déclenché. Pourtant, je ne suis pas bloque sur ma machine Kali
et je peux continuer à brute-force en boucle. C’est tout bête, c’est
simplement car le firewall windows est desactivé sur la metasploitable3.
Je vais garder ça comme ça, mais je constate tout de même que l’active
response c’est activé, donc c’est bon signe.

<img src="./media/image9.png"
style="width:6.26772in;height:1.97222in" />

<img src="./media/image23.png"
style="width:6.26772in;height:6.30556in" />

<img src="./media/image17.png"
style="width:6.26772in;height:2.41667in" />

<img src="./media/image41.png"
style="width:6.26772in;height:6.30556in" />

Essayons alors de tenter la même chose sur l’endpoint Ubuntu (IP :
192.168.115.3)

Il m’a fallu installer ssh et autoriser une connexion sur le port 22:

> sudo apt update
>
> sudo apt install ssh
>
> sudo ufw allow 22

<img src="./media/image2.png"
style="width:6.26772in;height:1.72222in" />

On voit un nouvel événement signalant une connexion ssh échouée. Suivant
la même logique qu’avant en ajoutant l’active response firewall-drop
avec ce ruleID.

\<active-response\>

\<disabled\>no\</disabled\>

\<command\>firewall-drop\</command\>

\<location\>local\</location\>

\<rules_id\>5760\</rules_id\>

\<timeout\>90\</timeout\>

\</active-response\>

l’active response fonctionne bien et aucune connexion ne peut être
établie après un echec d’authentification.

<img src="./media/image12.png"
style="width:6.26772in;height:2.97222in" />

<img src="./media/image33.png"
style="width:6.92927in;height:1.15104in" />

## Implémentation de Suricata

Les fonctionnalités de base de monitoring réseau offertes par Wazuh sont
satisfaisantes. Il serait cependant intéressant d’ajouter à nos
différents postes de travail un IDS/IPS. Il s’agit de sondes réseaux de
sécurité permet d’analyser les paquets qui passent par notre réseau. Il
existe deux types de sondes : IDS et IPS.

Un IDS (Intrusion Detection System) analyse les paquets et alerte
l’administrateur en cas de comportement suspect sans influer ou agir sur
le trafic et généralement en amont du pare-feu. Les IDS sont placés en
dehors du flux de trafic principal. Ils fonctionnent généralement en
mettant en miroir le trafic pour évaluer les menaces, ce qui permet de
préserver les performances du réseau en analysant un flux de données
dupliqué. Cette configuration permet à l'IDS de rester un observateur
non perturbateur.
([<u>https://www.paloaltonetworks.fr/cyberpedia/firewall-vs-ids-vs-ips#ids</u>](https://www.paloaltonetworks.fr/cyberpedia/firewall-vs-ids-vs-ips#ids))

Les systèmes IDS se présentent sous différentes formes : système de
détection des intrusions par le réseau (NIDS), système de détection des
intrusions par l'hôte (HIDS), système basé sur le protocole (PIDS),
système basé sur le protocole d'application (APIDS) et système hybride.
Il existe également un sous-groupe de méthodes de détection IDS. Les
deux variantes les plus courantes sont les IDS basés sur les signatures
et les IDS basés sur les anomalies.
([<u>https://www.paloaltonetworks.fr/cyberpedia/firewall-vs-ids-vs-ips#ids</u>](https://www.paloaltonetworks.fr/cyberpedia/firewall-vs-ids-vs-ips#ids))

De l’autre côté un IPS (Intrusion Prevention System) effectue la même
tâche mais peut cependant agir lorsqu’une activité suspecte est détectée
afin de bloquer la menace Contrairement à un IDS, un IPS est placé après
une pare-feu et analyse le réseau de façon dynamique. Il examine les
données entrantes et prend des mesures automatisées si nécessaire. Les
systèmes IPS peuvent signaler des alertes, rejeter les données
nuisibles, bloquer les adresses sources et réinitialiser les connexions
afin d'empêcher d'autres attaques. Ils sont particulièrement efficace
pour bloquer les vulnérabilités réseaux (quelques milisecondes)
([<u>https://www.paloaltonetworks.fr/cyberpedia/firewall-vs-ids-vs-ips#ids</u>](https://www.paloaltonetworks.fr/cyberpedia/firewall-vs-ids-vs-ips#ids))

Pour minimiser les faux positifs, les systèmes IPS font la différence
entre les menaces authentiques et les données bénignes. Les systèmes de
prévention des intrusions y parviennent en utilisant diverses
techniques, notamment la détection basée sur les signatures, qui
s'appuie sur des modèles connus d'exploits, la détection basée sur les
anomalies, qui compare l'activité du réseau à des lignes de base
établies, et la détection basée sur les politiques, qui applique des
règles de sécurité spécifiques configurées par les administrateurs. Ces
méthodes garantissent que seul l'accès autorisé est permis.
([<u>https://www.paloaltonetworks.fr/cyberpedia/firewall-vs-ids-vs-ips#ids</u>](https://www.paloaltonetworks.fr/cyberpedia/firewall-vs-ids-vs-ips#ids))

Nous allons utiliser un IDS/IPS opensource dans notre environnement
nommé Suricata qui pourra être directement lié à notre EDR afin de
centraliser les logs généré par l’IDS/IPS.

Nous avons allons installé Suricata en suivante la proof of concept
suivante rédigé par Wazuh :
[<u>https://documentation.wazuh.com/current/proof-of-concept-guide/integrate-network-ids-suricata.html</u>](https://documentation.wazuh.com/current/proof-of-concept-guide/integrate-network-ids-suricata.html)

Ensuite, nous allons prendre en main l’outil en se basant sur la
documentation officielle :
https://docs.suricata.io/en/suricata-8.0.4/security.html

<img src="./media/image39.png"
style="width:6.42188in;height:2.61477in" />

*Reference :
https://documentation.wazuh.com/current/user-manual/capabilities/active-response/ar-use-cases/blocking-ssh-brute-force.html*

J’ai également suivi les recommandations de la section *5.Security
Configurations* de la documentation officielle afin que Suricata tourne
sous un utilisateur autre que root après le démarrage. Suricata a
cependant besoin des privilèges *root* au démarrage, mais ces derniers
seront délaissés une fois démarré.

<img src="./media/image38.png"
style="width:5.70833in;height:1.16667in" />

Afin de tester les capacités de détection de suricata dans son état
actuel, j’ai utilisé l’outil de reconnaissance ***nmap*** sur ma machine
Kali. Il semblerait que Suricata ait bien détecté cette phase de
reconnaissance ainsi que l’usage de cet outil. Une autre information
intéressante : Une alerte a été remonté dû à la présence du nom Kali
dans les headers d’un paquet. Cela permet de facilement identifier une
machine extérieur à son environnement et la déclarer comme malveillante,
d’autant plus qu’il s’agit d’une Kali.

<img src="./media/image19.png"
style="width:7.18229in;height:2.70444in" />

<img src="./media/image25.png"
style="width:6.26772in;height:0.76389in" />

Par la suite, j’ai enchainé avec un brute-force Hydra encore une fois
pour vérifier si l’active-response fonctionne encore et surtout si
Suricata peut détecter quelque chose. Après la fin de la phase de
brute-force, des logs intéressants apparaissent sur Wazuh :

- L’active response fonctionne bien, mais pour rappel, il ne s’agit que
  d’un time-out. Notre machine d’attaque n’est bloquée que pendant 5
  minutes à la suite du brute-force et elle parvient tout de même à
  trouver le mot de passe. C’est un problème.

- Wazuh détecte les tentatives de connexion qui ont échoué dans un
  intervalle de temps très court : **PAM: Multiple failed logins in a
  small period of time.**

- Wazuh détecte qu’une tentative de connexion a réussi à la suite de
  plusieurs échecs : **Multiple authentication failures followed by a
  success.**

- Wazuh réagit à la tentative de brute-force, en plus de nous fournir
  l’adresse IP exacte dont provient la tentative **: sshd: brute force
  trying to get access to the system. Authentication failed.**

<img src="./media/image7.png"
style="width:6.26772in;height:5.13889in" />

Cependant, aucune trace de logs de la part de suricata. J’ai trouvé la
ressource suivante sur internet sur laquelle je vais possiblement
m’appuyer pour créer une régle de réponse à ce cas d’usage :
https://medium.com/@dinothunderkp/cybersecurity-solution-siem-open-source-wazuh-and-suricata-5ab047b96ca5

<img src="./media/image20.png"
style="width:6.26772in;height:3.31944in" />

<img src="./media/image30.png"
style="width:6.26772in;height:2.27778in" /><img src="./media/image18.png"
style="width:6.26772in;height:3.09722in" />

<img src="./media/image11.png"
style="width:6.26772in;height:3.58333in" />

<img src="./media/image16.png"
style="width:6.26772in;height:3.61111in" />

## Implémentation et configuration de OPNsense

<img src="./media/image1.png"
style="width:6.18504in;height:3.45833in" />

<img src="./media/image40.png"
style="width:6.18504in;height:3.40278in" />

La connexion à l’interface ne fonctionnait pas avec l’IP de base
([<u>https://192.168.1.1</u>](https://192.168.1.1)). J’ai alors défini
une nouvelle adresse pour l’interface LAN, ce qui a réglé le problème.
Je peux désormais accéder à l’interface depuis l’adresse
[<u>https://192.168.115.12</u>](https://192.168.115.12) avec le compte
root et le mot de passe par défaut, j’ai changé le mot de passe par
mesure de sécurité. L’interface utilisateur ne peut être accéder que
depuis le réseau LAN (192.168.1.1). Cependant, il est possible de
l’administrer avec l’adresse WAN en désactivant le firewall avec la
commande pfctl -d.

https://www.it-connect.fr/tuto-installer-et-configurer-opnsense/

<img src="./media/image27.png"
style="width:6.18504in;height:3.13889in" />

<img src="./media/image3.png"
style="width:6.18504in;height:6.70833in" />

<img src="./media/image29.png"
style="width:6.18504in;height:5.23611in" />

Ressources :

- DevSecOps :

  - https://medium.com/@dinothunderkp/devsecops-complete-tutorial-c984acb9c7a7

- SOC

  - [<u>https://www.reddit.com/r/homelab/comments/1hoxlfl/if_you_had_to_build_a_cybersecurity_oriented/</u>](https://www.reddit.com/r/homelab/comments/1hoxlfl/if_you_had_to_build_a_cybersecurity_oriented/)

  - [<u>https://blog.ecapuano.com/p/so-you-want-to-be-a-soc-analyst-intro</u>](https://blog.ecapuano.com/p/so-you-want-to-be-a-soc-analyst-intro)

  - [<u>https://medium.com/@nakkouchtarek/from-zero-to-soc-homelab-my-journey-to-defense-in-depth-and-full-security-automation-cc07373b8b6d</u>](https://medium.com/@nakkouchtarek/from-zero-to-soc-homelab-my-journey-to-defense-in-depth-and-full-security-automation-cc07373b8b6d)

  - [<u>https://www.youtube.com/watch?v=eWQ99r4zZ-8</u>](https://www.youtube.com/watch?v=eWQ99r4zZ-8)

  - 
