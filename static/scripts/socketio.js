document.addEventListener('DOMContentLoaded', () => {

  // Conecta ao websocket
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  // Recupera nome do usuário
  const nomeusuario = document.querySelector('#recebe-nomeusuario').innerHTML;

  let room = "Sala";
  junteSala("Sala");

  // Exibe todas as mensagem recebida
  socket.on('mensagem', data => {

    // Exibe mensagem atualizada
    if (data.msg) {
      const p = document.createElement('p');
      const span_nomeusuario = document.createElement('span');
      const span_timestamp = document.createElement('span');
      const br = document.createElement('br');

      // Exibe a própria mensagem do usuário
      if (data.nomeusuario == nomeusuario) {
        p.setAttribute("classe", "minha-msg");

        // Nome do usuário
        span_nomeusuario.setAttribute("classe", "meu-nomeusuario");
        span_nomeusuario.innerText = data.nomeusuario;

        // Timestamp
        span_timestamp.setAttribute("classe", "timestamp");
        span_timestamp.innerText = data.time_stamp;

        // HTML para anexar
        p.innerHTML += span_nomeusuario.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML

        // Anexar
        document.querySelector('#secao-exibe-mensagem').append(p);
      }
      // Exibe outras mensagens de usuários
       else if (typeof data.nomeusuario !== 'undefined') {
        p.setAttribute("classe", "outras-msg");

        // Nome de usuário
        span_nomeusuario.setAttribute("classe", "outro-nomeusuario");
        span_nomeusuario.innerText = data.nomeusuario;

        // Timestamp
        span_timestamp.setAttribute("classe", "timestamp");
        span_timestamp.innerText = data.time_stamp;

        // HTML para anexar
        p.innerHTML += span_nomeusuario.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML

        // Anexar
        document.querySelector('#secao-exibe-mensagem').append(p);
      }
      // Exibe mensagens do sistema
      else {
        imprimeSysMsg(data.msg);
      }
    }
    scrollDownChatWindows();
  });

  socket.on('algum-evento', data => {
      console.log(data);
  });

  // Envia mensagem
  document.querySelector('#envia_mensagem').onclick = () => {
    socket.emit('msg-recebida', {'msg': document.querySelector('#usuario_mensagem').value, 'nomeusuario': nomeusuario, 'sala': room });
    // Limpa área de entrada
    document.querySelector('#usuario_mensagem').value = '';
  };

  // Seleciona uma sala
  document.querySelectorAll('.selecione-sala').forEach(p => {
    p.onclick = () => {
      let novaSala = p.innerHTML;
      // Verifica se usuário já está dentro da sala
      if (novaSala == room) {
        msg = `Você já está dentro da sala ${room}.`;
        imprimeSysMsg(msg);
      } else {
        deixeSala(room);
        junteSala(novaSala);
        room = novaSala;
      }
    };

  });

  // Efetua logout do chat
  document.querySelector("#botao-logout").onclick = () => {
    deixeSala(room);
  }

  // Função Deixe a sala' se o usuário estava previamente em uma sala
  function deixeSala(room) {
    socket.emit('deixou', {'nomeusuario': nomeusuario, 'sala': room});

    document.querySelectorAll('.selecione-sala').forEach(p => {
      p.style.color = "black";
    });
  }

  // Função 'Junte-se a sala'
  function junteSala(room) {

    // Junte-se a sala
    socket.emit('juntou-se', {'nomeusuario': nomeusuario, 'sala': room});

    // Destaca a sala selecionada
    document.querySelector('#' + CSS.escape(room)).style.color = "#ffc107";
    document.querySelector('#' + CSS.escape(room)).style.backgroundColor = "white";

    // Área para limpar Mensagem
    document.querySelector('#secao-exibe-mensagem').innerHTML = ''

    // Autofocus na caixa de texto
    document.querySelector('#usuario_mensagem').focus();
  }

  // Função que rola a janela do chat para baixo
  function scrollDownChatWindows() {
    const janelaChat = document.querySelector("#secao-exibe-mensagem");
    janelaChat.scrollTop = janelaChat.scrollHeight;
  }

  // Imprime mensagem do sistema
  function imprimeSysMsg(msg) {
    const p = document.createElement('p');
    p.setAttribute("classe", "sistema-msg");
    p.innerHTML = msg;
    document.querySelector('#secao-exibe-mensagem').append(p);
    scrollDownChatWindows();

    // Autofocus na caixa de texto
    document.querySelector("#usuario_mensagem").focus();
  }

});
