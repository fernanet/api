document.addEventListener('DOMContentLoaded', () => {
  // Faz a tecla 'enter' submeter mensagem
  let msg = document.querySelector('#usuario_mensagem');
  msg.addEventListener('keyup', event => {
    event.preventDefault();
    if (event.keyCode === 13) {
      document.querySelector('#envia_mensagem').click();
    }
  })


})
