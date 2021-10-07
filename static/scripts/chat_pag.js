document.addEventListener('DOMContentLoaded', () => {

  // Faz a barra lateral recolher ao clicar
  document.querySelector('#exibe-botao-barralateral').onclick = () => {
    document.querySelector('#barralateral').classList.toggle('visualiza-barralateral')
  };

  // Faz a tecla 'enter' submeter mensagem
  let msg = document.querySelector('#usuario_mensagem');
  msg.addEventListener('keyup', function(event) => {
    event.preventDefault();
    if (event.keyCode === 13) {
      document.getElementById("envia_mensagem").click();
    }
  });
});
