instale o python na sua máquina
para iniciar o projeto será necessário criar e inicar uma nova venv (virtual environment) através do comando "python -m venv venv" e "venv/scripts/activate"
com a venv iniciada, rodar o comando "pip instal -r requirements.txt" para  que as bibliotecas sejam todas instaladas
com tudo pronto, instale o banco de dados postgresql e crie um banco de dados chamado "team_management"
o usuários "postgres" do banco de dados deve ter a senha "4C3SS0vv" para que o django possa criar a comunicação
rode o comando "python manage.py migrate" para criar o banco de dados e "python manage.py runserver" para iniciar o servidor de desenvolviemnto django
rode o comando "python manage.py createsuperuser" e siga os passos para criar um usuário super para o sistema
após esses passos, abra um cliente web e use o link "http://127.0.0.1:8000/" para acessar o servidor na sua máquina
log na plataforma com o seu login criado e estará tudo pronto para usar a plataforma
