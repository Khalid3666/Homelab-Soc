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

> <img src="../media/image36.png" style="width:6.26772in;height:4.05556in" />
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
