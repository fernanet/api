document.addEventListener('DOMContentLoaded', () => {
  var socket = io.connect('http://' + document.domain + ':' + location.port);

  let room = "Sala";
  junteSala("Sala");

  // Exibe mensagem recebida
  socket.on('message', data => {
      const p = document.createElement('p');
      const span_nomeusuario = document.createElement('span');
      const span_timestamp = document.createElement('span');
      const br = document.createElement('br');

      if (data.nomeusuario) {
        span_nomeusuario.innerHTML = data.nomeusuario;
        span_timestamp.innerHTML = data.time_stamp;
        p.innerHTML = span_nomeusuario.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;
        document.querySelector('#secao-exibe-mensagem').append(p);
      } else {
        imprimeSysMsg(data.msg);
      }
  });

  socket.on('algum-evento', data => {
      console.log(data);
  });

  // Envia mensagem
  document.querySelector('#envia_mensagem').onclick = () => {
    socket.send({'msg': document.querySelector('#usuario_mensagem').value, 'nomeusuario': nomeusuario, 'sala': room });
    // Limpa área de entrada
    document.querySelector('#usuario_mensagem').value = '';
  }

  // Seleção de sala
  document.querySelectorAll('selecione-sala').forEach(p => {
    p.onclick = () => {
      let novaSala = p.innerHTML;
      if (novaSala == room) {
        msg = `Você já está dentro da sala ${room}.
        imprimeSysMsg(msg);
      } else {
        deixeSala(room);
        junteSala(novaSala);
        room = novaSala;
      }
    }

  });

  // Deixe a sala
  function deixeSala(room) {
    socket.emit('deixou', {'nomeusuario': nomeusuario, 'sala': room});
  }

  // Junte-se a sala
  function junteSala(room) {
    socket.emit('juntou-se', {'nomeusuario': nomeusuario, 'sala': room});
    // Área para limpar Mensagem
    document.querySelector('#secao-exibe-mensagem').innerHTML = ''

    // Autofocus na caixa de texto
    document.querySelector('#usuario_mensagem')
  }

  // Imprime mensagem do sistema
  function imprimeSysMsg(msg) {
    const p = document.createElement('p');
    p.innerHTML = msg;
    document.querySelector('#secao-exibe-mensagem').append(p);

  }

})
