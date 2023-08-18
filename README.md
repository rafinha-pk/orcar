# Orcar - Um gerador de Orçamento em Django

Esse projeto foi criado principalmente para testas as funcionalidades do Django, é meu segundo projeto em Python/Django (o primeiro foi o ToDoo do tutorial) e não havia pretenções em sua criação, mas o resultado final ficou tão interessante que achei melhor por aqui para consultas futuras.


## ✔️ Técnicas e tecnologias utilizadas

- ``Python 3.10.12``
- ``Django 4.1.7``
- ``Bootstrap 5.3.0``
- ``jquery/ajax 3.7.0``
- ``Mysql 8.0.34``

## Instalação:

Instalar Python 3.10.12, Django 4.1.7 e Mysql 8.0.34, o Jquery e o Bootstrap já estão incorporado no código já na versão correta.
É necessario realizar alguns registros no Mysql para o funcionamento inicial do Orcar,esses registros devem ser importados depois das migrations, o aqrquivo .sql se encontra no diretorio /mysql/

### Avisos!
Esse projeto não foi feito para produção pois se trata de um "projeto laboratório", existem diferentes abordagens para os mesmos problemas (como o uso de "listas" e "chave estrangeira" para situações similares com o intuito de coompreender seus funcionamentos), não possui uma revisão voltada para a segurança, alem de ter parte de seus forms expostos (com finalidade de testes).
