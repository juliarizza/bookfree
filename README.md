# BookFree
O BookFree é uma aplicação web voltada para o empréstimo e controle de livros dos usuários. Nele, o usuário pode:
* Cadastrar todos os livros que possui ou que deseja adquirir
* Solicitar o empréstimo de livros de outros usuários, emprestar seus próprios livros e gerenciar todos os empréstimos por categorias como: tempo, conservação, proximidade, etc.
* Ser publicamente avaliado de acordo com os empréstimos realizados, criando boa reputação

Esta aplicação está em processo de desenvolvimento, para mais informações sobre suas funcionalidades acesse: http://sourceinnovation.com.br/wiki/BookFree (necessário cadastro)

## Instalação
Para instalar e executar, siga os seguintes passos:  

1. Clone o repositório

    ```
    $ git clone git@github.com:juliarizza/bookfree.git
    ```
    
2. Entre no repositório

    ```
    $ cd bookfree
    ```
    
3. Instale o `virtualenv`

    ```
    $ pip install virtualenv
    ```
    
4. Crie um novo `virtualenv`

    ```
    $ virtualenv -p python3 flask
    ```
    
5. Execute o `virtualenv`
 
    ```
    $ . flask/bin/activate
    ```
    
6. Instale as dependências
    
    ```
    $ flask/bin/pip3 install -r requirements.txt
    ```

6. Realiza as *migrations* do banco de dados

    ```
    $ python3 run.py db init
    $ python3 run.py db migrate
    $ python3 run.py db upgrade
    ```
    
7. Execute o programa

    ```
    $ python3 run.py runserver
    ```
    
8. Para parar a execução, basta pressionar CTRL+C
9. Para sair do `virtualenv`

    ```
    $ deactivate
    ```
    
