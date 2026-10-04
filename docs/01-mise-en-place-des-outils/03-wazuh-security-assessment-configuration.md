# Wazuh Security Assessment configuration.

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

<img src="../media/image24.png" style="width:6.26772in;height:1.72222in" />

Dans mon cas, le scan a relevé un score de conformité de 48% avec 117
règles échouées. Le nom du benchmark appliqué est : CIS Ubuntu Linux
24.04 LTS Benchmark v1.0.0. Il s’agit d’un benchmark déjà embarqué par
défaut sur Wazuh (Tout les benchmark disponibles :
[<u>https://documentation.wazuh.com/current/user-manual/capabilities/sec-config-assessment/available-sca-policies.html</u>](https://documentation.wazuh.com/current/user-manual/capabilities/sec-config-assessment/available-sca-policies.html))
Allons plus loin en observant les informations fournies par Wazuh.

<img src="../media/image14.png" style="width:6.26772in;height:2.84722in" />

Prenons le premier test écouhé avec l’ID 35509. La sortie se divise en 5
parties majeures :

- **<u>Rationale :</u>** Explication détaillée du problème ainsi que le
  danger apporté par sa présence.

- **<u>Remediation :</u>** Wazuh nous propose des actions de
  remediations pour corriger le problème de configuration

- Description :

- Checks

- Compliance

<img src="../media/image28.png" style="width:6.26772in;height:2.47222in" />

<img src="../media/image5.png" style="width:3.91667in;height:7.20833in" />
