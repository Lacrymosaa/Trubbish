# Trubbish
Trubbish é uma automação em Selenium que excluirá tweets da sua conta para você um a um. Você colocará seus dados e ele abrirá uma janela que executará a tarefa de excluir repetidamente até que não haja mais tweets.

# Problemas conhecidos
- Ele tem problemas com retweets, para lidar com isso e fazer os testes corretamente utilizei esse site para limpar os RTs da conta: https://tweethunter.io/unretweet
- O seu método de ignorar tweets de outras pessoas pode fazer ele ignorar alguns de seus tweets. Executa-lo novamente é uma solução. É possivel implementar um método de revisão para ele assim que ele terminar.
- Ele é naturalmente lento, já que excluirá um tweet de cada vez. Existe forma mais rápida de excluir todos os tweets (tweepy), mas aparentemente é necessário algum tipo de verificação para poder usar os métodos de exclusão de todos os tweets. Pensando nisso desenvolvi o Trubbish para lidar com a exclusão de contas com menos tweets.
