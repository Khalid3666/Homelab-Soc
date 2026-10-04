# Implémentation et configuration de OPNsense

<img src="../media/image1.png" style="width:6.18504in;height:3.45833in" />

<img src="../media/image40.png" style="width:6.18504in;height:3.40278in" />

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

<img src="../media/image27.png" style="width:6.18504in;height:3.13889in" />

<img src="../media/image3.png" style="width:6.18504in;height:6.70833in" />

<img src="../media/image29.png" style="width:6.18504in;height:5.23611in" />

Ressources :

- DevSecOps :

  - https://medium.com/@dinothunderkp/devsecops-complete-tutorial-c984acb9c7a7

- SOC

  - [<u>https://www.reddit.com/r/homelab/comments/1hoxlfl/if_you_had_to_build_a_cybersecurity_oriented/</u>](https://www.reddit.com/r/homelab/comments/1hoxlfl/if_you_had_to_build_a_cybersecurity_oriented/)

  - [<u>https://blog.ecapuano.com/p/so-you-want-to-be-a-soc-analyst-intro</u>](https://blog.ecapuano.com/p/so-you-want-to-be-a-soc-analyst-intro)

  - [<u>https://medium.com/@nakkouchtarek/from-zero-to-soc-homelab-my-journey-to-defense-in-depth-and-full-security-automation-cc07373b8b6d</u>](https://medium.com/@nakkouchtarek/from-zero-to-soc-homelab-my-journey-to-defense-in-depth-and-full-security-automation-cc07373b8b6d)

  - [<u>https://www.youtube.com/watch?v=eWQ99r4zZ-8</u>](https://www.youtube.com/watch?v=eWQ99r4zZ-8)

  - 
