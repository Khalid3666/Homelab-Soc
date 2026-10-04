# Wazuh Active response :

> <img src="../media/image8.png" style="width:6.26772in;height:6.06944in" />

Simulation de brute-force :

<img src="../media/image13.png" style="width:6.26772in;height:2.29167in" />

<img src="../media/image42.png" style="width:6.26772in;height:1.94444in" />

<img src="../media/image37.png" style="width:6.26772in;height:3.93056in" />

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

<img src="../media/image22.png" style="width:6.26772in;height:2.80556in" />

Malgré ca, je peux toujours essayer plusieurs mots de passes et la
policy ne s’active pas.

<img src="../media/image43.png" style="width:6.26772in;height:2.22222in" />

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

<img src="../media/image9.png" style="width:6.26772in;height:1.97222in" />

<img src="../media/image23.png" style="width:6.26772in;height:6.30556in" />

<img src="../media/image17.png" style="width:6.26772in;height:2.41667in" />

<img src="../media/image41.png" style="width:6.26772in;height:6.30556in" />

Essayons alors de tenter la même chose sur l’endpoint Ubuntu (IP :
192.168.115.3)

Il m’a fallu installer ssh et autoriser une connexion sur le port 22:

> sudo apt update
>
> sudo apt install ssh
>
> sudo ufw allow 22

<img src="../media/image2.png" style="width:6.26772in;height:1.72222in" />

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

<img src="../media/image12.png" style="width:6.26772in;height:2.97222in" />

<img src="../media/image33.png" style="width:6.92927in;height:1.15104in" />
